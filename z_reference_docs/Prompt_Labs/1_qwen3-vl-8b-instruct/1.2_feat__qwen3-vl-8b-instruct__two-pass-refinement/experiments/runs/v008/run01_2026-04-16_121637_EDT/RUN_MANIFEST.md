# v008 Run 01

- version: `v008`
- parent: `v007`
- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- base commit: `28e863b`
- run type: `assess_damage_only_validation`
- evaluation pack:
  - `tests/data/tank.jpg`
  - `destroyed_tank15.jpg`
  - `operational_tank4.jpg`
  - `destroyed_building4.jpg`
  - `operational_building7.jpg`
  - `office.jpg`

## Run Method

1. Froze `detect_objects` at the confirmed `v006` prompt.
2. Froze `summarize_scene` at the confirmed `v004` prompt.
3. Rewrote only `assess_damage` in `v008` to keep the `v007`
   firing-signature fix while explicitly banning kill-mechanism wording in
   `brief_supporting_logic`.
4. Built a clean `v008_effective_config.yaml` from the branch-aware baseline
   snapshot plus the `v008` prompt surfaces.
5. Ran the mixed pack with case-specific references:
   - `operational_tank4` used the known-good `v000` baseline as reference
   - the other controls used the confirmed `v006` line as the stability
     reference
6. Restored the live feature-branch config to the clean branch-aware baseline
   snapshot and verified it matched exactly.

## Headline Result

`v008` kept the valid `v007` operational-firing fix and removed the clearest
destroyed-case wording regression.

Most important result:

- `operational_tank4` stayed `NO DAMAGE` / `CONFIRMED`
- bbox stayed `[66, 317, 515, 499]`
- target-level logic stayed on firing-signature evidence instead of damage

Destroyed-case cleanup:

- `destroyed_tank15` stayed `DESTROYED` / `PROBABLE`
- bbox stayed `[36, 21, 448, 177]`
- `brief_supporting_logic` no longer uses `K-kill`

## Per-Case Read

- `tank_pressure`
  - held `DESTROYED` / `PROBABLE`
  - bbox stayed `[51, 37, 128, 73]`
- `destroyed_tank15`
  - held `DESTROYED` / `PROBABLE`
  - bbox stayed `[36, 21, 448, 177]`
  - wording is now factual again:
    `target body severely deformed; major components missing or detached; catastrophic damage visible`
- `operational_tank4`
  - preserved the `NO DAMAGE` / `CONFIRMED` recovery from `v007`
- `destroyed_building4`
  - kept the correct two-building result
  - both targets stayed `DESTROYED` / `PROBABLE`
- `operational_building7`
  - stayed `NO DAMAGE` / `CONFIRMED`
- `office_negative`
  - stayed `object_not_found`
  - raw `bda-svc` JSON still matches the confirmed negative behavior

## Tooling Note

`bda_eval` again hit the known `NOT APPLICABLE` limitation on the
office-vs-office comparison, so that case should be judged from the raw
`bda-svc` JSON rather than from a normal evaluation CSV.

## Decision

- `v008` is now the strongest assess-only candidate in this branch-aware line
- keep direction
- run one unchanged confirmation repeat before treating it as confirmed
