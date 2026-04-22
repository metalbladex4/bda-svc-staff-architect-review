# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run01_2026-04-12_165427_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v009`
- Input image: `tests/data/tank.jpg`
- Purpose: test whether a short, example-anchored `assess_damage` prompt can
  recover `DESTROYED` + `PROBABLE` while keeping generic target wording and
  preserving the cycle-2 conservative tone.

## Conditions

### Condition 1: `v007_working_baseline`

- Prompt/config source: merged full config using live current `main` plus the
  `v007` `detect_objects` and `assess_damage` overrides
- Effective config artifact:
  `v007_working_baseline/effective_config.v007-working-baseline.yaml`
- JSON report:
  `v007_working_baseline/tank_2026-04-12_205513Z.json`
- Debug overlay:
  `v007_working_baseline/tank_2026-04-12_205513Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v007_working_baseline/tank_2026-04-12_205513Z_debug/target_0_crop.jpg`

Headline result:

- `damage_category`: `DAMAGED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`

### Condition 2: `v009_candidate`

- Prompt/config source: `v009_assess_damage_example-anchored-generic-target.yaml`
- Effective config artifact:
  `v009_candidate/effective_config.v009.yaml`
- JSON report:
  `v009_candidate/tank_2026-04-12_205541Z.json`
- Debug overlay:
  `v009_candidate/tank_2026-04-12_205541Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v009_candidate/tank_2026-04-12_205541Z_debug/target_0_crop.jpg`

Headline result:

- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`

## Comparison Notes

- `v009` restored the target-level category from `DAMAGED` back to
  `DESTROYED`.
- `v009` kept `PROBABLE` confidence instead of sliding back to `CONFIRMED`.
- `v009` removed subtype drift from `brief_supporting_logic`.
- `v009` did not change bbox behavior in this loop; both conditions stayed at
  `[51, 37, 128, 73]`.
- Remaining watch items:
  - summary still says `dirt track`
  - summary still reaches for complete operational loss language

## Review Artifact

- Side-by-side overlay/crop review:
  `bbox_review_sheet.jpg`

## Initial Decision State

- `v009` is the best assessment candidate from cycle 02.
- It is not the full downstream winner because summary calibration still
  drifts.
- The next cycle should freeze `v009` target-level assessment behavior and
  focus on `summarize_scene`.
