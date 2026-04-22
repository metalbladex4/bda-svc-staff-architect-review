# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `2026-04-06_202124_EDT`
- Execution timestamp from report: `2026-04-07T00:22:41Z`
- Lab: `1.main__qwen3-vl_8b-instruct-q8_0`
- Condition: `current-main_baseline`
- Prompt/config source: refreshed `v000` baseline from `upstream/main`
- Runtime command path: live `bda-svc` CLI with local temporary debug image export enabled

## Input

- Image: `tests/data/tank.jpg`

## Command

```bash
uv run bda-svc \
  --input tests/data/tank.jpg \
  --output z_reference_docs/Prompt_Labs/1.main__qwen3-vl_8b-instruct-q8_0/experiments/runs/2026-04-06_202124_EDT/current-main_baseline \
  --debug-export-images
```

## Output Artifacts

- JSON report:
  `current-main_baseline/tank_2026-04-07_002241Z.json`
- Debug overlay:
  `current-main_baseline/tank_2026-04-07_002241Z_debug/target_0_overlay.jpg`
- Debug crop:
  `current-main_baseline/tank_2026-04-07_002241Z_debug/target_0_crop.jpg`

## Headline Result

- Detections: `1`
- `target_0.target_type`: `military_equipment`
- `target_0.damage_category`: `DESTROYED`
- `target_0.confidence_level`: `CONFIRMED`
- `target_0.bounding_box`: `[51, 37, 102, 73]`
- `metadata.inference_time`: `13.36`

## Summary Output

```text
1 military equipment (1 destroyed) visible in the scene. The image shows a single military vehicle engulfed in flames and thick black smoke, indicating complete destruction with no remaining functional components. The likely follow-on functional impact is zero combat capability for this unit, as it is fully destroyed and non-operational.
```

## Caveats And Notes

- This run used the current live main baseline, not the reconciled `v005` through `v008` prompt chain.
- Debug overlay/crop output is local temporary prompt-tuning instrumentation and should not be treated as an upstream product feature unless it is later promoted.
- The next comparison run should use a separate timestamped folder or a sibling condition folder under a new timestamp if run at a different time.
