# Qwen Detect Surface Run 04

- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- candidate version:
  `v013_detect_objects_building-priority-decision-order`
- worktree:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`
- run purpose:
  preserve the `v010` `destroyed_building4` recovery while testing whether a
  stronger instruction hierarchy can suppress the `destroyed_building3`
  background-building false positive and reduce the broad scene partitioning on
  `destroyed_building6`

## Candidate Scope

Only `detect_objects` changed.

Exact intervention:

- kept the `v010` adjacent-building target-body rule set intact
- added a top-of-prompt `BUILDING TARGET PRIORITY` decision order
- added one supporting foreground-vs-background building example
- kept doctrine injection, system prompt, assessment prompt, and summary prompt
  unchanged

## Validation

- static checks passed before the run:
  - `uv run pytest tests/unit/test_yamls.py tests/unit/test_utilities.py`

## Parent Control

This run reuses the `qwen_candidate_a/` outputs from detect-surface run01 as
the parent control because that folder exactly represents the live `v010`
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

## Commands

Candidate:

```bash
uv run bda-svc -i <run-root>/input_images -o <run-root>/qwen_candidate_v013
```

Parent-vs-candidate eval:

```bash
uv run python bda_eval/main.py \
  -r <run-root>/qwen_parent_control \
  -p <run-root>/qwen_candidate_v013 \
  -i <run-root>/input_images \
  -o <run-root>/eval_vs_parent_control
```

## Early Read

- `destroyed_building4` stayed recovered as one scene-central destroyed
  building
- `destroyed_building3` still boxed the background building as a second target
- `destroyed_building6` still returned three buildings
- `office_negative`, `operational_tank4`, and `tank_pressure` stayed clean
- some bbox and wording drift appeared, but not enough to count as a targeted
  win in the active `1.2` line

## Current Interpretation

This is not a clear upgrade over `v010` for the active Qwen line.

The stronger hierarchy wording did not move `1.2` enough on the two still-open
building failures, so it is not the next live state here.

Working implication:

- hierarchy can matter, but this specific form did not beat `v010` in `1.2`
- `v013` should be recorded, then rejected
- the best current local Qwen state remains `v010`

## Companion Artifacts

- candidate version:
  - `../../versions/v013_detect_objects_building-priority-decision-order.yaml`
- parent-vs-candidate eval:
  - `eval_vs_parent_control/`
- bbox review sheets:
  - `eval_vs_parent_control/images_bbox_review/`
- cross-branch review note:
  - `/home/williambenitez1/Capstone/z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detect_candidate_d_run04_review.md`
