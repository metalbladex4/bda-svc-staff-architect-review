"""Tests for BDA matching behavior."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import models
import numpy as np


def _target(
    label: str,
    xmin: int,
    ymin: int,
    xmax: int,
    ymax: int,
) -> models.BDATarget:
    """Create a minimal target for matching tests."""
    return models.BDATarget(
        target_label=label,
        target_type=models.TargetType.MILITARY_EQUIPMENT,
        damage_category=models.DamageMilitaryEquipment.DESTROYED,
        confidence=models.Confidence.PROBABLE,
        logic="test",
        box=models.BoundingBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax),
        ndarray=np.array(
            [
                models.TargetType.MILITARY_EQUIPMENT,
                models.DamageMilitaryEquipment.DESTROYED,
                models.Confidence.PROBABLE,
            ]
        ),
    )


def _report(image_filename: str, target: models.BDATarget) -> models.BDAReport:
    """Create a minimal BDA report for matching tests."""
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


def test_get_bda_matches_skips_logic_without_api_key(monkeypatch) -> None:
    """Matching should still succeed when LLMaaJ credentials are unavailable."""
    monkeypatch.delenv("OLLAMA_API_KEY", raising=False)

    reference = _report("tank.jpg", _target("target_0", 51, 37, 102, 73))
    predicted = _report("tank.jpg", _target("target_0", 51, 37, 102, 73))

    result = predicted.get_bda_matches(reference)

    assert result is not None
    matches, false_negatives, false_positives = result
    assert len(matches) == 1
    assert matches[0].score_logic == 0
    assert matches[0].score == matches[0].score_assess * matches[0].w_assess
    assert false_negatives == []
    assert false_positives == []
