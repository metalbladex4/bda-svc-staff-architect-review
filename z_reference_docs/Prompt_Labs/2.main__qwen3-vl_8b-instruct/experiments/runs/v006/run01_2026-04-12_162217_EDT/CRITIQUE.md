# Critique

## Comparison Frame

- Baseline comparator:
  `experiments/runs/baseline/run01_2026-04-10_205704_EDT/`
- Relevant prior candidates:
  - `v003` run01
  - `v004` run01
  - `v005` run01
- Current run under review:
  `v006/run01_2026-04-12_162217_EDT/`

## What Improved

- `v006` is the first active-sequence candidate that visibly moves the box onto
  the burning target body instead of mainly left-side terrain/context.
- The box now captures more of the visible object/flame interface and less of
  the empty left-side area than the baseline.
- `v006` removed the `locomotive` subtype wording from supporting logic.

## What Regressed

- Confidence increased from `PROBABLE` to `CONFIRMED`.
- Supporting logic became stronger and more categorical with
  `consistent with a K-kill`.
- Summary still contains the scene-surface misread (`dirt or gravel road`) and
  a stronger operational-loss claim.

## Observed Weaknesses

- `AS-03 confidence_inflation`
  The improved crop may be helping, but a single run is not enough to justify
  promotion to `CONFIRMED`.
- `SUM-03 unsupported_impact_claim`
  The summary becomes more categorical about total operational loss.
- `DET-08 bbox_loose`
  Improved, but still not fully solved; the box still includes some terrain
  context around the target.

## Interpretation

`v006` is the first promising bbox result in the cycle. The short,
contrastive-example strategy seems to be more salient to the model than the
abstract wording used in `v005`. That said, the win is not clean enough to
promote yet because the improved crop also changed downstream assessment and
summary behavior.

So this is not a final winner. It is a best-so-far candidate that needs one of
two follow-ups:

1. a confirmation repeat to see whether the bbox improvement holds
2. if it holds, a new cycle focused on downstream confidence/summary behavior

## Research Questions

1. How should we evaluate a detection-only prompt that improves bbox grounding
   but changes downstream confidence and summary language?
2. Do prompt-fragility sources suggest requiring a confirmation repeat before
   treating `v006` as a real win?
3. If `v006` holds up on repeat, should the next problem be confidence
   calibration or summary drift?

## Decision

- Decision: `best-so-far, not yet promoted`
- Keep:
  - the shorter, contrastive-example detection style
  - the explicit doctrinal-category-only rule
- Watch:
  - confidence inflation
  - stronger downstream impact language
- Next step:
  - close the three-loop cycle with a summary, then recommend a confirmation
    repeat of `v006` as the next practical action
