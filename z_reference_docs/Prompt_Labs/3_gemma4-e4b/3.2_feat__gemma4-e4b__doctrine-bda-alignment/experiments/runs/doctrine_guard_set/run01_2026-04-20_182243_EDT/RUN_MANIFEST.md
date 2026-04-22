# Gemma Doctrine Guard Set Run 01

- branch: `feat/gemma4-e4b/doctrine-bda-alignment`
- model line: `gemma4:e4b`
- doctrine candidate: `runtime_candidate_doctrine.v001.yaml`
- worktree:
  `/home/williambenitez1/Capstone_worktrees/3.2_feat__gemma4-e4b__doctrine-bda-alignment`
- Ollama host:
  `http://127.0.0.1:11435`
- input folder:
  `input_images/`
- output folder:
  `gemma_candidate/`

## Input Cases

- `destroyed_building4.jpg`
- `operational_building7.jpg`
- `tank_pressure.jpg`
- `operational_tank4.jpg`
- `destroyed_tank15.jpg`
- `office_negative.jpg`

## Command

```bash
OLLAMA_HOST=http://127.0.0.1:11435 uv run bda-svc -i <run-root>/input_images -o <run-root>/gemma_candidate
```

## Early Read

- held:
  - `tank_pressure`
  - `destroyed_tank15`
  - `office_negative`
- regressed:
  - `operational_tank4` returned to `DAMAGED / PROBABLE`
  - `operational_building7` gained a false-positive `military_equipment`
    detection
- unresolved:
  - `destroyed_building4` still did not improve into the stronger held Gemma
    direction from the active branch

## Current Interpretation

This first doctrine candidate is an early no-go for broader Gemma sweep. It
reopens held control regressions and does not solve the current building
severity problem cleanly enough to justify widening the evaluation yet.
