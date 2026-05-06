# v017e Gate Diagnosis

Status: `potential_winner_but_not_best_so_far`

## Candidate

- candidate: `v017e_footprint_aligned_anchors`
- parent: `v017d_visual_anchor_lock`
- axis: prompt-only footprint/contact alignment
- run: `../../runs/v017e/live_2026-05-03_043533Z/`

## What Worked

- Active hinge 11 without case `101` passed:
  - `22` matches
  - `23` false negatives
  - `14` false positives
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

## Comparison To v017d

`v017e` preserved the pass but did not improve the cycle:

- same hinge matches as `v017d`: `22`
- same hinge false negatives as `v017d`: `23`
- one more hinge false positive than `v017d`: `14` versus `13`
- same changed-source metrics as `v017d`
- same updated-report smoke metrics as `v017d`

The added footprint/contact wording appears to add prompt burden without solving
case `67`; that case remained at `1` match, `10` false negatives, and `9` false
positives.

## Next Prompt Axis

`v017f` should be the final approved prompt-only attempt in this overnight cycle.
It should return to the stronger `v017d` visual-anchor idea, but make the prompt
more compact and less overloaded:

- keep full-image body-backed recall
- keep single-target visual anchor lock
- reject row/group/region boxes and geometric interpolation
- include only a light dust/motion/context placement reminder
- avoid the heavier footprint/contact wording from `v017e`

The goal is not to invent a new direction; it is to see whether a cleaner
balanced prompt can preserve or slightly improve the `v017d` potential winner.
