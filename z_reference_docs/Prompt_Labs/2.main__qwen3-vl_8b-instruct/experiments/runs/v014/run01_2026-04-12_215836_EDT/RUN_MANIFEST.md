# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run01_2026-04-12_215836_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v014`
- Input image: `tests/data/tank.jpg`
- Purpose: keep the frozen `v009` working prompt surfaces and the two-pass ROI
  refinement path, but widen the refinement ROI buffer after `v013` showed no
  ROI-local second-pass detections at `0.35`.

## Conditions

### Condition 1: `v009_working_baseline`

- Prompt/config source: merged full config using live current `main` plus the
  frozen `v009` prompt surfaces
- Effective config artifact:
  `v009_working_baseline/effective_config.v009-working-baseline.yaml`
- JSON report:
  `v009_working_baseline/tank_2026-04-13_020326Z.json`
- Debug overlay:
  `v009_working_baseline/tank_2026-04-13_020326Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v009_working_baseline/tank_2026-04-13_020326Z_debug/target_0_crop.jpg`
- Raw pipeline debug:
  `v009_working_baseline/tank_2026-04-13_020326Z_debug/pipeline_debug.json`

Headline result:

- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`
- `metadata.inference_time`: `10.30`

### Condition 2: `v014_candidate`

- Prompt/config source:
  `v014_detect_objects_two-pass-roi-refinement-wide-buffer.yaml`
- Effective config artifact:
  `v014_candidate/effective_config.v014.yaml`
- JSON report:
  `v014_candidate/tank_2026-04-13_020329Z.json`
- Debug overlay:
  `v014_candidate/tank_2026-04-13_020329Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v014_candidate/tank_2026-04-13_020329Z_debug/target_0_crop.jpg`
- Raw pipeline debug:
  `v014_candidate/tank_2026-04-13_020329Z_debug/pipeline_debug.json`

Headline result:

- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 102, 73]`
- `metadata.inference_time`: `3.44`

## Comparison Notes

- The frozen baseline again returned raw detection `[200, 300, 500, 600]`,
  which mapped to `[51, 37, 128, 73]`.
- The `v014` candidate again returned narrowed first-pass raw detection
  `[200, 300, 400, 600]`, which mapped to `[51, 37, 102, 73]`.
- The wider refinement ROI expanded to `[13, 10, 140, 100]`.
- Even with that much larger ROI, the second pass still returned no detections.
- The runtime therefore kept the narrowed first-pass box again.

## Review Artifact

- Side-by-side review sheet:
  `bbox_review_sheet.jpg`

## Initial Decision State

- useful parameter-tuning evidence
- not a bbox win
- suggests ROI width alone is not enough to recover a useful second pass
