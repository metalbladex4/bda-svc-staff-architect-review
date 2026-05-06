# v017b/v017d Promotion Decision Package

Generated: `2026-05-03T19:59:38.911286+00:00`

This worktree-only package compares `v017b_group_box_rejection` and
`v017d_visual_anchor_lock` after the dev/no101 comparison reopened the primary
candidate decision. It uses the v2 holdout/no101 lane as the next evidence gate
and does not implement promotion or edit runtime configuration.

## Holdout Gate

- Manifest: `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/dev_validation/v017d_v017f_dev_no101/primary_candidate_comparison/promotion_decision_v017b_v017d/validation_manifests/human_report_challenge_v2_holdout_56_no101.yaml`
- Case count: `56`
- Case `101`: excluded
- Positive holdout diagnostic `166`: included
- Source: `stratified_split.json` filtered through
  `human_report_challenge_v2_all_current.yaml`

## Candidate Roles

- `v017b_group_box_rejection`: precision challenger after matching v017d on
  dev/no101 while reducing false positives by 3.
- `v017d_visual_anchor_lock`: stability comparator and prior primary candidate
  after stronger changed-source and updated-report smoke evidence.

## Boundary

This is evaluation evidence only. Promotion, runtime config adoption,
Graphify/Mem0 updates, source-truth changes, and main tracked edits are out of
scope for this package.
