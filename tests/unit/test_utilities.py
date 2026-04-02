"""Pipeline utility tests."""

from PIL import Image

from bda_svc.pipeline import utilities
from bda_svc.pipeline.utilities import (
    bbox_to_pixels,
    crop_with_buffer,
    draw_box_overlay,
    format_detection_doctrine,
    format_pda_doctrine,
    load_yaml,
    resize_for_vlm,
)


def test_load_yaml_reads_dict(tmp_path) -> None:
    """load_yaml should load YAML into a Python dictionary."""
    yaml_path = tmp_path / "sample.yaml"
    yaml_path.write_text("a: 1\nb: test\n", encoding="utf-8")
    data = load_yaml(yaml_path)
    assert data == {"a": 1, "b": "test"}


def test_format_detection_doctrine_includes_selected_categories(monkeypatch) -> None:
    """Format detection guidance for configured doctrinal categories."""
    fake_doctrine = {
        "buildings": {"detection_guidance": "Relevant buildings only."},
        "military_equipment": {"detection_guidance": "All relevant equipment."},
    }
    monkeypatch.setattr(utilities, "load_yaml", lambda path: fake_doctrine)
    output = format_detection_doctrine(["buildings", "military_equipment"])
    assert "buildings:" in output
    assert "Relevant buildings only." in output
    assert "military_equipment:" in output
    assert "All relevant equipment." in output


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
    output = format_pda_doctrine("buildings")
    assert "BUILDINGS PHYSICAL DAMAGE DEFINITIONS" in output
    assert "BUILDINGS PHYSICAL DAMAGE CONSIDERATIONS" in output
    assert "Building definitions." in output
    assert "Building considerations." in output
    assert "MILITARY EQUIPMENT PHYSICAL DAMAGE DEFINITIONS" not in output


def test_format_pda_doctrine_returns_fallback_for_unknown_category(monkeypatch) -> None:
    """Return fallback text when requested categories are missing."""
    fake_doctrine = {"buildings": {"physical_damage_definitions": "x"}}
    monkeypatch.setattr(utilities, "load_yaml", lambda path: fake_doctrine)
    output = format_pda_doctrine("not_a_real_category")
    assert output == "NO TARGET DOCTRINE AVAILABLE."


def test_bbox_to_pixels_converts_xyxy_1000_bbox() -> None:
    """bbox_to_pixels should scale the xyxy 0-1000 coordinates."""
    image = Image.new("RGB", (100, 50))
    bbox = bbox_to_pixels(image, image, [100, 100, 500, 900], "xyxy_1000")
    assert bbox == (10, 5, 50, 45)


def test_bbox_to_pixels_converts_yxyx_1000_bbox() -> None:
    """bbox_to_pixels should scale the yxyx 0-1000 coordinates."""
    image = Image.new("RGB", (100, 50))
    bbox = bbox_to_pixels(image, image, [100, 100, 900, 500], "yxyx_1000")
    assert bbox == (10, 5, 50, 45)


def test_bbox_to_pixels_converts_xyxy_1_bbox() -> None:
    """bbox_to_pixels should scale the xyxy 0.0-1.0 coordinates."""
    image = Image.new("RGB", (100, 50))
    bbox = bbox_to_pixels(image, image, [0.1, 0.1, 0.5, 0.9], "xyxy_1")
    assert bbox == (10, 5, 50, 45)


def test_bbox_to_pixels_converts_yxyx_1_bbox() -> None:
    """bbox_to_pixels should scale the yxyx 0.0-1.0 coordinates."""
    image = Image.new("RGB", (100, 50))
    bbox = bbox_to_pixels(image, image, [0.1, 0.1, 0.9, 0.5], "yxyx_1")
    assert bbox == (10, 5, 50, 45)


def test_bbox_to_pixels_returns_none_for_invalid_input() -> None:
    """Return None when bbox input is malformed or out of range."""
    image = Image.new("RGB", (100, 50))
    assert bbox_to_pixels(image, image, [100, 100, 500], "xyxy_1000") is None
    assert bbox_to_pixels(image, image, [-1, 100, 500, 900], "xyxy_1000") is None
    assert bbox_to_pixels(image, image, [100, 100, 1001, 900], "xyxy_1000") is None
    assert bbox_to_pixels(image, image, [500, 100, 100, 900], "xyxy_1000") is None
    assert bbox_to_pixels(image, image, [100, 900, 500, 100], "xyxy_1000") is None


def test_crop_with_buffer_adds_padding() -> None:
    """crop_with_buffer should enlarge crop using ratio padding."""
    image = Image.new("RGB", (100, 100))
    crop = crop_with_buffer(image, (10, 10, 30, 30), buffer_ratio=0.5)
    assert crop.size == (40, 40)


def test_resize_for_vlm_returns_original_size_within_limit() -> None:
    """Images within the limit should be returned unchanged in size."""
    image = Image.new("RGB", (800, 600))
    resized = resize_for_vlm(image, 1024)
    assert resized.size == (800, 600)


def test_resize_for_vlm_preserves_aspect_ratio() -> None:
    """Large images should be downscaled while preserving aspect ratio."""
    image = Image.new("RGB", (4000, 2000))
    resized = resize_for_vlm(image, 1024)
    assert resized.size == (1024, 512)


def test_draw_box_overlay_preserves_image_size() -> None:
    """draw_box_overlay should not change image dimensions."""
    image = Image.new("RGB", (64, 32))
    overlay = draw_box_overlay(image, (10, 5, 20, 15))
    assert overlay.size == image.size
