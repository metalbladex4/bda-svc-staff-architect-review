# Research Notes

- Hugging Face metadata showed `Qwen/Qwen3-VL-8B-Instruct-FP8` is an official Qwen public model, Apache-2.0, image-text-to-text, FP8 quantized from `Qwen/Qwen3-VL-8B-Instruct`, and endpoint-compatible.
- SGLang documentation supported OpenAI-compatible server launch through `python -m sglang.launch_server` with multimodal support and request-shape compatibility.
- vLLM documentation supported OpenAI-compatible multimodal serving with `image_url`, multimodal prompt limits, and Qwen3-VL-style pixel caps.
- Local eval evidence remains authoritative over external serving guidance.
