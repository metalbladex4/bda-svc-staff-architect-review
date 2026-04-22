# CRITIQUE — `v013` run02

## Confirmation Goal

Determine whether `v013` run01 was mostly first-pass wobble or whether the
two-pass ROI refinement path is actually stable in this configuration.

## What Held

- The frozen `v009` working baseline repeated exactly.
- The `v013` candidate also repeated exactly.
- First-pass raw detection again narrowed to `[200, 300, 400, 600]`.
- The ROI-local second pass again returned no detections.
- The final candidate bbox again stayed `[51, 37, 102, 73]`.
- Downstream target assessment again stayed `DESTROYED` + `PROBABLE`.

## What That Means

- This is no longer just run-to-run wobble.
- With the current ROI buffer and current prompt surfaces, the code-level
  refinement path is stable but not helpful on the tank pressure-test image.
- The main repeatable behavior is:
  - first pass narrows too much
  - second pass finds nothing inside the ROI
  - runtime keeps the narrowed first-pass box

## Comparison Against Run01

- `v013` run02 matched `v013` run01 exactly on:
  - baseline bbox
  - candidate bbox
  - baseline raw detection
  - candidate raw detection
  - refinement ROI
  - no-detection second pass

So the confirmation repeat strengthens the diagnosis from run01 instead of
changing it.

## Decision

- decision state:
  confirmed non-win
- keep direction / partial reuse only / reject direction:
  partial reuse only

Reason:

- The refinement framework itself is still useful and worth keeping.
- This specific refinement parameterization is not sufficient.

## Recommended Next Research Questions

1. How much larger should the ROI be before Qwen reliably re-detects the same
   target inside the crop?
2. Is the ROI-local prompt missing context cues that the full-scene first pass
   relied on?
3. Should the next code-level step preserve the original first-pass box as a
   floor and only accept a refined box when the second pass actually improves
   visible target-body coverage?
