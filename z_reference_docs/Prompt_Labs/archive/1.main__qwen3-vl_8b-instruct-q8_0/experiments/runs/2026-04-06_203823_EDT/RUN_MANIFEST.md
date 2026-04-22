# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `2026-04-06_203823_EDT`
- Lab: `1.main__qwen3-vl_8b-instruct-q8_0`
- Input image: `tests/data/tank.jpg`
- Purpose: compare the refreshed current-main baseline against the reconciled
  `v008` prompt chain on the current seed image.
- Output convention: timestamped experiment folder with separate condition
  subfolders.

## Conditions

### Condition 1: `current-main_baseline`

- Prompt/config source: refreshed `v000` baseline from `upstream/main`
- Run method: live `bda-svc` CLI with local temporary debug image export enabled
- JSON report:
  `current-main_baseline/tank_2026-04-07_004129Z.json`
- Debug overlay:
  `current-main_baseline/tank_2026-04-07_004129Z_debug/target_0_overlay.jpg`
- Debug crop:
  `current-main_baseline/tank_2026-04-07_004129Z_debug/target_0_crop.jpg`

Command:

```bash
uv run bda-svc \
  --input tests/data/tank.jpg \
  --output z_reference_docs/Prompt_Labs/1.main__qwen3-vl_8b-instruct-q8_0/experiments/runs/2026-04-06_203823_EDT/current-main_baseline \
  --debug-export-images
```

Headline result:

- Detections: `1`
- `target_0.target_type`: `military_equipment`
- `target_0.damage_category`: `DESTROYED`
- `target_0.confidence_level`: `CONFIRMED`
- `target_0.bounding_box`: `[51, 37, 102, 73]`
- `metadata.inference_time`: `12.38`

Summary output:

```text
1 military equipment (1 destroyed) visible in the scene. The image shows a single military vehicle engulfed in flames and thick black smoke, indicating complete destruction with no remaining functional components. The likely follow-on functional impact is zero combat capability for this unit, as it is fully destroyed and non-operational.
```

### Condition 2: `v008_reconciled-chain`

- Prompt/config source: `v008_summarize_scene_consistent-plaintext_postmerge.yaml`
- Effective config artifact:
  `v008_reconciled-chain/effective_config.v008.yaml`
- Run method: local script that loaded `v008` prompt surfaces into a temporary
  effective config without modifying `src/bda_svc/pipeline/config.yaml`
- JSON report:
  `v008_reconciled-chain/tank_2026-04-07_004133Z.json`
- Debug overlay:
  `v008_reconciled-chain/tank_2026-04-07_004133Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v008_reconciled-chain/tank_2026-04-07_004133Z_debug/target_0_crop.jpg`

Headline result:

- Detections: `1`
- `target_0.target_type`: `military_equipment`
- `target_0.damage_category`: `DESTROYED`
- `target_0.confidence_level`: `CONFIRMED`
- `target_0.bounding_box`: `[51, 49, 115, 85]`
- `metadata.inference_time`: `3.67`

Summary output:

```text
One military equipment target assessed as DESTROYED with CONFIRMED confidence. The scene shows a single vehicle engulfed in fire with thick black smoke rising, consistent with the prior assessment of structural deformation and burning components. No other relevant targets were assessed.
```

## Initial Comparison Notes

- Both conditions produced schema-valid JSON reports.
- Both conditions detected one `military_equipment` target and assessed it as
  `DESTROYED` with `CONFIRMED` confidence.
- The reconciled `v008` chain produced a different pixel-space bbox:
  `[51, 49, 115, 85]` compared with the current-main baseline
  `[51, 37, 102, 73]`.
- The `v008` summary was more constrained to prior target assessments and did
  not include the baseline's stronger "zero combat capability" phrasing.
- Visual review showed both bboxes are off target.
- Raw detection response review indicates the runtime conversion is behaving
  consistently with the configured `xyxy_1000` convention; the VLM is returning
  off-target normalized boxes.

## Raw Detection Review

Raw response notes are recorded in:

- `raw_detection_responses.md`

Key raw responses:

- baseline raw bbox: `[200, 300, 400, 600]`
- `v008` raw bbox: `[200, 400, 450, 700]`

Conclusion:

- classify this as a detection localization failure, not a coordinate
  conversion/export failure
- do not promote `v008` from this run
- focus the next prompt iteration on detection localization and bbox/crop
  reliability

## Caveats

- This is a single-image seed run and is not enough to accept or reject `v008`.
- This run is enough to block promotion of the current `v008` chain until the
  detection bbox issue is addressed.
- Debug overlay/crop output is local temporary prompt-tuning instrumentation.
- The `v008` condition used a temporary effective config file inside the run
  folder and did not modify the live pipeline config.
