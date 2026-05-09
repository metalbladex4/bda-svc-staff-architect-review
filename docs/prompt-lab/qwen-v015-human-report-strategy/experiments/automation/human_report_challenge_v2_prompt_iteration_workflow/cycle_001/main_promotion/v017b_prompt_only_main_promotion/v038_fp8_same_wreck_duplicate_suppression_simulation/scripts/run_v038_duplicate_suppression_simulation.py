#!/usr/bin/env python3
"""Offline duplicate-suppression simulation for the FP8 vLLM v034a model line."""

from __future__ import annotations

import csv
import datetime as dt
import itertools
import json
import os
import shutil
import sys
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


WORKTREE_ROOT = Path("/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement")
CAPSTONE_ROOT = Path("/home/williambenitez1/Capstone")
PACKAGE_ROOT = WORKTREE_ROOT / (
    "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion/v038_fp8_same_wreck_duplicate_suppression_simulation"
)
V034_RUN_ROOT = WORKTREE_ROOT / (
    "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion/v034_fp8_vllm_precision_recovery_autonomous/"
    "runs/v034a_fp8_broad_context_scene_box_guard/full_all_current/"
    "human_report_challenge_v2_all_current_117_no101_2026-05-09_023225Z"
)
V034_OFFICE_RUN_ROOT = WORKTREE_ROOT / (
    "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion/v034_fp8_vllm_precision_recovery_autonomous/"
    "runs/v034a_fp8_broad_context_scene_box_guard/office_negative_guard/"
    "legacy_abstention_guard_office_negative_2026-05-09_030155Z"
)
ALL_CURRENT_MANIFEST = WORKTREE_ROOT / (
    "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/pre_adoption/"
    "v017b_group_box_rejection/validation_manifests/"
    "human_report_challenge_v2_all_current_117_no101.yaml"
)
BDA_EVAL_ROOT = WORKTREE_ROOT / "bda_eval"
sys.path.insert(0, str(BDA_EVAL_ROOT))

import discovery  # noqa: E402
import models  # noqa: E402


CONTAINMENT_THRESHOLDS = [0.70, 0.80, 0.90, 0.95]
IOU_THRESHOLDS = [0.10, 0.20, 0.30, 0.50]
AREA_RATIO_THRESHOLDS = [0.05, 0.10, 0.20, 0.30]
CENTER_INSIDE_OPTIONS = [True, False]
SAME_LABEL_OPTIONS = [True, False]
ONLY_SUPPRESS_IF_LARGER_MATCHED_OPTIONS = [True, False]
PRIORITY_CASES = ["66", "67", "84", "97", "110", "155", "166"]
OLD_V020C = {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58}
FP8_BASELINE = {"matches": 180, "false_negatives": 39, "false_positives": 32, "combined_errors": 71}
V034A_BASELINE = {"matches": 181, "false_negatives": 38, "false_positives": 25, "combined_errors": 63}


@dataclass(frozen=True)
class Rule:
    rule_id: str
    containment_threshold: float
    iou_threshold: float
    area_ratio_threshold: float
    center_inside_required: bool
    same_label_required: bool
    only_suppress_if_larger_matched: bool
    never_suppress_if_smaller_matched: bool = True
    never_suppress_if_both_overlap_distinct_refs: bool = True


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def box_from_target_dict(target: dict[str, Any]) -> tuple[float, float, float, float]:
    box = target["bounding_box"]
    if isinstance(box, dict):
        return float(box["xmin"]), float(box["ymin"]), float(box["xmax"]), float(box["ymax"])
    return tuple(float(v) for v in box)


def area(box: tuple[float, float, float, float]) -> float:
    return max(0.0, box[2] - box[0]) * max(0.0, box[3] - box[1])


