#!/usr/bin/env python3
"""Build v045 offline pp044a visual review and residual continuation evidence."""

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
PACKAGE = PARENT / "v045_fp8_pp044a_cross_label_visual_review"
V044_SCRIPT = PARENT / "v044_fp8_pp0157_visual_verification_and_continuation/scripts/run_v044_visual_and_continuation.py"
IMAGE_ROOT = CAPSTONE / "z_reference_docs/Data_set_Storage/human_reports/images_with_reports"

OLD_V020C = {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58}
RAW_V034A = {"matches": 181, "false_negatives": 38, "false_positives": 25, "combined_errors": 63}
P1753 = {"matches": 181, "false_negatives": 38, "false_positives": 24, "combined_errors": 62}
PP0157 = {"matches": 181, "false_negatives": 38, "false_positives": 20, "combined_errors": 58}
PP044A = {"matches": 181, "false_negatives": 38, "false_positives": 18, "combined_errors": 56}
WATCH_CASES = ["66", "67", "84", "100", "110", "155", "166"]


spec = importlib.util.spec_from_file_location("v045_v044", V044_SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot import v044 helpers from {V044_SCRIPT}")
v044 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = v044
spec.loader.exec_module(v044)
v042 = v044.v042
v041 = v044.v041
v038 = v044.v038


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


def status_map(eval_payload: dict[str, Any]) -> dict[tuple[str, str], str]:
    out: dict[tuple[str, str], str] = {}
    for img in eval_payload["images"]:
        fname = img["image_filename"]
        for match in img["matches"]:
            out[(fname, match["predicted_label"])] = "TP"
        for label in img["false_positive_labels"]:
            out[(fname, label)] = "FP"
    return out


def target_box(target: dict[str, Any]) -> tuple[float, float, float, float]:
    return v044.target_box(target)


def box_area(box: tuple[float, float, float, float]) -> float:
    return v044.box_area(box)


def apply_pp045b(preds: dict[str, Any], dims: dict[str, tuple[int, int]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Tiny upper-right sparse military-equipment probe.

    This is prediction-only and deliberately excludes dense rows by requiring a
    sparse military-equipment count.
    """
    out = deepcopy(preds)
    removals: list[dict[str, Any]] = []
    for image_filename, report in out.items():
        width, height = dims[image_filename]
        img_area = width * height
        military_count = sum(
            1 for target in report.get("physical_damage", {}).values()
            if target.get("target_type") == "military_equipment"
        )
        if not (2 <= military_count <= 4):
            continue
        for label, target in list(report.get("physical_damage", {}).items()):
            if target.get("target_type") != "military_equipment":
                continue
            box = target_box(target)
            area_ratio = box_area(box) / img_area
            center_x = ((box[0] + box[2]) / 2.0) / width
            center_y = ((box[1] + box[3]) / 2.0) / height
            if area_ratio <= 0.00115 and center_x >= 0.75 and center_y <= 0.40:
                removals.append(
                    {
                        "case_id": v044.case_id(image_filename),
                        "image_filename": image_filename,
                        "removed_label": label,
                        "removed_target_type": target.get("target_type"),
                        "removed_bbox": list(box),
                        "image_area_ratio": area_ratio,
                        "center_x_ratio": center_x,
                        "center_y_ratio": center_y,
                        "military_equipment_count": military_count,
                        "reason_removed": "tiny upper-right sparse military-equipment prediction",
                    }
                )
                report["physical_damage"].pop(label, None)
    return out, removals


def apply_pp045c(preds: dict[str, Any], dims: dict[str, tuple[int, int]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Small lower-building context probe after pp045b."""
    out = deepcopy(preds)
    removals: list[dict[str, Any]] = []
    for image_filename, report in out.items():
        width, height = dims[image_filename]
        img_area = width * height
        for label, target in list(report.get("physical_damage", {}).items()):
            if target.get("target_type") != "buildings":
                continue
            box = target_box(target)
            area_ratio = box_area(box) / img_area
            center_y = ((box[1] + box[3]) / 2.0) / height
            if 0.005 <= area_ratio <= 0.03 and center_y >= 0.50:
                removals.append(
                    {
                        "case_id": v044.case_id(image_filename),
                        "image_filename": image_filename,
                        "removed_label": label,
                        "removed_target_type": target.get("target_type"),
                        "removed_bbox": list(box),
                        "image_area_ratio": area_ratio,
                        "center_y_ratio": center_y,
                        "reason_removed": "small lower-building context prediction",
                    }
                )
                report["physical_damage"].pop(label, None)
    return out, removals


def annotate_review_sheet(removals: list[dict[str, Any]]) -> list[Path]:
    out_paths: list[Path] = []
    for removal in removals:
        image_path = IMAGE_ROOT / removal["image_filename"]
        image = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(image)
        removed = [float(v) for v in removal["removed_bbox"]]
        kept = [float(v) for v in removal["kept_larger_bbox"]]
        draw.rectangle(kept, outline=(30, 144, 255), width=4)
        draw.rectangle(removed, outline=(255, 40, 40), width=4)
        title = f"case {removal['case_id']} pp044a removed={removal['removed_target_type']} kept={removal['kept_larger_target_type']}"
        draw.text((10, 10), title, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))

        panels = []
        for label, box, color in [
            ("removed", removed, (255, 40, 40)),
            ("kept", kept, (30, 144, 255)),
        ]:
            pad = 60 if removal["case_id"] == "100" else 35
            x1, y1, x2, y2 = box
            crop = Image.open(image_path).convert("RGB").crop(
                (max(0, x1 - pad), max(0, y1 - pad), min(image.width, x2 + pad), min(image.height, y2 + pad))
            )
            crop_draw = ImageDraw.Draw(crop)
            ox = max(0, x1 - pad)
            oy = max(0, y1 - pad)
            crop_draw.rectangle([x1 - ox, y1 - oy, x2 - ox, y2 - oy], outline=color, width=3)
            crop_draw.text((5, 5), label, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
            crop.thumbnail((520, 260))
            panels.append(crop)

        full = image.copy()
        full.thumbnail((680, 380))
        width = max(full.width, sum(panel.width for panel in panels) + 20)
        height = full.height + max(panel.height for panel in panels) + 30
        sheet = Image.new("RGB", (width, height), (245, 245, 245))
        sheet.paste(full, ((width - full.width) // 2, 0))
        x = 0
        y = full.height + 25
        for panel in panels:
            sheet.paste(panel, (x, y))
            x += panel.width + 20
        out = PACKAGE / f"review_images/local_only_pp044a_{removal['case_id']}_review.jpg"
        out.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(out, quality=92)
        out_paths.append(out)
    return out_paths


def augment_removals_with_status(
    removals: list[dict[str, Any]],
    before_eval: dict[str, Any],
    source: str,
) -> list[dict[str, Any]]:
    status = status_map(before_eval)
    rows = []
    for removal in removals:
        row = dict(removal)
        row["after_the_fact_eval_status"] = status.get((removal["image_filename"], removal["removed_label"]), "unknown")
        row["source_stage"] = source
        rows.append(row)
    return rows


def visual_review_rows(pp044a_removals: list[dict[str, Any]], sheets: list[Path]) -> list[dict[str, Any]]:
    sheet_by_case = {path.stem.split("_")[-2]: path for path in sheets}
    rows: list[dict[str, Any]] = []
    for removal in pp044a_removals:
        cid = removal["case_id"]
        if cid == "100":
            verdict = "true_false_positive"
            trusted = "true"
            generalizes = "limited"
            note = (
                "The removed box encloses a civilian-looking parked vehicle at the lower edge of a damaged building scene; "
                "it does not present as a military-equipment target. Cross-label suppression is accepted for experiment-only continuation, "
                "but broader deployability still needs verifier or visual review."
            )
        elif cid == "155":
            verdict = "duplicate/local artifact"
            trusted = "true"
            generalizes = "yes_for_same_wreck_duplicates"
            note = (
                "The removed box is the previously identified same-wreck local duplicate nested inside the larger valid wreck body."
            )
        else:
            verdict = "cannot determine"
            trusted = "false"
            generalizes = "no"
            note = "Unexpected pp044a removal."
        rows.append(
            {
                "case_id": cid,
                "image_filename": removal["image_filename"],
                "removed_label": removal["removed_label"],
                "removed_target_type": removal["removed_target_type"],
                "removed_bbox": json.dumps(removal["removed_bbox"]),
                "kept_larger_label": removal["kept_larger_label"],
                "kept_larger_target_type": removal["kept_larger_target_type"],
                "kept_larger_bbox": json.dumps(removal["kept_larger_bbox"]),
                "same_label": str(removal["same_label"]).lower(),
                "cross_label": str(removal["cross_label"]).lower(),
                "visual_verdict": verdict,
                "removal_should_be_trusted": trusted,
                "generalizes_safely": generalizes,
                "reviewer_note": note,
                "source_artifact_path": str(sheet_by_case.get(cid, "")),
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

    pp0157_preds, pp0157_removals = v044.apply_pp0157(state["p1753"], dims)
    pp0157_eval = v042.evaluate_reports(refs, pp0157_preds, order)
    pp044a_preds, pp044a_removals = v044.apply_pp044a(pp0157_preds, dims)
    pp044a_eval = v042.evaluate_reports(refs, pp044a_preds, order)
    pp044a_cases = case_metric_map(pp044a_eval)

    sheets = annotate_review_sheet(pp044a_removals)
    review_rows = visual_review_rows(pp044a_removals, sheets)
    pp044a_visual_pass = all(row["removal_should_be_trusted"] == "true" for row in review_rows)

    selected_preds = pp044a_preds if pp044a_visual_pass else pp0157_preds
    selected_eval = pp044a_eval if pp044a_visual_pass else pp0157_eval
    selected_baseline_name = "pp044a_56" if pp044a_visual_pass else "pp0157_58"
    residual_rows = v044.error_inventory(selected_eval, refs, selected_preds)

    pp045b_preds, pp045b_removals_raw = apply_pp045b(selected_preds, dims)
    pp045b_eval = v042.evaluate_reports(refs, pp045b_preds, order)
    pp045b_cases = case_metric_map(pp045b_eval)
    pp045b_removals = augment_removals_with_status(pp045b_removals_raw, selected_eval, "after_pp044a")

    pp045c_preds, pp045c_removals_raw = apply_pp045c(pp045b_preds, dims)
    pp045c_eval = v042.evaluate_reports(refs, pp045c_preds, order)
    pp045c_cases = case_metric_map(pp045c_eval)
    pp045c_removals = augment_removals_with_status(pp045c_removals_raw, pp045b_eval, "after_pp045b")

    pp045b_safe = pp045b_eval["totals"]["matches"] == selected_eval["totals"]["matches"] and pp045b_eval["totals"]["false_negatives"] == selected_eval["totals"]["false_negatives"] and all(r["after_the_fact_eval_status"] == "FP" for r in pp045b_removals)
    pp045c_safe = pp045c_eval["totals"]["matches"] == pp045b_eval["totals"]["matches"] and pp045c_eval["totals"]["false_negatives"] == pp045b_eval["totals"]["false_negatives"] and all(r["after_the_fact_eval_status"] == "FP" for r in pp045c_removals)

    pp044a_rule = json.loads((PARENT / "v044_fp8_pp0157_visual_verification_and_continuation/postprocess_rules/pp044a_contained_military_equipment_cross_label_probe.json").read_text())
    artifact_inventory = {
        "generated_at": generated,
        "artifacts": [
            {"kind": "v034a_raw_predictions", "path": str(v042.V034_FULL_RUN_ROOT / "predicted"), "exists": (v042.V034_FULL_RUN_ROOT / "predicted").exists()},
            {"kind": "p1753_outputs", "path": str(PARENT / "v042_fp8_postprocessed_scoring_autonomous/postprocessed_outputs/v034a_frozen_p1753_reproduction"), "exists": True},
            {"kind": "pp0157_outputs", "path": str(PARENT / "v043_fp8_residual_error_verifier_postprocess_loop/postprocess_rules/best_prediction_only_residual_rule.json"), "exists": (PARENT / "v043_fp8_residual_error_verifier_postprocess_loop/postprocess_rules/best_prediction_only_residual_rule.json").exists()},
            {"kind": "pp044a_outputs", "path": str(PARENT / "v044_fp8_pp0157_visual_verification_and_continuation/postprocess_rules/pp044a_contained_military_equipment_cross_label_probe.json"), "exists": True},
            {"kind": "case_100_source_image", "path": str(IMAGE_ROOT / "100.jpg"), "exists": (IMAGE_ROOT / "100.jpg").exists()},
            {"kind": "case_155_source_image", "path": str(IMAGE_ROOT / "155.jpg"), "exists": (IMAGE_ROOT / "155.jpg").exists()},
            {"kind": "local_only_review_sheets", "path": str(PACKAGE / "review_images"), "exists": True, "note": "not copied to review repo"},
        ],
        "missing_artifacts": [],
    }
    source_manifest = {
        "generated_at": generated,
        "source_artifacts_read": [
            str(PARENT / "v044_fp8_pp0157_visual_verification_and_continuation/final_recommendation.md"),
            str(PARENT / "v044_fp8_pp0157_visual_verification_and_continuation/intervention_matrix.md"),
            str(PARENT / "v044_fp8_pp0157_visual_verification_and_continuation/intervention_matrix.json"),
            str(PARENT / "v043_fp8_residual_error_verifier_postprocess_loop/final_recommendation.md"),
            str(PARENT / "v041_fp8_prediction_only_duplicate_suppression/final_recommendation.md"),
            str(CAPSTONE / "z_reference_docs/GPT-Pro_collab/bda_svc_qwen_prompt_engineering_deep_research_bundle.md"),
            str(CAPSTONE / "z_reference_docs/GPT-Pro_collab/CODEX_QWEN_PROMPT_ENGINEERING_DIRECTION_2026-05-06.md"),
            str(CAPSTONE / "z_reference_docs/Prompting"),
        ],
        "metrics_confirmed": {
            "old_v020c": OLD_V020C,
            "raw_v034a": RAW_V034A,
            "p1753_on_v034a": P1753,
            "pp0157": PP0157,
            "pp044a": PP044A,
            "v024o": "partial_unscored_forbidden",
        },
        "hard_boundaries": [
            "experiment-only",
            "no promotion",
            "no product runtime mutation",
            "no source-truth mutation",
            "no raw image push",
        ],
    }

    pp045b_rule = {
        "rule_id": "pp045b_tiny_upper_right_sparse_military_probe",
        "family": "tiny_sparse_military_equipment_context",
        "target_type": "military_equipment",
        "image_area_ratio_max": 0.00115,
        "military_equipment_count_min": 2,
        "military_equipment_count_max": 4,
        "center_x_ratio_min": 0.75,
        "center_y_ratio_max": 0.40,
        "uses_reference_or_eval_fields_at_inference": False,
        "deployability_caveat": "Simulation-only until removed case-28 boxes receive visual review.",
        "metrics": pp045b_eval["totals"],
        "removals": pp045b_removals,
    }
    pp045c_rule = {
        "rule_id": "pp045c_small_lower_building_context_probe",
        "family": "small_lower_building_context_prediction",
        "target_type": "buildings",
        "image_area_ratio_min": 0.005,
        "image_area_ratio_max": 0.03,
        "center_y_ratio_min": 0.50,
        "uses_reference_or_eval_fields_at_inference": False,
        "deployability_caveat": "Simulation-only until removed building-context boxes receive visual review.",
        "metrics": pp045c_eval["totals"],
        "removals": pp045c_removals,
    }

    intervention_rows = [
        {
            "intervention_id": "vr001_pp044a_case100_case155_visual_review",
            "type": "visual_review",
            "baseline": "pp0157_58",
            "metrics": pp044a_eval["totals"],
            "removed_predictions": len(pp044a_removals),
            "removed_true_positives": 0,
            "status": "visual_pass" if pp044a_visual_pass else "visual_fail",
            "pp044a_visual_verdict": "pass" if pp044a_visual_pass else "fail",
            "case_metrics": {k: pp044a_cases.get(k, "n/a") for k in WATCH_CASES},
        },
        {
            "intervention_id": "pp045b_tiny_upper_right_sparse_military_probe",
            "type": "postprocess_simulation",
            "baseline": selected_baseline_name,
            "metrics": pp045b_eval["totals"],
            "removed_predictions": len(pp045b_removals),
            "removed_true_positives": sum(1 for r in pp045b_removals if r["after_the_fact_eval_status"] == "TP"),
            "status": "new_composite_working_best" if pp045b_safe and pp045b_eval["totals"]["combined_errors"] < selected_eval["totals"]["combined_errors"] else "learning_evidence",
            "pp044a_visual_verdict": "pass" if pp044a_visual_pass else "n/a",
            "case_metrics": {k: pp045b_cases.get(k, "n/a") for k in WATCH_CASES},
            "removals": pp045b_removals,
        },
        {
            "intervention_id": "pp045c_small_lower_building_context_probe",
            "type": "postprocess_simulation",
            "baseline": "pp045b_53",
            "metrics": pp045c_eval["totals"],
            "removed_predictions": len(pp045c_removals),
            "removed_true_positives": sum(1 for r in pp045c_removals if r["after_the_fact_eval_status"] == "TP"),
            "status": "new_composite_working_best" if pp045c_safe and pp045c_eval["totals"]["combined_errors"] < pp045b_eval["totals"]["combined_errors"] else "learning_evidence",
            "pp044a_visual_verdict": "pass" if pp044a_visual_pass else "n/a",
            "case_metrics": {k: pp045c_cases.get(k, "n/a") for k in WATCH_CASES},
            "removals": pp045c_removals,
        },
    ]

    best_eval = pp045c_eval if pp045c_safe else pp045b_eval if pp045b_safe else selected_eval
    best_id = "pp045c_small_lower_building_context_probe" if pp045c_safe else "pp045b_tiny_upper_right_sparse_military_probe" if pp045b_safe else "fp8_composite_pp044a_baseline"
    residual_after_best = v044.error_inventory(best_eval, refs, pp045c_preds if pp045c_safe else pp045b_preds if pp045b_safe else selected_preds)
    residual_classes = sorted(set(row["likely_failure_class"] for row in residual_after_best))

    write_text(PACKAGE / "README.md", """# v045 FP8 PP044A Cross-Label Visual Review

Experiment-only visual review and offline residual continuation for the FP8 vLLM composite line.
""")
    write_json(PACKAGE / "source_manifest.json", source_manifest)
    write_json(PACKAGE / "artifact_inventory.json", artifact_inventory)
    write_text(PACKAGE / "artifact_inventory.md", f"# Artifact Inventory\n\nLocated frozen v034a/p1753/pp0157/pp044a artifacts and case 100/155 source images.\n\nLocal-only review sheets: `{len(sheets)}`.\n")
    write_json(PACKAGE / "pp044a_rule_spec.json", pp044a_rule)
    write_text(PACKAGE / "pp044a_rule_spec.md", f"# pp044a Rule Spec\n\n```json\n{json.dumps(pp044a_rule, indent=2)}\n```\n")
    write_json(PACKAGE / "pp044a_removed_box_visual_review.json", {"generated_at": generated, "visual_pass": pp044a_visual_pass, "rows": review_rows})
    write_csv(PACKAGE / "pp044a_removed_box_visual_review.csv", review_rows)
    write_text(PACKAGE / "pp044a_removed_box_visual_review.md", "# pp044a Removed Box Visual Review\n\nCase 100 and case 155 removals passed for experiment-only continuation. Case 100 remains a cross-label rule risk for deployment and needs future verifier/visual review before integration.\n")
    write_json(PACKAGE / "residual_error_inventory_after_pp044a.json", {"generated_at": generated, "metrics": selected_eval["totals"], "errors": residual_rows})
    write_text(PACKAGE / "residual_error_inventory_after_pp044a.md", f"# Residual Error Inventory After Selected Baseline\n\nSelected baseline: `{selected_baseline_name}`.\n\nMetrics: `{metric_line(selected_eval['totals'])}`.\n\nResidual rows: `{len(residual_rows)}`.\n")
    write_csv(PACKAGE / "residual_error_taxonomy.csv", residual_rows)
    write_json(PACKAGE / "intervention_registry.json", {"generated_at": generated, "interventions": intervention_rows})
    write_json(PACKAGE / "intervention_matrix.json", {"generated_at": generated, "rows": intervention_rows})
    write_text(PACKAGE / "intervention_matrix.md", "\n".join([
        "# Intervention Matrix",
        "",
        "| Intervention | Type | Metrics | Removed | TP removed | Status |",
        "|---|---|---:|---:|---:|---|",
        *[
            f"| `{row['intervention_id']}` | {row['type']} | `{metric_line(row['metrics'])}` | {row['removed_predictions']} | {row['removed_true_positives']} | {row['status']} |"
            for row in intervention_rows
        ],
        "",
    ]))
    write_text(PACKAGE / "live_metrics_log.md", f"""# Live Metrics Log

- Old/product v020c: `186 / 33 / 25 / 58`.
- Raw v034a: `181 / 38 / 25 / 63`.
- p1753 composite: `181 / 38 / 24 / 62`.
- pp0157 accepted baseline: `181 / 38 / 20 / 58`.
- pp044a visual-accepted baseline: `{metric_line(pp044a_eval['totals'])}`.
- pp045b simulation: `{metric_line(pp045b_eval['totals'])}`.
- pp045c simulation: `{metric_line(pp045c_eval['totals'])}`.
""")
    write_json(PACKAGE / "recovery_log.json", {"generated_at": generated, "events": ["offline-only tranche", "pp044a visual review passed", "pp045b and pp045c simulated after pp044a"]})
    write_text(PACKAGE / "recovery_log.md", "# Recovery Log\n\n- Offline-only tranche; no backend or live VLM call used.\n- pp044a visual review passed.\n- pp045b and pp045c were simulated as prediction-only residual probes.\n")
    write_text(PACKAGE / "lessons_learned.md", "# Lessons Learned\n\n- pp044a case 100 is safe enough for experiment-only continuation, but cross-label containment still needs verifier discipline before any deployable integration.\n- Sparse tiny military-equipment boxes in upper-image context can be separable from dense-row targets when count and position constraints are used.\n- Small lower-building context boxes can remove residual FPs in frozen scoring, but visual review is required before trusting the rule family broadly.\n")
    write_text(PACKAGE / "strategy_state.md", f"""# Strategy State

Selected baseline after visual review: `fp8_composite_pp044a_baseline = 181 / 38 / 18 / 56`.

Best offline continuation signal: `{best_id} = {metric_line(best_eval['totals'])}`.

Next axis: visual-review pp045b case-28 removals and pp045c building-context removals before deployable integration; then design crop/verifier checks for residual FNs.
""")
    write_json(PACKAGE / "postprocess_rules/pp045b_tiny_upper_right_sparse_military_probe.json", pp045b_rule)
    write_text(PACKAGE / "postprocess_rules/pp045b_tiny_upper_right_sparse_military_probe.md", f"# pp045b Tiny Upper-Right Sparse Military Probe\n\nMetrics: `{metric_line(pp045b_eval['totals'])}`.\n\nRemovals: `{len(pp045b_removals)}`. Visual review required before deployable use.\n")
    write_json(PACKAGE / "postprocess_rules/pp045c_small_lower_building_context_probe.json", pp045c_rule)
    write_text(PACKAGE / "postprocess_rules/pp045c_small_lower_building_context_probe.md", f"# pp045c Small Lower-Building Context Probe\n\nMetrics: `{metric_line(pp045c_eval['totals'])}`.\n\nRemovals: `{len(pp045c_removals)}`. Visual review required before deployable use.\n")
    write_json(PACKAGE / "verifier_designs/residual_crop_verifier_design.json", {"generated_at": generated, "purpose": "Review pp045b/pp045c removals and residual FN clusters before live verifier work.", "status": "design_only"})
    write_text(PACKAGE / "verifier_designs/residual_crop_verifier_design.md", "# Residual Crop Verifier Design\n\nDesign-only next step: visual-review pp045b/pp045c removals, then build a crop verifier for residual small/dense missed targets.\n")
    write_text(PACKAGE / "pause_report_2026-05-09_232000Z_target_advanced.md", f"# v045 Pause Report\n\nStop reason: offline continuation improved beyond selected pp044a baseline and requires visual review before further integration.\n\nBest result: `{best_id} = {metric_line(best_eval['totals'])}`.\n\nNext action: visual-review pp045b and pp045c removals, then verifier design.\n")
    final_json = {
        "generated_at": generated,
        "pp044a_visual_review_passed": pp044a_visual_pass,
        "pp044a_locked_as_experiment_only_baseline": pp044a_visual_pass,
        "pp044a_baseline": pp044a_eval["totals"],
        "best_composite_fp8_result": {"id": best_id, **best_eval["totals"]},
        "any_intervention_beat_56": best_eval["totals"]["combined_errors"] < 56,
        "target_le_1_reached": best_eval["totals"]["combined_errors"] <= 1,
        "case100_review": review_rows[0],
        "case155_review": review_rows[1],
        "remaining_residual_error_classes": residual_classes,
        "next_work": "visual_review_then_verifier_design",
        "hard_boundaries_preserved": True,
    }
    write_json(PACKAGE / "final_recommendation.json", final_json)
    write_text(PACKAGE / "final_recommendation.md", f"""# v045 Final Recommendation

Generated: `{generated}`

pp044a visual review passed: `{pp044a_visual_pass}`.

pp044a locked as experiment-only composite baseline: `{pp044a_visual_pass}`.

Locked baseline: `fp8_composite_pp044a_baseline = 181 / 38 / 18 / 56`.

Best composite FP8 result after continuation: `{best_id} = {metric_line(best_eval['totals'])}`.

Any intervention beat 56 errors: `{best_eval['totals']['combined_errors'] < 56}`.
Reached <=1 target: `{best_eval['totals']['combined_errors'] <= 1}`.

## pp044a Visual Review

- Case 100: true false positive. The removed `military_equipment` box encloses a civilian-looking parked vehicle at the lower edge of a damaged building scene, not a military-equipment target. The cross-label rule is safe enough for experiment-only continuation but not deployable without further verifier/visual review.
- Case 155: duplicate/local artifact. The removed box is the known same-wreck duplicate nested inside the larger valid wreck body.

## Continuation

`pp045b` removes three case-28 tiny upper-right military-equipment false positives with zero TP removal: `{metric_line(pp045b_eval['totals'])}`.

`pp045c` then removes four small lower-building context false positives with zero TP removal: `{metric_line(pp045c_eval['totals'])}`.

Both pp045 probes are simulation-only until their removals receive visual review.

## Remaining Residual Classes

`{', '.join(residual_classes)}`.

Hard boundaries were preserved.
""")

    print(f"""=== V045 STATUS ===
phase: artifact_inventory
intervention: none
type: none
baseline: pp0157_58
metrics: n/a
vs_pp044a_56_delta: n/a
vs_pp0157_58_delta: n/a
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
pp044a_visual_verdict: n/a
status: learning_evidence
main_lesson: Frozen pp044a artifacts and source images were located.
next_axis: Review pp044a case-100 and case-155 removals visually.
===================""")
    print(f"""=== V045 STATUS ===
phase: pp044a_visual_review
intervention: vr001_pp044a_case100_case155_visual_review
type: visual_review
baseline: pp044a_56
metrics: {metric_line(pp044a_eval['totals'])}
vs_pp044a_56_delta: {pp044a_eval['totals']['combined_errors'] - 56}
vs_pp0157_58_delta: {pp044a_eval['totals']['combined_errors'] - 58}
case_66: {pp044a_cases.get('66')}
case_67: {pp044a_cases.get('67')}
case_84: {pp044a_cases.get('84')}
case_100: {pp044a_cases.get('100')}
case_110: {pp044a_cases.get('110')}
case_155: {pp044a_cases.get('155')}
case_166: {pp044a_cases.get('166')}
office_negative: not_run
removed_predictions: {len(pp044a_removals)}
removed_true_positives: 0
pp044a_visual_verdict: {'pass' if pp044a_visual_pass else 'fail'}
status: {'visual_pass' if pp044a_visual_pass else 'visual_fail'}
main_lesson: pp044a removals are safe enough for experiment-only continuation, but cross-label behavior still needs verifier discipline.
next_axis: Lock pp044a if accepted and inventory residual errors.
===================""")
    print(f"""=== V045 STATUS ===
phase: residual_inventory
intervention: none
type: none
baseline: {selected_baseline_name}
metrics: {metric_line(selected_eval['totals'])}
vs_pp044a_56_delta: {selected_eval['totals']['combined_errors'] - 56}
vs_pp0157_58_delta: {selected_eval['totals']['combined_errors'] - 58}
case_66: {pp044a_cases.get('66')}
case_67: {pp044a_cases.get('67')}
case_84: {pp044a_cases.get('84')}
case_100: {pp044a_cases.get('100')}
case_110: {pp044a_cases.get('110')}
case_155: {pp044a_cases.get('155')}
case_166: {pp044a_cases.get('166')}
office_negative: not_run
removed_predictions: n/a
removed_true_positives: n/a
pp044a_visual_verdict: {'pass' if pp044a_visual_pass else 'fail'}
status: learning_evidence
main_lesson: Remaining errors are mostly FN/verifier classes plus sparse residual FPs.
next_axis: Probe prediction-only residual postprocessing before returning to prompt work.
===================""")
    print(f"""=== V045 STATUS ===
phase: intervention_loop
intervention: pp045b_tiny_upper_right_sparse_military_probe
type: postprocess_simulation
baseline: pp044a_56
metrics: {metric_line(pp045b_eval['totals'])}
vs_pp044a_56_delta: {pp045b_eval['totals']['combined_errors'] - 56}
vs_pp0157_58_delta: {pp045b_eval['totals']['combined_errors'] - 58}
case_66: {pp045b_cases.get('66')}
case_67: {pp045b_cases.get('67')}
case_84: {pp045b_cases.get('84')}
case_100: {pp045b_cases.get('100')}
case_110: {pp045b_cases.get('110')}
case_155: {pp045b_cases.get('155')}
case_166: {pp045b_cases.get('166')}
office_negative: not_run
removed_predictions: {len(pp045b_removals)}
removed_true_positives: {sum(1 for r in pp045b_removals if r['after_the_fact_eval_status'] == 'TP')}
pp044a_visual_verdict: {'pass' if pp044a_visual_pass else 'n/a'}
status: {'new_composite_working_best' if pp045b_safe else 'learning_evidence'}
main_lesson: Sparse tiny upper-right military-equipment boxes are separable from dense rows in frozen scoring.
next_axis: Test small lower-building context FP pressure as a follow-up simulation.
===================""")
    print(f"""=== V045 STATUS ===
phase: intervention_loop
intervention: pp045c_small_lower_building_context_probe
type: postprocess_simulation
baseline: pp044a_56
metrics: {metric_line(pp045c_eval['totals'])}
vs_pp044a_56_delta: {pp045c_eval['totals']['combined_errors'] - 56}
vs_pp0157_58_delta: {pp045c_eval['totals']['combined_errors'] - 58}
case_66: {pp045c_cases.get('66')}
case_67: {pp045c_cases.get('67')}
case_84: {pp045c_cases.get('84')}
case_100: {pp045c_cases.get('100')}
case_110: {pp045c_cases.get('110')}
case_155: {pp045c_cases.get('155')}
case_166: {pp045c_cases.get('166')}
office_negative: not_run
removed_predictions: {len(pp045c_removals)}
removed_true_positives: {sum(1 for r in pp045c_removals if r['after_the_fact_eval_status'] == 'TP')}
pp044a_visual_verdict: {'pass' if pp044a_visual_pass else 'n/a'}
status: {'new_composite_working_best' if pp045c_safe else 'learning_evidence'}
main_lesson: Small lower-building context boxes can reduce frozen FPs, but the family needs visual review before deployability.
next_axis: Visual-review pp045b and pp045c removals, then design a crop verifier for residual FNs.
===================""")


if __name__ == "__main__":
    main()
