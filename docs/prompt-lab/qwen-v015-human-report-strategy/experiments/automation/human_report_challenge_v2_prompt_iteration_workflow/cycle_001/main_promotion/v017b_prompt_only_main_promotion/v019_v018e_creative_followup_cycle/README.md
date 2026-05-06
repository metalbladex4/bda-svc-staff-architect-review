# v019 v018e Creative Follow-Up Cycle

This package runs a sequential, worktree-only follow-up from
`v018e_contrastive_body_anchor`.

The cycle keeps `v018e` as the anchor to beat, but does not pre-author all final
candidate prompts. It declares six axes, then authors, runs, diagnoses, and
uses the result of each candidate before writing the next one.

Baseline evidence from the closed v018 cycle:

- `v018e`: `173` matches, `46` false negatives, `29` false positives;
  `155`, `166`, and office-negative passed.
- `v018d`: `180` matches, `39` false negatives, `39` false positives;
  useful recall ceiling but too FP-heavy.
- `v017b` remains parked; no v018 prompt is promoted as-is.

Boundaries:

- detect prompt only
- no case `101`
- no raw human-report text in prompts
- no doctrine edit
- no runtime adoption
- no source-truth mutation
- no commit, push, PR, Graphify refresh, or Mem0 write in this wave
