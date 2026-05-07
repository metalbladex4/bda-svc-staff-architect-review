# v028 Stage 1 Backend Stability Diagnosis

Generated: `2026-05-07T23:32:12Z`

The deterministic Ollama-backed local endpoint failed Stage 1. Exact v020c
replay 1 returned `1/10/9`, exact replays 2 and 3 returned `9/2/4`, and the
blank-line/trailing-space probes returned `1/10/9`.

The run captured rendered prompt hashes, request-shape hashes, raw response
hashes, and response/parsing traces. The failure remains a serving/repeatability
blocker rather than prompt-learning evidence.
