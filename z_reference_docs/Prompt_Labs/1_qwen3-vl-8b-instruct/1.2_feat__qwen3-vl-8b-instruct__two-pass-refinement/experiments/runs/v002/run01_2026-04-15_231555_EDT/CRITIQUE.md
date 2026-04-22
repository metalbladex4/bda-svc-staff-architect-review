# v002 Critique

## Comparison Against Fresh Branch-Aware Baseline

- baseline bbox: `[51, 37, 102, 73]`
- `v002` bbox: `[46, 46, 123, 92]`
- baseline assessment: `DESTROYED`, `PROBABLE`
- `v002` assessment: `DAMAGED`, `PROBABLE`

## Comparison Against Parent (`v001`)

- `v001` bbox: `[46, 46, 123, 92]`
- `v001` assessment: `DESTROYED`, `CONFIRMED`
- `v002` preserved the same bbox while changing only downstream assessment
  behavior

## What Improved

- The larger `v001` grounding pattern held exactly.
- Confidence came back down from `CONFIRMED` to `PROBABLE`.
- Target-level subtype drift in `brief_supporting_logic` was removed.

## What Regressed

- Damage category overcorrected from `DESTROYED` to `DAMAGED`.
- Summary still contains unsupported contextual/functional overreach:
  - `vehicle on a track`
  - `complete loss of operational capability`

## Interpretation

This is a useful branch-aware result. It shows that the stronger `v001` box can
survive an assessment-only prompt change, so the bbox improvement is not tied
to the inflated `CONFIRMED` decision. But the new assessment framing is too
conservative for this image and suppresses `DESTROYED` too far.

## Decision

- partial reuse only
- next version should keep:
  - `v001` detection
  - `v002` anti-subtype and anti-overconfidence framing
- next version should specifically try to recover `DESTROYED` while preserving
  `PROBABLE`
