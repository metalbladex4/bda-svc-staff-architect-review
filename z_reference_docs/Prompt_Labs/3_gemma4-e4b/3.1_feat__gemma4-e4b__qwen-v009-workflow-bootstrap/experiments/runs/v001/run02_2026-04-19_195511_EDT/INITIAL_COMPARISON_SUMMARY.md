# Gemma `v001` Broader Follow-Up Summary

## Top Line

`v001` held up well on the broader inherited six-case pack.

Compared with the active post-`e7a22a9` Gemma `v000` anchor:

- `tank_pressure` recovered from `object_not_found / NOT APPLICABLE` to
  `DESTROYED / PROBABLE`
- `operational_tank4` recovered from `DAMAGED / PROBABLE` to
  `NO DAMAGE / CONFIRMED`
- `destroyed_tank15` held exactly
- `operational_building7` held at `NO DAMAGE / CONFIRMED`
- `office_negative` held exactly as `object_not_found / NOT APPLICABLE`
- `destroyed_building4` improved from two overlapping left-side moderate boxes
  to two separate building detections, but the left building is still
  undercalled at `MODERATE DAMAGE / CONFIRMED`

## Case Readout

### `tank_pressure`

- `v000`: `object_not_found / NOT APPLICABLE`
- `v001`: `military_equipment / DESTROYED / PROBABLE`
- kept bbox: `[68, 58, 158, 90]`
- detection debug confirms `v001` no longer abstains with
  `{"detections":[]}`

### `destroyed_tank15`

- `v000`: `DESTROYED / PROBABLE`
- `v001`: `DESTROYED / PROBABLE`
- kept bbox unchanged: `[0, 37, 458, 129]`

### `operational_tank4`

- `v000`: `DAMAGED / PROBABLE`
- `v001`: `NO DAMAGE / CONFIRMED`
- kept bbox improved upward: from `[29, 311, 545, 402]` to
  `[29, 252, 545, 401]`

### `destroyed_building4`

- `v000`: two overlapping left-side detections, both
  `MODERATE DAMAGE / CONFIRMED`
- `v001`: two separate building detections:
  - left building: `MODERATE DAMAGE / CONFIRMED`
  - right building: `DESTROYED / CONFIRMED`
- interpretation:
  - target separation is better than `v000`
  - building severity is still not trustworthy enough to call solved

### `operational_building7`

- `v000`: `NO DAMAGE / CONFIRMED`
- `v001`: `NO DAMAGE / CONFIRMED`
- geometry drift only

### `office_negative`

- `v000`: `object_not_found / NOT APPLICABLE`
- `v001`: `object_not_found / NOT APPLICABLE`
- detection debug still shows a clean empty detections list on this real
  negative scene

## Current Read

This is the strongest Gemma direction so far on the current repo base.

Why:

- the narrow detect-contract adjustment fixed both equipment regressions
- the held control cases did not break
- the known building failure surface improved meaningfully at the detection
  level

What is still not done:

- `destroyed_building4` is still undercalled on at least one building
- broader building-severity reliability is still unproven

## Decision

- treat `v001` as the new active Gemma candidate direction
- keep the active `v000` anchor preserved as the post-refresh baseline
- next Gemma work should iterate from `v001`, not from `v000`
- next validation should focus on building-severity behavior, especially
  `destroyed_building4`, before any promotion into tracked shared runtime truth
