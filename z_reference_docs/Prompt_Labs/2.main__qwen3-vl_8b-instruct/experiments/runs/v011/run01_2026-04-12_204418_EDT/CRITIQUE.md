# v011 Run01 Critique

## Comparison Frame

- baseline comparator:
  `v009_working_baseline`
- relevant prior detection comparators:
  `v001`, `v002`, `v006`, `v010`

## What Improved

1. `v011` recovered detection after `v010` collapsed to `object_not_found`.
2. The new raw debug export confirms the candidate returned a valid normalized
   detection payload instead of failing at schema parsing or bbox validation.
3. `v011` kept the stronger frozen assessment behavior:
   `DESTROYED` + `PROBABLE`.
4. `v011` did not reintroduce target-level subtype drift.

## What Did Not Improve Enough

1. The recovered bbox `[56, 46, 123, 76]` is not obviously better than the
   frozen `v009` baseline `[51, 37, 128, 73]`.
2. Numerically, `v011` converged back toward the older `v001` / `v002`
   tightened-down-right family instead of reproducing the stronger `v006`
   bbox win.
3. The summary still misreads the scene surface as a dirt/gravel road instead
   of rails/tracks, so downstream scene understanding remains loose.

## Key Diagnostic Takeaway

`v011` looks like a **recovery of the coordinate contract** more than a new
grounding breakthrough.

What it proved:

- the direct `_pixels` swap in `v010` was very likely the wrong lever for
  Qwen3-VL on this path
- normalized `xyxy_1000` is still the safer active contract

What it did not prove:

- that the new point-first wording is better than the best detection work we
  already had in `v006`

## Research Questions For The Next Step

1. Can we combine the contract lesson from `v011` with the stronger
   contrastive-example salience from `v006` without falling back into the same
   older off-target bbox family?
2. Are there Qwen-specific examples or community patterns that point to a
   better way to express point-first grounding while still keeping box edges on
   the visible connected target body?
3. If normalized-contract prompt refinements still converge to the old
   `v001` / `v002` box family, is the next best move a prompt-only `v012` or a
   code-level grounding aid?

## Decision

- keep the normalized-coordinate lesson from `v011`
- keep `v009` assessment frozen
- do not treat `v011` run01 as a clean bbox win yet
- either:
  - run one confirmation repeat to see whether `v011` is at least stable, or
  - use `v011` as evidence and draft `v012` from a different normalized
    grounding style instead of the same point-first wording
