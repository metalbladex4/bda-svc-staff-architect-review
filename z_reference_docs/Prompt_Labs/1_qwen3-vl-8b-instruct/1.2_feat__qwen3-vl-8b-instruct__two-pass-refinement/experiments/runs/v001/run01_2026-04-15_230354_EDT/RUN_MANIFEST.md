# v001 Run 01

- version: `v001`
- parent: `v000`
- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- base commit: `28e863b`
- changed prompt surface: `detect_objects`
- input image: `tests/data/tank.jpg`

## Run Method

1. Temporarily replaced the feature-branch `detect_objects` prompt in
   `src/bda_svc/pipeline/config.yaml` with the `v001` candidate wording.
2. Ran `bda-svc` on `tests/data/tank.jpg`.
3. Copied the candidate effective config into the run folder.
4. Restored `src/bda_svc/pipeline/config.yaml` to the clean branch-aware
   baseline prompt text.
5. Ran `bda_eval` against the fresh branch-aware baseline and the candidate
   report folder to generate overlays, crops, the evaluation CSV, and
   `bbox_review_sheet.jpg`.

## Artifacts

- [candidate JSON](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v001/run01_2026-04-15_230354_EDT/v001_candidate/tank_2026-04-16_030638Z.json)
- [candidate effective config](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v001/run01_2026-04-15_230354_EDT/v001_candidate/effective_config.v001.yaml)
- [evaluation CSV](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v001/run01_2026-04-15_230354_EDT/evaluation_2026-04-16_030840Z.csv)
- [bbox review sheet](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/v001/run01_2026-04-15_230354_EDT/bbox_review_sheet.jpg)

## Headline Result

- branch-aware baseline: bbox `[51, 37, 102, 73]`, `DESTROYED`, `PROBABLE`
- `v001`: bbox `[46, 46, 123, 92]`, `DESTROYED`, `CONFIRMED`

## Readout

- The candidate reproduced the stronger, larger grounding pattern from the
  older legacy `v006` family on the clean `28e863b` baseline.
- Visual review suggests the `v001` box is more meaningfully on the burning
  target body than the fresh branch-aware baseline, which remained too small
  and left of the most relevant target mass.
- The downstream tradeoff reappeared immediately:
  - confidence escalated from `PROBABLE` to `CONFIRMED`
  - subtype drift returned in target logic and summary (`locomotive`)
  - summary scene context drift returned (`railway track`)

## Decision

- treat `v001` as a detection improvement signal, not an overall winner
- keep the bbox hypothesis alive
- do not promote the full prompt set without addressing the downstream
  regressions that reappeared when the box moved
