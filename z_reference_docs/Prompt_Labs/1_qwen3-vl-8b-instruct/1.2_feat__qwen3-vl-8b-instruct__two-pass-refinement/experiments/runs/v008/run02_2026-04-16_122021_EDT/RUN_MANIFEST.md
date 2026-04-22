# v008 Run 02

- version: `v008`
- parent: `v007`
- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- base commit: `28e863b`
- run type: `confirmation_repeat`
- evaluation pack:
  - `tests/data/tank.jpg`
  - `destroyed_tank15.jpg`
  - `operational_tank4.jpg`
  - `destroyed_building4.jpg`
  - `operational_building7.jpg`
  - `office.jpg`

## Run Method

1. Reused the saved `v008_effective_config.yaml` from `run01`.
2. Ran the same six-image mixed pack again unchanged.
3. Compared each `run02` `v008_candidate` JSON against the matching `run01`
   `v008_candidate` JSON after removing only routine metadata:
   - `image_id`
   - `date_created`
   - `inference_time`
4. Restored the live feature-branch config to the clean branch-aware baseline
   snapshot and verified it matched exactly.

## Headline Result

`v008` replicated cleanly across the full mixed pack.

Per-case normalized JSON comparison result:

- `tank_pressure` -> `MATCH`
- `destroyed_tank15` -> `MATCH`
- `operational_tank4` -> `MATCH`
- `destroyed_building4` -> `MATCH`
- `operational_building7` -> `MATCH`
- `office_negative` -> `MATCH`

This confirms that the current `v008` assessment rule is stable on:

- the corrected operational firing case
- the tank pressure case
- the destroyed tank and destroyed building controls
- the operational building control
- the negative office scene

## Tooling Note

As expected, `bda_eval` still hit the known `NOT APPLICABLE` limitation on the
office-vs-office comparison when both reference and candidate were
`object_not_found`.

That did not affect the repeat conclusion because the raw `bda-svc` JSONs for
the office case matched exactly after routine metadata removal.

## Decision

- `v008` is now the confirmed assess-only leader for the current branch-aware
  line
- the current best frozen stack is:
  - `detect_objects` -> `v006`
  - `assess_damage` -> `v008`
  - `summarize_scene` -> `v004`
