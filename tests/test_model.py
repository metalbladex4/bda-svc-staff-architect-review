"""Pipeline model tests."""

import json

import pytest
from PIL import Image

from bda_svc.pipeline import model as pipeline_model
from bda_svc.pipeline.interfaces import BaseDetector, BaseVLM, Detection

# ---------------------------------------------------------------------------
# Test Setup: Create fake backends
# ---------------------------------------------------------------------------


class FakeVLM(BaseVLM):
    """Fake VLM that returns scripted responses."""

    def __init__(self, responses: list[str] | None = None) -> None:
        """Store scripted responses."""
        self.responses = list(responses or [])
        self.calls: list[dict] = []

    def generate(
        self,
        image: Image.Image | list[Image.Image],
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        """Return next scripted response and record the call."""
        if isinstance(image, list):
            image_size = [img.size for img in image]
        else:
            image_size = image.size
        self.calls.append(
            {
                "image_size": image_size,
                "prompt": prompt,
                "system_prompt": system_prompt,
            }
        )
        return self.responses.pop(0)


class FakeDetector(BaseDetector):
    """Fake detector that returns scripted detections."""

    def __init__(self, detections: list[Detection] | None = None) -> None:
        """Store scripted detections."""
        self.detections = list(detections or [])
        self.calls: list[list[str]] = []

    def detect(self, image: Image.Image, categories: list[str]) -> list[Detection]:
        """Return scripted detections and record category input."""
        self.calls.append(list(categories))
        return list(self.detections)


# ---------------------------------------------------------------------------
# Test Setup: Config and doctrine fixtures
# ---------------------------------------------------------------------------


def make_config(
    detection_provider: str = "detector",
    crop_buffer_ratio: float = 0.10,
) -> dict:
    """Return minimal config for model tests."""
    return {
        "pipeline": {
            "detection_provider": detection_provider,
            "crop_buffer_ratio": crop_buffer_ratio,
        },
        "vlm": {
            "family": "qwen3",
            "model_id": "Qwen/Qwen3-VL-8B-Instruct-FP8",
            "load_local": True,
            "max_new_tokens": 128,
        },
        "detector": {
            "family": "grounding_dino",
            "model_id": "IDEA-Research/grounding-dino-base",
            "load_local": True,
            "threshold": 0.25,
            "nms_threshold": 0.50,
            "label_map": {
                "buildings": ["building"],
                "military_equipment": ["military equipment", "tank"],
            },
        },
        "prompts": {
            "system": "system prompt",
            "detect_objects": "Detect objects from: {categories}",
            "assess_damage": "Assess {target_type}\n{doctrine}",
        },
    }


@pytest.fixture
def doctrine() -> dict:
    """Small doctrine fixture for model tests."""
    return {
        "buildings": {"physical_damage_definitions": "building doctrine"},
        "military_equipment": {"physical_damage_definitions": "equipment doctrine"},
    }


# ---------------------------------------------------------------------------
# Test Setup: Monkeypatch backend builders and config/doctrine
# ---------------------------------------------------------------------------


def patch_backends(
    monkeypatch: pytest.MonkeyPatch,
    vlm: BaseVLM | None = None,
    detector: BaseDetector | None = None,
) -> None:
    """Patch `build_vlm` and `build_detector` in pipeline."""
    if vlm is not None:
        monkeypatch.setattr(pipeline_model, "build_vlm", lambda cfg: vlm)
    if detector is not None:
        monkeypatch.setattr(pipeline_model, "build_detector", lambda cfg: detector)


def patch_config(monkeypatch: pytest.MonkeyPatch, config: dict, doctrine: dict) -> None:
    """Patch `load_yaml` in pipeline."""

    def fake_load_yaml(path):
        if path == pipeline_model.CONFIG_PATH:
            return config
        if path == pipeline_model.DOCTRINE_PATH:
            return doctrine

    monkeypatch.setattr(pipeline_model, "load_yaml", fake_load_yaml)


# ---------------------------------------------------------------------------
# Test Suite
# ---------------------------------------------------------------------------


def test_init_detector_mode_builds_detector(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict
) -> None:
    """Confirm detector mode is active."""
    config = make_config(detection_provider="detector")
    patch_config(monkeypatch, config, doctrine)
    patch_backends(monkeypatch, vlm=FakeVLM())
    pipeline = pipeline_model.BDAPipeline()
    assert pipeline.detection_provider == "detector"


def test_init_vlm_mode_skips_detector(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict
) -> None:
    """VLM mode should not create a detector."""
    config = make_config(detection_provider="vlm")
    patch_config(monkeypatch, config, doctrine)
    patch_backends(monkeypatch, vlm=FakeVLM(), detector=FakeDetector())
    pipeline = pipeline_model.BDAPipeline()
    assert pipeline.detector is None


def test_detect_objects_detector_mode_passes_doctrine_categories(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict
) -> None:
    """Pass doctrine categories to detector.detect in detector mode."""
    config = make_config(detection_provider="detector", crop_buffer_ratio=0.0)
    patch_config(monkeypatch, config, doctrine)
    fake_detector = FakeDetector(
        [Detection(label="buildings", score=0.8, box=(10, 10, 20, 20))]
    )
    patch_backends(monkeypatch, vlm=FakeVLM(), detector=fake_detector)
    pipeline = pipeline_model.BDAPipeline()
    pipeline.detect_objects(Image.new("RGB", (100, 100)))
    assert fake_detector.calls == [list(doctrine.keys())]


def test_detect_objects_detector_mode_attaches_crop_from_box(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict
) -> None:
    """Attach image crop to each detector output box."""
    config = make_config(detection_provider="detector", crop_buffer_ratio=0.0)
    patch_config(monkeypatch, config, doctrine)
    fake_detector = FakeDetector(
        [Detection(label="buildings", score=0.8, box=(10, 10, 20, 20))]
    )
    patch_backends(monkeypatch, vlm=FakeVLM(), detector=fake_detector)
    pipeline = pipeline_model.BDAPipeline()
    detections = pipeline.detect_objects(Image.new("RGB", (100, 100)))
    assert len(detections) == 1
    assert detections[0].crop is not None
    assert detections[0].crop.size == (10, 10)


def test_detect_objects_with_vlm_parses_1000_scale_bbox(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict
) -> None:
    """VLM detection should parse JSON and convert bbox to pixels."""
    config = make_config(detection_provider="vlm")
    patch_config(monkeypatch, config, doctrine)
    vlm_response = json.dumps(
        [
            {"target_type": "buildings", "bbox": [100, 100, 500, 900]},
            {"target_type": "invalid", "bbox": [0, 0, 100, 100]},
        ]
    )
    patch_backends(monkeypatch, vlm=FakeVLM([vlm_response]))
    pipeline = pipeline_model.BDAPipeline()
    detections = pipeline.detect_objects_with_vlm(Image.new("RGB", (100, 50)))
    assert detections == [Detection(label="buildings", box=(10, 5, 50, 45))]


def test_assess_detection_uses_scene_overlay_when_provided(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict
) -> None:
    """Verify assess detection uses scene overlay and crop."""
    config = make_config(detection_provider="vlm")
    patch_config(monkeypatch, config, doctrine)
    fake_vlm = FakeVLM(
        [
            json.dumps(
                {
                    "damage_category": "destroyed",
                    "confidence_level": "confirmed",
                    "logic": "Clear catastrophic damage.",
                }
            )
        ]
    )
    patch_backends(monkeypatch, vlm=fake_vlm)
    pipeline = pipeline_model.BDAPipeline()
    overlay = Image.new("RGB", (7, 7))
    monkeypatch.setattr(pipeline_model, "draw_box_overlay", lambda image, box: overlay)
    detection = Detection(
        label="buildings",
        box=(1, 2, 30, 40),
        crop=Image.new("RGB", (30, 40)),
    )
    pipeline.assess_detection(detection, scene_image=Image.new("RGB", (100, 100)))
    assert fake_vlm.calls[0]["image_size"] == [(7, 7), (30, 40)]


def test_assess_detection_returns_none_for_skip_target(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict
) -> None:
    """Assessment should skip detections flagged with skip_target."""
    config = make_config(detection_provider="vlm")
    patch_config(monkeypatch, config, doctrine)
    patch_backends(monkeypatch, vlm=FakeVLM([json.dumps({"skip_target": True})]))
    pipeline = pipeline_model.BDAPipeline()
    detection = Detection(
        label="buildings",
        box=(1, 2, 30, 40),
        crop=Image.new("RGB", (30, 40)),
    )
    assert pipeline.assess_detection(detection) is None


def test_analyze_vlm_mode_returns_humanized_target_with_pixel_bbox(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict, tmp_path
) -> None:
    """Run analyze end-to-end in VLM mode and verify output format."""
    config = make_config(detection_provider="vlm", crop_buffer_ratio=0.0)
    patch_config(monkeypatch, config, doctrine)
    fake_vlm = FakeVLM(
        [
            json.dumps([{"target_type": "buildings", "bbox": [0, 0, 500, 500]}]),
            json.dumps(
                {
                    "damage_category": "destroyed",
                    "confidence_level": "confirmed",
                    "logic": "Severe structural collapse.",
                }
            ),
        ]
    )
    patch_backends(monkeypatch, vlm=fake_vlm)
    pipeline = pipeline_model.BDAPipeline()
    image_path = tmp_path / "scene.png"
    Image.new("RGB", (100, 100)).save(image_path)
    result = pipeline.analyze(image_path)
    assert "target_0" in result
    assert result["target_0"]["target_type"] == "Buildings"
    assert result["target_0"]["bounding_box"] == {
        "xmin": 0,
        "ymin": 0,
        "xmax": 50,
        "ymax": 50
    }
