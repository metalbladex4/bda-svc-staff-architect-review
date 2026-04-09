"""Vision-Language Model BDA pipeline."""

import json
import os
from pathlib import Path

from json_repair import repair_json
from PIL import Image
from pydantic import BaseModel, Field, ValidationError

from bda_svc.pipeline.interfaces import Detection, OllamaVLM
from bda_svc.pipeline.utilities import (
    CONFIG_PATH,
    DOCTRINE_PATH,
    bbox_to_pixels,
    crop_with_buffer,
    draw_box_overlay,
    format_detection_doctrine,
    format_pda_doctrine,
    load_yaml,
    resize_for_vlm,
)


class DetectionItem(BaseModel):
    """Structured detection item returned by detection model."""

    target_type: str
    bbox: list[float] = Field(min_length=4, max_length=4)


class DetectionResponse(BaseModel):
    """Structured detection response returned by detection model."""

    detections: list[DetectionItem]


class AssessmentResponse(BaseModel):
    """Structured assessment response returned by assessment model."""

    damage_category: str
    confidence_level: str
    brief_supporting_logic: str


class BDAPipeline:
    """BDA pipeline combining detection and damage assessment."""

    def __init__(self) -> None:
        """Initialize configuration, doctrine, prompts, and backends."""
        # Load yamls
        self.config = load_yaml(CONFIG_PATH)
        self.doctrine = load_yaml(DOCTRINE_PATH)
        self.categories = list(self.doctrine.keys())

        # Load prompts
        prompts = self.config["prompts"]
        self.system_prompt = prompts["system"]
        self.detect_objects_prompt_template = prompts["detect_objects"]
        self.assess_damage_prompt_template = prompts["assess_damage"]
        self.summarize_scene_prompt_template = prompts["summarize_scene"]

        # Load detection backend
        detection_cfg = self.config["detection_vlm"]
        detection_model = os.environ.get("BDA_DETECTION_MODEL", detection_cfg["model"])
        self.detection_bbox_convention = detection_cfg["bbox_convention"]
        self.detection_temperature = float(detection_cfg["temperature"])
        self.detection_max_image_size = int(detection_cfg["max_image_size"])
        self.crop_buffer_ratio = float(detection_cfg["crop_buffer_ratio"])
        self.detection_vlm = OllamaVLM(model=detection_model)

        # Load assessment backend
        assessment_cfg = self.config["assessment_vlm"]
        assessment_model = os.environ.get(
            "BDA_ASSESSMENT_MODEL", assessment_cfg["model"]
        )
        self.assessment_temperature = float(assessment_cfg["temperature"])
        self.assessment_max_image_size = int(assessment_cfg["max_image_size"])
        self.assessment_vlm = OllamaVLM(model=assessment_model)

    def detect_objects(self, image: Image.Image) -> list[Detection]:
        """Produce detections for configured doctrinal categories.

        Args:
            image: PIL image to analyze.

        Returns:
            Detection records with crops attached.
        """
        # Get detections, bounding boxes are stored in pixel coordinates
        detections = self._vlm_detections(image)

        # Attach padded image crops to detections
        detections_with_crops = [
            Detection(
                label=det.label,
                bbox=det.bbox,
                crop=crop_with_buffer(image, det.bbox, self.crop_buffer_ratio),
            )
            for det in detections
        ]

        # Sort by label then left-to-right
        detections_with_crops.sort(key=lambda d: (d.label.lower(), d.bbox[0]))
        return detections_with_crops

    def _vlm_detections(self, image: Image.Image) -> list[Detection]:
        """Use the detection VLM to produce object detections.

        Args:
            image: PIL image to analyze.

        Returns:
            A list of parsed detections in raw pixel coordinates.
        """
        prompt = self.detect_objects_prompt_template

        # Format prompt with doctrinal categories
        categories = ", ".join(self.categories)
        prompt = prompt.replace("{categories}", categories)
        prompt = prompt.replace(
            "{detection_guidance}", format_detection_doctrine(self.categories)
        )

        # Format prompt with bbox format
        if self.detection_bbox_convention.startswith("xyxy"):
            bbox_format = "[xmin, ymin, xmax, ymax]"
        elif self.detection_bbox_convention.startswith("yxyx"):
            bbox_format = "[ymin, xmin, ymax, xmax]"
        else:
            raise ValueError(
                "Unsupported bounding box convention specified in config."
                " Supported formats start with 'xyxy' or 'yxyx'."
            )
        prompt = prompt.replace("{bbox_format}", bbox_format)

        # Format prompt with bbox scale
        if self.detection_bbox_convention.endswith("_1"):
            bbox_scale = "normalized coordinates from 0.0 to 1.0"
        elif self.detection_bbox_convention.endswith("_1000"):
            bbox_scale = "normalized coordinates from 0 to 1000"
        elif self.detection_bbox_convention.endswith("_pixels"):
            bbox_scale = "raw pixel coordinates relative to the image"
        else:
            raise ValueError(
                "Unsupported bounding box convention specified in config."
                " Supported formats end with '_1' or '_1000' or '_pixels'."
            )
        prompt = prompt.replace("{bbox_scale}", bbox_scale)

        # Get VLM response
        vlm_image = resize_for_vlm(image, self.detection_max_image_size)
        response = self.detection_vlm.generate(
            image=vlm_image,
            prompt=prompt,
            system_prompt=self.system_prompt,
            format_schema=DetectionResponse.model_json_schema(),
            temperature=self.detection_temperature,
        )

        # Fail safely
        try:
            payload = repair_json(response)
            payload = DetectionResponse.model_validate_json(payload)
        except ValidationError:
            return []

        # Return list of detections
        detections = []
        for item in payload.detections:
            # Validate target_type is doctrinal
            target_type = item.target_type.strip().lower()
            if target_type not in self.categories:
                continue

            # Validate bounding box is valid
            pixel_box = bbox_to_pixels(
                image,
                vlm_image,
                item.bbox,
                bbox_convention=self.detection_bbox_convention,
            )
            if pixel_box is None:
                continue

            detections.append(Detection(label=target_type, bbox=pixel_box))

        return detections

    def assess_detection(
        self,
        detection: Detection,
        scene_image: Image.Image | None = None,
    ) -> dict | None:
        """Assess damage for a single detected object crop.

        Args:
            detection: Detection with populated `bbox` and `crop`.
            scene_image: Optional full-scene for additional context.

        Returns:
            Final target assessment record.
        """
        # Format prompt
        doctrine = format_pda_doctrine(detection.label)
        prompt = self.assess_damage_prompt_template
        prompt = prompt.replace("{target_type}", detection.label)
        prompt = prompt.replace("{doctrine}", doctrine)

        # Format image inputs
        if scene_image is None:
            image_input = resize_for_vlm(detection.crop, self.assessment_max_image_size)
        else:
            scene_with_overlay = draw_box_overlay(scene_image, detection.bbox)
            image_input = [
                resize_for_vlm(scene_with_overlay, self.assessment_max_image_size),
                resize_for_vlm(detection.crop, self.assessment_max_image_size),
            ]

        # Get VLM response
        response = self.assessment_vlm.generate(
            image=image_input,
            prompt=prompt,
            system_prompt=self.system_prompt,
            format_schema=AssessmentResponse.model_json_schema(),
            temperature=self.assessment_temperature,
        )

        # Fail safely
        try:
            payload = repair_json(response)
            payload = AssessmentResponse.model_validate_json(payload)
        except ValidationError:
            return None

        # Return structured output
        return {
            "target_type": detection.label,
            "damage_category": payload.damage_category.upper(),
            "confidence_level": payload.confidence_level.upper(),
            "brief_supporting_logic": payload.brief_supporting_logic,
            "bounding_box": list(detection.bbox),
        }

    def summarize_scene(self, scene_image: Image.Image, targets: list[dict]) -> str:
        """Summarize the scene using the image and assessed targets.

        Args:
            scene_image: Full-scene image.
            targets: Finalized per-target assessment payloads.

        Returns:
            Concise scene summary text.
        """
        target_assessments = json.dumps(targets, indent=2)
        prompt = self.summarize_scene_prompt_template.replace(
            "{target_assessments}", target_assessments
        )
        summary_image = resize_for_vlm(scene_image, self.assessment_max_image_size)
        response = self.assessment_vlm.generate(
            image=summary_image,
            prompt=prompt,
            system_prompt=self.system_prompt,
            temperature=self.assessment_temperature,
        )
        return response.strip()

    def consolidate_results(
        self, targets: list[dict] | None, scene_summary: str
    ) -> dict:
        """Consolidate per-target results into the final output shape.

        Args:
            targets: Per-target assessment payloads.
            scene_summary: Scene-level summary.

        Returns:
            Final image-level result dictionary.
        """
        template = {"summary": scene_summary, "physical_damage": {}}

        if not targets:
            targets = [
                {
                    "target_type": "object_not_found",
                    "damage_category": "NOT APPLICABLE",
                    "confidence_level": "CONFIRMED",
                    "brief_supporting_logic": "No visible targets in image.",
                    "bounding_box": [0, 0, 0, 0],
                }
            ]

        for i, target in enumerate(targets):
            template["physical_damage"][f"target_{i}"] = target

        return template

    def analyze(self, image_path: str | Path) -> str:
        """Run the full BDA pipeline and return the final result payload.

        Args:
            image_path: Path to the input image.

        Returns:
            Final image-level BDA payload.
        """
        with Image.open(Path(image_path)).convert("RGB") as image:
            detections = self.detect_objects(image)
            targets = [self.assess_detection(d, scene_image=image) for d in detections]
            targets = [t for t in targets if t is not None]
            scene_summary = self.summarize_scene(image, targets)
            return self.consolidate_results(targets, scene_summary)
