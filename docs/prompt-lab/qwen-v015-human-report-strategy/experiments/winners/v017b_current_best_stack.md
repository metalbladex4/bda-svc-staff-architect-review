# v017b Current Best Stack

Status: `promoted_to_qwen_1_2_model_line_overlay`

`v017b_group_box_rejection` is now the current promoted Qwen 1.2 detection
prompt for the active two-pass-refinement worktree.

## Promotion Surface

- runtime surface:
  `src/bda_svc/pipeline/overlays/model_lines/qwen3-vl-8b-instruct.yaml`
- promotion report:
  `../promotion_reports/qwen_1_2_v017b_group_box_rejection_promotion.yaml`
- candidate overlay:
  `../automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/candidates/v017b/overlay.yaml`

The fold-in uses the model-line overlay rather than direct base
`config.yaml` mutation. Default runtime resolution now applies the v017b
detection prompt without `--experiment-overlay`.

## Evidence Summary

`v017b` became the promotion candidate after the fresh same-image comparison
against `v017d_visual_anchor_lock`:

- dev+holdout no101: `152` matches, `56` false negatives, `17` false positives
  across `111` images
- delta versus `v017d`: `+1` match, `-1` false negative, `-4` false positives
- final all-current no101: `158` matches, `61` false negatives, `25` false
  positives across `117` images
- positive `155`: `2` matches, `0` false negatives, `0` false positives
- positive `166`: `1` match, `0` false negatives, `0` false positives
- office-negative abstention: passed with `0` negative-scene false positives

## Policy Boundary

Case `101` remains diagnostic-only. It is excluded from forward pass/fail gates
because its reference/evaluation shape made it a poor promotion blocker.

This winner note records the active worktree state only. Promotion into `main`,
remote branches, project-brain memory, or broader docs requires separate
approval and validation.
