# v006 Run 01

- version: `v006`
- parent: `v005`
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

1. Took the fixed `v005` outputs as the reference condition.
2. Built `v006_effective_config.yaml` by starting from the saved
   `v005_effective_config.yaml` and replacing only the `detect_objects` prompt
   with the `v006` draft wording.
3. For each image in the mixed pack:
   - copied the source image into a case-local `images/` folder
   - copied `v006_effective_config.yaml` into the live feature-branch
     `src/bda_svc/pipeline/config.yaml`
   - ran `bda-svc` into `v006_candidate/`
   - ran `bda_eval` with the fixed `v005` reference report folder, the new
     `v006` candidate folder, and the case-local image folder
4. Restored `src/bda_svc/pipeline/config.yaml` to the clean branch-aware
   baseline snapshot and verified it matched exactly.

## Headline Result

`v006` is the strongest detect-only grounding candidate in the current
branch-aware line.

It preserved the useful `v005` building-separation behavior and fixed the
fatal office false positive:

- `destroyed_building4` still returned two separate buildings
- `office.jpg` returned `object_not_found` again
- `tank.jpg` held steady relative to the fixed `v005` reference

The main remaining problem in the mixed pack is not detection anymore:

- `operational_tank4` still reads as `DAMAGED`, but that stayed unchanged from
  the fixed `v005` reference and is an assessment-layer issue

## Decision

- best detect-only grounding candidate so far
- provisional new detect leader
- run one unchanged confirmation repeat before treating the detect rule as
  confirmed
