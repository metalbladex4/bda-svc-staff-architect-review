# Gemma `v002` Run Manifest

- version: `v002`
- date: `2026-04-19`
- branch: `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- model: `gemma4:e4b`
- host: `OLLAMA_HOST=http://127.0.0.1:11435`
- parent candidate: `v001`
  - broader follow-up:
    `experiments/runs/v001/run02_2026-04-19_195511_EDT/`
- prompt surface changed: `assess_damage` only
- diagnostics enabled:
  - `BDA_DEBUG_DETECTION_PATH`

## Change Summary

This run targets the remaining main Gemma failure surface after `v001`:

- undercalled building severity on `destroyed_building4`

`v002` keeps the `v001` detect behavior intact and adds building-specific
assessment guidance:

- do not anchor on small standing remnants when upper stories or most visible
  structural mass have collapsed
- prefer `SEVERE DAMAGE` when structural loss clearly exceeds moderate damage
  but substantial lower structure remains
- prefer `DESTROYED` when most visible structural mass is collapsed or reduced
  to rubble

## Focused Guard Set

1. `destroyed_building4`
2. `operational_building7`
3. `tank_pressure`
4. `operational_tank4`

## Evaluation Tracks

- `eval_vs_qwen_v009`
- raw detection diagnostics for all four cases

## Primary Question

Can a narrow building-specific assessment adjustment lift `destroyed_building4`
severity without reopening the recovered tank behavior or the intact-building
control?
