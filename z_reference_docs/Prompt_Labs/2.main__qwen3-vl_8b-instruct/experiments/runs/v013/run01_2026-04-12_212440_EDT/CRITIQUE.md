# CRITIQUE — `v013` run01

## Comparison Frame

- baseline comparator:
  `v009_working_baseline`
- prior grounding comparators:
  `v006`, `v011`, `v012`
- current experiment type:
  first code-level grounding aid, not a prompt-only rewrite

## What Improved

- The candidate preserved the stronger downstream target assessment behavior:
  `DESTROYED` + `PROBABLE`
- The new debug payload is useful. We can now see the first-pass raw box, the
  refinement ROI, the ROI-local second-pass response, and the final keep/drop
  decision in one place.

## What Regressed

- The final bbox narrowed back to `[51, 37, 102, 73]`, which is closer to the
  older `v003` / archived-baseline family than to the stronger `v006` result.
- The second pass did not refine the box at all. It returned no detections
  inside the ROI.
- Because the first pass itself shifted narrower before refinement, this run
  does not yet prove that the refinement logic improves grounding.

## What The Debug Evidence Says

- Baseline raw detection:
  `[200, 300, 500, 600]`
- Candidate first-pass raw detection:
  `[200, 300, 400, 600]`
- Candidate refinement ROI:
  `[33, 24, 120, 86]`
- Candidate second-pass response inside the ROI:
  empty detections list
- Candidate refinement decision:
  `kept_original_no_refined_detection`

Interpretation:

- The runtime refinement path behaved as designed.
- The main miss is still upstream in model grounding behavior.
- In this run, refinement did not make the box better because there was no
  refined child box to select.
- The first-pass wobble means we should be careful not to over-attribute the
  regression to the refinement step itself.

## Comparison Against Prior Versions

- versus `v011`:
  `v013` ended at `[51, 37, 102, 73]` rather than `[56, 46, 123, 76]`. This is
  not a cleaner grounding win; it is just a different narrower family.
- versus `v012`:
  `v013` avoided the downward/taller shift from `[51, 49, 128, 85]`, but it
  over-tightened the right edge again.
- versus `v006`:
  `v013` did not recover the stronger visible-target-body coverage that made
  `v006` the best bbox family so far.

## Decision

- decision state:
  partial evidence only
- keep direction / partial reuse only / reject direction:
  partial reuse only

Reason:

- The code-level refinement path is worth keeping because it gives us a
  controllable next lever and richer debug evidence.
- This specific run is not a bbox win and should not be promoted.

## Research Questions

1. Is the ROI too tight or too visually degraded for Qwen to re-detect the
   same target reliably on the second pass?
2. Would a larger refinement ROI buffer recover ROI-local detections without
   drifting back into full-scene context?
3. Should refinement use a contrastive overlap or area rule different from
   simple best-overlap selection once a child detection exists?
