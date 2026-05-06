# v016 Prompt Axis Recommendation

Status: `axis_selected_no_prompt_text`

## Selected Axis

`v016_reference_aware_candidate_discovery_with_evidence_budget`

This axis keeps the next experiment inside prompt engineering, but changes the
method before changing the prompt. The next v016 prompt should be designed
around a two-stage prompt interface:

- Candidate discovery: make the model look for plausible supported targets
  across the whole scene, including secondary and distant visible targets.
- Evidence budget and self-filter: accept only final detections with
  target-specific visual evidence, and reject broad group boxes, row fragments,
  adjacent context boxes, duplicate unsupported extras, and protected-negative
  violations.

This is not final prompt text. It is the design axis for a later prompt-authoring
wave.

## Why This Axis

v015e tells us that the prompt lane is not dead, but the simple
individual-body wording path is exhausted:

- It held dev false positives at `17`, equal to v014 and under the `21` cap.
- It failed dev recall with `61` matches and `56` false negatives, worse than
  the v014 dev baseline of `70` matches and `47` false negatives.
- Dense cases such as `66` and `84` show under-detection.
- Case `67` shows that count recovery can turn into misplaced enumeration.
- Cases `69`, `86`, `97`, and `103` show local precision rebound.
- Case `101` remains a manual diagnostic because the broad-box prediction and
  reference-shape caveats make aggregate metrics insufficient.

## Authoring Constraints For Later v016

The later v016 prompt-authoring wave should:

- Preserve `{categories}`, `{detection_guidance}`, `{bbox_format}`, and
  `{bbox_scale}`.
- Avoid raw human-report text in the runtime prompt.
- Avoid case-specific examples in the runtime prompt.
- Avoid scene-central-only language that hides legitimate visible secondary
  targets.
- Avoid blanket row/fragment enumeration.
- Require clear target-specific evidence before final output.
- Reject broad group/scene boxes as final detections.
- Preserve `{"detections": []}` / object-not-found abstention behavior where no
  valid target is visible.

## Calibration Targets

Dense recall recovery: `66`, `84`, `100`, `101`, `147`

Precision rebound controls: `67`, `69`, `86`, `97`, `103`

Protected controls: `155`, `166`

Manual diagnostic: `101`

## Next Approval Gate

If approved later, author one v016 prompt/overlay from this axis and run only a
hinge smoke first. Do not run dev, holdout, all-112, promotion, runtime config
adoption, Graphify refresh, evidence rebuild, Mem0 update, or source-truth
mutation without separate approval.
