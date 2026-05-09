# v032 Qwen3-VL FP8 vLLM Model-Line Prompt Refinement

This package records a separate model-line prompt-engineering tranche for the stable vLLM FP8 Qwen surface:

- Model line: `qwen3-vl-8b-instruct-fp8-vllm`.
- Backend: vLLM OpenAI-compatible server.
- Model: `Qwen/Qwen3-VL-8B-Instruct-FP8`.
- Endpoint: `http://localhost:8000/v1` during this run.

This is not a promotion path and not a replacement for the old product v020c prompt. The old product reference remains `186 / 33 / 25 / 58`. The FP8 model-line baseline remains `180 / 39 / 32 / 71`.

The tranche paused because `v032d_fp8_v019c_anchor_replay` timed out during full all-current on case 110. Its full result is invalid and unscored.

Read in order:

1. `source_manifest.json`
2. `model_line_manifest.json`
3. `comparison_matrix.md`
4. `diagnoses/v032_runtime_timeout_case110_diagnosis.md`
5. `final_recommendation.md`
6. `strategy_state.md`
