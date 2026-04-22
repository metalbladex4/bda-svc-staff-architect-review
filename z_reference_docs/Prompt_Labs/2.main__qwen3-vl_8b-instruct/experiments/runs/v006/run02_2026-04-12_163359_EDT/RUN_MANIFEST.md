# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run02_2026-04-12_163359_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v006`
- Input image: `tests/data/tank.jpg`
- Purpose: confirmation repeat for the best-so-far bbox candidate after
  `v006` run01 showed the first materially improved target-body grounding in
  the active sequence.

## Conditions

### Condition 1: `current-main_baseline`

- Prompt/config source: live current `main` baseline at upstream commit
  `21deaf5`
- Effective config artifact:
  `current-main_baseline/effective_config.baseline.yaml`
- JSON report:
  `current-main_baseline/tank_2026-04-12_203415Z.json`
- Debug overlay:
  `current-main_baseline/tank_2026-04-12_203415Z_debug/target_0_overlay.jpg`
- Debug crop:
  `current-main_baseline/tank_2026-04-12_203415Z_debug/target_0_crop.jpg`

Headline result:

- `target_0.target_type`: `military_equipment`
- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`

### Condition 2: `v006_candidate`

- Prompt/config source: `v006_detect_objects_short-contrastive-example.yaml`
- Effective config artifact:
  `v006_candidate/effective_config.v006.yaml`
- Command note:
  The candidate run used the same merged-config swap-and-restore method as
  `v006` run01. Post-run verification showed no diff in the live config.
- JSON report:
  `v006_candidate/tank_2026-04-12_203421Z.json`
- Debug overlay:
  `v006_candidate/tank_2026-04-12_203421Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v006_candidate/tank_2026-04-12_203421Z_debug/target_0_crop.jpg`

Headline result:

- `target_0.target_type`: `military_equipment`
- `damage_category`: `DESTROYED`
- `confidence_level`: `CONFIRMED`
- `target_0.bounding_box`: `[46, 46, 128, 92]`

## Confirmation Outcome

- `v006` run02 matched `v006` run01 exactly on:
  - `bounding_box`: `[46, 46, 128, 92]`
  - `confidence_level`: `CONFIRMED`
  - `brief_supporting_logic`
  - summary text
- The visual review sheet again shows the `v006` bbox placed materially more on
  the visible burning target body than the baseline bbox.

## Decision State

- The bbox improvement from `v006` now looks repeatable on the current seed
  case.
- That closes the question of whether the bbox gain was a one-off.
- The next prompt problem should shift from bbox localization to downstream
  confidence and summary calibration before any promotion decision is made.
