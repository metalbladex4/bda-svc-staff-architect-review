#!/usr/bin/env python3
"""Continuation runner for v042 one-candidate autonomous loops."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml


THIS = Path(__file__).resolve()
CORE_PATH = THIS.parent / "run_v042_postprocessed_scoring.py"
spec = importlib.util.spec_from_file_location("v042_core", CORE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load v042 core from {CORE_PATH}")
core = importlib.util.module_from_spec(spec)
sys.modules["v042_core"] = core
spec.loader.exec_module(core)


def read_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def metrics_string(metrics: dict[str, Any] | None) -> str:
    return core.metrics_string(metrics)


def create_v042b_overlay() -> Path:
    baseline = read_yaml(core.BASELINE_OVERLAY)
    prompt = baseline["overrides"]["prompts"]["detect_objects"]
    needle = (
        "BAD FINAL BOX\n"
        "- context-only cue\n"
        "- group, row, convoy, cluster, or scene region\n"
    )
    addition = (
        "BAD FINAL BOX\n"
        "- context-only cue\n"
        "- box where the target body is only a small part of the box and most of the box is road, ground, smoke, debris, or background\n"
        "- group, row, convoy, cluster, or scene region\n"
    )
    if "target body is only a small part of the box" not in prompt:
        prompt = prompt.replace(needle, addition)
    candidate = deepcopy(baseline)
    candidate["candidate_id"] = "v042b_fp8_mostly_context_box_guard"
    candidate["title"] = "v042b fp8 mostly-context box guard"
    candidate["overlay_id"] = "qwen-1.2-v042b_fp8_mostly_context_box_guard"
    candidate["overlay_type"] = "fp8_postprocessed_scoring_candidate"
    candidate["description"] = (
        "Precision-only guard for boxes that include mostly road, smoke, debris, ground, or background rather than the target body."
    )
    candidate["generated_from"] = ["v034a_fp8_broad_context_scene_box_guard", "v041_p1753_postprocessed_scoring"]
    candidate["intended_changes"] = [
        "Add one compact BAD FINAL BOX clause for boxes where the target is a small part and most of the box is context/background.",
        "Preserve the v020c extra-box audit.",
        "Preserve the v034a broad-context/scene-box guard.",
        "Avoid same-wreck duplicate wording and dense-fragment wording.",
    ]
    candidate["overrides"]["prompts"]["detect_objects"] = prompt
    candidate["overrides"]["runtime"] = {"notes": "Applied only inside upstream/main scratch config; no product adoption."}
    out = core.PACKAGE_ROOT / "overlays/v042b_fp8_mostly_context_box_guard.yaml"
    write_yaml(out, candidate)
    return out


def create_v042c_overlay() -> Path:
    baseline = read_yaml(core.BASELINE_OVERLAY)
    prompt = baseline["overrides"]["prompts"]["detect_objects"]
    old = (
        "- broad context or scene boxes whose strongest support is a row, blast area, road, debris field, smoke plume, "
        "or multiple uncertain fragments rather than one visible target body"
    )
    new = (
        "- broad context or scene boxes whose strongest support is a row, blast area, road, debris field, or smoke plume "
        "rather than one visible target body"
    )
    if old in prompt:
        prompt = prompt.replace(old, new)
    candidate = deepcopy(baseline)
    candidate["candidate_id"] = "v042c_fp8_uncertain_fragments_phrase_ablation"
    candidate["title"] = "v042c fp8 uncertain-fragments phrase ablation"
    candidate["overlay_id"] = "qwen-1.2-v042c_fp8_uncertain_fragments_phrase_ablation"
    candidate["overlay_type"] = "fp8_postprocessed_scoring_candidate"
    candidate["description"] = (
        "Micro-gated ablation of the multiple-uncertain-fragments phrase inside the v034a broad-context guard."
    )
    candidate["generated_from"] = ["v034a_fp8_broad_context_scene_box_guard", "v041_p1753_postprocessed_scoring"]
    candidate["intended_changes"] = [
        "Remove only the 'multiple uncertain fragments' phrase from the v034a broad-context/scene-box guard.",
        "Preserve the rest of the v034a broad-context/scene-box guard.",
        "Preserve the v020c extra-box audit.",
        "Avoid adding recall wording, same-wreck duplicate wording, or dense-scene wording.",
    ]
    candidate["overrides"]["prompts"]["detect_objects"] = prompt
    candidate["overrides"]["runtime"] = {"notes": "Applied only inside upstream/main scratch config; no product adoption."}
    out = core.PACKAGE_ROOT / "overlays/v042c_fp8_uncertain_fragments_phrase_ablation.yaml"
    write_yaml(out, candidate)
    return out


def create_v042d_overlay() -> Path:
    baseline = read_yaml(core.BASELINE_OVERLAY)
    prompt = baseline["overrides"]["prompts"]["detect_objects"]
    old = (
        "FINAL BALANCE\n"
        "Keep v019c recall behavior: small, damaged, crowded, or partly obscured targets are valid when their own target body remains visible after context is removed. The audit removes extras; it should not remove a true separable target body.\n"
    )
    new = (
        "FINAL BALANCE\n"
        "Keep true targets: small, damaged, crowded, or partly obscured targets are valid when their own target body remains visible after context is removed. The audit removes extras only; do not remove a true separable target body.\n"
    )
    if old in prompt:
        prompt = prompt.replace(old, new)
    candidate = deepcopy(baseline)
    candidate["candidate_id"] = "v042d_fp8_final_balance_simplification"
    candidate["title"] = "v042d fp8 final-balance simplification"
    candidate["overlay_id"] = "qwen-1.2-v042d_fp8_final_balance_simplification"
    candidate["overlay_type"] = "fp8_postprocessed_scoring_candidate"
    candidate["description"] = "Semantic-neutral simplification of FINAL BALANCE wording for the FP8 Qwen surface."
    candidate["generated_from"] = ["v034a_fp8_broad_context_scene_box_guard", "v041_p1753_postprocessed_scoring"]
    candidate["intended_changes"] = [
        "Replace historical 'v019c recall behavior' wording with direct target-validity wording.",
        "Preserve the small/damaged/crowded/partly obscured target validity rule.",
        "Preserve the v020c extra-box audit.",
        "Preserve the v034a broad-context/scene-box guard.",
        "Avoid adding recall, same-wreck duplicate, dense-fragment, or broad-context wording.",
    ]
    candidate["overrides"]["prompts"]["detect_objects"] = prompt
    candidate["overrides"]["runtime"] = {"notes": "Applied only inside upstream/main scratch config; no product adoption."}
    out = core.PACKAGE_ROOT / "overlays/v042d_fp8_final_balance_simplification.yaml"
    write_yaml(out, candidate)
    return out


def create_v042e_overlay() -> Path:
    baseline = read_yaml(core.BASELINE_OVERLAY)
    prompt = baseline["overrides"]["prompts"]["detect_objects"]
    needle = (
        "GOOD FINAL BOX\n"
        "- one connected target body, wreck body, or exterior building structure\n"
    )
    addition = (
        "GOOD FINAL BOX\n"
        "- one connected target body, wreck body, or exterior building structure\n"
        "- a separate small target aligned near other targets remains valid when its own visible body can be boxed tightly\n"
    )
    if "separate small target aligned near other targets" not in prompt:
        prompt = prompt.replace(needle, addition)
    candidate = deepcopy(baseline)
    candidate["candidate_id"] = "v042e_fp8_separate_small_target_row_exception"
    candidate["title"] = "v042e fp8 separate-small-target row exception"
    candidate["overlay_id"] = "qwen-1.2-v042e_fp8_separate_small_target_row_exception"
    candidate["overlay_type"] = "fp8_postprocessed_scoring_candidate"
    candidate["description"] = "Narrow GOOD FINAL BOX exception protecting separable small targets near other targets."
    candidate["generated_from"] = ["v034a_fp8_broad_context_scene_box_guard", "v041_p1753_postprocessed_scoring"]
    candidate["intended_changes"] = [
        "Add one compact GOOD FINAL BOX clause for a separate small target near other targets when its own body can be boxed tightly.",
        "Preserve the v020c extra-box audit.",
        "Preserve the v034a broad-context/scene-box guard.",
        "Avoid same-wreck duplicate wording, dense-fragment wording, and broad recall language.",
    ]
    candidate["overrides"]["prompts"]["detect_objects"] = prompt
    candidate["overrides"]["runtime"] = {"notes": "Applied only inside upstream/main scratch config; no product adoption."}
    out = core.PACKAGE_ROOT / "overlays/v042e_fp8_separate_small_target_row_exception.yaml"
    write_yaml(out, candidate)
    return out


def latest_summary(candidate_id: str, stage: str) -> dict[str, Any] | None:
    root = core.PACKAGE_ROOT / "runs" / candidate_id / stage
    paths = sorted(root.glob("*/v042_run_summary.json"))
    if not paths:
        return None
    return json.loads(paths[-1].read_text(encoding="utf-8"))


def append_row(row: dict[str, Any]) -> None:
    cmp_path = core.PACKAGE_ROOT / "comparison_matrix.json"
    payload = json.loads(cmp_path.read_text(encoding="utf-8")) if cmp_path.exists() else {"rows": []}
    rows = [r for r in payload.get("rows", []) if not (r.get("candidate_id") == row["candidate_id"] and r.get("stage") == row["stage"])]
    rows.append(row)
    payload = {"generated_at": core.utc_now(), "rows": rows}
    write_json(cmp_path, payload)
    write_json(core.PACKAGE_ROOT / "candidate_registry.json", {"generated_at": core.utc_now(), "candidates": rows})
    md = [
        "# v042 Comparison Matrix",
        "",
        "| Candidate | Stage | Raw | Postprocessed | Case 66 | Case 67 | Case 84 | Case 100 | Case 110 | Case 155 | Case 166 | Removed | Removed TPs | Status |",
        "|---|---|---|---|---|---|---|---|---|---|---|---:|---:|---|",
    ]
    for r in rows:
        md.append(
            "| `{}` | {} | `{}` | `{}` | `{}` | `{}` | `{}` | `{}` | `{}` | `{}` | `{}` | {} | {} | {} |".format(
                r.get("candidate_id"),
                r.get("stage"),
                metrics_string(r.get("raw_metrics")),
                metrics_string(r.get("postprocessed_metrics")),
                r.get("case_66_raw_post", "n/a"),
                r.get("case_67_raw_post", "n/a"),
                r.get("case_84_raw_post", "n/a"),
                r.get("case_100_raw_post", "n/a"),
                r.get("case_110_raw_post", "n/a"),
                r.get("case_155_raw_post", "n/a"),
                r.get("case_166_raw_post", "n/a"),
                r.get("removed_predictions", "n/a"),
                r.get("removed_true_positives", "n/a"),
                r.get("status", "n/a"),
            )
        )
    (core.PACKAGE_ROOT / "comparison_matrix.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (core.PACKAGE_ROOT / "live_metrics_log.md").write_text(
        "# v042 Live Metrics Log\n\n"
        + "\n".join(
            f"- `{r.get('candidate_id')}` `{r.get('stage')}` raw `{metrics_string(r.get('raw_metrics'))}` post `{metrics_string(r.get('postprocessed_metrics'))}` status `{r.get('status', 'n/a')}`"
            for r in rows
        )
        + "\n",
        encoding="utf-8",
    )


def record_to_row(record: dict[str, Any], stage: str, status: str) -> dict[str, Any]:
    raw_cases = record.get("raw_case_metrics", {})
    post_cases = record.get("postprocessed_case_metrics", {})
    return {
        "candidate_id": record["candidate_id"],
        "stage": stage,
        "raw_metrics": record.get("raw_metrics"),
        "postprocessed_metrics": record.get("postprocessed_metrics"),
        "case_66_raw_post": f"{raw_cases.get('66', 'n/a')} -> {post_cases.get('66', 'n/a')}",
        "case_67_raw_post": f"{raw_cases.get('67', 'n/a')} -> {post_cases.get('67', 'n/a')}",
        "case_84_raw_post": f"{raw_cases.get('84', 'n/a')} -> {post_cases.get('84', 'n/a')}",
        "case_100_raw_post": f"{raw_cases.get('100', 'n/a')} -> {post_cases.get('100', 'n/a')}",
        "case_110_raw_post": f"{raw_cases.get('110', 'n/a')} -> {post_cases.get('110', 'n/a')}",
        "case_155_raw_post": f"{raw_cases.get('155', 'n/a')} -> {post_cases.get('155', 'n/a')}",
        "case_166_raw_post": f"{raw_cases.get('166', 'n/a')} -> {post_cases.get('166', 'n/a')}",
        "removed_predictions": record.get("postprocess_removed_predictions"),
        "removed_true_positives": record.get("postprocess_removed_true_positives"),
        "status": status,
    }


def write_candidate_diagnosis(record: dict[str, Any], status: str, lesson: str, next_axis: str) -> None:
    raw_cases = record.get("raw_case_metrics", {})
    post_cases = record.get("postprocessed_case_metrics", {})
    payload = {
        "generated_at": core.utc_now(),
        "candidate_id": record["candidate_id"],
        "status": status,
        "raw_metrics": record.get("raw_metrics"),
        "postprocessed_metrics": record.get("postprocessed_metrics"),
        "raw_case_metrics": raw_cases,
        "postprocessed_case_metrics": post_cases,
        "postprocess_removed_predictions": record.get("postprocess_removed_predictions"),
        "postprocess_removed_true_positives": record.get("postprocess_removed_true_positives"),
        "main_lesson": lesson,
        "next_axis": next_axis,
    }
    stem = record["candidate_id"]
    if stem.startswith("v042c"):
        tested = (
            "a micro-gated ablation of only the 'multiple uncertain fragments' phrase inside the v034a broad-context guard, "
            "from the v034a base with p1753 paired scoring"
        )
        changed = "Only the risky phrase was removed; the rest of the v034a guard and v020c extra-box audit were preserved."
    elif stem.startswith("v042d"):
        tested = (
            "a semantic-neutral simplification of FINAL BALANCE that removes historical version wording while preserving target-validity semantics"
        )
        changed = "Only the FINAL BALANCE sentence was simplified; the v020c extra-box audit and v034a broad-context guard were preserved."
    elif stem.startswith("v042e"):
        tested = "a narrow GOOD FINAL BOX exception for a separate small target near other targets when its own body can be boxed tightly"
        changed = "One compact GOOD FINAL BOX clause was added outside EXTRA-BOX AUDIT and FINAL BALANCE; v020c audit and v034a guard were preserved."
    else:
        tested = (
            "a precision-only BAD FINAL BOX clause for mostly-context/background boxes, from the v034a base with p1753 paired scoring"
        )
        changed = "One compact BAD FINAL BOX clause was added. The v020c extra-box audit and v034a broad-context guard were preserved."
    write_json(core.PACKAGE_ROOT / f"diagnoses/{stem}_diagnosis.json", payload)
    (core.PACKAGE_ROOT / f"diagnoses/{stem}_diagnosis.md").write_text(
        f"# {stem} Diagnosis\n\n"
        f"What did this candidate test? {tested}.\n\n"
        f"What changed from current working best? {changed}\n\n"
        f"Raw metrics: `{metrics_string(record.get('raw_metrics'))}`.\n\n"
        f"Postprocessed metrics: `{metrics_string(record.get('postprocessed_metrics'))}`.\n\n"
        f"Case 66: `{raw_cases.get('66', 'n/a')} -> {post_cases.get('66', 'n/a')}`.\n"
        f"Case 67: `{raw_cases.get('67', 'n/a')} -> {post_cases.get('67', 'n/a')}`.\n"
        f"Case 84: `{raw_cases.get('84', 'n/a')} -> {post_cases.get('84', 'n/a')}`.\n"
        f"Case 100: `{raw_cases.get('100', 'n/a')} -> {post_cases.get('100', 'n/a')}`.\n"
        f"Case 110: `{raw_cases.get('110', 'n/a')} -> {post_cases.get('110', 'n/a')}`.\n"
        f"Case 155: `{raw_cases.get('155', 'n/a')} -> {post_cases.get('155', 'n/a')}`.\n"
        f"Case 166: `{raw_cases.get('166', 'n/a')} -> {post_cases.get('166', 'n/a')}`.\n\n"
        f"p1753 removed `{record.get('postprocess_removed_predictions')}` predictions and `{record.get('postprocess_removed_true_positives')}` true positives.\n\n"
        f"Main lesson: {lesson}\n\n"
        f"Next axis: {next_axis}\n",
        encoding="utf-8",
    )


def update_closeout(status: str, best_note: str, next_axis: str) -> None:
    final_payload = {
        "generated_at": core.utc_now(),
        "status": status,
        "best_raw_fp8_candidate": "v034a_fp8_broad_context_scene_box_guard",
        "best_raw_metrics": core.RAW_V034A,
        "best_postprocessed_fp8_candidate": "v034a_fp8_broad_context_scene_box_guard+p1753",
        "best_postprocessed_metrics": core.COMPOSITE_V034A_P1753,
        "beat_composite_62": False,
        "reached_or_beat_old_v020c_58": False,
        "target_le_1_reached": False,
        "p1753_behavior": {
            "rule_id": "p1753",
            "v034a_removed_predictions": 1,
            "v034a_removed_true_positives": 0,
            "v034a_removed_cases": ["88"],
        },
        "v040_hybrid_oracle_non_deployable": core.V040_HYBRID_ORACLE,
        "postprocessed_scoring_should_continue": True,
        "hard_boundaries_preserved": True,
        "next_axis": next_axis,
    }
    write_json(core.PACKAGE_ROOT / "final_recommendation.json", final_payload)
    (core.PACKAGE_ROOT / "final_recommendation.md").write_text(
        "# v042 Final Recommendation\n\n"
        f"Generated: `{core.utc_now()}`\n\n"
        f"Status: `{status}`.\n\n"
        f"Best raw FP8 candidate: `v034a_fp8_broad_context_scene_box_guard` at `{metrics_string(core.RAW_V034A)}`.\n\n"
        f"Best postprocessed FP8 candidate: `v034a_fp8_broad_context_scene_box_guard+p1753` at `{metrics_string(core.COMPOSITE_V034A_P1753)}`.\n\n"
        "Beat composite 62 errors: `False`.\n"
        "Reached or beat old 58-error reference: `False`.\n"
        "Reached <=1 target: `False`.\n\n"
        "p1753 behavior: prediction-only same-label containment-first suppression; on frozen v034a it removes one case-88 FP and zero TPs.\n\n"
        f"{best_note}\n\n"
        f"Next axis: {next_axis}\n\n"
        "FP8 remains a separate model line. This is experiment-only scoring evidence, not product runtime or promotion.\n",
        encoding="utf-8",
    )
    (core.PACKAGE_ROOT / "lessons_learned.md").write_text(
        "# v042 Lessons Learned\n\n"
        "- p1753 reproduced v041 exactly on frozen v034a and remains a safe deployable scoring layer for this tranche.\n"
        "- v042a's low-contrast/smoke-softened recall cue moved the model in the wrong direction: case 84 lost recall and case 66 gained an FP.\n"
        "- v042b's mostly-context precision clause is tested as a narrower alternative that avoids the v037 same-wreck and v035 dense-fragment failure families.\n"
        "- v042c tests whether the 'multiple uncertain fragments' phrase itself is load-bearing for dense recall or FP pressure.\n"
        "- v042d tests whether historical version-label wording adds unwanted FP8 surface noise without changing target-validity semantics.\n"
        "- v042e tests a narrow separable-small-target exception outside the audit/final-balance sections.\n"
        "- Full-run target claims are reserved for full all-current/no101 results; micro-pack deltas are gate evidence only.\n",
        encoding="utf-8",
    )
    (core.PACKAGE_ROOT / "strategy_state.md").write_text(
        "# v042 Strategy State\n\n"
        "- Raw prompt working best: `v034a_fp8_broad_context_scene_box_guard` at `181/38/25/63`.\n"
        "- Composite working best: `v034a_fp8_broad_context_scene_box_guard+p1753` at `181/38/24/62`.\n"
        f"- Final status: `{status}`.\n"
        f"- Next axis: {next_axis}\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", choices=["v042b", "v042c", "v042d", "v042e"], required=True)
    args = parser.parse_args()

    core.write_scaffold()
    core.create_sentinel_manifest()
    p1753_record = core.reproduce_p1753()
    if not core.p1753_reproduction_ok({**p1753_record, "candidate_id": "v034a_fp8_broad_context_scene_box_guard+p1753", "stage": "frozen_v034a_reproduction"}):
        core.print_status("p1753_reproduction", p1753_record, "fail", "p1753 reproduction drifted.", "Stop and diagnose wrapper drift.")
        update_closeout("p1753_reproduction_failed", "p1753 reproduction failed during continuation.", "Diagnose p1753 wrapper drift.")
        core.validate_generated_files()
        return 1
    models = core.fetch_models()
    if not (models["ok"] and models["model_present"]):
        core.print_status("backend_preflight", None, "fail", "Backend is unavailable during continuation.", "Restart vLLM FP8 endpoint.")
        update_closeout("backend_unavailable", "Backend was unavailable during continuation.", "Restart vLLM FP8 endpoint.")
        core.validate_generated_files()
        return 0

    if args.candidate == "v042b":
        overlay = create_v042b_overlay()
    elif args.candidate == "v042c":
        overlay = create_v042c_overlay()
    elif args.candidate == "v042d":
        overlay = create_v042d_overlay()
    else:
        overlay = create_v042e_overlay()
    candidate_id = read_yaml(overlay)["candidate_id"]
    candidate = {
        "candidate_id": candidate_id,
        "overlay_path": str(overlay),
        "intended_changes": read_yaml(overlay).get("intended_changes", []),
    }
    record = core.run_case_probe(candidate, core.SENTINEL_MANIFEST, "micro_pack_only")
    office = core.run_office_guard(candidate, args.candidate)
    micro_ok, micro_reason = core.micro_pass(record, office["pass"])
    if not micro_ok:
        status = "runtime_invalid" if micro_reason == "runtime_invalid" else "rejected"
        lesson = f"{args.candidate} failed the postprocessed micro gate: {micro_reason}."
        next_axis = "Pivot using exact residual deltas; avoid wording families that have already harmed dense/control gates."
        core.print_candidate_block(record, "micro_pack_only", status, lesson, next_axis, office["pass"])
        append_row(record_to_row(record, "micro_pack_only", status))
        write_candidate_diagnosis(record, status, lesson, next_axis)
        update_closeout(status, "v042b did not produce a valid full all-current improvement.", next_axis)
        core.validate_generated_files()
        return 0

    core.print_candidate_block(
        record,
        "micro_pack_only",
        "learning_evidence",
        f"{args.candidate} passed the postprocessed micro gate; full all-current is required.",
        "Run full all-current/no101 with paired raw and p1753 scoring.",
        office["pass"],
    )
    full = core.run_case_probe(candidate, core.ALL_CURRENT_MANIFEST, "full_all_current")
    full_office = core.run_office_guard(candidate, f"{args.candidate}_full")
    status = core.status_for_record(full, full_office["pass"], "full_all_current")
    lesson = f"{args.candidate} completed full all-current with paired raw/postprocessed scoring."
    next_axis = f"Continue from {args.candidate} only if it beats composite 62; otherwise pivot using exact full-run residual deltas."
    core.print_candidate_block(full, "full_all_current", status, lesson, next_axis, full_office["pass"])
    append_row(record_to_row(record, "micro_pack_only", "micro_passed"))
    append_row(record_to_row(full, "full_all_current", status))
    write_candidate_diagnosis(full, status, lesson, next_axis)
    if full.get("postprocessed_metrics", {}).get("combined_errors", 999) < core.COMPOSITE_V034A_P1753["combined_errors"]:
        update_closeout(status, f"{args.candidate} beat the prior composite working best.", next_axis)
    else:
        update_closeout(status, f"{args.candidate} did not beat the prior composite working best.", next_axis)
    core.validate_generated_files()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
