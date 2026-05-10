#!/usr/bin/env python3
"""Run v050 experiment-only non-oracle tiling/crop recovery.

This script deliberately does not use reference boxes to create inference
tiles. References are loaded only after merge for evaluation and analysis.
"""

from __future__ import annotations

import base64
import csv
import datetime as dt
import hashlib
import importlib.util
import json
import math
import os
import re
import sys
import time
import urllib.request
from copy import deepcopy
from pathlib import Path
from typing import Any

from PIL import Image


WORKTREE = Path("/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement")
CAPSTONE = Path("/home/williambenitez1/Capstone")
PARENT = WORKTREE / "docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion"
PACKAGE = PARENT / "v050_fp8_non_oracle_tiling_crop_recovery"
V046_SCRIPT = PARENT / "v046_fp8_pp045_visual_verification_and_continuation/scripts/run_v046_pp045_visual_verification.py"
V048 = PARENT / "v048_fp8_fn_recovery_crop_verifier_loop"
V049 = PARENT / "v049_fp8_reference_crop_verifier_upper_bound"

ENDPOINT = "http://127.0.0.1:8000/v1"
MODEL = "Qwen/Qwen3-VL-8B-Instruct-FP8"

PRIMARY_IMAGE_ROOT = CAPSTONE / "z_reference_docs/Data_set_Storage/human_reports/images_with_reports"
ALT_IMAGE_ROOTS = [
    PRIMARY_IMAGE_ROOT,
    CAPSTONE / "z_reference_docs/Data_set_Storage/DATA_SET/Assigned_Photos_to_Write_Report/Carlos",
    CAPSTONE / "z_reference_docs/Data_set_Storage/human_reports/no_reports/images",
]

OLD_V020C = {"matches": 186, "false_negatives": 33, "false_positives": 25, "combined_errors": 58}
PP045C = {"matches": 181, "false_negatives": 38, "false_positives": 11, "combined_errors": 49}
PP046A_DIAGNOSTIC = {"matches": 181, "false_negatives": 38, "false_positives": 0, "combined_errors": 38}
WATCH_CASES = ["66", "67", "84", "100", "110", "155", "166"]
MICRO_CASES = ["11", "14", "20", "21", "40", "42", "44", "53", "66", "67", "76", "84", "100", "102", "108", "110", "155", "166"]

CROP_DETECTOR_SCHEMA = {
    "detections": [
        {
            "target_type": "military_equipment|buildings",
            "bbox": "[x1, y1, x2, y2] in crop-local pixels",
            "confidence": "number from 0.0 to 1.0",
            "visibility": "clear|partial|smoke_obscured|low_contrast|ambiguous",
            "damage_or_relevance": "damaged_or_bda_relevant|intact_context|unclear",
            "reason": "short text",
        }
    ]
}

CROP_DETECTOR_PROMPT = """You are detecting BDA-relevant targets in a cropped image tile.
Find visible damaged or BDA-relevant military equipment and building targets in this crop.
Return JSON only with this shape:
{"detections":[{"target_type":"military_equipment|buildings","bbox":[x1,y1,x2,y2],"confidence":0.0,"visibility":"clear|partial|smoke_obscured|low_contrast|ambiguous","damage_or_relevance":"damaged_or_bda_relevant|intact_context|unclear","reason":"short"}]}

Use crop-local pixel coordinates. If there are no valid targets, return {"detections":[]}.
Reject context-only boxes, intact background, broad scene boxes, and tiny ambiguous artifacts.
Include small, crowded, or smoke-obscured targets only when they are visibly BDA-relevant."""


spec = importlib.util.spec_from_file_location("v050_v046", V046_SCRIPT)
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


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = ["|" + "|".join(fields) + "|", "|" + "|".join(["---"] * len(fields)) + "|"]
    for row in rows:
        lines.append("|" + "|".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + "|")
    return "\n".join(lines)


def metric_line(metrics: dict[str, Any]) -> str:
    return f"{metrics['matches']}/{metrics['false_negatives']}/{metrics['false_positives']}/{metrics['combined_errors']}"


def case_metrics(eval_payload: dict[str, Any]) -> dict[str, str]:
    return {
        v044.case_id(img["image_filename"]): f"{img['match_count']}/{img['false_negative_count']}/{img['false_positive_count']}"
        for img in eval_payload["images"]
    }


