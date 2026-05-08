# v030 Exact Model Operational Failure Diagnosis

## What Was Tested

v030 tested whether exact `Qwen/Qwen3-VL-8B-Instruct` could replace the unstable Ollama fallback and the behaviorally unacceptable v029 quantized vLLM surface.

## Result

Exact Qwen was public, downloaded without credentials, cached locally, and loaded through two local routes:

- vLLM OpenAI-compatible server with CPU offload.
- Experiment-only Hugging Face Transformers/FastAPI OpenAI-compatible shim.

Neither route completed the required BDA case-67 Stage 1 gate.

## Failure Mechanics

- vLLM exact Qwen launched, but the first BDA case-67 replay timed out through the fixed OpenAI-compatible client path.
- Hugging Face Transformers exact Qwen loaded and answered a tiny multimodal JSON smoke request.
- The first real BDA case-67 request through the shim failed with a device-map/offload error when inputs were forced to CUDA.
- After retrying with no forced input-device movement, the BDA case-67 request timed out.

## Interpretation

This is not a semantic prompt failure. It is an operational backend/model-surface failure for the exact model on this hardware and request path. Because Stage 1 did not pass, v030 did not run sentinel stability, did not run all-current, and did not resume prompt mutation.

## Next Requirement

Autonomous prompt refinement should remain paused until a backend/model surface can complete the case-67 gate and establish a fresh v020c baseline. The likely fix is more capable local serving hardware, a production-grade exact-model endpoint, or an explicitly approved experiment-runtime change that can handle exact Qwen without invalidating attribution.
