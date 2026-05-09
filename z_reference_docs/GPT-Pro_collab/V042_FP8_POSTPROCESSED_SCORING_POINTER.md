# V042 FP8 Postprocessed Scoring Review Pointer

Generated: `2026-05-09`

## Package

`docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v042_fp8_postprocessed_scoring_autonomous/`

## Current Status

Current pause reason: backend unavailable.

The v042 package was created as an experiment-only FP8 vLLM postprocessed-scoring tranche. It recovered and pinned the deployable prediction-only `p1753` rule, then stopped before live prompt execution because the local vLLM FP8 endpoint was unavailable.

## Verified Checkpoint

- p1753 reproduced on frozen v034a.
- Raw v034a: `181 / 38 / 25 / 63`.
- v034a + p1753: `181 / 38 / 24 / 62`.
- p1753 removed `1` false positive and `0` true positives.
- v042a overlay was authored but not run.
- No VLM candidate run occurred before pause.
- No product/runtime/source-truth mutation occurred.

## Next Action

Restart the vLLM FP8 endpoint for `Qwen/Qwen3-VL-8B-Instruct-FP8`, then resume v042 from the package pause report:

`docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v042_fp8_postprocessed_scoring_autonomous/pause_report_2026-05-09_185419Z_backend_unavailable.md`

This pointer is review evidence only. It is not a promotion, not a product replacement, and not product runtime truth.

## Resume Addendum

The vLLM FP8 endpoint was restarted and validated on `2026-05-09`.

Live candidate outcomes after resume:

- `v042a_fp8_case84_low_contrast_recall_probe`: rejected at micro-pack.
- `v042b_fp8_mostly_context_box_guard`: rejected at micro-pack.
- `v042c_fp8_uncertain_fragments_phrase_ablation`: rejected at micro-pack.
- `v042d_fp8_final_balance_simplification`: rejected at micro-pack.
- `v042e_fp8_separate_small_target_row_exception`: rejected at micro-pack.

Best raw FP8 prompt remains `v034a_fp8_broad_context_scene_box_guard = 181 / 38 / 25 / 63`.
Best experiment-only postprocessed result remains `v034a + p1753 = 181 / 38 / 24 / 62`.

No resumed candidate beat composite 62, reached the old 58-error reference, or reached the <=1 target. The current recommendation is to pause near-neighbor prompt wording and move next to verifier/postprocessing or visual review of the remaining v034a+p1753 deltas.
