# Critique

## Comparison Against Fixed `v005` Reference

`v006` was designed to keep the valid neighboring-target separation lesson from
`v005` while explicitly blocking indoor / office-style building hallucinations.

This worked.

## What Improved

- `office_negative` returned to `object_not_found` with bbox `[0, 0, 0, 0]`
  instead of a full-frame `buildings` false positive.
- `destroyed_building4` kept two separate building detections, so the useful
  target-separation behavior survived the guardrail tightening.
- `tank_pressure` stayed unchanged relative to the fixed `v005` reference.

## What Stayed Stable

- `destroyed_tank15` remained a `DESTROYED` / `PROBABLE` tank detection with
  only a small bbox shape change.
- `operational_building7` remained `NO DAMAGE` / `CONFIRMED`.
- `operational_tank4` stayed `DAMAGED` / `PROBABLE`, which means the current
  operational-tank problem is not being driven by the new detect wording.

## What This Means

`v006` is the first detect-only post-sweep candidate that:

- keeps the valid two-building separation on `destroyed_building4`
- removes the fatal office false positive
- preserves the current tank pressure-case behavior

That makes it the strongest detect-only grounding candidate in this branch-
aware line so far.

## Remaining Risks

- `operational_tank4` is still misread at the assessment layer, but this run
  suggests that should be addressed in `assess_damage`, not by reopening the
  detect rule again.
- `tank.jpg` grounding has shown repeatability wobble across earlier sweeps, so
  the new detect rule should still get one confirmation repeat before we treat
  it as confirmed.

## Decision

- `keep direction`
- run one unchanged repeat
