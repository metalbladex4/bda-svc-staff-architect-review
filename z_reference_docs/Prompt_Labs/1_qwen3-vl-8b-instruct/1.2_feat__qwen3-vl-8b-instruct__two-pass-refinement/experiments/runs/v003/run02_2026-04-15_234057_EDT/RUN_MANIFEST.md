# v003 Run 02

- version: `v003`
- parent: `v002`
- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- base commit: `28e863b`
- run purpose: repeatability check with no prompt changes
- input image: `tests/data/tank.jpg`

## Headline Result

- baseline: bbox `[51, 37, 102, 73]`, `DESTROYED`, `PROBABLE`
- `v003` run01: bbox `[46, 46, 123, 92]`, `DESTROYED`, `PROBABLE`
- `v003` run02: bbox `[46, 46, 123, 92]`, `DESTROYED`, `PROBABLE`

## Repeatability Read

- The run02 payload matched run01 exactly once routine metadata fields were
  ignored:
  - `image_id`
  - `date_created`
  - `inference_time`
- Target-level logic remained identical:
  - `sustained fire; dense smoke; target body catastrophically affected but partly obscured`
- The stronger bbox held exactly.
- Summary wording remained the same as run01, including the remaining scene
  overreach:
  - `military vehicle on a dirt track`
  - `complete loss of operational capability`

## Artifacts

- [candidate JSON](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v003/run02_2026-04-15_234057_EDT/v003_candidate/tank_2026-04-16_034757Z.json)
- [candidate effective config](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v003/run02_2026-04-15_234057_EDT/v003_candidate/effective_config.v003.yaml)
- [evaluation CSV](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v003/run02_2026-04-15_234057_EDT/evaluation_2026-04-16_035041Z.csv)
- [bbox review sheet](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v003/run02_2026-04-15_234057_EDT/bbox_review_sheet.jpg)

## Decision

- `v003` now has a successful repeat on the branch-aware line
- detection and target-level assessment should be treated as stable enough to
  freeze for the next cycle
- the next prompt surface to tune is `summarize_scene`
