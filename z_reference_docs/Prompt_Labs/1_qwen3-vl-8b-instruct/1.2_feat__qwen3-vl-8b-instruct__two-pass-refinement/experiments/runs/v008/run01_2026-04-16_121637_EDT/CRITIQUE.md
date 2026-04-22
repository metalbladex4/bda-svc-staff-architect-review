# Critique

## Comparison Against Mixed References

`v008` was designed to preserve the valid `v007` firing-signature fix while
removing destroyed-case overreach in `brief_supporting_logic`.

This worked.

## What Improved

- `operational_tank4` kept the correct:
  - `NO DAMAGE`
  - `CONFIRMED`
  - `target actively firing; muzzle flash and smoke originate from weapon; target body intact with no visible structural damage`
- `destroyed_tank15` no longer says `consistent with K-kill`
- Destroyed-case logic is now back on visible evidence wording rather than
  kill-mechanism shorthand

## What Stayed Stable

- `tank_pressure` stayed `DESTROYED` / `PROBABLE` with the same bbox.
- `destroyed_building4` kept two separate building detections and both stayed
  `DESTROYED` / `PROBABLE`.
- `operational_building7` stayed `NO DAMAGE` / `CONFIRMED`.
- `office_negative` stayed `object_not_found` in the raw `bda-svc` output.

## Remaining Caution

- This is still only `run01`, so the correct next step is an unchanged repeat.
- The office negative case still requires raw-JSON review because `bda_eval`
  does not yet score `NOT APPLICABLE` cleanly.

## What This Means

`v008` is the first assessment-only follow-up that:

- fixes the operational firing false-damage case
- preserves the destroyed and negative controls
- removes the clearest target-level wording regression from `v007`

That makes it the new leading assessment candidate in this branch-aware line.

## Decision

- `keep direction`
- run one unchanged repeat
- if the repeat holds, freeze:
  - `detect_objects` at `v006`
  - `assess_damage` at `v008`
  - `summarize_scene` at `v004`
