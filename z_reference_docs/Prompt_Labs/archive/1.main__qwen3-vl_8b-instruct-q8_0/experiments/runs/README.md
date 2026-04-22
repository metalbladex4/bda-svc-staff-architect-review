# Experiment Runs

This folder stores prompt-lab experiment outputs.

## Run Folder Convention

Every new experiment run should write outputs into a new timestamped folder:

```text
experiments/runs/YYYY-MM-DD_HHMMSS_TZ/
```

Inside each timestamped folder, use subfolders for each compared condition, for
example:

```text
experiments/runs/2026-04-06_202124_EDT/current-main_baseline/
experiments/runs/2026-04-06_202124_EDT/v008_reconciled-chain/
```

## Expected Contents

Each run folder should include:

- the exported JSON report
- any debug overlay/crop images used for prompt inspection
- a `RUN_MANIFEST.md` summarizing:
  - timestamp
  - prompt/config version
  - input image
  - command or run method
  - output artifacts
  - headline result
  - known caveats

## Working Rule

Do not mix outputs from different experiment times in the same folder. If a run
is repeated, create a new timestamped folder so results remain auditable.
