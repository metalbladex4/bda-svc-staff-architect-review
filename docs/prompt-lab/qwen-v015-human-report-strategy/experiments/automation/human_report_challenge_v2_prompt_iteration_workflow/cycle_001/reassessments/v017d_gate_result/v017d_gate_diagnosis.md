# v017d Gate Diagnosis

Status: `potential_winner_continue_cycle`

## Candidate

- candidate: `v017d_visual_anchor_lock`
- parent: `v017c_evidence_named_finalization`
- axis: prompt-only visual anchor lock
- run: `../../runs/v017d/live_2026-05-03_042808Z/`

## What Worked

- Active hinge 11 without case `101` passed and improved over `v017c`:
  - `22` matches
  - `23` false negatives
  - `13` false positives
  - positive control `155` passed
- Changed-source sanity passed:
  - `10` matches
  - `2` false negatives
  - `0` false positives
  - positive control `155` passed
- Updated-report smoke completed:
  - `24` matches
  - `7` false negatives
  - `1` false positive
- Separate `office-negative` abstention guard passed.

## Remaining Weakness

The strongest remaining active-gate issue is case `67`.

- case `67`: `1` match, `10` false negatives, `8` false positives
- case `84`: improved to `5` matches, `8` false negatives, `2` false positives

Manual inspection of the `67` prediction JSON against the reference boxes shows
the model found a row-like sequence, but many boxes drifted too high and left of
the reference target footprint. That makes the remaining failure more like
footprint/contact alignment than pure target-count recall.

## Next Prompt Axis

`v017e` should keep the visual-anchor lock but add a footprint/contact-point
alignment rule:

- place boxes around the visible lower body footprint, not dust/smoke above or
  ahead of the target
- in oblique rows, use visible body contact/grounding cues to set vertical
  placement
- do not shift boxes up-left toward motion/dust/context
- keep the single-body and no-row-proxy rules intact

The goal is to test whether row/formation targets can be aligned better without
reopening the precision rebound.
