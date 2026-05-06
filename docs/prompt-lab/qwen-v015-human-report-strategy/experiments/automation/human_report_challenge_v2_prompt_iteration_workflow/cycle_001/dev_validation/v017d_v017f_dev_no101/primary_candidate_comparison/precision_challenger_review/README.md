# v017b vs v017d Precision Challenger Review

This package reviews the fresh same-manifest comparison wrinkle from the
`primary_candidate_comparison` rerun: `v017b_group_box_rejection` tied
`v017d_visual_anchor_lock` on recall while reducing total false positives from
`16` to `13`.

The review is visual/evidence-focused and limited to the cases where v017b and
v017d differ:

- `66`: v017b saves two false positives.
- `67`: v017b adds one false positive.
- `84`: v017b saves one false positive.
- `103`: v017b saves one false positive.
- `155`: unchanged positive-control check.

## Scope Boundary

This is a review packet only. It does not authorize prompt authoring, holdout,
all-current/all-112 execution, promotion, runtime config adoption, source-truth
mutation, Graphify refresh, Mem0 update, MCP config change, or hook edits.
