# v029 Backend Feasibility Matrix

| Backend | Result | Notes |
| --- | --- | --- |
| vLLM | launched | Isolated `/tmp/bda_v029_vllm_env`; served public quantized Qwen3-VL 8B derivative on `localhost:8000/v1`. |
| SGLang | not attempted | vLLM reached compatibility/stability, so no need to widen install surface. |
| Transformers/FastAPI shim | not attempted | vLLM provided OpenAI-compatible multimodal serving. |
| Ollama | comparison only | v027/v028 instability keeps Ollama blocked for prompt optimization. |
