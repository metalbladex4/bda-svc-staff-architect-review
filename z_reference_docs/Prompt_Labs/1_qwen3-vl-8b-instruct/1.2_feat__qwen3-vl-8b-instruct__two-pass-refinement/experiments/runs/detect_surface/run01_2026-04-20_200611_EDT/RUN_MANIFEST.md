# Qwen Detect Surface Run 01

- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- candidate version: `v010_detect_objects_adjacent-building-target-body-priority`
- worktree:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`
- run purpose:
  test whether a stronger top-level adjacent-building target-body rule in the
  detection user prompt improves mixed-building target selection without
  reopening the held tank and negative controls

## Candidate Scope

Only `detect_objects` changed.

Exact intervention:

- added one higher-salience building-selection rule in the top `RULES` block
- tightened the later building boxing sentence to limit separate boxes to
  visibly separate exterior building bodies or clearly separate collapsed
  exterior structural remains
- kept doctrine injection, system prompt, assessment prompt, and summary prompt
  unchanged

## Validation

- static checks passed before the run:
  - `uv run pytest tests/unit/test_yamls.py tests/unit/test_utilities.py`

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

Parent control:

```bash
uv run bda-svc -i <run-root>/input_images -o <run-root>/qwen_parent_control
```

Candidate:

```bash
uv run bda-svc -i <run-root>/input_images -o <run-root>/qwen_candidate_a
```

Parent-vs-candidate eval:

```bash
uv run python bda_eval/main.py \
  -r <run-root>/qwen_parent_control \
  -p <run-root>/qwen_candidate_a \
  -i <run-root>/input_images \
  -o <run-root>/eval_vs_parent_control
```

## Early Read

- strong visual improvement on `destroyed_building4`:
  - parent control boxed two buildings
  - candidate collapsed the read to one scene-central destroyed building
  - bbox review suggests this is the intended target-body-selection recovery,
    not a random box drift
- `destroyed_building3` still boxes the background building as a second target
- `destroyed_building6` remains a broad scene-partitioning read
- `destroyed_building5`, `destroyed_building8`, `operational_building7`,
  `operational_tank4`, `tank_pressure`, and `office_negative` held cleanly
- minor non-material bbox drift appeared on:
  - `destroyed_tank15`
  - `operational_building2`
  - `operational_building91`

## Current Interpretation

This is a promising partial Qwen detection win.

It does not solve the full adjacent-building family, but it improves the most
important held failure surface, `destroyed_building4`, while keeping the core
negative and tank controls intact.

Working implication:

- the actual detection prompt surface is a stronger lever than doctrine-only
  wording for this problem
- the next iteration should preserve the `destroyed_building4` recovery while
  targeting the remaining `destroyed_building3` and `destroyed_building6`
  failures more directly

## Companion Artifacts

- candidate version:
  - `../../versions/v010_detect_objects_adjacent-building-target-body-priority.yaml`
- parent-vs-candidate eval:
  - `eval_vs_parent_control/`
- bbox review sheets:
  - `eval_vs_parent_control/images_bbox_review/`
- cross-branch review note:
  - `/home/williambenitez1/Capstone/z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detect_candidate_a_run01_review.md`
