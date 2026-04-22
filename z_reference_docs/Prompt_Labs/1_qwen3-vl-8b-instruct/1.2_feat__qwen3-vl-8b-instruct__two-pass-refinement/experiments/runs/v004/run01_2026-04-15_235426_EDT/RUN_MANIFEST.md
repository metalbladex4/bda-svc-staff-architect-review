# v004 Run 01

- version: `v004`
- parent: `v003`
- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- base commit: `28e863b`
- changed prompt surface: `summarize_scene`
- input image: `tests/data/tank.jpg`

## Run Method

1. Temporarily replaced the feature-branch live prompt config with:
   - `v001` detect prompt
   - `v003` assess prompt
   - `v004` summary prompt
2. Ran `bda-svc` on `tests/data/tank.jpg`.
3. Copied the candidate effective config into the run folder.
4. Restored `src/bda_svc/pipeline/config.yaml` to the clean branch-aware
   baseline prompt text and verified it matched the saved baseline snapshot.
5. Ran `bda_eval` against the fresh branch-aware baseline and the candidate
   report folder to keep the standard run artifact set.

## Headline Result

- baseline: bbox `[51, 37, 102, 73]`, `DESTROYED`, `PROBABLE`
- `v003` parent behavior: bbox `[46, 46, 123, 92]`, `DESTROYED`, `PROBABLE`
- `v004`: bbox `[46, 46, 123, 92]`, `DESTROYED`, `PROBABLE`

## Summary Change

Old `v003` summary:
- `military vehicle on a dirt track`
- `complete loss of the vehicle's operational capability due to destruction`

New `v004` summary:
- `The scene shows a burning target in open terrain with dense black smoke.`
- `The likely functional impact is severe degradation or loss of capability for the assessed target.`

## Readout

- Detection and target-level assessment stayed intact.
- The stronger `v001` bbox held.
- `DESTROYED` and `PROBABLE` held from `v003`.
- The summary is materially more conservative and generic:
  - no unsupported subtype wording
  - no unsupported dirt-track claim
  - no hard `complete loss` claim

## Decision

- best end-to-end branch-aware candidate so far
- provisional full-stack working leader pending one confirmation repeat
