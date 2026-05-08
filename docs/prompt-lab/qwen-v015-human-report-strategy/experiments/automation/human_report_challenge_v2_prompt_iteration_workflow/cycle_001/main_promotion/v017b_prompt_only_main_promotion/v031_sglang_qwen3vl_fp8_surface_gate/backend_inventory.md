# v030 Backend Inventory

Generated: `2026-05-08T21:29:06Z`

- preferred endpoint ok: `True`
- fallback endpoint ok: `True`
- selected backend: `vllm_qwen3vl_8b_fp8_local_8000`
- reason: vLLM official Qwen3-VL FP8 endpoint available on localhost:8000 with expected served model name; actual model root is recorded in /v1/models

Project docs only identify the preferred launch command as `vllm serve Qwen/Qwen3-VL-8B-Instruct-FP8`.
No installed vLLM/SGLang/Transformers stack was found in the probed Python environments.
