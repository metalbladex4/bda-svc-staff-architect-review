# Critique

## Comparison Frame

- Baseline comparator:
  `experiments/runs/baseline/run01_2026-04-10_205704_EDT/`
- Relevant prior candidates:
  - `v003` run01
  - `v004` run01
- Current run under review:
  `v005/run01_2026-04-12_161314_EDT/`

## What Improved

- No observable localization improvement.
- No confidence inflation.
- The run proved that the baseline behavior is still stable under another
  baseline-plus-candidate comparison.

## What Regressed

- No new regression relative to baseline, but also no measurable gain.
- Baseline subtype drift toward `locomotive` remained fully intact.
- Summary wording remained baseline-identical, so the candidate did not reduce
  rail-context leakage or over-specific scene interpretation.

## Observed Weaknesses

- `DET-09 bbox_off_target`
  The box stayed on the same wrong target region as baseline.
- `DET-08 bbox_loose`
  The box remained too wide to support a cleaner crop.
- `AS-06 unsupported_identity_detail`
  Supporting logic still says `locomotive`.
- `SUM-05 unsupported_identity_detail`
  Summary still carries the same context-derived subtype interpretation.

## Interpretation

`v005` appears to have been too weak or too abstract to change the model's
behavior. The point-first and occlusion-aware wording may be conceptually
better, but in this form it did not become salient enough to override the
baseline grounding habit.

This failure is different from `v004`. `v004` changed behavior in the wrong
direction. `v005` did not change behavior at all. That suggests the next draft
should not add more abstract prose. It should become shorter, more direct, and
more example-driven.

## Research Questions

1. When a longer grounding prompt is ignored, do official prompting guides
   recommend shorter, more direct instructions plus examples?
2. Would one or two contrastive examples make the desired bbox behavior more
   salient than the point-first wording alone?
3. How can examples reduce subtype drift while keeping the output at the
   doctrinal `target_type` level?

## Decision

- Decision: `reject direction`
- Keep:
  - the conceptual lesson that the next prompt must make the target-body
    recovery step more salient
- Reject:
  - the current `v005` wording family as too weak to move the model
- Next step:
  - research example-based and contrastive prompt steering, then draft a shorter
    `detect_objects` prompt from `v000`
