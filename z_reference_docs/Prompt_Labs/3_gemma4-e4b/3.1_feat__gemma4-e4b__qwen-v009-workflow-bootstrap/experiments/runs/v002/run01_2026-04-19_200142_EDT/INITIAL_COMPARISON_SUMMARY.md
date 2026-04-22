# Gemma `v002` Focused Building-Severity Summary

## Top Line

`v002` is an improvement over `v001` on the main remaining failure surface.

Compared with `v001`:

- `destroyed_building4` improved from:
  - left building `MODERATE DAMAGE / CONFIRMED`
  - right building `DESTROYED / CONFIRMED`
  to:
  - left building `SEVERE DAMAGE / PROBABLE`
  - right building `DESTROYED / PROBABLE`
- `tank_pressure` held at `DESTROYED / PROBABLE`
- `operational_tank4` held at `NO DAMAGE / CONFIRMED`
- `operational_building7` held at `NO DAMAGE / CONFIRMED`

## Main Case

### `destroyed_building4`

`v001`:

- `target_0`: `MODERATE DAMAGE / CONFIRMED`
- `target_1`: `DESTROYED / CONFIRMED`

`v002`:

- `target_0`: `SEVERE DAMAGE / PROBABLE`
- `target_1`: `DESTROYED / PROBABLE`

Why this is better:

- the left building is no longer undercalled as merely moderate
- the new left-building read is now closer to the clean baseline’s
  `SEVERE DAMAGE / PROBABLE`
- detection geometry did not degrade; the improvement came from assessment
  calibration, which is what this run was trying to test

### `eval_vs_qwen_v009`

- left building:
  - `v001` score `0.306`
  - `v002` score `0.330`
- right building:
  - `v001` score `0.120`
  - `v002` score `0.136`

That is not a perfect building win against the Qwen reference, but it is a
clean improvement in the right direction.

## Guard Cases

### `operational_building7`

- stayed `NO DAMAGE / CONFIRMED`
- bbox unchanged

### `tank_pressure`

- stayed `DESTROYED / PROBABLE`
- bbox unchanged from `v001`

### `operational_tank4`

- stayed `NO DAMAGE / CONFIRMED`
- bbox unchanged from `v001`

## Current Read

This is the best Gemma candidate direction so far:

- `v001` fixed the detect-contract regression and restored equipment behavior
- `v002` improved the remaining building-severity problem without reopening the
  recovered tank cases or the intact-building control

## Decision

- keep `v002` as the active next Gemma candidate
- do not promote it yet
- next step should be a broader `v002` follow-up on the full inherited pack,
  including the held controls not rerun here, before deciding whether `v002`
  should replace `v001` as the active direction
