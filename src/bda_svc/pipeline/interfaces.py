"""Pipeline interfaces, types, and structured output schemas."""

import base64
import io
import os
from dataclasses import dataclass

from openai import OpenAI
from PIL import Image
from pydantic import BaseModel, Field


@dataclass(frozen=True)
class Detection:
    """Lightweight record for detection output."""

    label: str
    bbox: tuple[int, int, int, int]
    crop: Image.Image | None = None


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


class VLMBackend:
    """OpenAI-compatible backend for vision-language text generation."""

    def __init__(self, model: str) -> None:
        """Initialize the VLM backend.

        Args:
            model: VLM model name.
        """
        self.model = model
        base_url = os.getenv("OPENAI_BASE_URL", "http://localhost:8000/v1")
        api_key = os.getenv("OPENAI_API_KEY", "no-auth")
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def _encode_image(self, image: Image.Image) -> str:
        """Encode a PIL image to a base64 string."""
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
        """Generate a response using the OpenAI Chat Completions API.

        Args:
            image: One image or list of images for multi-image prompts.
            prompt: User prompt text.
            system_prompt: Optional system prompt.
            format_schema: Optional JSON schema for structured output.
            temperature: Optional sampling temperature.

        Returns:
            Model response text, or a JSON string if schema is provided.
        """
        messages = []

        # Optional system prompt
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # Build user message
        image_list = image if isinstance(image, list) else [image]
        user_content = [{"type": "text", "text": prompt}]
        for img in image_list:
            user_content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{self._encode_image(img)}"
                    },
                }
            )
        messages.append({"role": "user", "content": user_content})

        # Build request
        request_kwargs = {"model": self.model, "messages": messages}

        # Optional structured output schema
        if format_schema is not None:
            request_kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": "response", "schema": format_schema},
            }

        # Optional sampling temperature
        if temperature is not None:
            request_kwargs["temperature"] = temperature

        # Return response string
        response = self.client.chat.completions.create(**request_kwargs)
        return response.choices[0].message.content or ""
