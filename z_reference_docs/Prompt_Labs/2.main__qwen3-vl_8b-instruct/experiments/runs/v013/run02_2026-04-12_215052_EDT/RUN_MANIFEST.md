# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run02_2026-04-12_215052_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v013`
- Input image: `tests/data/tank.jpg`
- Purpose: confirmation repeat of the first code-level grounding aid after
  `v013` run01 narrowed the first-pass box and saw no ROI-local second-pass
  detections.

## Conditions

### Condition 1: `v009_working_baseline`

- Prompt/config source: merged full config using live current `main` plus the
  frozen `v009` prompt surfaces
- Effective config artifact:
  `v009_working_baseline/effective_config.v009-working-baseline.yaml`
- JSON report:
  `v009_working_baseline/tank_2026-04-13_015357Z.json`
- Debug overlay:
  `v009_working_baseline/tank_2026-04-13_015357Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v009_working_baseline/tank_2026-04-13_015357Z_debug/target_0_crop.jpg`
- Raw pipeline debug:
  `v009_working_baseline/tank_2026-04-13_015357Z_debug/pipeline_debug.json`

Headline result:

- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`
- `metadata.inference_time`: `10.20`

### Condition 2: `v013_candidate`

- Prompt/config source:
  `v013_detect_objects_two-pass-roi-refinement.yaml`
- Effective config artifact:
  `v013_candidate/effective_config.v013.yaml`
- JSON report:
  `v013_candidate/tank_2026-04-13_015401Z.json`
- Debug overlay:
  `v013_candidate/tank_2026-04-13_015401Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v013_candidate/tank_2026-04-13_015401Z_debug/target_0_crop.jpg`
- Raw pipeline debug:
  `v013_candidate/tank_2026-04-13_015401Z_debug/pipeline_debug.json`

Headline result:

- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 102, 73]`
- `metadata.inference_time`: `3.48`

## Comparison Notes

- The frozen baseline repeated exactly again with raw detection
  `[200, 300, 500, 600]`.
- The `v013` candidate also repeated exactly again:
  first-pass raw detection `[200, 300, 400, 600]`,
  final bbox `[51, 37, 102, 73]`.
- The refinement ROI again expanded to `[33, 24, 120, 86]`.
- The ROI-local second pass again returned no detections.
- So the runtime again kept the narrowed first-pass box.

## Review Artifact

- Side-by-side review sheet:
  `bbox_review_sheet.jpg`

## Initial Decision State

- confirmed behavior
- not a bbox win
- next likely lever is refinement-parameter tuning rather than another repeat
