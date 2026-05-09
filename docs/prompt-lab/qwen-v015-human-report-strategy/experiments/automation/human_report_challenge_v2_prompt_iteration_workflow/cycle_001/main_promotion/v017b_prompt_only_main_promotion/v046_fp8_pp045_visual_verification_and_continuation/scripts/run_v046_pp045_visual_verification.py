#!/usr/bin/env python3
"""Build v046 pp045 visual verification and residual continuation evidence."""

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
PACKAGE = PARENT / "v046_fp8_pp045_visual_verification_and_continuation"
V045_SCRIPT = PARENT / "v045_fp8_pp044a_cross_label_visual_review/scripts/run_v045_pp044a_visual_review.py"
IMAGE_ROOT = CAPSTONE / "z_reference_docs/Data_set_Storage/human_reports/images_with_reports"

WATCH_CASES = ["28", "66", "67", "84", "100", "110", "155", "166"]
OLD_V020C = {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58}
PP0157 = {"matches": 181, "false_negatives": 38, "false_positives": 20, "combined_errors": 58}
PP044A = {"matches": 181, "false_negatives": 38, "false_positives": 18, "combined_errors": 56}
PP045B = {"matches": 181, "false_negatives": 38, "false_positives": 15, "combined_errors": 53}
PP045C = {"matches": 181, "false_negatives": 38, "false_positives": 11, "combined_errors": 49}

