# Qwen Doctrine-Side Detect Surface Run 04

- branch: `feat/qwen3-vl-8b-instruct/doctrine-bda-alignment`
- model line: `qwen3-vl:8b-instruct`
- mirrored candidate source:
  `1.2:v013_detect_objects_building-priority-decision-order`
- worktree:
  `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment`
- parent control branch:
  `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- run purpose:
  verify whether the same hierarchy-first follow-up helps when the doctrine-side
  branch keeps its different injected doctrine block

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
state before the `v013` wording change.

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
- `destroyed_building3` improved materially by removing the background-building
  false positive
- `destroyed_building6` still returned three buildings
- doctrine-side verification revealed a real but asymmetric gain that did not
  appear in `1.2`

## Current Interpretation

This mirrored run is useful evidence, but not enough to promote `v013`.

It shows that the stronger hierarchy wording can matter, especially when
combined with the doctrine-side prompt context, but the gain did not transfer
cleanly into the active `1.2` lane and the `destroyed_building6` failure still
remains.

Working implication:

- `v013` should be treated as a documented asymmetric signal, not a new live
  winner
- this branch’s live detect prompt has also been restored to the mirrored
  `v010` state

## Companion Artifacts

- parent-vs-candidate eval:
  - `eval_vs_parent_control/`
- bbox review sheets:
  - `eval_vs_parent_control/images_bbox_review/`
- cross-branch review note:
  - `/home/williambenitez1/Capstone/z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detect_candidate_d_run04_review.md`
