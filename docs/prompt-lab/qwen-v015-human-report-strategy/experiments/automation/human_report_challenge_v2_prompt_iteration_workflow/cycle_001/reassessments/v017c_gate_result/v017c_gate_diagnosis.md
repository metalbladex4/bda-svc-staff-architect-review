# v017c Gate Diagnosis

Status: `potential_winner_continue_cycle`

## Candidate

- candidate: `v017c_evidence_named_finalization`
- parent: `v017b_single_target_box_span_self_filter`
- axis: prompt-only evidence-named finalization
- run: `../../runs/v017c/live_2026-05-03_042040Z/`

## What Worked

- Active hinge 11 without case `101` passed:
  - `21` matches, greater than the v014 baseline gate `20`
  - `24` false negatives, less than the gate cap `25`
  - `15` false positives, within the cap `21`
  - positive control `155` passed
- Changed-source sanity passed:
  - `10` matches
  - `2` false negatives
  - `0` false positives
  - positive control `155` passed
- Updated-report smoke completed:
  - `25` matches
  - `6` false negatives
  - `1` false positive
- Separate `office-negative` abstention guard passed.

## Remaining Weakness

The pass is narrow. The hinge result still carries two visible risk clusters:

- case `67`: `1` match, `10` false negatives, `10` false positives
- case `84`: `4` matches, `9` false negatives, `1` false positive

Inspection of the generated predictions shows geometric row behavior remains a
problem. In case `67`, the model generated many small boxes in a progression
that did not match the references well. In case `84`, the model produced broad
or overlapping elongated boxes rather than reliably anchoring each box to a
separate body.

This is no longer the case `101` broad-box blocker. It is a remaining active
gate quality issue around row/formation target anchoring.

## Next Prompt Axis

`v017d` should keep the evidence-named finalization idea but add a visual-anchor
lock:

- do not create boxes by geometric interpolation, expected spacing, or row
  counting
- each final box must be anchored to a visible body center and visible body
  extent
- reject boxes that mainly follow a row, diagonal, lane, or formation geometry
- preserve secondary-target recall only when the body itself is visible

The goal is to see whether `v017d` can keep the `v017c` pass while reducing
active-gate false positives and box-placement artifacts.
