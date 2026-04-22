# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run01_2026-04-12_204418_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v011`
- Input image: `tests/data/tank.jpg`
- Purpose: recover from the failed `v010` `_pixels` swap by returning to the
  frozen `v009` working baseline and testing a normalized-coordinate,
  point-first detection prompt that stays closer to Qwen3-VL's apparent native
  grounding regime.

## Conditions

### Condition 1: `v009_working_baseline`

- Prompt/config source: merged full config using live current `main` plus the
  frozen `v009` prompt surfaces
- Effective config artifact:
  `v009_working_baseline/effective_config.v009-working-baseline.yaml`
- JSON report:
  `v009_working_baseline/tank_2026-04-13_004625Z.json`
- Debug overlay:
  `v009_working_baseline/tank_2026-04-13_004625Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v009_working_baseline/tank_2026-04-13_004625Z_debug/target_0_crop.jpg`
- Raw pipeline debug:
  `v009_working_baseline/tank_2026-04-13_004625Z_debug/pipeline_debug.json`

Headline result:

- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`
- `metadata.inference_time`: `10.56`

### Condition 2: `v011_candidate`

- Prompt/config source:
  `v011_detect_objects_qwen-native-normalized-point-first.yaml`
- Effective config artifact:
  `v011_candidate/effective_config.v011.yaml`
- JSON report:
  `v011_candidate/tank_2026-04-13_004628Z.json`
- Debug overlay:
  `v011_candidate/tank_2026-04-13_004628Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v011_candidate/tank_2026-04-13_004628Z_debug/target_0_crop.jpg`
- Raw pipeline debug:
  `v011_candidate/tank_2026-04-13_004628Z_debug/pipeline_debug.json`

Headline result:

- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[56, 46, 123, 76]`
- `metadata.inference_time`: `3.13`

## Comparison Notes

- `v011` successfully recovered detection after `v010` collapsed to
  `object_not_found`.
- The new `pipeline_debug.json` confirms the candidate returned a valid
  normalized `xyxy_1000` detection:
  `[220, 375, 480, 625]`, which mapped to pixel bbox `[56, 46, 123, 76]`.
- The baseline returned normalized detection `[200, 300, 500, 600]`, which
  mapped to `[51, 37, 128, 73]`.
- So the main thing `v011` proved is that the `v010` failure was very likely a
  coordinate-contract problem, not a general inability to detect the target.
- Numerically, the recovered `v011` box is much closer to the older
  `v001` / `v002` family than to the stronger `v006` bbox win.
- `v011` preserved the stronger `v009` assessment behavior:
  `DESTROYED` + `PROBABLE`, with no target-level subtype drift.

## Review Artifact

- Side-by-side review sheet:
  `bbox_review_sheet.jpg`

## Initial Decision State

- useful recovery from `v010`
- not yet a clear grounding win over the frozen `v009` working baseline
