# Critique

## Comparison Against Mixed References

`v007` was designed to fix one specific failure: the current assessment prompt
was misreading active firing signatures on `operational_tank4` as damage even
though the bbox and target identity were already correct.

That fix worked.

## What Improved

- `operational_tank4` now returns:
  - `NO DAMAGE`
  - `CONFIRMED`
  - `target actively firing; muzzle flash and smoke originate from weapon; target body intact with no visible structural damage`
- The bbox on `operational_tank4` stayed unchanged, which confirms the problem
  was in `assess_damage`, not in detection.
- `tank_pressure`, `destroyed_building4`, `operational_building7`, and the
  office negative case all stayed stable at the category/confidence level.

## What Stayed Acceptable

- `tank_pressure` kept `DESTROYED` / `PROBABLE` and the same bbox.
- `destroyed_building4` kept the correct two-target detection and both
  buildings stayed `DESTROYED` / `PROBABLE`.
- `operational_building7` stayed `NO DAMAGE` / `CONFIRMED`.
- `office_negative` stayed `object_not_found` in the raw `bda-svc` output.

## What Regressed

- `destroyed_tank15` reintroduced doctrinal overreach in
  `brief_supporting_logic`:
  - `consistent with K-kill`
- That violates the existing target-level rule that we should stay on visible
  evidence and avoid kill-mechanism wording unless it is directly supported.
- The destroyed-case wording also became more aggressive on the tank pressure
  case, even though the category and confidence did not change.

## What This Means

`v007` proves the operational-firing fix is viable.

It does **not** yet prove that the assessment prompt is ready to promote as a
new overall leader, because the destroyed-case language still needs to be
tightened back down.

So the reusable lesson is:

- keep the firing-signature guardrail
- keep the active-operation `NO DAMAGE` example
- restore a stricter visible-evidence rule for destroyed-case logic wording

## Decision

- `keep direction`
- next candidate should remain `assess_damage`-only
- explicitly ban kill-mechanism terminology in `brief_supporting_logic`
- preserve the `operational_tank4` fix while re-tightening destroyed-case
  language
