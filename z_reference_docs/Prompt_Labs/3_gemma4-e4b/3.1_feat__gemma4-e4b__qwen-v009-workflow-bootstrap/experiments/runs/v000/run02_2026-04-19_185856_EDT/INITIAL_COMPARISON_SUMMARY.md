# Gemma `v000` Reset Comparison Summary

## Overall Read

The rebuilt Gemma baseline shows that the `e7a22a9` repo-base change did not
just perturb the tank smoke pressure image. It materially shifted the broader
Gemma behavior read.

Compared with the first live Gemma `v000`:

- `destroyed_tank15` still holds
- `operational_building7` still holds
- `office_negative` still holds
- `tank_pressure` now collapses to `object_not_found`
- `operational_tank4` now regresses to `DAMAGED`
- `destroyed_building4` remains a building-specific failure

So the older Gemma `run01` conclusions are not portable onto the current
post-`e7a22a9` repo base.

## Case Readout

### `tank_pressure`

- New Gemma `v000`:
  - `object_not_found`
  - `NOT APPLICABLE`
  - bbox `[0, 0, 0, 0]`
- Old Gemma `v000`:
  - `DESTROYED`
  - `PROBABLE`
  - bbox `[67, 57, 154, 89]`
- Qwen active reference:
  - `DESTROYED`
  - `PROBABLE`
  - bbox `[51, 37, 128, 73]`
- `origin/main` baseline:
  - `DESTROYED`
  - `PROBABLE`
  - bbox `[51, 37, 102, 73]`

Read:

- This is the clearest reset regression.
- The current Gemma line no longer recognizes the pressure-test equipment
  target at all.
- This alone is enough to say the old Gemma baseline is not a safe active
  anchor on the new repo base.

### `destroyed_tank15`

- New Gemma `v000`:
  - `DESTROYED`
  - `PROBABLE`
  - bbox `[0, 37, 458, 129]`
- Old Gemma `v000`:
  - identical

Read:

- Strong hold.
- The reset did not damage every equipment case.
- This helps isolate the newer break as selective rather than universal.

### `operational_tank4`

- New Gemma `v000`:
  - `DAMAGED`
  - `PROBABLE`
  - bbox `[29, 311, 545, 402]`
- Old Gemma `v000`:
  - `NO DAMAGE`
  - `CONFIRMED`
  - bbox `[49, 252, 461, 401]`
- Qwen active reference:
  - `NO DAMAGE`
  - `CONFIRMED`

Read:

- This is the second major reset regression.
- The current Gemma line no longer preserves the earlier operational-firing
  behavior that had been one of the stronger signs of viability.
- The new wider box and damage call suggest the current inherited contract is
  now pushing Gemma toward over-reading fire/smoke or context as actual damage.

### `destroyed_building4`

- New Gemma `v000`:
  - target 0: `MODERATE DAMAGE`, `CONFIRMED`, bbox `[0, 54, 95, 176]`
  - target 1: `MODERATE DAMAGE`, `CONFIRMED`, bbox `[0, 53, 94, 176]`
- Old Gemma `v000`:
  - target 0: `MODERATE DAMAGE`, `CONFIRMED`, bbox `[0, 52, 96, 176]`
  - target 1: `NO DAMAGE`, `CONFIRMED`, bbox `[0, 53, 67, 176]`
- Qwen active reference:
  - two targets, both `DESTROYED / PROBABLE`
- `origin/main` baseline:
  - one `SEVERE DAMAGE / PROBABLE`
  - one `DESTROYED / CONFIRMED`

Read:

- This case is still not acceptable.
- There is a narrow local improvement over the old Gemma run because both
  targets now at least register damage, but the severity is still undercalled
  badly and the boxes still overlap the same left-side structure.
- The building problem remains unresolved and is no longer the only issue.

### `operational_building7`

- New Gemma `v000`:
  - `NO DAMAGE`
  - `CONFIRMED`
  - bbox `[14, 203, 1346, 432]`
- Old Gemma `v000`:
  - `NO DAMAGE`
  - `CONFIRMED`
  - bbox `[14, 121, 1346, 421]`

Read:

- Strong category/confidence hold.
- Geometry drift exists, but the doctrinal assessment stayed stable.

### `office_negative`

- New Gemma `v000`:
  - `object_not_found`
  - `NOT APPLICABLE`
  - `CONFIRMED`
- Old Gemma `v000`:
  - identical
- Qwen active reference:
  - identical

Read:

- Negative-scene behavior still holds correctly at the raw JSON level.
- `bda_eval` still does not emit a normal CSV for `NOT_APPLICABLE`, even
  though the eval run now exits `0` and still writes the review artifacts.
- This remains a secondary evaluation-loop limitation, not the primary reason
  the reset result is blocked.

## Answer To The Reset Question

The `e7a22a9` change did **not** only affect Gemma on the tank smoke seed.

It materially shifted the broader line enough that:

- the old Gemma `run01` conclusions are no longer portable
- the rebuilt `run02` baseline must become the active anchor
- immediate Gemma `v001` prompt iteration should pause

## Decision

- keep `run02_2026-04-19_185856_EDT` as the active Gemma `v000` anchor
- preserve `run01_2026-04-17_134308_EDT` as pre-refresh historical evidence
- do not start `v001` yet
- first reconsider the inherited detect-contract effect before deciding whether
  the next Gemma move is prompt iteration or a deeper runtime-contract change
