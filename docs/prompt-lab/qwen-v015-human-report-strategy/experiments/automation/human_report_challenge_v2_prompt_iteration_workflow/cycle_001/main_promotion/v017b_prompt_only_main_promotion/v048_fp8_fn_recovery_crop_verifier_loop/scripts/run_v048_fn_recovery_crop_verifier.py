#!/usr/bin/env python3
"""Build v048 FN recovery crop/verifier evidence.

This is experiment-only evidence generation. It reconstructs frozen v034a-based
postprocessed outputs through the locked pp045c baseline, inventories the 38
remaining false negatives, generates local-only crop/contact-sheet aids, and
writes a verifier/tiling strategy. It does not call a VLM or mutate product
runtime/config/eval truth.
"""

from __future__ import annotations

import csv
import datetime as dt
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw


WORKTREE = Path("/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement")
CAPSTONE = Path("/home/williambenitez1/Capstone")
PARENT = WORKTREE / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion"
PACKAGE = PARENT / "v048_fp8_fn_recovery_crop_verifier_loop"
V047_SCRIPT = PARENT / "v047_fp8_pp046a_visual_verification_and_fn_recovery/scripts/run_v047_pp046a_visual_fn_recovery.py"
IMAGE_ROOT = CAPSTONE / "z_reference_docs/Data_set_Storage/human_reports/images_with_reports"

OLD_V020C = {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58}
PP045C = {"matches": 181, "false_negatives": 38, "false_positives": 11, "combined_errors": 49}
PP046A_DIAGNOSTIC = {"matches": 181, "false_negatives": 38, "false_positives": 0, "combined_errors": 38}
WATCH_CASES = ["66", "67", "84", "100", "110", "155", "166"]

spec = importlib.util.spec_from_file_location("v048_v047", V047_SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot import v047 helpers from {V047_SCRIPT}")
v047 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = v047
spec.loader.exec_module(v047)
v046 = v047.v046
v045 = v047.v045
v044 = v047.v044
v042 = v047.v042


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
        fields = sorted({key for row in rows for key in row}) if rows else []
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


def box_area(box: list[float] | tuple[float, float, float, float]) -> float:
    x1, y1, x2, y2 = [float(v) for v in box]
    return max(0.0, x2 - x1) * max(0.0, y2 - y1)


def center(box: list[float] | tuple[float, float, float, float]) -> tuple[float, float]:
    x1, y1, x2, y2 = [float(v) for v in box]
    return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)


def iou(a: list[float], b: list[float]) -> float:
    ax1, ay1, ax2, ay2 = [float(v) for v in a]
    bx1, by1, bx2, by2 = [float(v) for v in b]
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
    union = box_area(a) + box_area(b) - inter
    return inter / union if union else 0.0


def center_distance(a: list[float], b: list[float], dims: tuple[int, int]) -> float:
    ax, ay = center(a)
    bx, by = center(b)
    diag = math.hypot(float(dims[0]), float(dims[1]))
    return math.hypot(ax - bx, ay - by) / diag if diag else 0.0


def reference_position(box: list[float], dims: tuple[int, int]) -> str:
    x, y = center(box)
    width, height = dims
    horiz = "left" if x < width / 3 else "right" if x > (2 * width / 3) else "center"
    vert = "upper" if y < height / 3 else "lower" if y > (2 * height / 3) else "middle"
    return f"{vert}_{horiz}"


def is_edge_target(box: list[float], dims: tuple[int, int]) -> bool:
    x1, y1, x2, y2 = [float(v) for v in box]
    width, height = dims
    return x1 <= 0.05 * width or y1 <= 0.05 * height or x2 >= 0.95 * width or y2 >= 0.95 * height


def nearest_prediction(ref_box: list[float], preds: dict[str, Any], image_filename: str, dims: tuple[int, int]) -> dict[str, Any]:
    best: dict[str, Any] | None = None
    for label, target in preds.get(image_filename, {}).get("physical_damage", {}).items():
        pred_box = list(v044.target_box(target))
        pred_iou = iou(ref_box, pred_box)
        dist = center_distance(ref_box, pred_box, dims)
        score = (pred_iou, -dist)
        if best is None or score > best["score"]:
            best = {
                "score": score,
                "label": label,
                "target_type": target.get("target_type", "unknown"),
                "bbox": pred_box,
                "iou": pred_iou,
                "center_distance": dist,
            }
    if best is None:
        return {
            "label": "",
            "target_type": "",
            "bbox": [],
            "iou": 0.0,
            "center_distance": "",
        }
    best.pop("score", None)
    return best


