# v017b Prompt Axis Recommendation

Status: `approved_and_executed_as_v017b_near_miss`

Update: the user approved this axis for one bounded worktree-local live wave.
`v017b_single_target_box_span_self_filter` was authored and run. It is a near
miss, not a winner, because case `101` still produced one broad group/scene box.
See `../v017b_gate_result/v017b_failure_diagnosis.md`.

## Recommended Axis

`v017b_single_target_box_span_self_filter`

This is a prompt-interface axis, not a structural guard. It keeps candidate
discovery, then adds a stricter final self-filter for whether a final detection
is a single target body with a tight box rather than a broad area containing
many possible targets.

## Why This Axis

`v017a` already showed that a prompt can suppress row-fragment enumeration on
case `101` while preserving useful v2 controls. The remaining blocker is that
the model accepted one large region as a military-equipment target. That means
the next prompt should not merely repeat "body-backed" or "do not enumerate
fragments." It should separate two ideas:

- candidate discovery may notice clusters, rows, and partially visible bodies
- final JSON may include only a tight box around one distinct target body

The prompt axis should make the model reject a final candidate when its box
spans multiple bodies, much empty/context area, or a scene-level group, even if
some target evidence exists inside that span.

## Constraints To Preserve

- Use `human_report_challenge_v2` only.
- Preserve the corrected positive-control meaning of `155`.
- Keep `166` holdout-only unless later approved.
- Preserve separate `office-negative` abstention safety.
- Preserve row-fragment suppression.
- Preserve recall for legitimate secondary or distant visible targets.
- Preserve required runtime placeholders if a later prompt is authored:
  `{categories}`, `{detection_guidance}`, `{bbox_format}`, and `{bbox_scale}`.

## Constraints To Add

- A final detection must be one target body, not a group, row, scene region, or
  large contextual span.
- The final box must be tight to the accepted body evidence.
- A candidate that contains multiple possible targets inside a large span
  should be rejected or split only when separate body evidence is clear.
- If the model cannot draw a tight single-body box, it should omit that
  candidate rather than output a broad proxy.

## What Not To Do

- Do not write final prompt text in this package.
- Do not create a `v017b` overlay, runner session, manifest, run directory, or
  evaluation output.
- Do not solve this by adding deterministic structural suppression in this
  prompt-authoring lane.
- Do not loosen the gate to let broad boxes pass.
- Do not run dev, holdout, all-112, or promotion checks before a later
  approved `v017b` wave.

## Suggested User Decision

This recommendation has been consumed by the approved `v017b` bounded live wave.
The next user decision is whether to pause the prompt-only lane for deeper
method critique or approve a later `v017c` direction. No `v017c` is authorized
by this recommendation.
