# Qwen Doctrine-Side Detect Surface Run 02

- branch: `feat/qwen3-vl-8b-instruct/doctrine-bda-alignment`
- model line: `qwen3-vl:8b-instruct`
- mirrored candidate source:
  `1.2:v011_detect_objects_scene-central-background-suppression`
- worktree:
  `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment`
- parent control branch:
  `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- run purpose:
  verify whether the same scene-dominance/background-suppression follow-up
  helps when the doctrine-side branch keeps its different injected doctrine
  block

## Candidate Scope

Only `detect_objects` changed, mirrored from the active `1.2` Qwen lane.

Doctrine remained unchanged in this run relative to the current `1.3` branch
state.

## Validation

- static checks passed before the run:
  - `uv run pytest tests/unit/test_yamls.py tests/unit/test_utilities.py`

## Parent Control

This run reuses the `qwen_candidate_a/` outputs from detect-surface run01 as
the parent control because that folder exactly represents the mirrored `v010`
state before the `v011` wording change.

## Input Cases

- `destroyed_building3.png`
- `destroyed_building4.jpg`
- `destroyed_building5.png`
- `destroyed_building6.jpg`
- `destroyed_building8.jpg`
- `operational_building2.jpg`
- `operational_building7.jpg`
- `operational_building91.jpg`
- `destroyed_tank15.jpg`
- `operational_tank4.jpg`
- `tank_pressure.jpg`
- `office_negative.jpg`

## Early Read

- `destroyed_building4` remained recovered as one scene-central destroyed
  building
- `destroyed_building3` still boxed the background building
- `destroyed_building6` still returned three buildings
- `office_negative` and `operational_tank4` remained clean
- doctrine-side verification did not reveal a hidden win that was missing in
  `1.2`

## Current Interpretation

This mirrored run agrees with `1.2`:

- `v011` does not beat `v010`
- the added scene-dominance/background-suppression wording is not enough to
  resolve the remaining building failures

Working implication:

- the doctrine-side lane still supports the same high-level read:
  prompt-surface weighting matters, but this specific next wording step was not
  strong enough
- `v010` remains the stronger local Qwen state to keep

## Companion Artifacts

- parent-vs-candidate eval:
  - `eval_vs_parent_control/`
- bbox review sheets:
  - `eval_vs_parent_control/images_bbox_review/`
- cross-branch review note:
  - `/home/williambenitez1/Capstone/z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detect_candidate_b_run02_review.md`
