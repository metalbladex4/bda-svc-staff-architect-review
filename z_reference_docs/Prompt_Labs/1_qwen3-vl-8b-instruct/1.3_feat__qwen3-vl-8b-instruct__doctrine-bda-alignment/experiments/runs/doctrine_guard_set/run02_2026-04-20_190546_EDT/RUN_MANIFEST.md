# Qwen Doctrine Guard Set Run 02

- branch: `feat/qwen3-vl-8b-instruct/doctrine-bda-alignment`
- model line: `qwen3-vl:8b-instruct`
- doctrine candidate: `runtime_candidate_doctrine.v002.yaml`
- worktree:
  `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment`
- parent control branch:
  `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- rerun purpose:
  test whether tightening only `buildings.detection_guidance` improves target
  selection in mixed adjacent-building scenes before touching Gemma again

## Validation

- static checks passed before the rerun:
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
- `tank_pressure.jpg`
- `operational_tank4.jpg`
- `destroyed_tank15.jpg`
- `office_negative.jpg`

## Commands

Candidate:

```bash
uv run bda-svc -i <run-root>/input_images -o <run-root>/qwen_candidate
```

Parent control:

```bash
uv run bda-svc -i <run-root>/input_images -o <run-root>/qwen_parent_control
```

Parent-vs-candidate eval:

```bash
uv run python bda_eval/main.py \
  -r <run-root>/qwen_parent_control \
  -p <run-root>/qwen_candidate \
  -i <run-root>/input_images \
  -o <run-root>/eval_vs_parent_control
```

## Early Read

- mostly neutral on the added building cases
- controls still held:
  - `destroyed_building5`
  - `destroyed_building8`
  - `operational_building2`
  - `operational_building7`
  - `operational_building91`
  - `operational_tank4`
  - `destroyed_tank15`
  - `office_negative`
- unresolved or negative:
  - `destroyed_building3` still boxed a background building as a second target
  - `destroyed_building6` remained a broad scene-partitioning read
  - `destroyed_building4` worsened relative to the held control:
    - held control: `SEVERE DAMAGE` + `DESTROYED`
    - candidate: `DESTROYED` + `DESTROYED`

## Current Interpretation

This is not a winning Qwen doctrine direction.

The `v002` change was intentionally narrow and useful as a test, but the result
shows that tighter building-selection wording inside doctrine is not a strong
enough lever, by itself, to fix the current adjacency/scene-partitioning
problem.

## Companion Artifacts

- parent-vs-candidate eval:
  - `eval_vs_parent_control/`
- bbox review sheets:
  - `eval_vs_parent_control/images_bbox_review/`
- doctrine notes:
  - `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/runtime_candidate_doctrine.v002.notes.md`
  - `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_destroyed_building4_manual_review.md`
