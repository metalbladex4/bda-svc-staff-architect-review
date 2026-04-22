# Baseline vs `v009`

## Bottom Line

`v009` did not explode on any of the three new challenge images, and it kept
the most important behaviors we cared about:

- multi-target building recall held
- smoke/fire handling did not regress
- complex foreground/background building separation held

## Quick Read By Image

### `destroyed_building6.jpg`

- baseline and `v009` both found 3 building targets
- `v009` made small bbox refinements without losing any target
- best interpretation:
  - additional evidence that the improved multi-target building behavior is
    generalizing beyond the earlier sweep image

### `destroyed_truck15.jpg`

- baseline and `v009` produced the same bbox and the same
  `DAMAGED / PROBABLE` assessment
- `v009` kept the newer cleaner wording discipline
- best interpretation:
  - strong non-regression check on a smoke/fire-obscured case

### `destroyed_building3.png`

- baseline and `v009` both separated:
  - one damaged foreground building
  - one intact background building
- `v009` expanded the background-building bbox to better cover the visible
  structure
- best interpretation:
  - modest but real bbox refinement on a harder cluttered scene

## Honest Claim Strength

This run supports a team-facing claim of:

- **real cross-image improvement in stability and recall discipline**

It does **not** support claiming:

- a dramatic win on every new image
- a fully benchmarked or statistically mature evaluation

## Best Way To Present This

Say that the new stack now has evidence across:

- the original mixed validation pack
- the direct `v009` focused comparison run
- this additional baseline-vs-`v009` challenge set

That is a much stronger position than a single seed image, even though the
latest three-image set mostly demonstrates **consistency and modest refinement**
rather than huge headline jumps.
