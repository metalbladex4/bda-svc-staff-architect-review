"""Grounding DINO detector backend."""

# Reference: https://huggingface.co/docs/transformers/en/model_doc/grounding-dino

import torch
from accelerate import Accelerator
from PIL import Image
from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor

from bda_svc.pipeline.interfaces import BaseDetector, Detection
from bda_svc.pipeline.utilities import nms


class GroundingDinoDetector(BaseDetector):
    """Grounding DINO backend for zero-shot object detection."""

    def __init__(
        self,
        model_dir: str,
        label_map: dict[str, list[str]],
        local_files_only: bool = True,
        threshold: float = 0.25,
        nms_threshold: float = 0.50,
    ) -> None:
        """Initialize the Grounding DINO detector backend.

        Args:
            model_dir: Path to the model directory or HF model_id.
            label_map: Mapping from doctrine key to detector phrase(s).
            local_files_only: Whether to load locally or from HF Hub.
            threshold: Minimum confidence threshold used for detections.
            nms_threshold: Non-maximum suppression threshold.
        """
        device = Accelerator().device
        self.model = AutoModelForZeroShotObjectDetection.from_pretrained(
            model_dir, local_files_only=local_files_only
        ).to(device)
        self.processor = AutoProcessor.from_pretrained(
            model_dir, local_files_only=local_files_only, use_fast=True
        )
        self.label_map = label_map
        self.threshold = threshold
        self.nms_threshold = nms_threshold

    def detect(self, image: Image.Image, categories: list[str]) -> list[Detection]:
        """Detect objects in an image.

        Args:
            image: PIL image to analyze.
            categories: Allowed doctrinal categories for the image.

        Returns:
            A list of detections for the requested categories.
        """
        # Build phrase -> doctrine label lookup
        phrase_to_category = {}
        for category in categories:
            for phrase in self.label_map[category]:
                key = phrase.strip().lower()
                if key in phrase_to_category and phrase_to_category[key] != category:
                    raise ValueError(
                        f"Duplicate detector phrase '{key}' for categories "
                        f"'{phrase_to_category[key]}' and '{category}'."
                    )
                phrase_to_category[key] = category

        # Get detector labels
        detector_labels = list(phrase_to_category)

        # Run inference
        inputs = self.processor(
            images=image,
            text=[detector_labels],
            return_tensors="pt",
        ).to(self.model.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        result = self.processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            threshold=self.threshold,
            text_threshold=self.threshold,
            target_sizes=[image.size[::-1]],
        )[0]

        # Convert output to Detection objects
        detections = []
        for box, score, label in zip(
            result["boxes"],
            result["scores"],
            result["text_labels"],
            strict=False,
        ):
            doctrine_label = phrase_to_category.get(str(label).strip().lower())
            if doctrine_label is None:
                continue
            detections.append(
                Detection(
                    label=doctrine_label,
                    score=float(score.item()),
                    box=tuple(int(round(x)) for x in box.tolist()),
                )
            )

        return nms(detections, self.nms_threshold)
