# v012 Run01 Critique

## Comparison Frame

- baseline comparator:
  `v009_working_baseline`
- relevant prior detection comparators:
  `v006`, `v011`

## What Improved

1. `v012` stayed on the corrected normalized contract and returned a valid raw
   detection payload.
2. `v012` preserved the frozen `v009` assessment behavior:
   `DESTROYED` + `PROBABLE`.
3. `v012` did not reintroduce target-level subtype drift.

## What Did Not Improve

1. `v012` is not a bbox win over the frozen baseline.
2. The raw debug payload shows the model kept the same left/right span as the
   baseline and only moved the box downward:
   - baseline raw bbox: `[200, 300, 500, 600]`
   - `v012` raw bbox: `[200, 400, 500, 700]`
3. So the new anti-over-shrinking rule did not recover the stronger `v006`
   behavior. It changed the vertical placement instead.
4. The summary still misreads the scene surface as a dirt/gravel road.

## Key Diagnostic Takeaway

`v012` confirms that the current problem is not the coordinate contract and not
the bbox conversion path.

What it shows:

- the model is still choosing the wrong raw box even when the contract is
  correct
- simply telling the model not to shrink around the most salient burn patch is
  not enough to recover the `v006` grounding behavior

## Decision

- keep the normalized `xyxy_1000` contract
- keep `v009` assessment frozen
- reject `v012` as a bbox-improving prompt
- treat prompt-only grounding as likely stalled on this seed case

## Recommended Next Step

- pause new prompt-only detection drafts
- either:
  - run a small control comparison on more images with the frozen best-known
    pair, or
  - move to a code-level grounding aid such as a two-pass refinement or a
    visually marked / region-guided approach
