# Overnight v017c To v017f Decision Packet

Status: `cycle_001_prompt_only_candidate_set_complete`

## Scope

This packet covers the approved overnight continuation from `v017c` through
`v017f` after case `101` was moved to diagnostic-only status. The active forward
gate was `human_report_challenge_v2_hinge_11_no101`.

No dev, holdout, all-112, promotion, runtime config adoption, structural guard
implementation, source-truth mutation, MCP config change, hook edit, or tool
installation was part of this cycle.

## Candidate Results

| Candidate | Classification | Hinge 11 no101 | Changed-source | Updated smoke | Office negative |
| --- | --- | --- | --- | --- | --- |
| `v017c_evidence_named_finalization` | potential winner | `21` matches, `24` FNs, `15` FPs | `10` matches, `2` FNs, `0` FPs | `25` matches, `6` FNs, `1` FP | passed |
| `v017d_visual_anchor_lock` | potential winner, best balanced | `22` matches, `23` FNs, `13` FPs | `10` matches, `2` FNs, `0` FPs | `24` matches, `7` FNs, `1` FP | passed |
| `v017e_footprint_aligned_anchors` | potential winner, not best | `22` matches, `23` FNs, `14` FPs | `10` matches, `2` FNs, `0` FPs | `24` matches, `7` FNs, `1` FP | passed |
| `v017f_compact_visual_anchor_balance` | potential winner, recall variant | `23` matches, `22` FNs, `17` FPs | `9` matches, `3` FNs, `1` FP | `24` matches, `7` FNs, `2` FPs | passed |

## Recommendation

Recommend `v017d_visual_anchor_lock` as the best balanced candidate for the
next human review gate.

Why:

- It improved over `v017c` on the active hinge while lowering false positives.
- It preserved the changed-source sanity pass with `10/2/0`.
- It preserved the office-negative abstention guard.
- It avoided the extra precision cost introduced by `v017f`.

`v017f` is the recall-oriented alternative if the next decision prioritizes
hinge matches above precision margin. It is inside the approved cap, but it is
less stable across changed-source and updated-report smoke checks.

## Next Decision

Morning review should choose one of:

- approve `v017d` for the next bounded dev-split plan
- approve `v017f` only if recall is prioritized over precision margin
- hold and request visual review of row/formation cases `67` and `84` before
  any dev split

Case `101` should remain diagnostic-only unless a later source/reference audit
changes that policy.
