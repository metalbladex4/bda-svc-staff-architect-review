# v2 Prompt-Iteration Live Decision Packet

- candidate: `v017b`
- classification: `near_miss`
- passed gates: `false`

## Recommended User Decision

review v017b failure/near-miss evidence before authoring the next candidate

## Gate Summary

### v2 hinge 12

- passed: `false`
- totals: `24` matches, `33` FNs, `13` FPs
- checks: `case_101_diagnostic=false`, `false_negative_count=true`, `false_positive_count=true`, `match_count=true`, `positive_control_155=true`
- positive control: `155` match_count=`2`, passed=`true`
- case `101`: detections=`1`, row_fragment_groups=`0`, broad_group_boxes=`1`, passed=`false`
- case `101` broad box: `[75, 58, 1000, 547]` area_ratio=`0.43137073516845703`

### changed-source sanity

- passed: `true`
- totals: `9` matches, `3` FNs, `0` FPs
- checks: `false_negative_count=true`, `false_positive_count=true`, `match_count=true`, `positive_control_155=true`
- positive control: `155` match_count=`2`, passed=`true`

### office-negative abstention

- passed: `true`
- totals: `1` matches, `0` FNs, `0` FPs
- checks: `negative_scene_abstention_correct_count=true`, `negative_scene_count=true`, `negative_scene_false_positive_count=true`

### updated-report smoke

- summary: `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/runs/v017b/live_2026-05-03_032920Z/human_report_challenge_v2_updated_report_smoke_2026-05-03_033207Z/candidate_manifest_run_summary.json`
- returncode: `0`
- totals: `22` matches, `9` FNs, `1` FPs
