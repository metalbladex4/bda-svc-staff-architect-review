"""Shared pipeline types and interfaces."""

import base64
import io
import os
from dataclasses import dataclass

from ollama import Client
from PIL import Image


@dataclass(frozen=True)
class Detection:
    """Lightweight record for detection output."""

    label: str
    bbox: tuple[int, int, int, int]
    crop: Image.Image | None = None


class OllamaVLM:
    """Ollama backend for image-conditioned text generation."""

    def __init__(self, model: str) -> None:
        """Initialize the Ollama VLM backend.

        Args:
            model: Ollama model name.
        """
        self.model = model
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.client = Client(host=ollama_host)

    def _encode_image(self, image: Image.Image) -> str:
        """Encode a PIL image to base64."""
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")

    def generate(
        self,
        image: Image.Image | list[Image.Image],
        prompt: str,
        system_prompt: str | None = None,
        format_schema: dict | None = None,
        temperature: float | None = None,
    ) -> str:
        """Generate a response from the VLM.

        Args:
            image: One image or list of images for multi-image prompts.
            prompt: User prompt text.
            system_prompt: Optional system prompt.
            format_schema: Optional JSON schema for structured output.
            temperature: Optional sampling temperature.

        Returns:
            Model response text.
        """
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        images = image if isinstance(image, list) else [image]
        messages.append(
            {
                "role": "user",
                "content": prompt,
                "images": [self._encode_image(img) for img in images],
            }
        )

        options = None
        if temperature is not None:
            options = {"temperature": temperature}

        response = self.client.chat(
            model=self.model,
            messages=messages,
            format=format_schema,
            options=options,
        )
        return response.message.content
