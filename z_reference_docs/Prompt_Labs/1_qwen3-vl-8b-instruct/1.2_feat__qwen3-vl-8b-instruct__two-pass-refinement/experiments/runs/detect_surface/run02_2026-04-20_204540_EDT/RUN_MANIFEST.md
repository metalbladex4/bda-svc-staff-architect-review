# Qwen Detect Surface Run 02

- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- candidate version:
  `v011_detect_objects_scene-central-background-suppression`
- worktree:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`
- run purpose:
  preserve the `v010` `destroyed_building4` recovery while suppressing the
  background-building false positive on `destroyed_building3` and reducing the
  wide-scene building count on `destroyed_building6`

## Candidate Scope

Only `detect_objects` changed.

Exact intervention:

- kept the `v010` adjacent-building target-body rule
- added one more building scene-dominance rule for smaller, distant, or
  peripheral buildings
- added one explicit background-building contrastive example
- kept doctrine injection, system prompt, assessment prompt, and summary prompt
  unchanged

## Validation

- static checks passed before the run:
  - `uv run pytest tests/unit/test_yamls.py tests/unit/test_utilities.py`

## Parent Control

This run reuses the `qwen_candidate_a/` outputs from detect-surface run01 as
the parent control because that folder exactly represents the live `v010`
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

## Commands

Candidate:

```bash
uv run bda-svc -i <run-root>/input_images -o <run-root>/qwen_candidate_b
```

Parent-vs-candidate eval:

```bash
uv run python bda_eval/main.py \
  -r <run-root>/qwen_parent_control \
  -p <run-root>/qwen_candidate_b \
  -i <run-root>/input_images \
  -o <run-root>/eval_vs_parent_control
```

## Early Read

- `destroyed_building4` stayed recovered as one scene-central destroyed
  building
- `destroyed_building3` still boxed the background building as a second target
  even though the second bbox tightened slightly
- `destroyed_building6` still returned three buildings
- `office_negative` and `operational_tank4` stayed clean
- `tank_pressure` and some other held controls drifted slightly without a clear
  benefit

## Current Interpretation

This is not a clear upgrade over `v010`.

It preserves the most important `destroyed_building4` gain, but it does not
actually fix either of the targeted remaining failures:

- `destroyed_building3`
- `destroyed_building6`

Working implication:

- scene-dominance wording alone is not a strong enough next lever
- the best current local Qwen state remains `v010`, not `v011`

## Companion Artifacts

- candidate version:
  - `../../versions/v011_detect_objects_scene-central-background-suppression.yaml`
- parent-vs-candidate eval:
  - `eval_vs_parent_control/`
- bbox review sheets:
  - `eval_vs_parent_control/images_bbox_review/`
- cross-branch review note:
  - `/home/williambenitez1/Capstone/z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detect_candidate_b_run02_review.md`
