# Upstream/v017b Prompt Diagnosis

Generated: `2026-05-04T18:59:08.032984+00:00`

## Why Upstream Is Doing Well

The current upstream prompt is short and permissive. It has `740`
characters, `32` lines, and `5`
bullets. On the same all-current/no101 pack, the prompt-controlled upstream row
scored `169`
matches, `50`
FNs, and `24`
FPs, but failed corrected positive-control `155`.

The accepted v017b prompt is much more defensive. It has
`5484` characters,
`135` lines, and
`40` bullets. It improved corrected
positive-control and false-positive behavior in the local reference row, but it
lost raw recall relative to the upstream prompt-controlled row.

## Working Hypothesis

- Upstream's brevity improves ordinary visible-target enumeration.
- v017b's repeated single-body filters suppress context boxes and fix `155`, but
  can make the model under-count clean multi-object scenes.
- v018 should keep upstream's simple recall path while importing only the
  highest-yield v017b controls.

## Candidate Set

Five candidates were authored:

- `v018a_upstream_plus_control_guard`: Upstream skeleton plus minimal v017b controls for broad/group boxes, object_not_found, and positive targets. (1755 chars, 10 bullets)
- `v018b_compressed_v017b`: v017b behavior compressed into shorter wording to reduce instruction overload. (2075 chars, 15 bullets)
- `v018c_upstream_first_precision_audit`: Upstream recall-first behavior followed by a compact v017b-style single-target audit. (1676 chars, 11 bullets)
- `v018d_evidence_budget_pruner`: Creative candidate using body-support evidence budget and pruning. (2202 chars, 6 bullets)
- `v018e_contrastive_body_anchor`: Creative candidate using good-box/bad-box contrast and dense-row body anchoring. (2360 chars, 14 bullets)

## Boundaries

This diagnosis is experiment evidence only. It does not change doctrine, source
truth, runtime config, GitHub PR state, Graphify, or Mem0.
