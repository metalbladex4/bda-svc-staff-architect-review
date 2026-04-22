# Grounding Generalization Pack V1

## Purpose

This pack exists to answer one question:

- can a grounding-rule change improve bbox behavior without overfitting to `tank.jpg`?

`tests/data/tank.jpg` remains the pressure test because it exposes the hardest
known grounding failure in this branch-aware line. It is not enough by itself
to justify a new detection winner.

Every future **detect-only** bbox candidate should be checked against this pack
before we treat it as a true improvement.

## Validation Images

### 1. Pressure Test

- `tests/data/tank.jpg`

Purpose:

- keep the hardest known burning-target localization case in the loop
- reject candidates that drift back to smoke, terrain, or an overly small burn
  patch

### 2. Destroyed Tank Control

- `/home/williambenitez1/Capstone/z_reference_docs/Data_set_Storage/Unlabeled Photos/Tanks/Destroyed/destroyed_tank15.jpg`

Purpose:

- check whether the grounding rule still works on another damaged armored
  target with different scene layout
- verify that the candidate does not become too tied to the exact geometry of
  the seed image

### 3. Operational Tank Control

- `/home/williambenitez1/Capstone/z_reference_docs/Data_set_Storage/Unlabeled Photos/Tanks/Operational/operational_tank4.jpg`

Purpose:

- verify that the rule still boxes the visible target body when fire and smoke
  are not the main visual cue
- catch over-reliance on “burning object” cues

### 4. Destroyed Building Control

- `/home/williambenitez1/Capstone/z_reference_docs/Data_set_Storage/Unlabeled Photos/Buildings/Destroyed/destroyed_building4.jpg`

Purpose:

- test whether the grounding rule generalizes across doctrinal target classes
- catch prompts that only work well on long horizontal vehicle-like shapes

### 5. Operational Building Control

- `/home/williambenitez1/Capstone/z_reference_docs/Data_set_Storage/Unlabeled Photos/Buildings/Operational/operational_building7.jpg`

Purpose:

- verify that the rule still behaves on intact structure imagery
- catch prompts that collapse onto only the most visually salient fragment

### 6. Negative / Non-BDA Scene Control

- `/home/williambenitez1/Capstone/z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/assets/spatial_understanding/office.jpg`

Purpose:

- catch hallucinated detections on scenes outside the project’s relevant target
  space
- make sure bbox changes do not increase false positives while solving the tank
  pressure case

## How To Use This Pack

For a new detect-only candidate:

1. Freeze `assess_damage` and `summarize_scene` at the current confirmed
   leader.
2. Change only `detect_objects`.
3. Run the fresh branch-aware `v000` baseline on each image.
4. Run the candidate on each image.
5. Use `bda_eval` artifact generation to review baseline vs candidate for each
   image.
6. Record the per-image readout in the run manifest or a sweep summary.

### Practical File-Handling Note

- Images sourced from `z_reference_docs/Data_set_Storage/` may be copied into
  per-run worktree or prompt-lab output folders when needed for evaluation.
- Those copied images can remain in the run folders as part of the preserved
  review artifact set.
- This is acceptable for the active branch-aware workflow and does not require
  moving the original source images out of `Data_set_Storage/`.

## Review Rules

When reviewing each image, ask:

- does the box stay on the visible connected target body or structure?
- does it avoid smoke, fire plume, shadow, road, rail, or empty ground?
- does it avoid collapsing to only the hottest or most salient local patch?
- does it behave reasonably when the target is intact, not burning, or not a
  vehicle?
- does it avoid creating a new false positive on the negative scene?

## Promotion Gate For Grounding Changes

A bbox candidate should not be treated as a new working leader unless:

- it improves or at least preserves the `tank.jpg` pressure case
- it does not introduce a clear regression on the mixed controls
- it does not increase false positives on the negative scene
- it does not reintroduce subtype drift or unsupported scene-detail wording as
  a side effect

## Current Default Comparison

Until a stronger cross-image winner is proven:

- reference baseline for mixed sweeps: `v000`
- current confirmed full-stack leader: `v004`
- current best detection-only signal to preserve: `v001`

This means the next grounding-focused micro-cycle should normally compare a
detect-only candidate against `v000` and then judge whether it is safe to carry
forward into the `v004` stack.
