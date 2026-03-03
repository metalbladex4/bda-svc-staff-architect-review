"""Qwen3 vision-language model backend."""

# Reference: https://github.com/QwenLM/Qwen3-VL

from PIL import Image
from transformers import AutoModelForImageTextToText, AutoProcessor

from bda_svc.pipeline.types import BaseVLM


class Qwen3VLM(BaseVLM):
    """Qwen3-VL backend for image-conditioned text generation."""

    def __init__(
        self, model_dir: str, local_files_only: bool = True, max_tokens: int = 1024
    ) -> None:
        """Initialize the Qwen3-VL backend.

        Args:
            model_dir: Path to the model directory or HF model_id.
            local_files_only: Whether to load locally or from HF Hub.
            max_tokens: Maximum number of new tokens to generate.
        """
        self.model = AutoModelForImageTextToText.from_pretrained(
            pretrained_model_name_or_path=model_dir,
            local_files_only=local_files_only,
            dtype="auto",
            device_map="auto",
        )
        self.processor = AutoProcessor.from_pretrained(model_dir)
        self.max_tokens = max_tokens

    def generate(
        self,
        image: Image.Image,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        """Generate a response from the VLM.

        Args:
            image: PIL image to analyze.
            prompt: User prompt text.
            system_prompt: Optional system prompt.

        Returns:
            Model response text.
        """
        # Build messages
        messages = []
        if system_prompt:
            messages.append(
                {"role": "system", "content": [{"type": "text", "text": system_prompt}]}
            )
        messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt},
                ],
            }
        )

        # Preparation for inference
        inputs = self.processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt",
        )
        inputs = inputs.to(self.model.device)

        # Inference: Generation of the output
        generated_ids = self.model.generate(**inputs, max_new_tokens=self.max_tokens)
        generated_ids_trimmed = [
            out_ids[len(in_ids) :]
            for in_ids, out_ids in zip(inputs.input_ids, generated_ids, strict=False)
        ]
        output_text = self.processor.batch_decode(
            generated_ids_trimmed,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )[0]

        return output_text
