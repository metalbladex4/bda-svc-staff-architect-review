"""Export utilities."""

import csv
import datetime
from pathlib import Path

import config
import models

# Define the order of columns
CSV_HEADERS_TARGETS = [
    "image_filename",
    "model_name",
    "inference_time",
    "target_type",
    "ref_target_label",
    "pred_target_label",
    "ref_damage",
    "pred_damage",
    "ref_confidence",
    "pred_confidence",
    "iou_score",
    # "w_d",
    # "w_c",
    "d_cost",
    "c_cost",
    "cost",
    "score_assess",
    "score_logic",
    # "w_assess",
    # "w_logic",
    "score",
    "match_status",
]


CSV_HEADERS_MODEL = [
    "model_name",
    "count_target",
    "count_fn",
    "count_fp",
    "inference_time_avg",
    "assess_avg",
    "logic_avg",
    "total_avg",
]


def _build_row_target(
    report_pred: models.BDAReport,
    match_status: str,
    match: models.BDAMatch | None = None,
    ref_target: models.BDATarget | None = None,
    pred_target: models.BDATarget | None = None,
) -> dict:
    """Helper function to create a CSV row (as dictionary).

    Args:
        report_pred: BDAReport to extract metadata
        match_status: One of (TP, FN, FP)
        match: BDAMatch object
        ref_target: Within a matched tuple, the reference BDATarget
        pred_target: Within a matched tuple, the predicted BDATarget

    Returns:
        Dictionary representing a CSV row
    """
    # Extract data from match (i.e. True Positive)
    if match:
        ref = match.ref_target
        pred = match.pred_target
        iou = f"{match.iou:.3f}"
        # w_d = f"{match.w_d:.3f}"
        # w_c = f"{match.w_c:.3f}"
        d_cost = f"{match.d_cost:.3f}"
        c_cost = f"{match.c_cost:.3f}"
        cost = f"{match.cost:.3f}"
        s_assess = f"{match.score_assess:.3f}"
        s_logic = f"{match.score_logic:.3f}"
        # w_assess = f"{match.w_assess:.3f}"
        # w_logic = f"{match.w_logic:.3f}"
        score = f"{match.score:.3f}"
    else:
        # Handle False Positives and False Negatives
        ref = ref_target
        pred = pred_target
        cost = iou = d_cost = c_cost = s_assess = s_logic = score = ""

    # Exit early if both ref and pred targets are missing
    if ref is not None:
        active_target = ref
    elif pred is not None:
        active_target = pred
    else:
        raise ValueError("[*] Unable to build row. Both targets are None")

    return {
        "image_filename": report_pred.metadata.image_filename,
        "model_name": report_pred.metadata.model_name,
        "inference_time": report_pred.metadata.inference_time,
        "target_type": active_target.target_type.text,
        "ref_target_label": ref.target_label if ref else "",
        "ref_damage": ref.damage_category if ref else "",
        "pred_target_label": pred.target_label if pred else "",
        "pred_damage": pred.damage_category if pred else "",
        "ref_confidence": ref.confidence if ref else "",
        "pred_confidence": pred.confidence if pred else "",
        "iou_score": iou,
        # "w_d": w_d,
        # "w_c": w_c,
        "d_cost": d_cost,
        "c_cost": c_cost,
        "cost": cost,
        "score_assess": s_assess,
        "score_logic": s_logic,
        # "w_assess": w_assess,
        # "w_logic": w_logic,
        "score": score,
        "match_status": match_status,
    }


def package_bda_report(
    report_pred: models.BDAReport,
    matches: list[models.BDAMatch],
    false_negatives: list[models.BDATarget],
    false_positives: list[models.BDATarget],
) -> list[dict]:
    """Consolidate evaluation results into a single object.

    Args:
        report_pred: Predicted BDA report
        matches: List of BDAMatch objects
        false_negatives: List of False Negative BDATargets
        false_positives: List of False Positive BDATargets

    Returns:
        List of CSV rows (each row representing an evaluation result)
    """
    rows = []

    for match in matches:
        rows.append(_build_row_target(report_pred, "TP", match=match))

    for fn in false_negatives:
        rows.append(_build_row_target(report_pred, "FN", ref_target=fn))

    for fp in false_positives:
        rows.append(_build_row_target(report_pred, "FP", pred_target=fp))

    return rows


def save_csv(
    filename: str, rows: list[dict], headers: list[str] = CSV_HEADERS_TARGETS
) -> Path | None:
    """Save evaluation report as CSV file.

    Args:
        filename: String to prepend to filename of generated CSV
        rows: List of evaluation results (dictionaries) to be written to CSV
        headers: List of header strings

    Returns:
        Path of written evaluation report (or None)
    """
    if not rows:
        return None

    timestamp = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d_%H%M%SZ")
    assert config.OUTPUT_DIR is not None, "[*] Output directory not initialized."
    csv_path = config.OUTPUT_DIR / f"{filename}_{timestamp}.csv"

    try:
        with csv_path.open("w", encoding="utf-8", newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=headers)

            csv_writer.writeheader()
            csv_writer.writerows(rows)

        return csv_path
    except (OSError, ValueError, csv.Error) as e:
        print(f"\n[*] Unable to write CSV file ({e})")
        return None
