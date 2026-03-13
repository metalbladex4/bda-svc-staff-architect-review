"""Export utilities."""

import csv
import datetime
from pathlib import Path

import models


CSV_HEADERS = [
    "image_filename",
    "model_name",
    "target_type",
    "ref_target_label",
    "pred_target_label",
    "ref_damage",
    "pred_damage",
    "ref_confidence",
    "pred_confidence",
    "iou_score",
    "cost",
    "match_status"
]


def _build_row(
    report_pred: models.BDAReport,
    match_status: str,
    ref_target: models.BDATarget | None = None,
    pred_target: models.BDATarget | None = None,
    cost: float | str = "",
    iou: float | str = ""
) -> dict:
    """Helper function to create a CSV row (as dictionary).
    
    Args:
        report_pred: BDAReport to extract metadata
        match_status: One of (TP, FN, FP)
        ref_target: Within a matched tuple, the reference BDATarget
        pred_target: Within a matched tuple, the predicted BDATarget
        cost: Cost calculated by Hungarian Algorithm (for matched targets)
        iou: IoU calculation (for matched targets)
    
    Returns:
        Dictionary representing a CSV row
    """
    # Exit early if both ref and pred targets are missing
    if ref_target is not None:
        active_target = ref_target
    elif pred_target is not None:
        active_target = pred_target
    else:
        return {}

    return {
        "image_filename": report_pred.metadata.image_filename,
        "model_name": report_pred.metadata.model_name,
        "target_type": active_target.target_type.text,
        "ref_target_label": ref_target.target_label if ref_target else "",
        "ref_damage": ref_target.damage_category.text if ref_target else "",
        "pred_target_label": pred_target.target_label if pred_target else "",
        "pred_damage": pred_target.damage_category.text if pred_target else "",
        "ref_confidence": ref_target.confidence.text if ref_target else "",
        "pred_confidence": pred_target.confidence.text if pred_target else "",
        "cost": str(cost) if cost != "" else "",
        "iou_score": str(iou) if iou != "" else "",
        "match_status": match_status        
    }


def package_bda_report(
    #report_ref: models.BDAReport,
    report_pred: models.BDAReport,
    matches: list[models.BDAMatch],
    false_negatives: list[models.BDATarget],
    false_positives: list[models.BDATarget]
) -> list[dict]:
    """Consolidate evaluation results into a single object.
    
    Args:
        report_ref: Reference BDA report
        report_pred: Predicted BDA report
        matches: List of BDAMatch objects

    Returns:
        List of CSV rows (each row representing an evaluation result)
    """
    rows = []

    for match in matches:
        rows.append(_build_row(
            report_pred=report_pred,
            match_status="TP",
            ref_target=match.ref_target,
            pred_target=match.pred_target,
            cost=match.cost,
            iou=match.iou
        ))

    for fn in false_negatives:
        rows.append(_build_row(
            report_pred=report_pred,
            match_status="FN",
            ref_target=fn
        ))

    for fp in false_positives:
        rows.append(_build_row(
            report_pred=report_pred,
            match_status="FP",
            pred_target=fp
        ))

    return rows


def save_csv(
    rows: list[dict],
    output_path: str | Path,
) -> Path | None:
    """Save evaluation report as CSV file.
    
    Args:
        rows: List of evaluation results (dictionaries) to be written to CSV
        output_path : Path of output folder
    
    Returns:
        Path of written evaluation report (or None)
    """
    if not rows:
        return None

    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d_%H%M%SZ")
    csv_path = output_path / f"evaluation_{timestamp}.csv"

    try:
        with csv_path.open("w", encoding="utf-8", newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)

            csv_writer.writeheader()
            csv_writer.writerows(rows)
            
        return csv_path
    except (OSError, ValueError, csv.Error):
        return None
