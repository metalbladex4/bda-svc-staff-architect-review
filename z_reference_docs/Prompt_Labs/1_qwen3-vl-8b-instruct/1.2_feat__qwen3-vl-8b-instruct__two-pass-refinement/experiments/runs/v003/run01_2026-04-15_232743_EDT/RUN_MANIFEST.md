# v003 Run 01

- version: `v003`
- parent: `v002`
- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- base commit: `28e863b`
- changed prompt surface: `assess_damage`
- input image: `tests/data/tank.jpg`

## Run Method

1. Temporarily replaced the feature-branch live prompt config with:
   - `v001` detect prompt
   - `v003` assess prompt
2. Ran `bda-svc` on `tests/data/tank.jpg`.
3. Copied the candidate effective config into the run folder.
4. Restored `src/bda_svc/pipeline/config.yaml` to the clean branch-aware
   baseline prompt text and verified it matched the saved baseline snapshot.
5. Ran `bda_eval` against the fresh branch-aware baseline and the candidate
   report folder to generate overlays, crops, the evaluation CSV, and
   `bbox_review_sheet.jpg`.

## Artifacts

- [candidate JSON](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v003/run01_2026-04-15_232743_EDT/v003_candidate/tank_2026-04-16_032949Z.json)
- [candidate effective config](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v003/run01_2026-04-15_232743_EDT/v003_candidate/effective_config.v003.yaml)
- [evaluation CSV](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v003/run01_2026-04-15_232743_EDT/evaluation_2026-04-16_033547Z.csv)
- [bbox review sheet](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v003/run01_2026-04-15_232743_EDT/bbox_review_sheet.jpg)

## Headline Result

- branch-aware baseline: bbox `[51, 37, 102, 73]`, `DESTROYED`, `PROBABLE`
- `v001` parent behavior: bbox `[46, 46, 123, 92]`, `DESTROYED`, `CONFIRMED`
- `v002` parent behavior: bbox `[46, 46, 123, 92]`, `DAMAGED`, `PROBABLE`
- `v003`: bbox `[46, 46, 123, 92]`, `DESTROYED`, `PROBABLE`

## Readout

- The stronger `v001` bbox held exactly again.
- `DESTROYED` was recovered after the `v002` overcorrection to `DAMAGED`.
- `PROBABLE` held, so the confidence regression from `v001` stayed fixed.
- Target-level subtype drift stayed out of `brief_supporting_logic`.
- The remaining issue is now mostly in the scene summary:
  - `military vehicle on a dirt track`
  - `complete loss of operational capability`

## Decision

- best combined branch-aware candidate so far
- treat as the current branch-aware working leader
- next prompt surface to focus on is `summarize_scene`, not detection or
  target-level assessment
