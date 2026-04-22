# v001 Critique

## Comparison Against Fresh Branch-Aware Baseline

- baseline bbox: `[51, 37, 102, 73]`
- `v001` bbox: `[46, 46, 123, 92]`
- baseline assessment: `DESTROYED`, `PROBABLE`
- `v001` assessment: `DESTROYED`, `CONFIRMED`

## What Improved

- The bounding box moved off the very small left-side patch seen in the fresh
  baseline.
- The candidate box covers more of the visible burning target body and aligns
  more closely with the older legacy `v006` detection behavior.
- The branch-aware `bda_eval` review path worked end-to-end for a real
  candidate run.

## What Regressed

- Confidence inflated back to `CONFIRMED`.
- Target-level logic drifted back to an unsupported subtype:
  - `The target is a locomotive ...`
- Scene summary drifted back to unsupported identity/context detail:
  - `single locomotive`
  - `railway track`

## Interpretation

The candidate appears to help the detection stage, but that same bbox shift
reintroduces the older downstream overreach pattern. On this clean branch-aware
baseline, better grounding and conservative downstream language are still not
moving together automatically.

## Decision

- partial reuse only
- keep this as the strongest branch-aware detection candidate so far
- next version should preserve the `v001` detection idea while explicitly
  countering the downstream confidence and subtype regressions
