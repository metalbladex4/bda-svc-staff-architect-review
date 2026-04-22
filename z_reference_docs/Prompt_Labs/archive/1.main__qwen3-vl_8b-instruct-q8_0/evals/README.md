# Eval Tracks

This folder isolates prompt evaluation by task so failures are attributable.

## Tracks

- `system_assess_track.yaml`
  Shared system prompt plus `assess_damage` on known single-target inputs.
- `detect_track.yaml`
  `detect_objects` on full-scene images with expected counts/labels/boxes.
- `summarize_track.yaml`
  `summarize_scene` on frozen target payloads plus a scene image.
- `regression_set.yaml`
  Frozen cases that must be rerun after every accepted prompt revision.

## Current Limitation

The repo currently ships one built-in image fixture:

- `tests/data/tank.jpg`

So these manifests start with one real seed case and explicit placeholders for
the next cases to be added during prompt iteration.

Important bbox note:

- the detection VLM prompt uses the configured bbox convention from
  `detection_vlm.bbox_convention`
- the exported report stores validated boxes converted into source-image pixel
  coordinates
- eval manifests should say which coordinate space they are reviewing

## Asset Convention

If local-only crops, overlays, or derived eval images are generated, store them
under:

- `z_reference_docs/Prompt_Labs/1.main__qwen3-vl_8b-instruct-q8_0/evals/assets/system_assess/`
- `z_reference_docs/Prompt_Labs/1.main__qwen3-vl_8b-instruct-q8_0/evals/assets/detect/`
- `z_reference_docs/Prompt_Labs/1.main__qwen3-vl_8b-instruct-q8_0/evals/assets/summarize/`

Keep the manifests as the source of truth for expected behavior.

## Run Output Convention

Live experiment outputs should be stored under timestamped folders:

- `z_reference_docs/Prompt_Labs/1.main__qwen3-vl_8b-instruct-q8_0/experiments/runs/YYYY-MM-DD_HHMMSS_TZ/`

Each run folder should include a `RUN_MANIFEST.md`. Do not reuse a previous run
folder for a new experiment.
