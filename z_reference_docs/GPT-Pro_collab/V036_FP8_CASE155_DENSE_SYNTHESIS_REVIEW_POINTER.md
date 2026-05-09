# v036 FP8 Case-155 Dense Synthesis Review Pointer

Generated: `2026-05-09`

## Review Package

- Package: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v036_fp8_case155_dense_synthesis/`
- Final recommendation: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v036_fp8_case155_dense_synthesis/final_recommendation.md`
- Prompt-axis decision: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v036_fp8_case155_dense_synthesis/prompt_axis_decision.md`
- Case-155 synthesis: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v036_fp8_case155_dense_synthesis/case155_fp_synthesis.md`
- Dense regression synthesis: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v036_fp8_case155_dense_synthesis/dense_case_regression_synthesis.md`
- Delta review: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v036_fp8_case155_dense_synthesis/v034a_v035a_delta_review.md`
- Visual taxonomy: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v036_fp8_case155_dense_synthesis/visual_failure_taxonomy.csv`
- Priority-case metrics: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v036_fp8_case155_dense_synthesis/tables/priority_case_metrics.csv`

## Current Status

- Old/product v020c remains incumbent under prior non-FP8 evidence: `186 / 33 / 25 / 58`.
- FP8 vLLM remains a separate model line, not a product replacement.
- FP8 baseline remains `180 / 39 / 32 / 71`.
- v032d remains rejected: `185 / 34 / 57 / 91`.
- v034a remains FP8 working best: `181 / 38 / 25 / 63`.
- v035a remains rejected at micro-pack: `41 / 15 / 19 / 34`.
- v024l remains learning evidence only.
- v025a remains rejected.
- v024o remains partial/unscored and forbidden.

## v036 Synthesis Result

v036 isolated the v035a case-155 gain as a nested same-wreck duplicate/local context box issue, not as a general dense-fragment rejection problem.

- Case 155 v034a: `2/0/1`; remaining FP was a small box at `[18,111,48,143]` inside or overlapping the larger valid wreck at `[13,93,153,176]`.
- Case 155 v035a: `2/0/0`; the nested duplicate/local FP disappeared while valid wreck detections remained.
- Case 66 v035a: `8/0/6`; worsened from v034a `8/0/5`.
- Case 67 v035a: `7/4/5`; collapsed from v034a `10/1/3`.
- Case 84 v035a: `8/5/0`; unchanged from v034a.
- Case 110 v035a: `4/3/2`; controlled relative to v032d, but not enough to offset dense-case regression.

The likely load-bearing risky phrase was the broad guard against `isolated dense-scene marks or partial fragments when the target body center and exterior boundary are not both visible`. Future candidates should avoid dense-scene, partial-fragment, uncertain-fragment, and body-center/exterior-boundary wording.

## Decision

Selected axis: `B` - try a local case-155 FP guard that does not mention dense scenes, partial fragments, or uncertain fragments.

v036 did not author `v036a_fp8_case155_local_fp_guard`. The package recommends a separate candidate tranche only after review, starting from v034a and adding at most one compact same-wreck duplicate-box guard while preserving the v020c extra-box audit and v034a broad-context/scene-box guard.

## Review Question

Is the case-155 nested same-wreck duplicate class sufficiently distinct from dense valid targets in cases 66/67/84 to justify one compact v034a-based same-wreck duplicate-box guard in a follow-up tranche?
