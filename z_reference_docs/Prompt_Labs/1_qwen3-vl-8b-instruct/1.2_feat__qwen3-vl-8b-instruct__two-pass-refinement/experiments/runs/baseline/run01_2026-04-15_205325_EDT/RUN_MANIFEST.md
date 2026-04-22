# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run01_2026-04-15_205325_EDT`
- Lab root:
  `1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`
- Git branch:
  `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- Live runtime baseline commit: `28e863b`
- Input image: `tests/data/tank.jpg`
- Purpose: record the first fresh branch-aware current-main baseline after the
  upstream sync to `28e863b` and the git/worktree reset.
- Output convention: version-first baseline run with one condition subfolder.

## Condition

### Condition 1: `current-main_baseline`

- Prompt/config source: live current `main` baseline at `28e863b`
- Run workspace:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`
- Effective config artifact:
  `current-main_baseline/effective_config.baseline.yaml`
- Run method: clean `bda-svc` CLI baseline from the feature worktree
- JSON report:
  `current-main_baseline/tank_2026-04-16_010530Z.json`

Command:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run bda-svc \
  --input tests/data/tank.jpg \
  --output /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/baseline/run01_2026-04-15_205325_EDT/current-main_baseline
```

Headline result:

- Detections: `1`
- `target_0.target_type`: `military_equipment`
- `target_0.damage_category`: `DESTROYED`
- `target_0.confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 102, 73]`
- `metadata.inference_time`: `10.85`

Summary output:

```text
One target assessed: 1 military_equipment, condition DESTROYED with PROBABLE confidence. The scene depicts a single military vehicle engulfed in fire and thick black smoke, situated on what appears to be a dirt or gravel road in an open, arid landscape. The likely functional impact is complete loss of operational capability for the assessed target.
```

## Initial Notes

- The run produced schema-valid JSON with one detected target.
- This fresh `28e863b` branch-aware baseline landed at bbox `[51, 37, 102, 73]`,
  which is tighter than the older preserved legacy baseline
  `[51, 37, 128, 73]`.
- Because this branch line starts from clean mirrored upstream, it did not use
  the older local temporary debug-export helper.
- This run should now be treated as the active baseline anchor for new work in
  this branch-aware lab, not the older `21deaf5`-anchored legacy baseline.

## Caveats

- This is still a single-image seed run.
- No extra debug overlay/crop artifacts were exported in this clean branch run.
- The summary still describes the surface as a dirt or gravel road, so scene
  wording remains a separate issue from this baseline reset.
