# Layout Check Run 02

- run type: `layout_check`
- purpose: confirm the clean branch-aware `bda_eval` prompt-lab artifact layout
- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- base commit: `28e863b`
- input image: `tests/data/tank.jpg`

## Inputs

- reference report folder:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/baseline/run01_2026-04-15_205325_EDT/current-main_baseline`
- candidate report folder:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/layout_check/run02_2026-04-15_224230_EDT/layout_check_candidate`

## Commands

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run bda-svc --input tests/data/tank.jpg --output /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/layout_check/run02_2026-04-15_224230_EDT/layout_check_candidate
```

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python main.py -r /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/baseline/run01_2026-04-15_205325_EDT/current-main_baseline -p /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/layout_check/run02_2026-04-15_224230_EDT/layout_check_candidate -i /home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/tests/data -o /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/layout_check/run02_2026-04-15_224230_EDT
```

## Headline Result

- baseline bbox: `[51, 37, 102, 73]`
- candidate bbox: `[51, 37, 102, 73]`
- outcome: no behavioral delta; this was a layout smoke test, not a prompt win/loss run

## Confirmed Artifacts

- `evaluation_2026-04-16_024745Z.csv`
- `images_bbox_both/bbox_tank.jpg`
- `images_bbox_reference/bbox_tank.jpg`
- `images_bbox_predicted/bbox_tank.jpg`
- `images_crop_reference/crop_tank.jpg`
- `images_crop_predicted/crop_tank.jpg`
- `images_bbox_review/bbox_review_tank.jpg`
- `bbox_review_sheet.jpg`

## Important Notes

- `bda_eval` now completes artifact generation without `OLLAMA_API_KEY` by
  skipping LLMaaJ logic scoring when credentials are absent.
- `bda_eval` also now tolerates prompt-lab runs where the predicted report
  folder already lives inside the run output root; it skips copying a source
  folder onto itself instead of failing.
- YAML config snapshots inside the compared report folders are still skipped by
  report discovery, which is expected.
