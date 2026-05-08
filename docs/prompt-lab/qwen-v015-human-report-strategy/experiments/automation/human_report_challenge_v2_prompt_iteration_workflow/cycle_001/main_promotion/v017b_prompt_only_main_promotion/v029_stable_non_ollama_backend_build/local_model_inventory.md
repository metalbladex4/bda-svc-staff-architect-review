# v029 Local Model Inventory

- Initial Hugging Face cache: no official `Qwen/Qwen3-VL-8B-Instruct` snapshot.
- v029 vLLM launch downloaded/cached
  `SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16`.
- Exact target `Qwen/Qwen3-VL-8B-Instruct` is public, non-gated, Apache-2.0,
  but its measured safetensor shards total about 17.53 GB, above the local
  16 GB VRAM envelope before KV/cache.
- Served quantized derivative is public, non-gated, Apache-2.0, and its
  measured safetensor shards total about 7.22 GB.
- Ollama cache remains available only as comparison/reference:
  `qwen3-vl:8b-instruct`, `qwen3-vl:8b-instruct-q8_0`, `qwen3-vl:8b`, and
  `qwen3-vl:8b-instruct-v028-deterministic`.
- No private credentials, tokens, or paid APIs were used.
