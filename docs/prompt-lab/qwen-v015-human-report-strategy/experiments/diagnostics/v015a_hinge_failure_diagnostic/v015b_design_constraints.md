# v015b Design Constraints

Status: `constraints_only_no_prompt_text`

These are implementation constraints for a future candidate, not
final runtime prompt text.

## Required Constraints

- Preserve the v015a recall-recovery idea only for clearly visible
  distinct doctrinal targets.
- Add a distinct-object filter before output: each detection must
  have visible object-body evidence, not only repeated row-like
  texture, smoke, fragments, or adjacent context.
- Reject broad scene/group boxes as final detections unless the
  task explicitly defines a grouped target. Case `101` shows why
  broad boxes can score as matches while remaining prompt-quality
  risks.
- Do not split one damaged building plus attached fire/smoke context
  into multiple building targets, as seen in case `12`.
- Do not promote tiny distant top-right shapes to equipment targets
  without clear vehicle/equipment body evidence, as seen in case
  `28`.
- Preserve protected object-not-found abstention behavior from case
  `155`.
- Treat case `101` as requiring manual review before interpreting
  any future metric change, because its reference truth has both a
  duplicated target box and a large grouped target.

## Stop Rule For Future Candidate Planning

Do not run the 56-case dev split until a future hinge candidate
keeps false positives within the hinge limit while preserving case
`155` and improving recall without row-fragment enumeration.
