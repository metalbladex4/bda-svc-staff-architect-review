#!/usr/bin/env python3
"""Build v047 pp046a visual verification and FN-recovery evidence."""

from __future__ import annotations

import csv
import datetime as dt
import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw


WORKTREE = Path("/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement")
CAPSTONE = Path("/home/williambenitez1/Capstone")
PARENT = WORKTREE / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion"
PACKAGE = PARENT / "v047_fp8_pp046a_visual_verification_and_fn_recovery"
V046_SCRIPT = PARENT / "v046_fp8_pp045_visual_verification_and_continuation/scripts/run_v046_pp045_visual_verification.py"
IMAGE_ROOT = CAPSTONE / "z_reference_docs/Data_set_Storage/human_reports/images_with_reports"

OLD_V020C = {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58}
PP045C = {"matches": 181, "false_negatives": 38, "false_positives": 11, "combined_errors": 49}
PP046A = {"matches": 181, "false_negatives": 38, "false_positives": 0, "combined_errors": 38}
WATCH_CASES = ["66", "67", "84", "100", "110", "155", "166"]

spec = importlib.util.spec_from_file_location("v047_v046", V046_SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot import v046 helpers from {V046_SCRIPT}")
v046 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = v046
spec.loader.exec_module(v046)
v045 = v046.v045
v044 = v046.v044
v042 = v046.v042


def now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


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


def case_metric_map(eval_payload: dict[str, Any]) -> dict[str, str]:
    return {
        v044.case_id(img["image_filename"]): f"{img['match_count']}/{img['false_negative_count']}/{img['false_positive_count']}"
        for img in eval_payload["images"]
    }


def generate_review_sheets(removals: list[dict[str, Any]]) -> dict[str, str]:
    by_case: dict[str, list[dict[str, Any]]] = {}
    for row in removals:
        by_case.setdefault(row["case_id"], []).append(row)
    sheet_paths: dict[str, str] = {}
    for case_id, rows in by_case.items():
        image_path = IMAGE_ROOT / rows[0]["image_filename"]
        src = Image.open(image_path).convert("RGB")
        overview = src.copy()
        draw = ImageDraw.Draw(overview)
        for idx, row in enumerate(rows, 1):
            box = [float(v) for v in row["removed_bbox"]]
            draw.rectangle(box, outline=(255, 40, 40), width=5)
            draw.text(
                (box[0] + 2, max(0, box[1] - 20)),
                f"{idx}:{row['removed_label']}",
                fill=(255, 255, 255),
                stroke_width=2,
                stroke_fill=(0, 0, 0),
            )
        draw.text((10, 10), f"case {case_id} pp046a review", fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
        overview.thumbnail((900, 520))
        crops: list[Image.Image] = []
        for idx, row in enumerate(rows, 1):
            box = [float(v) for v in row["removed_bbox"]]
            pad = 120
            crop = src.crop((max(0, box[0] - pad), max(0, box[1] - pad), min(src.width, box[2] + pad), min(src.height, box[3] + pad)))
            crop_draw = ImageDraw.Draw(crop)
            ox = max(0, box[0] - pad)
            oy = max(0, box[1] - pad)
            crop_draw.rectangle([box[0] - ox, box[1] - oy, box[2] - ox, box[3] - oy], outline=(255, 40, 40), width=4)
            crop_draw.text((5, 5), f"{idx}:{row['removed_label']} {row['removed_target_type']}", fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
            crop_draw.text((5, 28), row["reason_removed"][:42], fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
            crop.thumbnail((420, 260))
            crops.append(crop)
        cols = 2
        crop_w = max((crop.width for crop in crops), default=1)
        crop_h = max((crop.height for crop in crops), default=1)
        sheet = Image.new("RGB", (max(overview.width, cols * crop_w + 20), overview.height + 20 + ((len(crops) + 1) // 2) * (crop_h + 10)), (245, 245, 245))
        sheet.paste(overview, ((sheet.width - overview.width) // 2, 0))
        for idx, crop in enumerate(crops):
            sheet.paste(crop, ((idx % cols) * (crop_w + 10), overview.height + 20 + (idx // cols) * (crop_h + 10)))
        out = PACKAGE / f"review_images/local_only_pp046a_case_{case_id}_review.jpg"
        out.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(out, quality=92)
        sheet_paths[case_id] = str(out)
    return sheet_paths


def pp046a_visual_rows(removals: list[dict[str, Any]], sheet_paths: dict[str, str]) -> list[dict[str, Any]]:
    notes = {
        ("19", "target_0"): ("context artifact", "true", "right-edge statue/base and fence context beside the destroyed vehicle scene, not a building target for BDA scoring."),
        ("66", "target_4"): ("ambiguous", "false", "tiny far-tail convoy/vehicle sliver; may be real military equipment, so suppressing it is not safe enough to lock."),
        ("67", "target_0"): ("ambiguous", "false", "tiny far-left object/dust cue in a dense armor row; could be a real distant vehicle, so this threatens dense recall."),
        ("67", "target_1"): ("ambiguous", "false", "tiny far-left object/dust cue in a dense armor row; could be a real distant vehicle, so this threatens dense recall."),
        ("67", "target_2"): ("ambiguous", "false", "tiny far-left object/dust cue in a dense armor row; could be a real distant vehicle, so this threatens dense recall."),
        ("77", "target_1"): ("context artifact", "true", "right-edge adjacent damaged-building slice, broad context separate from the central annotated building body."),
        ("92", "target_1"): ("real target", "false", "box covers a visible trailer/cargo component attached to military equipment; suppressing cross-object equipment is visually unsafe."),
        ("97", "target_1"): ("context artifact", "true", "oversized right-side alley wall/context region rather than a discrete target body."),
        ("103", "target_0"): ("context artifact", "true", "intact adjacent school/annex building, not battle-damaged target evidence."),
        ("105", "target_2"): ("context artifact", "true", "right-edge canopy/tennis-court context, not a damaged building target."),
        ("110", "target_0"): ("context artifact", "true", "small pole/roadside/vehicle-edge context above the convoy, not a separate equipment target."),
    }
    rows: list[dict[str, Any]] = []
    for row in removals:
        verdict, trusted, note = notes[(row["case_id"], row["removed_label"])]
        rows.append(
            {
                "case_id": row["case_id"],
                "image_filename": row["image_filename"],
                "removed_label": row["removed_label"],
                "removed_target_type": row["removed_target_type"],
                "removed_bbox": json.dumps(row["removed_bbox"]),
                "rule_reason": row["reason_removed"],
                "visual_verdict": verdict,
                "removal_should_be_trusted": trusted,
                "generalizes_safely": "false" if trusted == "false" else "limited_needs_replay",
                "reviewer_note": note,
                "source_artifact_path": sheet_paths.get(row["case_id"], ""),
            }
        )
    return rows


def fn_class(case_id: str, target_type: str, bbox: list[float]) -> str:
    if case_id in {"67", "84"}:
        return "dense_valid_target_missed"
    if case_id == "110":
        return "smoke_or_debris_obscured"
    if target_type == "buildings":
        return "building_or_structure_piece"
    x1, y1, x2, y2 = bbox
    area = max(0.0, x2 - x1) * max(0.0, y2 - y1)
    if area < 3000:
        return "small_valid_target_missed"
    return "unknown"


def fn_recovery_type(case_id: str, cls: str) -> str:
    if cls in {"dense_valid_target_missed", "smoke_or_debris_obscured", "small_valid_target_missed"}:
        return "B"
    if cls == "building_or_structure_piece":
        return "D"
    return "C"


def residual_fn_rows(eval_payload: dict[str, Any], refs: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for image in eval_payload["images"]:
        cid = v044.case_id(image["image_filename"])
        ref_report = refs[image["image_filename"]]
        for label in image["false_negative_labels"]:
            target = ref_report["physical_damage"].get(label, {})
            ttype = target.get("target_type", "unknown")
            bbox = list(v044.target_box(target)) if target else []
            cls = fn_class(cid, ttype, bbox)
            recovery = fn_recovery_type(cid, cls)
            rows.append(
                {
                    "case_id": cid,
                    "image_filename": image["image_filename"],
                    "reference_label": label,
                    "target_type": ttype,
                    "reference_bbox": json.dumps(bbox),
                    "visual_class": cls,
                    "likely_recoverable_by": recovery,
                    "risk_to_dense_cases": str(cid in {"66", "67", "84", "97"}).lower(),
                    "risk_to_false_positives": "high" if recovery == "A" else "medium" if recovery in {"B", "C"} else "low",
                    "reviewer_note": "Needs crop/verifier or tiling review before any recall prompt; broad prompt recall is unsafe after prior dense-row failures.",
                }
            )
    return rows


def main() -> None:
    generated = now()
    for subdir in ["scripts", "tables", "review_images", "verifier_designs", "prompt_overlays", "runs"]:
        (PACKAGE / subdir).mkdir(parents=True, exist_ok=True)

    state = v044.load_state()
    refs = state["refs"]
    order = state["order"]
    dims = state["dims"]
    pp0157_preds, _ = v044.apply_pp0157(state["p1753"], dims)
    pp044a_preds, _ = v044.apply_pp044a(pp0157_preds, dims)
    pp045b_preds, _ = v045.apply_pp045b(pp044a_preds, dims)
    pp045c_preds, _ = v045.apply_pp045c(pp045b_preds, dims)
    pp045c_eval = v042.evaluate_reports(refs, pp045c_preds, order)
    pp046a_preds, pp046a_removals = v046.apply_pp046a(pp045c_preds, refs, order, dims)
    pp046a_eval = v042.evaluate_reports(refs, pp046a_preds, order)
    pp046a_cases = case_metric_map(pp046a_eval)
    pp045c_cases = case_metric_map(pp045c_eval)
    sheet_paths = generate_review_sheets(pp046a_removals)
    visual_rows = pp046a_visual_rows(pp046a_removals, sheet_paths)
    visual_failures = [row for row in visual_rows if row["removal_should_be_trusted"] != "true"]
    pp046a_pass = not visual_failures
    selected_eval = pp046a_eval if pp046a_pass else pp045c_eval
    selected_name = "pp046a_38" if pp046a_pass else "pp045c_49"
    selected_cases = pp046a_cases if pp046a_pass else pp045c_cases
    fn_rows = residual_fn_rows(pp046a_eval, refs)
    fn_classes = sorted({row["visual_class"] for row in fn_rows})
    verifier_plan = {
        "generated_at": generated,
        "selected_baseline": selected_name,
        "prompt_candidate_authored": False,
        "reason_no_prompt_candidate": "pp046a visual review failed/mixed; broad recall prompt remains high-risk, and FN clusters need crop/tiling/verifier review first.",
        "recommended_next_work": [
            {"axis": "visual_review", "description": "Review unsafe pp046a military-equipment removals in cases 66, 67, and 92 before any residual-FP rule lock."},
            {"axis": "crop_level_verifier", "description": "Create crops for each FN reference bbox and nearby predicted boxes to classify recoverable small/dense/smoke-obscured misses."},
            {"axis": "tiling_crop_strategy", "description": "Run experiment-only crop or tile pass for dense/small FN clusters before prompt wording."},
            {"axis": "prompt", "description": "Do not author prompt until FN crop review identifies one low-risk cluster and a micro-gated recall cue."},
        ],
    }
    source_manifest = {
        "generated_at": generated,
        "source_artifacts_read": [
            str(PARENT / "v046_fp8_pp045_visual_verification_and_continuation/final_recommendation.md"),
            str(PARENT / "v046_fp8_pp045_visual_verification_and_continuation/intervention_matrix.md"),
            str(PARENT / "v046_fp8_pp045_visual_verification_and_continuation/intervention_matrix.json"),
            str(PARENT / "v045_fp8_pp044a_cross_label_visual_review/final_recommendation.md"),
            str(PARENT / "v044_fp8_pp0157_visual_verification_and_continuation/final_recommendation.md"),
            str(CAPSTONE / "z_reference_docs/GPT-Pro_collab/bda_svc_qwen_prompt_engineering_deep_research_bundle.md"),
            str(CAPSTONE / "z_reference_docs/GPT-Pro_collab/CODEX_QWEN_PROMPT_ENGINEERING_DIRECTION_2026-05-06.md"),
            str(CAPSTONE / "z_reference_docs/Prompting"),
        ],
        "metrics_confirmed": {
            "old_v020c": OLD_V020C,
            "pp045c": PP045C,
            "pp046a": PP046A,
            "v024o": "partial_unscored_forbidden",
        },
        "hard_boundaries": ["experiment-only", "no promotion", "no product runtime mutation", "no source-truth mutation", "no raw image push"],
    }
    artifact_inventory = {
        "generated_at": generated,
        "artifacts": [
            {"kind": "v046_final_recommendation", "path": str(PARENT / "v046_fp8_pp045_visual_verification_and_continuation/final_recommendation.md"), "exists": True},
            {"kind": "v046_intervention_matrix", "path": str(PARENT / "v046_fp8_pp045_visual_verification_and_continuation/intervention_matrix.json"), "exists": True},
            {"kind": "pp046a_rule", "path": str(PARENT / "v046_fp8_pp045_visual_verification_and_continuation/postprocess_rules/pp046a_prediction_only_residual_fp_cleanup_probe.json"), "exists": True},
            {"kind": "v034a_raw_predictions", "path": str(v042.V034_FULL_RUN_ROOT / "predicted"), "exists": (v042.V034_FULL_RUN_ROOT / "predicted").exists()},
            {"kind": "local_only_pp046a_review_sheets", "path": str(PACKAGE / "review_images"), "exists": True, "note": "not copied to review repo"},
        ],
        "missing_artifacts": [],
    }
    interventions = [
        {
            "intervention_id": "vr001_pp046a_removed_box_visual_review",
            "type": "visual_review",
            "baseline": "pp046a_38",
            "metrics": pp046a_eval["totals"],
            "removed_predictions": len(pp046a_removals),
            "removed_true_positives": 0,
            "status": "visual_pass" if pp046a_pass else "visual_fail",
            "visual_verdict": "pass" if pp046a_pass else "mixed",
            "case_metrics": {k: pp046a_cases.get(k, "n/a") for k in WATCH_CASES},
            "unsafe_or_ambiguous_count": len(visual_failures),
        },
        {
            "intervention_id": "fn001_residual_fn_inventory",
            "type": "fn_inventory",
            "baseline": selected_name,
            "metrics": selected_eval["totals"],
            "status": "fn_inventory_complete",
            "fn_count": len(fn_rows),
            "classes": fn_classes,
        },
        {
            "intervention_id": "vd001_verifier_fn_recovery_plan",
            "type": "verifier_design",
            "baseline": selected_name,
            "metrics": selected_eval["totals"],
            "status": "verifier_plan_complete",
            "prompt_candidate_authored": False,
        },
    ]
    pp046a_rule = json.loads((PARENT / "v046_fp8_pp045_visual_verification_and_continuation/postprocess_rules/pp046a_prediction_only_residual_fp_cleanup_probe.json").read_text())
    pp046a_rule["visual_review_status"] = "pass" if pp046a_pass else "mixed_fail"
    pp046a_rule["accepted_as_baseline"] = pp046a_pass

    write_text(PACKAGE / "README.md", "# v047 FP8 PP046A Visual Verification And FN Recovery\n\nExperiment-only pp046a visual verification and false-negative recovery planning.\n")
    write_json(PACKAGE / "source_manifest.json", source_manifest)
    write_json(PACKAGE / "artifact_inventory.json", artifact_inventory)
    write_text(PACKAGE / "artifact_inventory.md", "# Artifact Inventory\n\nLocated v046 pp046a rule/removals, frozen v034a-derived outputs, eval state, and local source images for pp046a visual review.\n")
    write_json(PACKAGE / "pp046a_rule_spec.json", pp046a_rule)
    write_text(PACKAGE / "pp046a_rule_spec.md", f"# pp046a Rule Spec\n\n```json\n{json.dumps(pp046a_rule, indent=2)}\n```\n")
    write_json(PACKAGE / "pp046a_removed_box_visual_review.json", {"generated_at": generated, "pp046a_visual_pass": pp046a_pass, "visual_verdict": "pass" if pp046a_pass else "mixed", "rows": visual_rows})
    write_csv(PACKAGE / "pp046a_removed_box_visual_review.csv", visual_rows)
    write_text(PACKAGE / "pp046a_removed_box_visual_review.md", "\n".join([
        "# pp046a Removed Box Visual Review",
        "",
        f"Visual verdict: `{'pass' if pp046a_pass else 'mixed_fail'}`.",
        "",
        "pp046a is not locked because case 66, case 67, and case 92 removals look visually unsafe or ambiguous enough to threaten recall.",
        "",
    ]))
    write_json(PACKAGE / "residual_fn_inventory_after_pp046a.json", {"generated_at": generated, "baseline": "diagnostic_pp046a_38", "fn_count": len(fn_rows), "errors": fn_rows})
    write_text(PACKAGE / "residual_fn_inventory_after_pp046a.md", f"# Residual FN Inventory After pp046a Diagnostic Scoring\n\npp046a leaves `{len(fn_rows)}` false negatives. Because visual review failed, this is a diagnostic FN inventory, not a locked-baseline inventory.\n\nClasses: `{', '.join(fn_classes)}`.\n")
    write_csv(PACKAGE / "residual_fn_taxonomy.csv", fn_rows)
    write_json(PACKAGE / "verifier_design_plan.json", verifier_plan)
    write_text(PACKAGE / "verifier_design_plan.md", "# Verifier Design Plan\n\nDo not author another prompt yet. First visual-review unsafe pp046a removals, then build crop-level FN review/verifier data for dense, small, smoke-obscured, and building-piece misses.\n")
    write_json(PACKAGE / "intervention_registry.json", {"generated_at": generated, "interventions": interventions})
    write_json(PACKAGE / "intervention_matrix.json", {"generated_at": generated, "rows": interventions})
    write_text(PACKAGE / "intervention_matrix.md", "\n".join([
        "# Intervention Matrix",
        "",
        "| Intervention | Type | Baseline | Metrics | Status |",
        "|---|---|---|---:|---|",
        *[
            f"| `{row['intervention_id']}` | {row['type']} | {row['baseline']} | `{metric_line(row['metrics'])}` | {row['status']} |"
            for row in interventions
        ],
        "",
    ]))
    write_text(PACKAGE / "live_metrics_log.md", f"""# Live Metrics Log

- Old/product v020c: `186 / 33 / 25 / 58`.
- pp045c locked baseline: `{metric_line(pp045c_eval['totals'])}`.
- pp046a diagnostic simulation: `{metric_line(pp046a_eval['totals'])}`.
- pp046a visual verdict: `{'pass' if pp046a_pass else 'mixed_fail'}`.
""")
    write_json(PACKAGE / "recovery_log.json", {"generated_at": generated, "events": ["offline-only tranche", "pp046a visual review mixed/fail", "pp045c retained as locked baseline", "residual FN inventory created", "verifier plan written", "no prompt candidate authored"]})
    write_text(PACKAGE / "recovery_log.md", "# Recovery Log\n\n- Offline-only tranche; no backend or live VLM call used.\n- pp046a visual review was mixed/fail.\n- pp045c remains the locked experiment-only baseline.\n- Residual FN inventory and verifier plan were written.\n")
    write_text(PACKAGE / "lessons_learned.md", "# Lessons Learned\n\n- Zero-FP eval scoring is not enough: case 66, case 67, and case 92 removals include visually plausible military equipment.\n- pp046a is useful as a diagnostic upper bound on FP suppression, not as a locked deployable baseline.\n- The next honest lever is FN crop/verifier/tiling review, not another broad prompt recall cue.\n")
    write_text(PACKAGE / "strategy_state.md", f"# Strategy State\n\nSelected locked baseline: `fp8_composite_pp045c_baseline = {metric_line(pp045c_eval['totals'])}`.\n\nDiagnostic pp046a score: `{metric_line(pp046a_eval['totals'])}` but not locked.\n\nPrompt candidate authored: `False`.\n\nNext axis: pp046a unsafe-removal review plus FN crop/verifier design.\n")
    write_json(PACKAGE / "verifier_designs/fn_crop_verifier_design.json", verifier_plan)
    write_text(PACKAGE / "verifier_designs/fn_crop_verifier_design.md", "# FN Crop Verifier Design\n\nCreate reference-centered crops for all 38 FNs, include nearby predictions, and classify recoverability before any prompt recall candidate.\n")
    write_text(PACKAGE / "pause_report_2026-05-09_235900Z_pp046a_visual_mixed.md", f"# v047 Pause Report\n\nStop reason: pp046a visual review mixed/fail.\n\nLocked baseline remains `pp045c = {metric_line(pp045c_eval['totals'])}`.\n\nDiagnostic pp046a score remains `{metric_line(pp046a_eval['totals'])}` but is not locked.\n")

    final_json = {
        "generated_at": generated,
        "pp046a_visual_review_passed": pp046a_pass,
        "pp046a_locked_as_experiment_only_baseline": pp046a_pass,
        "selected_experiment_only_baseline": {"id": "fp8_composite_pp046a_baseline" if pp046a_pass else "fp8_composite_pp045c_baseline", **selected_eval["totals"]},
        "diagnostic_pp046a_result": {"id": "pp046a_prediction_only_residual_fp_cleanup_probe", **pp046a_eval["totals"], "visual_status": "pass" if pp046a_pass else "mixed_fail"},
        "target_le_1_reached": selected_eval["totals"]["combined_errors"] <= 1,
        "residual_fn_classes": fn_classes,
        "optional_prompt_candidate_run": False,
        "next_work": "verifier_or_tiling_crop_strategy_before_prompt",
        "hard_boundaries_preserved": True,
    }
    write_json(PACKAGE / "final_recommendation.json", final_json)
    write_text(PACKAGE / "final_recommendation.md", f"""# v047 Final Recommendation

Generated: `{generated}`

pp046a visual review passed: `{pp046a_pass}`.

pp046a locked as experiment-only composite baseline: `{pp046a_pass}`.

Selected locked baseline: `{'fp8_composite_pp046a_baseline' if pp046a_pass else 'fp8_composite_pp045c_baseline'} = {metric_line(selected_eval['totals'])}`.

Diagnostic pp046a score: `{metric_line(pp046a_eval['totals'])}`.

Reached <=1 target: `{selected_eval['totals']['combined_errors'] <= 1}`.

## pp046a Visual Review

Safe removals: cases `19`, `77`, `97`, `103`, `105`, and `110` looked like context artifacts or non-target structure.

Unsafe or ambiguous removals: case `66` target_4, case `67` targets 0-2, and case `92` target_1 look visually plausible as real military equipment or dense-row targets. pp046a therefore fails the visual lock gate.

## Residual FN Classes

`{', '.join(fn_classes)}`.

## Next Work

Do verifier/tiling/crop review before another prompt. No optional prompt candidate was authored.

Hard boundaries were preserved.
""")

    print(f"""=== V047 STATUS ===
phase: artifact_inventory
baseline: pp045c_49
intervention: none
type: none
metrics: n/a
case_66: n/a
case_67: n/a
case_84: n/a
case_100: n/a
case_110: n/a
case_155: n/a
case_166: n/a
office_negative: n/a
removed_predictions: n/a
removed_true_positives: n/a
pp046a_visual_verdict: n/a
status: stopped
main_lesson: v046 artifacts and pp046a removals were reconstructed from frozen outputs.
next_axis: Visual-review all pp046a removals.
===================""")
    print(f"""=== V047 STATUS ===
phase: pp046a_visual_review
baseline: {'pp046a_38' if pp046a_pass else 'pp045c_49'}
intervention: vr001_pp046a_removed_box_visual_review
type: visual_review
metrics: {metric_line(pp046a_eval['totals'])}
case_66: {pp046a_cases.get('66')}
case_67: {pp046a_cases.get('67')}
case_84: {pp046a_cases.get('84')}
case_100: {pp046a_cases.get('100')}
case_110: {pp046a_cases.get('110')}
case_155: {pp046a_cases.get('155')}
case_166: {pp046a_cases.get('166')}
office_negative: not_run
removed_predictions: {len(pp046a_removals)}
removed_true_positives: 0
pp046a_visual_verdict: {'pass' if pp046a_pass else 'mixed'}
status: {'visual_pass' if pp046a_pass else 'visual_fail'}
main_lesson: pp046a is not safe to lock because several military-equipment removals are visually ambiguous or real.
next_axis: Fall back to pp045c and inventory residual FNs.
===================""")
    print(f"""=== V047 STATUS ===
phase: residual_fn_inventory
baseline: {selected_name}
intervention: fn001_residual_fn_inventory
type: fn_inventory
metrics: {metric_line(selected_eval['totals'])}
case_66: {selected_cases.get('66')}
case_67: {selected_cases.get('67')}
case_84: {selected_cases.get('84')}
case_100: {selected_cases.get('100')}
case_110: {selected_cases.get('110')}
case_155: {selected_cases.get('155')}
case_166: {selected_cases.get('166')}
office_negative: not_run
removed_predictions: n/a
removed_true_positives: n/a
pp046a_visual_verdict: {'pass' if pp046a_pass else 'mixed'}
status: fn_inventory_complete
main_lesson: pp046a leaves 38 FNs, but FN recovery needs crop/verifier review before prompt wording.
next_axis: Write verifier/FN-recovery plan.
===================""")
    print(f"""=== V047 STATUS ===
phase: verifier_design
baseline: {selected_name}
intervention: vd001_verifier_fn_recovery_plan
type: verifier_design
metrics: {metric_line(selected_eval['totals'])}
case_66: {selected_cases.get('66')}
case_67: {selected_cases.get('67')}
case_84: {selected_cases.get('84')}
case_100: {selected_cases.get('100')}
case_110: {selected_cases.get('110')}
case_155: {selected_cases.get('155')}
case_166: {selected_cases.get('166')}
office_negative: not_run
removed_predictions: n/a
removed_true_positives: n/a
pp046a_visual_verdict: {'pass' if pp046a_pass else 'mixed'}
status: verifier_plan_complete
main_lesson: Next work should be verifier/tiling/crop strategy rather than prompt wording.
next_axis: Visual-review unsafe pp046a removals and build FN crop verifier data.
===================""")


if __name__ == "__main__":
    main()
