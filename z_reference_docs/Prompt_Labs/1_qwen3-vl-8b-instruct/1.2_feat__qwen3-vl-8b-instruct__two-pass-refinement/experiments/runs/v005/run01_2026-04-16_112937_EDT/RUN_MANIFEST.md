# v005 Run 01

- version: `v005`
- parent: `v004`
- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- base commit: `28e863b`
- changed prompt surface: `detect_objects`
- evaluation pack:
  - `tests/data/tank.jpg`
  - `destroyed_tank15.jpg`
  - `operational_tank4.jpg`
  - `destroyed_building4.jpg`
  - `operational_building7.jpg`
  - `office.jpg`

## Run Method

1. Took the fixed `v004` outputs from the first mixed sweep as the reference
   condition.
2. Built `v005_effective_config.yaml` by starting from the confirmed `v004`
   effective config and replacing only the `detect_objects` prompt with the
   `v005` draft wording.
3. For each image in the mixed pack:
   - copied the source image into a case-local `images/` folder
   - copied `v005_effective_config.yaml` into the live feature-branch
     `src/bda_svc/pipeline/config.yaml`
   - ran `bda-svc` into `v005_candidate/`
   - ran `bda_eval` with the fixed `v004` reference report folder, the new
     `v005` candidate folder, and the case-local image folder
4. Restored `src/bda_svc/pipeline/config.yaml` to the clean branch-aware
   baseline snapshot and verified it matched exactly.

## Headline Result

`v005` is not a promotion candidate.

It produced one meaningful improvement:

- `destroyed_building4` recovered two separate building detections instead of
  collapsing the scene into one target
- ground-truth clarification confirms that this image contains two different
  buildings, so `v005` is correct on that case

But it also introduced one fatal regression:

- `office.jpg` changed from `object_not_found` to a full-frame `buildings`
  false positive with bbox `[0, 0, 1440, 1920]`

Because the negative-scene regression is severe, `v005` cannot be treated as a
new grounding winner even though the building-separation idea is useful.

## Decision

- reject `v005` as a new grounding winner
- keep the building-separation lesson for partial reuse only
- do not carry forward the broadened non-burning / intact-target wording as-is
