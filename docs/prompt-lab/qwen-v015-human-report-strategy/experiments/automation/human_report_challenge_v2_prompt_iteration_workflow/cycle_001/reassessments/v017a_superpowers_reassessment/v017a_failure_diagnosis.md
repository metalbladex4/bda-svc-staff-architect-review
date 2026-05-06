# v017a Failure Diagnosis

Status: `diagnosis_complete`

## Symptom

`v017a_body_backed_candidate_filter` is a near miss, not a winner. It passed
several useful checks, but the full candidate gate failed because case `101`
failed the manual diagnostic.

The case `101` diagnostic expects no row-fragment enumeration and no broad
group/scene box. `v017a` satisfied the first half but failed the second:

- row-fragment group count: `0`
- broad group/scene box count: `1`
- broad box: `[75, 13, 1000, 571]`
- broad box area ratio: `0.49223899841308594`

## Evidence

The hinge gate summary records:

- hinge totals: `23` matches, `34` false negatives, `17` false positives
- hinge aggregate checks passed for match count, false negatives, false
  positives, and positive control `155`
- case `101` diagnostic failed
- positive control `155` passed with `2` matches

The changed-source sanity pack records:

- passed: `true`
- totals: `9` matches, `3` false negatives, `0` false positives
- positive control `155` passed

The legacy office-negative abstention guard records:

- passed: `true`
- negative-scene false positives: `0`

## Pattern Analysis

Earlier `v015` and `v016` prompt attempts struggled with two related but
different failure modes:

- row-fragment enumeration: many small repeated fragments are treated as
  separate targets
- broad group/scene boxing: a large region spanning many objects or context is
  treated as one target

`v017a` improved the first failure mode on case `101`: it did not enumerate row
fragments. The remaining blocker is the second failure mode. The prompt was
strict enough to avoid fragment spam, but not strict enough to reject a
scene-scale span as a final target when many visible military-equipment bodies
exist in the area.

That makes the failure prompt-addressable, but not by simply saying "avoid row
fragments" again. The next axis must make the model separate candidate discovery
from final target-box acceptance.

## Root Cause Hypothesis

The likely prompt-interface root cause is an incomplete final acceptance
rubric. `v017a` asked for body-backed targets, but the final filter still
allowed a box to be accepted when it had some target evidence inside a much
larger region. The model treated "contains target bodies" as sufficient, when
the gate needs "one final detection tightly encloses one distinct target body."

In short:

- `v017a` learned not to output rows of fragments
- it did not reliably learn that a broad box containing many possible bodies is
  also invalid as a final detection

## Not Root Causes

This diagnosis does not treat the following as the primary root cause:

- aggregate recall failure, because the hinge aggregate checks were numerically
  inside the v2 near-miss band
- protected-negative failure, because `155` is a positive v2 control and the
  separate office-negative abstention guard passed
- source-refresh drift, because this run used `human_report_challenge_v2`
- row-fragment enumeration, because the row-fragment count for `101` was `0`
- lack of Superpowers, because the operating contract existed; the process gap
  is that near misses now need diagnosis before next authoring

## Classification Labels

- `near_miss_not_winner`
- `prompt_addressable_candidate`
- `manual_diagnostic_failure`
- `broad_group_scene_box`
- `row_fragment_suppression_preserved`
- `positive_control_preserved`
- `abstention_guard_preserved`
- `no_dev_authorized`
- `v017b_requires_approval`

## Implication

The next move should be a prompt-axis decision, not an automatic `v017b` run.
The candidate axis should keep the useful parts of `v017a` while adding a
final candidate-level acceptance test for single-target box span. No prompt
text should be authored until that axis is reviewed and approved.
