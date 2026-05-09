#!/usr/bin/env python3
"""v043 offline residual-error verifier/postprocessing loop."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import importlib.util
import itertools
import json
import math
import statistics
import sys
from copy import deepcopy
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml


WORKTREE_ROOT = Path("/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement")
CAPSTONE_ROOT = Path("/home/williambenitez1/Capstone")
PARENT_ROOT = WORKTREE_ROOT / (
    "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion"
)
PACKAGE_ROOT = PARENT_ROOT / "v043_fp8_residual_error_verifier_postprocess_loop"
V042_SCRIPT = PARENT_ROOT / "v042_fp8_postprocessed_scoring_autonomous/scripts/run_v042_postprocessed_scoring.py"


spec = importlib.util.spec_from_file_location("v043_v042", V042_SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot import v042 helpers from {V042_SCRIPT}")
v042 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = v042
spec.loader.exec_module(v042)
v041 = v042.v041
v038 = v042.v038


OLD_V020C = {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58}
RAW_V034A = {"matches": 181, "false_negatives": 38, "false_positives": 25, "combined_errors": 63}
P1753_COMPOSITE = {"matches": 181, "false_negatives": 38, "false_positives": 24, "combined_errors": 62}
V040_HYBRID_ORACLE = {"matches": 181, "false_negatives": 38, "false_positives": 22, "combined_errors": 60}
WATCH_CASES = ["66", "67", "84", "97", "100", "110", "155", "166"]
DENSE_CASES = {"66", "67", "84", "97"}
CONTROL_CASES = {"155", "166"}


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None and rows:
        fieldnames = list(rows[0].keys())
    if not fieldnames:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def metrics_string(metrics: dict[str, Any] | None) -> str:
    if not metrics:
        return "n/a"
    return f"{metrics.get('matches')}/{metrics.get('false_negatives')}/{metrics.get('false_positives')}/{metrics.get('combined_errors')}"


def case_num(image_filename: str) -> str:
    return Path(image_filename).stem.lstrip("0") or "0"


def case_metric_map(eval_payload: dict[str, Any]) -> dict[str, str]:
    return {
        case_num(img["image_filename"]): f"{img['match_count']}/{img['false_negative_count']}/{img['false_positive_count']}"
        for img in eval_payload["images"]
    }


def parse_metric(text: str) -> tuple[int, int, int]:
    a, b, c = text.split("/")
    return int(a), int(b), int(c)


def is_worse(candidate: str, baseline: str) -> bool:
    c = parse_metric(candidate)
    b = parse_metric(baseline)
    return c[0] < b[0] or c[1] > b[1] or c[2] > b[2]


def target_box(target: dict[str, Any]) -> tuple[float, float, float, float]:
    return v038.box_from_target_dict(target)


def box_area(box: tuple[float, float, float, float]) -> float:
    return v038.area(box)


def target_type(target: dict[str, Any]) -> str:
    return str(target.get("target_type", "unknown"))


def get_target(report: dict[str, Any], label: str) -> dict[str, Any] | None:
    return report.get("physical_damage", {}).get(label)


def image_dims(cases: list[dict[str, Any]]) -> dict[str, tuple[int, int]]:
    return v041.image_dimensions(cases)


def load_state() -> dict[str, Any]:
    references, image_order, cases = v042.load_reference_reports(v042.ALL_CURRENT_MANIFEST)
    raw_predictions = v042.load_predicted_reports(v042.V034_FULL_RUN_ROOT / "predicted")
    raw_eval = v042.evaluate_reports(references, raw_predictions, image_order)
    p1753_payload = v042.apply_p1753_to_reports(references, raw_predictions, image_order, cases)
    composite_predictions = p1753_payload["postprocessed_reports"]
    composite_eval = p1753_payload["post_eval"]
    dims = image_dims(cases)
    return {
        "references": references,
        "image_order": image_order,
        "cases": cases,
        "raw_predictions": raw_predictions,
        "raw_eval": raw_eval,
        "composite_predictions": composite_predictions,
        "composite_eval": composite_eval,
        "p1753_removals": p1753_payload["removals"],
        "dims": dims,
    }


def pair_features_for_image(prediction: dict[str, Any], dims: tuple[int, int] | None) -> list[dict[str, Any]]:
    return v041.pair_features_prediction_only(prediction, dims)


def inventory_rows(state: dict[str, Any]) -> list[dict[str, Any]]:
    refs = state["references"]
    preds = state["composite_predictions"]
    eval_payload = state["composite_eval"]
    dims = state["dims"]
    rows: list[dict[str, Any]] = []
    for image in eval_payload["images"]:
        image_filename = image["image_filename"]
        case_id = case_num(image_filename)
        pred_report = preds[image_filename]
        ref_report = refs[image_filename]
        pred_pairs = pair_features_for_image(pred_report, dims.get(image_filename))
        pair_by_small: dict[str, list[dict[str, Any]]] = {}
        for pair in pred_pairs:
            pair_by_small.setdefault(pair["smaller_label"], []).append(pair)

        for label in image["false_positive_labels"]:
            target = get_target(pred_report, label) or {}
            box = target_box(target) if target else (0.0, 0.0, 0.0, 0.0)
            area = box_area(box)
            img_area = None
            if dims.get(image_filename):
                img_area = max(1, dims[image_filename][0] * dims[image_filename][1])
            pairs = pair_by_small.get(label, [])
            best_containment = max([p["containment_ratio"] for p in pairs], default=0.0)
            best_iou = max([p["iou"] for p in pairs], default=0.0)
            class_name = classify_fp(case_id, target_type(target), area / img_area if img_area else None, best_containment, best_iou)
            rows.append(
                {
                    "case_id": case_id,
                    "image_filename": image_filename,
                    "label": label,
                    "target_type": target_type(target),
                    "error_type": "FP",
                    "bbox": json.dumps(list(box)),
                    "likely_failure_class": class_name,
                    "prediction_only_geometry_addressable": str(class_name in {"contained_duplicate_prediction", "oversized_group_box", "broad_context_scene_box", "nested_local_context_box"}).lower(),
                    "crop_verifier_addressable": "true",
                    "prompt_wording_addressable": str(class_name in {"prompt_addressable", "broad_context_scene_box"}).lower(),
                    "visual_review_needed": "true",
                    "dense_case_risk": str(case_id in DENSE_CASES).lower(),
                    "case110_risk": str(case_id == "110").lower(),
                    "control_case_effect": str(case_id in CONTROL_CASES).lower(),
                    "notes": f"area={area:.1f}; containment={best_containment:.3f}; iou={best_iou:.3f}",
                }
            )
        for label in image["false_negative_labels"]:
            target = get_target(ref_report, label) or {}
            box = target_box(target) if target else (0.0, 0.0, 0.0, 0.0)
            class_name = classify_fn(case_id, target_type(target), box_area(box))
            rows.append(
                {
                    "case_id": case_id,
                    "image_filename": image_filename,
                    "label": label,
                    "target_type": target_type(target),
                    "error_type": "FN",
                    "bbox": json.dumps(list(box)),
                    "likely_failure_class": class_name,
                    "prediction_only_geometry_addressable": "false",
                    "crop_verifier_addressable": "true",
                    "prompt_wording_addressable": str(class_name in {"small_valid_target_missed", "dense_valid_target_missed"}).lower(),
                    "visual_review_needed": "true",
                    "dense_case_risk": str(case_id in DENSE_CASES).lower(),
                    "case110_risk": str(case_id == "110").lower(),
                    "control_case_effect": str(case_id in CONTROL_CASES).lower(),
                    "notes": f"reference_area={box_area(box):.1f}",
                }
            )
    return rows


def classify_fp(case_id: str, ttype: str, image_area_ratio: float | None, containment: float, iou: float) -> str:
    if containment >= 0.80:
        return "contained_duplicate_prediction"
    if case_id in {"66", "67"}:
        return "adjacent_target_confusion"
    if case_id == "155":
        return "nested_local_context_box"
    if case_id in {"100"} and ttype == "buildings":
        return "building_or_structure_piece"
    if image_area_ratio is not None and image_area_ratio >= 0.10:
        return "oversized_group_box"
    if case_id in {"110", "103", "97"}:
        return "broad_context_scene_box"
    if ttype == "buildings":
        return "building_or_structure_piece"
    return "verifier_needed"


def classify_fn(case_id: str, ttype: str, area: float) -> str:
    if case_id in DENSE_CASES:
        return "dense_valid_target_missed"
    if case_id in {"110"}:
        return "smoke_or_debris_confusion"
    if area <= 2500:
        return "small_valid_target_missed"
    if ttype == "buildings":
        return "building_or_structure_piece"
    return "verifier_needed"


@dataclass(frozen=True)
class SimRule:
    rule_id: str
    family: str
    containment_threshold: float | None = None
    iou_threshold: float | None = None
    area_ratio_max: float | None = None
    same_label_required: bool = True
    cross_label_allowed: bool = False
    image_area_min: float | None = None
    image_area_max: float | None = None
    same_type_count_min: int | None = None
    area_vs_same_type_median_min: float | None = None
    target_type_filter: str | None = None
    center_inside_required: bool = True
    never_suppress_if_smaller_contains_prediction: bool = True


def build_rules() -> list[SimRule]:
    rules: list[SimRule] = []
    n = 0
    for containment, area_ratio, iou in itertools.product([0.70, 0.80, 0.90, 0.95, 1.0], [0.03, 0.05, 0.08, 0.10, 0.15, 0.20], [None, 0.0, 0.03, 0.05, 0.10]):
        n += 1
        rules.append(SimRule(f"pp{n:04d}", "same_label_containment", containment, iou, area_ratio, same_label_required=True))
    for max_area in [0.0005, 0.001, 0.002, 0.005, 0.01]:
        for count_min in [2, 3, 5, 8]:
            n += 1
            rules.append(SimRule(f"pp{n:04d}", "tiny_dense_prediction", image_area_max=max_area, same_type_count_min=count_min, target_type_filter="military_equipment"))
    for min_area in [0.05, 0.10, 0.15, 0.20, 0.30]:
        n += 1
        rules.append(SimRule(f"pp{n:04d}", "large_image_area_prediction", image_area_min=min_area))
    for mult in [3.0, 5.0, 8.0, 10.0]:
        for count_min in [3, 5, 8]:
            n += 1
            rules.append(SimRule(f"pp{n:04d}", "same_type_area_outlier", area_vs_same_type_median_min=mult, same_type_count_min=count_min))
    return rules


def prediction_items(prediction: dict[str, Any], dims: tuple[int, int] | None) -> list[dict[str, Any]]:
    items = v041.prediction_items(prediction, dims)
    by_type: dict[str, list[float]] = {}
    for item in items:
        by_type.setdefault(item["target_type"], []).append(item["area"])
    med = {key: statistics.median(vals) for key, vals in by_type.items() if vals}
    for item in items:
        item["same_type_median_area"] = med.get(item["target_type"], 0.0)
        item["area_vs_same_type_median"] = item["area"] / item["same_type_median_area"] if item["same_type_median_area"] else 0.0
    return items


def labels_for_rule(prediction: dict[str, Any], dims: tuple[int, int] | None, rule: SimRule) -> list[dict[str, Any]]:
    removals: list[dict[str, Any]] = []
    if rule.family == "same_label_containment":
        pairs = pair_features_for_image(prediction, dims)
        seen = set()
        for pair in sorted(pairs, key=lambda p: (p["smaller_label"], -p["large_area"])):
            if pair["smaller_label"] in seen:
                continue
            if pair["containment_ratio"] < (rule.containment_threshold or 0.0):
                continue
            if rule.iou_threshold is not None and pair["iou"] < rule.iou_threshold:
                continue
            if rule.area_ratio_max is not None and pair["area_ratio"] > rule.area_ratio_max:
                continue
            if rule.center_inside_required and not pair["center_inside_larger"]:
                continue
            if rule.never_suppress_if_smaller_contains_prediction and pair["smaller_contains_prediction"]:
                continue
            if rule.same_label_required and not pair["same_target_type"]:
                continue
            seen.add(pair["smaller_label"])
            removals.append(
                {
                    "removed_label": pair["smaller_label"],
                    "reason": rule.family,
                    "kept_larger_label": pair["larger_label"],
                    "removed_target_type": pair["removed_target_type"],
                    "kept_larger_target_type": pair["kept_larger_target_type"],
                    "removed_bbox": pair["removed_bbox"],
                    "kept_larger_bbox": pair["kept_larger_bbox"],
                    "containment_ratio": pair["containment_ratio"],
                    "iou": pair["iou"],
                    "area_ratio": pair["area_ratio"],
                    "image_area_ratio": None,
                    "area_vs_same_type_median": None,
                }
            )
        return removals

    for item in prediction_items(prediction, dims):
        if rule.target_type_filter and item["target_type"] != rule.target_type_filter:
            continue
        if rule.same_type_count_min is not None and item["type_count"] < rule.same_type_count_min:
            continue
        if rule.image_area_min is not None:
            ratio = item.get("image_area_ratio")
            if ratio is None or ratio < rule.image_area_min:
                continue
        if rule.image_area_max is not None:
            ratio = item.get("image_area_ratio")
            if ratio is None or ratio > rule.image_area_max:
                continue
        if rule.area_vs_same_type_median_min is not None and item.get("area_vs_same_type_median", 0.0) < rule.area_vs_same_type_median_min:
            continue
        removals.append(
            {
                "removed_label": item["label"],
                "reason": rule.family,
                "kept_larger_label": "",
                "removed_target_type": item["target_type"],
                "kept_larger_target_type": "",
                "removed_bbox": item["bbox"],
                "kept_larger_bbox": "",
                "containment_ratio": None,
                "iou": None,
                "area_ratio": None,
                "image_area_ratio": item.get("image_area_ratio"),
                "area_vs_same_type_median": item.get("area_vs_same_type_median"),
            }
        )
    return removals


def apply_sim_rule(predictions: dict[str, dict[str, Any]], dims: dict[str, tuple[int, int]], rule: SimRule) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    mutated = deepcopy(predictions)
    all_removals: list[dict[str, Any]] = []
    for image_filename, prediction in predictions.items():
        for removal in labels_for_rule(prediction, dims.get(image_filename), rule):
            label = removal["removed_label"]
            if label not in mutated[image_filename].get("physical_damage", {}):
                continue
            del mutated[image_filename]["physical_damage"][label]
            all_removals.append({"rule_id": rule.rule_id, "case_id": case_num(image_filename), "image_filename": image_filename, **removal})
    return mutated, all_removals


def annotate_removals(removals: list[dict[str, Any]], baseline_eval: dict[str, Any], candidate_eval: dict[str, Any]) -> list[dict[str, Any]]:
    base_maps = v038.matched_maps(baseline_eval)
    base_by_image = {item["image_filename"]: item for item in baseline_eval["images"]}
    cand_by_image = {item["image_filename"]: item for item in candidate_eval["images"]}
    rows = []
    for row in removals:
        image_filename = row["image_filename"]
        label = row["removed_label"]
        base = base_by_image[image_filename]
        cand = cand_by_image[image_filename]
        base_map = base_maps[image_filename]
        removed_tp = label in base_map["matched_preds"]
        removed_fp = label in base_map["false_positives"]
        rows.append(
            {
                **row,
                "removed_true_positive": removed_tp,
                "removed_false_positive": removed_fp,
                "case_delta_matches": cand["match_count"] - base["match_count"],
                "case_delta_false_negatives": cand["false_negative_count"] - base["false_negative_count"],
                "case_delta_false_positives": cand["false_positive_count"] - base["false_positive_count"],
            }
        )
    return rows


def safety_reasons(result: dict[str, Any], baseline_eval: dict[str, Any], baseline_cases: dict[str, str]) -> list[str]:
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
        if is_worse(result["case_metrics"].get(case_id, "0/999/999"), baseline_cases.get(case_id, "0/999/999")):
            reasons.append(f"case_{case_id}_worse")
    return reasons


def summarize_rule(rule: SimRule, state: dict[str, Any]) -> dict[str, Any]:
    post, removals = apply_sim_rule(state["composite_predictions"], state["dims"], rule)
    eval_payload = v042.evaluate_reports(state["references"], post, state["image_order"])
    annotated = annotate_removals(removals, state["composite_eval"], eval_payload)
    case_metrics = case_metric_map(eval_payload)
    result = {
        "intervention_id": rule.rule_id,
        "type": "postprocess_simulation",
        "stage": "offline_only",
        "rule": asdict(rule),
        "metrics": eval_payload["totals"],
        "case_metrics": case_metrics,
        "removals": annotated,
        "removed_predictions": len(annotated),
        "removed_true_positives": sum(1 for r in annotated if r["removed_true_positive"]),
        "removed_false_positives": sum(1 for r in annotated if r["removed_false_positive"]),
    }
    result["safety_reasons"] = safety_reasons(result, state["composite_eval"], case_metric_map(state["composite_eval"]))
    result["safe"] = not result["safety_reasons"]
    return result


def row_for_result(result: dict[str, Any]) -> dict[str, Any]:
    m = result["metrics"]
    c = result["case_metrics"]
    r = result["rule"]
    return {
        "intervention_id": result["intervention_id"],
        "type": result["type"],
        "family": r["family"],
        "matches": m["matches"],
        "false_negatives": m["false_negatives"],
        "false_positives": m["false_positives"],
        "combined_errors": m["combined_errors"],
        "image_count": m["image_count"],
        "vs_composite_62_delta": m["combined_errors"] - P1753_COMPOSITE["combined_errors"],
        "vs_old_v020c_58_delta": m["combined_errors"] - OLD_V020C["combined_errors"],
        "removed_predictions": result["removed_predictions"],
        "removed_true_positives": result["removed_true_positives"],
        "removed_false_positives": result["removed_false_positives"],
        "safe": result["safe"],
        "safety_reasons": ";".join(result["safety_reasons"]),
        "case_66": c.get("66", "n/a"),
        "case_67": c.get("67", "n/a"),
        "case_84": c.get("84", "n/a"),
        "case_97": c.get("97", "n/a"),
        "case_100": c.get("100", "n/a"),
        "case_110": c.get("110", "n/a"),
        "case_155": c.get("155", "n/a"),
        "case_166": c.get("166", "n/a"),
    }


def choose_best(results: list[dict[str, Any]]) -> dict[str, Any] | None:
    safe = [r for r in results if r["safe"]]
    if not safe:
        return None
    return sorted(safe, key=lambda r: (r["metrics"]["combined_errors"], r["metrics"]["false_positives"], r["removed_true_positives"], len(r["rule"]["family"])))[0]


def write_scaffold() -> None:
    for d in ["scripts", "tables", "postprocess_rules", "verifier_designs", "visual_review", "prompt_overlays", "runs"]:
        (PACKAGE_ROOT / d).mkdir(parents=True, exist_ok=True)
    write_json(
        PACKAGE_ROOT / "source_manifest.json",
        {
            "generated_at": utc_now(),
            "package": "v043_fp8_residual_error_verifier_postprocess_loop",
            "source_artifacts": [
                "z_reference_docs/GPT-Pro_collab/V042_FP8_POSTPROCESSED_SCORING_POINTER.md",
                str(PARENT_ROOT / "v042_fp8_postprocessed_scoring_autonomous/final_recommendation.md"),
                str(PARENT_ROOT / "v042_fp8_postprocessed_scoring_autonomous/comparison_matrix.md"),
                str(PARENT_ROOT / "v041_fp8_prediction_only_duplicate_suppression/final_recommendation.md"),
                str(PARENT_ROOT / "v040_fp8_experiment_only_duplicate_postprocessing/final_recommendation.md"),
                str(PARENT_ROOT / "v034_fp8_vllm_precision_recovery_autonomous/final_recommendation.md"),
                "z_reference_docs/GPT-Pro_collab/bda_svc_qwen_prompt_engineering_deep_research_bundle.md",
                "z_reference_docs/GPT-Pro_collab/CODEX_QWEN_PROMPT_ENGINEERING_DIRECTION_2026-05-06.md",
            ],
            "graphify_recall": {"attempted": True, "query": "v042 FP8 p1753 v034a residual errors", "status": "no_recall_match"},
            "frozen_artifacts_only": True,
            "vlm_called": False,
            "product_runtime_modified": False,
        },
    )
    write_json(PACKAGE_ROOT / "backend_preflight.json", {"generated_at": utc_now(), "backend_required_for_phase1": False, "vlm_called": False, "status": "offline_not_required"})
    write_text(PACKAGE_ROOT / "README.md", "# v043 FP8 Residual Error Verifier/Postprocess Loop\n\nExperiment-only residual-error inventory and offline prediction-only postprocessing simulation for the FP8 vLLM model line.\n")
    write_text(PACKAGE_ROOT / "recovery_log.md", "# v043 Recovery Log\n\n- Re-grounded in v042/v041/v040/v034 source artifacts.\n- Graphify recall attempted and returned no direct v042/v043 match.\n- Used frozen v034a and p1753 outputs only; no live VLM call.\n")
    write_json(PACKAGE_ROOT / "recovery_log.json", {"generated_at": utc_now(), "events": ["source_grounded", "offline_only", "no_vlm_call"]})


def write_inventory(rows: list[dict[str, Any]], state: dict[str, Any]) -> None:
    fields = [
        "case_id", "image_filename", "label", "target_type", "error_type", "bbox", "likely_failure_class",
        "prediction_only_geometry_addressable", "crop_verifier_addressable", "prompt_wording_addressable",
        "visual_review_needed", "dense_case_risk", "case110_risk", "control_case_effect", "notes",
    ]
    write_csv(PACKAGE_ROOT / "residual_error_taxonomy.csv", rows, fields)
    by_class: dict[str, int] = {}
    by_type: dict[str, int] = {}
    for row in rows:
        by_class[row["likely_failure_class"]] = by_class.get(row["likely_failure_class"], 0) + 1
        by_type[row["error_type"]] = by_type.get(row["error_type"], 0) + 1
    payload = {
        "generated_at": utc_now(),
        "baseline": {"raw_v034a": RAW_V034A, "v034a_plus_p1753": P1753_COMPOSITE},
        "totals": state["composite_eval"]["totals"],
        "residual_error_count": len(rows),
        "by_error_type": by_type,
        "by_failure_class": dict(sorted(by_class.items())),
        "priority_cases": {case: case_metric_map(state["composite_eval"]).get(case, "n/a") for case in WATCH_CASES},
        "rows": rows,
    }
    write_json(PACKAGE_ROOT / "residual_error_inventory.json", payload)
    write_text(
        PACKAGE_ROOT / "residual_error_inventory.md",
        "# v043 Residual Error Inventory\n\n"
        f"Composite baseline: `v034a + p1753 = {metrics_string(P1753_COMPOSITE)}`.\n\n"
        f"Residual errors inventoried: `{len(rows)}` (`{by_type.get('FN', 0)}` FNs, `{by_type.get('FP', 0)}` FPs).\n\n"
        "Failure classes:\n\n"
        + "\n".join(f"- `{k}`: {v}" for k, v in sorted(by_class.items()))
        + "\n",
    )


def write_verifier_design(rows: list[dict[str, Any]]) -> None:
    design = {
        "generated_at": utc_now(),
        "intervention_id": "vd001_crop_level_residual_verifier_design",
        "type": "verifier_design",
        "status": "design_only",
        "input": ["image crop around candidate box", "full image with bbox overlay", "candidate target_type", "neighbor boxes if any"],
        "output_schema": {
            "decision": "keep_prediction | suppress_prediction | needs_visual_review",
            "target_body_visible": "boolean",
            "box_mostly_target_body": "boolean",
            "duplicate_or_nested_context": "boolean",
            "broad_context_scene_box": "boolean",
            "rationale_short": "string",
        },
        "guardrails": [
            "Verifier is advisory and experiment-only.",
            "Do not suppress if target body visibility is uncertain in dense cases 66/67/84/97.",
            "Do not use ground truth at inference time.",
            "Score verifier decisions separately before product consideration.",
        ],
        "priority_failure_classes": sorted({r["likely_failure_class"] for r in rows if r["error_type"] == "FP"}),
    }
    write_json(PACKAGE_ROOT / "verifier_designs/crop_level_residual_verifier_design.json", design)
    write_text(
        PACKAGE_ROOT / "verifier_designs/crop_level_residual_verifier_design.md",
        "# Crop-Level Residual Verifier Design\n\n"
        "This design is experiment-only. It targets residual FPs that prediction-only geometry cannot safely separate, especially adjacent-target confusion, broad context boxes, and building/structure pieces.\n\n"
        "The verifier should receive a crop, the full overlay, the candidate target type, and neighbor-box context, then emit a small JSON decision. Dense cases require a conservative keep/needs-review bias rather than automatic suppression.\n",
    )
    print("=== V043 INTERVENTION COMPLETE ===")
    print("intervention: vd001_crop_level_residual_verifier_design")
    print("type: verifier_design")
    print("stage: offline_only")
    print("raw_metrics: n/a")
    print("postprocessed_metrics: n/a")
    print("vs_composite_62_delta: n/a")
    print("vs_old_v020c_58_delta: n/a")
    for case in ["66", "67", "84", "100", "110", "155", "166"]:
        print(f"case_{case}: n/a")
    print("office_negative: n/a")
    print("removed_predictions: n/a")
    print("removed_true_positives: n/a")
    print("status: design_only")
    print("main_lesson: Residual FPs need crop/verifier evidence because broad geometry cannot safely distinguish dense true targets from extra boxes.")
    print("next_axis: Build a FiftyOne or crop-review dataset before any live verifier suppression run.")
    print("===============================")


def print_intervention(result: dict[str, Any], status: str, lesson: str, next_axis: str) -> None:
    m = result["metrics"]
    c = result["case_metrics"]
    print("=== V043 INTERVENTION COMPLETE ===")
    print(f"intervention: {result['intervention_id']}")
    print("type: postprocess_simulation")
    print("stage: offline_only")
    print("raw_metrics: n/a")
    print(f"postprocessed_metrics: {metrics_string(m)}")
    print(f"vs_composite_62_delta: {m['combined_errors'] - P1753_COMPOSITE['combined_errors']}")
    print(f"vs_old_v020c_58_delta: {m['combined_errors'] - OLD_V020C['combined_errors']}")
    for case in ["66", "67", "84", "100", "110", "155", "166"]:
        print(f"case_{case}: {c.get(case, 'n/a')}")
    print("office_negative: n/a")
    print(f"removed_predictions: {result['removed_predictions']}")
    print(f"removed_true_positives: {result['removed_true_positives']}")
    print(f"status: {status}")
    print(f"main_lesson: {lesson}")
    print(f"next_axis: {next_axis}")
    print("===============================")


def write_results(results: list[dict[str, Any]], best: dict[str, Any] | None, rows: list[dict[str, Any]]) -> None:
    grid_rows = [row_for_result(r) for r in results]
    fields = list(grid_rows[0].keys()) if grid_rows else []
    write_csv(PACKAGE_ROOT / "tables/postprocess_simulation_grid.csv", grid_rows, fields)
    write_json(PACKAGE_ROOT / "tables/postprocess_simulation_grid.json", {"generated_at": utc_now(), "rows": grid_rows})
    write_json(PACKAGE_ROOT / "intervention_registry.json", {"generated_at": utc_now(), "interventions": grid_rows})
    write_json(PACKAGE_ROOT / "intervention_matrix.json", {"generated_at": utc_now(), "rows": grid_rows})
    write_text(
        PACKAGE_ROOT / "intervention_matrix.md",
        "# v043 Intervention Matrix\n\n"
        "| Intervention | Type | Family | Metrics | Removed | Removed TPs | Safe | Status |\n"
        "|---|---|---|---|---:|---:|---|---|\n"
        + "\n".join(
            f"| `{r['intervention_id']}` | postprocess_simulation | {r['family']} | `{r['matches']}/{r['false_negatives']}/{r['false_positives']}/{r['combined_errors']}` | {r['removed_predictions']} | {r['removed_true_positives']} | {r['safe']} | {'new_composite_working_best' if best and r['intervention_id'] == best['intervention_id'] and r['combined_errors'] < 62 else 'learning_evidence' if r['safe'] else 'rejected'} |"
            for r in grid_rows[:50]
        )
        + "\n",
    )
    if best:
        write_json(PACKAGE_ROOT / "postprocess_rules/best_prediction_only_residual_rule.json", {"generated_at": utc_now(), **best})
        write_text(PACKAGE_ROOT / "postprocess_rules/best_prediction_only_residual_rule.md", f"# Best Residual Rule\n\n`{best['intervention_id']}`: `{metrics_string(best['metrics'])}`.\n")

    status = "new_composite_working_best" if best and best["metrics"]["combined_errors"] < 62 else "learning_evidence"
    best_metrics = best["metrics"] if best and best["metrics"]["combined_errors"] < 62 else P1753_COMPOSITE
    best_name = best["intervention_id"] if best and best["metrics"]["combined_errors"] < 62 else "v034a+p1753"
    final = {
        "generated_at": utc_now(),
        "status": status,
        "best_composite_fp8_result": {"id": best_name, **best_metrics},
        "any_intervention_beat_62": bool(best and best["metrics"]["combined_errors"] < 62),
        "reached_or_beat_old_v020c_58": bool(best and best["metrics"]["combined_errors"] <= 58),
        "target_le_1_reached": bool(best and best["metrics"]["combined_errors"] <= 1),
        "winning_intervention_type": "postprocess_simulation" if best and best["metrics"]["combined_errors"] < 62 else "none",
        "remaining_residual_error_classes": sorted({r["likely_failure_class"] for r in rows}),
        "postprocessed_scoring_should_continue": True,
        "hard_boundaries_preserved": True,
        "next_axis": "Use visual/crop verifier review before any live verifier suppression or prompt mutation.",
    }
    write_json(PACKAGE_ROOT / "final_recommendation.json", final)
    write_text(
        PACKAGE_ROOT / "final_recommendation.md",
        "# v043 Final Recommendation\n\n"
        f"Generated: `{utc_now()}`\n\n"
        f"Best composite FP8 result: `{best_name}` at `{metrics_string(best_metrics)}`.\n\n"
        f"Any intervention beat 62 errors: `{final['any_intervention_beat_62']}`.\n"
        f"Reached or beat old 58-error reference: `{final['reached_or_beat_old_v020c_58']}`.\n"
        f"Reached <=1 target: `{final['target_le_1_reached']}`.\n\n"
        f"Winning intervention type: `{final['winning_intervention_type']}`.\n\n"
        "Remaining residual error classes: "
        + ", ".join(f"`{x}`" for x in final["remaining_residual_error_classes"])
        + ".\n\n"
        "Recommendation: continue postprocessed scoring, but move next to visual/crop verifier review. Do not resume near-neighbor prompt wording churn from v034a.\n",
    )
    write_text(
        PACKAGE_ROOT / "lessons_learned.md",
        "# v043 Lessons Learned\n\n"
        "- The residual inventory confirms p1753 leaves both dense missed targets and FP clusters; geometry-only suppression is high-risk around cases 66/67/84/110.\n"
        "- Prediction-only postprocessing must reject any rule that removes TPs, drops matches, increases FNs, or worsens dense/control cases.\n"
        "- Crop/verifier review is the next useful lever before prompt wording resumes.\n",
    )
    write_text(
        PACKAGE_ROOT / "strategy_state.md",
        "# v043 Strategy State\n\n"
        f"- Composite working best: `{best_name}` at `{metrics_string(best_metrics)}`.\n"
        "- Raw prompt working best remains `v034a = 181/38/25/63`.\n"
        "- Prompt wording remains paused.\n"
        "- Next axis: visual/crop verifier review of residual FP/FN classes.\n",
    )
    write_text(
        PACKAGE_ROOT / "live_metrics_log.md",
        "# v043 Live Metrics Log\n\n"
        + "\n".join(
            f"- `{r['intervention_id']}` `{r['family']}` metrics `{r['matches']}/{r['false_negatives']}/{r['false_positives']}/{r['combined_errors']}` safe `{r['safe']}`"
            for r in grid_rows[:50]
        )
        + "\n",
    )


def validate_files() -> dict[str, Any]:
    errors = []
    counts = {"json": 0, "csv": 0, "yaml": 0}
    for path in PACKAGE_ROOT.rglob("*.json"):
        counts["json"] += 1
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"json:{path}:{exc!r}")
    for path in PACKAGE_ROOT.rglob("*.csv"):
        counts["csv"] += 1
        try:
            with path.open("r", encoding="utf-8", newline="") as handle:
                list(csv.reader(handle))
        except Exception as exc:
            errors.append(f"csv:{path}:{exc!r}")
    for path in list(PACKAGE_ROOT.rglob("*.yaml")) + list(PACKAGE_ROOT.rglob("*.yml")):
        counts["yaml"] += 1
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"yaml:{path}:{exc!r}")
    result = {
        "generated_at": utc_now(),
        "counts": counts,
        "errors": errors,
        "ok": not errors,
        "baseline_confirmations": {
            "old_v020c": OLD_V020C,
            "raw_v034a": RAW_V034A,
            "p1753_on_v034a": P1753_COMPOSITE,
            "v040_hybrid_oracle_non_deployable": V040_HYBRID_ORACLE,
            "v024o_unscored": True,
        },
    }
    write_json(PACKAGE_ROOT / "validation_report.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if not args.run:
        parser.print_help()
        return 0
    write_scaffold()
    state = load_state()
    rows = inventory_rows(state)
    write_inventory(rows, state)
    results = [summarize_rule(rule, state) for rule in build_rules()]
    best = choose_best(results)
    if best:
        status = "new_composite_working_best" if best["metrics"]["combined_errors"] < 62 else "learning_evidence"
        lesson = (
            "Prediction-only residual postprocessing found a safe improvement."
            if best["metrics"]["combined_errors"] < 62
            else "Prediction-only residual postprocessing did not beat the p1753 composite baseline."
        )
        next_axis = "Use crop/verifier review to separate residual FPs that geometry-only rules cannot safely remove."
        print_intervention(best, status, lesson, next_axis)
    write_verifier_design(rows)
    write_results(results, best, rows)
    validate_files()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
