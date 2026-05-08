# Exact Model Feasibility

Generated: 2026-05-08T16:08:55Z

Exact target: `Qwen/Qwen3-VL-8B-Instruct`.

Result: feasible to access locally. The model is public/non-gated, was downloaded from Hugging Face without credentials, and is now cached at `~/.cache/huggingface/hub/models--Qwen--Qwen3-VL-8B-Instruct`.

Operational result: exact model serving did not pass the BDA case-67 gate. vLLM launched with CPU offload but timed out on the first project request. The Hugging Face Transformers shim loaded the model and served a tiny multimodal JSON smoke request, but the real BDA case-67 request failed once with a device-map error and once with a timeout.
