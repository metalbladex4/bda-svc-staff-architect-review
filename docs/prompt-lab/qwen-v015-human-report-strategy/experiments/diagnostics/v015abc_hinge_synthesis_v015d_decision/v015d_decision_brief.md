# v015d Decision Brief

Status: `constraints_and_decision_only_no_prompt_text`

## Decision

Do not author or run `v015d` yet. The next design decision should be whether
`v015d` is:

1. a final prompt-only fail-closed attempt, or
2. a structural output-shape guard/validator experiment that catches row
   fragments and broad group boxes before deeper prompt tuning.

The evidence now leans toward planning the guard/validator path before spending
more dev or holdout budget, because three prompt-only variants failed the same
case `101` structural boundary.

## Evidence Basis

- `v015a`: recall improved, but false positives rebounded across `101`, `12`,
  and `28`.
- `v015b`: distinct-object wording did not prevent `101` row-fragment
  enumeration and amplified that failure.
- `v015c`: count-first uncertainty wording repaired `12` and `28`, preserved
  `155`, and still failed `101` with row fragments plus a broad group box.

## If A Final Prompt-Only v015d Is Approved Later

Constraints only, not prompt text:

- It must be fail-closed for ambiguous row-like small shapes.
- It must reject broad group, convoy, row, building-complex, or scene boxes as
  final detections.
- It must preserve the v015c gains on `12`, `28`, and `155`.
- It must not use raw human-report text or case-specific examples in the
  runtime prompt.
- It must stop at hinge smoke before dev.

## If A Structural Guard Is Approved Later

Constraints only, not implementation:

- Detect regular rows of small boxes that look like fragment enumeration.
- Detect overly broad group/scene boxes that cannot represent a distinct
  target body.
- Produce auditable diagnostics before suppressing or flagging a detection.
- Keep source truth unchanged and treat the guard as candidate-local evidence
  until separately validated.
- Do not hide the underlying model output; retain before/after records for
  review.

## Stop Rule

Do not run the 56-case dev split for v015a, v015b, or v015c. Do not run a
v015d dev split until a future hinge-smoke gate passes and case `101` receives
manual review.
