# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run01_2026-04-10_234135_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v002`
- Input image: `tests/data/tank.jpg`
- Purpose: compare the fresh current-main baseline against the second
  detection-only candidate in the restarted `qwen3-vl:8b-instruct` sequence.

## Conditions

### Condition 1: `current-main_baseline`

- Prompt/config source: live current `main` baseline at `c077cd8`
- Effective config artifact:
  `current-main_baseline/effective_config.baseline.yaml`
- JSON report:
  `current-main_baseline/tank_2026-04-11_034215Z.json`
- Debug overlay:
  `current-main_baseline/tank_2026-04-11_034215Z_debug/target_0_overlay.jpg`
- Debug crop:
  `current-main_baseline/tank_2026-04-11_034215Z_debug/target_0_crop.jpg`

Headline result:

- `target_0.target_type`: `military_equipment`
- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`
- `metadata.inference_time`: `17.05`

### Condition 2: `v002_candidate`

- Prompt/config source: `v002_detect_objects_edge-by-edge-grounding.yaml`
- Effective config artifact:
  `v002_candidate/effective_config.v002.yaml`
- JSON report:
  `v002_candidate/tank_2026-04-11_034241Z.json`
- Debug overlay:
  `v002_candidate/tank_2026-04-11_034241Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v002_candidate/tank_2026-04-11_034241Z_debug/target_0_crop.jpg`

Headline result:

- `target_0.target_type`: `military_equipment`
- `damage_category`: `DESTROYED`
- `confidence_level`: `CONFIRMED`
- `target_0.bounding_box`: `[56, 46, 123, 79]`
- `metadata.inference_time`: `6.22`

## Comparison Notes

- `v002` changed the box from `[51, 37, 128, 73]` to `[56, 46, 123, 79]`.
- Relative to baseline, the candidate box:
  - moved `+5` px right
  - moved `+9` px down
  - narrowed by `10` px
  - increased height by `6` px
- `v002` also raised confidence from `PROBABLE` to `CONFIRMED`.
- `v002` preserved the same subtype drift toward `locomotive`.
- `v002` summary language still introduced rail/logistics impact claims.
- Most importantly, the `v002` candidate output matches the earlier `v001`
  `run01` result exactly in bbox, confidence, and summary behavior.

## Review Artifact

- Side-by-side overlay/crop review:
  `bbox_review_sheet.jpg`

## Initial Decision State

- `v002` does not appear to open a genuinely new behavior path relative to
  `v001`.
- If the visual result is still off target, we should treat `v002` as another
  non-winning detection draft rather than iterate the same wording pattern.
