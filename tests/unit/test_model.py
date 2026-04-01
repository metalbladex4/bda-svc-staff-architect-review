"""Pipeline model tests."""

import json

import pytest
from PIL import Image

from bda_svc.pipeline import model as pipeline_model
from bda_svc.pipeline.interfaces import Detection

# ----------------------------------------------------------------------
# Test Setup: Create fake backends
# ----------------------------------------------------------------------


class FakeVLM:
    """Fake Ollama backend that returns scripted responses."""

    def __init__(self, responses: list[str] | None = None) -> None:
        """Store scripted responses."""
        self.responses = list(responses or [])
        self.calls: list[dict] = []

    def generate(
        self,
        image: Image.Image | list[Image.Image],
        prompt: str,
        system_prompt: str | None = None,
        format_schema: dict | None = None,
        temperature: float | None = None,
    ) -> str:
        """Return the next scripted response and record the call."""
        if isinstance(image, list):
            image_size = [img.size for img in image]
        else:
            image_size = image.size

        self.calls.append(
            {
                "image_size": image_size,
                "prompt": prompt,
                "system_prompt": system_prompt,
                "format_schema": format_schema,
                "temperature": temperature,
            }
        )
        return self.responses.pop(0)


# ----------------------------------------------------------------------
# Test Setup: Config and doctrine fixtures
# ----------------------------------------------------------------------


def make_config(crop_buffer_ratio: float = 0.10) -> dict:
    """Return minimal config for model tests."""
    return {
        "detection_vlm": {
            "model": "detection-model",
            "temperature": 0.0,
            "max_image_size": 1024,
            "crop_buffer_ratio": crop_buffer_ratio,
        },
        "assessment_vlm": {
            "model": "assessment-model",
            "temperature": 0.0,
            "max_image_size": 1024,
        },
        "prompts": {
            "system": "system prompt",
            "detect_objects": "Detect objects from: {categories}",
            "assess_damage": "Assess {target_type}\n{doctrine}",
            "summarize_scene": "Summarize scene using:\n{target_assessments}",
        },
    }


@pytest.fixture
def doctrine() -> dict:
    """Small doctrine fixture for model tests."""
    return {
        "buildings": {"physical_damage_definitions": "building doctrine"},
        "military_equipment": {"physical_damage_definitions": "equipment doctrine"},
    }


# ----------------------------------------------------------------------
# Test Setup: Monkeypatch backend builders and config/doctrine
# ----------------------------------------------------------------------


def patch_backends(
    monkeypatch: pytest.MonkeyPatch,
    detection_vlm: FakeVLM | None = None,
    assessment_vlm: FakeVLM | None = None,
    model_names: list[str] | None = None,
) -> None:
    """Patch `OllamaVLM` in the pipeline module."""
    fake_instances = [detection_vlm or FakeVLM(), assessment_vlm or FakeVLM()]

    def fake_ollama_vlm(model: str) -> FakeVLM:
        if model_names is not None:
            model_names.append(model)
        return fake_instances.pop(0)

    monkeypatch.setattr(pipeline_model, "OllamaVLM", fake_ollama_vlm)


def patch_config(monkeypatch: pytest.MonkeyPatch, config: dict, doctrine: dict) -> None:
    """Patch `load_yaml` in the pipeline module."""

    def fake_load_yaml(path):
        if path == pipeline_model.CONFIG_PATH:
            return config
        if path == pipeline_model.DOCTRINE_PATH:
            return doctrine
        return None

    monkeypatch.setattr(pipeline_model, "load_yaml", fake_load_yaml)


# ----------------------------------------------------------------------
# Test Suite
# ----------------------------------------------------------------------


def test_init_loads_backend_settings(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict
) -> None:
    """Pipeline should load backend instances and key settings from config."""
    config = make_config()
    patch_config(monkeypatch, config, doctrine)
    detection_vlm = FakeVLM()
    assessment_vlm = FakeVLM()
    patch_backends(
        monkeypatch, detection_vlm=detection_vlm, assessment_vlm=assessment_vlm
    )
    pipeline = pipeline_model.BDAPipeline()
    assert pipeline.detection_vlm is detection_vlm
    assert pipeline.assessment_vlm is assessment_vlm
    assert pipeline.crop_buffer_ratio == 0.10
    assert pipeline.detection_temperature == 0.0
    assert pipeline.assessment_temperature == 0.0
    assert pipeline.detection_max_image_size == 1024
    assert pipeline.assessment_max_image_size == 1024


