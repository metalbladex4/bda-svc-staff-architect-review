"""Grounding DINO detector backend."""

# Reference: https://huggingface.co/docs/transformers/en/model_doc/grounding-dino

import torch
from accelerate import Accelerator
from PIL import Image
from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor

from bda_svc.pipeline.types import BaseDetector, Detection
from bda_svc.pipeline.utilities import crop_with_buffer, nms


class GroundingDinoDetector(BaseDetector):
    """Grounding DINO backend for zero-shot object detection."""

    def __init__(
        self,
        model_dir: str,
        local_files_only: bool = True,
        threshold: float = 0.25,
        text_threshold: float = 0.25,
        nms_threshold: float = 0.50,
    ) -> None:
        """Initialize the Grounding DINO detector backend.

        Args:
            model_dir: Path to the model directory or HF model_id.
            local_files_only: Whether to load locally or from HF Hub.
            threshold: Minimum confidence for box predictions.
            text_threshold: Minimum confidence for text-labels.
            nms_threshold: Non-maximum suppression threshold.
        """
        device = Accelerator().device
        self.model = AutoModelForZeroShotObjectDetection.from_pretrained(
            model_dir, local_files_only=local_files_only
        ).to(device)
        self.processor = AutoProcessor.from_pretrained(
            model_dir, local_files_only=local_files_only, use_fast=True
        )
        self.threshold = threshold
        self.text_threshold = text_threshold
        self.nms_threshold = nms_threshold

    def detect(
        self, image: Image.Image, text_labels: list[list[str]]
    ) -> list[Detection]:
        """Detect objects in an image.

        Args:
            image: PIL image to analyze.
            text_labels: Candidate text labels for inference.

        Returns:
            A list of normalized detection records.
        """
        inputs = self.processor(images=image, text=text_labels, return_tensors="pt").to(
            self.model.device
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
        results = self.processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            threshold=self.threshold,
            text_threshold=self.text_threshold,
            target_sizes=[image.size[::-1]],
        )
        result = results[0]

        # Build detection output and apply NMS
        detections = []
        for box, score, label in zip(
            result["boxes"],
            result["scores"],
            result["text_labels"],
            strict=False,
        ):
            rounded_box = tuple(int(round(x)) for x in box.tolist())
            crop = crop_with_buffer(image, rounded_box)
            detections.append(
                Detection(
                    label=str(label),
                    score=float(score.item()),
                    box=rounded_box,
                    crop=crop,
                )
            )

        return nms(detections, self.nms_threshold)
