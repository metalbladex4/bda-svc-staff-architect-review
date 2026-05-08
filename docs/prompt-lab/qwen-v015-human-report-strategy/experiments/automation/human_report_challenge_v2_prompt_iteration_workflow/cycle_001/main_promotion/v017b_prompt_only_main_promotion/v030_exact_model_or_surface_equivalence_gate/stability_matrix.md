# Stability Matrix

Generated: 2026-05-08T16:08:55Z

Stage 1 case-67 stability: **failed**.

- vLLM exact Qwen timed out on the first case-67 replay.
- Hugging Face Transformers exact Qwen served a tiny multimodal JSON smoke request, but the real BDA case-67 request failed with a device-map error and then timed out after the input-device retry.
- Stage 2 sentinel was not run because Stage 1 did not pass.

Trace summaries are in `stability_matrix.json`.
