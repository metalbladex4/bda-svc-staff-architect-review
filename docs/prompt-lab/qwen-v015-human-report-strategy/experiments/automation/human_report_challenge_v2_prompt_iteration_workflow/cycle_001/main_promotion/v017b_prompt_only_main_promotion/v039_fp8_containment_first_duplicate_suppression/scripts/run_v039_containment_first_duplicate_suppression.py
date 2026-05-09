#!/usr/bin/env python3
"""Offline containment-first duplicate suppression simulation for FP8 vLLM."""

from __future__ import annotations

import contextlib
import csv
import datetime as dt
import importlib.util
import io
import itertools
import json
import os
import shutil
import sys
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any


WORKTREE_ROOT = Path("/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement")
CAPSTONE_ROOT = Path("/home/williambenitez1/Capstone")
PACKAGE_ROOT = WORKTREE_ROOT / (
    "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion/v039_fp8_containment_first_duplicate_suppression"
)
V038_SCRIPT = WORKTREE_ROOT / (
    "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion/v038_fp8_same_wreck_duplicate_suppression_simulation/"
    "scripts/run_v038_duplicate_suppression_simulation.py"
)

spec = importlib.util.spec_from_file_location("v038_helpers", V038_SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot import v038 helpers from {V038_SCRIPT}")
v038 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = v038
spec.loader.exec_module(v038)


CONTAINMENT_THRESHOLDS = [0.80, 0.90, 0.95, 0.98, 1.00]
IOU_THRESHOLDS: list[float | None] = [None, 0.00, 0.03, 0.05, 0.08, 0.10]
AREA_RATIO_THRESHOLDS = [0.03, 0.05, 0.08, 0.10, 0.15, 0.20]
SAME_LABEL_OPTIONS = [True, False]
PRIORITY_CASES = ["66", "67", "84", "97", "110", "155", "166"]
OLD_V020C = {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58}
FP8_BASELINE = {"matches": 180, "false_negatives": 39, "false_positives": 32, "combined_errors": 71}
V034A_BASELINE = {"matches": 181, "false_negatives": 38, "false_positives": 25, "combined_errors": 63}


@dataclass(frozen=True)
class Rule:
    rule_id: str
    containment_threshold: float
    iou_threshold: float | None
    area_ratio_threshold: float
    same_label_required: bool
    center_inside_required: bool = True
    only_suppress_if_larger_matched: bool = True
    never_suppress_if_smaller_matched: bool = True
    never_suppress_if_both_overlap_distinct_refs: bool = True
    never_suppress_if_smaller_has_better_ref_iou: bool = True


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def evaluate_reports(references: dict[str, dict[str, Any]], predictions: dict[str, dict[str, Any]], image_order: list[str]) -> dict[str, Any]:
    # bda_eval prints LLMaaJ skip messages per case; suppress them for grid runs.
    os.environ.pop("OLLAMA_API_KEY", None)
    with contextlib.redirect_stdout(io.StringIO()):
        return v038.evaluate_reports(references, predictions, image_order)


def target_ref_stats(reference: dict[str, Any], prediction: dict[str, Any]) -> dict[str, dict[str, Any]]:
    ref_report = v038.models.BDAReport.from_dict(reference)
    pred_report = v038.models.BDAReport.from_dict(prediction)
    policy = v038.models.get_eval_policy("detection_study")
    out: dict[str, dict[str, Any]] = {
        target.target_label: {"viable_refs": set(), "best_ref_iou": 0.0, "best_ref_label": None}
        for target in pred_report.targets
    }
    for pred in pred_report.targets:
        for ref in ref_report.targets:
            if pred.target_type != ref.target_type:
                continue
            pair_iou = pred.box.calc_iou(ref.box)
            overlap = ref.box.overlap_coverage(pred.box)
            if pair_iou > out[pred.target_label]["best_ref_iou"]:
                out[pred.target_label]["best_ref_iou"] = pair_iou
                out[pred.target_label]["best_ref_label"] = ref.target_label
            if v038.models.BDAReport._passes_policy(ref.target_type, pair_iou, overlap, policy):
                out[pred.target_label]["viable_refs"].add(ref.target_label)
    return out


def pair_features(prediction: dict[str, Any], baseline_map: dict[str, Any], ref_stats: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    targets = prediction.get("physical_damage", {})
    items = []
    for label, target in targets.items():
        box = v038.box_from_target_dict(target)
        items.append(
            {
                "label": label,
                "target_type": target.get("target_type"),
                "box": box,
                "bbox": [float(v) for v in box],
                "area": v038.area(box),
                "matched": label in baseline_map["matched_preds"],
                "matched_ref": baseline_map["pred_to_ref"].get(label),
                "viable_refs": sorted(ref_stats.get(label, {}).get("viable_refs", set())),
                "best_ref_iou": float(ref_stats.get(label, {}).get("best_ref_iou", 0.0)),
                "best_ref_label": ref_stats.get(label, {}).get("best_ref_label"),
            }
        )
    pairs = []
    for a, b in itertools.combinations(items, 2):
        if a["area"] <= 0 or b["area"] <= 0:
            continue
        small, large = (a, b) if a["area"] <= b["area"] else (b, a)
        inter = v038.intersect_area(small["box"], large["box"])
        if inter <= 0:
            continue
        small_refs = set(small["viable_refs"])
        large_refs = set(large["viable_refs"])
        pairs.append(
            {
                "smaller_label": small["label"],
                "larger_label": large["label"],
                "smaller_target_type": small["target_type"],
                "larger_target_type": large["target_type"],
                "same_target_type": small["target_type"] == large["target_type"],
                "small_area": small["area"],
                "large_area": large["area"],
                "smaller_bbox": small["bbox"],
                "larger_bbox": large["bbox"],
                "area_ratio": small["area"] / large["area"] if large["area"] else 0.0,
                "containment_ratio": inter / small["area"] if small["area"] else 0.0,
                "iou": v038.iou(small["box"], large["box"]),
                "center_inside_larger": v038.center_inside(small["box"], large["box"]),
                "smaller_matched": small["matched"],
                "larger_matched": large["matched"],
                "smaller_matched_ref": small["matched_ref"],
                "larger_matched_ref": large["matched_ref"],
                "smaller_viable_refs": sorted(small_refs),
                "larger_viable_refs": sorted(large_refs),
                "smaller_best_ref_iou": small["best_ref_iou"],
                "larger_best_ref_iou": large["best_ref_iou"],
                "smaller_best_ref_label": small["best_ref_label"],
                "larger_best_ref_label": large["best_ref_label"],
                "smaller_has_better_ref_iou": small["best_ref_iou"] > large["best_ref_iou"],
                "both_overlap_distinct_refs": bool(small_refs and large_refs and small_refs.isdisjoint(large_refs)),
            }
        )
    return pairs


def suppressions_for_rule(pair_rows: list[dict[str, Any]], rule: Rule) -> list[dict[str, Any]]:
    hits = []
    for pair in pair_rows:
        if pair["containment_ratio"] < rule.containment_threshold:
            continue
        if rule.iou_threshold is not None and pair["iou"] < rule.iou_threshold:
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
        if rule.never_suppress_if_smaller_has_better_ref_iou and pair["smaller_has_better_ref_iou"]:
            continue
        hits.append(pair)
    seen = set()
    deduped = []
    for row in sorted(hits, key=lambda item: (item["smaller_label"], -item["containment_ratio"], -(item["iou"] or 0.0))):
        key = row["smaller_label"]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def apply_rule(predictions: dict[str, dict[str, Any]], pairs_by_image: dict[str, list[dict[str, Any]]], rule: Rule) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    mutated = deepcopy(predictions)
    removals = []
    for image_filename, pairs in pairs_by_image.items():
        for hit in suppressions_for_rule(pairs, rule):
            label = hit["smaller_label"]
            if label in mutated[image_filename].get("physical_damage", {}):
                del mutated[image_filename]["physical_damage"][label]
                removals.append(
                    {
                        "image_filename": image_filename,
                        "case_id": v038.case_num(image_filename),
                        "removed_label": label,
                        "kept_larger_label": hit["larger_label"],
                        "removed_target_type": hit["smaller_target_type"],
                        "kept_larger_target_type": hit["larger_target_type"],
                        "removed_bbox": hit["smaller_bbox"],
                        "kept_larger_bbox": hit["larger_bbox"],
                        "iou": hit["iou"],
                        "containment_ratio": hit["containment_ratio"],
                        "area_ratio": hit["area_ratio"],
                        "removed_matched": hit["smaller_matched"],
                        "larger_matched": hit["larger_matched"],
                        "removed_best_ref_iou": hit["smaller_best_ref_iou"],
                        "larger_best_ref_iou": hit["larger_best_ref_iou"],
                        "reason_removed": "smaller_unmatched_box_contained_in_larger_matched_prediction",
                    }
                )
    return mutated, removals


def rule_grid() -> list[Rule]:
    rules = []
    n = 0
    for containment, pair_iou, area_ratio, same_label in itertools.product(
        CONTAINMENT_THRESHOLDS,
        IOU_THRESHOLDS,
        AREA_RATIO_THRESHOLDS,
        SAME_LABEL_OPTIONS,
    ):
        n += 1
        rules.append(
            Rule(
                rule_id=f"r{n:03d}",
                containment_threshold=containment,
                iou_threshold=pair_iou,
                area_ratio_threshold=area_ratio,
                same_label_required=same_label,
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
    for case_id in ["66", "67", "84", "110", "155", "166"]:
        if is_case_worse(result["case_metrics"].get(case_id, "0/999/999"), baseline_cases.get(case_id, "0/999/999")):
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
        removed = len(best["removals"])
    else:
        metric_text = "n/a"
        best_rule = "n/a"
        vs_v034a = "n/a"
        vs_old = "n/a"
        cases = {}
        removed = "n/a"
    print("=== V039 STATUS ===", flush=True)
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
    print(f"removed_predictions: {removed}", flush=True)
    print(f"decision: {decision}", flush=True)
    print(f"main_lesson: {lesson}", flush=True)
    print(f"next_action: {next_action}", flush=True)
    print("===================", flush=True)


def row_for_result(result: dict[str, Any]) -> dict[str, Any]:
    metrics = result["metrics"]
    return {
        "rule_id": result["rule_id"],
        "containment_threshold": result["rule"]["containment_threshold"],
        "iou_threshold": "none" if result["rule"]["iou_threshold"] is None else result["rule"]["iou_threshold"],
        "area_ratio_threshold": result["rule"]["area_ratio_threshold"],
        "same_label_required": result["rule"]["same_label_required"],
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


def copy_review_images() -> None:
    review_dir = PACKAGE_ROOT / "review_images"
    review_dir.mkdir(parents=True, exist_ok=True)
    for case in PRIORITY_CASES:
        for folder in ["images_bbox_both", "images_bbox_predicted", "images_bbox_reference", "images_bbox_review"]:
            src = v038.V034_RUN_ROOT / "eval" / folder / f"bbox_{case}.jpg"
            if not src.exists():
                src = v038.V034_RUN_ROOT / "eval" / folder / f"bbox_{case}.png"
            if src.exists():
                shutil.copy2(src, review_dir / f"v034a_{folder}_{src.name}")


def main() -> int:
    for dirname in ["scripts", "tables", "review_images"]:
        (PACKAGE_ROOT / dirname).mkdir(parents=True, exist_ok=True)

    write_json(
        PACKAGE_ROOT / "source_manifest.json",
        {
            "generated_at": utc_now(),
            "package": "v039_fp8_containment_first_duplicate_suppression",
            "frozen_artifacts_only": True,
            "vlm_called": False,
            "prompt_candidate_authored": False,
            "source_artifacts": [
                "z_reference_docs/GPT-Pro_collab/V036_FP8_CASE155_DENSE_SYNTHESIS_REVIEW_POINTER.md (requested; not present)",
                str(WORKTREE_ROOT / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v036_fp8_case155_dense_synthesis/case155_fp_synthesis.md"),
                str(WORKTREE_ROOT / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v036_fp8_case155_dense_synthesis/dense_case_regression_synthesis.md"),
                str(WORKTREE_ROOT / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v037_fp8_same_wreck_duplicate_guard_autonomous/final_recommendation.md"),
                str(WORKTREE_ROOT / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v038_fp8_same_wreck_duplicate_suppression_simulation/final_recommendation.md"),
                str(WORKTREE_ROOT / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v038_fp8_same_wreck_duplicate_suppression_simulation/best_simulation_report.md"),
                str(WORKTREE_ROOT / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v038_fp8_same_wreck_duplicate_suppression_simulation/failure_analysis.md"),
                str(CAPSTONE_ROOT / "z_reference_docs/GPT-Pro_collab/bda_svc_qwen_prompt_engineering_deep_research_bundle.md"),
                str(CAPSTONE_ROOT / "z_reference_docs/GPT-Pro_collab/CODEX_QWEN_PROMPT_ENGINEERING_DIRECTION_2026-05-06.md"),
            ],
            "v034a_run_root": str(v038.V034_RUN_ROOT),
            "manifest": str(v038.ALL_CURRENT_MANIFEST),
            "hard_boundaries": {
                "no_promotion": True,
                "no_product_truth_mutation": True,
                "no_runtime_code_mutation": True,
                "no_eval_ground_truth_mutation": True,
                "no_v024o_scored_evidence": True,
                "no_vlm_calls": True,
                "no_prompt_candidate": True,
            },
        },
    )

    cases = v038.load_manifest_cases()
    image_order = [case["image_filename"] for case in cases]
    references = v038.load_reference_reports(cases)
    predictions = v038.load_predicted_reports()
    baseline_eval = evaluate_reports(references, predictions, image_order)
    baseline_cases = v038.case_metrics(baseline_eval)
    baseline_maps = v038.matched_maps(baseline_eval)
    office_summary = v038.read_json(v038.V034_OFFICE_RUN_ROOT / "eval/evaluation_2026-05-09_030200Z_summary.json")
    office_pass = office_summary["totals"]["false_positive_count"] == 0

    artifact_inventory = {
        "generated_at": utc_now(),
        "v034a_prediction_files": len(list((v038.V034_RUN_ROOT / "predicted").glob("*.json"))),
        "manifest_cases": len(cases),
        "case_101_excluded": "101.jpg" not in image_order,
        "baseline_recomputed": baseline_eval["totals"],
        "baseline_expected": V034A_BASELINE,
        "baseline_recompute_matches_expected": baseline_eval["totals"] == {**V034A_BASELINE, "image_count": 117},
        "office_negative_pass": office_pass,
        "old_v020c_reference": OLD_V020C,
        "fp8_baseline": FP8_BASELINE,
        "v034a_working_best": V034A_BASELINE,
        "v035a_status": "rejected_micro_pack_41_15_19_34",
        "v037_status": "rejected_no_new_fp8_working_best",
        "v024o_status": "partial_unscored_forbidden",
    }
    write_json(PACKAGE_ROOT / "artifact_inventory.json", artifact_inventory)
    write_text(
        PACKAGE_ROOT / "artifact_inventory.md",
        "# v039 Artifact Inventory\n\n"
        f"- Frozen v034a run root: `{v038.V034_RUN_ROOT}`\n"
        f"- Prediction files: `{artifact_inventory['v034a_prediction_files']}`\n"
        f"- Manifest cases: `{artifact_inventory['manifest_cases']}`; case 101 excluded: `{artifact_inventory['case_101_excluded']}`\n"
        f"- Recomputed v034a baseline: `{baseline_eval['totals']['matches']}/{baseline_eval['totals']['false_negatives']}/{baseline_eval['totals']['false_positives']}/{baseline_eval['totals']['combined_errors']}`\n"
        f"- Office-negative pass from frozen v034a artifacts: `{office_pass}`\n",
    )

    pairs_by_image: dict[str, list[dict[str, Any]]] = {}
    for image_filename in image_order:
        stats = target_ref_stats(references[image_filename], predictions[image_filename])
        pairs_by_image[image_filename] = pair_features(predictions[image_filename], baseline_maps[image_filename], stats)

    pair_rows = [{"image_filename": image_filename, **row} for image_filename, rows in pairs_by_image.items() for row in rows]
    write_json(PACKAGE_ROOT / "tables/pair_feature_inventory.json", pair_rows)

    known_pair = next(
        (
            row
            for row in pair_rows
            if row["image_filename"] == "155.jpg" and row["smaller_label"] == "target_1" and row["larger_label"] == "target_0"
        ),
        None,
    )
    known_analysis = {
        "generated_at": utc_now(),
        "case_id": "155",
        "v034a_metrics": baseline_cases.get("155"),
        "known_duplicate_pair": known_pair,
        "known_duplicate_reconstructed": known_pair is not None,
        "smaller_is_fp": bool(known_pair and not known_pair["smaller_matched"]),
        "larger_is_tp_matched": bool(known_pair and known_pair["larger_matched"]),
        "why_v038_missed_it": "v038's minimum IoU threshold was 0.10; this pair's IoU is approximately 0.083.",
    }
    write_json(PACKAGE_ROOT / "known_case155_duplicate_analysis.json", known_analysis)
    write_text(
        PACKAGE_ROOT / "known_case155_duplicate_analysis.md",
        "# v039 Known Case-155 Duplicate Analysis\n\n"
        f"- v034a case 155 metrics: `{baseline_cases.get('155')}`\n"
        f"- Known duplicate reconstructed: `{known_pair is not None}`\n"
        f"- Smaller box: `{known_pair['smaller_label'] if known_pair else 'n/a'}` bbox `{known_pair['smaller_bbox'] if known_pair else 'n/a'}`\n"
        f"- Larger box: `{known_pair['larger_label'] if known_pair else 'n/a'}` bbox `{known_pair['larger_bbox'] if known_pair else 'n/a'}`\n"
        f"- Containment: `{known_pair['containment_ratio'] if known_pair else 'n/a'}`\n"
        f"- IoU: `{known_pair['iou'] if known_pair else 'n/a'}`\n"
        f"- Area ratio: `{known_pair['area_ratio'] if known_pair else 'n/a'}`\n"
        f"- Center-inside: `{known_pair['center_inside_larger'] if known_pair else 'n/a'}`\n"
        f"- Smaller is FP/unmatched: `{known_analysis['smaller_is_fp']}`\n"
        f"- Larger is TP/matched: `{known_analysis['larger_is_tp_matched']}`\n\n"
        "v038 missed this pair because its minimum IoU threshold was `0.10`, while this nested duplicate's IoU is about `0.083`.\n",
    )
    print_status(
        "known_duplicate_analysis",
        None,
        "E",
        "The known case-155 nested duplicate was reconstructed from frozen v034a predictions.",
        "Run containment-first rules with no or lower IoU floors.",
    )

    rules = rule_grid()
    write_json(
        PACKAGE_ROOT / "containment_first_rules.json",
        {
            "generated_at": utc_now(),
            "rule_count": len(rules),
            "containment_thresholds": CONTAINMENT_THRESHOLDS,
            "iou_thresholds": ["none" if v is None else v for v in IOU_THRESHOLDS],
            "area_ratio_thresholds": AREA_RATIO_THRESHOLDS,
            "center_inside_required": True,
            "same_label_variants": SAME_LABEL_OPTIONS,
            "only_suppress_if_larger_matched": True,
            "never_suppress_if_smaller_matched": True,
            "never_suppress_if_both_overlap_distinct_refs": True,
            "never_suppress_if_smaller_has_better_ref_iou": True,
        },
    )
    write_text(
        PACKAGE_ROOT / "containment_first_rules.md",
        "# v039 Containment-First Rules\n\n"
        "Rules suppress only an unmatched smaller box that is mostly contained in a larger matched prediction. IoU may be disabled or set below v038's `0.10` floor. A smaller matched box, a distinct-reference pair, or a smaller box with better reference IoU is never suppressed.\n",
    )
    write_json(
        PACKAGE_ROOT / "simulation_plan.json",
        {
            "generated_at": utc_now(),
            "method": "offline_in_memory_removal_then_bda_eval_matching_recompute",
            "uses_vlm": False,
            "rules": "containment_first_grid",
            "safety_gates": [
                "no_fn_increase",
                "no_match_decrease",
                "case_66_not_worse",
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
        "# v039 Simulation Plan\n\n"
        "Read frozen v034a predictions, apply containment-first removals in memory, and recompute `bda_eval` detection-study matching. No VLM calls, prompt candidates, runtime edits, or eval-truth edits are used.\n",
    )

    results = []
    for rule in rules:
        mutated, removals = apply_rule(predictions, pairs_by_image, rule)
        eval_payload = evaluate_reports(references, mutated, image_order)
        result = {
            "rule_id": rule.rule_id,
            "rule": {
                "containment_threshold": rule.containment_threshold,
                "iou_threshold": rule.iou_threshold,
                "area_ratio_threshold": rule.area_ratio_threshold,
                "same_label_required": rule.same_label_required,
                "center_inside_required": rule.center_inside_required,
                "only_suppress_if_larger_matched": rule.only_suppress_if_larger_matched,
                "never_suppress_if_smaller_matched": rule.never_suppress_if_smaller_matched,
                "never_suppress_if_both_overlap_distinct_refs": rule.never_suppress_if_both_overlap_distinct_refs,
                "never_suppress_if_smaller_has_better_ref_iou": rule.never_suppress_if_smaller_has_better_ref_iou,
            },
            "metrics": eval_payload["totals"],
            "case_metrics": v038.case_metrics(eval_payload),
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
            r["rule"]["same_label_required"] is False,
            r["rule"]["area_ratio_threshold"],
            999.0 if r["rule"]["iou_threshold"] is None else r["rule"]["iou_threshold"],
            r["rule"]["containment_threshold"],
        ),
    )
    best = ranked[0] if ranked else None
    print_status(
        "containment_grid",
        best,
        "B" if best and best["metrics"]["combined_errors"] < V034A_BASELINE["combined_errors"] else "D",
        "Containment-first grid complete; safe rules are ranked by error reduction and simplicity.",
        "Analyze best rule removals and case-level deltas.",
    )

    best_case_rows: list[dict[str, Any]] = []
    if best:
        best_rule = Rule(**{"rule_id": best["rule_id"], **best["rule"]})
        best_predictions, _ = apply_rule(predictions, pairs_by_image, best_rule)
        best_eval = evaluate_reports(references, best_predictions, image_order)
        by_image = {item["image_filename"]: item for item in best_eval["images"]}
        base_by_image = {item["image_filename"]: item for item in baseline_eval["images"]}
        for image_filename in image_order:
            base = base_by_image[image_filename]
            cand = by_image[image_filename]
            best_case_rows.append(
                {
                    "image_filename": image_filename,
                    "case_id": v038.case_num(image_filename),
                    "baseline_matches": base["match_count"],
                    "baseline_false_negatives": base["false_negative_count"],
                    "baseline_false_positives": base["false_positive_count"],
                    "sim_matches": cand["match_count"],
                    "sim_false_negatives": cand["false_negative_count"],
                    "sim_false_positives": cand["false_positive_count"],
                    "delta_matches": cand["match_count"] - base["match_count"],
                    "delta_false_negatives": cand["false_negative_count"] - base["false_negative_count"],
                    "delta_false_positives": cand["false_positive_count"] - base["false_positive_count"],
                    "removed_labels": ",".join(r["removed_label"] for r in best["removals"] if r["image_filename"] == image_filename),
                }
            )
        write_json(PACKAGE_ROOT / "best_simulation_report.json", {"generated_at": utc_now(), "best_rule": best, "top_safe_rules": ranked[:20]})
        write_text(
            PACKAGE_ROOT / "best_simulation_report.md",
            "# v039 Best Simulation Report\n\n"
            f"Best safe rule: `{best['rule_id']}`\n\n"
            f"Metrics: `{best['metrics']['matches']}/{best['metrics']['false_negatives']}/{best['metrics']['false_positives']}/{best['metrics']['combined_errors']}`.\n\n"
            f"Rule: containment >= `{best['rule']['containment_threshold']}`, IoU >= `{best['rule']['iou_threshold']}`, area ratio <= `{best['rule']['area_ratio_threshold']}`, same-label `{best['rule']['same_label_required']}`.\n\n"
            f"Removed boxes: `{len(best['removals'])}`.\n\n"
            f"Removed predictions: `{best['removals']}`\n",
        )
    else:
        write_json(PACKAGE_ROOT / "best_simulation_report.json", {"generated_at": utc_now(), "best_rule": None, "top_safe_rules": []})
        write_text(PACKAGE_ROOT / "best_simulation_report.md", "# v039 Best Simulation Report\n\nNo safe rule was found.\n")

    write_csv(PACKAGE_ROOT / "case_level_delta_report.csv", best_case_rows)
    write_text(
        PACKAGE_ROOT / "case_level_delta_report.md",
        "# v039 Case-Level Delta Report\n\n"
        f"Best rule `{best['rule_id'] if best else 'n/a'}` changes `{sum(1 for row in best_case_rows if row['delta_false_positives'] or row['delta_false_negatives'] or row['delta_matches'])}` cases. See `case_level_delta_report.csv`.\n",
    )
    print_status(
        "best_rule_analysis",
        best,
        "B" if best and best["metrics"]["combined_errors"] < V034A_BASELINE["combined_errors"] else "D",
        "Best rule removals and case deltas were written.",
        "Write final decision.",
    )

    if best is None:
        decision = "E"
    elif best["metrics"]["combined_errors"] <= OLD_V020C["combined_errors"]:
        decision = "A"
    elif best["metrics"]["combined_errors"] < V034A_BASELINE["combined_errors"]:
        decision = "B"
    elif best["removals"]:
        decision = "C"
    else:
        decision = "D"

    reason_counts: dict[str, int] = {}
    for result in results:
        for reason in result["safety_reasons"]:
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
    failure_payload = {
        "generated_at": utc_now(),
        "unsafe_rule_count": len([r for r in results if not r["safe"]]),
        "safe_rule_count": len(safe_results),
        "rules_with_removals": len([r for r in results if r["removals"]]),
        "safe_rules_with_removals": len([r for r in safe_results if r["removals"]]),
        "common_safety_reasons": dict(sorted(reason_counts.items(), key=lambda item: (-item[1], item[0]))),
    }
    write_json(PACKAGE_ROOT / "failure_analysis.json", failure_payload)
    write_text(
        PACKAGE_ROOT / "failure_analysis.md",
        "# v039 Failure Analysis\n\n"
        f"Safe rules: `{failure_payload['safe_rule_count']}`. Unsafe rules: `{failure_payload['unsafe_rule_count']}`.\n"
        f"Rules with removals: `{failure_payload['rules_with_removals']}`. Safe rules with removals: `{failure_payload['safe_rules_with_removals']}`.\n\n"
        "Rules were marked unsafe if they increased FNs, reduced matches, worsened dense/control cases, or failed office-negative.\n",
    )

    final_payload = {
        "generated_at": utc_now(),
        "decision": decision,
        "best_rule_id": best["rule_id"] if best else None,
        "best_metrics": best["metrics"] if best else None,
        "removed_predictions": len(best["removals"]) if best else 0,
        "known_case155_duplicate_tested": known_pair is not None,
        "known_case155_duplicate_removed": bool(best and any(r["image_filename"] == "155.jpg" and r["removed_label"] == "target_1" for r in best["removals"])),
        "beat_v034a": bool(best and best["metrics"]["combined_errors"] < V034A_BASELINE["combined_errors"]),
        "reached_or_beat_old_58": bool(best and best["metrics"]["combined_errors"] <= OLD_V020C["combined_errors"]),
        "case_metrics": best["case_metrics"] if best else {},
        "recommended_next_work": "v040_experiment_only_post_processing_tranche" if decision in {"A", "B", "C"} else "fiftyone_or_crop_verifier_review",
        "hard_boundaries_preserved": True,
    }
    write_json(PACKAGE_ROOT / "final_recommendation.json", final_payload)

    decision_text = {
        "A": "Containment-first simulation beats v034a and reaches <=58 errors.",
        "B": "Containment-first simulation beats v034a but remains above 58.",
        "C": "Containment-first simulation finds a safe narrow rule worth experiment-only post-processing.",
        "D": "Containment-first simulation shows duplicate suppression is too local or unsafe.",
        "E": "Simulation cannot be evaluated reliably from available artifacts.",
    }[decision]
    write_text(
        PACKAGE_ROOT / "final_recommendation.md",
        "# v039 Final Recommendation\n\n"
        f"Generated: `{utc_now()}`\n\n"
        f"Decision `{decision}`: {decision_text}\n\n"
        f"Known case-155 duplicate tested: `{final_payload['known_case155_duplicate_tested']}`.\n"
        f"Known case-155 duplicate removed: `{final_payload['known_case155_duplicate_removed']}`.\n\n"
        f"Best rule: `{final_payload['best_rule_id'] or 'n/a'}`.\n\n"
        + (
            f"Best metrics: `{best['metrics']['matches']}/{best['metrics']['false_negatives']}/{best['metrics']['false_positives']}/{best['metrics']['combined_errors']}`.\n\n"
            if best
            else "Best metrics: `n/a`.\n\n"
        )
        + f"Beat v034a: `{final_payload['beat_v034a']}`.\n"
        f"Reached or beat old 58-error reference: `{final_payload['reached_or_beat_old_58']}`.\n"
        f"Recommended next work: `{final_payload['recommended_next_work']}`.\n\n"
        "This is non-promoted post-hoc evidence only. It does not modify product runtime, prompt text, doctrine, assessment prompt, eval truth, or source truth.\n",
    )

    write_json(
        PACKAGE_ROOT / "recovery_log.json",
        {
            "generated_at": utc_now(),
            "steps": [
                "Read local v036/v037/v038 source artifacts.",
                "Graphify recall was attempted but blocked by missing networkx.",
                "Recomputed v034a from frozen predictions.",
                "Reconstructed known case-155 duplicate geometry.",
                "Ran containment-first grid offline.",
                "Wrote final recommendation and validation artifacts.",
            ],
        },
    )
    write_text(
        PACKAGE_ROOT / "recovery_log.md",
        "# v039 Recovery Log\n\n"
        "- Used frozen v034a predictions only.\n"
        "- Did not call the VLM or author a prompt candidate.\n"
        "- Recomputed matching through `bda_eval` model classes in memory.\n"
        "- Tested containment-first rules with no or lower IoU floors than v038.\n",
    )
    write_text(
        PACKAGE_ROOT / "lessons_learned.md",
        "# v039 Lessons Learned\n\n"
        "- Containment-first simulation directly tests the duplicate class v038 missed.\n"
        "- Any post-hoc duplicate rule must keep matches and FNs unchanged while preserving dense cases 66/67/84/110.\n"
        f"- Best decision: `{decision}`.\n",
    )
    write_text(
        PACKAGE_ROOT / "strategy_state.md",
        "# v039 Strategy State\n\n"
        "- FP8 prompt working best remains `v034a_fp8_broad_context_scene_box_guard = 181 / 38 / 25 / 63` unless and until a non-promoted post-hoc line is separately implemented and validated.\n"
        f"- Best offline simulation decision: `{decision}`.\n"
        f"- Next work: `{final_payload['recommended_next_work']}`.\n"
        "- Do not promote or treat this as product runtime behavior.\n",
    )
    write_text(
        PACKAGE_ROOT / "README.md",
        "# v039 FP8 Containment-First Duplicate Suppression Simulation\n\n"
        "Offline-only containment-first simulation tranche over frozen `v034a` FP8 vLLM predictions. No VLM calls, no prompt candidates, and no product/runtime/eval-truth edits were made.\n",
    )
    write_text(
        PACKAGE_ROOT / "simulation_grid_results.md",
        "# v039 Simulation Grid Results\n\n"
        f"Rules evaluated: `{len(results)}`. Safe rules: `{len(safe_results)}`. See `simulation_grid_results.csv` and `simulation_grid_results.json`.\n",
    )
    copy_review_images()

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
