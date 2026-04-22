# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run01_2026-04-12_201305_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v010`
- Input image: `tests/data/tank.jpg`
- Purpose: test whether switching the confirmed `v006`/`v009` direction from `xyxy_1000` to `xyxy_pixels` improves grounding and bbox placement before opening a summary-only cycle.

## Conditions

### Condition 1: `v009_working_baseline`

- Prompt/config source: merged full config using live current `main` plus the frozen `v009` prompt surfaces
- Effective config artifact:
  `v009_working_baseline/effective_config.v009-working-baseline.yaml`
- JSON report:
  `v009_working_baseline/tank_2026-04-13_001638Z.json`
- Debug overlay:
  `v009_working_baseline/tank_2026-04-13_001638Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v009_working_baseline/tank_2026-04-13_001638Z_debug/target_0_crop.jpg`

Headline result:

- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`
- `metadata.inference_time`: `10.88`

### Condition 2: `v010_candidate`

- Prompt/config source: `v010_detect_objects_pixels-native-grounding.yaml`
- Effective config artifact:
  `v010_candidate/effective_config.v010.yaml`
- Command note:
  The version file is a prompt-surface wrapper plus a code-supported `runtime_overrides` block. The candidate run used a merged full config generated from the live baseline plus the `v010` detection override and `xyxy_pixels` bbox convention. That merged config was swapped into `src/bda_svc/pipeline/config.yaml` for the run and the live config was restored immediately afterward.
- JSON report:
  `v010_candidate/tank_2026-04-13_001640Z.json`
- Debug overlay / crop:
  none generated because the candidate returned no detected targets

Headline result:

- `damage_category`: `NOT APPLICABLE`
- `confidence_level`: `CONFIRMED`
- `target_0.target_type`: `object_not_found`
- `target_0.bounding_box`: `[0, 0, 0, 0]`
- `metadata.inference_time`: `1.64`

## Comparison Notes

- `v010` changes detection coordinates from normalized `xyxy_1000` to native `xyxy_pixels` while keeping the best-known assessment prompt frozen.
- On `tank.jpg`, that change collapsed the detection stage entirely and produced `object_not_found`.
- Because no targets were detected, the candidate generated no overlay/crop review artifacts.
- This is a stronger failure than a slightly worse bbox: the `_pixels` change broke detection for this seed case.

## Review Artifact

- Side-by-side review sheet:
  `bbox_review_sheet.jpg`

## Initial Decision State

- reject `v010` as the first `_pixels` grounding tactic on this image/model path
