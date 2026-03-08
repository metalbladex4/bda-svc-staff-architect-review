"""Shared pipeline types and interfaces."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from PIL import Image


@dataclass(frozen=True)
class Detection:
    """Lightweight record for detection output."""

    label: str
    score: float | None = None
    box: tuple[int, int, int, int] | None = None
    crop: Image.Image | None = None


class BaseDetector(ABC):
    """Shared detector interface."""

    @abstractmethod
    def detect(self, image: Image.Image, categories: list[str]) -> list[Detection]:
        """Detect objects in an image.

        Args:
            image: PIL image to analyze.
            categories: Allowed doctrinal categories for the image.

        Returns:
            A list of detections for the requested categories.
        """


class BaseVLM(ABC):
    """Shared VLM interface."""

    @abstractmethod
    def generate(
        self,
        image: Image.Image | list[Image.Image],
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        """Generate a response from the VLM.

        Args:
            image: One image or list of images for multi-image prompts.
            prompt: User prompt text.
            system_prompt: Optional system prompt.

        Returns:
            Model response text.
        """