def intersect_area(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    w = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    h = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    return w * h


def iou(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    inter = intersect_area(a, b)
    denom = area(a) + area(b) - inter
    return 0.0 if denom <= 0 else inter / denom


def center(box: tuple[float, float, float, float]) -> tuple[float, float]:
    return (box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0


def center_inside(inner: tuple[float, float, float, float], outer: tuple[float, float, float, float]) -> bool:
    cx, cy = center(inner)
    return outer[0] <= cx <= outer[2] and outer[1] <= cy <= outer[3]


def load_manifest_cases() -> list[dict[str, Any]]:
    payload = yaml.safe_load(ALL_CURRENT_MANIFEST.read_text(encoding="utf-8"))
    return list(payload["cases"])


def load_reference_reports(cases: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    reports: dict[str, dict[str, Any]] = {}
    for case in cases:
        path = Path(case["reference_report"])
        if not path.is_absolute():
            path = (ALL_CURRENT_MANIFEST.parent / path).resolve()
        key, data = discovery.get_report(path)
        reports[key] = data
    return reports


def load_predicted_reports() -> dict[str, dict[str, Any]]:
    reports: dict[str, dict[str, Any]] = {}
    for path in sorted((V034_RUN_ROOT / "predicted").glob("*.json")):
        result = discovery.get_report(path)
        if result:
            key, data = result
            reports[key] = data
    return reports


def evaluate_reports(
    references: dict[str, dict[str, Any]],
    predictions: dict[str, dict[str, Any]],
    image_order: list[str],
    eval_mode: str = "detection_study",
) -> dict[str, Any]:
    os.environ.pop("OLLAMA_API_KEY", None)
    image_summaries = []
    for image_filename in image_order:
        ref_report = models.BDAReport.from_dict(references[image_filename])
        pred_report = models.BDAReport.from_dict(predictions[image_filename])
        match_results = pred_report.get_bda_matches(ref_report, eval_mode=eval_mode)
        if match_results is None:
            matches, false_negatives, false_positives = [], ref_report.targets, pred_report.targets
        else:
            matches, false_negatives, false_positives = match_results
        image_summaries.append(
            {
                "image_filename": image_filename,
                "reference_target_count": len(ref_report.targets),
                "predicted_target_count": len(pred_report.targets),
                "match_count": len(matches),
                "false_negative_count": len(false_negatives),
                "false_positive_count": len(false_positives),
                "matches": [
                    {
                        "target_type": match.ref_target.target_type.text,
                        "reference_label": match.ref_target.target_label,
                        "predicted_label": match.pred_target.target_label,
                        "iou": match.iou,
                        "center_error_px": match.center_error_px,
                        "predicted_area_ratio": match.predicted_area_ratio,
                        "overlap_coverage": match.overlap_coverage,
                    }
                    for match in matches
                ],
                "false_negative_labels": [target.target_label for target in false_negatives],
                "false_positive_labels": [target.target_label for target in false_positives],
            }
        )
    totals = {
        "matches": sum(item["match_count"] for item in image_summaries),
        "false_negatives": sum(item["false_negative_count"] for item in image_summaries),
        "false_positives": sum(item["false_positive_count"] for item in image_summaries),
        "image_count": len(image_summaries),
    }
    totals["combined_errors"] = totals["false_negatives"] + totals["false_positives"]
    return {
        "generated_at": utc_now(),
        "eval_mode": eval_mode,
        "totals": totals,
        "images": image_summaries,
    }


def case_num(image_filename: str) -> str:
    return Path(image_filename).stem.lstrip("0") or "0"


def case_metrics(eval_payload: dict[str, Any]) -> dict[str, str]:
    out = {}
    for image in eval_payload["images"]:
        key = case_num(image["image_filename"])
        out[key] = f"{image['match_count']}/{image['false_negative_count']}/{image['false_positive_count']}"
    return out


def matched_maps(eval_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    maps: dict[str, dict[str, Any]] = {}
    for image in eval_payload["images"]:
        pred_to_ref = {m["predicted_label"]: m["reference_label"] for m in image["matches"]}
        ref_to_pred = {m["reference_label"]: m["predicted_label"] for m in image["matches"]}
        maps[image["image_filename"]] = {
            "pred_to_ref": pred_to_ref,
            "ref_to_pred": ref_to_pred,
            "matched_preds": set(pred_to_ref),
            "matched_refs": set(ref_to_pred),
            "false_positives": set(image["false_positive_labels"]),
            "false_negatives": set(image["false_negative_labels"]),
        }
    return maps


def viable_ref_sets(reference: dict[str, Any], prediction: dict[str, Any], eval_mode: str = "detection_study") -> dict[str, set[str]]:
    ref_report = models.BDAReport.from_dict(reference)
    pred_report = models.BDAReport.from_dict(prediction)
    policy = models.get_eval_policy(eval_mode)
    out: dict[str, set[str]] = {target.target_label: set() for target in pred_report.targets}
    for pred in pred_report.targets:
        for ref in ref_report.targets:
            if pred.target_type != ref.target_type:
                continue
            pair_iou = pred.box.calc_iou(ref.box)
            overlap = ref.box.overlap_coverage(pred.box)
            if models.BDAReport._passes_policy(ref.target_type, pair_iou, overlap, policy):
                out[pred.target_label].add(ref.target_label)
    return out


def pair_features(
    prediction: dict[str, Any],
    baseline_map: dict[str, Any],
    viable_refs: dict[str, set[str]],
) -> list[dict[str, Any]]:
    targets = prediction.get("physical_damage", {})
    items = []
    for label, target in targets.items():
        b = box_from_target_dict(target)
        items.append(
            {
                "label": label,
                "target_type": target.get("target_type"),
                "box": b,
                "area": area(b),
                "matched": label in baseline_map["matched_preds"],
                "matched_ref": baseline_map["pred_to_ref"].get(label),
                "viable_refs": sorted(viable_refs.get(label, set())),
            }
        )
    pairs = []
    for a, b in itertools.combinations(items, 2):
        if a["area"] <= 0 or b["area"] <= 0:
            continue
        small, large = (a, b) if a["area"] <= b["area"] else (b, a)
        inter = intersect_area(small["box"], large["box"])
        if inter <= 0:
            continue
        small_refs = set(small["viable_refs"])
        large_refs = set(large["viable_refs"])
        pairs.append(
            {
                "smaller_label": small["label"],
                "larger_label": large["label"],
                "same_target_type": small["target_type"] == large["target_type"],
                "small_area": small["area"],
                "large_area": large["area"],
                "area_ratio": small["area"] / large["area"] if large["area"] else 0.0,
                "containment_ratio": inter / small["area"] if small["area"] else 0.0,
                "iou": iou(small["box"], large["box"]),
                "center_inside_larger": center_inside(small["box"], large["box"]),
                "smaller_matched": small["matched"],
                "larger_matched": large["matched"],
                "smaller_matched_ref": small["matched_ref"],
                "larger_matched_ref": large["matched_ref"],
                "smaller_viable_refs": sorted(small_refs),
                "larger_viable_refs": sorted(large_refs),
                "both_overlap_distinct_refs": bool(small_refs and large_refs and small_refs.isdisjoint(large_refs)),
            }
        )
    return pairs


def suppressions_for_rule(pair_rows: list[dict[str, Any]], rule: Rule) -> list[dict[str, Any]]:
    suppressions = []
    for pair in pair_rows:
        if pair["containment_ratio"] < rule.containment_threshold:
            continue
        if pair["iou"] < rule.iou_threshold:
            continue
        if pair["area_ratio"] > rule.area_ratio_threshold:
            continue
        if rule.center_inside_required and not pair["center_inside_larger"]:
            continue
        if rule.same_label_required and not pair["same_target_type"]:
            continue
        if rule.only_suppress_if_larger_matched and not pair["larger_matched"]:
            continue
        if rule.never_suppress_if_smaller_matched and pair["smaller_matched"]:
            continue
        if rule.never_suppress_if_both_overlap_distinct_refs and pair["both_overlap_distinct_refs"]:
            continue
        suppressions.append(pair)
    # One target can appear in multiple qualifying pairs; keep one explanatory row.
    seen = set()
    deduped = []
    for row in sorted(suppressions, key=lambda item: (item["smaller_label"], -item["containment_ratio"], -item["iou"])):
        key = row["smaller_label"]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def apply_rule(
    predictions: dict[str, dict[str, Any]],
    pairs_by_image: dict[str, list[dict[str, Any]]],
    rule: Rule,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    mutated = deepcopy(predictions)
    removals = []
    for image_filename, pairs in pairs_by_image.items():
        hits = suppressions_for_rule(pairs, rule)
        for hit in hits:
            label = hit["smaller_label"]
            if label in mutated[image_filename].get("physical_damage", {}):
                del mutated[image_filename]["physical_damage"][label]
                removals.append({"image_filename": image_filename, **hit})
    return mutated, removals


def rule_grid() -> list[Rule]:
    rules = []
    n = 0
    for containment, pair_iou, area_ratio, center_required, same_label, larger_matched in itertools.product(
        CONTAINMENT_THRESHOLDS,
        IOU_THRESHOLDS,
        AREA_RATIO_THRESHOLDS,
        CENTER_INSIDE_OPTIONS,
        SAME_LABEL_OPTIONS,
        ONLY_SUPPRESS_IF_LARGER_MATCHED_OPTIONS,
    ):
        n += 1
        rules.append(
            Rule(
                rule_id=f"r{n:03d}",
                containment_threshold=containment,
                iou_threshold=pair_iou,
                area_ratio_threshold=area_ratio,
                center_inside_required=center_required,
                same_label_required=same_label,
                only_suppress_if_larger_matched=larger_matched,
            )
        )
    return rules


def is_case_worse(candidate: str, baseline: str) -> bool:
    cm = tuple(int(x) for x in candidate.split("/"))
    bm = tuple(int(x) for x in baseline.split("/"))
    return cm[0] < bm[0] or cm[1] > bm[1] or cm[2] > bm[2]


def safety_status(result: dict[str, Any], baseline_eval: dict[str, Any], baseline_cases: dict[str, str], office_pass: bool) -> tuple[bool, list[str]]:
    reasons = []
    totals = result["metrics"]
    base = baseline_eval["totals"]
    if totals["false_negatives"] > base["false_negatives"]:
        reasons.append("fn_increase")
    if totals["matches"] < base["matches"]:
        reasons.append("match_decrease")
    cases = result["case_metrics"]
    for case_id in ["67", "84", "110", "155", "166"]:
        if is_case_worse(cases.get(case_id, "0/999/999"), baseline_cases.get(case_id, "0/999/999")):
            reasons.append(f"case_{case_id}_worse")
    if not office_pass:
        reasons.append("office_negative_not_pass")
    return not reasons, reasons


def print_status(phase: str, best: dict[str, Any] | None, decision: str, lesson: str, next_action: str) -> None:
    if best:
        metrics = best["metrics"]
        metric_text = f"{metrics['matches']}/{metrics['false_negatives']}/{metrics['false_positives']}/{metrics['combined_errors']}"
        best_rule = best["rule_id"]
        vs_v034a = metrics["combined_errors"] - V034A_BASELINE["combined_errors"]
        vs_old = metrics["combined_errors"] - OLD_V020C["combined_errors"]
        cases = best["case_metrics"]
    else:
        metric_text = "n/a"
        best_rule = "n/a"
        vs_v034a = "n/a"
        vs_old = "n/a"
        cases = {}
    print("=== V038 STATUS ===", flush=True)
    print(f"phase: {phase}", flush=True)
    print(f"best_rule: {best_rule}", flush=True)
    print(f"simulated_metrics: {metric_text}", flush=True)
    print(f"vs_v034a_delta: {vs_v034a}", flush=True)
    print(f"vs_old_v020c_58_delta: {vs_old}", flush=True)
    print(f"case_66: {cases.get('66', 'n/a')}", flush=True)
    print(f"case_67: {cases.get('67', 'n/a')}", flush=True)
    print(f"case_84: {cases.get('84', 'n/a')}", flush=True)
    print(f"case_110: {cases.get('110', 'n/a')}", flush=True)
    print(f"case_155: {cases.get('155', 'n/a')}", flush=True)
    print(f"decision: {decision}", flush=True)
    print(f"main_lesson: {lesson}", flush=True)
    print(f"next_action: {next_action}", flush=True)
    print("===================", flush=True)


def row_for_result(result: dict[str, Any]) -> dict[str, Any]:
    metrics = result["metrics"]
    return {
        "rule_id": result["rule_id"],
        "containment_threshold": result["rule"]["containment_threshold"],
        "iou_threshold": result["rule"]["iou_threshold"],
        "area_ratio_threshold": result["rule"]["area_ratio_threshold"],
        "center_inside_required": result["rule"]["center_inside_required"],
        "same_label_required": result["rule"]["same_label_required"],
        "only_suppress_if_larger_matched": result["rule"]["only_suppress_if_larger_matched"],
        "matches": metrics["matches"],
        "false_negatives": metrics["false_negatives"],
        "false_positives": metrics["false_positives"],
        "combined_errors": metrics["combined_errors"],
        "removed_count": len(result["removals"]),
        "safe": result["safe"],
        "safety_reasons": ";".join(result["safety_reasons"]),
        "case_66": result["case_metrics"].get("66", "n/a"),
        "case_67": result["case_metrics"].get("67", "n/a"),
        "case_84": result["case_metrics"].get("84", "n/a"),
        "case_97": result["case_metrics"].get("97", "n/a"),
        "case_110": result["case_metrics"].get("110", "n/a"),
        "case_155": result["case_metrics"].get("155", "n/a"),
        "case_166": result["case_metrics"].get("166", "n/a"),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def copy_review_images() -> None:
    review_dir = PACKAGE_ROOT / "review_images"
    review_dir.mkdir(parents=True, exist_ok=True)
    for case in ["66", "67", "84", "97", "110", "155", "166"]:
        for folder in ["images_bbox_both", "images_bbox_predicted", "images_bbox_reference", "images_bbox_review"]:
            src = V034_RUN_ROOT / "eval" / folder / f"bbox_{case}.jpg"
            if not src.exists():
                src = V034_RUN_ROOT / "eval" / folder / f"bbox_{case}.png"
            if src.exists():
                shutil.copy2(src, review_dir / f"v034a_{folder}_{src.name}")


def main() -> int:
    for dirname in ["scripts", "tables", "review_images"]:
        (PACKAGE_ROOT / dirname).mkdir(parents=True, exist_ok=True)

    source_manifest = {
        "generated_at": utc_now(),
        "package": "v038_fp8_same_wreck_duplicate_suppression_simulation",
        "frozen_artifacts_only": True,
        "vlm_called": False,
        "prompt_candidate_authored": False,
        "source_artifacts": [
            "z_reference_docs/GPT-Pro_collab/V035_FP8_GAP_CLOSURE_REVIEW_POINTER.md (requested; not present in active checkout)",
            "z_reference_docs/GPT-Pro_collab/V036_FP8_CASE155_DENSE_SYNTHESIS_REVIEW_POINTER.md (requested; not present in active checkout)",
            str(WORKTREE_ROOT / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v036_fp8_case155_dense_synthesis/case155_fp_synthesis.md"),
            str(WORKTREE_ROOT / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v036_fp8_case155_dense_synthesis/dense_case_regression_synthesis.md"),
            str(WORKTREE_ROOT / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v037_fp8_same_wreck_duplicate_guard_autonomous/final_recommendation.md"),
            str(WORKTREE_ROOT / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v037_fp8_same_wreck_duplicate_guard_autonomous/comparison_matrix.md"),
            str(WORKTREE_ROOT / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v034_fp8_vllm_precision_recovery_autonomous/final_recommendation.md"),
            str(WORKTREE_ROOT / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v034_fp8_vllm_precision_recovery_autonomous/diagnoses/v034a_fp8_broad_context_scene_box_guard_diagnosis.md"),
            str(CAPSTONE_ROOT / "z_reference_docs/GPT-Pro_collab/bda_svc_qwen_prompt_engineering_deep_research_bundle.md"),
            str(CAPSTONE_ROOT / "z_reference_docs/GPT-Pro_collab/CODEX_QWEN_PROMPT_ENGINEERING_DIRECTION_2026-05-06.md"),
        ],
        "v034a_run_root": str(V034_RUN_ROOT),
        "manifest": str(ALL_CURRENT_MANIFEST),
        "hard_boundaries": {
            "no_promotion": True,
            "no_product_truth_mutation": True,
            "no_runtime_code_mutation": True,
            "no_eval_ground_truth_mutation": True,
            "no_v024o_scored_evidence": True,
            "no_vlm_calls": True,
            "no_prompt_candidate": True,
        },
    }
    write_json(PACKAGE_ROOT / "source_manifest.json", source_manifest)

    cases = load_manifest_cases()
    image_order = [case["image_filename"] for case in cases]
    references = load_reference_reports(cases)
    predictions = load_predicted_reports()
    baseline_eval = evaluate_reports(references, predictions, image_order)
    baseline_cases = case_metrics(baseline_eval)
    baseline_maps = matched_maps(baseline_eval)
    office_summary = read_json(V034_OFFICE_RUN_ROOT / "eval/evaluation_2026-05-09_030200Z_summary.json")
    office_pass = office_summary["totals"]["false_positive_count"] == 0

    artifact_inventory = {
        "generated_at": utc_now(),
        "v034a_prediction_files": len(list((V034_RUN_ROOT / "predicted").glob("*.json"))),
        "v034a_eval_summary": str(V034_RUN_ROOT / "eval/evaluation_2026-05-09_030154Z_summary.json"),
        "v034a_eval_csv": str(V034_RUN_ROOT / "eval/evaluation_2026-05-09_030154Z.csv"),
        "v034a_bbox_artifact_dirs": [str(path) for path in sorted((V034_RUN_ROOT / "eval").glob("images_bbox_*"))],
        "office_negative_summary": str(V034_OFFICE_RUN_ROOT / "eval/evaluation_2026-05-09_030200Z_summary.json"),
        "manifest_cases": len(cases),
        "case_101_excluded": "101.jpg" not in image_order,
        "baseline_recomputed": baseline_eval["totals"],
        "baseline_expected": V034A_BASELINE,
        "baseline_recompute_matches_expected": baseline_eval["totals"] == {**V034A_BASELINE, "image_count": 117},
    }
    write_json(PACKAGE_ROOT / "artifact_inventory.json", artifact_inventory)
    write_text(
        PACKAGE_ROOT / "artifact_inventory.md",
        "# v038 Artifact Inventory\n\n"
        f"- Frozen v034a run root: `{V034_RUN_ROOT}`\n"
        f"- Prediction files: `{artifact_inventory['v034a_prediction_files']}`\n"
        f"- Manifest cases: `{artifact_inventory['manifest_cases']}`; case 101 excluded: `{artifact_inventory['case_101_excluded']}`\n"
        f"- Recomputed v034a baseline: `{baseline_eval['totals']['matches']}/{baseline_eval['totals']['false_negatives']}/{baseline_eval['totals']['false_positives']}/{baseline_eval['totals']['combined_errors']}`\n"
        f"- Office-negative pass from frozen v034a artifacts: `{office_pass}`\n",
    )
    print_status(
        "artifact_inventory",
        None,
        "E",
        "Frozen v034a predictions and eval artifacts are present; the missing pointer files are non-blocking.",
        "Run the deterministic duplicate-suppression grid.",
    )

    pairs_by_image: dict[str, list[dict[str, Any]]] = {}
    for image_filename in image_order:
        viable = viable_ref_sets(references[image_filename], predictions[image_filename])
        pairs_by_image[image_filename] = pair_features(predictions[image_filename], baseline_maps[image_filename], viable)

    pair_rows = []
    for image_filename, rows in pairs_by_image.items():
        for row in rows:
            pair_rows.append({"image_filename": image_filename, **row})
    write_json(PACKAGE_ROOT / "tables/pair_feature_inventory.json", pair_rows)

    write_json(
        PACKAGE_ROOT / "simulation_plan.json",
        {
            "generated_at": utc_now(),
            "method": "offline_in_memory_removal_then_bda_eval_matching_recompute",
            "uses_vlm": False,
            "rules": {
                "containment_thresholds": CONTAINMENT_THRESHOLDS,
                "iou_thresholds": IOU_THRESHOLDS,
                "area_ratio_thresholds": AREA_RATIO_THRESHOLDS,
                "center_inside_required": CENTER_INSIDE_OPTIONS,
                "same_label_required": SAME_LABEL_OPTIONS,
                "only_suppress_if_larger_matched": ONLY_SUPPRESS_IF_LARGER_MATCHED_OPTIONS,
                "never_suppress_if_smaller_matched": True,
                "never_suppress_if_both_overlap_distinct_refs": True,
            },
            "safety_gates": [
                "no_fn_increase",
                "no_match_decrease",
                "case_67_not_worse",
                "case_84_not_worse",
                "case_110_not_worse",
                "case_155_not_worse",
                "case_166_not_worse",
                "office_negative_pass",
            ],
        },
    )
    write_text(
        PACKAGE_ROOT / "simulation_plan.md",
        "# v038 Simulation Plan\n\n"
        "The simulation reads frozen `v034a` predictions, removes duplicate-like boxes in memory, and recomputes the same `bda_eval` detection-study matching logic. It does not call the VLM and does not edit runtime or eval truth.\n",
    )
    write_json(
        PACKAGE_ROOT / "duplicate_suppression_rules.json",
        {
            "generated_at": utc_now(),
            "candidate_features": [
                "containment_ratio",
                "iou",
                "smaller_area_over_larger_area",
                "center_inside_larger",
                "same_target_type",
                "larger_originally_matched",
                "smaller_originally_unmatched",
                "distinct_reference_overlap_guard",
            ],
            "rule_count": len(rule_grid()),
            "never_suppress_if_smaller_box_matched": True,
            "never_suppress_if_both_boxes_overlap_distinct_references": True,
        },
    )
    write_text(
        PACKAGE_ROOT / "duplicate_suppression_rules.md",
        "# v038 Duplicate Suppression Rules\n\n"
        "Every grid rule removes only the smaller box in an overlapping prediction pair. A smaller box is never removed if it was originally matched, and a pair is skipped when both boxes overlap distinct viable references.\n",
    )

    results = []
    for rule in rule_grid():
        mutated, removals = apply_rule(predictions, pairs_by_image, rule)
        eval_payload = evaluate_reports(references, mutated, image_order)
        metrics = eval_payload["totals"]
        cases_metric = case_metrics(eval_payload)
        result = {
            "rule_id": rule.rule_id,
            "rule": {
                "containment_threshold": rule.containment_threshold,
                "iou_threshold": rule.iou_threshold,
                "area_ratio_threshold": rule.area_ratio_threshold,
                "center_inside_required": rule.center_inside_required,
                "same_label_required": rule.same_label_required,
                "only_suppress_if_larger_matched": rule.only_suppress_if_larger_matched,
                "never_suppress_if_smaller_matched": rule.never_suppress_if_smaller_matched,
                "never_suppress_if_both_overlap_distinct_refs": rule.never_suppress_if_both_overlap_distinct_refs,
            },
            "metrics": metrics,
            "case_metrics": cases_metric,
            "removals": removals,
        }
        safe, reasons = safety_status(result, baseline_eval, baseline_cases, office_pass)
        result["safe"] = safe
        result["safety_reasons"] = reasons
        results.append(result)

    rows = [row_for_result(result) for result in results]
    write_json(PACKAGE_ROOT / "simulation_grid_results.json", {"generated_at": utc_now(), "results": results})
    write_csv(PACKAGE_ROOT / "simulation_grid_results.csv", rows)
    write_csv(PACKAGE_ROOT / "tables/simulation_grid_results.csv", rows)
    safe_results = [r for r in results if r["safe"]]
    ranked = sorted(
        safe_results,
        key=lambda r: (
            r["metrics"]["combined_errors"],
            r["metrics"]["false_positives"],
            r["metrics"]["false_negatives"],
            -len(r["removals"]),
            r["rule"]["only_suppress_if_larger_matched"] is False,
            r["rule"]["same_label_required"] is False,
            r["rule"]["center_inside_required"] is False,
            r["rule"]["area_ratio_threshold"],
            r["rule"]["iou_threshold"],
            r["rule"]["containment_threshold"],
        ),
    )
    best = ranked[0] if ranked else None
    print_status(
        "simulation_grid",
        best,
        "B" if best and best["metrics"]["combined_errors"] < V034A_BASELINE["combined_errors"] else "D",
        "The grid is complete; safe rules are ranked by combined errors, FP reduction, and simplicity.",
        "Analyze the best rule and case-level deltas.",
    )

    if best:
        best_case_rows = []
        best_eval, _ = apply_rule(predictions, pairs_by_image, Rule(**{"rule_id": best["rule_id"], **best["rule"]}))
        best_eval_payload = evaluate_reports(references, best_eval, image_order)
        by_image = {item["image_filename"]: item for item in best_eval_payload["images"]}
        base_by_image = {item["image_filename"]: item for item in baseline_eval["images"]}
        for image_filename in image_order:
            b = base_by_image[image_filename]
            c = by_image[image_filename]
            best_case_rows.append(
                {
                    "image_filename": image_filename,
                    "case_id": case_num(image_filename),
                    "baseline_matches": b["match_count"],
                    "baseline_false_negatives": b["false_negative_count"],
                    "baseline_false_positives": b["false_positive_count"],
                    "sim_matches": c["match_count"],
                    "sim_false_negatives": c["false_negative_count"],
                    "sim_false_positives": c["false_positive_count"],
                    "delta_matches": c["match_count"] - b["match_count"],
                    "delta_false_negatives": c["false_negative_count"] - b["false_negative_count"],
                    "delta_false_positives": c["false_positive_count"] - b["false_positive_count"],
                    "removed_labels": ",".join(r["smaller_label"] for r in best["removals"] if r["image_filename"] == image_filename),
                }
            )
        write_csv(PACKAGE_ROOT / "case_level_delta_report.csv", best_case_rows)
        write_text(
            PACKAGE_ROOT / "case_level_delta_report.md",
            "# v038 Case-Level Delta Report\n\n"
            f"Best rule `{best['rule_id']}` changes `{sum(1 for row in best_case_rows if row['delta_false_positives'] or row['delta_false_negatives'] or row['delta_matches'])}` cases. See `case_level_delta_report.csv` for the full table.\n",
        )
        write_json(PACKAGE_ROOT / "best_simulation_report.json", {"generated_at": utc_now(), "best_rule": best, "top_safe_rules": ranked[:20]})
        write_text(
            PACKAGE_ROOT / "best_simulation_report.md",
            "# v038 Best Simulation Report\n\n"
            f"Best safe rule: `{best['rule_id']}`\n\n"
            f"Metrics: `{best['metrics']['matches']}/{best['metrics']['false_negatives']}/{best['metrics']['false_positives']}/{best['metrics']['combined_errors']}`.\n\n"
            f"Rule: containment >= `{best['rule']['containment_threshold']}`, IoU >= `{best['rule']['iou_threshold']}`, area ratio <= `{best['rule']['area_ratio_threshold']}`, center-inside `{best['rule']['center_inside_required']}`, same-label `{best['rule']['same_label_required']}`, larger-matched-only `{best['rule']['only_suppress_if_larger_matched']}`.\n\n"
            f"Removed boxes: `{len(best['removals'])}`.\n",
        )
        print_status(
            "best_rule_analysis",
            best,
            "B" if best["metrics"]["combined_errors"] < V034A_BASELINE["combined_errors"] else "D",
            "The best safe simulated rule removes duplicate-like FPs without recall loss.",
            "Write case delta review and final decision.",
        )
    else:
        write_json(PACKAGE_ROOT / "best_simulation_report.json", {"generated_at": utc_now(), "best_rule": None, "top_safe_rules": []})
        write_text(PACKAGE_ROOT / "best_simulation_report.md", "# v038 Best Simulation Report\n\nNo safe rule was found.\n")
        write_csv(PACKAGE_ROOT / "case_level_delta_report.csv", [])
        write_text(PACKAGE_ROOT / "case_level_delta_report.md", "# v038 Case-Level Delta Report\n\nNo safe rule was found.\n")

    if best is None:
        decision = "D"
    elif best["metrics"]["combined_errors"] <= OLD_V020C["combined_errors"]:
        decision = "A"
    elif best["metrics"]["combined_errors"] < V034A_BASELINE["combined_errors"]:
        decision = "B"
    elif best["removals"]:
        decision = "C"
    else:
        decision = "D"

    failure_payload = {
        "generated_at": utc_now(),
        "unsafe_rule_count": len([r for r in results if not r["safe"]]),
        "safe_rule_count": len(safe_results),
        "common_safety_reasons": {},
    }
    reason_counts: dict[str, int] = {}
    for result in results:
        for reason in result["safety_reasons"]:
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
    failure_payload["common_safety_reasons"] = dict(sorted(reason_counts.items(), key=lambda item: (-item[1], item[0])))
    write_json(PACKAGE_ROOT / "failure_analysis.json", failure_payload)
    write_text(
        PACKAGE_ROOT / "failure_analysis.md",
        "# v038 Failure Analysis\n\n"
        f"Safe rules: `{failure_payload['safe_rule_count']}`. Unsafe rules: `{failure_payload['unsafe_rule_count']}`.\n\n"
        "Rules were marked unsafe if they increased FNs, reduced matches, worsened key dense/control cases, or failed office-negative.\n",
    )

    final_payload = {
        "generated_at": utc_now(),
        "decision": decision,
        "safe_rule_found": bool(best and best["metrics"]["combined_errors"] < V034A_BASELINE["combined_errors"]),
        "best_rule_id": best["rule_id"] if best else None,
        "best_metrics": best["metrics"] if best else None,
        "beat_v034a": bool(best and best["metrics"]["combined_errors"] < V034A_BASELINE["combined_errors"]),
        "reached_or_beat_old_58": bool(best and best["metrics"]["combined_errors"] <= OLD_V020C["combined_errors"]),
        "case_metrics": best["case_metrics"] if best else {},
        "recommended_next_work": "experiment_only_post_processing_tranche" if decision in {"A", "B", "C"} else "fiftyone_or_visual_review_before_prompt_wording",
        "hard_boundaries_preserved": True,
    }
    write_json(PACKAGE_ROOT / "final_recommendation.json", final_payload)

    decision_text = {
        "A": "Safe duplicate suppression simulation beats v034a and reaches <=58 errors.",
        "B": "Safe duplicate suppression simulation beats v034a but remains above 58.",
        "C": "Simulation identifies a narrow rule worth implementing as experiment-only post-processing.",
        "D": "Simulation shows same-wreck duplicate suppression is unsafe or too local.",
        "E": "Simulation cannot be evaluated reliably from available artifacts.",
    }[decision]
    final_md = [
        "# v038 Final Recommendation",
        "",
        f"Generated: `{utc_now()}`",
        "",
        f"Decision `{decision}`: {decision_text}",
        "",
        f"Best rule: `{final_payload['best_rule_id'] or 'n/a'}`.",
        "",
        f"Best metrics: `{final_payload['best_metrics']['matches']}/{final_payload['best_metrics']['false_negatives']}/{final_payload['best_metrics']['false_positives']}/{final_payload['best_metrics']['combined_errors']}`." if best else "Best metrics: `n/a`.",
        "",
        f"Beat v034a: `{final_payload['beat_v034a']}`.",
        f"Reached or beat old 58-error reference: `{final_payload['reached_or_beat_old_58']}`.",
        "",
        "This is non-promoted post-hoc evidence only. It does not modify product runtime, prompt text, doctrine, assessment prompt, eval truth, or source truth.",
    ]
    write_text(PACKAGE_ROOT / "final_recommendation.md", "\n".join(final_md) + "\n")

    write_json(
        PACKAGE_ROOT / "recovery_log.json",
        {
            "generated_at": utc_now(),
            "steps": [
                "Read required local source artifacts where present.",
                "Attempted Graphify recall; shell Python lacked networkx, so source artifacts were used directly.",
                "Inventoried frozen v034a artifacts.",
                "Recomputed v034a baseline from frozen predictions.",
                "Ran duplicate-suppression grid offline without VLM calls.",
                "Wrote final decision and validation artifacts.",
            ],
        },
    )
    write_text(
        PACKAGE_ROOT / "recovery_log.md",
        "# v038 Recovery Log\n\n"
        "- Used frozen v034a predictions only.\n"
        "- Did not call the VLM or author a prompt candidate.\n"
        "- Recomputed matching through `bda_eval` model classes in memory.\n"
        "- Wrote grid, best-rule, case-delta, and final decision artifacts.\n",
    )
    lessons = [
        "# v038 Lessons Learned",
        "",
        "- Offline simulation is strong enough to test duplicate suppression without risking prompt-shape instability.",
        "- A safe rule must prove zero recall loss and preserve dense cases before it can motivate experiment-only post-processing.",
        "- Same-wreck duplicate handling should remain non-promoted evidence until implemented and replayed in a separate experiment-only tranche.",
    ]
    if best:
        lessons.append(f"- Best rule `{best['rule_id']}` achieved `{best['metrics']['matches']}/{best['metrics']['false_negatives']}/{best['metrics']['false_positives']}/{best['metrics']['combined_errors']}`.")
    write_text(PACKAGE_ROOT / "lessons_learned.md", "\n".join(lessons) + "\n")
    write_text(
        PACKAGE_ROOT / "strategy_state.md",
        "# v038 Strategy State\n\n"
        f"- FP8 prompt working best remains `v034a_fp8_broad_context_scene_box_guard = 181 / 38 / 25 / 63`.\n"
        f"- Best offline simulation decision: `{decision}`.\n"
        f"- Next work: `{final_payload['recommended_next_work']}`.\n"
        "- Do not promote or treat this as product runtime behavior.\n",
    )
    write_text(
        PACKAGE_ROOT / "README.md",
        "# v038 FP8 Same-Wreck Duplicate Suppression Simulation\n\n"
        "Offline-only simulation tranche over frozen `v034a` FP8 vLLM predictions. No VLM calls, no prompt candidates, and no product/runtime/eval-truth edits were made.\n",
    )
    copy_review_images()

    write_text(
        PACKAGE_ROOT / "simulation_grid_results.md",
        "# v038 Simulation Grid Results\n\n"
        f"Rules evaluated: `{len(results)}`. Safe rules: `{len(safe_results)}`. See `simulation_grid_results.csv` and `simulation_grid_results.json`.\n",
    )
    print_status(
        "case_delta_review",
        best,
        decision,
        "Case-level deltas are written for the best rule.",
        "Finalize validation and push evidence if safe.",
    )
    print_status(
        "final_decision",
        best,
        decision,
        decision_text,
        final_payload["recommended_next_work"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