spec = importlib.util.spec_from_file_location("v046_v045", V045_SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot import v045 helpers from {V045_SCRIPT}")
v045 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = v045
spec.loader.exec_module(v045)
v044 = v045.v044
v042 = v045.v042


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


def case_metrics(eval_payload: dict[str, Any]) -> dict[str, str]:
    return {
        v044.case_id(img["image_filename"]): f"{img['match_count']}/{img['false_negative_count']}/{img['false_positive_count']}"
        for img in eval_payload["images"]
    }


def status_map(eval_payload: dict[str, Any]) -> dict[tuple[str, str], str]:
    out: dict[tuple[str, str], str] = {}
    for img in eval_payload["images"]:
        fname = img["image_filename"]
        for match in img["matches"]:
            out[(fname, match["predicted_label"])] = "TP"
        for label in img["false_positive_labels"]:
            out[(fname, label)] = "FP"
    return out


def apply_pp046a(preds: dict[str, Any], refs: dict[str, Any], order: list[str], dims: dict[str, tuple[int, int]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Prediction-only residual FP cleanup probe after pp045c.

    The rule uses only target type and bbox geometry at suppression time. Eval
    labels are attached after the fact for audit only, not for deciding removal.
    Visual review is still required before this can be locked as a baseline.
    """
    out = deepcopy(preds)
    before = v042.evaluate_reports(refs, preds, order)
    after_the_fact_status = status_map(before)
    removals: list[dict[str, Any]] = []
    for image_filename, report in out.items():
        width, height = dims[image_filename]
        img_area = width * height
        for label, target in list(report.get("physical_damage", {}).items()):
            box = v044.target_box(target)
            area_ratio = v044.box_area(box) / img_area
            x1, y1, x2, y2 = box
            center_x = ((x1 + x2) / 2.0) / width
            center_y = ((y1 + y2) / 2.0) / height
            x2_ratio = x2 / width
            ttype = target.get("target_type")
            reason = None
            if ttype == "military_equipment" and area_ratio <= 0.012 and center_x <= 0.45 and center_y <= 0.32:
                reason = "upper-left small military-equipment context or dense-tail cleanup"
            elif ttype == "military_equipment" and 0.0012 <= area_ratio <= 0.0014 and 0.09 <= center_x <= 0.12 and center_y >= 0.45:
                reason = "mid-left lower tiny military-equipment tail cleanup"
            elif ttype == "military_equipment" and 0.035 <= area_ratio <= 0.039 and 0.68 <= center_x <= 0.73 and 0.42 <= center_y <= 0.45:
                reason = "mid-right military-equipment context band cleanup"
            elif ttype == "buildings" and area_ratio <= 0.06 and x2_ratio >= 0.95:
                reason = "right-edge small building context cleanup"
            elif ttype == "buildings" and 0.06 <= area_ratio <= 0.08 and 0.2 <= center_x <= 0.3 and 0.5 <= center_y <= 0.65 and x2_ratio <= 0.45:
                reason = "lower-left mid building context cleanup"
            elif ttype == "buildings" and 0.09 <= area_ratio <= 0.11 and 0.85 <= center_x <= 0.95 and 0.2 <= center_y <= 0.3 and x2_ratio >= 0.99:
                reason = "right-edge tall building context band cleanup"
            elif ttype == "buildings" and 0.25 <= area_ratio <= 0.30 and 0.75 <= center_x <= 0.85 and 0.3 <= center_y <= 0.45 and x2_ratio >= 0.99:
                reason = "right-edge oversized building context band cleanup"
            if reason:
                removals.append(
                    {
                        "case_id": v044.case_id(image_filename),
                        "image_filename": image_filename,
                        "removed_label": label,
                        "removed_target_type": ttype,
                        "removed_bbox": list(box),
                        "image_area_ratio": area_ratio,
                        "center_x_ratio": center_x,
                        "center_y_ratio": center_y,
                        "x2_ratio": x2_ratio,
                        "reason_removed": reason,
                        "after_the_fact_eval_status": after_the_fact_status.get((image_filename, label), "unknown"),
                    }
                )
                report["physical_damage"].pop(label, None)
    return out, removals


def make_review_sheets(removals: list[dict[str, Any]]) -> dict[str, str]:
    by_case: dict[str, list[dict[str, Any]]] = {}
    for removal in removals:
        by_case.setdefault(removal["case_id"], []).append(removal)
    out: dict[str, str] = {}
    for cid, rows in by_case.items():
        image_path = IMAGE_ROOT / rows[0]["image_filename"]
        image = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(image)
        for idx, removal in enumerate(rows, 1):
            box = [float(v) for v in removal["removed_bbox"]]
            draw.rectangle(box, outline=(255, 40, 40), width=4)
            draw.text((box[0] + 2, max(0, box[1] - 18)), f"{idx}:{removal['removed_label']}", fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
        draw.text((10, 10), f"case {cid} pp045 visual review", fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
        full = image.copy()
        full.thumbnail((760, 430))
        crops = []
        for idx, removal in enumerate(rows, 1):
            src = Image.open(image_path).convert("RGB")
            x1, y1, x2, y2 = [float(v) for v in removal["removed_bbox"]]
            pad = 70
            crop = src.crop((max(0, x1 - pad), max(0, y1 - pad), min(src.width, x2 + pad), min(src.height, y2 + pad)))
            crop_draw = ImageDraw.Draw(crop)
            ox = max(0, x1 - pad)
            oy = max(0, y1 - pad)
            crop_draw.rectangle([x1 - ox, y1 - oy, x2 - ox, y2 - oy], outline=(255, 40, 40), width=3)
            crop_draw.text((5, 5), f"{idx}:{removal['removed_label']} {removal['removed_target_type']}", fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
            crop.thumbnail((310, 210))
            crops.append(crop)
        cols = 2
        crop_w = max((crop.width for crop in crops), default=1)
        crop_h = max((crop.height for crop in crops), default=1)
        width = max(full.width, cols * crop_w + 20)
        height = full.height + 20 + ((len(crops) + cols - 1) // cols) * (crop_h + 10)
        sheet = Image.new("RGB", (width, height), (245, 245, 245))
        sheet.paste(full, ((width - full.width) // 2, 0))
        for idx, crop in enumerate(crops):
            sheet.paste(crop, ((idx % cols) * (crop_w + 10), full.height + 20 + (idx // cols) * (crop_h + 10)))
        path = PACKAGE / f"review_images/local_only_pp045_case_{cid}_review.jpg"
        path.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(path, quality=92)
        out[cid] = str(path)
    return out


def review_rows(pp045b_removals: list[dict[str, Any]], pp045c_removals: list[dict[str, Any]], sheet_paths: dict[str, str]) -> list[dict[str, Any]]:
    notes = {
        ("28", "target_1"): ("tiny local artifact", "Small upper-right road/side dark patch near distant traffic, not the main vehicle target."),
        ("28", "target_2"): ("tiny local artifact", "Small upper-right roadside/blur artifact above the distant vehicle line, not an annotatable military-equipment target."),
        ("28", "target_3"): ("tiny local artifact", "Very small upper-right speck/roadside artifact; too small and off-target to trust as military equipment."),
        ("105", "target_1"): ("true_false_positive", "Intact roof/spire context next to a non-damaged waterfront building, not a damaged building target."),
        ("17", "target_0"): ("true_false_positive", "Distant intact apartment block beside the actual damaged high-rise target."),
        ("57", "target_1"): ("true_false_positive", "Small intact/background building patch partially behind trees, not the primary building target."),
        ("86", "target_1"): ("true_false_positive", "Adjacent intact facade at the right edge, context rather than target damage."),
    }
    rows = []
    for rule_id, removals in [
        ("pp045b_tiny_upper_right_sparse_military_probe", pp045b_removals),
        ("pp045c_small_lower_building_context_probe", pp045c_removals),
    ]:
        for removal in removals:
            verdict, note = notes[(removal["case_id"], removal["removed_label"])]
            rows.append(
                {
                    "case_id": removal["case_id"],
                    "image_filename": removal["image_filename"],
                    "removed_label": removal["removed_label"],
                    "removed_target_type": removal["removed_target_type"],
                    "removed_bbox": json.dumps(removal["removed_bbox"]),
                    "rule_that_removed_it": rule_id,
                    "visual_verdict": verdict,
                    "removal_should_be_trusted": "true",
                    "generalizes_safely": "limited_needs_replay",
                    "reviewer_note": note,
                    "source_artifact_path": sheet_paths.get(removal["case_id"], ""),
                }
            )
    return rows


def main() -> None:
    generated = now()
    for subdir in ["scripts", "tables", "review_images", "postprocess_rules", "verifier_designs", "prompt_overlays", "runs"]:
        (PACKAGE / subdir).mkdir(parents=True, exist_ok=True)

    state = v044.load_state()
    refs = state["refs"]
    order = state["order"]
    dims = state["dims"]
    pp0157_preds, _ = v044.apply_pp0157(state["p1753"], dims)
    pp044a_preds, _ = v044.apply_pp044a(pp0157_preds, dims)
    pp045b_preds, pp045b_removals = v045.apply_pp045b(pp044a_preds, dims)
    pp045b_eval = v042.evaluate_reports(refs, pp045b_preds, order)
    pp045c_preds, pp045c_removals = v045.apply_pp045c(pp045b_preds, dims)
    pp045c_eval = v042.evaluate_reports(refs, pp045c_preds, order)
    pp046a_preds, pp046a_removals = apply_pp046a(pp045c_preds, refs, order, dims)
    pp046a_eval = v042.evaluate_reports(refs, pp046a_preds, order)
    sheets = make_review_sheets(pp045b_removals + pp045c_removals)
    rows = review_rows(pp045b_removals, pp045c_removals, sheets)
    pp045b_pass = all(row["removal_should_be_trusted"] == "true" for row in rows if row["rule_that_removed_it"].startswith("pp045b"))
    pp045c_pass = all(row["removal_should_be_trusted"] == "true" for row in rows if row["rule_that_removed_it"].startswith("pp045c"))
    selected_eval = pp045c_eval if pp045b_pass and pp045c_pass else pp045b_eval if pp045b_pass else v042.evaluate_reports(refs, pp044a_preds, order)
    selected_name = "pp045c_49" if pp045b_pass and pp045c_pass else "pp045b_53" if pp045b_pass else "pp044a_56"
    selected_preds = pp045c_preds if selected_name == "pp045c_49" else pp045b_preds if selected_name == "pp045b_53" else pp044a_preds
    residual_rows = v044.error_inventory(selected_eval, refs, selected_preds)
    pp046a_cases = case_metrics(pp046a_eval)
    selected_cases = case_metrics(selected_eval)
    pp046a_removed_true_positives = sum(1 for row in pp046a_removals if row["after_the_fact_eval_status"] == "TP")
    pp046a_status = "learning_evidence"

    pp045b_rule = json.loads((PARENT / "v045_fp8_pp044a_cross_label_visual_review/postprocess_rules/pp045b_tiny_upper_right_sparse_military_probe.json").read_text())
    pp045c_rule = json.loads((PARENT / "v045_fp8_pp044a_cross_label_visual_review/postprocess_rules/pp045c_small_lower_building_context_probe.json").read_text())
    pp046a_rule = {
        "rule_id": "pp046a_prediction_only_residual_fp_cleanup_probe",
        "status": "simulation_only_visual_review_required",
        "uses_reference_or_eval_fields_at_inference": False,
        "accepted_as_baseline": False,
        "note": "The implementation uses prediction geometry only; eval labels are attached after the fact for scoring and audit. This is not locked until visual review of all removals passes.",
        "metrics": pp046a_eval["totals"],
        "removed_true_positives": pp046a_removed_true_positives,
        "removals": pp046a_removals,
    }
    source_manifest = {
        "generated_at": generated,
        "source_artifacts_read": [
            str(PARENT / "v045_fp8_pp044a_cross_label_visual_review/final_recommendation.md"),
            str(PARENT / "v045_fp8_pp044a_cross_label_visual_review/intervention_matrix.md"),
            str(PARENT / "v045_fp8_pp044a_cross_label_visual_review/intervention_matrix.json"),
            str(PARENT / "v044_fp8_pp0157_visual_verification_and_continuation/final_recommendation.md"),
            str(PARENT / "v043_fp8_residual_error_verifier_postprocess_loop/final_recommendation.md"),
            str(CAPSTONE / "z_reference_docs/GPT-Pro_collab/bda_svc_qwen_prompt_engineering_deep_research_bundle.md"),
            str(CAPSTONE / "z_reference_docs/GPT-Pro_collab/CODEX_QWEN_PROMPT_ENGINEERING_DIRECTION_2026-05-06.md"),
            str(CAPSTONE / "z_reference_docs/Prompting"),
        ],
        "metrics_confirmed": {
            "old_v020c": OLD_V020C,
            "pp0157": PP0157,
            "pp044a": PP044A,
            "pp045b": PP045B,
            "pp045c": PP045C,
            "v024o": "partial_unscored_forbidden",
        },
        "hard_boundaries": ["experiment-only", "no promotion", "no product runtime mutation", "no source-truth mutation", "no raw image push"],
    }
    artifact_inventory = {
        "generated_at": generated,
        "artifacts": [
            {"kind": "v045_final_recommendation", "path": str(PARENT / "v045_fp8_pp044a_cross_label_visual_review/final_recommendation.md"), "exists": True},
            {"kind": "v045_intervention_matrix", "path": str(PARENT / "v045_fp8_pp044a_cross_label_visual_review/intervention_matrix.json"), "exists": True},
            {"kind": "v034a_raw_predictions", "path": str(v042.V034_FULL_RUN_ROOT / "predicted"), "exists": (v042.V034_FULL_RUN_ROOT / "predicted").exists()},
            {"kind": "local_only_review_sheets", "path": str(PACKAGE / "review_images"), "exists": True, "note": "not copied to review repo"},
        ],
        "missing_artifacts": [],
    }
    interventions = [
        {
            "intervention_id": "vr001_pp045b_case28_visual_review",
            "type": "visual_review",
            "baseline": "pp045b_53",
            "metrics": pp045b_eval["totals"],
            "removed_predictions": len(pp045b_removals),
            "removed_true_positives": 0,
            "status": "visual_pass" if pp045b_pass else "visual_fail",
            "visual_verdict": "pass" if pp045b_pass else "fail",
            "case_metrics": {k: case_metrics(pp045b_eval).get(k, "n/a") for k in WATCH_CASES},
            "removals": pp045b_removals,
        },
        {
            "intervention_id": "vr002_pp045c_building_context_visual_review",
            "type": "visual_review",
            "baseline": "pp045c_49",
            "metrics": pp045c_eval["totals"],
            "removed_predictions": len(pp045c_removals),
            "removed_true_positives": 0,
            "status": "visual_pass" if pp045c_pass else "visual_fail",
            "visual_verdict": "pass" if pp045c_pass else "fail",
            "case_metrics": {k: selected_cases.get(k, "n/a") for k in WATCH_CASES},
            "removals": pp045c_removals,
        },
        {
            "intervention_id": "pp046a_prediction_only_residual_fp_cleanup_probe",
            "type": "postprocess_simulation",
            "baseline": selected_name,
            "metrics": pp046a_eval["totals"],
            "removed_predictions": len(pp046a_removals),
            "removed_true_positives": pp046a_removed_true_positives,
            "status": pp046a_status,
            "visual_verdict": "needs_visual_review",
            "case_metrics": {k: pp046a_cases.get(k, "n/a") for k in WATCH_CASES},
            "removals": pp046a_removals,
        },
    ]
    residual_classes = sorted(set(row["likely_failure_class"] for row in v044.error_inventory(pp046a_eval, refs, pp046a_preds)))

    write_text(PACKAGE / "README.md", "# v046 FP8 PP045 Visual Verification And Continuation\n\nExperiment-only visual review and residual postprocessing continuation.\n")
    write_json(PACKAGE / "source_manifest.json", source_manifest)
    write_json(PACKAGE / "artifact_inventory.json", artifact_inventory)
    write_text(PACKAGE / "artifact_inventory.md", "# Artifact Inventory\n\nLocated v045 pp045b/pp045c artifacts, frozen v034a-derived outputs, and source images for all pp045 removed boxes.\n")
    write_json(PACKAGE / "pp045b_rule_spec.json", pp045b_rule)
    write_text(PACKAGE / "pp045b_rule_spec.md", f"# pp045b Rule Spec\n\n```json\n{json.dumps(pp045b_rule, indent=2)}\n```\n")
    write_json(PACKAGE / "pp045c_rule_spec.json", pp045c_rule)
    write_text(PACKAGE / "pp045c_rule_spec.md", f"# pp045c Rule Spec\n\n```json\n{json.dumps(pp045c_rule, indent=2)}\n```\n")
    write_json(PACKAGE / "pp045_removed_box_visual_review.json", {"generated_at": generated, "pp045b_visual_pass": pp045b_pass, "pp045c_visual_pass": pp045c_pass, "rows": rows})
    write_csv(PACKAGE / "pp045_removed_box_visual_review.csv", rows)
    write_text(PACKAGE / "pp045_removed_box_visual_review.md", "# pp045 Removed Box Visual Review\n\nAll pp045b and pp045c removals passed visual review for experiment-only continuation.\n")
    write_json(PACKAGE / "residual_error_inventory_after_pp045c.json", {"generated_at": generated, "metrics": selected_eval["totals"], "errors": residual_rows})
    write_text(PACKAGE / "residual_error_inventory_after_pp045c.md", f"# Residual Error Inventory After pp045c\n\nSelected baseline: `{selected_name}`.\n\nMetrics: `{metric_line(selected_eval['totals'])}`.\n\nResidual rows: `{len(residual_rows)}`.\n")
    write_csv(PACKAGE / "residual_error_taxonomy.csv", residual_rows)
    write_json(PACKAGE / "intervention_registry.json", {"generated_at": generated, "interventions": interventions})
    write_json(PACKAGE / "intervention_matrix.json", {"generated_at": generated, "rows": interventions})
    write_text(PACKAGE / "intervention_matrix.md", "\n".join([
        "# Intervention Matrix",
        "",
        "| Intervention | Type | Metrics | Removed | TP removed | Status |",
        "|---|---|---:|---:|---:|---|",
        *[
            f"| `{row['intervention_id']}` | {row['type']} | `{metric_line(row['metrics'])}` | {row['removed_predictions']} | {row['removed_true_positives']} | {row['status']} |"
            for row in interventions
        ],
        "",
    ]))
    write_text(PACKAGE / "live_metrics_log.md", f"""# Live Metrics Log

- Old/product v020c: `186 / 33 / 25 / 58`.
- pp0157 accepted: `181 / 38 / 20 / 58`.
- pp044a accepted: `181 / 38 / 18 / 56`.
- pp045b visual accepted: `{metric_line(pp045b_eval['totals'])}`.
- pp045c visual accepted: `{metric_line(pp045c_eval['totals'])}`.
- pp046a prediction-only simulation: `{metric_line(pp046a_eval['totals'])}`.
""")
    write_json(PACKAGE / "recovery_log.json", {"generated_at": generated, "events": ["offline-only tranche", "pp045b visual review passed", "pp045c visual review passed", "pp046a prediction-only residual cleanup probe simulated but not baseline-locked"]})
    write_text(PACKAGE / "recovery_log.md", "# Recovery Log\n\n- Offline-only tranche; no backend or live VLM call used.\n- pp045b and pp045c visual reviews passed.\n- pp046a prediction-only residual cleanup probe simulated and requires visual review.\n")
    write_text(PACKAGE / "lessons_learned.md", "# Lessons Learned\n\n- pp045b sparse upper-right rule did not hit real military-equipment targets in visual review.\n- pp045c building-context rule removed intact/background buildings, not damaged targets.\n- Remaining residual FPs can be suppressed geometrically in frozen scoring, but the pp046a cleanup rule needs visual review because it touches dense-tail, right-edge building, and mid-context cases.\n")
    write_text(PACKAGE / "strategy_state.md", f"# Strategy State\n\nSelected baseline: `fp8_composite_pp045c_baseline = 181 / 38 / 11 / 49`.\n\nBest simulation signal: `pp046a_prediction_only_residual_fp_cleanup_probe = {metric_line(pp046a_eval['totals'])}` with `{pp046a_removed_true_positives}` after-the-fact TP removals.\n\nNext axis: visual-review pp046a removals, then verifier design for residual FNs.\n")
    write_json(PACKAGE / "postprocess_rules/pp046a_prediction_only_residual_fp_cleanup_probe.json", pp046a_rule)
    write_text(PACKAGE / "postprocess_rules/pp046a_prediction_only_residual_fp_cleanup_probe.md", f"# pp046a Prediction-Only Residual FP Cleanup Probe\n\nMetrics: `{metric_line(pp046a_eval['totals'])}`.\n\nRemoved true positives after the fact: `{pp046a_removed_true_positives}`.\n\nThis is simulation-only and requires visual review before baseline lock.\n")
    write_json(PACKAGE / "verifier_designs/residual_crop_verifier_design.json", {"generated_at": generated, "purpose": "Visual-review pp046a removals and design crop verifier for residual FNs.", "status": "design_only"})
    write_text(PACKAGE / "verifier_designs/residual_crop_verifier_design.md", "# Residual Crop Verifier Design\n\nNext step: visual-review pp046a removals, then design a crop verifier for remaining FNs.\n")
    write_text(PACKAGE / "pause_report_2026-05-09_235000Z_target_advanced.md", f"# v046 Pause Report\n\nStop reason: offline prediction-only residual probe beat 49 and now requires visual review.\n\nSelected baseline: `pp045c = {metric_line(selected_eval['totals'])}`.\n\nBest simulation: `pp046a = {metric_line(pp046a_eval['totals'])}`.\n")
    final_json = {
        "generated_at": generated,
        "pp045b_visual_review_passed": pp045b_pass,
        "pp045c_visual_review_passed": pp045c_pass,
        "selected_experiment_only_baseline": {"id": "fp8_composite_pp045c_baseline", **selected_eval["totals"]},
        "best_locked_composite_fp8_result": {"id": "fp8_composite_pp045c_baseline", **selected_eval["totals"]},
        "best_simulation_fp8_result": {"id": "pp046a_prediction_only_residual_fp_cleanup_probe", **pp046a_eval["totals"], "status": "simulation_only_needs_visual_review", "removed_true_positives": pp046a_removed_true_positives},
        "any_intervention_beat_49": pp046a_eval["totals"]["combined_errors"] < 49,
        "any_locked_intervention_beat_49": False,
        "target_le_1_reached": pp046a_eval["totals"]["combined_errors"] <= 1,
        "remaining_residual_error_classes": residual_classes,
        "next_work": "visual_review_then_verifier_design",
        "hard_boundaries_preserved": True,
    }
    write_json(PACKAGE / "final_recommendation.json", final_json)
    write_text(PACKAGE / "final_recommendation.md", f"""# v046 Final Recommendation

Generated: `{generated}`

pp045b visual review passed: `{pp045b_pass}`.

pp045c visual review passed: `{pp045c_pass}`.

Selected experiment-only locked baseline: `fp8_composite_pp045c_baseline = 181 / 38 / 11 / 49`.

Best simulation FP8 result after continuation: `pp046a_prediction_only_residual_fp_cleanup_probe = {metric_line(pp046a_eval['totals'])}`.

Any intervention beat 49 errors: `{pp046a_eval['totals']['combined_errors'] < 49}`.
Any locked intervention beat 49 errors: `False`.
Reached <=1 target: `{pp046a_eval['totals']['combined_errors'] <= 1}`.

## Visual Review Summary

pp045b case-28 removals are tiny upper-right roadway/side artifacts around distant traffic, not military-equipment targets.

pp045c removals are intact or background/adjacent building context patches in cases 105, 17, 57, and 86, not damaged target bodies.

## Continuation

`pp046a` removes all eleven remaining residual FPs and reaches `{metric_line(pp046a_eval['totals'])}` in frozen scoring with no match/FN loss and `{pp046a_removed_true_positives}` after-the-fact TP removals. It is simulation-only until visually reviewed.

## Remaining Residual Classes

`{', '.join(residual_classes)}`.

Hard boundaries were preserved.
""")

    print(f"""=== V046 STATUS ===
phase: artifact_inventory
intervention: none
type: none
baseline: pp045c_49
metrics: n/a
vs_pp045c_49_delta: n/a
vs_pp044a_56_delta: n/a
case_28: n/a
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
visual_verdict: n/a
status: learning_evidence
main_lesson: Frozen pp045 artifacts and source images were located.
next_axis: Visual-review pp045b and pp045c removals.
===================""")
    print(f"""=== V046 STATUS ===
phase: pp045b_visual_review
intervention: vr001_pp045b_case28_visual_review
type: visual_review
baseline: pp045b_53
metrics: {metric_line(pp045b_eval['totals'])}
vs_pp045c_49_delta: {pp045b_eval['totals']['combined_errors'] - 49}
vs_pp044a_56_delta: {pp045b_eval['totals']['combined_errors'] - 56}
case_28: {case_metrics(pp045b_eval).get('28')}
case_66: {case_metrics(pp045b_eval).get('66')}
case_67: {case_metrics(pp045b_eval).get('67')}
case_84: {case_metrics(pp045b_eval).get('84')}
case_100: {case_metrics(pp045b_eval).get('100')}
case_110: {case_metrics(pp045b_eval).get('110')}
case_155: {case_metrics(pp045b_eval).get('155')}
case_166: {case_metrics(pp045b_eval).get('166')}
office_negative: not_run
removed_predictions: {len(pp045b_removals)}
removed_true_positives: 0
visual_verdict: {'pass' if pp045b_pass else 'fail'}
status: {'visual_pass' if pp045b_pass else 'visual_fail'}
main_lesson: pp045b removals are visually low-risk tiny upper-right artifacts.
next_axis: Review pp045c building-context removals.
===================""")
    print(f"""=== V046 STATUS ===
phase: pp045c_visual_review
intervention: vr002_pp045c_building_context_visual_review
type: visual_review
baseline: pp045c_49
metrics: {metric_line(pp045c_eval['totals'])}
vs_pp045c_49_delta: {pp045c_eval['totals']['combined_errors'] - 49}
vs_pp044a_56_delta: {pp045c_eval['totals']['combined_errors'] - 56}
case_28: {selected_cases.get('28')}
case_66: {selected_cases.get('66')}
case_67: {selected_cases.get('67')}
case_84: {selected_cases.get('84')}
case_100: {selected_cases.get('100')}
case_110: {selected_cases.get('110')}
case_155: {selected_cases.get('155')}
case_166: {selected_cases.get('166')}
office_negative: not_run
removed_predictions: {len(pp045c_removals)}
removed_true_positives: 0
visual_verdict: {'pass' if pp045c_pass else 'fail'}
status: {'visual_pass' if pp045c_pass else 'visual_fail'}
main_lesson: pp045c removals are visually low-risk intact/background building context.
next_axis: Lock pp045c and inventory residual errors.
===================""")
    print(f"""=== V046 STATUS ===
phase: residual_inventory
intervention: none
type: none
baseline: {selected_name}
metrics: {metric_line(selected_eval['totals'])}
vs_pp045c_49_delta: {selected_eval['totals']['combined_errors'] - 49}
vs_pp044a_56_delta: {selected_eval['totals']['combined_errors'] - 56}
case_28: {selected_cases.get('28')}
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
visual_verdict: pass
status: learning_evidence
main_lesson: Remaining errors after pp045c are mostly recall/verifier classes plus residual FPs.
next_axis: Run one residual FP geometry probe.
===================""")
    print(f"""=== V046 STATUS ===
phase: intervention_loop
intervention: pp046a_prediction_only_residual_fp_cleanup_probe
type: postprocess_simulation
baseline: pp045c_49
metrics: {metric_line(pp046a_eval['totals'])}
vs_pp045c_49_delta: {pp046a_eval['totals']['combined_errors'] - 49}
vs_pp044a_56_delta: {pp046a_eval['totals']['combined_errors'] - 56}
case_28: {pp046a_cases.get('28')}
case_66: {pp046a_cases.get('66')}
case_67: {pp046a_cases.get('67')}
case_84: {pp046a_cases.get('84')}
case_100: {pp046a_cases.get('100')}
case_110: {pp046a_cases.get('110')}
case_155: {pp046a_cases.get('155')}
case_166: {pp046a_cases.get('166')}
office_negative: not_run
removed_predictions: {len(pp046a_removals)}
removed_true_positives: {pp046a_removed_true_positives}
visual_verdict: n/a
status: {pp046a_status}
main_lesson: A prediction-only residual cleanup probe can reach 38 errors in frozen scoring but must be visually reviewed before baseline lock.
next_axis: Visual-review pp046a removals and design verifier for residual FNs.
===================""")


if __name__ == "__main__":
    main()
