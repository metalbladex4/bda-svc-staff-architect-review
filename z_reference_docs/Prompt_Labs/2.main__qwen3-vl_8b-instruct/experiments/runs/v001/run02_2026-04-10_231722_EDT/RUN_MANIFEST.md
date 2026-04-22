# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run02_2026-04-10_231722_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v001`
- Input image: `tests/data/tank.jpg`
- Purpose: repeat the `v001` comparison round to test whether the baseline and
  candidate behaviors are stable across a second run.

## Conditions

### Condition 1: `current-main_baseline`

- Prompt/config source: live current `main` baseline at `c077cd8`
- Effective config artifact:
  `current-main_baseline/effective_config.baseline.yaml`
- JSON report:
  `current-main_baseline/tank_2026-04-11_031823Z.json`
- Debug overlay:
  `current-main_baseline/tank_2026-04-11_031823Z_debug/target_0_overlay.jpg`
- Debug crop:
  `current-main_baseline/tank_2026-04-11_031823Z_debug/target_0_crop.jpg`

Headline result:

- `target_0.target_type`: `military_equipment`
- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`
- `metadata.inference_time`: `14.72`

### Condition 2: `v001_candidate`

- Prompt/config source: `v001_detect_objects_visible-boundary-tightening.yaml`
- Effective config artifact:
  `v001_candidate/effective_config.v001.yaml`
- JSON report:
  `v001_candidate/tank_2026-04-11_031847Z.json`
- Debug overlay:
  `v001_candidate/tank_2026-04-11_031847Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v001_candidate/tank_2026-04-11_031847Z_debug/target_0_crop.jpg`

Headline result:

- `target_0.target_type`: `military_equipment`
- `damage_category`: `DESTROYED`
- `confidence_level`: `CONFIRMED`
- `target_0.bounding_box`: `[56, 46, 123, 85]`
- `metadata.inference_time`: `5.48`

## Stability Notes

- The baseline repeated exactly from `run01`:
  - bbox stayed `[51, 37, 128, 73]`
  - confidence stayed `PROBABLE`
  - supporting logic stayed materially the same
- `v001` did not repeat exactly:
  - `run01` bbox: `[56, 46, 123, 79]`
  - `run02` bbox: `[56, 46, 123, 85]`
- `v001` did stay directionally consistent:
  - confidence remained `CONFIRMED`
  - subtype wording still drifted toward `locomotive`
  - summary still added rail/logistics implications

## Review Artifact

- Side-by-side overlay/crop review:
  `bbox_review_sheet.jpg`

## Initial Decision State

- The baseline appears stable across repeated runs.
- `v001` appears only partially stable: its general direction is consistent,
  but bbox placement still shifts and remains visually questionable.
- This repeat run supports the view that `v001` is not a clean enough win to
  promote.
