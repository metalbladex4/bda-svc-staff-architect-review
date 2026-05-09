# v034 FP8 Precision Recovery Review Pointer

Generated: `2026-05-09`

## Review Package

- Package: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v034_fp8_vllm_precision_recovery_autonomous/`
- Final recommendation: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v034_fp8_vllm_precision_recovery_autonomous/final_recommendation.md`
- Candidate diagnosis: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v034_fp8_vllm_precision_recovery_autonomous/diagnoses/v034a_fp8_broad_context_scene_box_guard_diagnosis.md`
- Comparison matrix: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v034_fp8_vllm_precision_recovery_autonomous/comparison_matrix.md`
- Live metrics log: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v034_fp8_vllm_precision_recovery_autonomous/live_metrics_log.md`
- Strategy state: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v034_fp8_vllm_precision_recovery_autonomous/strategy_state.md`
- Candidate overlay: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v034_fp8_vllm_precision_recovery_autonomous/overlays/v034a_fp8_broad_context_scene_box_guard.yaml`

## Status

- Old/product v020c remains incumbent under prior non-FP8 evidence: `186 / 33 / 25 / 58`.
- FP8 vLLM remains a separate model line, not a product replacement.
- FP8 baseline remains `v020c_fp8_vllm_baseline = 180 / 39 / 32 / 71`.
- v032d remains rejected after clean v033 replay: `185 / 34 / 57 / 91`.
- v024l remains learning evidence only.
- v025a remains rejected.
- v024o remains partial/unscored and forbidden.

## v034 Result

`v034a_fp8_broad_context_scene_box_guard` became the new FP8 working best:

- Full all-current/no101: `181 / 38 / 25 / 63`.
- Delta versus FP8 baseline: `-8` combined errors.
- Delta versus old v020c reference: `+5` combined errors.
- Case 67: `10/1/3`.
- Case 110: `3/4/1`.
- Case 155: `2/0/1`.
- Case 166: `1/0/0`.
- Office-negative: pass.

## Review Question

Does v034a provide a strong enough FP8 model-line improvement to justify a follow-up tranche from v034a toward the old 58-error reference, while keeping FP8 separate from product v020c?
