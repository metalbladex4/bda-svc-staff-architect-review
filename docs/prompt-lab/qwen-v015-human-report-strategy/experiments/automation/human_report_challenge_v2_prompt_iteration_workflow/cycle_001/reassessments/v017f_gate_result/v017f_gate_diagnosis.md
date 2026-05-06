# v017f Gate Diagnosis

Status: `potential_winner_recall_variant_not_best_balanced`

## Candidate

- candidate: `v017f_compact_visual_anchor_balance`
- parent: `v017d_visual_anchor_lock`
- axis: final compact visual-anchor balance
- run: `../../runs/v017f/live_2026-05-03_044145Z/`

## What Worked

- Active hinge 11 without case `101` passed:
  - `23` matches
  - `22` false negatives
  - `17` false positives
  - positive control `155` passed
- Changed-source sanity passed:
  - `9` matches
  - `3` false negatives
  - `1` false positive
  - positive control `155` passed
- Updated-report smoke completed:
  - `24` matches
  - `7` false negatives
  - `2` false positives
- Separate `office-negative` abstention guard passed.

## Comparison To v017d

`v017f` improved hinge recall over `v017d`:

- `23` hinge matches versus `22`
- `22` hinge false negatives versus `23`

But it paid for that improvement with more false positives and weaker sanity
behavior:

- `17` hinge false positives versus `13`
- changed-source dropped from `10/2/0` to `9/3/1`
- updated-report smoke dropped from `24/7/1` to `24/7/2`

## Decision

`v017f` is a valid potential winner if the next priority is maximum hinge recall
within the approved cap. It is not the best balanced candidate from the cycle.

The balanced recommendation remains `v017d_visual_anchor_lock`.
