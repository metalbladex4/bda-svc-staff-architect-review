# Failure Taxonomy

Use these tags when reviewing prompt behavior. A single run can receive multiple
tags.

## System Prompt Failures

- `SYS-01 unseen_inference`
  Model infers hidden, internal, or off-image damage.
- `SYS-02 format_drift`
  Model ignores the requested output mode or adds preamble/explanation.
- `SYS-03 chain_of_thought_leak`
  Model exposes analysis process instead of just the required answer.
- `SYS-04 doctrine_overreach`
  Model uses doctrine to justify claims that are not visually supported.

## Assessment Failures

- `AS-01 wrong_target_focus`
  Assessment describes nearby objects instead of only the selected target.
- `AS-02 doctrine_label_drift`
  Damage category is not valid for the target type.
- `AS-03 confidence_inflation`
  Confidence is too strong for the available visual evidence.
- `AS-04 logic_style_drift`
  `brief_supporting_logic` is too verbose, narrative, or mentions the prompt/crop.
- `AS-05 functional_drift`
  Assessment drifts into functionality, intent, or broader intelligence claims.
- `AS-06 unsupported_identity_detail`
  Assessment introduces a specific object subtype or identity that is not
  required by the schema and is not sufficiently supported by the visible
  evidence.

## Detection Failures

- `DET-01 undercount`
  Visible doctrinal objects are missed.
- `DET-02 overcount`
  Extra detections are added beyond the visible object count.
- `DET-03 duplicate_detection`
  Same object appears multiple times.
- `DET-04 merge_error`
  Multiple objects are merged into one detection.
- `DET-05 split_error`
  One object is split into multiple detections.
- `DET-06 label_drift`
  Detection uses a non-doctrinal or incorrect target label.
- `DET-07 bbox_invalid`
  Box is malformed, out of range, or unusable.
- `DET-08 bbox_loose`
  Box is too loose or too tight to support reliable crop generation.
- `DET-09 bbox_off_target`
  Box is well-formed and converts correctly, but it is visually placed over the
  wrong area or misses the target object.

## Summary Failures

- `SUM-01 new_target_hallucination`
  Summary introduces targets not present in prior target assessments.
- `SUM-02 assessment_conflict`
  Summary contradicts prior target-level assessments.
- `SUM-03 unsupported_impact_claim`
  Summary makes unsupported functional or combat-effect claims.
- `SUM-04 format_drift`
  Output is not concise plain text.
- `SUM-05 unsupported_identity_detail`
  Summary introduces a specific object subtype or identity not present in the
  prior doctrinal target assessment or not sufficiently supported by the image.

## Review Convention

For each failed run, record:

- case ID
- prompt version
- failure tags
- one-line symptom
- likely cause
- keep/reject decision
