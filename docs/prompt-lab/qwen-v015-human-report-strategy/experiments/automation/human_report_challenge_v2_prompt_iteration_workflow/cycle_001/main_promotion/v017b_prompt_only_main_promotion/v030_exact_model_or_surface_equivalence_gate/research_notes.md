# Research Notes

Generated: 2026-05-08T16:08:55Z

- Hugging Face model metadata checked for `Qwen/Qwen3-VL-8B-Instruct`: public, Apache-2.0, image-text-to-text, architecture `qwen3_vl`, roughly 8.8B parameters. No token or license gate was encountered during download.
- Hugging Face Transformers documentation via Context7 showed the local Qwen3-VL path with `AutoProcessor`, `AutoModelForImageTextToText` / Qwen3-VL model classes, `apply_chat_template`, and `generate`.
- vLLM documentation via Context7 showed OpenAI-compatible multimodal serving with `image_url`, `response_format=json_schema`, and Qwen3-VL examples.

Local evidence overrides external docs: both exact-model local serving routes failed the BDA case-67 operational gate on this machine.
