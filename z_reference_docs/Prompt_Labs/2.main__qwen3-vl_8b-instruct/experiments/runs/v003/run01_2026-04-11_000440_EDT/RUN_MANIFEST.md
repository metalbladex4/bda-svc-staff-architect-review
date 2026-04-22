# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run01_2026-04-11_000440_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v003`
- Input image: `tests/data/tank.jpg`
- Purpose: compare the fresh current-main baseline against the third
  detection-only candidate in the restarted `qwen3-vl:8b-instruct` sequence.

## Conditions

### Condition 1: `current-main_baseline`

- Prompt/config source: live current `main` baseline at `c077cd8`
- Effective config artifact:
  `current-main_baseline/effective_config.baseline.yaml`
- Command:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run bda-svc \
  --input tests/data/tank.jpg \
  --output z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/experiments/runs/v003/run01_2026-04-11_000440_EDT/current-main_baseline \
  --debug-export-images
```

- JSON report:
  `current-main_baseline/tank_2026-04-11_040611Z.json`
- Debug overlay:
  `current-main_baseline/tank_2026-04-11_040611Z_debug/target_0_overlay.jpg`
- Debug crop:
  `current-main_baseline/tank_2026-04-11_040611Z_debug/target_0_crop.jpg`

Headline result:

- `target_0.target_type`: `military_equipment`
- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`
- `metadata.inference_time`: `16.64`

### Condition 2: `v003_candidate`

- Prompt/config source: `v003_detect_objects_center-first-example-anchored.yaml`
- Effective config artifact:
  `v003_candidate/effective_config.v003.yaml`
- Command note:
  The candidate run was executed by temporarily swapping
  `effective_config.v003.yaml` into `src/bda_svc/pipeline/config.yaml`,
  running `bda-svc`, and then restoring the live config immediately after the
  run. Post-run verification showed no diff in the live config.
- JSON report:
  `v003_candidate/tank_2026-04-11_040709Z.json`
- Debug overlay:
  `v003_candidate/tank_2026-04-11_040709Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v003_candidate/tank_2026-04-11_040709Z_debug/target_0_crop.jpg`

Headline result:

- `target_0.target_type`: `military_equipment`
- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 102, 73]`
- `metadata.inference_time`: `5.86`

## Comparison Notes

- `v003` changed the box from `[51, 37, 128, 73]` to `[51, 37, 102, 73]`.
- Relative to baseline, the candidate box:
  - kept the same `xmin`
  - kept the same `ymin`
  - reduced `xmax` by `26` px
  - kept the same `ymax`
- `v003` preserved `PROBABLE` confidence instead of raising it to
  `CONFIRMED` the way `v001` and `v002` did.
- `v003` removed the word `locomotive` from `brief_supporting_logic`, changing
  it to the more neutral `object`.
- `v003` numerically tightened the bbox back to `[51, 37, 102, 73]`, which
  matches the older archived `q8_0` baseline bbox and is tighter than `v001`
  run01 `[56, 46, 123, 79]`, `v001` run02 `[56, 46, 123, 85]`, and `v002`
  run01 `[56, 46, 123, 79]`.
- `v003` summary language still introduces a scene interpretation issue by
  calling the surface a dirt or gravel road instead of a track.

## Review Artifact

- Side-by-side overlay/crop review:
  `bbox_review_sheet.jpg`

## Initial Decision State

- `v003` is the first active-sequence candidate to materially tighten the bbox
  without also raising confidence to `CONFIRMED`.
- This is promising numerically, but promotion should wait for manual visual
  review of whether the tightened box actually lands on the visible target body.
- If the overlay still misses the target body, `v003` should be treated as
  another non-winning detection draft despite the tighter coordinates.
