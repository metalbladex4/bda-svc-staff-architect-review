# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run01_2026-04-12_161314_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v005`
- Input image: `tests/data/tank.jpg`
- Purpose: continue the first critique/research/revise cycle by testing a
  point-first, occlusion-aware grounding method against the stable
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
  --output z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/experiments/runs/v005/run01_2026-04-12_161314_EDT/current-main_baseline \
  --debug-export-images
```

- JSON report:
  `current-main_baseline/tank_2026-04-12_201331Z.json`
- Debug overlay:
  `current-main_baseline/tank_2026-04-12_201331Z_debug/target_0_overlay.jpg`
- Debug crop:
  `current-main_baseline/tank_2026-04-12_201331Z_debug/target_0_crop.jpg`

Headline result:

- `target_0.target_type`: `military_equipment`
- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`
- `metadata.inference_time`: `16.12`

### Condition 2: `v005_candidate`

- Prompt/config source: `v005_detect_objects_point-first-occlusion-aware.yaml`
- Effective config artifact:
  `v005_candidate/effective_config.v005.yaml`
- Command note:
  The version file is a prompt-surface wrapper, so the candidate run used a
  merged full config generated from the live baseline plus the `v005`
  `detect_objects` override. That merged config was swapped into
  `src/bda_svc/pipeline/config.yaml` for the run and the live config was
  restored immediately afterward. Post-run verification showed no diff in the
  live config.
- JSON report:
  `v005_candidate/tank_2026-04-12_201528Z.json`
- Debug overlay:
  `v005_candidate/tank_2026-04-12_201528Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v005_candidate/tank_2026-04-12_201528Z_debug/target_0_crop.jpg`

Headline result:

- `target_0.target_type`: `military_equipment`
- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`
- `metadata.inference_time`: `6.42`

## Comparison Notes

- `v005` matched the baseline bbox exactly: `[51, 37, 128, 73]`.
- `v005` matched the baseline confidence exactly: `PROBABLE`.
- `v005` matched the baseline supporting-logic subtype drift exactly:
  `locomotive`.
- `v005` matched the baseline summary wording exactly apart from timestamps and
  metadata fields.
- The only observable differences were runtime metadata values such as
  `image_id`, `date_created`, and `inference_time`.

## Review Artifact

- Side-by-side overlay/crop review:
  `bbox_review_sheet.jpg`

## Initial Decision State

- `v005` is not a winning direction.
- The run was still useful because it showed the point-first, occlusion-aware
  prose did not meaningfully override the baseline behavior.
- The next draft should become more salient, probably by getting shorter and
  using explicit examples rather than adding another abstract instruction block.
