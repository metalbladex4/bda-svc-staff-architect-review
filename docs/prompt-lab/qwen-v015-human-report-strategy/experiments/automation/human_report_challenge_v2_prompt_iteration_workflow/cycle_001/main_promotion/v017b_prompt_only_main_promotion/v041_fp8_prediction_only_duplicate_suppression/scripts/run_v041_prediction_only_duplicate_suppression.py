#!/usr/bin/env python3
"""Prediction-only duplicate suppression simulation for frozen FP8 v034a outputs."""

from __future__ import annotations

import contextlib
import csv
import datetime as dt
import importlib.util
import io
import itertools
import json
import os
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
    "v017b_prompt_only_main_promotion/v041_fp8_prediction_only_duplicate_suppression"
)
V039_SCRIPT = WORKTREE_ROOT / (
    "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion/v039_fp8_containment_first_duplicate_suppression/"
    "scripts/run_v039_containment_first_duplicate_suppression.py"
)

spec = importlib.util.spec_from_file_location("v039_helpers", V039_SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot import v039 helpers from {V039_SCRIPT}")
v039 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = v039
spec.loader.exec_module(v039)
v038 = v039.v038


OLD_V020C = {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58}
FP8_BASELINE = {"matches": 180, "false_negatives": 39, "false_positives": 32, "combined_errors": 71}
V034A_BASELINE = {"matches": 181, "false_negatives": 38, "false_positives": 25, "combined_errors": 63}
V040_HYBRID = {"matches": 181, "false_negatives": 38, "false_positives": 22, "combined_errors": 60}
V040_R019 = {"matches": 181, "false_negatives": 38, "false_positives": 23, "combined_errors": 61}
PRIORITY_CASES = ["66", "67", "84", "88", "97", "100", "110", "155", "166"]

CONTAINMENT_THRESHOLDS = [0.80, 0.90, 0.95, 0.98, 1.00]
IOU_THRESHOLDS: list[float | None] = [None, 0.00, 0.03, 0.05, 0.08, 0.10]
AREA_RATIO_THRESHOLDS = [0.03, 0.05, 0.08, 0.10, 0.15, 0.20]
CROSS_AREA_RATIO_THRESHOLDS = [0.03, 0.05, 0.08]
CROSS_CONTAINMENT_THRESHOLDS = [0.90, 0.95, 0.98]
CROSS_NOT_ONLY_TYPE_OPTIONS = [True, False]
LARGER_IMAGE_AREA_MAX_THRESHOLDS: list[float | None] = [None, 0.50, 0.75, 1.00]
KEEP_LARGEST_ONLY_OPTIONS = [True, False]
NEVER_SUPPRESS_IF_SMALLER_CONTAINS_OPTIONS = [True, False]


@dataclass(frozen=True)
class PredictionOnlyRule:
    rule_id: str
    containment_threshold: float
    iou_threshold: float | None
    area_ratio_threshold: float
    center_inside_required: bool = True
    same_label_required: bool = True
    cross_label_allowed: bool = False
    cross_area_ratio_threshold: float | None = None
    cross_containment_threshold: float | None = None
    cross_removed_not_only_type_required: bool = True
    larger_image_area_max_ratio: float | None = None
    keep_largest_only: bool = True
    never_suppress_if_smaller_contains_prediction: bool = True


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
    os.environ.pop("OLLAMA_API_KEY", None)
    with contextlib.redirect_stdout(io.StringIO()):
        return v039.evaluate_reports(references, predictions, image_order)


def image_dimensions(cases: list[dict[str, Any]]) -> dict[str, tuple[int, int]]:
    try:
        from PIL import Image
    except Exception:
        return {}
    dims: dict[str, tuple[int, int]] = {}
    for case in cases:
        path = Path(case["image_path"])
        if not path.exists():
            continue
        with Image.open(path) as img:
            dims[case["image_filename"]] = img.size
    return dims


def prediction_items(prediction: dict[str, Any], dims: tuple[int, int] | None) -> list[dict[str, Any]]:
    targets = prediction.get("physical_damage", {})
    type_counts: dict[str, int] = {}
    for target in targets.values():
        target_type = str(target.get("target_type"))
        type_counts[target_type] = type_counts.get(target_type, 0) + 1

    img_area = None
    if dims:
        img_area = max(1, dims[0] * dims[1])

    items = []
    for label, target in targets.items():
        box = v038.box_from_target_dict(target)
        target_type = str(target.get("target_type"))
        box_area = v038.area(box)
        items.append(
            {
                "label": label,
                "target_type": target_type,
                "box": box,
                "bbox": [float(v) for v in box],
                "area": box_area,
                "type_count": type_counts.get(target_type, 0),
                "image_area_ratio": None if img_area is None else box_area / img_area,
            }
        )
    return items


def pair_features_prediction_only(prediction: dict[str, Any], dims: tuple[int, int] | None) -> list[dict[str, Any]]:
    items = prediction_items(prediction, dims)
    pairs = []
    for a, b in itertools.combinations(items, 2):
        if a["area"] <= 0 or b["area"] <= 0:
            continue
        small, large = (a, b) if a["area"] <= b["area"] else (b, a)
        inter = v038.intersect_area(small["box"], large["box"])
        if inter <= 0:
            continue
        smaller_contains_other = False
        for other in items:
            if other["label"] in {small["label"], large["label"]} or other["area"] <= 0:
                continue
            other_inter = v038.intersect_area(other["box"], small["box"])
            if other_inter / other["area"] >= 0.80 and v038.center_inside(other["box"], small["box"]):
                smaller_contains_other = True
                break
        pairs.append(
            {
                "smaller_label": small["label"],
                "larger_label": large["label"],
                "removed_label": small["label"],
                "kept_larger_label": large["label"],
                "removed_target_type": small["target_type"],
                "kept_larger_target_type": large["target_type"],
                "same_target_type": small["target_type"] == large["target_type"],
                "cross_label": small["target_type"] != large["target_type"],
                "removed_type_count": small["type_count"],
                "removed_not_only_type": small["type_count"] > 1,
                "removed_bbox": small["bbox"],
                "kept_larger_bbox": large["bbox"],
                "small_area": small["area"],
                "large_area": large["area"],
                "area_ratio": small["area"] / large["area"] if large["area"] else 0.0,
                "containment_ratio": inter / small["area"] if small["area"] else 0.0,
                "iou": v038.iou(small["box"], large["box"]),
                "center_inside_larger": v038.center_inside(small["box"], large["box"]),
                "larger_image_area_ratio": large["image_area_ratio"],
                "smaller_contains_prediction": smaller_contains_other,
            }
        )
    return pairs


def rule_to_dict(rule: PredictionOnlyRule) -> dict[str, Any]:
    return {
        "rule_id": rule.rule_id,
        "containment_threshold": rule.containment_threshold,
        "iou_threshold": rule.iou_threshold,
        "area_ratio_threshold": rule.area_ratio_threshold,
        "center_inside_required": rule.center_inside_required,
        "same_label_required": rule.same_label_required,
        "cross_label_allowed": rule.cross_label_allowed,
        "cross_area_ratio_threshold": rule.cross_area_ratio_threshold,
        "cross_containment_threshold": rule.cross_containment_threshold,
        "cross_removed_not_only_type_required": rule.cross_removed_not_only_type_required,
        "larger_image_area_max_ratio": rule.larger_image_area_max_ratio,
        "keep_largest_only": rule.keep_largest_only,
        "never_suppress_if_smaller_contains_prediction": rule.never_suppress_if_smaller_contains_prediction,
        "oracle_fields_used": [],
    }


def qualifies_prediction_only(pair: dict[str, Any], rule: PredictionOnlyRule) -> bool:
    if pair["containment_ratio"] < rule.containment_threshold:
        return False
    if rule.iou_threshold is not None and pair["iou"] < rule.iou_threshold:
        return False
    if pair["area_ratio"] > rule.area_ratio_threshold:
        return False
    if rule.center_inside_required and not pair["center_inside_larger"]:
        return False
    if rule.larger_image_area_max_ratio is not None:
        larger_ratio = pair.get("larger_image_area_ratio")
        if larger_ratio is not None and larger_ratio > rule.larger_image_area_max_ratio:
            return False
    if rule.never_suppress_if_smaller_contains_prediction and pair["smaller_contains_prediction"]:
        return False
    if pair["same_target_type"]:
        return True
    if rule.same_label_required or not rule.cross_label_allowed:
        return False
    if rule.cross_area_ratio_threshold is not None and pair["area_ratio"] > rule.cross_area_ratio_threshold:
        return False
    if rule.cross_containment_threshold is not None and pair["containment_ratio"] < rule.cross_containment_threshold:
        return False
    if rule.cross_removed_not_only_type_required and not pair["removed_not_only_type"]:
        return False
    return True


def suppressions_for_rule(pair_rows: list[dict[str, Any]], rule: PredictionOnlyRule) -> list[dict[str, Any]]:
    hits = [pair for pair in pair_rows if qualifies_prediction_only(pair, rule)]
    if rule.keep_largest_only:
        hits = sorted(hits, key=lambda item: (item["smaller_label"], -item["large_area"], -item["containment_ratio"], -(item["iou"] or 0.0)))
    else:
        hits = sorted(hits, key=lambda item: (item["smaller_label"], -item["containment_ratio"], -(item["iou"] or 0.0)))
    seen = set()
    deduped = []
    for row in hits:
        key = row["smaller_label"]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def apply_rule(
    predictions: dict[str, dict[str, Any]],
    pairs_by_image: dict[str, list[dict[str, Any]]],
    rule: PredictionOnlyRule,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    mutated = deepcopy(predictions)
    removals = []
    for image_filename, pairs in pairs_by_image.items():
        for hit in suppressions_for_rule(pairs, rule):
            label = hit["smaller_label"]
            if label not in mutated[image_filename].get("physical_damage", {}):
                continue
            del mutated[image_filename]["physical_damage"][label]
            removals.append(
                {
                    "rule_id": rule.rule_id,
                    "case_id": v038.case_num(image_filename),
                    "image_filename": image_filename,
                    "removed_label": label,
                    "kept_larger_label": hit["larger_label"],
                    "removed_target_type": hit["removed_target_type"],
                    "kept_larger_target_type": hit["kept_larger_target_type"],
                    "removed_bbox": hit["removed_bbox"],
                    "kept_larger_bbox": hit["kept_larger_bbox"],
                    "iou": hit["iou"],
                    "containment_ratio": hit["containment_ratio"],
                    "area_ratio": hit["area_ratio"],
                    "center_inside": hit["center_inside_larger"],
                    "same_label": hit["same_target_type"],
                    "cross_label": hit["cross_label"],
                    "removed_type_count": hit["removed_type_count"],
                    "removed_not_only_type": hit["removed_not_only_type"],
                    "larger_image_area_ratio": hit["larger_image_area_ratio"],
                    "smaller_contains_prediction": hit["smaller_contains_prediction"],
                    "prediction_only_reason_removed": "contained_smaller_prediction_geometry_rule",
                }
            )
    return mutated, removals


def rule_grid() -> list[PredictionOnlyRule]:
    rules: list[PredictionOnlyRule] = []
    n = 0
    for containment, pair_iou, area_ratio, keep_largest, never_contains in itertools.product(
        CONTAINMENT_THRESHOLDS,
        IOU_THRESHOLDS,
        AREA_RATIO_THRESHOLDS,
        KEEP_LARGEST_ONLY_OPTIONS,
        NEVER_SUPPRESS_IF_SMALLER_CONTAINS_OPTIONS,
    ):
        n += 1
        rules.append(
            PredictionOnlyRule(
                rule_id=f"p{n:04d}",
                containment_threshold=containment,
                iou_threshold=pair_iou,
                area_ratio_threshold=area_ratio,
                same_label_required=True,
                cross_label_allowed=False,
                keep_largest_only=keep_largest,
                never_suppress_if_smaller_contains_prediction=never_contains,
            )
        )
        for cross_area, cross_containment, not_only, larger_max in itertools.product(
            CROSS_AREA_RATIO_THRESHOLDS,
            CROSS_CONTAINMENT_THRESHOLDS,
            CROSS_NOT_ONLY_TYPE_OPTIONS,
            LARGER_IMAGE_AREA_MAX_THRESHOLDS,
        ):
            n += 1
            rules.append(
                PredictionOnlyRule(
                    rule_id=f"p{n:04d}",
                    containment_threshold=containment,
                    iou_threshold=pair_iou,
                    area_ratio_threshold=area_ratio,
                    same_label_required=False,
                    cross_label_allowed=True,
                    cross_area_ratio_threshold=cross_area,
                    cross_containment_threshold=cross_containment,
                    cross_removed_not_only_type_required=not_only,
                    larger_image_area_max_ratio=larger_max,
                    keep_largest_only=keep_largest,
                    never_suppress_if_smaller_contains_prediction=never_contains,
                )
            )
    return rules


def case_metrics(eval_payload: dict[str, Any]) -> dict[str, str]:
    return v038.case_metrics(eval_payload)


def is_case_worse(candidate: str, baseline: str) -> bool:
    cm = tuple(int(x) for x in candidate.split("/"))
    bm = tuple(int(x) for x in baseline.split("/"))
    return cm[0] < bm[0] or cm[1] > bm[1] or cm[2] > bm[2]


def baseline_maps(eval_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return v038.matched_maps(eval_payload)


def annotate_removals(
    removals: list[dict[str, Any]],
    baseline_eval: dict[str, Any],
    candidate_eval: dict[str, Any],
) -> list[dict[str, Any]]:
    base_maps = baseline_maps(baseline_eval)
    base_by_image = {item["image_filename"]: item for item in baseline_eval["images"]}
    cand_by_image = {item["image_filename"]: item for item in candidate_eval["images"]}
    out = []
    for removal in removals:
        image_filename = removal["image_filename"]
        label = removal["removed_label"]
        base_map = base_maps[image_filename]
        base = base_by_image[image_filename]
        cand = cand_by_image[image_filename]
        removed_tp = label in base_map["matched_preds"]
        removed_fp = label in base_map["false_positives"]
        row = {
            **removal,
            "removed_true_positive": removed_tp,
            "removed_false_positive": removed_fp,
            "match_count_changed": cand["match_count"] != base["match_count"],
            "fn_changed": cand["false_negative_count"] != base["false_negative_count"],
            "fp_changed": cand["false_positive_count"] != base["false_positive_count"],
            "case_delta_matches": cand["match_count"] - base["match_count"],
            "case_delta_false_negatives": cand["false_negative_count"] - base["false_negative_count"],
            "case_delta_false_positives": cand["false_positive_count"] - base["false_positive_count"],
        }
        out.append(row)
    return out


def removal_key(removals: list[dict[str, Any]]) -> tuple[tuple[str, str], ...]:
    return tuple(sorted((item["image_filename"], item["removed_label"]) for item in removals))


def safety_reasons(
    result: dict[str, Any],
    baseline_eval: dict[str, Any],
    baseline_cases: dict[str, str],
    office_pass: bool,
) -> list[str]:
    reasons = []
    metrics = result["metrics"]
    base = baseline_eval["totals"]
    if metrics["false_negatives"] > base["false_negatives"]:
        reasons.append("fn_increase")
    if metrics["matches"] < base["matches"]:
        reasons.append("match_decrease")
    if result["removed_true_positives"] > 0:
        reasons.append("removed_true_positive")
    for case_id in ["66", "67", "84", "110", "155", "166"]:
        if is_case_worse(result["case_metrics"].get(case_id, "0/999/999"), baseline_cases.get(case_id, "0/999/999")):
            reasons.append(f"case_{case_id}_worse")
    if not office_pass:
        reasons.append("office_negative_not_pass")
    return reasons


def summarize_rule(
    rule: PredictionOnlyRule,
    references: dict[str, dict[str, Any]],
    predictions: dict[str, dict[str, Any]],
    image_order: list[str],
    pairs_by_image: dict[str, list[dict[str, Any]]],
    baseline_eval: dict[str, Any],
    baseline_cases: dict[str, str],
    office_pass: bool,
    eval_cache: dict[tuple[tuple[str, str], ...], tuple[dict[str, Any], dict[str, dict[str, Any]]]],
) -> dict[str, Any]:
    postprocessed, removals = apply_rule(predictions, pairs_by_image, rule)
    key = removal_key(removals)
    if key in eval_cache:
        eval_payload, postprocessed = eval_cache[key]
    else:
        eval_payload = evaluate_reports(references, postprocessed, image_order)
        eval_cache[key] = (eval_payload, postprocessed)
    annotated_removals = annotate_removals(removals, baseline_eval, eval_payload)
    result = {
        "rule_id": rule.rule_id,
        "rule": rule_to_dict(rule),
        "metrics": eval_payload["totals"],
        "case_metrics": case_metrics(eval_payload),
        "removals": annotated_removals,
        "removed_true_positives": sum(1 for row in annotated_removals if row["removed_true_positive"]),
        "removed_false_positives": sum(1 for row in annotated_removals if row["removed_false_positive"]),
    }
    result["safety_reasons"] = safety_reasons(result, baseline_eval, baseline_cases, office_pass)
    result["safe"] = not result["safety_reasons"]
    return result


def row_for_result(result: dict[str, Any]) -> dict[str, Any]:
    metrics = result["metrics"]
    cases = result["case_metrics"]
    rule = result["rule"]
    return {
        "rule_id": result["rule_id"],
        "containment_threshold": rule["containment_threshold"],
        "iou_threshold": "none" if rule["iou_threshold"] is None else rule["iou_threshold"],
        "area_ratio_threshold": rule["area_ratio_threshold"],
        "same_label_required": rule["same_label_required"],
        "cross_label_allowed": rule["cross_label_allowed"],
        "cross_area_ratio_threshold": rule["cross_area_ratio_threshold"],
        "cross_containment_threshold": rule["cross_containment_threshold"],
        "cross_removed_not_only_type_required": rule["cross_removed_not_only_type_required"],
        "larger_image_area_max_ratio": rule["larger_image_area_max_ratio"],
        "keep_largest_only": rule["keep_largest_only"],
        "never_suppress_if_smaller_contains_prediction": rule["never_suppress_if_smaller_contains_prediction"],
        "matches": metrics["matches"],
        "false_negatives": metrics["false_negatives"],
        "false_positives": metrics["false_positives"],
        "combined_errors": metrics["combined_errors"],
        "image_count": metrics["image_count"],
        "removed_predictions": len(result["removals"]),
        "removed_true_positives": result["removed_true_positives"],
        "removed_false_positives": result["removed_false_positives"],
        "safe": result["safe"],
        "safety_reasons": ";".join(result["safety_reasons"]),
        "case_66": cases.get("66", "n/a"),
        "case_67": cases.get("67", "n/a"),
        "case_84": cases.get("84", "n/a"),
        "case_88": cases.get("88", "n/a"),
        "case_97": cases.get("97", "n/a"),
        "case_100": cases.get("100", "n/a"),
        "case_110": cases.get("110", "n/a"),
        "case_155": cases.get("155", "n/a"),
        "case_166": cases.get("166", "n/a"),
    }


def case_delta_rows(rule_id: str, baseline_eval: dict[str, Any], candidate_eval: dict[str, Any], removals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    base_by_image = {item["image_filename"]: item for item in baseline_eval["images"]}
    cand_by_image = {item["image_filename"]: item for item in candidate_eval["images"]}
    rows = []
    for image_filename, base in base_by_image.items():
        cand = cand_by_image[image_filename]
        rows.append(
            {
                "rule_id": rule_id,
                "image_filename": image_filename,
                "case_id": v038.case_num(image_filename),
                "baseline_matches": base["match_count"],
                "baseline_false_negatives": base["false_negative_count"],
                "baseline_false_positives": base["false_positive_count"],
                "post_matches": cand["match_count"],
                "post_false_negatives": cand["false_negative_count"],
                "post_false_positives": cand["false_positive_count"],
                "delta_matches": cand["match_count"] - base["match_count"],
                "delta_false_negatives": cand["false_negative_count"] - base["false_negative_count"],
                "delta_false_positives": cand["false_positive_count"] - base["false_positive_count"],
                "removed_labels": ",".join(r["removed_label"] for r in removals if r["image_filename"] == image_filename),
            }
        )
    return rows


def status_block(phase: str, best: dict[str, Any] | None, decision: str, lesson: str, next_action: str) -> None:
    if best:
        metrics = best["metrics"]
        metric_text = f"{metrics['matches']}/{metrics['false_negatives']}/{metrics['false_positives']}/{metrics['combined_errors']}"
        best_rule = best["rule_id"]
        vs_v034a = metrics["combined_errors"] - V034A_BASELINE["combined_errors"]
        vs_v040 = metrics["combined_errors"] - V040_HYBRID["combined_errors"]
        vs_old = metrics["combined_errors"] - OLD_V020C["combined_errors"]
        cases = best["case_metrics"]
        removed = len(best["removals"])
        removed_tps = best["removed_true_positives"]
    else:
        metric_text = "n/a"
        best_rule = "n/a"
        vs_v034a = "n/a"
        vs_v040 = "n/a"
        vs_old = "n/a"
        cases = {}
        removed = "n/a"
        removed_tps = "n/a"
    print("=== V041 STATUS ===", flush=True)
    print(f"phase: {phase}", flush=True)
    print(f"best_rule: {best_rule}", flush=True)
    print(f"metrics: {metric_text}", flush=True)
    print(f"vs_v034a_delta: {vs_v034a}", flush=True)
    print(f"vs_v040_hybrid_delta: {vs_v040}", flush=True)
    print(f"vs_old_v020c_58_delta: {vs_old}", flush=True)
    print(f"case_66: {cases.get('66', 'n/a')}", flush=True)
    print(f"case_67: {cases.get('67', 'n/a')}", flush=True)
    print(f"case_84: {cases.get('84', 'n/a')}", flush=True)
    print(f"case_88: {cases.get('88', 'n/a')}", flush=True)
    print(f"case_100: {cases.get('100', 'n/a')}", flush=True)
    print(f"case_110: {cases.get('110', 'n/a')}", flush=True)
    print(f"case_155: {cases.get('155', 'n/a')}", flush=True)
    print(f"removed_predictions: {removed}", flush=True)
    print(f"removed_true_positives: {removed_tps}", flush=True)
    print(f"decision: {decision}", flush=True)
    print(f"main_lesson: {lesson}", flush=True)
    print(f"next_action: {next_action}", flush=True)
    print("===================", flush=True)


def write_common_docs() -> None:
    source_artifacts = [
        "docs/.../v040_fp8_experiment_only_duplicate_postprocessing/final_recommendation.md",
        "docs/.../v040_fp8_experiment_only_duplicate_postprocessing/r019_vs_r020_tradeoff.md",
        "docs/.../v040_fp8_experiment_only_duplicate_postprocessing/postprocess_validation_results.csv",
        "docs/.../v040_fp8_experiment_only_duplicate_postprocessing/failure_analysis.md",
        "docs/.../v039_fp8_containment_first_duplicate_suppression/final_recommendation.md",
        "docs/.../v039_fp8_containment_first_duplicate_suppression/best_simulation_report.md",
        "docs/.../v034_fp8_vllm_precision_recovery_autonomous/final_recommendation.md",
        "z_reference_docs/GPT-Pro_collab/bda_svc_qwen_prompt_engineering_deep_research_bundle.md",
        "z_reference_docs/GPT-Pro_collab/CODEX_QWEN_PROMPT_ENGINEERING_DIRECTION_2026-05-06.md",
    ]
    write_json(
        PACKAGE_ROOT / "source_manifest.json",
        {
            "generated_at": utc_now(),
            "package": "v041_fp8_prediction_only_duplicate_suppression",
            "frozen_artifacts_only": True,
            "vlm_called": False,
            "prompt_candidate_authored": False,
            "product_runtime_modified": False,
            "source_artifacts": source_artifacts,
            "v034a_run_root": str(v038.V034_RUN_ROOT),
            "manifest": str(v038.ALL_CURRENT_MANIFEST),
            "graphify_recall": {
                "attempted": True,
                "status": "blocked",
                "error": "ModuleNotFoundError: No module named 'networkx'",
            },
            "hard_boundaries": {
                "no_promotion": True,
                "no_product_truth_mutation": True,
                "no_runtime_code_mutation": True,
                "no_eval_ground_truth_mutation": True,
                "no_v024o_scored_evidence": True,
                "no_vlm_calls": True,
                "no_prompt_candidate": True,
                "no_graphify_or_mem0_update": True,
            },
        },
    )
    write_json(
        PACKAGE_ROOT / "oracle_to_deployable_gap.json",
        {
            "generated_at": utc_now(),
            "oracle_dependent_v039_v040_fields": [
                "larger_matched",
                "smaller_matched",
                "both_overlap_distinct_refs",
                "smaller_has_better_ref_iou",
                "removed_best_ref_iou",
                "larger_best_ref_iou",
                "matched/unmatched state",
                "reference boxes",
            ],
            "deployable_fields": [
                "predicted boxes",
                "predicted target_type",
                "bbox geometry",
                "area ratios",
                "containment",
                "IoU between predictions",
                "center-inside relation",
                "image dimensions",
                "prediction labels/order",
            ],
            "risk_after_de_oracle": "without match/reference guards, a geometry-only rule may suppress a true positive or a distinct valid target",
            "mitigation": "score after suppression only, reject any rule that removes TPs, reduces matches, increases FNs, or harms dense/control cases",
        },
    )
    write_text(
        PACKAGE_ROOT / "oracle_to_deployable_gap.md",
        "# v041 Oracle-To-Deployable Gap\n\n"
        "v039/v040 proved that containment-first duplicate suppression can reduce FP8 false positives, but the strongest rules used oracle fields: matched/unmatched state, larger-box matched status, distinct-reference overlap, and best reference IoU. Those fields are valid for offline simulation but unavailable at inference time.\n\n"
        "v041 therefore restricts rule logic to prediction-only information: predicted boxes, target types, geometry, area ratios, containment, pairwise IoU, center-inside relation, image dimensions, and prediction labels/order. Reference and match data are used only after suppression to score the result and audit whether the rule removed a true positive.\n",
    )
    status_block("oracle_gap", None, "n/a", "Oracle-only fields were separated from deployable prediction-only geometry.", "Define and run prediction-only rule families.")


def main() -> int:
    for dirname in ["scripts", "tables", "review_images"]:
        (PACKAGE_ROOT / dirname).mkdir(parents=True, exist_ok=True)

    write_common_docs()

    cases = v038.load_manifest_cases()
    image_order = [case["image_filename"] for case in cases]
    references = v038.load_reference_reports(cases)
    predictions = v038.load_predicted_reports()
    dims = image_dimensions(cases)
    baseline_eval = evaluate_reports(references, predictions, image_order)
    baseline_cases = case_metrics(baseline_eval)
    office_summary = v038.read_json(v038.V034_OFFICE_RUN_ROOT / "eval/evaluation_2026-05-09_030200Z_summary.json")
    office_pass = office_summary["totals"]["false_positive_count"] == 0

    pairs_by_image = {
        image_filename: pair_features_prediction_only(predictions[image_filename], dims.get(image_filename))
        for image_filename in image_order
    }
    pair_rows = [{"image_filename": image_filename, "case_id": v038.case_num(image_filename), **row} for image_filename, rows in pairs_by_image.items() for row in rows]
    write_json(PACKAGE_ROOT / "tables/prediction_only_pair_features.json", pair_rows)

    rules = rule_grid()
    write_json(
        PACKAGE_ROOT / "prediction_only_rule_specs.json",
        {
            "generated_at": utc_now(),
            "rule_count": len(rules),
            "rule_logic_uses_oracle_fields": False,
            "containment_thresholds": CONTAINMENT_THRESHOLDS,
            "iou_thresholds": ["none" if value is None else value for value in IOU_THRESHOLDS],
            "area_ratio_thresholds": AREA_RATIO_THRESHOLDS,
            "center_inside_required": True,
            "same_label_required_variants": [True, False],
            "cross_label_variants": {
                "cross_area_ratio_thresholds": CROSS_AREA_RATIO_THRESHOLDS,
                "cross_containment_thresholds": CROSS_CONTAINMENT_THRESHOLDS,
                "removed_not_only_type_options": CROSS_NOT_ONLY_TYPE_OPTIONS,
                "larger_image_area_max_ratio_options": LARGER_IMAGE_AREA_MAX_THRESHOLDS,
            },
            "keep_largest_only_options": KEEP_LARGEST_ONLY_OPTIONS,
            "never_suppress_if_smaller_contains_prediction_options": NEVER_SUPPRESS_IF_SMALLER_CONTAINS_OPTIONS,
        },
    )
    write_text(
        PACKAGE_ROOT / "prediction_only_rule_specs.md",
        "# v041 Prediction-Only Rule Specs\n\n"
        f"The grid contains `{len(rules)}` deployable geometry rules. Every rule uses prediction-only fields only. Same-label rules test strict nested duplicate suppression. Cross-label rules are allowed only under extra geometry constraints: small area ratio, high containment, optional not-only-type requirement, and optional larger-box image-area cap.\n",
    )
    write_json(
        PACKAGE_ROOT / "simulation_plan.json",
        {
            "generated_at": utc_now(),
            "method": "apply_prediction_only_rule_to_frozen_v034a_predictions_then_score_with_bda_eval",
            "uses_vlm": False,
            "uses_prompt_candidates": False,
            "rule_logic_uses_ground_truth": False,
            "ground_truth_used_only_for_after_the_fact_scoring": True,
            "safety_gates": [
                "reject_fn_increase",
                "reject_match_decrease",
                "reject_case_66_worse",
                "reject_case_67_worse",
                "reject_case_84_worse",
                "reject_case_110_worse",
                "reject_155_166_office_harm",
                "reject_removed_true_positive",
            ],
        },
    )
    write_text(
        PACKAGE_ROOT / "simulation_plan.md",
        "# v041 Simulation Plan\n\n"
        "Apply each prediction-only rule to frozen v034a predictions in memory, then recompute `bda_eval` detection-study matching. Ground truth and match labels are not available to the rule; they are used only after suppression for scoring and auditing.\n",
    )
    status_block("rule_spec", None, "n/a", "Prediction-only geometry rule families were defined without oracle fields.", "Run cached grid evaluation.")

    eval_cache: dict[tuple[tuple[str, str], ...], tuple[dict[str, Any], dict[str, dict[str, Any]]]] = {}
    results = [
        summarize_rule(rule, references, predictions, image_order, pairs_by_image, baseline_eval, baseline_cases, office_pass, eval_cache)
        for rule in rules
    ]
    rows = [row_for_result(result) for result in results]
    compact_grid_json = {
        "generated_at": utc_now(),
        "note": "Compact grid JSON stores row-level metrics only; full per-rule removal objects are intentionally omitted to keep the evidence package GitHub-safe.",
        "rule_count": len(results),
        "rows": rows,
    }
    write_json(PACKAGE_ROOT / "prediction_only_grid_results.json", compact_grid_json)
    write_csv(PACKAGE_ROOT / "prediction_only_grid_results.csv", rows)
    write_csv(PACKAGE_ROOT / "tables/prediction_only_grid_results.csv", rows)

    safe_results = [result for result in results if result["safe"]]
    ranked = sorted(
        safe_results,
        key=lambda result: (
            result["metrics"]["combined_errors"],
            result["metrics"]["false_positives"],
            result["metrics"]["false_negatives"],
            result["rule"]["same_label_required"] is False,
            result["rule"]["cross_label_allowed"] is True,
            result["removed_true_positives"],
            -result["removed_false_positives"],
            result["rule"]["area_ratio_threshold"],
            result["rule"]["containment_threshold"],
            999.0 if result["rule"]["iou_threshold"] is None else result["rule"]["iou_threshold"],
        ),
    )
    best = ranked[0] if ranked else None
    status_block(
        "simulation_grid",
        best,
        "n/a",
        "Prediction-only grid finished; safe rules were ranked against v034a and v040 oracle results.",
        "Analyze whether any deployable rule reproduces r019 or r020/hybrid.",
    )

    if not best:
        decision = "E"
        decision_text = "Prediction-only rules are too weak/no-op after removing oracle features."
        top_safe = []
    else:
        top_safe = ranked[:25]
        if best["metrics"]["combined_errors"] == V040_HYBRID["combined_errors"]:
            decision = "A"
            decision_text = "Prediction-only rule matches hybrid/r020 at 181/38/22/60 safely."
        elif best["metrics"]["combined_errors"] == V040_R019["combined_errors"] and best["rule"]["same_label_required"]:
            decision = "B"
            decision_text = "Prediction-only same-label rule matches r019 at 181/38/23/61 safely."
        elif best["metrics"]["combined_errors"] < V034A_BASELINE["combined_errors"]:
            decision = "C"
            decision_text = "Prediction-only rule improves v034a but does not match oracle results."
        else:
            any_unsafe_improving = any(
                result["metrics"]["combined_errors"] < V034A_BASELINE["combined_errors"]
                and (result["removed_true_positives"] > 0 or not result["safe"])
                for result in results
            )
            if any_unsafe_improving:
                decision = "D"
                decision_text = "Prediction-only rules are unsafe because improvements require TP/control harm."
            else:
                decision = "E"
                decision_text = "Prediction-only rules are too weak/no-op after removing oracle features."

    if best:
        best_key = removal_key(best["removals"])
        best_eval, _ = eval_cache[best_key]
        case_rows = case_delta_rows(best["rule_id"], baseline_eval, best_eval, best["removals"])
        removed_audit = best["removals"]
    else:
        case_rows = []
        removed_audit = []

    write_json(PACKAGE_ROOT / "best_prediction_only_rule.json", {"generated_at": utc_now(), "best_rule": best, "top_safe_rules": top_safe, "decision": decision})
    write_text(
        PACKAGE_ROOT / "best_prediction_only_rule.md",
        "# v041 Best Prediction-Only Rule\n\n"
        + (
            f"Best rule: `{best['rule_id']}`\n\n"
            f"Metrics: `{best['metrics']['matches']}/{best['metrics']['false_negatives']}/{best['metrics']['false_positives']}/{best['metrics']['combined_errors']}`.\n\n"
            f"Removed predictions: `{len(best['removals'])}`; removed true positives: `{best['removed_true_positives']}`.\n\n"
            f"Rule: `{json.dumps(best['rule'], sort_keys=True)}`\n"
            if best
            else "No safe improving prediction-only rule was found.\n"
        ),
    )
    write_csv(PACKAGE_ROOT / "case_level_delta_report.csv", case_rows)
    write_text(PACKAGE_ROOT / "case_level_delta_report.md", "# v041 Case-Level Delta Report\n\nSee `case_level_delta_report.csv`.\n")
    write_csv(PACKAGE_ROOT / "removed_prediction_audit.csv", removed_audit)
    write_text(
        PACKAGE_ROOT / "removed_prediction_audit.md",
        "# v041 Removed Prediction Audit\n\n"
        "The audit lists removals for the selected best prediction-only rule and annotates TP/FP effects after scoring. Rule logic did not use those eval annotations.\n",
    )

    matched_r020 = bool(best and best["metrics"]["combined_errors"] == V040_HYBRID["combined_errors"])
    matched_r019 = bool(best and best["metrics"]["combined_errors"] == V040_R019["combined_errors"] and best["rule"]["same_label_required"])
    removes_tp = int(best["removed_true_positives"]) if best else 0
    cross_label_acceptable = bool(best and not any(row["cross_label"] for row in best["removals"]))
    case155_fixed_results = [result for result in results if result["case_metrics"].get("155") == "2/0/0"]
    safe_case155_fixed_results = [result for result in case155_fixed_results if result["safe"]]
    best_safe_case155_fix = min(
        safe_case155_fixed_results,
        key=lambda result: (result["metrics"]["combined_errors"], len(result["removals"]), result["rule"]["same_label_required"] is False),
        default=None,
    )
    both_88_155_results = [
        result for result in results if {"88", "155"} <= {row["case_id"] for row in result["removals"]}
    ]
    safe_both_88_155_results = [result for result in both_88_155_results if result["safe"]]
    minimal_both_88_155 = min(
        both_88_155_results,
        key=lambda result: (result["removed_true_positives"], len(result["removals"]), result["metrics"]["combined_errors"]),
        default=None,
    )
    next_work = (
        "v042_experiment_only_postprocessing_integration_on_future_fp8_outputs"
        if decision in {"A", "B", "C"}
        else "stop_duplicate_suppression_and_consider_fiftyone_or_crop_verifier"
    )
    autonomous_prompt_with_postprocessed_scoring = decision in {"A", "B", "C"}

    failure = {
        "generated_at": utc_now(),
        "decision": decision,
        "safety_summary": {
            "safe_rule_count": len(safe_results),
            "unsafe_rule_count": len(results) - len(safe_results),
            "unsafe_improving_count": sum(1 for result in results if result["metrics"]["combined_errors"] < V034A_BASELINE["combined_errors"] and not result["safe"]),
            "case155_fixed_rule_count": len(case155_fixed_results),
            "safe_case155_fixed_rule_count": len(safe_case155_fixed_results),
            "both_88_155_rule_count": len(both_88_155_results),
            "safe_both_88_155_rule_count": len(safe_both_88_155_results),
        },
        "best_removed_true_positives": removes_tp,
        "cross_label_result": "accepted_only_if_best_removals_are_same_label" if cross_label_acceptable else "cross_label_removal_present_or_no_best",
        "de_oracle_loss_mode": {
            "summary": "A safe prediction-only rule can remove case 155 alone, but no safe rule removed both the case-88 and case-155 FPs that r019 removed; broadening enough to catch both also catches a case-159 TP.",
            "best_safe_case155_fix_rule": None if best_safe_case155_fix is None else best_safe_case155_fix["rule_id"],
            "best_safe_case155_fix_metrics": None if best_safe_case155_fix is None else best_safe_case155_fix["metrics"],
            "best_safe_case155_fix_removals": None if best_safe_case155_fix is None else best_safe_case155_fix["removals"],
            "minimal_both_88_155_rule": None if minimal_both_88_155 is None else minimal_both_88_155["rule_id"],
            "minimal_both_88_155_metrics": None if minimal_both_88_155 is None else minimal_both_88_155["metrics"],
            "minimal_both_88_155_removed_true_positives": None if minimal_both_88_155 is None else minimal_both_88_155["removed_true_positives"],
            "minimal_both_88_155_removals": None if minimal_both_88_155 is None else minimal_both_88_155["removals"],
        },
    }
    write_json(PACKAGE_ROOT / "failure_analysis.json", failure)
    write_text(
        PACKAGE_ROOT / "failure_analysis.md",
        "# v041 Failure Analysis\n\n"
        f"- Safe rules: `{len(safe_results)}`.\n"
        f"- Best rule removed true positives: `{removes_tp}`.\n"
        f"- Best rule matched r020/hybrid: `{matched_r020}`.\n"
        f"- Best rule matched r019: `{matched_r019}`.\n"
        f"- Cross-label suppression acceptable for selected rule: `{cross_label_acceptable}`.\n"
        + f"- Rules that fixed case 155: `{len(case155_fixed_results)}`; safe case-155-fixing rules: `{len(safe_case155_fixed_results)}`.\n"
        + f"- Rules that removed both case 88 and case 155: `{len(both_88_155_results)}`; safe rules removing both: `{len(safe_both_88_155_results)}`.\n"
        + "- Main de-oracle loss mode: case 155 is separable as a one-FP safe rule, but combining case 88 and 155 without oracle checks also catches a case-159 true positive.\n",
    )

    final = {
        "generated_at": utc_now(),
        "decision": decision,
        "decision_text": decision_text,
        "best_rule": None if best is None else best["rule_id"],
        "best_metrics": None if best is None else best["metrics"],
        "matched_r020_hybrid": matched_r020,
        "matched_r019": matched_r019,
        "removed_true_positives": removes_tp,
        "removed_predictions": [] if best is None else best["removals"],
        "cross_label_suppression_acceptable": cross_label_acceptable,
        "case155_fixed_rule_count": len(case155_fixed_results),
        "safe_case155_fixed_rule_count": len(safe_case155_fixed_results),
        "best_safe_case155_rule": None if best_safe_case155_fix is None else best_safe_case155_fix["rule_id"],
        "best_safe_case155_metrics": None if best_safe_case155_fix is None else best_safe_case155_fix["metrics"],
        "best_safe_case155_removed_predictions": None if best_safe_case155_fix is None else best_safe_case155_fix["removals"],
        "safe_both_88_155_rule_count": len(safe_both_88_155_results),
        "de_oracle_loss_mode": "case155 duplicate removal is separable as a one-FP rule, but r019-style two-FP removal was not separable from a case-159 TP using this prediction-only geometry grid",
        "next_work": next_work,
        "autonomous_prompt_refinement_can_resume_with_postprocessed_scoring_as_separate_experimental_objective": autonomous_prompt_with_postprocessed_scoring,
        "hard_boundaries_preserved": True,
        "old_v020c_reference": OLD_V020C,
        "fp8_baseline": FP8_BASELINE,
        "v034a_prompt_working_best": V034A_BASELINE,
        "v040_hybrid_oracle_score": V040_HYBRID,
        "v024o_status": "partial_unscored_forbidden",
    }
    write_json(PACKAGE_ROOT / "final_recommendation.json", final)
    write_text(
        PACKAGE_ROOT / "final_recommendation.md",
        "# v041 Final Recommendation\n\n"
        f"Generated: `{utc_now()}`\n\n"
        f"Decision `{decision}`: {decision_text}\n\n"
        + (
            f"Best prediction-only rule: `{best['rule_id']}`.\n"
            f"Best metrics: `{best['metrics']['matches']}/{best['metrics']['false_negatives']}/{best['metrics']['false_positives']}/{best['metrics']['combined_errors']}`.\n"
            f"Removed predictions: `{len(best['removals'])}`; removed true positives: `{best['removed_true_positives']}`.\n\n"
            if best
            else "No safe improving prediction-only rule was found.\n\n"
        )
        + f"Matched r020/hybrid: `{matched_r020}`.\n"
        f"Matched r019: `{matched_r019}`.\n"
        f"Cross-label suppression acceptable for selected rule: `{cross_label_acceptable}`.\n\n"
        f"Next work: `{next_work}`.\n\n"
        "This is experiment-only evidence. It does not modify product runtime, prompts, doctrine, assessment prompt, eval truth, or source truth.\n",
    )
    write_json(
        PACKAGE_ROOT / "recovery_log.json",
        {
            "generated_at": utc_now(),
            "steps": [
                "Read v040/v039/v034 source artifacts.",
                "Attempted Graphify recall; blocked by missing networkx.",
                "Separated oracle fields from deployable prediction-only fields.",
                "Built prediction-only rule grid and cached evaluation by removal set.",
                "Scored frozen v034a outputs after suppression only.",
                "Wrote final recommendation and validation artifacts.",
            ],
        },
    )
    write_text(
        PACKAGE_ROOT / "recovery_log.md",
        "# v041 Recovery Log\n\n"
        "- Read v040, v039, and v034 source artifacts.\n"
        "- Graphify recall was attempted and blocked by missing `networkx`.\n"
        "- Built and ran prediction-only duplicate suppression simulation over frozen v034a predictions.\n"
        "- No VLM calls or prompt candidates were used.\n",
    )
    write_text(
        PACKAGE_ROOT / "lessons_learned.md",
        "# v041 Lessons Learned\n\n"
        "- Oracle duplicate suppression must be de-risked before any deployable integration claim.\n"
        "- Same-label containment is the first safe deployable proxy to compare against r019.\n"
        "- Cross-label geometry needs stronger constraints or visual review because reference-IoU guards are not deployable.\n",
    )
    write_text(
        PACKAGE_ROOT / "strategy_state.md",
        "# v041 Strategy State\n\n"
        f"- Old/product v020c reference remains `{OLD_V020C['matches']}/{OLD_V020C['false_negatives']}/{OLD_V020C['false_positives']}/{OLD_V020C['combined_errors']}`.\n"
        f"- FP8 baseline remains `{FP8_BASELINE['matches']}/{FP8_BASELINE['false_negatives']}/{FP8_BASELINE['false_positives']}/{FP8_BASELINE['combined_errors']}`.\n"
        f"- v034a prompt working best remains `{V034A_BASELINE['matches']}/{V034A_BASELINE['false_negatives']}/{V034A_BASELINE['false_positives']}/{V034A_BASELINE['combined_errors']}`.\n"
        f"- v040 hybrid oracle score remains `{V040_HYBRID['matches']}/{V040_HYBRID['false_negatives']}/{V040_HYBRID['false_positives']}/{V040_HYBRID['combined_errors']}`.\n"
        f"- v041 decision: `{decision}`.\n"
    )
    write_text(
        PACKAGE_ROOT / "README.md",
        "# v041 FP8 Prediction-Only Duplicate Suppression\n\n"
        "This package converts v040 oracle duplicate suppression into deployable prediction-only geometry simulations over frozen v034a FP8 outputs. It does not run the VLM, author prompts, modify product runtime, or mutate eval truth.\n\n"
        f"Decision: `{decision}`.\n"
    )
    status_block("best_rule_analysis", best, decision, decision_text, next_work)
    status_block("final_decision", best, decision, decision_text, next_work)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
