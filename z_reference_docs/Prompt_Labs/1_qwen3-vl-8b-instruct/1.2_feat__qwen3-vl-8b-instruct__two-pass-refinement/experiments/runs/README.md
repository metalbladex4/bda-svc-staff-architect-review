# Experiment Runs

This folder stores branch-aware experiment outputs for:

- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`

## Run Folder Convention

Every new experiment run should write outputs into a version-first folder:

```text
experiments/runs/baseline/run01_YYYY-MM-DD_HHMMSS_TZ/
experiments/runs/baseline/run02_YYYY-MM-DD_HHMMSS_TZ/
experiments/runs/v001/run01_YYYY-MM-DD_HHMMSS_TZ/
```

Inside each run folder, use one subfolder per compared condition when
applicable.

## Expected Contents

Each run folder should include:

- the exported JSON report
- an `effective_config` snapshot when applicable
- when bbox comparison is needed, the paired `bda_eval` output folder should
  include:
  - combined overlays
  - per-condition overlays
  - per-condition crops
  - `bbox_review_sheet.jpg` for single-image comparison runs
- a `RUN_MANIFEST.md` summarizing:
  - timestamp
  - prompt/config version
  - input image
  - command or run method
  - output artifacts
  - headline result
  - known caveats

## Clean-Branch Note

This branch-aware line starts from clean `28e863b`.

By default, do not assume the older local temporary debug-export helper exists
here. If later work reintroduces extra debug artifacts, document that
explicitly in the relevant run manifest and methodology notes.

Preferred bbox-review path for this branch:

- use `bda_eval` with the reference report folder, predicted report folder, and
  source image folder
- treat the `bda_eval` review artifacts as the replacement for the old prompt-
  lab overlay/crop helper on this clean line

## Confirmed Layout Check

The first successful clean-line `bda_eval` layout check is:

- `layout_check/run02_2026-04-15_224230_EDT/`

That run verified the real run-root layout now includes:

- `bbox_review_sheet.jpg`
- `images_bbox_both/`
- `images_bbox_reference/`
- `images_bbox_predicted/`
- `images_crop_reference/`
- `images_crop_predicted/`
- `images_bbox_review/`
- the copied reference/predicted report folders
- the evaluation CSV

It also verified that bbox-artifact generation can proceed even when:

- `OLLAMA_API_KEY` is absent
- the predicted report folder already lives inside the run output root
