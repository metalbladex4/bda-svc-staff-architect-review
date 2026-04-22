# CRITIQUE — `v014` run01

## Comparison Frame

- baseline comparator:
  `v009_working_baseline`
- prior code-level comparators:
  `v013` run01 and run02
- current experiment type:
  refinement-parameter tuning only

## What Improved

- The refinement ROI is now much larger, which means this run gives us a
  stronger answer about whether missing local context was the main blocker.
- The downstream target assessment still stayed at `DESTROYED` + `PROBABLE`.

## What Did Not Improve

- The candidate bbox stayed exactly in the same narrowed family as `v013`:
  `[51, 37, 102, 73]`
- The first-pass raw detection again narrowed to `[200, 300, 400, 600]`
- The second pass still returned no detections, even inside the wider ROI
  `[13, 10, 140, 100]`

## Interpretation

- Increasing the ROI buffer alone did not unlock useful second-pass grounding.
- That makes the current diagnosis stronger:
  the second pass is not failing only because the ROI was too tight.
- The repeated first-pass narrowing also means the code-level refinement path is
  currently being asked to rescue a first-pass box family that is already
  weaker than the frozen baseline.

## Comparison Against `v013`

- `v013` with `roi_buffer_ratio = 0.35`:
  no second-pass detections
- `v014` with `roi_buffer_ratio = 0.75`:
  still no second-pass detections

So the ROI size change, by itself, did not change the outcome.

## Decision

- decision state:
  reject as helpful parameter change
- keep direction / partial reuse only / reject direction:
  partial reuse only

Reason:

- The refinement framework still gives us diagnostic value.
- This specific wider-buffer change did not produce a better result.

## Research Questions

1. Does the second-pass prompt need explicit ROI-local instructions instead of
   reusing the full-scene detection prompt unchanged?
2. Should the refinement step use the original first-pass box as a floor and
   refuse narrower first-pass boxes from becoming the only path to refinement?
3. Is the better next code-level aid a visually marked / region-guided prompt
   instead of a plain second pass on the cropped ROI?
