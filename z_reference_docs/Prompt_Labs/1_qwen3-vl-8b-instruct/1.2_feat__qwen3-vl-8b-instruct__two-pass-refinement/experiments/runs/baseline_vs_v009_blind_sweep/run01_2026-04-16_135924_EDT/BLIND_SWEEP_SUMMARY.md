# Blind Sweep Summary

## Bottom Line

The 10-image blind sweep gives us a stronger team-facing position:

- `v009` preserved target-count recall on all 10 additional images
- `v009` stayed stable across all six target-state buckets we sampled
- most differences from baseline were:
  - wording cleanup
  - confidence calibration
  - modest bbox adjustments
- only 2 of 10 cases changed damage category at all

## Strongest Honest Claim

We can now say:

- the prompt changes are **not** just a tank-specific mockup
- the current stack generalizes across additional buildings, tanks, and trucks
- the biggest gains are in:
  - cross-image stability
  - preserved recall
  - cleaner doctrinal wording
  - more conservative confidence handling

## What We Should Not Overclaim

We should **not** say:

- every new image improved dramatically
- the stack is final or benchmark-complete
- all judgment changes were automatically better

## Most Important Caution Cases

- `destroyed_building5`
  - changed from `SEVERE DAMAGE` to `DESTROYED`
- `destroyed_tank37`
  - changed from `DESTROYED` to `DAMAGED`

These are the two images to show if we want to be transparent about the fact
that the stack is stronger overall but still not beyond further review.

## Deeper Review Of The Caution Cases

- `destroyed_building5`
  - both baseline and `v009` identified the same building, and the bbox change
    is only a modest widening
  - the real difference is damage calibration
  - the local building doctrine says high multistory buildings should be judged
    relative to the whole structure, not just the worst-hit section
  - the left side is catastrophically damaged, but a substantial right-side
    section remains standing
  - current judgment: baseline `SEVERE DAMAGE / PROBABLE` is more defensible
    than `v009` `DESTROYED / PROBABLE`

- `destroyed_tank37`
  - `v009` produced the cleaner bbox, with less extra smoke/background in the
    box than baseline
  - the real difference is again in damage calibration
  - the target body is engulfed in sustained fire and heavy smoke, but the
    viewing angle and obscuration make a cautious `DAMAGED / PROBABLE` call
    arguable
  - the remaining issue is that the current `v009` logic text says the target
    is "catastrophically affected," which aligns more naturally with
    `DESTROYED` than `DAMAGED`

Working interpretation:

- these caution cases are real and should stay visible in team-facing
  discussion
- neither one is a recall failure
- `destroyed_building5` is mainly a building-severity overcall in `v009`
- `destroyed_tank37` is mainly a logic/category consistency watch case in
  `v009`: the bbox is cleaner, the cautious `DAMAGED` label is arguable, but
  the supporting logic remains too catastrophic for that label

## Best Way To Present This To The Team

Frame it this way:

1. The original mixed pack already showed the new stack could fix earlier
   regressions.
2. The direct `v009` focused run proved the unified winner file faithfully
   packages the proven surfaces.
3. This 10-image blind sweep shows that the stack remains stable on additional
   unseen images across multiple target classes.

That is a much stronger case than a quick mockup, even though the sweep still
includes a couple of review-worthy judgment differences.
