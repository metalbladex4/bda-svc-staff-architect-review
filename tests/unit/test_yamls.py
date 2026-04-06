"""Pipeline config and doctrine tests."""

from bda_svc.pipeline.utilities import CONFIG_PATH, DOCTRINE_PATH, load_yaml

EXPECTED_CONFIG_KEYS = {"detection_vlm", "assessment_vlm", "prompts"}
EXPECTED_DETECTION_VLM_KEYS = {
    "model",
    "temperature",
    "max_image_size",
    "crop_buffer_ratio",
}
EXPECTED_ASSESSMENT_VLM_KEYS = {"model", "temperature", "max_image_size"}
EXPECTED_PROMPT_KEYS = {"system", "detect_objects", "assess_damage", "summarize_scene"}
EXPECTED_DOCTRINE_CATEGORIES = {"buildings", "military_equipment"}
REQUIRED_DOCTRINE_ENTRY_KEYS = {"physical_damage_definitions"}
ALLOWED_DOCTRINE_ENTRY_KEYS = {
    "physical_damage_definitions",
    "physical_damage_considerations",
}

# ----------------------------------------------------------------------
# Test Setup: Pipeline config tests
# ----------------------------------------------------------------------


def test_config_top_level_keys_exact() -> None:
    """Config should contain only expected top-level sections."""
    config = load_yaml(CONFIG_PATH)
    assert set(config.keys()) == EXPECTED_CONFIG_KEYS


def test_config_section_keys_exact() -> None:
    """Config detection and assessment VLM keys should be exact."""
    config = load_yaml(CONFIG_PATH)
    assert set(config["detection_vlm"].keys()) == EXPECTED_DETECTION_VLM_KEYS
    assert set(config["assessment_vlm"].keys()) == EXPECTED_ASSESSMENT_VLM_KEYS


# ----------------------------------------------------------------------
# Test Setup: Prompt tests
# ----------------------------------------------------------------------


def test_prompt_sections_and_placeholders() -> None:
    """Prompts should contain required sections and templates."""
    config = load_yaml(CONFIG_PATH)
    prompts = config["prompts"]
    assert set(prompts.keys()) == EXPECTED_PROMPT_KEYS
    assert "{categories}" in prompts["detect_objects"]
    assert "{target_type}" in prompts["assess_damage"]
    assert "{doctrine}" in prompts["assess_damage"]
    assert "{target_assessments}" in prompts["summarize_scene"]


# ----------------------------------------------------------------------
# Test Setup: Doctrine tests
# ----------------------------------------------------------------------


def test_doctrine_categories_and_entry_keys_valid() -> None:
    """Doctrine should use allowed keys with required definitions."""
    doctrine = load_yaml(DOCTRINE_PATH)
    assert set(doctrine.keys()) == EXPECTED_DOCTRINE_CATEGORIES
    for entry in doctrine.values():
        assert REQUIRED_DOCTRINE_ENTRY_KEYS.issubset(set(entry.keys()))
        assert set(entry.keys()).issubset(ALLOWED_DOCTRINE_ENTRY_KEYS)
