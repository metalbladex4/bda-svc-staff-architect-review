# Cycle 03 Plan: Post-v010 Grounding Recovery

## Scope

- Cycle versions: `v010` to `v012`
- Active problem:
  grounding reliability and bounding-box placement
- Reason for reprioritizing:
  `v006` is the best bbox family so far and `v009` is the best assessment
  family so far, but the tank seed still wobbles enough that summary tuning
  would be premature if the grounding layer is not yet trustworthy

## What Stays Frozen

- `assess_damage` from `v009`
- `summarize_scene` from `v009`
- shared `system` prompt from the active line

## Why This Cycle Exists

- Official Qwen grounding examples are short, direct, and box/point-native.
- The direct `xyxy_pixels` swap in `v010` failed hard enough to show that a
  code-supported bbox convention is not automatically a model-aligned one.
- The deeper research pass after `v010` points back toward Qwen3-VL's
  normalized grounding regime rather than raw pixel coordinates.
- Community field reports also suggest that grounding quality can vary by
  backend/runtime, so we should pressure-test a more native coordinate path
  before assuming the prompt family is exhausted.

## New Cycle Considerations

- use `pipeline_debug.json` after each failed grounding run to decide whether
  the main problem is:
  - raw model bbox choice
  - schema/repair failure
  - target filtering
  - bbox validation / conversion
- if the raw bbox is valid but still off-target, treat that as a model-grounding
  choice problem, not a runtime conversion problem
- keep the prompt generic across doctrinal target classes and images; do not
  tune specifically for the tank pressure-test image
- avoid grounding methods that shrink around the hottest, brightest, or most
  central burn patch when more visible connected target body is present
- only reopen code-level grounding aids after prompt-only normalized-contract
  variants have clearly stalled
- prompt-only normalized-contract variants have now stalled enough that the
  next escalation should be the smallest code-level grounding aid rather than
  another small wording rewrite

## Planned Versions

### `v010`

- Main change:
  switch `detection_vlm.bbox_convention` from `xyxy_1000` to `xyxy_pixels`
  while keeping the short `v006` detection family and making the pixel-space
  instruction explicit
- Goal:
  test whether raw pixel coordinates relative to the image shown to the model
  improve grounding salience and bbox placement
- Outcome:
  rejected after collapsing to `object_not_found`

### `v011`

- Main change:
  return to `xyxy_1000` and keep the `v009` working baseline, but rewrite only
  `detect_objects` to be more explicitly Qwen-native: normalized `0..1000`
  coordinates, a short point-first grounding rule, and one compact
  contrastive example
- Goal:
  recover from the `v010` coordinate-contract mismatch without reopening the
  assessment surface
- Outcome:
  detection recovered and the normalized contract looks correct again, but the
  bbox converged toward the older `v001` / `v002` family instead of clearly
  improving past the frozen `v009` working baseline

### `v012` (only if needed)

- Main change:
  keep the normalized `xyxy_1000` contract and return to a stronger
  contrastive-example style, but explicitly say to box the full visible
  connected target body and not to shrink around the most salient burn patch
- Goal:
  test whether the model can keep the correct contract from `v011` while
  avoiding the point-first over-shrinking behavior that pulled it toward the
  older `v001` / `v002` family
- Outcome:
  rejected as a bbox-improving prompt; raw debug kept the baseline left/right
  span and only shifted the box downward

## Success Criteria

A version counts as a grounding win only if:

- the bbox is visibly better centered on the connected target body
- the raw bbox in `pipeline_debug.json` supports that same interpretation
- the result holds on at least one confirmation repeat
- target-level subtype drift does not worsen
- there is no schema/runtime regression

## Stop Rule

- If `v010` materially improves grounding and holds on repeat, stop the cycle
  early and reassess whether summary tuning can resume.
- `v010` did not improve grounding, `v011` only partially recovered the
  direction, and `v012` did not produce a bbox win.
- Prompt-only normalized-contract variants now look close to stalled on this
  seed case.
- The next move is now a code-level grounding aid: two-pass ROI refinement.
- That refinement path is implemented behind:
  - `detection_vlm.refinement_enabled`
  - `detection_vlm.refinement_roi_buffer_ratio`
- A first follow-on run of that aid now exists as `v013`:
  the first pass narrowed before refinement helped, the ROI-local second pass
  returned no detections, and the runtime kept the narrowed first-pass box.
- That means the code-level path is still worth iterating on, but `v013`
  should be treated as partial evidence rather than a grounding win.
