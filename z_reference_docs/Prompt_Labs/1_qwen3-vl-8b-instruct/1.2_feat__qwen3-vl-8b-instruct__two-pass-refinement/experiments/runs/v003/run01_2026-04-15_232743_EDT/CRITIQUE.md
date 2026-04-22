# v003 Critique

## Comparison Against Fresh Branch-Aware Baseline

- baseline bbox: `[51, 37, 102, 73]`
- `v003` bbox: `[46, 46, 123, 92]`
- baseline assessment: `DESTROYED`, `PROBABLE`
- `v003` assessment: `DESTROYED`, `PROBABLE`

## Comparison Against `v001`

- `v001` bbox: `[46, 46, 123, 92]`
- `v001` assessment: `DESTROYED`, `CONFIRMED`
- `v003` preserved the same stronger bbox while pulling confidence down to
  `PROBABLE`

## Comparison Against `v002`

- `v002` bbox: `[46, 46, 123, 92]`
- `v002` assessment: `DAMAGED`, `PROBABLE`
- `v003` preserved the same stronger bbox while recovering `DESTROYED`

## What Improved

- Stronger bbox held.
- `DESTROYED` recovered.
- `PROBABLE` held.
- Target-level subtype drift stayed out.
- Target-level logic is now concise and generic:
  - `sustained fire; dense smoke; target body catastrophically affected but partly obscured`

## What Still Needs Work

- Summary still overreaches:
  - `military vehicle on a dirt track`
  - `complete loss of operational capability`
- So the next remaining prompt problem is mostly scene-summary calibration, not
  detection or target-level assessment.

## Decision

- current best combined branch-aware candidate
- promote as the branch-aware working leader for the next cycle
- next cycle should freeze:
  - `detect_objects` from `v001`
  - `assess_damage` from `v003`
- next cycle should tune only `summarize_scene`
