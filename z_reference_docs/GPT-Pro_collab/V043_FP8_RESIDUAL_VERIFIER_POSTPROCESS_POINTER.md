# V043 FP8 Residual Verifier/Postprocess Pointer

Package path:

`docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v043_fp8_residual_error_verifier_postprocess_loop/`

## Status

v043 is an experiment-only residual-error verifier/postprocessing tranche for the FP8 vLLM model line. It is not promotion, product runtime, or a replacement for old/product v020c.

Starting state:

- Old/product v020c reference: `186 / 33 / 25 / 58`.
- Raw FP8 prompt best, v034a: `181 / 38 / 25 / 63`.
- Composite FP8 best, v034a + p1753: `181 / 38 / 24 / 62`.
- v040 hybrid oracle: `181 / 38 / 22 / 60`, documented as non-deployable.
- v024o remains unscored and forbidden.

Result:

- Best intervention: `pp0157`.
- Type: offline prediction-only postprocess simulation.
- Metrics: `181 / 38 / 20 / 58`.
- Delta vs composite 62: `-4`.
- Delta vs old/product 58 reference: `0`.
- Removed predictions: 4.
- Removed true positives: 0.
- Winning removals: four tiny `military_equipment` false positives in case 66.

Control behavior:

- Case 66 improved from `8 / 0 / 5` to `8 / 0 / 1`.
- Case 67 stayed `10 / 1 / 3`.
- Case 84 stayed `8 / 5 / 0`.
- Case 100 stayed `1 / 2 / 1`.
- Case 110 stayed `3 / 4 / 1`.
- Case 155 stayed `2 / 0 / 1`.
- Case 166 stayed `1 / 0 / 0`.
- Office-negative was not rerun because this tranche was offline-only over frozen outputs.

## Boundaries

- No product/runtime/source-truth mutation.
- No doctrine, assessment prompt, or eval-ground-truth mutation.
- No promotion.
- No live VLM calls.
- No prompt candidate authored or run.
- No raw images, credentials, auth state, API keys, tokens, or raw Codex state copied.

## Next Action

Use visual/crop verifier review to inspect the four case-66 removals and the remaining dense/control residual classes before experiment-only integration or any new prompt work.
