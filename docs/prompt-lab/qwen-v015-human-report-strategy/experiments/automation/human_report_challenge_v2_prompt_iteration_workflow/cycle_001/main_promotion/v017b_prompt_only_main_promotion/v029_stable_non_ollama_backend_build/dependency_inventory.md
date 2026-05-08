# v029 Dependency Inventory

- System and Qwen worktree Python envs did not have `vllm`, `sglang`, `transformers`, `torch`, or `openai` installed.
- Created isolated vLLM env: `/tmp/bda_v029_vllm_env`.
- vLLM env: `vllm 0.20.1`, `torch 2.11.0`, `transformers 5.8.0`, `openai 2.36.0`.
- GPU: NVIDIA RTX 5000 Ada Generation Laptop GPU, 16,376 MiB VRAM.
- Disk: about 840 GB available at inventory time.
