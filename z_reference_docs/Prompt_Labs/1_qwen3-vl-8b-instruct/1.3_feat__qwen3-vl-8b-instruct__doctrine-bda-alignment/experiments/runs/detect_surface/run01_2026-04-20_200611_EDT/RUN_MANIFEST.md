# Qwen Doctrine-Side Detect Surface Run 01

- branch: `feat/qwen3-vl-8b-instruct/doctrine-bda-alignment`
- model line: `qwen3-vl:8b-instruct`
- mirrored candidate source:
  `1.2:v010_detect_objects_adjacent-building-target-body-priority`
- worktree:
  `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment`
- parent control branch:
  `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- run purpose:
  verify whether the same detect-only user-prompt weighting change behaves
  similarly when the doctrine-side branch keeps its different injected doctrine
  block

## Candidate Scope

Only `detect_objects` changed, mirrored from the active `1.2` Qwen lane.

Doctrine remained unchanged in this run relative to the current `1.3` branch
state.

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

- `destroyed_building4` shows the same key recovery direction as `1.2`:
  - parent control split the scene into two destroyed buildings
  - candidate collapsed the read to one scene-central destroyed building
- `destroyed_building3` still boxes the background building as a second target
- `destroyed_building6` remains the same broad scene-partitioning pattern,
  aside from tiny coordinate drift
- `office_negative` and `operational_tank4` remained clean
- `tank_pressure` and `destroyed_tank15` showed only small bbox drift
- doctrine-side verification did not collapse into a materially different read
  from the active `1.2` branch on the main building-selection question

## Current Interpretation

This mirrored run supports the same conclusion as the active `1.2` lane:

- detect-surface weighting is a real lever
- doctrine-only wording was not the main lever
- the new rule is promising because it improves `destroyed_building4` in both
  branches, not just one

The remaining open question is how to preserve that gain while fixing
`destroyed_building3` and `destroyed_building6`.

## Companion Artifacts

- parent-vs-candidate eval:
  - `eval_vs_parent_control/`
- bbox review sheets:
  - `eval_vs_parent_control/images_bbox_review/`
- cross-branch review note:
  - `/home/williambenitez1/Capstone/z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detect_candidate_a_run01_review.md`
