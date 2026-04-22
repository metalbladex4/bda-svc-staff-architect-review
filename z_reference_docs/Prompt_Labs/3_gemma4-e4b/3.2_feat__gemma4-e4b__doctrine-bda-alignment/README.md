# 3.2 Doctrine Lab

This is the doctrine-alignment experiment branch for the Gemma line.

- branch: `feat/gemma4-e4b/doctrine-bda-alignment`
- parent branch: `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- model line: `gemma4:e4b`
- creation base commit: `9ae27e9`

## Purpose

This branch exists to test whether a more doctrine-faithful but
prompt-compatible Phase-1 PDA doctrine file can improve or clarify behavior
without degrading the current held Gemma cases.

## Working Rule

- use the parent feature branch as the control
- keep the experiment scoped to doctrine replacement first, not broad prompt
  rewrites
- respect the local Gemma host requirement:
  - `OLLAMA_HOST=http://127.0.0.1:11435`

## Audit Package

The shared doctrine audit and candidate files for this branch live under:

- `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/`

## Current Status

- the first runtime candidate doctrine is now installed in this branch
- static runtime checks passed:
  - `uv run pytest tests/unit/test_yamls.py tests/unit/test_utilities.py`
- the first doctrine-sensitive guard-set run now exists under:
  - `experiments/runs/doctrine_guard_set/run01_2026-04-20_182243_EDT/`
- early read:
  - held `tank_pressure`, `destroyed_tank15`, and `office_negative`
  - regressed `operational_tank4` back to `DAMAGED / PROBABLE`
  - introduced a false-positive `military_equipment` detection on
    `operational_building7`
- next gate:
  - do **not** broaden this candidate to a full inherited sweep until a
    revision removes those reopened control regressions
