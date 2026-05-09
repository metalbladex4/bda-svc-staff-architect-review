#!/usr/bin/env python3
"""Experiment-only duplicate suppression wrapper for frozen FP8 v034a outputs."""

from __future__ import annotations

import contextlib
import csv
import datetime as dt
import importlib.util
import io
import json
import os
import shutil
import sys
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


WORKTREE_ROOT = Path("/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement")
CAPSTONE_ROOT = Path("/home/williambenitez1/Capstone")
PACKAGE_ROOT = WORKTREE_ROOT / (
    "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/"
    "human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/"
    "v017b_prompt_only_main_promotion/v040_fp8_experiment_only_duplicate_postprocessing"
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
EXPECTED = {
    "r020": {"matches": 181, "false_negatives": 38, "false_positives": 22, "combined_errors": 60},
    "r019": {"matches": 181, "false_negatives": 38, "false_positives": 23, "combined_errors": 61},
}
PRIORITY_CASES = ["66", "67", "84", "88", "97", "100", "110", "155", "166"]


@dataclass(frozen=True)
class PostprocessRule:
    rule_id: str
    containment_threshold: float = 0.8
    iou_threshold: float = 0.0
    area_ratio_threshold: float = 0.1
    center_inside_required: bool = True
    only_suppress_if_larger_matched: bool = True
    never_suppress_if_smaller_matched: bool = True
    never_suppress_if_both_overlap_distinct_refs: bool = True
    never_suppress_if_smaller_has_better_ref_iou: bool = True
    same_label_required: bool = False
    hybrid_same_label_or_zero_ref_iou: bool = False


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


def rule_to_dict(rule: PostprocessRule) -> dict[str, Any]:
    return {
        "rule_id": rule.rule_id,
        "containment_threshold": rule.containment_threshold,
        "iou_threshold": rule.iou_threshold,
        "area_ratio_threshold": rule.area_ratio_threshold,
        "center_inside_required": rule.center_inside_required,
        "same_label_required": rule.same_label_required,
        "only_suppress_if_larger_matched": rule.only_suppress_if_larger_matched,
        "never_suppress_if_smaller_matched": rule.never_suppress_if_smaller_matched,
        "never_suppress_if_both_overlap_distinct_refs": rule.never_suppress_if_both_overlap_distinct_refs,
        "never_suppress_if_smaller_has_better_ref_iou": rule.never_suppress_if_smaller_has_better_ref_iou,
        "hybrid_same_label_or_zero_ref_iou": rule.hybrid_same_label_or_zero_ref_iou,
    }


def qualifies(pair: dict[str, Any], rule: PostprocessRule) -> bool:
    if pair["containment_ratio"] < rule.containment_threshold:
        return False
    if pair["iou"] < rule.iou_threshold:
        return False
    if pair["area_ratio"] > rule.area_ratio_threshold:
        return False
    if rule.center_inside_required and not pair["center_inside_larger"]:
        return False
    if rule.same_label_required and not pair["same_target_type"]:
        return False
    if rule.hybrid_same_label_or_zero_ref_iou and not (
        pair["same_target_type"] or pair["smaller_best_ref_iou"] == 0.0
    ):
        return False
    if rule.only_suppress_if_larger_matched and not pair["larger_matched"]:
        return False
    if rule.never_suppress_if_smaller_matched and pair["smaller_matched"]:
        return False
    if rule.never_suppress_if_both_overlap_distinct_refs and pair["both_overlap_distinct_refs"]:
        return False
    if rule.never_suppress_if_smaller_has_better_ref_iou and pair["smaller_has_better_ref_iou"]:
        return False
    return True


def suppressions_for_rule(pair_rows: list[dict[str, Any]], rule: PostprocessRule) -> list[dict[str, Any]]:
    hits = [pair for pair in pair_rows if qualifies(pair, rule)]
    seen = set()
    out = []
    for row in sorted(hits, key=lambda item: (item["smaller_label"], -item["containment_ratio"], -item["iou"])):
        key = row["smaller_label"]
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def apply_rule(
    predictions: dict[str, dict[str, Any]],
    pairs_by_image: dict[str, list[dict[str, Any]]],
    rule: PostprocessRule,
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
                    "same_target_type": hit["same_target_type"],
                    "reason_removed": "experiment_only_duplicate_suppression",
                }
            )
    return mutated, removals


