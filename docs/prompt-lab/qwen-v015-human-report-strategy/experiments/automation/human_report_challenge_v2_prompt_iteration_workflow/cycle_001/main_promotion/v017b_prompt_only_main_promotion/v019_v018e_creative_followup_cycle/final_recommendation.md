# v019 v018e Creative Follow-Up Cycle

Generated: `2026-05-04T23:04:04.921988+00:00`

## Fresh Anchor

| Anchor | Matches | FNs | FPs | Controls |
| --- | ---: | ---: | ---: | --- |
| `v018e_anchor_replay` | 173 | 46 | 29 | pass |

## Candidate Results

| Rank | Candidate | Matches | FNs | FPs | `155` | `166` | Office | Verdict |
| ---: | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| 1 | `v019c_context_shadow_reversal` | 174 | 45 | 28 | 2m/0fn/0fp | 1m/0fn/0fp | pass | strong next-primary |
| 2 | `v019e_cartographer_grid_sweep` | 177 | 42 | 31 | 2m/0fn/0fp | 1m/0fn/0fp | pass | learning-only |
| 3 | `v019d_triage_ladder_detector` | 175 | 44 | 48 | 2m/0fn/1fp | 1m/0fn/0fp | pass | learning-only |
| 4 | `v019b_budgeted_recall_fuse` | 174 | 45 | 36 | 2m/0fn/0fp | 1m/0fn/0fp | pass | learning-only |
| 5 | `v019a_fp_sieve` | 173 | 46 | 36 | 2m/0fn/0fp | 1m/0fn/0fp | pass | learning-only |
| 6 | `v019f_adversarial_box_jury` | 171 | 48 | 36 | 2m/0fn/1fp | 1m/0fn/0fp | pass | learning-only |

## Dense Case Snapshot

| Candidate | 66 | 67 | 84 | 97 |
| --- | --- | --- | --- | --- |
| `v019c_context_shadow_reversal` | 8/0/6 | 2/9/10 | 6/7/0 | 1/0/1 |
| `v019e_cartographer_grid_sweep` | 8/0/3 | 3/8/9 | 6/7/0 | 1/0/2 |
| `v019d_triage_ladder_detector` | 8/0/5 | 2/9/14 | 6/7/1 | 1/0/2 |
| `v019b_budgeted_recall_fuse` | 8/0/4 | 5/6/13 | 5/8/2 | 0/1/1 |
| `v019a_fp_sieve` | 8/0/11 | 1/10/10 | 8/5/0 | 1/0/2 |
| `v019f_adversarial_box_jury` | 8/0/5 | 1/10/11 | 6/7/0 | 1/0/2 |

## Recommendation

Verdict: `strong_next_primary_found`.

Recommended candidate: `v019c_context_shadow_reversal`.

Conditional `v019g-i` triggered: `False`.

Decision rule reminder:

- adoption-grade: `>173` matches, `<46` FNs, `<=22` raw FPs, controls pass
- strong next-primary: beats fresh `v018e` recall and reduces FPs below fresh
  `v018e`, controls pass
- learning-only: useful evidence but not adoption-ready

## Boundaries

No source reports, references, doctrine, runtime config adoption, commit, push,
Graphify refresh, or Mem0 write happened in this wave.
