# v029 Backend Inventory

Generated: `2026-05-08T00:18:35Z`

- preferred endpoint ok: `True`
- fallback endpoint ok: `True`
- selected backend: `vllm_quantized_qwen3_vl_8b_local_8000`
- reason: non-Ollama vLLM endpoint available on localhost:8000 with expected served model name; actual model root is recorded in /v1/models

Project docs identify the preferred non-Ollama route as vLLM serving
`Qwen/Qwen3-VL-8B-Instruct`. v029 installed vLLM in an isolated `/tmp`
environment and launched a public quantized Qwen3-VL 8B derivative on
`localhost:8000/v1`.

Important model note: `/v1/models` serves the expected model name
`Qwen/Qwen3-VL-8B-Instruct`, but the actual model root is
`SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16`.

The original Ollama fallback at `localhost:11434/v1` remained available but was
not used for prompt optimization.
