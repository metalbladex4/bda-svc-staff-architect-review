"""Pipeline config and doctrine tests."""

from bda_svc.pipeline.utilities import CONFIG_PATH, DOCTRINE_PATH, load_yaml

EXPECTED_CONFIG_KEYS = {"pipeline", "vlm", "detector", "prompts"}
EXPECTED_PIPELINE_KEYS = {"detection_provider", "crop_buffer_ratio"}
EXPECTED_VLM_KEYS = {"family", "model_id", "load_local", "max_new_tokens"}
EXPECTED_DETECTOR_KEYS = {
    "family",
    "model_id",
    "load_local",
    "threshold",
    "nms_threshold",
    "label_map",
}
EXPECTED_PROMPT_KEYS = {"system", "detect_objects", "assess_damage"}
EXPECTED_DOCTRINE_CATEGORIES = {"buildings", "military_equipment"}
REQUIRED_DOCTRINE_ENTRY_KEYS = {"physical_damage_definitions"}
ALLOWED_DOCTRINE_ENTRY_KEYS = {
    "physical_damage_definitions",
    "physical_damage_considerations",
}


def test_config_top_level_keys_exact() -> None:
    """Config should contain only expected top-level sections."""
    config = load_yaml(CONFIG_PATH)
    assert set(config.keys()) == EXPECTED_CONFIG_KEYS


def test_config_section_keys_exact() -> None:
    """Config pipeline, vlm, and detector keys should be exact."""
    config = load_yaml(CONFIG_PATH)
    assert set(config["pipeline"].keys()) == EXPECTED_PIPELINE_KEYS
    assert set(config["vlm"].keys()) == EXPECTED_VLM_KEYS
    assert set(config["detector"].keys()) == EXPECTED_DETECTOR_KEYS
    assert config["pipeline"]["detection_provider"] in {"detector", "vlm"}


def test_detector_label_map_is_dict_of_string_lists() -> None:
    """Detector label_map should be dict[str, list[str]]."""
    config = load_yaml(CONFIG_PATH)
    label_map = config["detector"]["label_map"]
    assert isinstance(label_map, dict)
    assert set(label_map.keys()) == EXPECTED_DOCTRINE_CATEGORIES
    for category, phrases in label_map.items():
        assert isinstance(category, str)
        assert isinstance(phrases, list)


def test_prompt_sections_and_placeholders() -> None:
    """Prompts should contain required sections and templates."""
    config = load_yaml(CONFIG_PATH)
    prompts = config["prompts"]
    assert set(prompts.keys()) == EXPECTED_PROMPT_KEYS
    assert "{categories}" in prompts["detect_objects"]
    assert "{target_type}" in prompts["assess_damage"]
    assert "{doctrine}" in prompts["assess_damage"]


def test_doctrine_categories_and_entry_keys_valid() -> None:
    """Doctrine should use allowed keys with required definitions."""
    doctrine = load_yaml(DOCTRINE_PATH)
    assert set(doctrine.keys()) == EXPECTED_DOCTRINE_CATEGORIES
    for entry in doctrine.values():
        assert REQUIRED_DOCTRINE_ENTRY_KEYS.issubset(set(entry.keys()))
        assert set(entry.keys()).issubset(ALLOWED_DOCTRINE_ENTRY_KEYS)


def test_backend_families_are_from_supported_set() -> None:
    """Config backend families should be in the supported sets."""
    config = load_yaml(CONFIG_PATH)
    assert config["vlm"]["family"] in {"qwen3"}
    assert config["detector"]["family"] in {"grounding_dino"}
