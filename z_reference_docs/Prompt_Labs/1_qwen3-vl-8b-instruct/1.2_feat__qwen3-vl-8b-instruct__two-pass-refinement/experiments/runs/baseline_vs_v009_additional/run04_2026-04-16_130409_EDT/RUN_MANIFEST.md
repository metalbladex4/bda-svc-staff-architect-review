# Additional Baseline Comparison Run 04

- comparison type: `origin_main baseline vs v009`
- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- base commit: `28e863b`
- baseline source: `baseline/config.pipeline-baseline.yaml`
- candidate source: `experiments/versions/v009_unified_best-stack.yaml`

## Purpose

Run three new challenge images from `z_reference_docs/Data_set_Storage/`
against:

- the clean `origin/main` baseline prompt stack
- the unified `v009` winner stack

This run was intended as a stronger sanity check for the team: do the prompt
changes still behave usefully on new images that were not part of the earlier
mixed pack?

## Selected Images

1. `multi_object_destroyed_building6`
   - source:
     `Data_set_Storage/Unlabeled Photos/Buildings/Destroyed/destroyed_building6.jpg`
   - reason:
     multi-object urban scene with three distinct building masses and heavy
     rubble in the foreground

2. `smoke_fire_destroyed_truck15`
   - source:
     `Data_set_Storage/Unlabeled Photos/Trucks/Destroyed/destroyed_truck15.jpg`
   - reason:
     target body is partly obscured by smoke and visible flame, with additional
     scene clutter

3. `complex_destroyed_building3`
   - source:
     `Data_set_Storage/Unlabeled Photos/Buildings/Destroyed/destroyed_building3.png`
   - reason:
     complex vertical scene with a heavily damaged foreground building, a
     secondary intact building in the background, and distracting wires /
     foreground people

## Run Method

1. Verified the saved branch-aware baseline snapshot matches
   `/home/williambenitez1/Capstone/src/bda_svc/pipeline/config.yaml`.
2. Built `v009_effective_config.yaml` by applying the unified `v009` prompt
   surfaces onto the same baseline runtime config.
3. For each image:
   - ran `bda-svc` once with the baseline config into `baseline_origin_main/`
   - ran `bda-svc` once with the unified `v009` config into `v009_candidate/`
   - ran `bda_eval` with baseline as reference and `v009` as candidate to
     produce:
     - `evaluation_*.csv`
     - `bbox_review_sheet.jpg`
4. Restored the live feature-branch config and verified it matched the saved
   baseline snapshot exactly.

## Headline Read

These three additional tests do **not** show a dramatic win in every case.

What they do show is still useful:

- `v009` stayed stable on all three new challenge images
- it preserved target recall on the new multi-object and complex scenes
- it preserved the same smoke/fire case classification and bbox while keeping
  the newer wording discipline
- it made small bbox refinements on the building scenes without introducing new
  target-count regressions

That means the current stack looks more like a real generalization improvement
than a tank-only mockup, but the evidence is still stronger for
**consistency/stability** than for a huge across-the-board leap.

## Per-Case Read

### `multi_object_destroyed_building6`

- baseline:
  - 3 building targets
  - `SEVERE DAMAGE` / `PROBABLE` on the left structure
  - two `MODERATE DAMAGE` / `PROBABLE` right-side buildings
- `v009`:
  - same 3 target count
  - same category/confidence structure
  - slightly adjusted boxes:
    - left building widened from `[0, 143, 544, 306]` to `[0, 143, 571, 306]`
    - middle building shifted to `[843, 105, 1088, 296]`
    - right building tightened vertically to `[1088, 74, 1360, 296]`

Read:

- this is a **stability win**, not a categorical win
- the important part is that `v009` preserved full three-building recall on a
  new multi-object scene
- that helps show the multi-target building behavior is not limited to the one
  older validation image

### `smoke_fire_destroyed_truck15`

- baseline:
  - 1 `military_equipment`
  - `DAMAGED` / `PROBABLE`
  - bbox `[97, 120, 1173, 600]`
- `v009`:
  - same target count
  - same `DAMAGED` / `PROBABLE`
  - same bbox `[97, 120, 1173, 600]`
  - shorter, cleaner supporting logic tied to visible fire/smoke on the target
    body

Read:

- this is a **non-regression result**
- the newer stack did not break on a smoke/fire-obscured case
- the main gain here is cleaner wording discipline, not changed detection or
  category output

### `complex_destroyed_building3`

- baseline:
  - 2 building targets
  - damaged foreground tower: `SEVERE DAMAGE` / `PROBABLE`
  - intact background building: `NO DAMAGE` / `CONFIRMED`
  - second bbox `[500, 269, 621, 429]`
- `v009`:
  - same 2 target count
  - same category/confidence structure
  - same main damaged-building box `[95, 0, 431, 552]`
  - larger second-building box `[500, 263, 689, 552]`

Read:

- this is the clearest bbox refinement among the three new tests
- `v009` preserved the difficult foreground/background separation and expanded
  the intact background-building box to cover more of the visible building body
- that is a small but real sign that the refined detect rule is carrying over
  to another cluttered building scene

## Decision

- `keep`
- treat this run as additional support that `v009` is a genuine generalization
  improvement, especially on multi-object building behavior
- be honest that the new stack shows:
  - clear stability
  - some bbox refinement
  - cleaner logic/summary discipline
  - but not a dramatic win on every new image

## Team-Facing Framing

The strongest honest takeaway for the team is:

- the prompt changes are **not** just a one-image mockup
- on new challenge images, the current stack continues to:
  - preserve multi-target recall
  - avoid regressions on smoke/fire cases
  - keep difficult foreground/background separations intact
- the improvements are currently strongest in:
  - cross-image consistency
  - doctrinal wording discipline
  - preserved target separation
  - modest bbox refinement on some scenes
