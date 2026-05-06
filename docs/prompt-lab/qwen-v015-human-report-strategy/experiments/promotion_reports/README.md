# Promotion Reports

This directory records worktree-local promotion/adoption authority for the
human-report-informed Qwen 1.2 prompt lane.

Current approved promotion:

- `qwen_1_2_v017b_group_box_rejection_promotion.yaml`
  - promotes `v017b_group_box_rejection`
  - fold-in surface:
    `src/bda_svc/pipeline/overlays/model_lines/qwen3-vl-8b-instruct.yaml`
  - source gate: `human_report_challenge_v2`
  - case `101` remains diagnostic-only and excluded from forward pass/fail
    gates
