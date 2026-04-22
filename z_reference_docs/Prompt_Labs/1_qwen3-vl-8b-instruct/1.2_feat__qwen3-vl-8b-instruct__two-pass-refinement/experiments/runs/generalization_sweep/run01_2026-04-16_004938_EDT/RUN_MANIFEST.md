# Mixed Grounding Generalization Sweep Run 01

- run type: `generalization_sweep`
- purpose: compare the fresh branch-aware `v000` baseline against the confirmed
  `v004` stack across the mixed image pack
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

## Run Method

1. Created a sweep root under `experiments/runs/generalization_sweep/`.
2. Saved the pre-run live feature-branch config at:
   - `original_live_config.before_sweep.yaml`
3. For each image in the mixed pack:
   - copied the source image into a case-local `images/` folder
   - copied the fresh branch-aware baseline config into the live worktree
     `src/bda_svc/pipeline/config.yaml`
   - ran `bda-svc` into `v000_baseline/`
   - copied the confirmed `v004` effective config into the live worktree
     `src/bda_svc/pipeline/config.yaml`
   - ran `bda-svc` into `v004_candidate/`
   - ran `bda_eval` on the paired report folders and case-local image folder
4. Restored the live feature-branch config to the saved branch-aware baseline
   and verified it matched exactly.

## Headline Result

The sweep answered the core question directly:

- the current `v004` stack is strong on the original seed case
- but it is **not yet a clean cross-image grounding winner**

Why:

- `tank.jpg` still moved in the more helpful direction relative to baseline,
  but it did **not** repeat the earlier confirmed `v004` bbox exactly
- `destroyed_tank15` looked acceptable and conservative
- `operational_building7` held cleanly
- `office.jpg` did not introduce a false positive
- but `operational_tank4` regressed from `NO DAMAGE` to `DAMAGED`
- and `destroyed_building4` collapsed a two-target building scene into one
  target, which is a clear detection recall/generalization regression

## Per-Case Readout

### `tank_pressure`

- baseline:
  - bbox `[51, 37, 102, 73]`
  - `DESTROYED`
  - `PROBABLE`
- `v004`:
  - bbox `[51, 37, 128, 73]`
  - `DESTROYED`
  - `PROBABLE`

Read:

- still better horizontal coverage than the baseline box
- but this did not match the earlier confirmed `v004` tank bbox
  `[46, 46, 123, 92]`
- so the seed-case improvement signal remains useful, but repeatability is not
  yet clean enough to call the grounding rule fully stable

### `destroyed_tank15`

- baseline:
  - bbox `[36, 21, 448, 166]`
  - `DESTROYED`
  - `CONFIRMED`
- `v004`:
  - bbox `[36, 21, 448, 166]`
  - `DESTROYED`
  - `PROBABLE`

Read:

- bbox held exactly
- confidence became more conservative
- no obvious grounding regression on this destroyed armored target control

### `operational_tank4`

- baseline:
  - bbox `[66, 317, 515, 499]`
  - `NO DAMAGE`
  - `CONFIRMED`
- `v004`:
  - bbox `[66, 317, 515, 499]`
  - `DAMAGED`
  - `PROBABLE`

Read:

- bbox held exactly
- this is a **target-level assessment regression**, not a grounding regression
- the current `v004` stack still overreads muzzle flash and smoke as damage on
  an operational firing vehicle

### `destroyed_building4`

- baseline:
  - two targets:
    - `[0, 18, 63, 176]` -> `SEVERE DAMAGE`, `PROBABLE`
    - `[63, 18, 287, 176]` -> `DESTROYED`, `CONFIRMED`
- `v004`:
  - one target:
    - `[69, 18, 287, 176]` -> `DESTROYED`, `PROBABLE`

Read:

- this is the clearest cross-image regression in the sweep
- ground-truth clarification now confirms that this image contains two distinct
  buildings
- the candidate missed the left-side damaged building and collapsed the scene
  into one target
- this is a real warning that the current grounding rule is not yet safe to
  promote as a general detect rule across image types

### `operational_building7`

- baseline:
  - bbox `[64, 119, 1315, 478]`
  - `NO DAMAGE`
  - `CONFIRMED`
- `v004`:
  - bbox `[64, 119, 1315, 478]`
  - `NO DAMAGE`
  - `CONFIRMED`

Read:

- stable and acceptable
- no grounding or assessment regression on this intact building control

### `office_negative`

- baseline:
  - `object_not_found`
  - bbox `[0, 0, 0, 0]`
- `v004`:
  - `object_not_found`
  - bbox `[0, 0, 0, 0]`

Read:

- no false-positive increase
- this is a useful pass on the negative scene
- `bda_eval` still hit a current limitation here because `NOT APPLICABLE`
  damage labels do not cleanly flow through the evaluation CSV path

## Artifact Notes

Per-case visual review artifacts were generated for all six cases, including:

- `images_bbox_both/`
- `images_bbox_reference/`
- `images_bbox_predicted/`
- `images_crop_reference/`
- `images_crop_predicted/`
- `images_bbox_review/`
- root `bbox_review_sheet.jpg`

The negative office case still emitted those image artifacts, but `bda_eval`
did not complete the final CSV because it does not yet handle
`NOT APPLICABLE` cleanly in the scoring path.

## Decision

- keep `v004` as the confirmed **seed-case** leader
- do **not** treat `v004` as a proven cross-image grounding winner yet
- use this sweep as the new evidence base for the next detect-only
  generalization cycle

## Next Step

The next grounding step should be more controlled than this full-stack sweep:

1. keep `assess_damage` and `summarize_scene` fixed
2. change only `detect_objects`
3. rerun the mixed pack
4. judge the next bbox candidate on:
   - `tank.jpg` pressure-test performance
   - destroyed-building multi-target recall
   - negative-scene false-positive behavior
