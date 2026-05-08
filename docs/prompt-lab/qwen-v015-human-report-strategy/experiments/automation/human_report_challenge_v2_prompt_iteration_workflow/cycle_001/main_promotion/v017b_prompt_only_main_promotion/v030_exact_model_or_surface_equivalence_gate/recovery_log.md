# Recovery Log

- stopped lingering vLLM processes from exact-model timeout attempts
- installed accelerate and qwen-vl-utils into isolated /tmp/bda_v029_vllm_env
- created experiment-only Hugging Face Transformers OpenAI shim inside v030 package
- compiled shim with py_compile
- launched exact Qwen via local Transformers/FastAPI shim
- ran tiny multimodal OpenAI-compatible JSON smoke successfully
- ran v030 case-67 gate through bda-svc path; failed by timeout after input-device retry
