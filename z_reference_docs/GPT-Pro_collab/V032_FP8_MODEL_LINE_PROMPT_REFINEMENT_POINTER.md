# V032 FP8 Model-Line Prompt Refinement Pointer

Purpose: point GPT-5.5 Pro and reviewers to the v032 separate model-line prompt-engineering evidence for the stable vLLM FP8 Qwen surface.

Package path:

`docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v032_qwen3vl_fp8_vllm_model_line_prompt_refinement/`

Key files:

- `README.md`
- `model_line_manifest.json`
- `comparison_matrix.md`
- `comparison_matrix.json`
- `live_metrics_log.md`
- `diagnoses/v032_runtime_timeout_case110_diagnosis.md`
- `diagnoses/v032d_fp8_v019c_anchor_replay_diagnosis.md`
- `final_recommendation.md`
- `final_recommendation.json`
- `strategy_state.md`
- `lessons_learned.md`
- `pause_report_2026-05-08_runtime_timeout_case110.md`

Current status:

- Old/product v020c remains incumbent under prior evidence: `186 / 33 / 25 / 58`.
- FP8 vLLM is a separate model line, not a product replacement.
- FP8 vLLM baseline remains `180 / 39 / 32 / 71`.
- v032 candidates did not produce a complete all-current improvement.
- v032 paused because `v032d_fp8_v019c_anchor_replay` timed out during full all-current on case 110.
- v032d micro evidence suggests FP reduction and case-155 improvement, but with dense recall tradeoffs and no valid full score.
- v024l remains learning evidence only; v025a remains rejected; v024o remains forbidden as scored evidence.

Review question:

Should the FP8 model line continue after fixing the full-run timeout/retry policy, and should the next prompt axis be a small v019c/v020c hybrid that preserves v020c dense recall while reducing FP8-specific case-155 FP pressure?
