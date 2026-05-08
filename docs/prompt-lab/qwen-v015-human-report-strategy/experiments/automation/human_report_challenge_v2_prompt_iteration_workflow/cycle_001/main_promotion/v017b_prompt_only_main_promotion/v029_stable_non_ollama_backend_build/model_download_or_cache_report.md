# v029 Model Download Or Cache Report

- Exact target model: `Qwen/Qwen3-VL-8B-Instruct`.
- HF status: public, non-gated, Apache-2.0.
- Exact target weight shards measured by HEAD requests: about 17.53 GB.
- Local GPU VRAM: 16,376 MiB, so exact BF16 8B was not launched because it exceeds the practical VRAM envelope before KV/cache.
- Served model: `SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16`.
- Served model status: public, non-gated, Apache-2.0, base model is Qwen3-VL 8B.
- Served model weight shards measured by HEAD requests: about 7.22 GB.
- vLLM downloaded/used the public quantized model through the local Hugging Face cache. No token or private credential was used.
