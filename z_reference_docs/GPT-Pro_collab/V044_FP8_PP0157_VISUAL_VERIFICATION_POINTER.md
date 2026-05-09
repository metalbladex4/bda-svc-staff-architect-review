# V044 FP8 PP0157 Visual Verification Pointer

Package path:

`docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v044_fp8_pp0157_visual_verification_and_continuation/`

## Status

- pp0157 visual review passed for the four case-66 removals.
- pp0157 is locked as the experiment-only FP8 composite baseline:
  `v034a + p1753 + pp0157 = 181 / 38 / 20 / 58`.
- The four pp0157 removals are tiny far-tail case-66 military-equipment slivers before the first annotated reference target, accepted as low-risk false positives relative to current reference scope.
- Offline continuation found `pp044a_contained_military_equipment_cross_label_probe = 181 / 38 / 18 / 56`.
- pp044a is a cross-label containment probe and requires visual review before deployable integration.
- No VLM call or prompt candidate was run in v044.
- No product/runtime/source-truth/doctrine/assessment/eval-ground-truth mutation occurred.
- No raw images or contact sheets were copied into this review snapshot.
- FP8 vLLM remains a separate experiment-only model line, not a product replacement.

## Next Action

Visual-review pp044a case-100 and case-155 removals, then design a crop/verifier or stricter postprocessor before any prompt wording resumes.
