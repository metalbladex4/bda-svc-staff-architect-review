# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run01_2026-04-12_212440_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v013`
- Input image: `tests/data/tank.jpg`
- Purpose: keep the frozen `v009` working prompt surfaces and test the new
  two-pass ROI refinement runtime aid in isolation.

## Conditions

### Condition 1: `v009_working_baseline`

- Prompt/config source: merged full config using live current `main` plus the
  frozen `v009` prompt surfaces
- Effective config artifact:
  `v009_working_baseline/effective_config.v009-working-baseline.yaml`
- JSON report:
  `v009_working_baseline/tank_2026-04-13_012623Z.json`
- Debug overlay:
  `v009_working_baseline/tank_2026-04-13_012623Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v009_working_baseline/tank_2026-04-13_012623Z_debug/target_0_crop.jpg`
- Raw pipeline debug:
  `v009_working_baseline/tank_2026-04-13_012623Z_debug/pipeline_debug.json`

Headline result:

- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`
- `metadata.inference_time`: `10.66`

### Condition 2: `v013_candidate`

- Prompt/config source:
  `v013_detect_objects_two-pass-roi-refinement.yaml`
- Effective config artifact:
  `v013_candidate/effective_config.v013.yaml`
- JSON report:
  `v013_candidate/tank_2026-04-13_012627Z.json`
- Debug overlay:
  `v013_candidate/tank_2026-04-13_012627Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v013_candidate/tank_2026-04-13_012627Z_debug/target_0_crop.jpg`
- Raw pipeline debug:
  `v013_candidate/tank_2026-04-13_012627Z_debug/pipeline_debug.json`

Headline result:

- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 102, 73]`
- `metadata.inference_time`: `3.45`

## Comparison Notes

- The frozen baseline again returned raw detection `[200, 300, 500, 600]`,
  which mapped to `[51, 37, 128, 73]`.
- The `v013` candidate first pass returned narrower raw detection
  `[200, 300, 400, 600]`, which mapped to `[51, 37, 102, 73]`.
- The code-level refinement pass then expanded an ROI to
  `[33, 24, 120, 86]`, but the second pass returned no detections inside that
  ROI.
- Because no refined child box was found, the runtime kept the narrowed
  first-pass box as the final result.
- `v013` preserved the stronger `v009` assessment behavior:
  `DESTROYED` + `PROBABLE`

## Review Artifact

- Side-by-side review sheet:
  `bbox_review_sheet.jpg`

## Initial Decision State

- useful evidence about the first code-level grounding aid
- not a bbox win
- needs a repeat before we can cleanly separate refinement value from first-pass
  detection wobble
