# Critique

## What This Run Was For

`v009` is not a new exploratory draft. It is the unified packaging of:

- `detect_objects` from `v006`
- `assess_damage` from `v008`
- `summarize_scene` from `v004`

So the right question for this run was simple:

- does the unified version behave like the proven source surfaces it was built
  from?

## What Happened

Yes. On all three focused comparison cases, `v009` matched the `v008 run02`
reference exactly after removing only routine metadata:

- `tank_pressure`
- `operational_tank4`
- `destroyed_building4`

## What That Means By Source Version

- `v006` contribution confirmed:
  - the key representative detection boxes held
  - `tank_pressure` stayed at `[51, 37, 128, 73]`
  - `destroyed_building4` stayed at two separate building boxes:
    - `[0, 18, 69, 141]`
    - `[69, 18, 250, 158]`
- `v008` contribution confirmed:
  - `operational_tank4` stayed at `NO DAMAGE` / `CONFIRMED`
  - `tank_pressure` stayed at `DESTROYED` / `PROBABLE`
  - `destroyed_building4` stayed at two `DESTROYED` / `PROBABLE` building
    targets
- `v004` contribution confirmed:
  - the seed-case summary stayed conservative and generic
  - no drift back toward `track`, `rail`, or overclaimed functional language

## Important Limitation

This run does not prove new superiority over the source versions. It proves
that the unified packaging is faithful to them.

That is still useful because it gives us one explicit version file we can now:

- compare against future candidates
- reference in winner docs
- promote into tracked branch config work when ready

## Decision

- `keep`
- treat `v009` as the official unified winner stack
- use `v009` for future comparisons instead of reconstructing the frozen stack
  manually from `v006`, `v008`, and `v004`
