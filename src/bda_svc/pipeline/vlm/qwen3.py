"""Qwen3 vision-language model backend."""

# Reference: https://huggingface.co/collections/Qwen/qwen3-vl

from PIL import Image
from transformers import AutoProcessor, Qwen3VLForConditionalGeneration

from bda_svc.pipeline.interfaces import BaseVLM


class Qwen3VLM(BaseVLM):
    """Qwen3-VL backend for image-conditioned text generation."""

    def __init__(
        self, model_dir: str, local_files_only: bool = True, max_tokens: int = 512
    ) -> None:
        """Initialize the Qwen3-VL backend.

        Args:
            model_dir: Path to the model directory or HF model_id.
            local_files_only: Whether to load locally or from HF Hub.
            max_tokens: Maximum number of new tokens to generate.
        """
        self.model = Qwen3VLForConditionalGeneration.from_pretrained(
            pretrained_model_name_or_path=model_dir,
            local_files_only=local_files_only,
            dtype="auto",
            device_map="auto",
        )
        self.processor = AutoProcessor.from_pretrained(
            model_dir, local_files_only=local_files_only
        )
        self.max_tokens = max_tokens

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
        images = image if isinstance(image, list) else [image]

        # Build messages
        messages = []
        if system_prompt:
            messages.append(
                {"role": "system", "content": [{"type": "text", "text": system_prompt}]}
            )
        user_content = [{"type": "image", "image": img} for img in images]
        user_content.append({"type": "text", "text": prompt})
        messages.append(
            {
                "role": "user",
                "content": user_content,
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
