# Qwen Doctrine Guard Set Run 01

- branch: `feat/qwen3-vl-8b-instruct/doctrine-bda-alignment`
- model line: `qwen3-vl:8b-instruct`
- doctrine candidate: `runtime_candidate_doctrine.v001.yaml`
- worktree:
  `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment`
- input folder:
  `input_images/`
- output folder:
  `qwen_candidate/`

## Input Cases

- `destroyed_building4.jpg`
- `operational_building7.jpg`
- `tank_pressure.jpg`
- `operational_tank4.jpg`
- `destroyed_tank15.jpg`
- `office_negative.jpg`

## Command

```bash
uv run bda-svc -i <run-root>/input_images -o <run-root>/qwen_candidate
```

## Early Read

- held:
  - `office_negative`
  - `operational_building7`
  - `operational_tank4`
  - `destroyed_tank15`
  - `tank_pressure`
- changed:
  - `destroyed_building4` returned two `DESTROYED / PROBABLE` buildings

## Current Interpretation

The first pass preserved the control cases, but later same-input parent-control
comparison showed that `destroyed_building4` is not a meaningful doctrine win.
The held Qwen control already returns the same two `DESTROYED / PROBABLE`
buildings.

## Follow-Up Review

- parent control folder:
  - `qwen_parent_control/`
- bbox review folder:
  - `destroyed_building4_eval/`
- focused note:
  - `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_destroyed_building4_manual_review.md`

Current conclusion:

- the doctrine candidate did not materially improve bbox quality
- the doctrine candidate did not materially improve doctrinal fit on
  `destroyed_building4`
- the main remaining Qwen issue on this scene is target
  delimitation/localization rather than PDA wording alone
