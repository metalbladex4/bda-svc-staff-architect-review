# Gemma `v001` Run Manifest

- version: `v001`
- date: `2026-04-19`
- branch: `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- model: `gemma4:e4b`
- host: `OLLAMA_HOST=http://127.0.0.1:11435`
- parent anchor: `v000` active baseline
  - `experiments/runs/v000/run02_2026-04-19_185856_EDT/`
- follow-up type: broader six-case validation
- prompt surface changed: `detect_objects` only
- diagnostics enabled:
  - `BDA_DEBUG_DETECTION_PATH`

## Change Summary

This run reuses the same narrow `v001` detect-only adjustment first proven on
the two tank cases:

- use `{"detections": []}` only when no doctrinal target body or connected
  structural remains are visibly present
- if smoke, fire, flame, or dust partially obscures a target but some
  connected target body remains visible, return a detection rather than an
  empty detections list

## Validation Pack

The full inherited six-case comparison pack:

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

Does the narrow `v001` recovery from the two-case tank probe generalize across
the broader inherited Gemma comparison pack without breaking the held controls?
