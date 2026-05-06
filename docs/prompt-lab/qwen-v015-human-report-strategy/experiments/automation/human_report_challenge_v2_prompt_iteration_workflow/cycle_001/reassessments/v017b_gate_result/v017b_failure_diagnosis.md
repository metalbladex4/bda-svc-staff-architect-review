# v017b Failure Diagnosis

Status: `old_gate_near_miss_case101_now_diagnostic_only`

## Candidate

- candidate: `v017b_single_target_box_span_self_filter`
- parent: `v017a_body_backed_candidate_filter`
- axis: prompt-only single-target box-span self-filter
- run: `../../runs/v017b/live_2026-05-03_032920Z/`

## What Worked

- Live run completed for all approved packs.
- Hinge aggregate checks passed:
  - `24` matches, greater than the v014 gate baseline `21`
  - `33` false negatives, less than the gate cap `36`
  - `13` false positives, within the cap `21`
- Positive control `155` passed in the hinge pack with `2` matches.
- Changed-source sanity passed:
  - `9` matches
  - `3` false negatives
  - `0` false positives
  - positive control `155` passed
- Updated-report smoke completed with return code `0`:
  - `22` matches
  - `9` false negatives
  - `1` false positive
- Separate `office-negative` abstention guard passed.
- Case `101` row-fragment enumeration stayed suppressed:
  - `row_fragment_group_count = 0`

## Blocker

Case `101` still failed the required manual diagnostic:

- detections: `1`
- row-fragment groups: `0`
- broad group/scene boxes: `1`
- broad box: `[75, 58, 1000, 547]`
- broad box area ratio: `0.43137073516845703`

This is the same broad-box failure class as `v017a`, not a return to the older
row-fragment-enumeration failure. The prompt successfully discouraged many
small fragment outputs, but the model still converted a large region containing
target evidence into one accepted military-equipment detection.

## Diagnosis

The single-target box-span self-filter improved aggregate behavior but did not
make the model enforce the final-box audit on case `101`. The likely failure is
not that the model missed the concept of rejecting rows. It appears to have
treated the broad visual region as a single acceptable equipment target despite
the prompt's explicit tight-box rule.

That means another prompt-only attempt should not simply add more synonyms for
"tight" or "single body." A next prompt direction would need to change the
interface more meaningfully, such as forcing the model to abstain from case-level
regions unless it can name the visual body evidence for the proposed box. That
next direction is not authorized here.

## Decision

`v017b` remains learning evidence and should not proceed directly to dev,
holdout, all-112, promotion, or runtime adoption.

After the later user decision, case `101` is no longer a forward pass/fail
evaluation case. It is retained as diagnostic-only evidence. The `v017b`
old-gate diagnosis should inform later prompt design, but it should not stop
the approved cycle from continuing through `v017f` unless a hard stop triggers.
