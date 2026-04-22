# Mixed Generalization Sweep Run 02

- run type: `generalization_sweep`
- purpose: compare the fresh branch-aware `v000` baseline against the frozen
  `v006 + v008 + v004` stack across the mixed image pack
- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- base commit: `28e863b`
- sweep pack:
  - `tests/data/tank.jpg`
  - `destroyed_tank15.jpg`
  - `operational_tank4.jpg`
  - `destroyed_building4.jpg`
  - `operational_building7.jpg`
  - `office.jpg`

## Frozen Stack Under Test

- `detect_objects` from `v006`
- `assess_damage` from `v008`
- `summarize_scene` from `v004`

## Run Method

1. Created a sweep root under `experiments/runs/generalization_sweep/`.
2. Saved the pre-sweep live feature-branch config at:
   - `original_live_config.before_sweep.yaml`
3. Built:
   - `frozen_v006_v008_v004_effective_config.yaml`
4. For each image in the mixed pack:
   - copied the source image into a case-local `images/` folder
   - copied the fresh branch-aware baseline config into the live worktree
     `src/bda_svc/pipeline/config.yaml`
   - ran `bda-svc` into `v000_baseline/`
   - copied the frozen full-stack config into the live worktree
     `src/bda_svc/pipeline/config.yaml`
   - ran `bda-svc` into `frozen_v006_v008_v004_stack/`
   - ran `bda_eval` on the paired report folders and case-local image folder
5. Restored the live feature-branch config to the saved branch-aware baseline
   and verified it matched exactly.

## Headline Result

This frozen stack clears the two most important failures from the earlier
`v000` vs `v004` sweep:

- `operational_tank4` no longer regresses to `DAMAGED`
- `destroyed_building4` no longer collapses into one target

So this is the strongest cross-image stack in the branch-aware line so far.

## Per-Case Readout

### `tank_pressure`

- baseline:
  - bbox `[51, 37, 102, 73]`
  - `DESTROYED`
  - `PROBABLE`
- frozen stack:
  - bbox `[51, 37, 128, 73]`
  - `DESTROYED`
  - `PROBABLE`

Read:

- candidate keeps the wider rightward coverage relative to baseline
- category/confidence stay stable
- summary remains cleaner and more conservative than the baseline wording

### `destroyed_tank15`

- baseline:
  - bbox `[36, 21, 448, 166]`
  - `DESTROYED`
  - `CONFIRMED`
- frozen stack:
  - bbox `[36, 21, 457, 166]`
  - `DESTROYED`
  - `PROBABLE`

Read:

- bbox stayed very close with slightly wider horizontal coverage
- confidence became more conservative
- logic wording stayed factual and did not reintroduce `K-kill`

### `operational_tank4`

- baseline:
  - bbox `[66, 317, 515, 499]`
  - `NO DAMAGE`
  - `CONFIRMED`
- frozen stack:
  - bbox `[66, 317, 515, 499]`
  - `NO DAMAGE`
  - `CONFIRMED`

Read:

- the earlier full-stack regression is now fixed
- bbox held exactly
- the new assessment wording correctly treats the visible flash and smoke as a
  firing signature rather than body damage

### `destroyed_building4`

- baseline:
  - two targets:
    - `[0, 18, 63, 176]` -> `SEVERE DAMAGE`, `PROBABLE`
    - `[63, 18, 287, 176]` -> `DESTROYED`, `CONFIRMED`
- frozen stack:
  - two targets:
    - `[0, 18, 69, 141]` -> `DESTROYED`, `PROBABLE`
    - `[69, 18, 250, 158]` -> `DESTROYED`, `PROBABLE`

Read:

- the major recall failure from the earlier sweep is fixed
- the image is no longer collapsed into one building target
- residual nuance:
  - the frozen stack assesses both buildings as `DESTROYED`
  - the baseline split them as `SEVERE DAMAGE` and `DESTROYED`
- so the recall/generalization problem is clearly improved, but building
  severity calibration is still something to keep watching

### `operational_building7`

- baseline:
  - bbox `[64, 119, 1315, 478]`
  - `NO DAMAGE`
  - `CONFIRMED`
- frozen stack:
  - bbox `[64, 119, 1315, 459]`
  - `NO DAMAGE`
  - `CONFIRMED`

Read:

- stable and acceptable
- no meaningful regression in target-level behavior

### `office_negative`

- baseline:
  - `object_not_found`
  - bbox `[0, 0, 0, 0]`
- frozen stack:
  - `object_not_found`
  - bbox `[0, 0, 0, 0]`

Read:

- no false-positive increase
- raw `bda-svc` JSON remained correct on both sides
- `bda_eval` still hit the current `NOT APPLICABLE` scoring limitation, so
  this case should still be judged from the raw JSON and image artifacts

## Decision

- the frozen `v006 + v008 + v004` stack is now the strongest cross-image
  branch-aware candidate so far
- it resolves the earlier operational-tank assessment regression
- it resolves the earlier destroyed-building recall regression
- it keeps the negative office behavior clean
- the main residual caution is building-severity calibration on
  `destroyed_building4`, not detection recall
