"""Object Detection and Vision-Language Model BDA pipeline."""

import json
from pathlib import Path
from typing import Any

from huggingface_hub import snapshot_download
from PIL import Image

from bda_svc.pipeline.detector.grounding_dino import GroundingDinoDetector
from bda_svc.pipeline.interfaces import BaseDetector, BaseVLM, Detection
from bda_svc.pipeline.utilities import (
    CONFIG_PATH,
    DOCTRINE_PATH,
    REPO_PATH,
    bbox_from_1000,
    crop_with_buffer,
    draw_box_overlay,
    format_pda_doctrine,
    load_yaml,
    parse_json,
)
from bda_svc.pipeline.vlm.qwen3 import Qwen3VLM

VLM_FAMILIES = {
    "qwen3": Qwen3VLM,
}
DETECTOR_FAMILIES = {
    "grounding_dino": GroundingDinoDetector,
}


def build_vlm(vlm_cfg: dict[str, Any]) -> BaseVLM:
    """Build the configured VLM backend.

    Args:
        vlm_cfg: VLM configuration from `config.yaml`.

    Returns:
        A configured VLM backend implementing `BaseVLM`.

    Raises:
        ValueError: If configuration values are invalid.
    """
    # Load kwargs
    family = vlm_cfg.get("family")
    backend_cls = VLM_FAMILIES.get(family)
    if backend_cls is None:
        raise ValueError(f"Unsupported VLM family: {family}")
    model_id = vlm_cfg["model_id"]
    max_tokens = int(vlm_cfg["max_new_tokens"])
    load_local = vlm_cfg["load_local"]

    # Load from remote
    if not load_local:
        return backend_cls(
            model_dir=model_id,
            local_files_only=False,
            max_tokens=max_tokens,
        )

    # Load local
    local_model_dir = REPO_PATH / "models" / model_id.replace("/", "--")
    local_model_dir.mkdir(parents=True, exist_ok=True)
    try:
        return backend_cls(
            model_dir=local_model_dir,
            local_files_only=True,
            max_tokens=max_tokens,
        )
    except (OSError, ValueError):
        snapshot_download(model_id, local_dir=local_model_dir)
        return backend_cls(
            model_dir=local_model_dir,
            local_files_only=True,
            max_tokens=max_tokens,
        )


def build_detector(detector_cfg: dict[str, Any]) -> BaseDetector:
    """Build the configured detector backend.

    Args:
        detector_cfg: Detector configuration from `config.yaml`.

    Returns:
        A configured detector backend implementing `BaseDetector`.

    Raises:
        ValueError: If configuration values are invalid.
    """
    # Load kwargs
    family = detector_cfg.get("family")
    backend_cls = DETECTOR_FAMILIES.get(family)
    if backend_cls is None:
        raise ValueError(f"Unsupported detector family: {family}")
    model_id = detector_cfg["model_id"]
    load_local = detector_cfg["load_local"]
    detector_kwargs = {
        "label_map": detector_cfg["label_map"],
        "threshold": float(detector_cfg["threshold"]),
        "nms_threshold": float(detector_cfg["nms_threshold"]),
    }

    # Load from remote
    if not load_local:
        return backend_cls(
            model_dir=model_id,
            local_files_only=False,
            **detector_kwargs,
        )

    # Load local
    local_model_dir = REPO_PATH / "models" / model_id.replace("/", "--")
    local_model_dir.mkdir(parents=True, exist_ok=True)
    try:
        return backend_cls(
            model_dir=local_model_dir,
            local_files_only=True,
            **detector_kwargs,
        )
    except (OSError, ValueError):
        snapshot_download(model_id, local_dir=local_model_dir)
        return backend_cls(
            model_dir=local_model_dir,
            local_files_only=True,
            **detector_kwargs,
        )


