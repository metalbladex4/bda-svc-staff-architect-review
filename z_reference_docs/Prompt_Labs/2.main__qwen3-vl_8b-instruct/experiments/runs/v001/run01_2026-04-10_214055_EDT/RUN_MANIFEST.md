# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run01_2026-04-10_214055_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v001`
- Input image: `tests/data/tank.jpg`
- Purpose: compare the fresh current-main baseline against the first
  detection-only candidate in the restarted `qwen3-vl:8b-instruct` sequence.
- Output convention: version-first run folder with separate baseline and
  candidate condition subfolders.

## Conditions

### Condition 1: `current-main_baseline`

- Prompt/config source: live current `main` baseline at `c077cd8`
- Effective config artifact:
  `current-main_baseline/effective_config.baseline.yaml`
- Run method: live `bda-svc` CLI with local temporary debug image export enabled
- JSON report:
  `current-main_baseline/tank_2026-04-11_014144Z.json`
- Debug overlay:
  `current-main_baseline/tank_2026-04-11_014144Z_debug/target_0_overlay.jpg`
- Debug crop:
  `current-main_baseline/tank_2026-04-11_014144Z_debug/target_0_crop.jpg`

Headline result:

- Detections: `1`
- `target_0.target_type`: `military_equipment`
- `target_0.damage_category`: `DESTROYED`
- `target_0.confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`
- `metadata.inference_time`: `10.24`

### Condition 2: `v001_candidate`

- Prompt/config source: `v001_detect_objects_visible-boundary-tightening.yaml`
- Effective config artifact:
  `v001_candidate/effective_config.v001.yaml`
- Run method: local in-memory prompt override using the live runtime without
  modifying `src/bda_svc/pipeline/config.yaml`
- JSON report:
  `v001_candidate/tank_2026-04-11_014913Z.json`
- Debug overlay:
  `v001_candidate/tank_2026-04-11_014913Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v001_candidate/tank_2026-04-11_014913Z_debug/target_0_crop.jpg`

Headline result:

- Detections: `1`
- `target_0.target_type`: `military_equipment`
- `target_0.damage_category`: `DESTROYED`
- `target_0.confidence_level`: `CONFIRMED`
- `target_0.bounding_box`: `[56, 46, 123, 79]`
- `metadata.inference_time`: `10.32`

## Comparison Notes

- `v001` changed the box from `[51, 37, 128, 73]` to `[56, 46, 123, 79]`.
- Relative to baseline, the candidate box:
  - moved `+5` px right
  - moved `+9` px down
  - narrowed by `10` px
  - increased height by `6` px
- `v001` also raised confidence from `PROBABLE` to `CONFIRMED`.
- The subtype wording drift to `locomotive` remained present in both supporting
  logic and summary text.
- `v001` summary language became more specific and included rail/logistics
  impact language that may be stronger than the desired Phase 1 framing.

## Review Artifact

- Side-by-side overlay/crop review:
  `bbox_review_sheet.jpg`

## Initial Decision State

- Do not promote or reject `v001` from JSON alone.
- Manual visual review should decide whether the new box is genuinely tighter on
  the physical target body or simply shifted.
- If the box is better, the next iteration should focus on controlling subtype
  specificity and summary drift.
- If the box is not better, keep the main focus on detection localization.
