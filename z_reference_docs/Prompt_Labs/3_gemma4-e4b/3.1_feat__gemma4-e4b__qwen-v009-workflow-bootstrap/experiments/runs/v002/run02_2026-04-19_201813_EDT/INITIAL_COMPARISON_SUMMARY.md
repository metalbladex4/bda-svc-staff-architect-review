# Gemma `v002` Full-Pack Follow-Up Summary

## Top Line

`v002` held the full inherited six-case pack and is now the strongest Gemma
direction so far on the current repo base.

Compared with the broader `v001` run:

- `tank_pressure` held at `DESTROYED / PROBABLE`
- `destroyed_tank15` held at `DESTROYED / PROBABLE`
- `operational_tank4` held at `NO DAMAGE / CONFIRMED`
- `operational_building7` held at `NO DAMAGE / CONFIRMED`
- `office_negative` held exactly as `object_not_found / NOT APPLICABLE`
- `destroyed_building4` kept the improved two-target separation and improved
  building severity to:
  - `SEVERE DAMAGE / PROBABLE`
  - `DESTROYED / PROBABLE`

## What Changed Relative To `v001`

Only `assess_damage` changed. Detection behavior remained stable:

- `tank_pressure` still returns one valid `military_equipment` detection
- `operational_tank4` still returns one valid `military_equipment` detection
- `destroyed_building4` still returns two valid `buildings` detections
- `office_negative` still returns an empty detections list

So the change in `destroyed_building4` is a true assessment-calibration shift,
not a new detection artifact.

## Case Readout

### `tank_pressure`

- held from `v001`
- final output:
  - `military_equipment`
  - `DESTROYED`
  - `PROBABLE`
  - bbox `[68, 58, 158, 90]`

### `destroyed_tank15`

- held from `v001`
- final output:
  - `military_equipment`
  - `DESTROYED`
  - `PROBABLE`
  - bbox `[0, 37, 458, 129]`

### `operational_tank4`

- held from `v001`
- final output:
  - `military_equipment`
  - `NO DAMAGE`
  - `CONFIRMED`
  - bbox `[29, 252, 545, 401]`

### `destroyed_building4`

`v001`:

- `MODERATE DAMAGE / CONFIRMED`
- `DESTROYED / CONFIRMED`

`v002`:

- `SEVERE DAMAGE / PROBABLE`
- `DESTROYED / PROBABLE`

Why this is better:

- the left building now aligns more closely with the clean baseline’s
  `SEVERE DAMAGE / PROBABLE` read
- the right building still stays in the catastrophic-loss family
- the two-building separation remains intact

### `operational_building7`

- held from `v001`
- final output:
  - `buildings`
  - `NO DAMAGE`
  - `CONFIRMED`

### `office_negative`

- held from `v001`
- final output:
  - `object_not_found`
  - `NOT APPLICABLE`
  - `CONFIRMED`

## Evaluation Read

All `bda_eval` lanes exited `0`.

Notable score movement on `destroyed_building4` vs Qwen:

- left building score improved from `0.306` in `v001` to `0.330` in `v002`
- right building score improved from `0.120` in `v001` to `0.136` in `v002`

The full-pack holds elsewhere show that this gain did not come from breaking
the equipment or control cases.

## Decision

- treat `v002` as the new active Gemma candidate direction
- iterate from `v002`, not `v001`
- the line is now in a better place for broader candidate work because the
  equipment regression is fixed and the main building-severity issue is
  materially improved
