# v007 Run 02

- version: `v007`
- parent: `v006`
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
3. Rewrote only `assess_damage` in `v007` to distinguish firing signatures
   from actual target-body damage.
4. Built a clean `v007_effective_config.yaml` from the branch-aware baseline
   snapshot plus the `v007` prompt surfaces.
5. Ran the mixed pack with case-specific references:
   - `operational_tank4` used the known-good `v000` baseline as reference
   - the other controls used the confirmed `v006` line as the stability
     reference
6. Restored the live feature-branch config to the clean branch-aware baseline
   snapshot and verified it matched exactly.

## Headline Result

`v007` fixed the operational firing false-damage case without reopening the
detect rule.

Most important change:

- `operational_tank4` moved from `DAMAGED` / `PROBABLE` to
  `NO DAMAGE` / `CONFIRMED`
- the bbox stayed exactly the same at `[66, 317, 515, 499]`
- the target-level logic now correctly treats the visible flash and smoke as
  a firing signature rather than body damage

## Per-Case Read

- `tank_pressure`
  - held `DESTROYED` / `PROBABLE`
  - bbox stayed `[51, 37, 128, 73]`
  - summary stayed aligned with the confirmed `v004` wording
- `destroyed_tank15`
  - held `DESTROYED` / `PROBABLE`
  - bbox stayed `[36, 21, 448, 177]`
  - target-level logic became more aggressive and reintroduced
    `consistent with K-kill`, which is a wording regression
- `operational_tank4`
  - recovered `NO DAMAGE` / `CONFIRMED`
  - bbox stayed `[66, 317, 515, 499]`
- `destroyed_building4`
  - kept the correct two-building result
  - both targets stayed `DESTROYED` / `PROBABLE`
- `operational_building7`
  - stayed `NO DAMAGE` / `CONFIRMED`
- `office_negative`
  - stayed `object_not_found`
  - target-level JSON still matched the confirmed `v006` behavior

## Tooling Note

`bda_eval` again hit the known `NOT APPLICABLE` limitation on the
office-vs-office comparison, so that case should be judged from the raw
`bda-svc` JSON rather than from a normal evaluation CSV.

## Decision

- `v007` is a strong partial win
- keep the new operational-firing assessment idea
- do not promote `v007` unchanged because destroyed-case logic wording still
  overreaches
- next step should stay `assess_damage`-only and tighten the anti-K-kill /
  visible-evidence wording while preserving the `operational_tank4` fix
