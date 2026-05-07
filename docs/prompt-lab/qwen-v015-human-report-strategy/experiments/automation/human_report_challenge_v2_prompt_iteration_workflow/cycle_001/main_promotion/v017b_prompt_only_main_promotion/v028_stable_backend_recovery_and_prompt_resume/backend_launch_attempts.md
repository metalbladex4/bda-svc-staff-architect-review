# v028 Backend Launch Attempts

Generated: `2026-05-07T23:32:12Z`

## Original Preferred Backend

- endpoint: `http://localhost:8000/v1`
- status before recovery: `unavailable`
- established project command found: `vllm serve Qwen/Qwen3-VL-8B-Instruct`
- vLLM installed locally: `no`
- Qwen/Qwen3-VL-8B-Instruct HF cache present: `no`

## Deterministic Ollama Recovery

- model alias: `qwen3-vl:8b-instruct-v028-deterministic`
- source model: cached `qwen3-vl:8b-instruct`
- endpoint launched: `http://localhost:8000/v1`
- server kind: `Ollama OpenAI-compatible`
- result: `launched but failed Stage 1 stability`
- cleanup: experiment-only port-8000 Ollama process was stopped after failure.
