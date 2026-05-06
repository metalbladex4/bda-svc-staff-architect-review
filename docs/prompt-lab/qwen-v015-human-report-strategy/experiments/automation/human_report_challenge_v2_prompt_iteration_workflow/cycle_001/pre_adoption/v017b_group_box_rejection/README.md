# v017b Pre-Adoption Check

Generated: `2026-05-03T20:23:03.264704+00:00`

This package runs the final evaluation evidence for
`v017b_group_box_rejection` before any runtime adoption decision. It is
evaluation-only and does not edit runtime config.

## Gates

- Final smoke:
  - changed-source sanity
  - updated-report smoke
  - office-negative abstention
- Final broad pack:
  - `human_report_challenge_v2_all_current_117_no101`

Case `101` is excluded because the current policy treats it as diagnostic-only,
not a forward pass/fail gate. Cases `155` and `166` remain positive controls in
the all-current/no101 pack.
