# Baseline vs `v009` Blind Sweep Run 01

- comparison type: `origin_main baseline vs v009`
- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- base commit: `28e863b`
- baseline source: `baseline/config.pipeline-baseline.yaml`
- candidate source: `experiments/versions/v009_unified_best-stack.yaml`
- sweep size: `10 images`

## Purpose

Run a broader balanced challenge sweep so we can tell the team something
stronger than “the new stack looks good on a few hand-tuned examples.”

This sweep compared the clean `origin/main` baseline prompt stack against the
current unified `v009` winner stack on ten additional images spanning:

- destroyed buildings
- operational buildings
- destroyed tanks
- operational tanks
- destroyed trucks
- operational trucks

## Selected Pack

Destroyed buildings:

- `destroyed_building5.png`
- `destroyed_building7.jpg`

Operational buildings:

- `operational_building59.jpg`
- `operational_building90.jpg`

Destroyed tanks:

- `destroyed_tank10.jpg`
- `destroyed_tank37.jpg`

Operational tanks:

- `operational_tank21.jpg`
- `operational_tank33.jpg`

Destroyed / operational trucks:

- `destroyed_truck1.jpg`
- `operational_truck14.jpg`

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

## Headline Numbers

- cases run: `10`
- same target count baseline vs `v009`: `10 / 10`
- same damage/confidence structure: `6 / 10`
- exact same bbox set: `2 / 10`
- cases with changed damage category: `2 / 10`
- cases with changed confidence only: `2 / 10`

## Headline Read

This sweep supports a stronger claim than a seed-case demo, but still an honest
one:

- `v009` is **stable** across a broader unseen pack
- it preserved target-count recall on all 10 additional images
- most differences are calibration / wording / bbox refinements rather than
  target-count collapses or new hallucinated targets
- there are still a couple of genuine judgment changes we should keep visible
  as caution cases

## Case Buckets

### 1. Stable Or Near-Stable Cases

These kept the same basic target count and damage/confidence interpretation,
with only minor wording or bbox differences:

- `destroyed_building7`
- `operational_building59`
- `operational_building90`
- `operational_tank21`
- `operational_tank33`
- `operational_truck14`

Interpretation:

- this is strong evidence that the current stack is not fragile outside the
  original mixed pack

### 2. Conservative Calibration Shifts

These kept the same core category but moved confidence down from
`CONFIRMED` to `PROBABLE`:

- `destroyed_tank10`
- `destroyed_truck1`

Interpretation:

- this is directionally consistent with the broader design of the newer stack:
  prefer lower confidence unless the visual evidence is unmistakable
- for team-facing framing, these are better described as **calibration
  differences**, not outright regressions

### 3. Meaningful Judgment Changes

These changed the damage-category call itself:

- `destroyed_building5`
  - baseline: `SEVERE DAMAGE`
  - `v009`: `DESTROYED`
- `destroyed_tank37`
  - baseline: `DESTROYED`
  - `v009`: `DAMAGED`

Interpretation:

- these are the two cases that most clearly deserve follow-up review
- `destroyed_building5` may reflect a stricter catastrophic-loss read by the
  new stack
- `destroyed_tank37` is the clearest caution case, because the new stack became
  more conservative on a vehicle that is visibly burning and smoke-obscured

## Decision

- `keep`
- treat this sweep as added support that `v009` is a real improvement in
  cross-image stability and recall discipline
- do **not** claim the sweep proves perfection
- carry `destroyed_building5` and especially `destroyed_tank37` forward as the
  most important review cases if we do any future fine-tuning
