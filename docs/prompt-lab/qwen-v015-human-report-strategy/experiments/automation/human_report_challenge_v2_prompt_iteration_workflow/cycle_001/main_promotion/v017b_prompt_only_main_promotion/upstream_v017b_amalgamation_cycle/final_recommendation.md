# v018 Upstream/v017b Amalgamation Cycle

Generated: `2026-05-04T20:14:06.726032+00:00`

## Baselines

| Row | Matches | FNs | FPs | `155` |
| --- | ---: | ---: | ---: | --- |
| upstream prompt-controlled | 169 | 50 | 24 | fail |
| v017b local Qwen | 165 | 54 | 22 raw / 21 effective | pass |
| v017b upstream-code compat | 166 | 53 | 26 | pass |

## Candidate Results

| Rank | Candidate | Matches | FNs | FPs | `155` | `166` | Office | Verdict |
| ---: | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| 1 | `v018d_evidence_budget_pruner` | 180 | 39 | 39 | 2m/0fn/0fp | 1m/0fn/0fp | pass | near/pareto |
| 2 | `v018b_compressed_v017b` | 178 | 41 | 36 | 2m/0fn/0fp | 1m/0fn/0fp | pass | near/pareto |
| 3 | `v018c_upstream_first_precision_audit` | 175 | 44 | 43 | 2m/0fn/0fp | 1m/0fn/0fp | pass | near/pareto |
| 4 | `v018a_upstream_plus_control_guard` | 174 | 45 | 40 | 2m/0fn/1fp | 1m/0fn/0fp | pass | near/pareto |
| 5 | `v018e_contrastive_body_anchor` | 173 | 46 | 29 | 2m/0fn/0fp | 1m/0fn/0fp | pass | near/pareto |

## Dense Case Snapshot

| Candidate | 66 | 67 | 84 | 97 |
| --- | --- | --- | --- | --- |
| `v018d_evidence_budget_pruner` | 7/1/5 | 2/9/9 | 7/6/0 | 1/0/2 |
| `v018b_compressed_v017b` | 8/0/5 | 4/7/8 | 7/6/0 | 1/0/2 |
| `v018c_upstream_first_precision_audit` | 8/0/5 | 1/10/10 | 7/6/0 | 0/1/1 |
| `v018a_upstream_plus_control_guard` | 8/0/5 | 4/7/8 | 6/7/2 | 0/1/1 |
| `v018e_contrastive_body_anchor` | 8/0/5 | 2/9/10 | 8/5/0 | 1/0/1 |

## Recommendation

Verdict: `no_outright_winner_rank_best_pareto_candidate`.

Recommended candidate: `v018d_evidence_budget_pruner`.

Decision rule reminder: an outright winner must beat upstream raw recall
(`>169` matches and `<50` FNs), stay at or below the v017b raw FP ceiling
(`<=22`), and pass `155`, `166`, and office-negative.

## Operator Interpretation

Do not promote any v018 prompt from this cycle as-is. All five candidates
passed `155`, `166`, and the office-negative guard, and all five improved recall
over both upstream and v017b. However, every candidate exceeded the FP ceiling.

`v018d_evidence_budget_pruner` is the recall-ceiling candidate: it reached
`180` matches and `39` FNs, but its `39` FPs make it too loose for adoption.
`v018e_contrastive_body_anchor` is the better precision-balanced follow-up
axis: it reached `173` matches and `46` FNs with the lowest v018 FP count
(`29`), while keeping `155`, `166`, and office-negative safe.

Recommended next action: focused visual review of `v018e` false positives and
`v018d` recall wins, then author one narrower candidate that keeps v018e's
contrastive/body-anchor discipline while selectively importing v018d's
evidence-budget recall behavior.

## Boundaries

No source reports, references, doctrine, runtime config adoption, commit, push,
Graphify refresh, or Mem0 write happened in this wave.
