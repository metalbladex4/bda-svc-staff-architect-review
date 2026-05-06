# v017b Single-Target Box-Span Self-Filter

Status: `authorized_for_bounded_live_gate_run`

`v017b_single_target_box_span_self_filter` is the approved follow-up to the
`v017a` near miss. It is still prompt-only work inside the Qwen `1.2`
`human_report_challenge_v2` automation lane.

## Parent Result

`v017a_body_backed_candidate_filter` preserved several useful behaviors:

- changed-source sanity passed
- positive control `155` passed
- separate `office-negative` abstention passed
- case `101` row-fragment enumeration stayed suppressed

The blocker was narrower: case `101` still emitted one broad military-equipment
group/scene box, `[75, 13, 1000, 571]`, with area ratio about `0.4922`.

## Prompt Axis

The approved v017b axis is:

`v017b_single_target_box_span_self_filter`

The prompt keeps candidate discovery but adds a stricter final audit:

- final detections must be one distinct visible target body
- final boxes must be tight to that accepted body
- broad group, row, convoy, cluster, scene, or context spans must be rejected
  even when target evidence exists somewhere inside them
- uncertain candidates are omitted rather than converted into broad proxy boxes

## Approved Run Scope

Allowed in this wave:

- author this worktree-local candidate overlay and hypothesis
- run the v2 hinge pack
- run changed-source sanity
- run updated-report smoke
- run the separate `office-negative` abstention guard
- write gate and decision artifacts for user review

Not allowed in this wave:

- dev, holdout, all-112, or promotion
- runtime config adoption
- structural guard implementation
- source-truth mutation
- MCP config changes or hook edits
- tool installs

## Decision Gate

`v017b` must pass the current v2 gates before it can be treated as a potential
winner. Case `101` remains the hard manual diagnostic: no row-fragment groups
and no broad group/scene boxes.
