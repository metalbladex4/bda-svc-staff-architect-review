# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run01_2026-04-10_205704_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Input image: `tests/data/tank.jpg`
- Purpose: record the first fresh current-main baseline under the new active
  `qwen3-vl:8b-instruct` lab structure.
- Output convention: version-first baseline run with one condition subfolder.

## Condition

### Condition 1: `current-main_baseline`

- Prompt/config source: live current `main` baseline at `c077cd8`
- Effective config artifact:
  `current-main_baseline/effective_config.baseline.yaml`
- Run method: live `bda-svc` CLI with local temporary debug image export enabled
- JSON report:
  `current-main_baseline/tank_2026-04-11_005830Z.json`
- Debug overlay:
  `current-main_baseline/tank_2026-04-11_005830Z_debug/target_0_overlay.jpg`
- Debug crop:
  `current-main_baseline/tank_2026-04-11_005830Z_debug/target_0_crop.jpg`

Command:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run bda-svc \
  --input tests/data/tank.jpg \
  --output z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/experiments/runs/baseline/run01_2026-04-10_205704_EDT/current-main_baseline \
  --debug-export-images
```

Headline result:

- Detections: `1`
- `target_0.target_type`: `military_equipment`
- `target_0.damage_category`: `DESTROYED`
- `target_0.confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`
- `metadata.inference_time`: `38.86`

Summary output:

```text
One target assessed: 1 military_equipment (DESTROYED, PROBABLE) located at bounding box [51, 37, 128, 73]. The scene depicts a burning military vehicle on a track in a barren, open landscape with thick smoke rising from the fire. The likely functional impact is complete loss of operational capability for the destroyed equipment.
```

## Initial Notes

- The run produced schema-valid JSON with one detected target.
- The target type remained doctrinally broad as `military_equipment`, but the
  assessment logic used the more specific word `locomotive`.
- Confidence softened to `PROBABLE` compared with the older archived baseline.
- This run establishes the first recorded reference report, overlay, crop, and
  pixel-space bbox for the new active lab.

## Caveats

- This is a single-image baseline seed run, not enough to judge prompt quality
  broadly.
- Manual bbox review is still needed before we treat the recorded box as a good
  localization reference.
- Debug overlay/crop export is local temporary prompt-tuning instrumentation.
