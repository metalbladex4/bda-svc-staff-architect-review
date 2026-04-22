# Experiment Run: 2026-04-06_210720_EDT

## Purpose

Evaluate whether `v009_detect_objects_physical-target-only` improves detection
bbox localization after the `2026-04-06_203823_EDT` run showed `DET-09
bbox_off_target` in both the current-main baseline and `v008`.

## Conditions

- `current-main_baseline`: live current-main prompt config.
- `v009_physical-target-only`: `v009` prompt chain with only `detect_objects`
  changed from `v008`.

## Input

- `tests/data/tank.jpg`

## Notes

- Live `src/bda_svc/pipeline/config.yaml` must be restored after the `v009`
  condition.
- Use temporary debug image export for overlay/crop review.

## Outputs

- `current-main_baseline/tank_2026-04-07_010920Z.json`
- `current-main_baseline/tank_2026-04-07_010920Z_debug/target_0_overlay.jpg`
- `current-main_baseline/tank_2026-04-07_010920Z_debug/target_0_crop.jpg`
- `v009_physical-target-only/effective_config.v009.yaml`
- `v009_physical-target-only/tank_2026-04-07_010925Z.json`
- `v009_physical-target-only/tank_2026-04-07_010925Z_debug/target_0_overlay.jpg`
- `v009_physical-target-only/tank_2026-04-07_010925Z_debug/target_0_crop.jpg`
- `bbox_review_sheet.jpg`

## Result Summary

Current-main baseline:

- detection count: `1`
- target type: `military_equipment`
- damage category: `DESTROYED`
- confidence level: `CONFIRMED`
- exported bbox: `[51, 37, 102, 73]`
- summary issue: stronger functional-impact wording, including "zero combat capability"

`v009_physical-target-only`:

- detection count: `1`
- target type: `military_equipment`
- damage category: `DESTROYED`
- confidence level: `CONFIRMED`
- exported bbox: `[51, 49, 128, 73]`
- assessment issue: `brief_supporting_logic` introduced unsupported subtype wording: "locomotive"
- summary issue: summary repeated unsupported "locomotive" identity and added broader scene details

## Visual Review

The side-by-side review sheet shows that `v009` did not fix the localization
failure. The box moved horizontally and remained over the smoke/plume region
rather than the physical target body.

Failure tags:

- `DET-09 bbox_off_target`
- `AS-06 unsupported_identity_detail`
- `SUM-05 unsupported_identity_detail`

## Decision

Reject `v009` for this seed case. Do not promote it. The next detection prompt
iteration needs a stronger localization strategy than simply adding
physical-target-only exclusion rules.