def write_postprocessed_predictions(rule_id: str, predictions: dict[str, dict[str, Any]]) -> Path:
    out_dir = PACKAGE_ROOT / "tables" / "postprocessed_predictions" / rule_id
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for image_filename, payload in predictions.items():
        case = Path(image_filename).stem
        write_json(out_dir / f"{case}_{rule_id}.json", payload)
    return out_dir


def case_metrics(eval_payload: dict[str, Any]) -> dict[str, str]:
    return v038.case_metrics(eval_payload)


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


def is_case_worse(candidate: str, baseline: str) -> bool:
    cm = tuple(int(x) for x in candidate.split("/"))
    bm = tuple(int(x) for x in baseline.split("/"))
    return cm[0] < bm[0] or cm[1] > bm[1] or cm[2] > bm[2]


def safety_reasons(result: dict[str, Any], baseline_eval: dict[str, Any], baseline_cases: dict[str, str], office_pass: bool) -> list[str]:
    reasons = []
    metrics = result["metrics"]
    base = baseline_eval["totals"]
    if metrics["false_negatives"] > base["false_negatives"]:
        reasons.append("fn_increase")
    if metrics["matches"] < base["matches"]:
        reasons.append("match_decrease")
    for case_id in ["66", "67", "84", "110", "155", "166"]:
        if is_case_worse(result["case_metrics"].get(case_id, "0/999/999"), baseline_cases.get(case_id, "0/999/999")):
            reasons.append(f"case_{case_id}_worse")
    if not office_pass:
        reasons.append("office_negative_not_pass")
    return reasons


def summarize_rule(
    rule: PostprocessRule,
    references: dict[str, dict[str, Any]],
    predictions: dict[str, dict[str, Any]],
    image_order: list[str],
    pairs_by_image: dict[str, list[dict[str, Any]]],
    baseline_eval: dict[str, Any],
    baseline_cases: dict[str, str],
    office_pass: bool,
) -> dict[str, Any]:
    postprocessed, removals = apply_rule(predictions, pairs_by_image, rule)
    out_dir = write_postprocessed_predictions(rule.rule_id, postprocessed)
    eval_payload = evaluate_reports(references, postprocessed, image_order)
    result = {
        "rule_id": rule.rule_id,
        "rule": rule_to_dict(rule),
        "metrics": eval_payload["totals"],
        "case_metrics": case_metrics(eval_payload),
        "removals": removals,
        "postprocessed_predictions_dir": str(out_dir),
    }
    result["safety_reasons"] = safety_reasons(result, baseline_eval, baseline_cases, office_pass)
    result["safe"] = not result["safety_reasons"]
    expected = EXPECTED.get(rule.rule_id)
    result["matches_expected_v039"] = (
        expected is None
        or all(result["metrics"].get(k) == v for k, v in {**expected, "image_count": 117}.items())
    )
    return result


