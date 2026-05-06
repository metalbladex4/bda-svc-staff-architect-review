# v018a Dense-Formation Body-Center Anchor

Status: `authorized_for_bounded_dense_smoke`

`v018a_dense_formation_body_center_anchor` is a prompt-only follow-up to the
case `67` diagnostic. It keeps the accepted `v017b` single-target box-span
self-filter as the parent discipline and adds one narrow behavior: in dense,
smoky, dusty, perspective-row military-equipment scenes, final boxes must be
anchored on visible body mass and body-center/ground-contact evidence rather
than dust plume, rowline, top-edge, or spacing cues.

## Parent Result

`v017b_group_box_rejection` is the parked prompt-only main promotion candidate.
It matched `v017d` recall on the fresh dev/no101 comparison while reducing
false positives. Its preserved limitation is case `67`, where all compared
prompt families matched only the largest/rightmost vehicle and missed the other
ten references.

The case `67` diagnostic found that this is not a case `101`-style broad group
box failure. It is a dense-formation perspective and smoke/dust/top-edge
anchoring failure, made harder by tiny `possible` references in the row.

## Prompt Axis

The v018a axis is:

`dense_formation_body_center_anchor_under_smoke_dust_perspective`

The prompt should:

- preserve `v017b` group/scene/row-box rejection
- keep final detections as single target bodies
- reject boxes based mainly on dust, plume, sky, rowline, top-edge, or equal
  spacing
- require each dense-row candidate to have its own visible body mass,
  lower-body/ground-contact footprint, or connected wreck outline
- avoid inventing tiny row targets from an expected count
- still recover clearly visible separate bodies, including small or distant
  ones when their body evidence is tight-boxable

## Approved Run Scope

Allowed in this wave:

- author this worktree-local candidate overlay and hypothesis
- run `human_report_challenge_v2_hinge_11_no101`
- run `legacy_abstention_guard_office_negative`
- write a bounded gate/decision summary

Not allowed in this wave:

- dev, holdout, all-current, or promotion
- runtime config adoption
- structural guard implementation
- source-truth mutation
- Graphify refresh or Mem0 write unless separately requested
- MCP config changes, hook edits, commits, or pushes
