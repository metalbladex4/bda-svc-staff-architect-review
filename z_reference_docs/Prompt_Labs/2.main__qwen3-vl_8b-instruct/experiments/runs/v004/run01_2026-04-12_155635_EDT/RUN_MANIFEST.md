# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run01_2026-04-12_155635_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v004`
- Input image: `tests/data/tank.jpg`
- Purpose: start the first critique/research/revise loop by comparing the
  active current-main baseline against a fire-source-to-object-body grounding
  candidate.

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
  --output z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/experiments/runs/v004/run01_2026-04-12_155635_EDT/current-main_baseline \
  --debug-export-images
```

- JSON report:
  `current-main_baseline/tank_2026-04-12_195653Z.json`
- Debug overlay:
  `current-main_baseline/tank_2026-04-12_195653Z_debug/target_0_overlay.jpg`
- Debug crop:
  `current-main_baseline/tank_2026-04-12_195653Z_debug/target_0_crop.jpg`

Headline result:

- `target_0.target_type`: `military_equipment`
- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`
- `metadata.inference_time`: `17.22`

### Condition 2: `v004_candidate`

- Prompt/config source: `v004_detect_objects_fire-source-object-body.yaml`
- Effective config artifact:
  `v004_candidate/effective_config.v004.yaml`
- Command note:
  The version file is a prompt-surface wrapper, so the candidate run used a
  merged full config generated from the live baseline plus the `v004`
  `detect_objects` override. That merged config was swapped into
  `src/bda_svc/pipeline/config.yaml` for the run and the live config was
  restored immediately afterward. Post-run verification showed no diff in the
  live config.
- JSON report:
  `v004_candidate/tank_2026-04-12_195746Z.json`
- Debug overlay:
  `v004_candidate/tank_2026-04-12_195746Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v004_candidate/tank_2026-04-12_195746Z_debug/target_0_crop.jpg`

Headline result:

- `target_0.target_type`: `military_equipment`
- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 102, 61]`
- `metadata.inference_time`: `6.47`

## Comparison Notes

- The baseline reproduced the current active baseline behavior again:
  `[51, 37, 128, 73]`, `PROBABLE`.
- Relative to baseline, `v004`:
  - kept the same `xmin`
  - kept the same `ymin`
  - reduced `xmax` by `26` px
  - reduced `ymax` by `12` px
- Relative to `v003` `[51, 37, 102, 73]`, `v004` kept the tighter right edge
  but also cut the bottom edge upward, which reduced the candidate crop height
  further.
- `v004` reintroduced unsupported subtype wording:
  - supporting logic: `locomotive or rolling stock`
  - summary: `likely a locomotive or heavy transport`

## Review Artifact

- Side-by-side overlay/crop review:
  `bbox_review_sheet.jpg`

## Initial Decision State

- `v004` is not a winning direction.
- The experiment was useful because it showed that anchoring to the visible
  body segment nearest the fire source over-shrinks the box and still does not
  land on the actual target body.
- The reusable lesson is narrower:
  use fire and smoke as search cues, but do not let the prompt collapse onto
  the nearest dark patch adjacent to the fire.