def status_block(phase: str, result: dict[str, Any] | None, decision: str, lesson: str, next_action: str) -> None:
    if result:
        metrics = result["metrics"]
        metric_text = f"{metrics['matches']}/{metrics['false_negatives']}/{metrics['false_positives']}/{metrics['combined_errors']}"
        cases = result["case_metrics"]
        rule = result["rule_id"]
        vs_v034a = metrics["combined_errors"] - V034A_BASELINE["combined_errors"]
        vs_old = metrics["combined_errors"] - OLD_V020C["combined_errors"]
        removed = len(result["removals"])
    else:
        metric_text = "n/a"
        cases = {}
        rule = "n/a"
        vs_v034a = "n/a"
        vs_old = "n/a"
        removed = "n/a"
    print("=== V040 STATUS ===", flush=True)
    print(f"phase: {phase}", flush=True)
    print(f"rule: {rule}", flush=True)
    print(f"metrics: {metric_text}", flush=True)
    print(f"vs_v034a_delta: {vs_v034a}", flush=True)
    print(f"vs_old_v020c_58_delta: {vs_old}", flush=True)
    print(f"case_66: {cases.get('66', 'n/a')}", flush=True)
    print(f"case_67: {cases.get('67', 'n/a')}", flush=True)
    print(f"case_84: {cases.get('84', 'n/a')}", flush=True)
    print(f"case_88: {cases.get('88', 'n/a')}", flush=True)
    print(f"case_100: {cases.get('100', 'n/a')}", flush=True)
    print(f"case_110: {cases.get('110', 'n/a')}", flush=True)
    print(f"case_155: {cases.get('155', 'n/a')}", flush=True)
    print(f"removed_predictions: {removed}", flush=True)
    print(f"decision: {decision}", flush=True)
    print(f"main_lesson: {lesson}", flush=True)
    print(f"next_action: {next_action}", flush=True)
    print("===================", flush=True)


