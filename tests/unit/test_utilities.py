"""Pipeline utility tests."""

import pytest
from PIL import Image

from bda_svc.pipeline import utilities
from bda_svc.pipeline.utilities import (
    bbox_to_pixels,
    crop_with_buffer,
    format_detection_doctrine,
    format_pda_doctrine,
    load_yaml,
    resize_for_vlm,
)

# ----------------------------------------------------------------------
# YAML load into dictionary test
# ----------------------------------------------------------------------


def test_load_yaml_reads_dict(tmp_path) -> None:
    """load_yaml should load YAML into a Python dictionary."""
    yaml_path = tmp_path / "sample.yaml"
    yaml_path.write_text("a: 1\nb: test\n", encoding="utf-8")
    data = load_yaml(yaml_path)
    assert data == {"a": 1, "b": "test"}


# ----------------------------------------------------------------------
# Prompt formatting tests
# ----------------------------------------------------------------------


def test_format_detection_doctrine(monkeypatch: pytest.MonkeyPatch) -> None:
    """Detection guidance should only contain valid categories."""
    fake_doctrine = {
        "buildings": {
            "detection_guidance": "Detect buildings.",
        },
        "military_equipment": {
            "detection_guidance": "Detect military equipment.",
        },
    }

    monkeypatch.setattr(utilities, "load_yaml", lambda path: fake_doctrine)
    output = format_detection_doctrine(["buildings", "military_equipment", "trenches"])

    # 'buildings' and 'military_equipment' have entries in fake_doctrine
    assert "buildings" in output
    assert "Detect buildings." in output
    assert "military_equipment" in output
    assert "Detect military equipment." in output
    # 'trenches' does not have an entry in fake_doctrine and should be skipped
    assert "trenches" not in output


def test_format_pda_doctrine(monkeypatch: pytest.MonkeyPatch) -> None:
    """Doctrine output should contain only one category."""
    fake_doctrine = {
        "buildings": {
            "physical_damage_definitions": "Building definitions.",
            "physical_damage_considerations": "Building considerations.",
        },
        "military_equipment": {
            "physical_damage_definitions": "Equipment definitions.",
            "physical_damage_considerations": "Equipment considerations.",
        },
    }

    monkeypatch.setattr(utilities, "load_yaml", lambda path: fake_doctrine)
    output = format_pda_doctrine("buildings")

    # 'buildings' definitions and considerations should be in output
    assert "BUILDINGS PHYSICAL DAMAGE DEFINITIONS" in output
    assert "Building definitions." in output
    assert "BUILDINGS PHYSICAL DAMAGE CONSIDERATIONS" in output
    assert "Building considerations." in output
    # 'military_equipment' should not be in output
    assert "MILITARY EQUIPMENT" not in output


def test_format_pda_doctrine_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    """Doctrine output should provide fallback for missing category."""
    fake_doctrine = {}

    monkeypatch.setattr(utilities, "load_yaml", lambda path: fake_doctrine)
    output = format_pda_doctrine("not_a_real_category")

    # Should return fallback text for invalid category
    assert output == "NO TARGET DOCTRINE AVAILABLE."


# ----------------------------------------------------------------------
# Bounding box conversion to image pixel space tests
# ----------------------------------------------------------------------


def test_bbox_to_pixels_converts_xyxy_1000_bbox() -> None:
    """Convert xyxy 0-1000 bbox coordinates to image pixels."""
    image = Image.new("RGB", (100, 50))
    bbox = bbox_to_pixels(image, image, [100, 100, 500, 900], "xyxy_1000")
    assert bbox == (10, 5, 50, 45)


def test_bbox_to_pixels_converts_yxyx_1000_bbox() -> None:
    """Convert yxyx 0-1000 bbox coordinates to image pixels."""
    image = Image.new("RGB", (100, 50))
    bbox = bbox_to_pixels(image, image, [100, 100, 900, 500], "yxyx_1000")
    assert bbox == (10, 5, 50, 45)


def test_bbox_to_pixels_returns_none_for_invalid_bbox() -> None:
    """Return None for malformed or invalid bounding boxes."""
    image = Image.new("RGB", (100, 50))
    # All failure modes should fail safely and return None
    assert bbox_to_pixels(image, image, [100, 100, 500], "xyxy_1000") is None
    assert bbox_to_pixels(image, image, [100, 100, "900,", 500], "xyxy_1000") is None
    assert bbox_to_pixels(image, image, [100, 100, 900, 500], "xy_xy_1000") is None
    assert bbox_to_pixels(image, image, [-1, 100, 500, 900], "xyxy_1000") is None
    assert bbox_to_pixels(image, image, [100, 100, 1001, 900], "xyxy_1000") is None
    assert bbox_to_pixels(image, image, [500, 100, 100, 900], "xyxy_1000") is None


# ----------------------------------------------------------------------
# Crop with buffer tests
# ----------------------------------------------------------------------


def test_crop_with_buffer_adds_padding() -> None:
    """Add padding around the detection box."""
    image = Image.new("RGB", (100, 100))
    crop = crop_with_buffer(image, (10, 10, 30, 30), buffer_ratio=0.5)
    # Happy path returns correct padding
    assert crop.size == (40, 40)


def test_crop_with_buffer_enforces_minimum_size() -> None:
    """Return at least the minimum crop size for very small boxes."""
    image = Image.new("RGB", (100, 100))
    crop = crop_with_buffer(image, (10, 10, 12, 12), buffer_ratio=0.0, min_size=32)
    # VLMs need a minimum size image, very small crops should satisfy this requirement
    assert crop.size == (32, 32)


# ----------------------------------------------------------------------
# Resize image tests
# ----------------------------------------------------------------------


def test_resize_for_vlm_keeps_small_images_unchanged() -> None:
    """Keep smaller images at their original size."""
    image = Image.new("RGB", (800, 600))
    resized = resize_for_vlm(image, 1024)
    # If an image is below the maximum size, do not change it
    assert resized.size == (800, 600)


def test_resize_for_vlm_downsizes_large_images() -> None:
    """Downsize larger images while keeping their aspect ratio."""
    image = Image.new("RGB", (4000, 2000))
    resized = resize_for_vlm(image, 1024)
    # If an image is above the maximum size, resize it proportionally
    assert resized.size == (1024, 512)
