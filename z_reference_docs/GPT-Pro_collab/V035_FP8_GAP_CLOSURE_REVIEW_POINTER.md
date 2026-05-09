# v035 FP8 Gap Closure Review Pointer

Generated: `2026-05-09`

## Review Package

- Package: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v035_fp8_vllm_gap_closure_autonomous/`
- Final recommendation: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v035_fp8_vllm_gap_closure_autonomous/final_recommendation.md`
- Candidate diagnosis: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v035_fp8_vllm_gap_closure_autonomous/diagnoses/v035a_fp8_dense_uncertain_fragment_guard_diagnosis.md`
- Comparison matrix: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v035_fp8_vllm_gap_closure_autonomous/comparison_matrix.md`
- Strategy state: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v035_fp8_vllm_gap_closure_autonomous/strategy_state.md`
- Candidate overlay: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v035_fp8_vllm_gap_closure_autonomous/overlays/v035a_fp8_dense_uncertain_fragment_guard.yaml`

## Current Status

- Old/product v020c remains incumbent under prior non-FP8 evidence: `186 / 33 / 25 / 58`.
- FP8 vLLM remains a separate model line, not a product replacement.
- FP8 baseline remains `180 / 39 / 32 / 71`.
- v032d remains rejected: `185 / 34 / 57 / 91`.
- v034a remains FP8 working best: `181 / 38 / 25 / 63`.
- v024l remains learning evidence only.
- v025a remains rejected.
- v024o remains partial/unscored and forbidden.

## v035 Result

`v035a_fp8_dense_uncertain_fragment_guard` was rejected at micro-pack:

- Micro-pack: `41 / 15 / 19 / 34`.
- Case 66: `8/0/6`.
- Case 67: `7/4/5`; hard dense-case gate failure.
- Case 84: `8/5/0`.
- Case 110: `4/3/2`.
- Case 155: `2/0/0`; useful local FP improvement.
- Case 166: `1/0/0`.
- Office-negative: pass.
- Full all-current was not run.

## Review Question

Does the case-155 gain justify a more local visual/eval artifact synthesis before another prompt candidate, or should v035 confirm that dense-fragment rejection wording is too risky for the FP8 line?
