# Gemma `v001` Run Manifest

- version: `v001`
- date: `2026-04-19`
- branch: `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- model: `gemma4:e4b`
- host: `OLLAMA_HOST=http://127.0.0.1:11435`
- parent anchor: `v000` active baseline
  - `experiments/runs/v000/run02_2026-04-19_185856_EDT/`
- prompt surface changed: `detect_objects` only
- diagnostics enabled:
  - `BDA_DEBUG_DETECTION_PATH`

## Change Summary

This run tests one narrow detect-contract adjustment only.

Previous post-`e7a22a9` evidence showed:

- `tank_pressure` collapsed to `object_not_found / NOT APPLICABLE`
- a diagnostic rerun confirmed Gemma explicitly returned `{"detections":[]}`
- `operational_tank4` still detected a target, but drifted into
  `DAMAGED / PROBABLE`

`v001` changes only the no-target instruction:

- use `{"detections": []}` only when no doctrinal target body or connected
  structural remains are visibly present anywhere in the image
- if fire, smoke, flame, or dust partially obscures a doctrinal target but
  some connected target body remains visible, return a detection instead of
  `{"detections": []}`

## Cases Run

1. `tank_pressure`
   - input: `/home/williambenitez1/Capstone/tests/data/tank.jpg`
2. `operational_tank4`
   - input:
     `/home/williambenitez1/Capstone/z_reference_docs/Data_set_Storage/Unlabeled Photos/Tanks/Operational/operational_tank4.jpg`

## Evaluation Tracks

- `eval_vs_qwen_v009` for both tank cases
- raw detection diagnostics captured for both tank cases

## Primary Question

Can a minimal detect-only adjustment reverse the explicit empty-detections
abstention on `tank_pressure` without reopening the `operational_tank4`
regression?
