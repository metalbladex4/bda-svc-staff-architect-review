# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run01_2026-04-12_210945_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v012`
- Input image: `tests/data/tank.jpg`
- Purpose: keep the corrected normalized `xyxy_1000` contract from `v011`,
  return to a stronger contrastive detection prompt, and explicitly resist
  over-shrinking around the most salient burn patch.

## Conditions

### Condition 1: `v009_working_baseline`

- Prompt/config source: merged full config using live current `main` plus the
  frozen `v009` prompt surfaces
- Effective config artifact:
  `v009_working_baseline/effective_config.v009-working-baseline.yaml`
- JSON report:
  `v009_working_baseline/tank_2026-04-13_011024Z.json`
- Debug overlay:
  `v009_working_baseline/tank_2026-04-13_011024Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v009_working_baseline/tank_2026-04-13_011024Z_debug/target_0_crop.jpg`
- Raw pipeline debug:
  `v009_working_baseline/tank_2026-04-13_011024Z_debug/pipeline_debug.json`

Headline result:

- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`
- `metadata.inference_time`: `10.59`

### Condition 2: `v012_candidate`

- Prompt/config source:
  `v012_detect_objects_normalized-full-body-contrastive.yaml`
- Effective config artifact:
  `v012_candidate/effective_config.v012.yaml`
- JSON report:
  `v012_candidate/tank_2026-04-13_011033Z.json`
- Debug overlay:
  `v012_candidate/tank_2026-04-13_011033Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v012_candidate/tank_2026-04-13_011033Z_debug/target_0_crop.jpg`
- Raw pipeline debug:
  `v012_candidate/tank_2026-04-13_011033Z_debug/pipeline_debug.json`

Headline result:

- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 49, 128, 85]`
- `metadata.inference_time`: `8.12`

## Comparison Notes

- `v012` stayed on the corrected normalized contract and returned a valid raw
  detection payload:
  `[200, 400, 500, 700]`
- The frozen baseline again returned:
  `[200, 300, 500, 600]`
- So `v012` did not change the left/right span of the raw box. It moved the
  box downward and made it taller.
- That means the anti-over-shrinking wording did not restore the stronger
  `v006` bbox behavior.
- `v012` preserved the stronger `v009` assessment behavior:
  `DESTROYED` + `PROBABLE`

## Review Artifact

- Side-by-side review sheet:
  `bbox_review_sheet.jpg`

## Initial Decision State

- useful evidence about the current failure mode
- not a bbox win
