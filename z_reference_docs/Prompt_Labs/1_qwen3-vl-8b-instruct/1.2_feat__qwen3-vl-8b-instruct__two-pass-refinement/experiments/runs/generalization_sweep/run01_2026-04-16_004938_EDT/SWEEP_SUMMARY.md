# Sweep Summary

## Conclusion

The current `v004` stack behaves **well enough to stay the seed-case leader**
but **not well enough to be treated as a general grounding-rule winner**.

## Why

- It still improves the original `tank.jpg` pressure case relative to the
  fresh baseline.
- It does not increase false positives on the negative office scene.
- It behaves acceptably on another destroyed tank and on an intact building.
- But it regresses on:
  - `operational_tank4` at the assessment layer
  - `destroyed_building4` at the detection/recall layer

Ground-truth clarification:

- `destroyed_building4` contains two different buildings.
- That means the sweep result there is a true regression in `v004`, not just an
  ambiguous interpretation difference.
- `v004` missed one valid building target on that image.

## Most Important Lesson

We can no longer treat “better on the tank image” as enough.

The next bbox cycle has to be:

- detect-only
- mixed-set validated
- especially sensitive to:
  - multi-target structural scenes
  - non-burning operational vehicles
  - negative-scene false positives

## Working Recommendation

Start a new detect-only micro-cycle from the current branch-aware line and use
this sweep as the promotion gate for any future grounding-rule change.
