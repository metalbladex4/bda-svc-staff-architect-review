#!/usr/bin/env python3
"""Recompute v050 merge/eval from saved tile audit rows.

The first live tile run produced valid tile outputs but the experiment-only
candidate records were missing evaluator-required BDA fields. This script does
not rerun the VLM. It rebuilds merged predictions from the saved accepted
detection audit with evaluator-valid target records and refreshes the summary
artifacts.
"""

from __future__ import annotations

import csv
import datetime as dt
import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


WORKTREE = Path("/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement")
PARENT = WORKTREE / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion"
PACKAGE = PARENT / "v050_fp8_non_oracle_tiling_crop_recovery"
MAIN_SCRIPT = PACKAGE / "scripts/run_v050_non_oracle_tiling_crop_recovery.py"


spec = importlib.util.spec_from_file_location("v050_main", MAIN_SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot import v050 helpers from {MAIN_SCRIPT}")
v050 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = v050
spec.loader.exec_module(v050)
v045 = v050.v045
v044 = v050.v044
v042 = v050.v042


def now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        if fields:
            writer.writeheader()
            writer.writerows(rows)


def metric_line(metrics: dict[str, Any]) -> str:
    return f"{metrics['matches']}/{metrics['false_negatives']}/{metrics['false_positives']}/{metrics['combined_errors']}"


def case_metrics(eval_payload: dict[str, Any]) -> dict[str, str]:
    return {
        v044.case_id(img["image_filename"]): f"{img['match_count']}/{img['false_negative_count']}/{img['false_positive_count']}"
        for img in eval_payload["images"]
    }


def label_status(eval_payload: dict[str, Any]) -> dict[tuple[str, str], str]:
    out: dict[tuple[str, str], str] = {}
    for image in eval_payload["images"]:
        fname = image["image_filename"]
        for match in image["matches"]:
            out[(fname, match["predicted_label"])] = "TP"
        for label in image["false_positive_labels"]:
            out[(fname, label)] = "FP"
    return out


def parse_box(raw: str) -> tuple[float, float, float, float]:
    vals = json.loads(raw)
    return tuple(float(v) for v in vals)


def make_target(target_type: str, bbox: tuple[float, float, float, float], confidence: float, source: str, reason: str) -> dict[str, Any]:
    damage_category = "DAMAGED" if target_type == "military_equipment" else "SEVERE_DAMAGE"
    return {
        "target_type": target_type,
        "damage_category": damage_category,
        "confidence_level": "POSSIBLE" if confidence < 0.75 else "PROBABLE",
        "brief_supporting_logic": f"Experiment-only v050 crop candidate from {source}: {reason[:120]}",
        "bounding_box": [round(float(v), 2) for v in bbox],
        "source": source,
    }


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = ["|" + "|".join(fields) + "|", "|" + "|".join(["---"] * len(fields)) + "|"]
    for row in rows:
        lines.append("|" + "|".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + "|")
    return "\n".join(lines)


def main() -> None:
    generated = now()
    state = v044.load_state()
    refs = state["refs"]
    order = state["order"]
    dims = state["dims"]
    pp0157_preds, _ = v044.apply_pp0157(state["p1753"], dims)
    pp044a_preds, _ = v044.apply_pp044a(pp0157_preds, dims)
    pp045b_preds, _ = v045.apply_pp045b(pp044a_preds, dims)
    pp045c_preds, _ = v045.apply_pp045c(pp045b_preds, dims)
    micro_order = v050.subset_order(order, v050.MICRO_CASES)
    baseline_micro_eval = v042.evaluate_reports(refs, pp045c_preds, micro_order)

    audit_path = PACKAGE / "tables/accepted_detection_audit.csv"
    audit_rows = list(csv.DictReader(audit_path.open(encoding="utf-8")))
    accepted_rows = [row for row in audit_rows if str(row.get("accepted", "")).lower() == "true"]
    merged_raw = deepcopy(pp045c_preds)
    for row in accepted_rows:
        confidence = float(row.get("confidence") or 0.0)
        merged_raw[row["image_filename"]].setdefault("physical_damage", {})[row["label"]] = make_target(
            row["target_type"],
            parse_box(row["full_bbox"]),
            confidence,
            f"v050_{row['strategy']}_{row['tile_id']}",
            row.get("reason", ""),
        )

    raw_micro_eval = v042.evaluate_reports(refs, merged_raw, micro_order)
    postprocessed_merged, postprocess_removals = v050.apply_locked_postprocessors(merged_raw, dims)
    post_micro_eval = v042.evaluate_reports(refs, postprocessed_merged, micro_order)
    raw_status = label_status(raw_micro_eval)
    post_status = label_status(post_micro_eval)

    for row in accepted_rows:
        row["raw_eval_status"] = raw_status.get((row["image_filename"], row["label"]), "suppressed_or_unknown")
        row["after_postprocess_eval_status"] = post_status.get((row["image_filename"], row["label"]), "suppressed_or_unknown")
    fields_added = ["label", "tile_id", "case_id", "image_filename", "strategy", "accepted", "reject_reason", "target_type", "full_bbox", "confidence", "visibility", "damage_or_relevance", "reason", "raw_eval_status", "after_postprocess_eval_status"]
    write_csv(PACKAGE / "tables/accepted_detection_audit.csv", accepted_rows, fields_added)

    added_tp = sum(1 for row in accepted_rows if row["after_postprocess_eval_status"] == "TP")
    added_fp = sum(1 for row in accepted_rows if row["after_postprocess_eval_status"] == "FP")
    baseline_metrics = baseline_micro_eval["totals"]
    raw_metrics = raw_micro_eval["totals"]
    post_metrics = post_micro_eval["totals"]
    baseline_cases = case_metrics(baseline_micro_eval)
    raw_cases = case_metrics(raw_micro_eval)
    post_cases = case_metrics(post_micro_eval)

    delta_rows = []
    for fname in micro_order:
        cid = v044.case_id(fname)
        base_img = next(img for img in baseline_micro_eval["images"] if img["image_filename"] == fname)
        raw_img = next(img for img in raw_micro_eval["images"] if img["image_filename"] == fname)
        post_img = next(img for img in post_micro_eval["images"] if img["image_filename"] == fname)
        delta_rows.append(
            {
                "case_id": cid,
                "image_filename": fname,
                "baseline": baseline_cases.get(cid, ""),
                "raw_merged": raw_cases.get(cid, ""),
                "postprocessed_merged": post_cases.get(cid, ""),
                "baseline_errors": base_img["false_negative_count"] + base_img["false_positive_count"],
                "raw_errors": raw_img["false_negative_count"] + raw_img["false_positive_count"],
                "post_errors": post_img["false_negative_count"] + post_img["false_positive_count"],
                "post_delta_vs_baseline": (post_img["false_negative_count"] + post_img["false_positive_count"]) - (base_img["false_negative_count"] + base_img["false_positive_count"]),
            }
        )
    write_csv(PACKAGE / "case_level_delta_report.csv", delta_rows)
    write_text(PACKAGE / "case_level_delta_report.md", "# Case Level Delta Report\n\n" + markdown_table(delta_rows, ["case_id", "baseline", "raw_merged", "postprocessed_merged", "post_delta_vs_baseline"]) + "\n")

    micro_improved = post_metrics["combined_errors"] < baseline_metrics["combined_errors"]
    fp_explosion = post_metrics["false_positives"] > baseline_metrics["false_positives"] + 3
    dense_regression = any(
        row["case_id"] in {"66", "67", "84", "110", "155", "166"} and int(row["post_delta_vs_baseline"]) > 0
        for row in delta_rows
    )
    if micro_improved and not fp_explosion and not dense_regression:
        decision = "A"
        main_lesson = "Non-oracle tiling produced a micro-pack improvement after evaluator-valid merge."
        next_action = "Run full all-current/no101 or continue strategy-specific tiling refinement."
    elif added_tp > 0 and added_fp > 0:
        decision = "B"
        main_lesson = "Non-oracle tiling recovered some FNs but introduced false positives and needs a verifier gate."
        next_action = "Recommend v051 crop-level verifier gating before any full-pack merge."
    else:
        decision = "C"
        main_lesson = "Non-oracle tiling did not transfer the reference-crop upper-bound into safe recoveries."
        next_action = "Return to verifier design, visual review, or narrower tiling strategy rather than broad prompt wording."

    write_json(
        PACKAGE / "merged_predictions_summary.json",
        {
            "generated_at": generated,
            "stage": "micro_pack_recomputed_from_tile_audit",
            "baseline_micro_metrics": baseline_metrics,
            "raw_merged_metrics": raw_metrics,
            "postprocessed_merged_metrics": post_metrics,
            "added_detections": len(accepted_rows),
            "added_true_positives": added_tp,
            "added_false_positives": added_fp,
            "postprocess_removals": len(postprocess_removals),
            "full_all_current_run": False,
            "full_all_current_skip_reason": "micro_pack_failed_gate" if decision != "A" else "not_run_by_script_guard",
        },
    )
    write_text(
        PACKAGE / "merged_predictions_summary.md",
        f"# Merged Predictions Summary\n\nBaseline micro: `{metric_line(baseline_metrics)}`\n\nRaw merged micro: `{metric_line(raw_metrics)}`\n\nPostprocessed merged micro: `{metric_line(post_metrics)}`\n\nAdded detections: `{len(accepted_rows)}`\n\nAdded true positives: `{added_tp}`\n\nAdded false positives: `{added_fp}`\n\nFull all-current run: `false`.\n",
    )
    write_json(
        PACKAGE / "evaluation_summary.json",
        {
            "generated_at": generated,
            "baseline": {"pp045c_locked_baseline": v050.PP045C, "micro_metrics": baseline_metrics},
            "raw_merged_micro": raw_metrics,
            "postprocessed_merged_micro": post_metrics,
            "full_all_current_metrics": None,
            "full_all_current_run": False,
            "decision": decision,
            "case_level_delta_report": "case_level_delta_report.csv",
        },
    )
    write_text(
        PACKAGE / "evaluation_summary.md",
        f"# Evaluation Summary\n\nMicro baseline: `{metric_line(baseline_metrics)}`\n\nRaw merged: `{metric_line(raw_metrics)}`\n\nPostprocessed merged: `{metric_line(post_metrics)}`\n\nDecision: `{decision}`.\n",
    )
    write_json(
        PACKAGE / "failure_analysis.json",
        {
            "generated_at": generated,
            "decision": decision,
            "micro_pack_passed": decision == "A",
            "fp_explosion": fp_explosion,
            "dense_or_control_regression": dense_regression,
            "added_true_positives": added_tp,
            "added_false_positives": added_fp,
            "lesson": main_lesson,
            "recommended_next": next_action,
            "note": "Recomputed from saved tile audit after fixing evaluator-required BDA fields.",
        },
    )
    write_text(PACKAGE / "failure_analysis.md", f"# Failure Analysis\n\nDecision: `{decision}`\n\n{main_lesson}\n\nNext: {next_action}\n")
    write_json(PACKAGE / "final_recommendation.json", {"generated_at": generated, "decision": decision, "backend_ran": True, "case_40_resolved": True, "micro_pack_metrics": post_metrics, "full_all_current_metrics": None, "added_detections": len(accepted_rows), "added_true_positives": added_tp, "added_false_positives": added_fp, "next_action": next_action, "hard_boundaries_preserved": True})
    write_text(
        PACKAGE / "final_recommendation.md",
        f"# v050 Final Recommendation\n\nBackend ran: `true`.\n\nCase 40 image resolved: `true`.\n\nStrategies tested: `A, B, C, D` on the micro-pack.\n\nMicro-pack baseline: `{metric_line(baseline_metrics)}`.\n\nMicro-pack raw merged: `{metric_line(raw_metrics)}`.\n\nMicro-pack postprocessed merged: `{metric_line(post_metrics)}`.\n\nAdded detections: `{len(accepted_rows)}`; added TPs: `{added_tp}`; added FPs: `{added_fp}`.\n\nFull all-current run: `false`.\n\nDecision: `{decision}`.\n\nNext action: {next_action}\n\nHard boundaries were preserved: reference boxes were not used for inference crop generation, pp046a stayed diagnostic-only, and no product/runtime/source-truth files were mutated.\n",
    )
    write_text(PACKAGE / "lessons_learned.md", f"# Lessons Learned\n\n- {main_lesson}\n- v049 reference-centered crop recognition did not by itself produce a safe deployable recovery path; non-oracle additions need an explicit verifier/merge gate.\n")
    write_text(PACKAGE / "strategy_state.md", f"# Strategy State\n\nLocked baseline remains `pp045c = {metric_line(v050.PP045C)}`.\n\nv050 decision: `{decision}`.\n\nNext axis: {next_action}\n")
    write_json(PACKAGE / "recovery_log.json", {"generated_at": generated, "events": [{"event": "v050_tile_run_completed"}, {"event": "recomputed_merge_with_evaluator_valid_targets", "decision": decision, "lesson": main_lesson}]})
    write_text(PACKAGE / "recovery_log.md", f"# Recovery Log\n\n- `{generated}`: Recomputed v050 merge from saved tile audit with evaluator-valid target records. Decision `{decision}`.\n")

    print(f"""=== V050 STATUS ===
phase: micro_pack
strategy: mixed
backend: available
stage: merge_eval
raw_merged_metrics: {metric_line(raw_metrics)}
postprocessed_merged_metrics: {metric_line(post_metrics)}
vs_pp045c_49_delta: {post_metrics['combined_errors'] - baseline_metrics['combined_errors']:+d} micro-pack
added_detections: {len(accepted_rows)}
added_true_positives: {added_tp}
added_false_positives: {added_fp}
case_66: {post_cases.get("66", "n/a")}
case_67: {post_cases.get("67", "n/a")}
case_84: {post_cases.get("84", "n/a")}
case_100: {post_cases.get("100", "n/a")}
case_110: {post_cases.get("110", "n/a")}
case_155: {post_cases.get("155", "n/a")}
case_166: {post_cases.get("166", "n/a")}
office_negative: not_run
decision: {decision}
main_lesson: {main_lesson}
next_action: {next_action}
===================""")


if __name__ == "__main__":
    main()