def test_init_uses_config_model_names_by_default(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict
) -> None:
    """Pipeline should use config model names when env overrides are absent."""
    config = make_config()
    patch_config(monkeypatch, config, doctrine)
    monkeypatch.delenv("BDA_DETECTION_MODEL", raising=False)
    monkeypatch.delenv("BDA_ASSESSMENT_MODEL", raising=False)
    model_names = []
    detection_vlm = FakeVLM()
    assessment_vlm = FakeVLM()
    patch_backends(
        monkeypatch,
        detection_vlm=detection_vlm,
        assessment_vlm=assessment_vlm,
        model_names=model_names,
    )
    pipeline = pipeline_model.BDAPipeline()
    assert pipeline.detection_vlm is detection_vlm
    assert pipeline.assessment_vlm is assessment_vlm
    assert model_names == ["detection-model", "assessment-model"]


def test_init_uses_env_model_names_when_set(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict
) -> None:
    """Pipeline should prefer env model names over config values."""
    config = make_config()
    patch_config(monkeypatch, config, doctrine)
    monkeypatch.setenv("BDA_DETECTION_MODEL", "env-detection-model")
    monkeypatch.setenv("BDA_ASSESSMENT_MODEL", "env-assessment-model")
    model_names = []
    detection_vlm = FakeVLM()
    assessment_vlm = FakeVLM()
    patch_backends(
        monkeypatch,
        detection_vlm=detection_vlm,
        assessment_vlm=assessment_vlm,
        model_names=model_names,
    )
    pipeline = pipeline_model.BDAPipeline()
    assert pipeline.detection_vlm is detection_vlm
    assert pipeline.assessment_vlm is assessment_vlm
    assert model_names == ["env-detection-model", "env-assessment-model"]


def test_detect_objects_resizes_model_input_and_attaches_original_image_crop(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict
) -> None:
    """Detection should resize VLM input but keep bbox mapping on the original image."""
    config = make_config(crop_buffer_ratio=0.0)
    patch_config(monkeypatch, config, doctrine)
    detection_vlm = FakeVLM(
        [
            json.dumps(
                {
                    "detections": [
                        {"target_type": "buildings", "bbox": [100, 100, 500, 900]}
                    ]
                }
            )
        ]
    )
    patch_backends(monkeypatch, detection_vlm=detection_vlm, assessment_vlm=FakeVLM())
    pipeline = pipeline_model.BDAPipeline()
    detections = pipeline.detect_objects(Image.new("RGB", (4000, 2000)))
    assert len(detections) == 1
    assert detection_vlm.calls[0]["image_size"] == (1024, 512)
    assert detection_vlm.calls[0]["format_schema"] is not None
    assert detections[0].label == "buildings"
    assert detections[0].bbox == (400, 200, 2000, 1800)
    assert detections[0].crop is not None
    assert detections[0].crop.size == (1600, 1600)


def test_detect_objects_returns_empty_for_invalid_detection_payload(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict
) -> None:
    """Detection should fail safely when structured output is invalid."""
    config = make_config()
    patch_config(monkeypatch, config, doctrine)
    patch_backends(
        monkeypatch,
        detection_vlm=FakeVLM([json.dumps([{"target_type": "buildings"}])]),
        assessment_vlm=FakeVLM(),
    )
    pipeline = pipeline_model.BDAPipeline()
    assert pipeline.detect_objects(Image.new("RGB", (100, 100))) == []


def test_assess_detection_uses_overlay_and_returns_structured_output(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict
) -> None:
    """Assessment should use the overlay plus crop and return the expected payload."""
    config = make_config()
    patch_config(monkeypatch, config, doctrine)
    assessment_vlm = FakeVLM(
        [
            json.dumps(
                {
                    "damage_category": "destroyed",
                    "confidence_level": "confirmed",
                    "brief_supporting_logic": "roof collapse; wall breach; burn damage",
                }
            )
        ]
    )
    patch_backends(monkeypatch, detection_vlm=FakeVLM(), assessment_vlm=assessment_vlm)
    monkeypatch.setattr(
        pipeline_model,
        "draw_box_overlay",
        lambda image, bbox: Image.new("RGB", (1200, 600)),
    )
    pipeline = pipeline_model.BDAPipeline()
    detection = Detection(
        label="buildings",
        bbox=(1, 2, 30, 40),
        crop=Image.new("RGB", (2000, 1000)),
    )

    result = pipeline.assess_detection(
        detection, scene_image=Image.new("RGB", (4000, 2000))
    )
    assert assessment_vlm.calls[0]["image_size"] == [(1024, 512), (1024, 512)]
    assert assessment_vlm.calls[0]["format_schema"] is not None
    assert result == {
        "target_type": "buildings",
        "damage_category": "DESTROYED",
        "confidence_level": "CONFIRMED",
        "brief_supporting_logic": "roof collapse; wall breach; burn damage",
        "bounding_box": [1, 2, 30, 40],
    }


