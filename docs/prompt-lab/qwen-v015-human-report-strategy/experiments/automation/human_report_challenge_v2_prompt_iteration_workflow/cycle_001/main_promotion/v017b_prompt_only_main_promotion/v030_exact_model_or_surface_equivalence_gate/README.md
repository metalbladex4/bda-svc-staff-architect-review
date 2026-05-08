# v030 Exact Model Or Surface Equivalence Gate

Generated: 2026-05-08T16:08:55Z

Purpose: find a stable model/backend surface close enough to the old Qwen v020c surface to safely resume prompt engineering.

Current product incumbent under prior evidence remains `v020c_anchor_replay / v020c_extra_box_audit` at `186 / 33 / 25 / 58`.

Result: **semantic prompt refinement did not resume**. Exact `Qwen/Qwen3-VL-8B-Instruct` was public and downloaded locally. It could launch via vLLM and via a v030-local Hugging Face Transformers/FastAPI shim, but no exact-model surface completed the Stage 1 BDA case-67 stability gate.

Decision: see `surface_equivalence_decision.md`.
