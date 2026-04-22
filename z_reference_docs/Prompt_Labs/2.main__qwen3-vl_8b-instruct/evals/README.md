# Eval Tracks

This folder isolates prompt evaluation by task so failures stay attributable.

## Tracks

- `system_assess_track.yaml`
  Shared system prompt plus `assess_damage` on known single-target inputs.
- `detect_track.yaml`
  `detect_objects` on full-scene images with expected counts, labels, and
  review targets.
- `summarize_track.yaml`
  `summarize_scene` on frozen target-assessment payloads so summary quality is
  not contaminated by detector or assessment failures.
- `regression_set.yaml`
  Frozen cases that must be rerun after every accepted prompt revision.

## Current State

This is a fresh active lab for the current `main` runtime contract at commit
`c077cd8`.

The built-in repo fixture currently available for baseline work is:

- `tests/data/tank.jpg`

The first fresh baseline run for this lab still needs to be recorded. Until
that run exists, manifests should be treated as ready-to-fill scaffolding for
the new sequence.

## Asset Convention

If local-only crops, overlays, or derived eval images are generated, store them
under:

- `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/evals/assets/system_assess/`
- `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/evals/assets/detect/`
- `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/evals/assets/summarize/`

Keep the manifests as the source of truth for expected behavior.

## Run Output Convention

Live experiment outputs should be stored under the version-first run layout:

- `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/experiments/runs/baseline/run01_YYYY-MM-DD_HHMMSS_TZ/`
- `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/experiments/runs/v001/run01_YYYY-MM-DD_HHMMSS_TZ/`

Each run folder should include a `RUN_MANIFEST.md`. Do not reuse a previous run
folder for a new experiment.
