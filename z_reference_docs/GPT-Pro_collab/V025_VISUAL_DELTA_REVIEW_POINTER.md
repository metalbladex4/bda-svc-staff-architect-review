# v025 Visual Delta Review Pointer

Generated: 2026-05-06
Updated: 2026-05-07

## Package Path

```text
docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v025_visual_delta_prompt_recovery/
```

## Purpose

This package is the first-pass visual delta review lane for comparing the
current Qwen incumbent against the high-recall challenger, then recording the
single approved `v025a` prompt-candidate result and failure autopsy.

## Current Status

The v025 scaffold is complete and published for review. First-pass static
visual review is complete for the priority slice. `v025a` was authored and run
after explicit approval, then rejected.

## Source Candidates

- Incumbent: `v020c_anchor_replay` / `v020c_extra_box_audit`
- Challenger only: `v024l_v023s_no_wheel_track_ablation`
- Rejected candidate: `v025a_v020c_compact_separate_body_recovery`

`v024l` is high-recall learning evidence only. It is not the incumbent.

## v025a Result

- `v025a`: `176` matches / `43` FNs / `35` FPs / `78` errors
- hard disqualifier: case `67` collapsed to `1/10/9`
- controls passed: `155`, `166`, and office-negative
- reopened FP classes: `adjacent_off_target_object` and `nested_fragment_box`
- no `v025b` authored
- `v020c` remains incumbent at `186 / 33 / 25 / 58`
- `v024l` remains high-recall learning evidence only at `188 / 31 / 35 / 66`

## Forbidden Evidence

`v024o_v024l_intact_building_piece_exclusion` is partial and unscored. Do not
score it, copy its outputs, or use it as evidence unless it is rerun fully from
scratch.

## Prompt Boundary

Only `v025a` has been authored in this package. No `v025b` or other follow-up
`detect_objects` prompt candidate has been authored.

## Current Recommendation

Keep `v020c` as incumbent. Do not branch from `v024l`. Do not attempt another
positive separate-body cue in the audit/final-balance region. The v025 autopsy
recommends exactly one next direction if later approved:

```text
D. Run a targeted replay/micro-ablation pack before all-current.
```
