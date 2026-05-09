# V033 FP8 Timeout Repair Review Pointer

Purpose: point GPT-5.5 Pro and reviewers to the v033 FP8 vLLM timeout repair and clean v032d replay evidence.

Package path:

`docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v033_fp8_timeout_repair_and_v032d_replay/`

Key files:

- `timeout_case110_diagnosis.md/json`
- `retry_policy_design.md/json`
- `v032d_full_replay_summary.md/json`
- `comparison_matrix.md/json`
- `diagnoses/v033_v032d_clean_replay_diagnosis.md`
- `final_recommendation.md/json`
- `strategy_state.md`
- `lessons_learned.md`
- `recovery_log.md/json`

Current status:

- Case 110 timeout was diagnosed and repaired with experiment-only instrumentation.
- v033 used a 180-second per-request timeout, max 2 retries, and 5-second cooldown. Product runtime was not changed.
- Case 110 completed for both FP8 baseline and v032d under the policy.
- v032d clean full all-current completed all 117 no101 images with no retries.
- v032d full metrics: `185 / 34 / 57 / 91`.
- v032d is rejected and did not become the FP8 working best.
- Autonomous FP8 prompt refinement did not resume.
- Old/product v020c remains incumbent under prior evidence: `186 / 33 / 25 / 58`.
- FP8 baseline remains `180 / 39 / 32 / 71`.
- v024l remains learning evidence only, v025a remains rejected, and v024o remains forbidden as scored evidence.

Review question:

Given that v032d fixed case 155 but exploded full-run false positives, especially case 110, should the FP8 line pivot to a precision-only guard/hybrid from v020c, or should FP8 prompt work pause in favor of model/backend or non-prompt suppression work?