def test_assess_detection_returns_none_for_invalid_assessment_payload(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict
) -> None:
    """Assessment should fail safely when structured output is invalid."""
    config = make_config()
    patch_config(monkeypatch, config, doctrine)
    patch_backends(
        monkeypatch,
        detection_vlm=FakeVLM(),
        assessment_vlm=FakeVLM([json.dumps({"damage_category": "destroyed"})]),
    )
    pipeline = pipeline_model.BDAPipeline()
    detection = Detection(
        label="buildings",
        bbox=(1, 2, 30, 40),
        crop=Image.new("RGB", (30, 40)),
    )
    assert pipeline.assess_detection(detection) is None


def test_summarize_scene_uses_resized_image_and_serialized_targets(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict
) -> None:
    """Scene summary should use the full scene and serialized target assessments."""
    config = make_config()
    patch_config(monkeypatch, config, doctrine)
    assessment_vlm = FakeVLM(["Concise scene summary."])
    patch_backends(
        monkeypatch,
        detection_vlm=FakeVLM(),
        assessment_vlm=assessment_vlm,
    )
    pipeline = pipeline_model.BDAPipeline()
    targets = [
        {
            "target_type": "buildings",
            "damage_category": "DESTROYED",
            "confidence_level": "CONFIRMED",
            "brief_supporting_logic": "roof collapse; wall breach",
            "bounding_box": [0, 0, 50, 50],
        }
    ]
    summary = pipeline.summarize_scene(Image.new("RGB", (4000, 2000)), targets)
    assert summary == "Concise scene summary."
    assert assessment_vlm.calls[0]["image_size"] == (1024, 512)
    assert json.dumps(targets, indent=2) in assessment_vlm.calls[0]["prompt"]


def test_analyze_returns_summary_and_numbered_targets(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict, tmp_path
) -> None:
    """Analyze should produce a summary plus numbered target results."""
    config = make_config(crop_buffer_ratio=0.0)
    patch_config(monkeypatch, config, doctrine)
    detection_vlm = FakeVLM(
        [
            json.dumps(
                {"detections": [{"target_type": "buildings", "bbox": [0, 0, 500, 500]}]}
            )
        ]
    )
    assessment_vlm = FakeVLM(
        [
            json.dumps(
                {
                    "damage_category": "destroyed",
                    "confidence_level": "confirmed",
                    "brief_supporting_logic": "roof collapse; fire damage",
                }
            ),
            "Scene summary grounded in target assessments.",
        ]
    )
    patch_backends(
        monkeypatch, detection_vlm=detection_vlm, assessment_vlm=assessment_vlm
    )
    pipeline = pipeline_model.BDAPipeline()
    image_path = tmp_path / "scene.png"
    Image.new("RGB", (100, 100)).save(image_path)
    result = pipeline.analyze(image_path)
    assert result["summary"] == "Scene summary grounded in target assessments."
    assert result["physical_damage"]["target_0"] == {
        "target_type": "buildings",
        "damage_category": "DESTROYED",
        "confidence_level": "CONFIRMED",
        "brief_supporting_logic": "roof collapse; fire damage",
        "bounding_box": [0, 0, 50, 50],
    }


def test_analyze_returns_summary_only_when_no_targets(
    monkeypatch: pytest.MonkeyPatch, doctrine: dict, tmp_path
) -> None:
    """Analyze should return the no-target placeholder when detection finds nothing."""
    config = make_config()
    patch_config(monkeypatch, config, doctrine)
    detection_vlm = FakeVLM(["not valid json"])
    assessment_vlm = FakeVLM(["No relevant targets were assessed in the scene."])
    patch_backends(
        monkeypatch, detection_vlm=detection_vlm, assessment_vlm=assessment_vlm
    )
    pipeline = pipeline_model.BDAPipeline()
    image_path = tmp_path / "scene.png"
    Image.new("RGB", (100, 100)).save(image_path)
    result = pipeline.analyze(image_path)
    assert result["summary"] == "No relevant targets were assessed in the scene."
    assert result["physical_damage"]["target_0"] == {
        "target_type": "object_not_found",
        "damage_category": "NOT APPLICABLE",
        "confidence_level": "CONFIRMED",
        "brief_supporting_logic": "No visible targets in image.",
        "bounding_box": [0, 0, 0, 0],
    }
