# v006 Run 02

- version: `v006`
- parent: `v005`
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

1. Reused the saved `v006_effective_config.yaml` from `run01`.
2. Ran the same six-image mixed pack again unchanged.
3. Compared each `run02` `v006_candidate` JSON against the matching `run01`
   `v006_candidate` JSON after removing only routine metadata:
   - `image_id`
   - `date_created`
   - `inference_time`
4. Restored the live feature-branch config to the clean branch-aware baseline
   snapshot and verified it matched exactly.

## Headline Result

`v006` replicated cleanly across the full mixed pack.

Per-case normalized JSON comparison result:

- `tank_pressure` -> `MATCH`
- `destroyed_tank15` -> `MATCH`
- `operational_tank4` -> `MATCH`
- `destroyed_building4` -> `MATCH`
- `operational_building7` -> `MATCH`
- `office_negative` -> `MATCH`

This confirms that the current `v006` detect rule is stable on:

- the tank pressure case
- the corrected two-building scene
- the negative office scene

## Tooling Note

As expected, `bda_eval` still hit the known `NOT APPLICABLE` limitation on the
office-vs-office comparison when both reference and candidate were
`object_not_found`.

That did not affect the underlying repeat conclusion because the raw `bda-svc`
JSONs for the office case matched exactly after routine metadata removal.

## Decision

- `v006` is now a confirmed detect-only grounding leader for the current
  branch-aware line
- the next unresolved issue in the mixed pack is the operational-tank
  assessment behavior, not the detect rule
