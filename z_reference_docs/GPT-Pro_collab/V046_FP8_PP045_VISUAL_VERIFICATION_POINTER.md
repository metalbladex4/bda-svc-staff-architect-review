# V046 FP8 PP045 Visual Verification Pointer

Package path:
`docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v046_fp8_pp045_visual_verification_and_continuation/`

Status:
- Experiment-only FP8 vLLM evidence tranche.
- No promotion and no product/runtime/source-truth mutation.
- pp045b visual review passed.
- pp045c visual review passed.
- Locked experiment-only baseline: `fp8_composite_pp045c_baseline = 181 / 38 / 11 / 49`.
- pp046a prediction-only residual cleanup probe reached `181 / 38 / 0 / 38` with 0 after-the-fact TP removals, but is simulation-only and still needs visual review before baseline lock.
- Raw/product reference remains old v020c under prior evidence: `186 / 33 / 25 / 58`.
- FP8 remains a separate model line and is not a product replacement.
- v024o remains partial/unscored and forbidden.
- Review images/contact sheets are local-only and are not included in this private review snapshot.

Next action:
Visual-review pp046a removals, then design verifier/recovery work for the remaining 38 FNs.
