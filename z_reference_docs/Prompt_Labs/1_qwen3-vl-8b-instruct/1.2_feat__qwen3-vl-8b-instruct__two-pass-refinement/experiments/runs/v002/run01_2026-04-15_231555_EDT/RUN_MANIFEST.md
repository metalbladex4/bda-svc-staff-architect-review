# v002 Run 01

- version: `v002`
- parent: `v001`
- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- base commit: `28e863b`
- changed prompt surface: `assess_damage`
- input image: `tests/data/tank.jpg`

## Run Method

1. Temporarily replaced the feature-branch live prompt config with:
   - `v001` detect prompt
   - `v002` assess prompt
2. Ran `bda-svc` on `tests/data/tank.jpg`.
3. Copied the candidate effective config into the run folder.
4. Restored `src/bda_svc/pipeline/config.yaml` to the clean branch-aware
   baseline prompt text and verified it matched the saved baseline snapshot.
5. Ran `bda_eval` against the fresh branch-aware baseline and the candidate
   report folder to generate overlays, crops, the evaluation CSV, and
   `bbox_review_sheet.jpg`.

## Artifacts

- [candidate JSON](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v002/run01_2026-04-15_231555_EDT/v002_candidate/tank_2026-04-16_031854Z.json)
- [candidate effective config](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v002/run01_2026-04-15_231555_EDT/v002_candidate/effective_config.v002.yaml)
- [evaluation CSV](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v002/run01_2026-04-15_231555_EDT/evaluation_2026-04-16_032414Z.csv)
- [bbox review sheet](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v002/run01_2026-04-15_231555_EDT/bbox_review_sheet.jpg)

## Headline Result

- branch-aware baseline: bbox `[51, 37, 102, 73]`, `DESTROYED`, `PROBABLE`
- `v001` parent behavior: bbox `[46, 46, 123, 92]`, `DESTROYED`, `CONFIRMED`
- `v002`: bbox `[46, 46, 123, 92]`, `DAMAGED`, `PROBABLE`

## Readout

- The stronger `v001` bbox held exactly. Visually, the candidate overlay
  remained on the larger burning target body instead of collapsing back to the
  fresh baseline box.
- The assessment prompt did pull confidence back from `CONFIRMED` to
  `PROBABLE`.
- The target-level subtype drift was reduced:
  - target logic no longer says `locomotive`
- But the assessment overcorrected:
  - `DESTROYED` dropped to `DAMAGED`
- The summary still contains some unsupported overreach:
  - `vehicle on a track`
  - `complete loss of operational capability`

## Decision

- partial reuse only
- keep the `v001` detection behavior as the current best branch-aware bbox lead
- use `v002` as evidence that the safer assessment framing can hold the better
  box, but it needs refinement to recover `DESTROYED` without bringing back
  `CONFIRMED` or subtype drift