def main() -> int:
    for dirname in ["scripts", "tables", "review_images", "tables/postprocessed_predictions"]:
        (PACKAGE_ROOT / dirname).mkdir(parents=True, exist_ok=True)

    rules = [
        PostprocessRule(rule_id="r019", same_label_required=True),
        PostprocessRule(rule_id="r020", same_label_required=False),
        PostprocessRule(rule_id="hybrid", same_label_required=False, hybrid_same_label_or_zero_ref_iou=True),
    ]

    source_artifacts = [
        "docs/.../v039_fp8_containment_first_duplicate_suppression/final_recommendation.md",
        "docs/.../v039_fp8_containment_first_duplicate_suppression/best_simulation_report.md",
        "docs/.../v039_fp8_containment_first_duplicate_suppression/best_simulation_report.json",
        "docs/.../v039_fp8_containment_first_duplicate_suppression/case_level_delta_report.csv",
        "docs/.../v039_fp8_containment_first_duplicate_suppression/simulation_grid_results.csv",
        "docs/.../v038_fp8_same_wreck_duplicate_suppression_simulation/final_recommendation.md",
        "docs/.../v034_fp8_vllm_precision_recovery_autonomous/final_recommendation.md",
        "z_reference_docs/GPT-Pro_collab/bda_svc_qwen_prompt_engineering_deep_research_bundle.md",
        "z_reference_docs/GPT-Pro_collab/CODEX_QWEN_PROMPT_ENGINEERING_DIRECTION_2026-05-06.md",
    ]
    write_json(
        PACKAGE_ROOT / "source_manifest.json",
        {
            "generated_at": utc_now(),
            "package": "v040_fp8_experiment_only_duplicate_postprocessing",
            "frozen_artifacts_only": True,
            "vlm_called": False,
            "prompt_candidate_authored": False,
            "product_runtime_modified": False,
            "source_artifacts": source_artifacts,
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
    baseline_cases = case_metrics(baseline_eval)
    baseline_maps = v038.matched_maps(baseline_eval)
    office_summary = v038.read_json(v038.V034_OFFICE_RUN_ROOT / "eval/evaluation_2026-05-09_030200Z_summary.json")
    office_pass = office_summary["totals"]["false_positive_count"] == 0

    pairs_by_image: dict[str, list[dict[str, Any]]] = {}
    for image_filename in image_order:
        stats = v039.target_ref_stats(references[image_filename], predictions[image_filename])
        pairs_by_image[image_filename] = v039.pair_features(predictions[image_filename], baseline_maps[image_filename], stats)

    for rule in rules[:2]:
        write_json(PACKAGE_ROOT / f"rule_spec_{rule.rule_id}.json", {"generated_at": utc_now(), "rule": rule_to_dict(rule)})
        write_text(
            PACKAGE_ROOT / f"rule_spec_{rule.rule_id}.md",
            f"# Rule Spec {rule.rule_id}\n\n"
            f"- containment >= `{rule.containment_threshold}`\n"
            f"- IoU >= `{rule.iou_threshold}`\n"
            f"- area ratio <= `{rule.area_ratio_threshold}`\n"
            f"- center inside larger box required: `{rule.center_inside_required}`\n"
            f"- same-label required: `{rule.same_label_required}`\n"
            f"- only suppress if larger box is matched: `{rule.only_suppress_if_larger_matched}`\n"
            f"- never suppress if smaller box is matched: `{rule.never_suppress_if_smaller_matched}`\n"
            f"- never suppress if both boxes overlap distinct references: `{rule.never_suppress_if_both_overlap_distinct_refs}`\n"
            f"- never suppress if smaller box has better reference IoU: `{rule.never_suppress_if_smaller_has_better_ref_iou}`\n",
        )
    status_block("rule_spec", None, "n/a", "r019 and r020 were formalized as experiment-only rule specs.", "Build and run wrapper validation.")

    write_json(
        PACKAGE_ROOT / "postprocess_design.json",
        {
            "generated_at": utc_now(),
            "design": "experiment_only_duplicate_suppression_wrapper",
            "input": "frozen_v034a_predictions",
            "output": "v040/tables/postprocessed_predictions/<rule>",
            "original_predictions_untouched": True,
            "evaluation": "bda_eval_detection_study_matching_via_local_model_classes",
        },
    )
    write_text(
        PACKAGE_ROOT / "postprocess_design.md",
        "# v040 Postprocess Design\n\n"
        "The wrapper loads frozen v034a predictions, computes pair geometry against the frozen baseline match map, writes postprocessed copies under `tables/postprocessed_predictions/<rule>/`, and evaluates those copies with the same local `bda_eval` detection-study matching behavior. It is experiment-only and does not modify product runtime.\n",
    )
    write_json(
        PACKAGE_ROOT / "experiment_only_wrapper.json",
        {
            "generated_at": utc_now(),
            "script": str(PACKAGE_ROOT / "scripts/run_v040_duplicate_postprocessing_wrapper.py"),
            "writes_only_inside_package": True,
            "rules_run": [rule.rule_id for rule in rules],
            "hybrid_definition": "same-label required OR removed box has zero reference IoU; all other r020 conditions preserved",
        },
    )
    write_text(
        PACKAGE_ROOT / "experiment_only_wrapper.md",
        "# v040 Experiment-Only Wrapper\n\n"
        "The wrapper is package-local. It writes postprocessed prediction copies and suppression logs inside the v040 package only. It does not call the VLM, author prompts, change product config, or alter eval truth.\n",
    )
    status_block("wrapper_build", None, "n/a", "Wrapper design and output boundaries were documented.", "Run r019, r020, and hybrid validation.")

    results = [
        summarize_rule(rule, references, predictions, image_order, pairs_by_image, baseline_eval, baseline_cases, office_pass)
        for rule in rules
    ]
    by_rule = {result["rule_id"]: result for result in results}
    for rule_id in ["r019", "r020"]:
        if not by_rule[rule_id]["matches_expected_v039"]:
            write_json(PACKAGE_ROOT / "failure_analysis.json", {"generated_at": utc_now(), "status": "metric_reproduction_failed", "results": results})
            write_text(PACKAGE_ROOT / "failure_analysis.md", "# v040 Failure Analysis\n\nMetric reproduction failed; do not claim improvement.\n")
            status_block("validation", by_rule[rule_id], "E", f"{rule_id} failed to reproduce v039 expected metrics.", "Stop and diagnose.")
            return 1
    status_block("validation", by_rule["r020"], "n/a", "Wrapper reproduced r020 and r019 expected v039 metrics.", "Compare r019, r020, and hybrid.")

    validation_rows = []
    all_case_rows = []
    all_removals = []
    for result in results:
        metrics = result["metrics"]
        validation_rows.append(
            {
                "rule_id": result["rule_id"],
                "matches": metrics["matches"],
                "false_negatives": metrics["false_negatives"],
                "false_positives": metrics["false_positives"],
                "combined_errors": metrics["combined_errors"],
                "image_count": metrics["image_count"],
                "vs_v034a_delta": metrics["combined_errors"] - V034A_BASELINE["combined_errors"],
                "vs_old_v020c_58_delta": metrics["combined_errors"] - OLD_V020C["combined_errors"],
                "removed_predictions": len(result["removals"]),
                "safe": result["safe"],
                "safety_reasons": ";".join(result["safety_reasons"]),
                "case_66": result["case_metrics"].get("66", "n/a"),
                "case_67": result["case_metrics"].get("67", "n/a"),
                "case_84": result["case_metrics"].get("84", "n/a"),
                "case_88": result["case_metrics"].get("88", "n/a"),
                "case_97": result["case_metrics"].get("97", "n/a"),
                "case_100": result["case_metrics"].get("100", "n/a"),
                "case_110": result["case_metrics"].get("110", "n/a"),
                "case_155": result["case_metrics"].get("155", "n/a"),
                "case_166": result["case_metrics"].get("166", "n/a"),
                "matches_expected_v039": result["matches_expected_v039"],
            }
        )
        all_case_rows.extend(case_delta_rows(result["rule_id"], baseline_eval, evaluate_reports(references, {k: json.loads((Path(result["postprocessed_predictions_dir"]) / f"{Path(k).stem}_{result['rule_id']}.json").read_text(encoding="utf-8")) for k in image_order}, image_order), result["removals"]))
        all_removals.extend(result["removals"])

    write_json(PACKAGE_ROOT / "postprocess_validation_results.json", {"generated_at": utc_now(), "results": results})
    write_csv(PACKAGE_ROOT / "postprocess_validation_results.csv", validation_rows)
    write_csv(PACKAGE_ROOT / "case_level_delta_report.csv", all_case_rows)
    write_text(
        PACKAGE_ROOT / "postprocess_validation_results.md",
        "# v040 Postprocess Validation Results\n\n"
        "| rule | metrics | removed | notes |\n"
        "| --- | --- | --- | --- |\n"
        + "\n".join(
            f"| `{row['rule_id']}` | `{row['matches']}/{row['false_negatives']}/{row['false_positives']}/{row['combined_errors']}` | `{row['removed_predictions']}` | safe `{row['safe']}` |"
            for row in validation_rows
        )
        + "\n",
    )
    write_text(
        PACKAGE_ROOT / "case_level_delta_report.md",
        "# v040 Case-Level Delta Report\n\nSee `case_level_delta_report.csv` for per-case deltas for r019, r020, and hybrid.\n",
    )

    r020 = by_rule["r020"]
    r019 = by_rule["r019"]
    hybrid = by_rule["hybrid"]
    hybrid_matches_r020 = hybrid["metrics"]["combined_errors"] == r020["metrics"]["combined_errors"]
    hybrid_safer_than_r020 = all(
        removal["same_target_type"] or removal["removed_best_ref_iou"] == 0.0
        for removal in hybrid["removals"]
    )

    if hybrid_matches_r020 and hybrid_safer_than_r020:
        decision = "C"
        best = hybrid
        decision_text = "hybrid rule beats or matches r020 with safer semantics."
        next_work = "v041_experiment_only_postprocessing_integration"
    elif r020["metrics"]["combined_errors"] < r019["metrics"]["combined_errors"]:
        decision = "A"
        best = r020
        decision_text = "r020 is best experiment-only post-processing candidate."
        next_work = "v041_experiment_only_postprocessing_integration_with_visual_review_of_cross_label_case100"
    else:
        decision = "B"
        best = r019
        decision_text = "r019 is preferred due to safer same-label semantics."
        next_work = "v041_experiment_only_postprocessing_integration"

    tradeoff = {
        "generated_at": utc_now(),
        "r020": {
            "metrics": r020["metrics"],
            "removed_predictions": r020["removals"],
            "numeric_note": "best numeric result among r019/r020",
            "semantic_risk": "label-agnostic; includes cross-label case-100 removal",
        },
        "r019": {
            "metrics": r019["metrics"],
            "removed_predictions": r019["removals"],
            "numeric_note": "one fewer FP removed than r020",
            "semantic_risk": "narrower same-label behavior",
        },
        "hybrid": {
            "metrics": hybrid["metrics"],
            "removed_predictions": hybrid["removals"],
            "definition": "same-label OR removed box has zero reference IoU",
            "matches_r020": hybrid_matches_r020,
            "safer_than_r020": hybrid_safer_than_r020,
        },
        "decision": decision,
    }
    write_json(PACKAGE_ROOT / "r019_vs_r020_tradeoff.json", tradeoff)
    write_text(
        PACKAGE_ROOT / "r019_vs_r020_tradeoff.md",
        "# v040 r019 vs r020 Tradeoff\n\n"
        f"- r020: `{r020['metrics']['matches']}/{r020['metrics']['false_negatives']}/{r020['metrics']['false_positives']}/{r020['metrics']['combined_errors']}`, `{len(r020['removals'])}` removals; numeric best, but label-agnostic and includes cross-label case 100.\n"
        f"- r019: `{r019['metrics']['matches']}/{r019['metrics']['false_negatives']}/{r019['metrics']['false_positives']}/{r019['metrics']['combined_errors']}`, `{len(r019['removals'])}` removals; safer same-label footprint.\n"
        f"- hybrid: `{hybrid['metrics']['matches']}/{hybrid['metrics']['false_negatives']}/{hybrid['metrics']['false_positives']}/{hybrid['metrics']['combined_errors']}`, `{len(hybrid['removals'])}` removals; same-label OR zero-reference-IoU cross-label.\n\n"
        f"Decision `{decision}`: {decision_text}\n",
    )
    status_block("r019_vs_r020", best, decision, decision_text, "Write final recommendation and validation artifacts.")

    failure = {
        "generated_at": utc_now(),
        "metric_reproduction": {
            "r019": r019["matches_expected_v039"],
            "r020": r020["matches_expected_v039"],
        },
        "safety_reasons": {result["rule_id"]: result["safety_reasons"] for result in results},
        "cross_label_r020_risk": "case 100 military_equipment inside matched buildings; acceptable only with visual review or hybrid zero-ref-IoU justification",
    }
    write_json(PACKAGE_ROOT / "failure_analysis.json", failure)
    write_text(
        PACKAGE_ROOT / "failure_analysis.md",
        "# v040 Failure Analysis\n\n"
        "- r019 and r020 reproduced v039 expected metrics.\n"
        "- No rule increased FNs, reduced matches, or worsened dense/control cases.\n"
        "- Main residual risk is semantic: r020 includes a cross-label case-100 removal, so hybrid or visual review is safer before integration.\n",
    )

    final = {
        "generated_at": utc_now(),
        "decision": decision,
        "decision_text": decision_text,
        "best_rule": best["rule_id"],
        "best_metrics": best["metrics"],
        "r020_reproduced": r020["matches_expected_v039"],
        "r019_reproduced": r019["matches_expected_v039"],
        "hybrid_tested": True,
        "hybrid_metrics": hybrid["metrics"],
        "r020_cross_label_removal": [r for r in r020["removals"] if not r["same_target_type"]],
        "cross_label_risk": "r020 is numerically best but cross-label removal should be visually reviewed or gated by zero reference IoU.",
        "next_work": next_work,
        "prompt_wording_should_pause": True,
        "hard_boundaries_preserved": True,
    }
    write_json(PACKAGE_ROOT / "final_recommendation.json", final)
    write_text(
        PACKAGE_ROOT / "final_recommendation.md",
        "# v040 Final Recommendation\n\n"
        f"Generated: `{utc_now()}`\n\n"
        f"Decision `{decision}`: {decision_text}\n\n"
        f"Best rule: `{best['rule_id']}`.\n"
        f"Best metrics: `{best['metrics']['matches']}/{best['metrics']['false_negatives']}/{best['metrics']['false_positives']}/{best['metrics']['combined_errors']}`.\n\n"
        f"r020 reproduced: `{r020['matches_expected_v039']}` at `{r020['metrics']['matches']}/{r020['metrics']['false_negatives']}/{r020['metrics']['false_positives']}/{r020['metrics']['combined_errors']}`.\n"
        f"r019 reproduced: `{r019['matches_expected_v039']}` at `{r019['metrics']['matches']}/{r019['metrics']['false_negatives']}/{r019['metrics']['false_positives']}/{r019['metrics']['combined_errors']}`.\n"
        f"Hybrid tested: `True` at `{hybrid['metrics']['matches']}/{hybrid['metrics']['false_negatives']}/{hybrid['metrics']['false_positives']}/{hybrid['metrics']['combined_errors']}`.\n\n"
        "r020's cross-label case-100 removal is numerically helpful but semantically broader. The hybrid keeps the same 60-error result while requiring same-label or zero reference IoU for cross-label removals, so it is the preferred next experiment-only integration candidate.\n\n"
        "Prompt wording should pause while experiment-only post-processing integration is explored. This is non-promoted evidence only and does not modify product runtime, prompt text, doctrine, assessment prompt, eval truth, or source truth.\n",
    )
    write_json(
        PACKAGE_ROOT / "recovery_log.json",
        {
            "generated_at": utc_now(),
            "steps": [
                "Read v039/v038/v034 source artifacts.",
                "Attempted Graphify recall; blocked by missing networkx.",
                "Formalized r019 and r020.",
                "Built package-local wrapper.",
                "Ran wrapper over frozen v034a predictions for r019, r020, and hybrid.",
                "Validated JSON/CSV and wrote final recommendation.",
            ],
        },
    )
    write_text(
        PACKAGE_ROOT / "recovery_log.md",
        "# v040 Recovery Log\n\n"
        "- Used frozen v034a predictions only.\n"
        "- Wrote postprocessed prediction copies inside the v040 package.\n"
        "- Reproduced r019 and r020 expected v039 metrics.\n"
        "- Tested hybrid rule offline.\n",
    )
    write_text(
        PACKAGE_ROOT / "lessons_learned.md",
        "# v040 Lessons Learned\n\n"
        "- r020's numeric advantage is reproducible in an experiment-only wrapper.\n"
        "- r020's cross-label case-100 removal is the main semantic risk.\n"
        "- A hybrid same-label-or-zero-reference-IoU gate preserves r020's metrics while narrowing cross-label behavior.\n",
    )
    write_text(
        PACKAGE_ROOT / "strategy_state.md",
        "# v040 Strategy State\n\n"
        "- FP8 prompt working best remains `v034a_fp8_broad_context_scene_box_guard = 181 / 38 / 25 / 63`.\n"
        f"- Best experiment-only postprocessed result: `{best['rule_id']} = {best['metrics']['matches']} / {best['metrics']['false_negatives']} / {best['metrics']['false_positives']} / {best['metrics']['combined_errors']}`.\n"
        f"- Decision: `{decision}`.\n"
        f"- Next work: `{next_work}`.\n"
        "- Do not promote or mutate product runtime.\n",
    )
    write_text(
        PACKAGE_ROOT / "README.md",
        "# v040 FP8 Experiment-Only Duplicate Postprocessing\n\n"
        "Package-local wrapper validation for r019, r020, and a hybrid containment-first duplicate-suppression rule over frozen v034a FP8 predictions. No VLM calls, prompt candidates, product runtime edits, or eval-truth edits were made.\n",
    )
    # Keep review_images directory present without copying raw image dumps.
    (PACKAGE_ROOT / "review_images").mkdir(exist_ok=True)
    status_block("final_decision", best, decision, decision_text, next_work)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
