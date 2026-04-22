# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run01_2026-04-12_162217_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v006`
- Input image: `tests/data/tank.jpg`
- Purpose: complete the first critique/research/revise cycle by testing a
  shorter, contrastive-example grounding prompt against the stable
  current-main baseline.

## Conditions

### Condition 1: `current-main_baseline`

- Prompt/config source: live current `main` baseline at upstream commit
  `21deaf5`, executed from local `main` with the temporary debug-export helper
  commit still present for overlay/crop review
- Effective config artifact:
  `current-main_baseline/effective_config.baseline.yaml`
- Command:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run bda-svc \
  --input tests/data/tank.jpg \
  --output z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/experiments/runs/v006/run01_2026-04-12_162217_EDT/current-main_baseline \
  --debug-export-images
```

- JSON report:
  `current-main_baseline/tank_2026-04-12_202234Z.json`
- Debug overlay:
  `current-main_baseline/tank_2026-04-12_202234Z_debug/target_0_overlay.jpg`
- Debug crop:
  `current-main_baseline/tank_2026-04-12_202234Z_debug/target_0_crop.jpg`

Headline result:

- `target_0.target_type`: `military_equipment`
- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`
- `metadata.inference_time`: `16.39`

### Condition 2: `v006_candidate`

- Prompt/config source: `v006_detect_objects_short-contrastive-example.yaml`
- Effective config artifact:
  `v006_candidate/effective_config.v006.yaml`
- Command note:
  The version file is a prompt-surface wrapper, so the candidate run used a
  merged full config generated from the live baseline plus the `v006`
  `detect_objects` override. That merged config was swapped into
  `src/bda_svc/pipeline/config.yaml` for the run and the live config was
  restored immediately afterward. Post-run verification showed no diff in the
  live config.
- JSON report:
  `v006_candidate/tank_2026-04-12_202240Z.json`
- Debug overlay:
  `v006_candidate/tank_2026-04-12_202240Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v006_candidate/tank_2026-04-12_202240Z_debug/target_0_crop.jpg`

Headline result:

- `target_0.target_type`: `military_equipment`
- `damage_category`: `DESTROYED`
- `confidence_level`: `CONFIRMED`
- `target_0.bounding_box`: `[46, 46, 128, 92]`
- `metadata.inference_time`: `5.18`

## Comparison Notes

- Relative to baseline, `v006`:
  - moved `xmin` left by `5` px
  - moved `ymin` down by `9` px
  - kept the same `xmax`
  - moved `ymax` down by `19` px
- Manual review of `bbox_review_sheet.jpg` shows `v006` is the first active
  candidate to move the box materially onto the visible burning target body
  instead of mostly left-side terrain/context.
- `v006` also removed the `locomotive` subtype wording from
  `brief_supporting_logic`.
- New watch items appeared downstream:
  - confidence rose from `PROBABLE` to `CONFIRMED`
  - supporting logic now says `consistent with a K-kill`
  - summary still misreads the surface as a dirt/gravel road

## Review Artifact

- Side-by-side overlay/crop review:
  `bbox_review_sheet.jpg`

## Initial Decision State

- `v006` is the best bbox candidate in the cycle so far.
- It is still not ready for promotion because the first apparent bbox win also
  changed downstream confidence and summary behavior.
- The next decision point should be whether to run a confirmation repeat of
  `v006` before moving on to the next prompt problem.
