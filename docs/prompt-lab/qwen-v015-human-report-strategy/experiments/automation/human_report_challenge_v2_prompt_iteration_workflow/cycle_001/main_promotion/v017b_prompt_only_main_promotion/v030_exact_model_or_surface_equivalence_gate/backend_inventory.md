# v030 Backend Inventory

Generated: `2026-05-08T16:03:25Z`

- preferred endpoint ok: `True`
- fallback endpoint ok: `True`
- selected backend: `vllm_exact_qwen3_vl_8b_local_8000`
- reason: non-Ollama vLLM endpoint available on localhost:8000 with expected served model name; actual model root is recorded in /v1/models

Project docs only identify the preferred launch command as `vllm serve Qwen/Qwen3-VL-8B-Instruct`.
No installed vLLM/SGLang/Transformers stack was found in the probed Python environments.