class BDAPipeline:
    """BDA pipeline combining detection and VLM damage assessment."""

    def __init__(self) -> None:
        """Initialize configuration, doctrine, prompts, and backends.

        Raises:
            ValueError: If required config keys are missing or invalid.
        """
        # Load config, doctrine, prompts
        self.config = load_yaml(CONFIG_PATH)
        self.doctrine = load_yaml(DOCTRINE_PATH)
        self.categories = list(self.doctrine.keys())

        prompts = self.config["prompts"]
        self.system_prompt = prompts["system"]
        self.detect_objects_prompt_template = prompts["detect_objects"]
        self.assess_damage_prompt_template = prompts["assess_damage"]

        pipeline_cfg = self.config["pipeline"]
        self.crop_buffer_ratio = float(pipeline_cfg["crop_buffer_ratio"])
        self.detection_provider = pipeline_cfg["detection_provider"]
        if self.detection_provider not in {"detector", "vlm"}:
            raise ValueError("pipeline.detection_provider must be 'detector' or 'vlm'.")

        # Initialize VLM
        vlm_cfg = self.config["vlm"]
        self.vlm = build_vlm(vlm_cfg)

        # Initialize Detector
        self.detector = None
        if self.detection_provider == "detector":
            detector_cfg = self.config.get("detector")
            self.detector = build_detector(detector_cfg)

    def detect_objects(self, image: Image.Image) -> list[Detection]:
        """Produce detections for configured doctrinal categories.

        Args:
            image: PIL image to analyze.

        Returns:
            Detection records with crops attached.
        """
        # Get detections
        if self.detection_provider == "detector":
            detections = self.detector.detect(image, self.categories)
        else:
            detections = self.detect_objects_with_vlm(image)

        # Attach padded image crops to detections
        detections_with_crops = []
        for detection in detections:
            detections_with_crops.append(
                Detection(
                    label=detection.label,
                    score=detection.score,
                    box=detection.box,
                    crop=crop_with_buffer(image, detection.box, self.crop_buffer_ratio),
                )
            )

        return detections_with_crops

    def detect_objects_with_vlm(self, image: Image.Image) -> list[Detection]:
        """Use the VLM backend to produce object detections.

        Args:
            image: PIL image to analyze.

        Returns:
            A list of parsed detections in raw pixel coordinates.

        Raises:
            ValueError: If the VLM returns a non-list JSON payload.
        """
        # Format prompt
        categories_text = ", ".join(self.categories)
        prompt = self.detect_objects_prompt_template.replace(
            "{categories}", categories_text
        )

        # Get VLM response
        response = self.vlm.generate(
            image=image,
            prompt=prompt,
            system_prompt=self.system_prompt,
        )
        payload = parse_json(response)
        if not isinstance(payload, list):
            raise ValueError("VLM detection output must be a JSON list.")

        # Return list of detections
        detections = []
        for item in payload:
            if not isinstance(item, dict):
                continue

            target_type = item.get("target_type")
            if not isinstance(target_type, str):
                continue
            target_type = target_type.strip().lower()
            if target_type not in self.categories:
                continue

            bbox = item.get("bbox")
            if not isinstance(bbox, (list, tuple)):
                continue

            pixel_box = bbox_from_1000(image, list(bbox))
            if pixel_box is None:
                continue

            detections.append(Detection(label=target_type, box=pixel_box))

        return detections

    def assess_detection(
        self,
        detection: Detection,
        scene_image: Image.Image | None = None,
    ) -> dict | None:
        """Assess damage for a single detected object crop.

        Args:
            detection: Detection with populated `crop` and `box`.
            scene_image: Optional full-scene for additional context.

        Returns:
            Final target assessment record or `None` if skipped.

        Raises:
            ValueError: If JSON output is invalid.
        """
        # Format prompt
        doctrine = format_pda_doctrine([detection.label])
        prompt = self.assess_damage_prompt_template.replace(
            "{target_type}", detection.label
        )
        prompt = prompt.replace("{doctrine}", doctrine)

        # Format image inputs
        if scene_image is None:
            image_input = detection.crop
        else:
            scene_with_overlay = draw_box_overlay(scene_image, detection.box)
            image_input = [scene_with_overlay, detection.crop]

        # Get VLM response
        response = self.vlm.generate(
            image=image_input,
            prompt=prompt,
            system_prompt=self.system_prompt,
        )
        payload = parse_json(response)
        if not isinstance(payload, dict):
            raise ValueError("Damage assessment output must be a JSON object.")

        # Return `None` if detection is not important
        if payload.get("skip_target") is True:
            return None

        # Format response values for human-readable output
        def _humanize(value: object) -> str:
            text = str(value).replace("_", " ").strip()
            return " ".join(word.capitalize() for word in text.split())

        return {
            "target_type": _humanize(detection.label),
            "damage_category": _humanize(payload["damage_category"]),
            "confidence_level": _humanize(payload["confidence_level"]),
            "logic": payload["logic"],
            "bbox": list(detection.box),
        }

    def consolidate_results(self, targets: list[dict]) -> dict:
        """Consolidate per-target results into the final output shape.

        Args:
            targets: Per-target assessment payloads.

        Returns:
            Final image-level result dictionary.
        """
        if not targets:
            return {"No Targets": {"logic": "No visible targets in image."}}

        return {
            f"target_{index}": target for index, target in enumerate(targets, start=1)
        }

    def analyze(self, image_path: str | Path) -> str:
        """Run the full BDA pipeline and return a JSON string.

        Args:
            image_path: Path to the input image.

        Returns:
            Final target-level BDA as JSON text.
        """
        with Image.open(Path(image_path)).convert("RGB") as image:
            detections = self.detect_objects(image)
            targets = []
            for detection in detections:
                result = self.assess_detection(detection, scene_image=image)
                if result is not None:
                    targets.append(result)
            return json.dumps(self.consolidate_results(targets))