def classify_fn(case_id: str, target_type: str, ref_box: list[float], dims: tuple[int, int], nearest: dict[str, Any]) -> tuple[str, list[str]]:
    area_ratio = box_area(ref_box) / float(dims[0] * dims[1])
    tags: list[str] = []
    if case_id in {"67", "84"}:
        tags.append("dense_valid_target_missed")
    if case_id == "110":
        tags.append("smoke_or_debris_obscured")
    if target_type == "buildings":
        tags.append("building_or_structure_piece")
    if area_ratio <= 0.006:
        tags.append("small_valid_target_missed")
    if is_edge_target(ref_box, dims):
        tags.append("edge_or_boundary_target")
    if nearest.get("iou", 0.0) > 0.0 or (isinstance(nearest.get("center_distance"), float) and nearest["center_distance"] < 0.12):
        tags.append("adjacent_target_confusion")
    if not tags:
        tags.append("unknown")
    priority = [
        "dense_valid_target_missed",
        "smoke_or_debris_obscured",
        "small_valid_target_missed",
        "building_or_structure_piece",
        "adjacent_target_confusion",
        "edge_or_boundary_target",
        "unknown",
    ]
    primary = next((tag for tag in priority if tag in tags), "unknown")
    return primary, tags


def likely_recovery(primary_class: str, tags: list[str], target_type: str) -> tuple[str, str]:
    if primary_class in {"dense_valid_target_missed", "small_valid_target_missed", "smoke_or_debris_obscured"}:
        return "B", "crop/tiling pass can increase local resolution without globally relaxing the prompt"
    if primary_class == "building_or_structure_piece":
        return "C", "crop-level verifier can separate reference building pieces from ambiguous structure context"
    if "adjacent_target_confusion" in tags:
        return "C", "crop-level verifier can compare the missed reference against nearby predictions"
    if target_type == "military_equipment":
        return "B", "tiling/crop pass is safer than broad recall wording for equipment misses"
    return "D", "needs visual review or FiftyOne-style adjudication before any recovery mechanism"


def build_fn_inventory(eval_payload: dict[str, Any], refs: dict[str, Any], preds: dict[str, Any], dims: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for image in eval_payload["images"]:
        image_filename = image["image_filename"]
        case_id = v044.case_id(image_filename)
        ref_report = refs[image_filename]
        for label in image["false_negative_labels"]:
            target = ref_report.get("physical_damage", {}).get(label, {})
            target_type = target.get("target_type", "unknown")
            ref_box = list(v044.target_box(target)) if target else []
            nearest = nearest_prediction(ref_box, preds, image_filename, dims[image_filename]) if ref_box else {}
            area = box_area(ref_box) if ref_box else 0.0
            area_ratio = area / float(dims[image_filename][0] * dims[image_filename][1])
            primary_class, tags = classify_fn(case_id, target_type, ref_box, dims[image_filename], nearest)
            recovery_code, recovery_reason = likely_recovery(primary_class, tags, target_type)
            rows.append(
                {
                    "case_id": case_id,
                    "image_filename": image_filename,
                    "reference_label": label,
                    "target_type": target_type,
                    "reference_bbox": json.dumps(ref_box),
                    "reference_area": round(area, 2),
                    "reference_area_ratio": round(area_ratio, 6),
                    "reference_position": reference_position(ref_box, dims[image_filename]) if ref_box else "",
                    "nearest_predicted_label": nearest.get("label", ""),
                    "nearest_prediction_target_type": nearest.get("target_type", ""),
                    "nearest_prediction_bbox": json.dumps(nearest.get("bbox", [])),
                    "iou_with_nearest_prediction": round(float(nearest.get("iou", 0.0) or 0.0), 6),
                    "distance_to_nearest_prediction_center": round(float(nearest.get("center_distance", 0.0) or 0.0), 6) if nearest.get("center_distance") != "" else "",
                    "primary_failure_class": primary_class,
                    "taxonomy_tags": ";".join(tags),
                    "likely_recoverable_by": recovery_code,
                    "recovery_reason": recovery_reason,
                    "risk_to_dense_cases": str(case_id in {"66", "67", "84", "97"}).lower(),
                    "risk_to_case_110": str(case_id == "110").lower(),
                    "risk_to_controls_155_166_office": str(case_id in {"155", "166"}).lower(),
                    "reviewer_note": "Initial geometry inventory; crop review should decide whether this is visually obvious, ambiguous, or verifier-needed.",
                }
            )
    return rows


def crop_bounds(box: list[float], dims: tuple[int, int]) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = [float(v) for v in box]
    width, height = dims
    pad = max(80.0, 0.75 * max(x2 - x1, y2 - y1))
    return (
        int(max(0, x1 - pad)),
        int(max(0, y1 - pad)),
        int(min(width, x2 + pad)),
        int(min(height, y2 + pad)),
    )


def draw_box(draw: ImageDraw.ImageDraw, box: list[float], offset: tuple[int, int], color: tuple[int, int, int], label: str, width: int = 4) -> None:
    ox, oy = offset
    shifted = [box[0] - ox, box[1] - oy, box[2] - ox, box[3] - oy]
    draw.rectangle(shifted, outline=color, width=width)
    draw.text((shifted[0] + 2, max(0, shifted[1] - 18)), label, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))


