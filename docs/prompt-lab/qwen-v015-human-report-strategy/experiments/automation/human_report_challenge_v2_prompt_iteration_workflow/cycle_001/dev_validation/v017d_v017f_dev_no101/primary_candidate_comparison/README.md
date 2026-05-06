# v017d Primary Candidate Comparison Rerun

This package reruns the focused comparison set against the same
`human_report_challenge_v2_dev_55_no101` manifest used for the bounded v017d
and v017f dev validation. It exists to judge `v017d_visual_anchor_lock` against
fresh same-image outputs rather than only adjusted historical baselines.

## Scope

- Active manifest:
  `../validation_manifests/human_report_challenge_v2_dev_55_no101.yaml`
- Forward evaluation excludes case `101`.
- Positive control `155` remains included and must stay positive-control safe.
- Dense-formation review cases are `66`, `67`, and `84`.
- Fresh outputs are written only under `runs/<candidate_id>/`.

## Candidate Set

- `v009_control_baseline`
- `v014_weighted_building_selection`
- `v015e_individual_body_evidence`
- `v016a_reference_aware_candidate_discovery`
- `v017a_broad_group_box_lock`
- `v017b_group_box_rejection`
- `v017c_count_then_anchor`
- `v017d_visual_anchor_lock`
- `v017e_anti_span_guard`
- `v017f_compact_visual_anchor_balance`

## Boundaries

This is comparison/evaluation only. It does not authorize prompt authoring,
holdout, all-current/all-112 runs, promotion, runtime config adoption,
source-truth mutation, Graphify refresh, Mem0 updates, MCP config changes, or
hook edits.

## Outputs

- `source_manifest.json`
- `candidate_registry.json`
- `runs/<candidate_id>/...`
- `primary_candidate_comparison.json`
- `primary_candidate_comparison.md`