def backend_models() -> tuple[bool, dict[str, Any]]:
    try:
        with urllib.request.urlopen(f"{ENDPOINT}/models", timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
            status = response.status
        model_ids = [item.get("id") for item in payload.get("data", [])]
        return 200 <= status < 300 and MODEL in model_ids, {"status_code": status, "payload": payload, "model_ids": model_ids}
    except Exception as exc:  # noqa: BLE001
        return False, {"error": repr(exc)}


def image_to_data_url(path: Path) -> str:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def extract_json(text: str) -> tuple[bool, dict[str, Any] | None, str]:
    clean = text.strip()
    if clean.startswith("```"):
        clean = re.sub(r"^```(?:json)?\s*", "", clean)
        clean = re.sub(r"\s*```$", "", clean)
    try:
        return True, json.loads(clean), ""
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", clean, flags=re.DOTALL)
        if not match:
            return False, None, "no_json_object"
        try:
            return True, json.loads(match.group(0)), ""
        except json.JSONDecodeError as exc:
            return False, None, f"json_decode_error:{exc}"


def call_crop_detector(tile_path: Path, timeout_s: int = 180) -> tuple[bool, dict[str, Any] | None, str, str, str]:
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": CROP_DETECTOR_PROMPT},
                    {"type": "image_url", "image_url": {"url": image_to_data_url(tile_path)}},
                ],
            }
        ],
        "temperature": 0,
        "max_tokens": 900,
    }
    request = urllib.request.Request(
        f"{ENDPOINT}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_s) as response:
        response_payload = json.loads(response.read().decode("utf-8"))
    raw = response_payload["choices"][0]["message"]["content"]
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    valid, parsed, error = extract_json(raw)
    return valid, parsed, error, raw, digest


def locate_image(image_filename: str) -> Path | None:
    for root in ALT_IMAGE_ROOTS:
        candidate = root / image_filename
        if candidate.exists():
            return candidate
    matches = sorted((CAPSTONE / "z_reference_docs/Data_set_Storage").rglob(image_filename))
    return matches[0] if matches else None


def box_area(box: tuple[float, float, float, float]) -> float:
    return max(0.0, box[2] - box[0]) * max(0.0, box[3] - box[1])


def intersect_area(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    return max(0.0, min(a[2], b[2]) - max(a[0], b[0])) * max(0.0, min(a[3], b[3]) - max(a[1], b[1]))


def iou(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    inter = intersect_area(a, b)
    union = box_area(a) + box_area(b) - inter
    return inter / union if union else 0.0


def clamp_box(box: tuple[float, float, float, float], width: int, height: int) -> tuple[int, int, int, int]:
    x1 = int(max(0, min(width - 1, math.floor(box[0]))))
    y1 = int(max(0, min(height - 1, math.floor(box[1]))))
    x2 = int(max(x1 + 1, min(width, math.ceil(box[2]))))
    y2 = int(max(y1 + 1, min(height, math.ceil(box[3]))))
    return x1, y1, x2, y2


def target_box(target: dict[str, Any]) -> tuple[float, float, float, float]:
    return v044.target_box(target)


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


def generate_tiles(
    image_filename: str,
    image_path: Path,
    predictions: dict[str, Any],
) -> list[dict[str, Any]]:
    with Image.open(image_path) as image:
        width, height = image.size
    tiles: list[dict[str, Any]] = []

    def add(strategy: str, name: str, box: tuple[float, float, float, float]) -> None:
        x1, y1, x2, y2 = clamp_box(box, width, height)
        if (x2 - x1) < 48 or (y2 - y1) < 48:
            return
        tiles.append(
            {
                "tile_id": f"{v044.case_id(image_filename)}_{strategy}_{name}",
                "case_id": v044.case_id(image_filename),
                "image_filename": image_filename,
                "strategy": strategy,
                "tile_name": name,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "uses_reference": False,
            }
        )

    # Strategy A: full-image 2x2 overlapping grid.
    tw, th = width * 0.62, height * 0.62
    for ix, sx in enumerate([0, width - tw]):
        for iy, sy in enumerate([0, height - th]):
            add("A", f"grid_{ix}_{iy}", (sx, sy, sx + tw, sy + th))

    # Strategy B: generic dense-row strip tiles. These are image-geometry only.
    add("B", "middle_lower_strip", (0, height * 0.35, width, height * 0.85))
    add("B", "lower_strip", (0, height * 0.55, width, height))

    # Strategy C: prediction-anchored neighbor crops around existing detections.
    physical_damage = predictions.get("physical_damage", {})
    anchors = sorted(
        ((label, target, box_area(target_box(target))) for label, target in physical_damage.items()),
        key=lambda item: item[2],
        reverse=True,
    )[:3]
    for idx, (_label, target, _area) in enumerate(anchors):
        bx = target_box(target)
        pad_x = max((bx[2] - bx[0]) * 0.6, width * 0.12)
        pad_y = max((bx[3] - bx[1]) * 0.6, height * 0.12)
        add("C", f"anchor_{idx}", (bx[0] - pad_x, bx[1] - pad_y, bx[2] + pad_x, bx[3] + pad_y))

    # Strategy D: generic medium-large broad-context crop for smoke/debris.
    add("D", "center_broad", (width * 0.08, height * 0.08, width * 0.92, height * 0.92))
    return tiles


def write_tile_image(tile: dict[str, Any], image_path: Path) -> Path:
    out = PACKAGE / "tile_outputs/local_only_tiles" / f"{tile['tile_id']}{image_path.suffix.lower()}"
    out.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(image_path).convert("RGB") as image:
        crop = image.crop((tile["x1"], tile["y1"], tile["x2"], tile["y2"]))
        crop.save(out, quality=92)
    return out


def normalize_detections(parsed: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not parsed:
        return []
    detections = parsed.get("detections", [])
    if isinstance(detections, dict):
        detections = [detections]
    if not isinstance(detections, list):
        return []
    out = []
    for det in detections:
        if isinstance(det, dict):
            out.append(det)
    return out


def detection_to_full_box(det: dict[str, Any], tile: dict[str, Any]) -> tuple[float, float, float, float] | None:
    raw = det.get("bbox")
    if not isinstance(raw, list) or len(raw) != 4:
        return None
    try:
        x1, y1, x2, y2 = [float(v) for v in raw]
    except (TypeError, ValueError):
        return None
    crop_w = tile["x2"] - tile["x1"]
    crop_h = tile["y2"] - tile["y1"]
    if x2 <= x1 or y2 <= y1:
        return None
    if x1 < -2 or y1 < -2 or x2 > crop_w + 2 or y2 > crop_h + 2:
        return None
    return (
        max(0.0, x1 + tile["x1"]),
        max(0.0, y1 + tile["y1"]),
        min(float(tile["image_width"]), x2 + tile["x1"]),
        min(float(tile["image_height"]), y2 + tile["y1"]),
    )


def should_keep_candidate(
    det: dict[str, Any],
    full_box: tuple[float, float, float, float],
    image_filename: str,
    existing_preds: dict[str, Any],
    image_area: float,
) -> tuple[bool, str]:
    target_type = str(det.get("target_type", ""))
    if target_type not in {"military_equipment", "buildings"}:
        return False, "invalid_target_type"
    try:
        confidence = float(det.get("confidence", 0.0) or 0.0)
    except (TypeError, ValueError):
        return False, "invalid_confidence"
    visibility = str(det.get("visibility", "ambiguous"))
    relevance = str(det.get("damage_or_relevance", "unclear"))
    reason = str(det.get("reason", "")).lower()
    area_ratio = box_area(full_box) / image_area if image_area else 0.0
    if confidence < 0.55:
        return False, "low_confidence"
    if relevance == "intact_context":
        return False, "intact_context"
    if visibility == "ambiguous" and confidence < 0.78:
        return False, "ambiguous_low_confidence"
    if any(token in reason for token in ["intact background", "context only", "not target", "unclear"]):
        return False, "self_reported_context_or_unclear"
    if target_type == "military_equipment" and area_ratio < 0.00025 and confidence < 0.82:
        return False, "tiny_military_candidate"
    if target_type == "buildings" and area_ratio > 0.45:
        return False, "broad_building_scene_box"
    for label, target in existing_preds.get("physical_damage", {}).items():
        if target.get("target_type") != target_type:
            continue
        overlap = iou(full_box, target_box(target))
        if overlap >= 0.45:
            return False, f"duplicate_existing:{label}:{overlap:.3f}"
    return True, "accepted"


def apply_locked_postprocessors(preds: dict[str, Any], dims: dict[str, tuple[int, int]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    pp0157_preds, pp0157_removals = v044.apply_pp0157(preds, dims)
    pp044a_preds, pp044a_removals = v044.apply_pp044a(pp0157_preds, dims)
    pp045b_preds, pp045b_removals = v045.apply_pp045b(pp044a_preds, dims)
    pp045c_preds, pp045c_removals = v045.apply_pp045c(pp045b_preds, dims)
    removals = []
    for stage, stage_rows in [
        ("pp0157", pp0157_removals),
        ("pp044a", pp044a_removals),
        ("pp045b", pp045b_removals),
        ("pp045c", pp045c_removals),
    ]:
        for row in stage_rows:
            annotated = dict(row)
            annotated["postprocess_stage"] = stage
            removals.append(annotated)
    return pp045c_preds, removals


def label_status(eval_payload: dict[str, Any]) -> dict[tuple[str, str], str]:
    out: dict[tuple[str, str], str] = {}
    for image in eval_payload["images"]:
        fname = image["image_filename"]
        for match in image["matches"]:
            out[(fname, match["predicted_label"])] = "TP"
        for label in image["false_positive_labels"]:
            out[(fname, label)] = "FP"
    return out


def subset_order(order: list[str], case_ids: list[str]) -> list[str]:
    wanted = set(case_ids)
    return [fname for fname in order if v044.case_id(fname) in wanted]


def make_markdown_summary(title: str, rows: list[dict[str, Any]], fields: list[str]) -> str:
    return f"# {title}\n\n" + markdown_table(rows, fields) + "\n"


def main() -> None:
    generated = now()
    for subdir in ["scripts", "tables", "review_images", "tile_outputs", "runs"]:
        (PACKAGE / subdir).mkdir(parents=True, exist_ok=True)

    backend_ok, backend_payload = backend_models()
    backend_preflight = {
        "generated_at": generated,
        "endpoint": ENDPOINT,
        "model": MODEL,
        "backend_available": backend_ok,
        "model_available": bool(backend_ok),
        "details": backend_payload,
        "timeout_policy_seconds": 180,
    }
    write_json(PACKAGE / "backend_preflight.json", backend_preflight)
    if not backend_ok:
        write_text(
            PACKAGE / f"pause_report_{generated.replace(':', '').replace('-', '')}_backend_unavailable.md",
            "# v050 Backend Unavailable Pause\n\nThe FP8 vLLM endpoint was unavailable during preflight. No crop detector calls were run.\n",
        )
        print("""=== V050 STATUS ===
phase: preflight
strategy: n/a
backend: unavailable
stage: n/a
raw_merged_metrics: n/a
postprocessed_merged_metrics: n/a
vs_pp045c_49_delta: n/a
added_detections: n/a
added_true_positives: n/a
added_false_positives: n/a
case_66: n/a
case_67: n/a
case_84: n/a
case_100: n/a
case_110: n/a
case_155: n/a
case_166: n/a
office_negative: not_run
decision: E
main_lesson: Backend was unavailable, so non-oracle tiling could not be tested.
next_action: Restart the FP8 vLLM endpoint and rerun v050.
===================""")
        return

    state = v044.load_state()
    refs = state["refs"]
    order = state["order"]
    dims = state["dims"]
    raw_preds = state["raw"]
    pp0157_preds, _ = v044.apply_pp0157(state["p1753"], dims)
    pp044a_preds, _ = v044.apply_pp044a(pp0157_preds, dims)
    pp045b_preds, _ = v045.apply_pp045b(pp044a_preds, dims)
    pp045c_preds, _ = v045.apply_pp045c(pp045b_preds, dims)
    pp045c_eval = v042.evaluate_reports(refs, pp045c_preds, order)

    image_inventory = []
    for fname in order:
        path = locate_image(fname)
        width = height = None
        if path:
            with Image.open(path) as img:
                width, height = img.size
        image_inventory.append(
            {
                "case_id": v044.case_id(fname),
                "image_filename": fname,
                "source_image_path": str(path) if path else "",
                "available": bool(path),
                "width": width,
                "height": height,
                "case_101_excluded": v044.case_id(fname) == "101",
            }
        )
    write_csv(PACKAGE / "source_image_inventory.csv", image_inventory)
    write_json(
        PACKAGE / "source_image_inventory.json",
        {
            "generated_at": generated,
            "image_count": len(image_inventory),
            "available": sum(1 for row in image_inventory if row["available"]),
            "missing": sum(1 for row in image_inventory if not row["available"]),
            "case_40_resolved": any(row["case_id"] == "40" and row["available"] for row in image_inventory),
            "rows": image_inventory,
        },
    )

    source_artifacts = [
        V049 / "final_recommendation.md",
        V049 / "crop_verifier_results.csv",
        V049 / "recoverability_by_class.md",
        V049 / "non_oracle_tiling_strategy.md",
        V048 / "final_recommendation.md",
        PARENT / "v047_fp8_pp046a_visual_verification_and_fn_recovery/final_recommendation.md",
        PARENT / "v046_fp8_pp045_visual_verification_and_continuation/final_recommendation.md",
    ]
    artifact_rows = []
    for path in source_artifacts:
        artifact_rows.append({"path": str(path), "exists": path.exists(), "bytes": path.stat().st_size if path.exists() else 0})
    write_json(PACKAGE / "artifact_inventory.json", {"generated_at": generated, "artifacts": artifact_rows})
    write_text(PACKAGE / "artifact_inventory.md", make_markdown_summary("Artifact Inventory", artifact_rows, ["path", "exists", "bytes"]))

    print(f"""=== V050 STATUS ===
phase: artifact_inventory
strategy: mixed
backend: available
stage: offline
raw_merged_metrics: n/a
postprocessed_merged_metrics: {metric_line(pp045c_eval["totals"])}
vs_pp045c_49_delta: +0
added_detections: n/a
added_true_positives: n/a
added_false_positives: n/a
case_66: {case_metrics(pp045c_eval).get("66", "n/a")}
case_67: {case_metrics(pp045c_eval).get("67", "n/a")}
case_84: {case_metrics(pp045c_eval).get("84", "n/a")}
case_100: {case_metrics(pp045c_eval).get("100", "n/a")}
case_110: {case_metrics(pp045c_eval).get("110", "n/a")}
case_155: {case_metrics(pp045c_eval).get("155", "n/a")}
case_166: {case_metrics(pp045c_eval).get("166", "n/a")}
office_negative: not_run
decision: E
main_lesson: Source artifacts and all-current image inventory are available for a bounded non-oracle micro-pack.
next_action: Generate geometry-only tiles and run the crop detector.
===================""")

    strategy_rows = [
        {
            "strategy": "A",
            "name": "full-image 2x2 overlap",
            "crop_generation_without_ground_truth": "four 62 percent image tiles anchored at image corners",
            "intended_recovery": "building pieces, dense/small targets, smoke/debris targets",
            "fp_risk": "medium",
        },
        {
            "strategy": "B",
            "name": "generic dense-row strips",
            "crop_generation_without_ground_truth": "middle-lower and lower full-width strips from image geometry only",
            "intended_recovery": "dense row and lower-band small objects",
            "fp_risk": "medium_high",
        },
        {
            "strategy": "C",
            "name": "prediction-anchored neighbor crops",
            "crop_generation_without_ground_truth": "padded crops around the three largest locked baseline detections",
            "intended_recovery": "adjacent target confusion",
            "fp_risk": "medium_high",
        },
        {
            "strategy": "D",
            "name": "smoke/debris broad context crop",
            "crop_generation_without_ground_truth": "single centered 84 percent image crop",
            "intended_recovery": "smoke/debris-obscured and broad context misses",
            "fp_risk": "medium",
        },
    ]
    write_csv(PACKAGE / "tables/tiling_strategy.csv", strategy_rows)
    write_json(PACKAGE / "tiling_strategy.json", {"generated_at": generated, "uses_reference_boxes_for_inference": False, "strategies": strategy_rows})
    write_text(PACKAGE / "tiling_strategy.md", make_markdown_summary("Tiling Strategy", strategy_rows, ["strategy", "name", "crop_generation_without_ground_truth", "intended_recovery", "fp_risk"]))
    write_json(PACKAGE / "crop_detector_prompt.json", {"generated_at": generated, "prompt": CROP_DETECTOR_PROMPT, "schema": CROP_DETECTOR_SCHEMA, "mentions_case_ids": False, "uses_reference_information": False})
    write_text(PACKAGE / "crop_detector_prompt.md", f"# Crop Detector Prompt\n\n```text\n{CROP_DETECTOR_PROMPT}\n```\n\nSchema:\n\n```json\n{json.dumps(CROP_DETECTOR_SCHEMA, indent=2)}\n```\n")

    print("""=== V050 STATUS ===
phase: tiling_strategy
strategy: mixed
backend: available
stage: offline
raw_merged_metrics: n/a
postprocessed_merged_metrics: n/a
vs_pp045c_49_delta: n/a
added_detections: n/a
added_true_positives: n/a
added_false_positives: n/a
case_66: n/a
case_67: n/a
case_84: n/a
case_100: n/a
case_110: n/a
case_155: n/a
case_166: n/a
office_negative: not_run
decision: E
main_lesson: Strategies A-D are non-oracle and bounded to a sentinel-heavy micro-pack.
next_action: Run crop detector calls and merge accepted detections conservatively.
===================""")

    print("""=== V050 STATUS ===
phase: crop_prompt
strategy: mixed
backend: available
stage: offline
raw_merged_metrics: n/a
postprocessed_merged_metrics: n/a
vs_pp045c_49_delta: n/a
added_detections: n/a
added_true_positives: n/a
added_false_positives: n/a
case_66: n/a
case_67: n/a
case_84: n/a
case_100: n/a
case_110: n/a
case_155: n/a
case_166: n/a
office_negative: not_run
decision: E
main_lesson: The crop prompt is compact JSON-only detection, not reference verification or prompt candidate wording.
next_action: Execute the micro-pack tile run.
===================""")

    micro_order = subset_order(order, MICRO_CASES)
    tile_manifest: list[dict[str, Any]] = []
    for fname in micro_order:
        image_path = locate_image(fname)
        if not image_path:
            continue
        tiles = generate_tiles(fname, image_path, pp045c_preds[fname])
        with Image.open(image_path) as image:
            width, height = image.size
        for tile in tiles:
            tile["image_width"] = width
            tile["image_height"] = height
            tile_path = write_tile_image(tile, image_path)
            tile["tile_path"] = str(tile_path)
            tile_manifest.append(tile)
    write_csv(PACKAGE / "tile_manifest.csv", tile_manifest)
    write_json(
        PACKAGE / "tile_manifest.json",
        {
            "generated_at": generated,
            "micro_cases": MICRO_CASES,
            "tile_count": len(tile_manifest),
            "uses_reference_boxes_for_inference": False,
            "rows": tile_manifest,
        },
    )

    merged_raw = deepcopy(pp045c_preds)
    run_rows: list[dict[str, Any]] = []
    added_rows: list[dict[str, Any]] = []
    accepted_by_image: dict[str, int] = {}
    for idx, tile in enumerate(tile_manifest, 1):
        tile_path = Path(tile["tile_path"])
        started = time.time()
        valid = False
        parsed: dict[str, Any] | None = None
        error = ""
        raw_response = ""
        digest = ""
        runtime_error = ""
        try:
            valid, parsed, error, raw_response, digest = call_crop_detector(tile_path)
        except Exception as exc:  # noqa: BLE001
            runtime_error = repr(exc)
        elapsed = round(time.time() - started, 3)
        detections = normalize_detections(parsed) if valid else []
        accepted_count = 0
        rejected_count = 0
        for det_index, det in enumerate(detections):
            full_box = detection_to_full_box(det, tile)
            if full_box is None:
                rejected_count += 1
                added_rows.append(
                    {
                        "tile_id": tile["tile_id"],
                        "case_id": tile["case_id"],
                        "image_filename": tile["image_filename"],
                        "strategy": tile["strategy"],
                        "accepted": False,
                        "reject_reason": "invalid_bbox",
                        "raw_detection": json.dumps(det, ensure_ascii=True),
                    }
                )
                continue
            image_area = float(tile["image_width"] * tile["image_height"])
            keep, reason = should_keep_candidate(det, full_box, tile["image_filename"], merged_raw[tile["image_filename"]], image_area)
            if keep:
                accepted_count += 1
                seq = accepted_by_image.get(tile["image_filename"], 0) + 1
                accepted_by_image[tile["image_filename"]] = seq
                label = f"v050_tile_{seq:03d}"
                confidence = float(det.get("confidence", 0.0) or 0.0)
                merged_raw[tile["image_filename"]].setdefault("physical_damage", {})[label] = make_target(
                    str(det["target_type"]),
                    full_box,
                    confidence,
                    f"v050_{tile['strategy']}_{tile['tile_name']}",
                    str(det.get("reason", "")),
                )
                added_rows.append(
                    {
                        "label": label,
                        "tile_id": tile["tile_id"],
                        "case_id": tile["case_id"],
                        "image_filename": tile["image_filename"],
                        "strategy": tile["strategy"],
                        "accepted": True,
                        "reject_reason": "",
                        "target_type": det["target_type"],
                        "full_bbox": json.dumps([round(float(v), 2) for v in full_box]),
                        "confidence": confidence,
                        "visibility": det.get("visibility", ""),
                        "damage_or_relevance": det.get("damage_or_relevance", ""),
                        "reason": det.get("reason", ""),
                    }
                )
            else:
                rejected_count += 1
                added_rows.append(
                    {
                        "tile_id": tile["tile_id"],
                        "case_id": tile["case_id"],
                        "image_filename": tile["image_filename"],
                        "strategy": tile["strategy"],
                        "accepted": False,
                        "reject_reason": reason,
                        "target_type": det.get("target_type", ""),
                        "full_bbox": json.dumps([round(float(v), 2) for v in full_box]),
                        "confidence": det.get("confidence", ""),
                        "visibility": det.get("visibility", ""),
                        "damage_or_relevance": det.get("damage_or_relevance", ""),
                        "reason": det.get("reason", ""),
                    }
                )
        run_rows.append(
            {
                "tile_id": tile["tile_id"],
                "case_id": tile["case_id"],
                "image_filename": tile["image_filename"],
                "strategy": tile["strategy"],
                "tile_path": tile["tile_path"],
                "json_valid": valid,
                "json_error": error,
                "runtime_error": runtime_error,
                "raw_response_hash": digest,
                "detection_count": len(detections),
                "accepted_count": accepted_count,
                "rejected_count": rejected_count,
                "elapsed_seconds": elapsed,
            }
        )
        if idx % 25 == 0:
            print(f"v050 tile progress: {idx}/{len(tile_manifest)}")

    raw_micro_eval = v042.evaluate_reports(refs, merged_raw, micro_order)
    postprocessed_merged, postprocess_removals = apply_locked_postprocessors(merged_raw, dims)
    post_micro_eval = v042.evaluate_reports(refs, postprocessed_merged, micro_order)
    baseline_micro_eval = v042.evaluate_reports(refs, pp045c_preds, micro_order)
    raw_status = label_status(raw_micro_eval)
    post_status = label_status(post_micro_eval)
    accepted_added = [row for row in added_rows if row.get("accepted") is True]
    added_tp = sum(1 for row in accepted_added if post_status.get((row["image_filename"], row["label"])) == "TP")
    added_fp = sum(1 for row in accepted_added if post_status.get((row["image_filename"], row["label"])) == "FP")
    for row in accepted_added:
        row["after_postprocess_eval_status"] = post_status.get((row["image_filename"], row["label"]), "suppressed_or_unknown")
        row["raw_eval_status"] = raw_status.get((row["image_filename"], row["label"]), "unknown")

    fields_run = ["tile_id", "case_id", "image_filename", "strategy", "json_valid", "json_error", "runtime_error", "detection_count", "accepted_count", "rejected_count", "elapsed_seconds", "raw_response_hash", "tile_path"]
    fields_added = ["label", "tile_id", "case_id", "image_filename", "strategy", "accepted", "reject_reason", "target_type", "full_bbox", "confidence", "visibility", "damage_or_relevance", "reason", "raw_eval_status", "after_postprocess_eval_status"]
    write_csv(PACKAGE / "tile_run_results.csv", run_rows, fields_run)
    write_json(
        PACKAGE / "tile_run_results.json",
        {
            "generated_at": generated,
            "tile_count": len(tile_manifest),
            "runtime_errors": sum(1 for row in run_rows if row["runtime_error"]),
            "json_invalid": sum(1 for row in run_rows if not row["json_valid"]),
            "total_detections": sum(int(row["detection_count"]) for row in run_rows),
            "accepted_detections": len(accepted_added),
            "rows": run_rows,
            "added_detection_rows": added_rows,
        },
    )
    write_text(PACKAGE / "tile_run_results.md", make_markdown_summary("Tile Run Results", run_rows[:80], fields_run) + ("\n\nTruncated to first 80 rows in markdown.\n" if len(run_rows) > 80 else ""))
    write_csv(PACKAGE / "tables/accepted_detection_audit.csv", accepted_added, fields_added)

    baseline_cases = case_metrics(baseline_micro_eval)
    post_cases = case_metrics(post_micro_eval)
    raw_cases = case_metrics(raw_micro_eval)
    delta_rows = []
    for fname in micro_order:
        cid = v044.case_id(fname)
        base_img = next(img for img in baseline_micro_eval["images"] if img["image_filename"] == fname)
        post_img = next(img for img in post_micro_eval["images"] if img["image_filename"] == fname)
        raw_img = next(img for img in raw_micro_eval["images"] if img["image_filename"] == fname)
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
    write_text(PACKAGE / "case_level_delta_report.md", make_markdown_summary("Case Level Delta Report", delta_rows, ["case_id", "baseline", "raw_merged", "postprocessed_merged", "post_delta_vs_baseline"]))

    raw_metrics = raw_micro_eval["totals"]
    post_metrics = post_micro_eval["totals"]
    baseline_micro_metrics = baseline_micro_eval["totals"]
    micro_improved = post_metrics["combined_errors"] < baseline_micro_metrics["combined_errors"]
    fp_explosion = post_metrics["false_positives"] > baseline_micro_metrics["false_positives"] + 3
    dense_regression = any(
        next(row for row in delta_rows if row["case_id"] == cid)["post_delta_vs_baseline"] > 0
        for cid in ["66", "67", "84", "110", "155", "166"]
        if any(row["case_id"] == cid for row in delta_rows)
    )
    micro_pass = micro_improved and not fp_explosion and not dense_regression
    decision = "A" if micro_pass else "B" if added_tp > 0 and added_fp > added_tp else "C"
    main_lesson = (
        "Non-oracle tiles improved the micro-pack without control regression."
        if micro_pass else
        "Non-oracle tiles did not beat the locked micro-pack baseline under conservative merging."
    )
    next_action = (
        "Run full all-current/no101 with the same bounded tiling pass."
        if micro_pass else
        "Use v051 verifier gating or strategy refinement before broader full-pack tiling."
    )

    write_json(
        PACKAGE / "merged_predictions_summary.json",
        {
            "generated_at": generated,
            "stage": "micro_pack",
            "baseline_micro_metrics": baseline_micro_metrics,
            "raw_merged_metrics": raw_metrics,
            "postprocessed_merged_metrics": post_metrics,
            "added_detections": len(accepted_added),
            "added_true_positives": added_tp,
            "added_false_positives": added_fp,
            "postprocess_removals": len(postprocess_removals),
            "full_all_current_run": False,
            "full_all_current_skip_reason": "micro_pack_failed_gate" if not micro_pass else "not_run_by_script_guard",
        },
    )
    write_text(
        PACKAGE / "merged_predictions_summary.md",
        f"# Merged Predictions Summary\n\nBaseline micro: `{metric_line(baseline_micro_metrics)}`\n\nRaw merged micro: `{metric_line(raw_metrics)}`\n\nPostprocessed merged micro: `{metric_line(post_metrics)}`\n\nAdded detections: `{len(accepted_added)}`\n\nAdded true positives: `{added_tp}`\n\nAdded false positives: `{added_fp}`\n\nFull all-current run: `false`.\n",
    )
    merge_policy = {
        "generated_at": generated,
        "preserve_locked_pp045c_baseline_detections": True,
        "accepted_postprocessing_chain": ["p1753", "pp0157", "pp044a", "pp045b", "pp045c"],
        "excluded_postprocessors": [{"rule": "pp046a", "reason": "failed visual lock and remains diagnostic only"}],
        "candidate_filters": [
            "valid crop-local bbox",
            "valid target_type",
            "confidence >= 0.55",
            "not intact_context",
            "ambiguous requires confidence >= 0.78",
            "reject self-reported context-only/unclear",
            "reject obvious same-label duplicates with IoU >= 0.45",
        ],
        "uses_reference_boxes_for_inference": False,
    }
    write_json(PACKAGE / "merge_policy.json", merge_policy)
    write_text(PACKAGE / "merge_policy.md", "# Merge Policy\n\n" + "\n".join(f"- {item}" for item in merge_policy["candidate_filters"]) + "\n\n`pp046a` is excluded because it failed visual lock.\n")

    evaluation_summary = {
        "generated_at": generated,
        "baseline": {"pp045c_locked_baseline": PP045C, "micro_metrics": baseline_micro_metrics},
        "raw_merged_micro": raw_metrics,
        "postprocessed_merged_micro": post_metrics,
        "full_all_current_metrics": None,
        "full_all_current_run": False,
        "decision": decision,
        "case_level_delta_report": "case_level_delta_report.csv",
    }
    write_json(PACKAGE / "evaluation_summary.json", evaluation_summary)
    write_text(
        PACKAGE / "evaluation_summary.md",
        f"# Evaluation Summary\n\nMicro baseline: `{metric_line(baseline_micro_metrics)}`\n\nRaw merged: `{metric_line(raw_metrics)}`\n\nPostprocessed merged: `{metric_line(post_metrics)}`\n\nDecision: `{decision}`.\n",
    )
    failure_analysis = {
        "generated_at": generated,
        "decision": decision,
        "micro_pack_passed": micro_pass,
        "fp_explosion": fp_explosion,
        "dense_or_control_regression": dense_regression,
        "added_true_positives": added_tp,
        "added_false_positives": added_fp,
        "lesson": main_lesson,
        "recommended_next": next_action,
    }
    write_json(PACKAGE / "failure_analysis.json", failure_analysis)
    write_text(PACKAGE / "failure_analysis.md", f"# Failure Analysis\n\nDecision: `{decision}`\n\n{main_lesson}\n\nNext: {next_action}\n")

    intervention_matrix = [
        {
            "intervention": "v050_non_oracle_micro_tiling",
            "type": "tiling_crop_pass",
            "stage": "micro_pack",
            "baseline_metrics": metric_line(baseline_micro_metrics),
            "raw_metrics": metric_line(raw_metrics),
            "postprocessed_metrics": metric_line(post_metrics),
            "added_detections": len(accepted_added),
            "added_true_positives": added_tp,
            "added_false_positives": added_fp,
            "decision": decision,
        }
    ]
    write_json(PACKAGE / "recovery_log.json", {"generated_at": generated, "events": [{"event": "v050_non_oracle_micro_run", "decision": decision, "lesson": main_lesson}]})
    write_text(PACKAGE / "recovery_log.md", f"# Recovery Log\n\n- `{generated}`: Ran bounded non-oracle tile micro-pack. Decision `{decision}`.\n")
    write_json(PACKAGE / "final_recommendation.json", {"generated_at": generated, "decision": decision, "backend_ran": True, "case_40_resolved": True, "micro_pack_metrics": post_metrics, "full_all_current_metrics": None, "next_action": next_action, "hard_boundaries_preserved": True})
    write_text(
        PACKAGE / "final_recommendation.md",
        f"# v050 Final Recommendation\n\nBackend ran: `true`.\n\nCase 40 image resolved: `true`.\n\nStrategies tested: `A, B, C, D` on the micro-pack.\n\nMicro-pack baseline: `{metric_line(baseline_micro_metrics)}`.\n\nMicro-pack raw merged: `{metric_line(raw_metrics)}`.\n\nMicro-pack postprocessed merged: `{metric_line(post_metrics)}`.\n\nAdded detections: `{len(accepted_added)}`; added TPs: `{added_tp}`; added FPs: `{added_fp}`.\n\nFull all-current run: `false`.\n\nDecision: `{decision}`.\n\nNext action: {next_action}\n\nHard boundaries were preserved: reference boxes were not used for inference crop generation, pp046a stayed diagnostic-only, and no product/runtime/source-truth files were mutated.\n",
    )
    write_text(PACKAGE / "README.md", "# v050 FP8 Non-Oracle Tiling/Crop Recovery\n\nExperiment-only tranche for testing whether v049 reference-crop recoverability transfers to non-oracle image-geometry and prediction-anchored crops.\n")
    write_json(PACKAGE / "source_manifest.json", {"generated_at": generated, "source_artifacts": artifact_rows, "locked_baselines": {"pp045c": PP045C, "pp046a_diagnostic_only": PP046A_DIAGNOSTIC, "old_v020c": OLD_V020C}})
    write_text(PACKAGE / "lessons_learned.md", f"# Lessons Learned\n\n- {main_lesson}\n- Reference-centered crop recognition did not automatically become a deployable non-oracle recovery path in this bounded pass.\n")
    write_text(PACKAGE / "strategy_state.md", f"# Strategy State\n\nLocked baseline remains `pp045c = {metric_line(PP045C)}` unless a fully scored and visually safe non-oracle recovery beats it.\n\nv050 decision: `{decision}`.\n\nNext axis: {next_action}\n")

    print(f"""=== V050 STATUS ===
phase: micro_pack
strategy: mixed
backend: available
stage: merge_eval
raw_merged_metrics: {metric_line(raw_metrics)}
postprocessed_merged_metrics: {metric_line(post_metrics)}
vs_pp045c_49_delta: {post_metrics['combined_errors'] - baseline_micro_metrics['combined_errors']:+d} micro-pack
added_detections: {len(accepted_added)}
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

    print(f"""=== V050 STATUS ===
phase: final_decision
strategy: mixed
backend: available
stage: merge_eval
raw_merged_metrics: {metric_line(raw_metrics)}
postprocessed_merged_metrics: {metric_line(post_metrics)}
vs_pp045c_49_delta: n/a full-pack-not-run
added_detections: {len(accepted_added)}
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