def create_crops_and_sheets(fn_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    crop_rows: list[dict[str, Any]] = []
    by_class: dict[str, list[Path]] = {}
    for row in fn_rows:
        image_path = IMAGE_ROOT / row["image_filename"]
        if not image_path.exists():
            crop_rows.append({**row, "crop_path": "", "contact_sheet_path": "", "crop_status": "missing_source_image"})
            continue
        image = Image.open(image_path).convert("RGB")
        ref_box = json.loads(row["reference_bbox"])
        bounds = crop_bounds(ref_box, (image.width, image.height))
        crop = image.crop(bounds)
        draw = ImageDraw.Draw(crop)
        draw_box(draw, ref_box, (bounds[0], bounds[1]), (30, 220, 80), "FN ref")
        nearest_box = json.loads(row["nearest_prediction_bbox"])
        if nearest_box:
            nx1, ny1, nx2, ny2 = nearest_box
            intersects = not (nx2 < bounds[0] or nx1 > bounds[2] or ny2 < bounds[1] or ny1 > bounds[3])
            if intersects:
                draw_box(draw, nearest_box, (bounds[0], bounds[1]), (255, 140, 0), "nearest pred", width=3)
        draw.text((6, 6), f"case {row['case_id']} {row['reference_label']} {row['target_type']}", fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
        crop.thumbnail((520, 360))
        crop_dir = PACKAGE / "review_images/local_only_fn_crops"
        crop_dir.mkdir(parents=True, exist_ok=True)
        safe_label = f"case_{row['case_id']}_{row['reference_label']}_{row['target_type']}".replace("/", "_")
        crop_path = crop_dir / f"local_only_fn_{safe_label}.jpg"
        crop.save(crop_path, quality=92)
        by_class.setdefault(row["primary_failure_class"], []).append(crop_path)
        crop_rows.append(
            {
                "case_id": row["case_id"],
                "image_filename": row["image_filename"],
                "reference_label": row["reference_label"],
                "target_type": row["target_type"],
                "primary_failure_class": row["primary_failure_class"],
                "reference_bbox": row["reference_bbox"],
                "crop_path": str(crop_path),
                "contact_sheet_path": "",
                "crop_status": "generated_local_only",
            }
        )

    sheet_paths: dict[str, str] = {}
    for cls, paths in sorted(by_class.items()):
        thumbs: list[tuple[str, Image.Image]] = []
        for path in paths:
            thumb = Image.open(path).convert("RGB")
            thumb.thumbnail((300, 210))
            thumbs.append((path.stem.replace("local_only_fn_", ""), thumb))
        cols = 3
        cell_w, cell_h = 320, 250
        rows_n = max(1, math.ceil(len(thumbs) / cols))
        sheet = Image.new("RGB", (cols * cell_w, 50 + rows_n * cell_h), (245, 245, 245))
        draw = ImageDraw.Draw(sheet)
        draw.text((12, 12), f"local-only FN contact sheet: {cls} ({len(thumbs)})", fill=(0, 0, 0))
        for idx, (label, thumb) in enumerate(thumbs):
            x = (idx % cols) * cell_w + 10
            y = 50 + (idx // cols) * cell_h
            sheet.paste(thumb, (x, y))
            draw.text((x, y + thumb.height + 4), label[:42], fill=(0, 0, 0))
        sheet_path = PACKAGE / f"review_images/local_only_fn_class_{cls}.jpg"
        sheet.save(sheet_path, quality=92)
        sheet_paths[cls] = str(sheet_path)

    for row in crop_rows:
        row["contact_sheet_path"] = sheet_paths.get(row["primary_failure_class"], "")
    return crop_rows, sheet_paths


def crop_review_rows(fn_rows: list[dict[str, Any]], crop_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    crop_by_key = {
        (row["case_id"], row["reference_label"]): row
        for row in crop_rows
    }
    reviews: list[dict[str, Any]] = []
    for row in fn_rows:
        crop = crop_by_key[(row["case_id"], row["reference_label"])]
        primary = row["primary_failure_class"]
        if primary == "dense_valid_target_missed":
            visual_class = "dense-row valid target"
            intervention = "B"
            note = "Dense-row FN; crop or tile pass is safer than global prompt recall because prior wording collapsed dense precision."
        elif primary == "smoke_or_debris_obscured":
            visual_class = "smoke/debris-obscured target"
            intervention = "B"
            note = "Obscured convoy/vehicle FN; local crop pass can increase scrutiny without changing full-scene FP gates."
        elif primary == "small_valid_target_missed":
            visual_class = "tiny but real target"
            intervention = "B"
            note = "Small FN; tiling/crop pass should be tested before prompt wording."
        elif primary == "building_or_structure_piece":
            visual_class = "building/structure ambiguity"
            intervention = "C"
            note = "Building-piece FN; use crop verifier and manual review before adding boxes."
        elif primary == "adjacent_target_confusion":
            visual_class = "possible target but ambiguous"
            intervention = "C"
            note = "Near an existing prediction; crop verifier should decide whether a separate box is justified."
        else:
            visual_class = "verifier_needed"
            intervention = "C"
            note = "Unclear from geometry alone; needs crop review/verifier dataset."
        reviews.append(
            {
                "case_id": row["case_id"],
                "image_filename": row["image_filename"],
                "reference_label": row["reference_label"],
                "target_type": row["target_type"],
                "primary_failure_class": primary,
                "visual_review_class": visual_class,
                "recommended_intervention": intervention,
                "prompt_addressable": "false",
                "crop_or_tiling_addressable": str(intervention == "B").lower(),
                "verifier_needed": str(intervention in {"C", "D"} or primary == "building_or_structure_piece").lower(),
                "reviewer_note": note,
                "crop_path": crop["crop_path"],
                "contact_sheet_path": crop["contact_sheet_path"],
            }
        )
    return reviews


def class_counts(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row[key]] = counts.get(row[key], 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = ["|" + "|".join(fields) + "|", "|" + "|".join(["---"] * len(fields)) + "|"]
    for row in rows:
        lines.append("|" + "|".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + "|")
    return "\n".join(lines)


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
    case_metrics = case_metric_map(pp045c_eval)
    fn_rows = build_fn_inventory(pp045c_eval, refs, pp045c_preds, dims)
    crop_rows, sheet_paths = create_crops_and_sheets(fn_rows)
    review_rows = crop_review_rows(fn_rows, crop_rows)
    fn_class_counts = class_counts(fn_rows, "primary_failure_class")
    review_counts = class_counts(review_rows, "visual_review_class")
    intervention_counts = class_counts(review_rows, "recommended_intervention")
    source_images_found = sum(1 for row in crop_rows if row["crop_status"] == "generated_local_only")

    if pp045c_eval["totals"]["combined_errors"] != 49 or pp045c_eval["totals"]["false_negatives"] != 38:
        raise RuntimeError(f"pp045c reproduction failed: {pp045c_eval['totals']}")
    if pp046a_eval["totals"]["combined_errors"] != 38:
        raise RuntimeError(f"pp046a diagnostic reproduction failed: {pp046a_eval['totals']}")
    if len(fn_rows) != 38:
        raise RuntimeError(f"Expected 38 FNs, found {len(fn_rows)}")

    source_manifest = {
        "generated_at": generated,
        "package": str(PACKAGE),
        "source_artifacts_read": [
            str(PARENT / "v047_fp8_pp046a_visual_verification_and_fn_recovery/final_recommendation.md"),
            str(PARENT / "v047_fp8_pp046a_visual_verification_and_fn_recovery/intervention_matrix.md"),
            str(PARENT / "v046_fp8_pp045_visual_verification_and_continuation/final_recommendation.md"),
            str(PARENT / "v045_fp8_pp044a_cross_label_visual_review/final_recommendation.md"),
            str(CAPSTONE / "z_reference_docs/GPT-Pro_collab/bda_svc_qwen_prompt_engineering_deep_research_bundle.md"),
            str(CAPSTONE / "z_reference_docs/GPT-Pro_collab/CODEX_QWEN_PROMPT_ENGINEERING_DIRECTION_2026-05-06.md"),
            str(CAPSTONE / "z_reference_docs/Prompting"),
        ],
        "metrics_confirmed": {
            "old_v020c": OLD_V020C,
            "locked_pp045c": pp045c_eval["totals"],
            "diagnostic_pp046a": pp046a_eval["totals"],
            "v024o": "partial_unscored_forbidden",
        },
        "hard_boundaries": [
            "experiment-only",
            "no promotion",
            "no product runtime mutation",
            "no source-truth mutation",
            "no eval-ground-truth mutation",
            "no live VLM calls",
            "local-only crop/contact-sheet images",
        ],
    }
    artifact_inventory = {
        "generated_at": generated,
        "case_101_excluded": "101.jpg" not in order and "101.png" not in order,
        "image_count_preserved": pp045c_eval["totals"].get("image_count"),
        "source_image_root": str(IMAGE_ROOT),
        "source_images_found_for_fns": source_images_found,
        "fn_count": len(fn_rows),
        "artifacts": [
            {"kind": "pp045c_locked_outputs", "path": "reconstructed from v034a+p1753+pp0157+pp044a+pp045b+pp045c helpers", "exists": True, "count": len(pp045c_preds)},
            {"kind": "v034a_raw_predictions", "path": str(v042.V034_FULL_RUN_ROOT / "predicted"), "exists": (v042.V034_FULL_RUN_ROOT / "predicted").exists()},
            {"kind": "eval_summaries", "path": "in-memory bda_eval emulation via v042.evaluate_reports", "exists": True},
            {"kind": "reference_annotations", "path": "loaded through v044.load_state()", "exists": True, "count": len(refs)},
            {"kind": "fn_local_only_crops", "path": str(PACKAGE / "review_images/local_only_fn_crops"), "exists": True, "count": source_images_found},
            {"kind": "fn_local_only_contact_sheets", "path": str(PACKAGE / "review_images"), "exists": True, "count": len(sheet_paths)},
        ],
        "missing_artifacts": [] if source_images_found == len(fn_rows) else ["some source images missing for FN crop generation"],
        "review_repo_publish_note": "Do not push raw images or local-only crop/contact-sheet JPG files.",
    }
    fn_recovery_strategy = {
        "generated_at": generated,
        "baseline": {"id": "fp8_composite_pp045c_baseline", **pp045c_eval["totals"]},
        "diagnostic_pp046a_not_locked": {"id": "pp046a", **pp046a_eval["totals"], "reason": "visual review failed/mixed in v047"},
        "fn_count": len(fn_rows),
        "dominant_classes": fn_class_counts,
        "recommendation": "Build an experiment-only crop/tiling verifier tranche before any prompt candidate.",
        "prompt_candidate_authorized": False,
        "why_no_prompt_candidate": "No low-risk prompt-addressable cluster was identified; dominant classes require local resolution or visual verification, and broad recall cues previously harmed dense cases.",
    }
    verifier_design = {
        "generated_at": generated,
        "objective": "Recover FNs without reintroducing FPs by using local crop evidence and strict merge gates.",
        "inference_inputs_allowed": [
            "full-image predictions",
            "image tiles or reference-free proposed crop windows",
            "crop-level VLM/detector outputs",
            "prediction geometry",
            "target_type labels",
        ],
        "inference_inputs_forbidden": [
            "reference boxes",
            "eval matched/unmatched state",
            "case ID special casing",
            "ground truth IoU",
        ],
        "verifier_json_schema": {
            "object_found": "boolean",
            "target_type": "buildings|military_equipment",
            "bbox_in_crop": "[x1,y1,x2,y2]",
            "confidence_rationale": "short string",
            "reject_reason": "short string or empty",
            "merge_candidate": "boolean",
        },
        "merge_gates": [
            "candidate must be generated from a fixed tile/crop policy, not reference-centered inference in deployment",
            "candidate target_type must be supported by visible damage/equipment evidence in crop",
            "candidate must not be mostly contained by an existing accepted prediction unless verifier says separate target",
            "candidate should be rejected if it is only smoke, road, intact structure, shadow, debris, or context",
            "full all-current scoring must show no FP increase and no dense/control regression",
        ],
        "micro_pack": [12, 14, 16, 42, 66, 67, 77, 84, 88, 90, 97, 100, 103, 110, 155, 166, 172],
        "stop_modes": [
            "any verifier-added FP on dense/control cases",
            "case 66/67/84/110 degradation",
            "office-negative false positive",
            "JSON instability",
            "verifier requires reference boxes at inference time",
        ],
    }
    tiling_strategy = {
        "generated_at": generated,
        "recommended": True,
        "why": "The residual FNs are largely small, dense, obscured, or structure-piece targets where local resolution and crop adjudication are safer than broad prompt recall.",
        "tile_policy": {
            "experiment_only_start": "2x2 overlapping tiles plus center crop",
            "overlap": 0.2,
            "crop_padding": "include enough context to distinguish separate targets from fragments",
            "merge": "map crop boxes back to image coordinates and pass through existing pp045c-safe postprocessing plus verifier gates",
        },
        "class_targets": {
            "dense_valid_target_missed": "tiling plus same-type verifier",
            "small_valid_target_missed": "tiling/crop pass",
            "smoke_or_debris_obscured": "crop verifier only, with conservative reject rules",
            "building_or_structure_piece": "manual visual review and verifier design, not automatic add",
            "unknown": "FiftyOne or contact-sheet review before live model work",
        },
    }
    optional_prompt_decision = {
        "generated_at": generated,
        "prompt_candidate_authored": False,
        "prompt_candidate_run": False,
        "decision": "do_not_author_prompt",
        "reason": "Crop review points to verifier/tiling as the lower-risk lever; no narrow prompt-addressable cluster was isolated.",
        "conditions_to_author_future_prompt": [
            "one FN cluster is visually obvious and prompt-addressable",
            "micro-pack protects 66/67/84/110/155/166 and office-negative",
            "wording does not broaden recall globally",
            "v034a extra-box discipline remains intact",
        ],
    }
    interventions = [
        {
            "intervention_id": "fn001_pp045c_residual_fn_inventory",
            "type": "fn_inventory",
            "stage": "offline_only",
            "baseline": "pp045c_49",
            "metrics": pp045c_eval["totals"],
            "fn_count": len(fn_rows),
            "status": "inventory_complete",
            "class_counts": fn_class_counts,
        },
        {
            "intervention_id": "crop001_reference_centered_local_only_aids",
            "type": "crop_review",
            "stage": "offline_only",
            "baseline": "pp045c_49",
            "metrics": pp045c_eval["totals"],
            "fn_count": len(fn_rows),
            "status": "crop_review_complete",
            "generated_crops": source_images_found,
            "contact_sheets": sheet_paths,
            "review_counts": review_counts,
        },
        {
            "intervention_id": "ver001_crop_verifier_tiling_plan",
            "type": "verifier_design",
            "stage": "offline_only",
            "baseline": "pp045c_49",
            "metrics": pp045c_eval["totals"],
            "status": "verifier_plan_complete",
            "prompt_candidate_authored": False,
        },
    ]
    final = {
        "generated_at": generated,
        "all_38_fns_inventoried": True,
        "dominant_fn_classes": fn_class_counts,
        "local_crops_generated": source_images_found,
        "local_contact_sheets_generated": len(sheet_paths),
        "verifier_tiling_strategy_completed": True,
        "prompt_candidate_authored": False,
        "optional_prompt_candidate_run": False,
        "selected_baseline": {"id": "fp8_composite_pp045c_baseline", **pp045c_eval["totals"]},
        "pp046a_status": {"id": "pp046a", **pp046a_eval["totals"], "locked": False, "reason": "visual review failed/mixed"},
        "next_work": "verifier_or_tiling_crop_pass",
        "hard_boundaries_preserved": True,
    }

    # Core docs and data.
    write_text(PACKAGE / "README.md", "# v048 FP8 FN Recovery Crop/Verifier Loop\n\nExperiment-only false-negative recovery planning from the locked pp045c FP8 composite baseline. This tranche does not promote FP8, mutate product runtime, or call the VLM.\n")
    write_json(PACKAGE / "source_manifest.json", source_manifest)
    write_json(PACKAGE / "artifact_inventory.json", artifact_inventory)
    write_text(PACKAGE / "artifact_inventory.md", f"""# Artifact Inventory

- Locked baseline: `pp045c = {metric_line(pp045c_eval['totals'])}`.
- Diagnostic pp046a: `{metric_line(pp046a_eval['totals'])}`, not locked.
- Case 101 excluded: `{artifact_inventory['case_101_excluded']}`.
- Image count preserved: `{artifact_inventory['image_count_preserved']}`.
- Residual FNs inventoried: `{len(fn_rows)}`.
- Local-only FN crops generated: `{source_images_found}`.
- Local-only contact sheets generated: `{len(sheet_paths)}`.

Do not push JPG crop/contact-sheet files to the private review repo.
""")
    write_json(PACKAGE / "residual_fn_inventory.json", {"generated_at": generated, "baseline": "pp045c_49", "fn_count": len(fn_rows), "class_counts": fn_class_counts, "rows": fn_rows})
    write_csv(PACKAGE / "residual_fn_taxonomy.csv", fn_rows)
    write_text(PACKAGE / "residual_fn_inventory.md", f"""# Residual FN Inventory

Baseline: `pp045c = {metric_line(pp045c_eval['totals'])}`.

All `{len(fn_rows)}` false negatives were inventoried.

## Class Counts

{markdown_table([{"class": key, "count": value} for key, value in fn_class_counts.items()], ["class", "count"])}

## Case Notes

Dense cases remain the key recall challenge: case 67 has `{case_metrics.get('67')}` and case 84 has `{case_metrics.get('84')}` under pp045c. Case 110 remains `{case_metrics.get('110')}` and is smoke/debris-obscured. Case 155 and 166 controls remain `{case_metrics.get('155')}` and `{case_metrics.get('166')}`.
""")
    write_json(PACKAGE / "fn_crop_manifest.json", {"generated_at": generated, "local_only": True, "rows": crop_rows, "contact_sheets": sheet_paths})
    write_csv(PACKAGE / "fn_crop_manifest.csv", crop_rows)
    write_json(PACKAGE / "fn_crop_review.json", {"generated_at": generated, "rows": review_rows, "review_counts": review_counts, "intervention_counts": intervention_counts})
    write_text(PACKAGE / "fn_crop_review.md", f"""# FN Crop Review

Local-only crops/contact sheets were generated for `{source_images_found}` of `{len(fn_rows)}` FNs.

The review does not authorize prompt wording. It routes residual FN clusters toward crop/tiling and verifier work.

## Review Counts

{markdown_table([{"review_class": key, "count": value} for key, value in review_counts.items()], ["review_class", "count"])}

## Intervention Counts

{markdown_table([{"intervention": key, "count": value} for key, value in intervention_counts.items()], ["intervention", "count"])}
""")
    write_json(PACKAGE / "fn_recovery_strategy.json", fn_recovery_strategy)
    write_text(PACKAGE / "fn_recovery_strategy.md", f"""# FN Recovery Strategy

Selected baseline: `fp8_composite_pp045c_baseline = {metric_line(pp045c_eval['totals'])}`.

pp046a remains diagnostic only: `{metric_line(pp046a_eval['totals'])}` was not locked because visual review failed/mixed.

The next recovery lever should be experiment-only crop/tiling plus verifier design, not prompt wording. The residual classes are:

{markdown_table([{"class": key, "count": value} for key, value in fn_class_counts.items()], ["class", "count"])}

No optional prompt candidate was authored.
""")
    write_json(PACKAGE / "verifier_design_plan.json", verifier_design)
    write_text(PACKAGE / "verifier_design_plan.md", f"""# Verifier Design Plan

Objective: recover selected FNs without reintroducing false positives.

The verifier should operate on crop/tile proposals and prediction geometry. It must not use reference boxes, eval state, case IDs, or ground truth at inference time.

## JSON Contract

```json
{json.dumps(verifier_design['verifier_json_schema'], indent=2)}
```

## Merge Gates

{chr(10).join(f"- {gate}" for gate in verifier_design['merge_gates'])}

## Stop Modes

{chr(10).join(f"- {mode}" for mode in verifier_design['stop_modes'])}
""")
    write_json(PACKAGE / "tiling_crop_strategy.json", tiling_strategy)
    write_text(PACKAGE / "tiling_crop_strategy.md", f"""# Tiling Crop Strategy

Recommendation: use an experiment-only crop/tiling pass before prompt wording.

Start with `{tiling_strategy['tile_policy']['experiment_only_start']}` and overlap `{tiling_strategy['tile_policy']['overlap']}`. Merge mapped boxes only through strict verifier and postprocessing gates.

## Class Targets

{markdown_table([{"class": key, "strategy": value} for key, value in tiling_strategy['class_targets'].items()], ["class", "strategy"])}
""")
    write_json(PACKAGE / "optional_prompt_candidate_decision.json", optional_prompt_decision)
    write_text(PACKAGE / "optional_prompt_candidate_decision.md", """# Optional Prompt Candidate Decision

Decision: `do_not_author_prompt`.

No narrow, low-risk prompt-addressable FN cluster was isolated. The current evidence points to verifier and tiling/crop work first. A future prompt candidate should only be considered after crop review proves one cluster can be addressed without broad recall wording or dense-case regression.
""")
    write_json(PACKAGE / "intervention_registry.json", {"generated_at": generated, "interventions": interventions})
    write_json(PACKAGE / "intervention_matrix.json", {"generated_at": generated, "rows": interventions})
    write_text(PACKAGE / "intervention_matrix.md", "\n".join([
        "# Intervention Matrix",
        "",
        "| Intervention | Type | Baseline | Metrics | FN Count | Status |",
        "|---|---|---|---:|---:|---|",
        *[
            f"| `{row['intervention_id']}` | {row['type']} | {row['baseline']} | `{metric_line(row['metrics'])}` | {row.get('fn_count', 'n/a')} | {row['status']} |"
            for row in interventions
        ],
        "",
    ]))
    write_text(PACKAGE / "live_metrics_log.md", f"""# Live Metrics Log

- Old/product v020c: `186 / 33 / 25 / 58`.
- Locked pp045c baseline: `{metric_line(pp045c_eval['totals'])}`.
- Diagnostic pp046a: `{metric_line(pp046a_eval['totals'])}`, not locked.
- Optional prompt candidate authored: `False`.
- Live VLM calls: `0`.
""")
    write_json(PACKAGE / "recovery_log.json", {"generated_at": generated, "events": ["offline-only v048 started", "pp045c reconstructed", "38 FNs inventoried", "local-only crops/contact sheets generated", "crop review and verifier/tiling strategy written", "no prompt candidate authored"]})
    write_text(PACKAGE / "recovery_log.md", "# Recovery Log\n\n- Reconstructed pp045c from frozen v034a-derived outputs.\n- Inventoried all 38 FNs.\n- Generated local-only crops and contact sheets.\n- Wrote verifier and tiling/crop strategy.\n- No prompt candidate authored; no live VLM call made.\n")
    write_text(PACKAGE / "lessons_learned.md", "# Lessons Learned\n\n- The locked pp045c surface has already reduced FPs substantially; remaining improvement is FN-heavy.\n- pp046a proves an upper bound for FP cleanup but failed visual lock, so it cannot be used as the baseline.\n- Remaining FNs are better approached through crop/tiling/verifier design than broad prompt recall wording.\n")
    write_text(PACKAGE / "strategy_state.md", f"# Strategy State\n\nCurrent locked baseline: `fp8_composite_pp045c_baseline = {metric_line(pp045c_eval['totals'])}`.\n\nDiagnostic only: `pp046a = {metric_line(pp046a_eval['totals'])}`, not locked.\n\nResidual FNs: `{len(fn_rows)}`.\n\nPrompt candidate authored: `False`.\n\nNext axis: experiment-only crop/tiling verifier tranche.\n")
    write_json(PACKAGE / "verifier_designs/fn_crop_verifier_design.json", verifier_design)
    write_text(PACKAGE / "verifier_designs/fn_crop_verifier_design.md", (PACKAGE / "verifier_design_plan.md").read_text(encoding="utf-8"))
    write_json(PACKAGE / "final_recommendation.json", final)
    write_text(PACKAGE / "final_recommendation.md", f"""# v048 Final Recommendation

Generated: `{generated}`

All 38 FNs inventoried: `true`.

Locked baseline remains: `fp8_composite_pp045c_baseline = {metric_line(pp045c_eval['totals'])}`.

pp046a remains diagnostic only: `{metric_line(pp046a_eval['totals'])}`; it failed visual lock in v047.

## Dominant FN Classes

{markdown_table([{"class": key, "count": value} for key, value in fn_class_counts.items()], ["class", "count"])}

## Crop/Verifier Result

Local-only crops/contact sheets were generated under `review_images/` for review. These image files should not be pushed to the private review repo.

Verifier/tiling strategy completed: `true`.

Prompt candidate authored: `false`.

## Recommendation

Next work should be an experiment-only verifier or tiling/crop pass. Do not resume prompt wording until crop review isolates a narrow, low-risk, prompt-addressable FN cluster.

Hard boundaries were preserved.
""")

    # Required stdout blocks.
    print(f"""=== V048 STATUS ===
phase: artifact_inventory
baseline: pp045c_49
intervention: none
type: none
metrics: {metric_line(pp045c_eval['totals'])}
fn_count: n/a
case_66: {case_metrics.get('66')}
case_67: {case_metrics.get('67')}
case_84: {case_metrics.get('84')}
case_100: {case_metrics.get('100')}
case_110: {case_metrics.get('110')}
case_155: {case_metrics.get('155')}
case_166: {case_metrics.get('166')}
office_negative: not_run
prompt_candidate_authored: false
status: inventory_complete
main_lesson: Frozen pp045c artifacts were reconstructed and matched the locked 181/38/11/49 baseline.
next_axis: Inventory all residual FNs and generate local-only crop aids.
===================""")
    print(f"""=== V048 STATUS ===
phase: fn_inventory
baseline: pp045c_49
intervention: fn001_pp045c_residual_fn_inventory
type: fn_inventory
metrics: {metric_line(pp045c_eval['totals'])}
fn_count: {len(fn_rows)}
case_66: {case_metrics.get('66')}
case_67: {case_metrics.get('67')}
case_84: {case_metrics.get('84')}
case_100: {case_metrics.get('100')}
case_110: {case_metrics.get('110')}
case_155: {case_metrics.get('155')}
case_166: {case_metrics.get('166')}
office_negative: not_run
prompt_candidate_authored: false
status: inventory_complete
main_lesson: The remaining error surface is all recall work plus 11 locked-baseline FPs, with 38 FNs dominated by dense, small, smoke-obscured, and structure-piece misses.
next_axis: Generate local-only FN crops and contact sheets.
===================""")
    print(f"""=== V048 STATUS ===
phase: crop_generation
baseline: pp045c_49
intervention: crop001_reference_centered_local_only_aids
type: crop_review
metrics: {metric_line(pp045c_eval['totals'])}
fn_count: {len(fn_rows)}
case_66: {case_metrics.get('66')}
case_67: {case_metrics.get('67')}
case_84: {case_metrics.get('84')}
case_100: {case_metrics.get('100')}
case_110: {case_metrics.get('110')}
case_155: {case_metrics.get('155')}
case_166: {case_metrics.get('166')}
office_negative: not_run
prompt_candidate_authored: false
status: crop_review_complete
main_lesson: Reference-centered crop aids were generated locally for all available FN source images and are excluded from review-repo publishing.
next_axis: Review crop classes and decide verifier versus prompt.
===================""")
    print(f"""=== V048 STATUS ===
phase: crop_review
baseline: pp045c_49
intervention: crop001_reference_centered_local_only_aids
type: crop_review
metrics: {metric_line(pp045c_eval['totals'])}
fn_count: {len(fn_rows)}
case_66: {case_metrics.get('66')}
case_67: {case_metrics.get('67')}
case_84: {case_metrics.get('84')}
case_100: {case_metrics.get('100')}
case_110: {case_metrics.get('110')}
case_155: {case_metrics.get('155')}
case_166: {case_metrics.get('166')}
office_negative: not_run
prompt_candidate_authored: false
status: crop_review_complete
main_lesson: Crop review routes the residual FN surface to crop/tiling and verifier design rather than prompt wording.
next_axis: Write verifier and tiling/crop strategy.
===================""")
    print(f"""=== V048 STATUS ===
phase: verifier_design
baseline: pp045c_49
intervention: ver001_crop_verifier_tiling_plan
type: verifier_design
metrics: {metric_line(pp045c_eval['totals'])}
fn_count: {len(fn_rows)}
case_66: {case_metrics.get('66')}
case_67: {case_metrics.get('67')}
case_84: {case_metrics.get('84')}
case_100: {case_metrics.get('100')}
case_110: {case_metrics.get('110')}
case_155: {case_metrics.get('155')}
case_166: {case_metrics.get('166')}
office_negative: not_run
prompt_candidate_authored: false
status: verifier_plan_complete
main_lesson: The next safe tranche should test an experiment-only crop/tiling verifier before any prompt candidate.
next_axis: Run a gated crop/tiling verifier tranche; prompt only after a narrow cluster is proven low risk.
===================""")


if __name__ == "__main__":
    main()
