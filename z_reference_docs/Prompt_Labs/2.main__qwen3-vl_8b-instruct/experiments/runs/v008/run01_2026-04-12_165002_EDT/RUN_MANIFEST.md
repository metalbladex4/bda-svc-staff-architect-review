# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run01_2026-04-12_165002_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v008`
- Input image: `tests/data/tank.jpg`
- Purpose: test whether explicit `CATEGORY GUIDANCE` can recover
  `DESTROYED` while preserving the more conservative `PROBABLE` confidence and
  non-K-kill wording from `v007`.

## Conditions

### Condition 1: `v007_working_baseline`

- Prompt/config source: merged full config using live current `main` plus the
  `v007` `detect_objects` and `assess_damage` overrides
- Effective config artifact:
  `v007_working_baseline/effective_config.v007-working-baseline.yaml`
- JSON report:
  `v007_working_baseline/tank_2026-04-12_205140Z.json`
- Debug overlay:
  `v007_working_baseline/tank_2026-04-12_205140Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v007_working_baseline/tank_2026-04-12_205140Z_debug/target_0_crop.jpg`

Headline result:

- `damage_category`: `DAMAGED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`

### Condition 2: `v008_candidate`

- Prompt/config source: `v008_assess_damage_destroyed-probable-burn-rule.yaml`
- Effective config artifact:
  `v008_candidate/effective_config.v008.yaml`
- JSON report:
  `v008_candidate/tank_2026-04-12_205203Z.json`
- Debug overlay:
  `v008_candidate/tank_2026-04-12_205203Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v008_candidate/tank_2026-04-12_205203Z_debug/target_0_crop.jpg`

Headline result:

- `damage_category`: `DAMAGED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`

## Comparison Notes

- `v008` did not recover `DESTROYED`; category and confidence stayed identical to
  the `v007_working_baseline` condition in this run.
- `v008` also did not change bbox behavior in this run.
- Regression:
  - subtype drift reappeared in `brief_supporting_logic` (`locomotive`)
  - summary now talks about rail transport disruption, which is more coherent to
    the visible scene but still depends on subtype inference we do not want

## Review Artifact

- Side-by-side overlay/crop review:
  `bbox_review_sheet.jpg`

## Initial Decision State

- `v008` is not a winner.
- The abstract category guidance did not move the model.
- The next attempt should favor a short, concrete assessment example rather than
  more abstract rules.
