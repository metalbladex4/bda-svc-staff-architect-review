# v004 Run 02

- version: `v004`
- parent: `v003`
- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- base commit: `28e863b`
- run purpose: repeatability check with no prompt changes
- input image: `tests/data/tank.jpg`

## Headline Result

- baseline: bbox `[51, 37, 102, 73]`, `DESTROYED`, `PROBABLE`
- `v004` run01: bbox `[46, 46, 123, 92]`, `DESTROYED`, `PROBABLE`
- `v004` run02: bbox `[46, 46, 123, 92]`, `DESTROYED`, `PROBABLE`

## Repeatability Read

- The run02 payload matched run01 exactly once routine metadata fields were
  ignored:
  - `image_id`
  - `date_created`
  - `inference_time`
- The improved summary also repeated exactly:
  - `One target assessed: 1 military_equipment, condition DESTROYED with PROBABLE confidence. The scene shows a burning target in open terrain with dense black smoke. The likely functional impact is severe degradation or loss of capability for the assessed target.`
- So detection, target-level assessment, and summary all held on repeat.

## Artifacts

- [candidate JSON](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v004/run02_2026-04-16_001251_EDT/v004_candidate/tank_2026-04-16_041928Z.json)
- [candidate effective config](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v004/run02_2026-04-16_001251_EDT/v004_candidate/effective_config.v004.yaml)
- [evaluation CSV](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v004/run02_2026-04-16_001251_EDT/evaluation_2026-04-16_042113Z.csv)
- [bbox review sheet](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v004/run02_2026-04-16_001251_EDT/bbox_review_sheet.jpg)

## Decision

- `v004` is now a confirmed branch-aware full-stack working leader
- no additional prompt surface currently looks higher priority than broader
  validation or packaging the branch-aware lessons
