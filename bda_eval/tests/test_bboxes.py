"""Tests for bbox artifact generation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import bboxes
import config
import models
from PIL import Image


def _target(
    label: str,
    xmin: int,
    ymin: int,
    xmax: int,
    ymax: int,
) -> models.BDATarget:
    """Create a minimal target for bbox tests."""
    return models.BDATarget(
        target_label=label,
        target_type=models.TargetType.MILITARY_EQUIPMENT,
        damage_category=models.DamageMilitaryEquipment.DESTROYED,
        confidence=models.Confidence.PROBABLE,
        logic="test",
        box=models.BoundingBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax),
        ndarray=[],
    )


def _report(image_filename: str, target: models.BDATarget) -> models.BDAReport:
    """Create a minimal BDA report for bbox tests."""
    metadata = models.BDAReportMetadata(
        model_name="test-model",
        image_id="test-image-id",
        image_filename=image_filename,
        date_created="2026-04-15T00:00:00Z",
        report_type="PDA",
        analyst="pytest",
        inference_time="1.23",
    )
    return models.BDAReport(metadata=metadata, targets=[target])


def test_draw_bboxes_emits_review_artifacts(tmp_path: Path) -> None:
    """draw_bboxes should emit overlays, crops, and review sheets."""
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    img_path = image_dir / "tank.jpg"
    Image.new("RGB", (256, 122), color="white").save(img_path)

    output_dir = tmp_path / "results"
    config.IMAGES_DIR = image_dir
    config.OUTPUT_DIR = output_dir
    config.REFERENCE_DIR = Path("baseline")
    config.PREDICTED_DIR = Path("candidate")
    config.REFERENCE_LABEL = "Baseline"
    config.PREDICTED_LABEL = "Candidate"
    config.CROP_BUFFER_RATIO = 0.2

    reference = _report("tank.jpg", _target("target_0", 51, 37, 128, 73))
    predicted = _report("tank.jpg", _target("target_0", 46, 46, 128, 92))

    bboxes.draw_bboxes(
        img_filename="tank.jpg",
        R_report=reference,
        P_report=predicted,
        write_root_review_sheet=True,
    )

    assert (output_dir / "images_bbox_both" / "bbox_tank.jpg").exists()
    assert (output_dir / "images_bbox_reference" / "bbox_tank.jpg").exists()
    assert (output_dir / "images_bbox_predicted" / "bbox_tank.jpg").exists()
    assert (output_dir / "images_crop_reference" / "crop_tank.jpg").exists()
    assert (output_dir / "images_crop_predicted" / "crop_tank.jpg").exists()
    assert (output_dir / "images_bbox_review" / "bbox_review_tank.jpg").exists()
    assert (output_dir / "bbox_review_sheet.jpg").exists()
