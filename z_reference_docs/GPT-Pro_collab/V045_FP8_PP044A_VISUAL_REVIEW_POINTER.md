# V045 FP8 PP044A Visual Review Pointer

Package path:

`docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v045_fp8_pp044a_cross_label_visual_review/`

## Status

- pp044a visual review passed for case 100 and case 155.
- pp044a is locked as the experiment-only FP8 composite baseline:
  `v034a + p1753 + pp0157 + pp044a = 181 / 38 / 18 / 56`.
- Case 100 removal is accepted as a true false positive: the removed `military_equipment` box is a civilian-looking parked vehicle inside a damaged building scene.
- Case 155 removal is accepted as the known same-wreck local duplicate nested inside the larger valid wreck body.
- Offline continuation found:
  - `pp045b_tiny_upper_right_sparse_military_probe = 181 / 38 / 15 / 53`
  - `pp045c_small_lower_building_context_probe = 181 / 38 / 11 / 49`
- pp045b and pp045c are simulation-only until their removed boxes receive visual review.
- No VLM call or prompt candidate was run in v045.
- No product/runtime/source-truth/doctrine/assessment/eval-ground-truth mutation occurred.
- No raw images or contact sheets were copied into this review snapshot.
- FP8 vLLM remains a separate experiment-only model line, not a product replacement.

## Next Action

Visual-review pp045b case-28 removals and pp045c building-context removals, then design a crop/verifier check for remaining residual FNs before any prompt wording resumes.
