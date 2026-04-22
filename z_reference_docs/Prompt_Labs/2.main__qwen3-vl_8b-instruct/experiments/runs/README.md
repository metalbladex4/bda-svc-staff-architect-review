# Experiment Runs

This folder stores prompt-lab experiment outputs for the active
`qwen3-vl:8b-instruct` sequence.

## Run Folder Convention

Every new experiment run should write outputs into a version-first folder:

```text
experiments/runs/baseline/run01_YYYY-MM-DD_HHMMSS_TZ/
experiments/runs/baseline/run02_YYYY-MM-DD_HHMMSS_TZ/
experiments/runs/v001/run01_YYYY-MM-DD_HHMMSS_TZ/
experiments/runs/v001/run02_YYYY-MM-DD_HHMMSS_TZ/
```

Inside each run folder, use subfolders for each compared condition, for example:

```text
experiments/runs/baseline/run01_YYYY-MM-DD_HHMMSS_TZ/current-main_baseline/
experiments/runs/v001/run01_YYYY-MM-DD_HHMMSS_TZ/current-main_baseline/
experiments/runs/v001/run01_YYYY-MM-DD_HHMMSS_TZ/v001_candidate/
```

## Expected Contents

Each run folder should include:

- the exported JSON report
- any debug overlay/crop images used for prompt inspection
- `pipeline_debug.json` when the run is executed with the temporary
  `--debug-export-images` path and the pipeline records raw debug payloads
- an `effective_config` snapshot for the candidate condition when applicable
- a `RUN_MANIFEST.md` summarizing:
  - timestamp
  - prompt/config version
  - input image
  - command or run method
  - output artifacts
  - headline result
  - known caveats

## Temporary Debug Payload

When a run is executed with `--debug-export-images`, the temporary debug folder
may now also include:

- `pipeline_debug.json`

Purpose:

- preserve the raw detection payload before downstream fallback behavior hides
  it
- show how the model's raw bbox was interpreted by the current bbox convention
- show whether two-pass refinement was enabled and how each ROI refinement
  attempt behaved
- help distinguish prompt failures from contract/validation failures

Current use:

- for grounding experiments, review `pipeline_debug.json` alongside the JSON
  report, overlay, and crop
- if a candidate collapses to `object_not_found`, inspect `pipeline_debug.json`
  first before drafting the next prompt hypothesis
- if refinement is enabled, inspect the ROI box, translated child candidates,
  and the final refinement decision before assuming the second pass helped
- treat it as temporary prompt-lab instrumentation, not part of the live
  external output contract

## Working Rule

Do not mix outputs from different experiment times in the same folder. If a run
is repeated, increment the `runNN` prefix and create a new timestamped folder so
results remain auditable.
