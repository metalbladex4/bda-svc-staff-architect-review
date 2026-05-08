# v029 Recovery Log

- Read v028/v027 source evidence and GPT-Pro collaboration directives.
- Inventoried GPU, disk, endpoint status, processes, Python packages, HF cache, and Ollama cache.
- Verified exact Qwen3-VL 8B is public/non-gated but too large for the 16 GB VRAM envelope in BF16.
- Installed vLLM into `/tmp/bda_v029_vllm_env`.
- Launched vLLM with public quantized Qwen3-VL 8B derivative on `localhost:8000/v1`.
- Fixed bda-svc compatibility by allowing two images per prompt.
- Ran case-67 stability, sentinel stability, full v020c all-current baseline, and office-negative guard.
- Stopped semantic prompt refinement because the new backend-specific baseline was `153 / 66 / 25 / 91`.
