# v025 Visual Delta Review Pointer

Generated: 2026-05-06

## Package Path

```text
docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v025_visual_delta_prompt_recovery/
```

## Purpose

This package is the first-pass visual delta review lane for comparing the
current Qwen incumbent against the high-recall challenger before any new prompt
candidate is authored.

## Current Status

The v025 scaffold has been created and published for review. First-pass static
visual review is pending or in progress.

## Source Candidates

- Incumbent: `v020c_anchor_replay` / `v020c_extra_box_audit`
- Challenger only: `v024l_v023s_no_wheel_track_ablation`

`v024l` is high-recall learning evidence only. It is not the incumbent.

## Forbidden Evidence

`v024o_v024l_intact_building_piece_exclusion` is partial and unscored. Do not
score it, copy its outputs, or use it as evidence unless it is rerun fully from
scratch.

## Prompt Boundary

No `v025a` or other `detect_objects` prompt candidate has been authored in this
package.
