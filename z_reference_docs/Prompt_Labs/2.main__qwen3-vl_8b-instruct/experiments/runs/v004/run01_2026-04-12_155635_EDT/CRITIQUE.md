# Critique

## Comparison Frame

- Baseline comparator:
  `experiments/runs/baseline/run01_2026-04-10_205704_EDT/`
- Relevant prior candidates:
  - `v001` run01, run02
  - `v002` run01
  - `v003` run01
- Current run under review:
  `v004/run01_2026-04-12_155635_EDT/`

## What Improved

- `v004` kept the tighter right edge introduced by `v003` instead of drifting
  back to the wide baseline box.
- Confidence stayed at `PROBABLE` instead of inflating to `CONFIRMED`.
- The run confirmed that the baseline behavior is stable and reproducible.

## What Regressed

- The bottom edge moved upward from `73` to `61`, making the box even less
  aligned with the visible target body than `v003`.
- Manual overlay review showed the box still misses the actual target body and
  now trims too aggressively around the fire-adjacent patch.
- Supporting logic drifted back into unsupported subtype language:
  `locomotive or rolling stock`.
- Summary drift also worsened by calling the target `likely a locomotive or
  heavy transport`.

## Observed Weaknesses

- `DET-09 bbox_off_target`
  The candidate still grounds on the wrong region rather than the actual target
  body.
- `DET-08 bbox_loose`
  The box is now too tight in the wrong place to support a reliable crop.
- `AS-06 unsupported_identity_detail`
  Assessment logic adds an unsupported subtype guess.
- `SUM-05 unsupported_identity_detail`
  Summary repeats and amplifies the subtype drift.

## Interpretation

`v004` proved that "nearest object body to the fire source" is too narrow a
localization instruction for this image. The model appears to snap to the
closest dark/burning patch instead of recovering the broader visible
man-made body segment. That makes the box smaller without making it more
correct.

This is a useful failure. It suggests the next draft should not simply shrink
around the fire source. It needs a better way to identify the object's visible
center or attached body extent before expanding to the box boundary.

## Research Questions

1. What do official Qwen grounding references suggest about using center-point
   or point-first localization for partially occluded objects?
2. How should we phrase occlusion-aware localization so the model recovers the
   visible attached object body instead of the nearest burning patch?
3. How can we keep doctrinal `target_type` detection while suppressing subtype
   guesses triggered by rails or rolling-stock context?

## Decision

- Decision: `partial reuse only`
- Keep:
  - fire/smoke as search cues rather than bbox boundaries
- Reject:
  - anchoring the box to the nearest fire-adjacent body fragment
- Next step:
  - research point/center grounding plus occlusion-aware phrasing, then draft a
    new detection-only candidate from `v000` that uses those findings without
    inheriting `v004` wholesale
