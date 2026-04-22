# Experiment Run: 2026-04-06_212840_EDT

## Purpose

Evaluate whether `v010_detect_objects_effect-cue-anchored` improves detection
bbox localization after `v009` failed to correct `DET-09 bbox_off_target`.

## Conditions

- `current-main_baseline`: live current-main prompt config.
- `v010_effect-cue-anchored`: `v010` prompt chain with only `detect_objects`
  changed from `v008`.

## Input

- `tests/data/tank.jpg`

## Method

- Run each condition through the live CLI with temporary debug image export.
- Store JSON, overlay, crop, and effective config artifacts in this timestamped
  run folder.
- Restore `src/bda_svc/pipeline/config.yaml` after the `v010` condition.
- Build a side-by-side bbox review sheet after both conditions finish.

## Pre-Run Expectation

`v010` should use fire, smoke, scorch marks, and debris as cues, then anchor the
bbox to visible solid target structure instead of boxing the smoke or plume
area.

## Outputs

- `current-main_baseline/tank_2026-04-07_013243Z.json`
- `current-main_baseline/tank_2026-04-07_013243Z_debug/target_0_overlay.jpg`
- `current-main_baseline/tank_2026-04-07_013243Z_debug/target_0_crop.jpg`
- `v010_effect-cue-anchored/effective_config.v010.yaml`
- `v010_effect-cue-anchored/tank_2026-04-07_013247Z.json`
- `v010_effect-cue-anchored/tank_2026-04-07_013247Z_debug/target_0_overlay.jpg`
- `v010_effect-cue-anchored/tank_2026-04-07_013247Z_debug/target_0_crop.jpg`
- `bbox_review_sheet.jpg`
- `result_summary.json`

## Result Summary

Current-main baseline:

- detection count: `1`
- target type: `military_equipment`
- damage category: `DESTROYED`
- confidence level: `CONFIRMED`
- exported bbox: `[51, 37, 102, 73]`
- summary issue: stronger functional-impact wording, including "zero combat capability"

Prior comparison points:

- `v008` exported bbox: `[51, 49, 115, 85]`
- rejected `v009` exported bbox: `[51, 49, 128, 73]`

`v010_effect-cue-anchored`:

- detection count: `1`
- target type: `military_equipment`
- damage category: `DESTROYED`
- confidence level: `CONFIRMED`
- exported bbox: `[51, 49, 128, 85]`
- assessment text no longer introduced the unsupported "locomotive" identity detail from `v009`
- summary stayed more conservative than baseline and did not repeat "locomotive"

## Visual Review

The side-by-side review sheet shows that `v010` did not fix the localization
failure. The `v010` box expanded relative to `v009`, but it still covers the
smoke/plume region rather than the physical vehicle/equipment body.

Failure tags:

- `DET-09 bbox_off_target`

## Decision

Reject `v010` for this seed case. Do not promote it. The positive cue strategy
improved the unsupported identity wording compared with `v009`, but it did not
solve bbox placement.
