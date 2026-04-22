## What changed

This branch contributes two linked updates:

1. Adds prompt-lab visual review artifacts to `bda_eval`
   - overlay outputs for reference and predicted bboxes
   - crop outputs for reference and predicted targets
   - per-image review sheets
   - root `bbox_review_sheet.jpg` support for prompt-lab comparisons
   - tests covering the new review-artifact behavior

2. Promotes the active working Qwen prompt stack for this model line into
   `src/bda_svc/pipeline/config.yaml`
   - `detect_objects` from `v006`
   - `assess_damage` from `v008`
   - `summarize_scene` from `v004`

## Why it changed

The goal was to move from isolated prompt-lab experimentation toward a tracked,
reviewable working config for this Qwen model line.

The prompt stack was built and validated incrementally, then unified as `v009`
after:

- focused confirmation on representative cases
- extra hard-case comparisons
- a broader 10-image baseline-vs-`v009` blind-style sweep

The `bda_eval` changes were added so prompt-grounding review can rely on
tracked evaluation functionality rather than temporary local-only debug export
helpers.

The resulting `v009` stack is not just the best local winner note anymore. It
is now the active working config for this model line going forward, with the
prompt-lab evidence trail preserved separately under local `z_reference_docs`.

## Validation used

Tracked checks:

- `uv run pytest bda_eval/tests`
- `uv run pytest tests/unit/test_yamls.py bda_eval/tests`

GitHub Actions CI for this PR validates branch health:

- unit and integration test execution
- Docker build and runnable pipeline behavior
- CI/runtime compatibility for the tracked branch state

It does **not** currently assert exact parity with the prompt-lab `v009`
winner outputs. The prompt-behavior evidence for this PR comes from the
prompt-lab validation runs recorded under local `z_reference_docs`, which are
kept outside normal branch history on purpose.

Prompt-lab validation highlights:

- direct `v009` focused confirmation on:
  - `tank_pressure`
  - `operational_tank4`
  - `destroyed_building4`
- additional baseline-vs-`v009` challenge comparison on 3 new images
- broader 10-image baseline-vs-`v009` blind sweep

Blind-sweep headline:

- `10 / 10` preserved target-count recall
- `6 / 10` preserved the same damage/confidence structure
- only `2 / 10` changed damage category at all

## Strongest claim

This is not just a tank-specific prompt mockup.

The strongest evidence is:

- preserved cross-image recall
- cleaner negative-scene behavior
- better multi-target separation
- improved cross-image stability across buildings, tanks, and trucks

## Known caveats

Two blind-sweep watch cases remain visible and should stay part of review:

- `destroyed_building5`
  - likely a real `v009` building-severity overcall
- `destroyed_tank37`
  - `v009` gives the cleaner bbox
  - `DAMAGED` is arguable under smoke/angle obscuration
  - but the current supporting logic is still too catastrophic for a clean
    `DAMAGED` read

These are category-calibration watch cases, not recall failures.

## Commit structure

- `566892a` — `Add prompt-lab review artifacts to bda_eval`
- `127051a` — `Promote v009 prompt stack into pipeline config`
- `ebeae30` — `Install workspace packages in CI`
