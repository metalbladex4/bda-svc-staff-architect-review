# Gemma `v002` Run Manifest

- version: `v002`
- date: `2026-04-19`
- branch: `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- model: `gemma4:e4b`
- host: `OLLAMA_HOST=http://127.0.0.1:11435`
- parent candidate:
  - focused `v002` guard-set run:
    `experiments/runs/v002/run01_2026-04-19_200142_EDT/`
  - broader `v001` comparison run:
    `experiments/runs/v001/run02_2026-04-19_195511_EDT/`
- prompt surface changed: `assess_damage` only
- diagnostics enabled:
  - `BDA_DEBUG_DETECTION_PATH`

## Change Summary

This run takes the focused `v002` building-severity improvement and checks it
against the full inherited six-case Gemma comparison pack.

`v002` keeps the recovered `v001` detect behavior and adds building-specific
severity guidance so visible collapse and rubble push building assessments
upward toward `SEVERE DAMAGE` or `DESTROYED`.

## Validation Pack

1. `tank_pressure`
2. `destroyed_tank15`
3. `operational_tank4`
4. `destroyed_building4`
5. `operational_building7`
6. `office_negative`

## Evaluation Tracks

- `eval_vs_qwen_v009`
- `eval_vs_origin_main_baseline`
- raw detection diagnostics for every case

## Primary Question

Can the focused `v002` building-severity improvement hold the full inherited
pack without reopening the recovered tank behavior or the negative/intact
controls?
