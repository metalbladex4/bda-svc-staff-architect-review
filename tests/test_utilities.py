"""Pipeline utility tests."""

import pytest
from PIL import Image

from bda_svc.pipeline import utilities
from bda_svc.pipeline.interfaces import Detection
from bda_svc.pipeline.utilities import (
    bbox_from_1000,
    crop_with_buffer,
    draw_box_overlay,
    load_yaml,
    nms,
    parse_json,
)


def test_load_yaml_reads_dict(tmp_path) -> None:
    """load_yaml should load YAML into a Python dictionary."""
    yaml_path = tmp_path / "sample.yaml"
    yaml_path.write_text("a: 1\nb: test\n", encoding="utf-8")
    data = load_yaml(yaml_path)
    assert data == {"a": 1, "b": "test"}


def test_parse_json_repairs_simple_invalid_json() -> None:
    """parse_json should repair simple malformed JSON."""
    dict_payload = parse_json("{'a': 1}")
    list_payload = parse_json("[{'a': 1}]")
    assert dict_payload == {"a": 1}
    assert list_payload == [{"a": 1}]


def test_parse_json_raises_for_unparseable_text() -> None:
    """parse_json should raise ValueError if cannot parse response."""
    with pytest.raises(ValueError):
        parse_json("this is not json at all")


def test_format_pda_doctrine_formats_selected_category(monkeypatch) -> None:
    """Format doctrine text for one selected category."""
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
    output = utilities.format_pda_doctrine(["buildings"])
    assert "TARGET CATEGORY: BUILDINGS" in output
    assert "BUILDINGS PHYSICAL DAMAGE DEFINITIONS" in output
    assert "BUILDINGS PHYSICAL DAMAGE CONSIDERATIONS" in output
    assert "Building definitions." in output
    assert "Building considerations." in output
    assert "TARGET CATEGORY: MILITARY EQUIPMENT" not in output


def test_format_pda_doctrine_returns_fallback_for_unknown_category(monkeypatch) -> None:
    """Return fallback text when requested categories are missing."""
    fake_doctrine = {"buildings": {"physical_damage_definitions": "x"}}
    monkeypatch.setattr(utilities, "load_yaml", lambda path: fake_doctrine)
    output = utilities.format_pda_doctrine(["not_a_real_category"])
    assert output == "NO TARGET DOCTRINE AVAILABLE."


def test_bbox_from_1000_converts_bbox_to_pixels() -> None:
    """bbox_from_1000 should scale coordinates to pixel space."""
    image = Image.new("RGB", (100, 50))
    bbox = bbox_from_1000(image, [100, 100, 500, 900])
    assert bbox == (10, 5, 50, 45)


def test_bbox_from_1000_returns_none_for_wrong_length() -> None:
    """Return None when bbox does not have four values."""
    image = Image.new("RGB", (100, 50))
    assert bbox_from_1000(image, [100, 100, 500]) is None


def test_bbox_from_1000_returns_none_for_out_of_range_values() -> None:
    """Return None when bbox values are outside 0-1000 range."""
    image = Image.new("RGB", (100, 50))
    assert bbox_from_1000(image, [-1, 100, 500, 900]) is None
    assert bbox_from_1000(image, [100, 100, 1001, 900]) is None


def test_bbox_from_1000_returns_none_for_invalid_box_order() -> None:
    """Return None when xmin/xmax or ymin/ymax ordering is invalid."""
    image = Image.new("RGB", (100, 50))
    assert bbox_from_1000(image, [500, 100, 100, 900]) is None
    assert bbox_from_1000(image, [100, 900, 500, 100]) is None


def test_crop_with_buffer_adds_padding() -> None:
    """crop_with_buffer should enlarge crop using ratio padding."""
    image = Image.new("RGB", (100, 100))
    crop = crop_with_buffer(image, (10, 10, 30, 30), buffer_ratio=0.5)
    assert crop.size == (40, 40)


def test_draw_box_overlay_preserves_image_size() -> None:
    """draw_box_overlay should not change image dimensions."""
    image = Image.new("RGB", (64, 32))
    overlay = draw_box_overlay(image, (10, 5, 20, 15))
    assert overlay.size == image.size


def test_nms_suppresses_same_label_overlap() -> None:
    """NMS should keep only the top-score box for same-label overlap."""
    detections = [
        Detection(label="military_equipment", score=0.9, box=(10, 10, 40, 40)),
        Detection(label="military_equipment", score=0.8, box=(12, 12, 42, 42)),
    ]
    filtered = nms(detections, iou_threshold=0.5)
    assert len(filtered) == 1
    assert filtered[0].score == 0.9


def test_nms_keeps_overlaps_for_different_labels() -> None:
    """NMS should keep overlapping boxes when labels differ."""
    detections = [
        Detection(label="military_equipment", score=0.9, box=(10, 10, 40, 40)),
        Detection(label="buildings", score=0.8, box=(12, 12, 42, 42)),
    ]
    filtered = nms(detections, iou_threshold=0.5)
    assert len(filtered) == 2
