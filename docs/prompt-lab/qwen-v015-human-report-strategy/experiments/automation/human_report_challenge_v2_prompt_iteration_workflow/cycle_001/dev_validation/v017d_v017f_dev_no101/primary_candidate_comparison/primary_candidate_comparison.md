# v017d Primary Candidate Comparison

## Verdict

- Recommendation: `reopen_candidate_review_precision_challenger`
- v017d anchor acceptable: `True`
- Fresh v017d delta from accepted 72/34/16: `{'match_count': 0, 'false_negative_count': 0, 'false_positive_count': 0}`
- Case 101 present in fresh runs: `False`

## Fresh Rerun Ranking

| Rank | Candidate | Matches | FNs | FPs | 155 safe | Dense 66/67/84 error units |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| 1 | `v009_control_baseline` | 74 | 32 | 27 | False | 38 |
| 2 | `v017f_compact_visual_anchor_balance` | 73 | 33 | 18 | True | 33 |
| 3 | `v017b_group_box_rejection` | 72 | 34 | 13 | True | 31 |
| 4 | `v017d_visual_anchor_lock` | 72 | 34 | 16 | True | 33 |
| 5 | `v017e_anti_span_guard` | 71 | 35 | 15 | True | 34 |
| 6 | `v017a_broad_group_box_lock` | 71 | 35 | 18 | True | 33 |
| 7 | `v017c_count_then_anchor` | 70 | 36 | 16 | True | 35 |
| 8 | `v014_weighted_building_selection` | 69 | 37 | 17 | False | 32 |
| 9 | `v016a_reference_aware_candidate_discovery` | 68 | 38 | 19 | False | 34 |
| 10 | `v015e_individual_body_evidence` | 60 | 46 | 17 | False | 39 |

## Historical Reference Rows

| Baseline | Matches | FNs | FPs | Source |
| --- | ---: | ---: | ---: | --- |
| `v009_all_current_118_v2_adjusted_dev55_no101` | 74 | 32 | 27 | `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/source_refresh/human_report_challenge_v2_refresh/adjusted_baselines/v009_all_current_118_adjusted_summary.json` |
| `v014_all_current_118_v2_adjusted_dev55_no101` | 69 | 37 | 17 | `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/source_refresh/human_report_challenge_v2_refresh/adjusted_baselines/v014_all_current_118_adjusted_summary.json` |
| `v015e_dev_v2_dev55_no101` | 59 | 47 | 18 | `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/source_refresh/human_report_challenge_v2_refresh/recalibrations/v015e_dev/eval/evaluation_2026-04-30_202320Z_summary.json` |

## Dense Formation Cases

| Candidate | 66 | 67 | 84 | Dense error units |
| --- | --- | --- | --- | ---: |
| `v017d_visual_anchor_lock` | 8/0/6 | 1/10/8 | 5/8/1 | 33 |
| `v009_control_baseline` | 7/1/4 | 1/10/12 | 5/8/3 | 38 |
| `v014_weighted_building_selection` | 7/1/5 | 1/10/8 | 5/8/0 | 32 |
| `v015e_individual_body_evidence` | 1/7/0 | 1/10/10 | 1/12/0 | 39 |
| `v016a_reference_aware_candidate_discovery` | 7/1/4 | 1/10/9 | 4/9/1 | 34 |
| `v017a_broad_group_box_lock` | 7/1/4 | 1/10/9 | 5/8/1 | 33 |
| `v017b_group_box_rejection` | 8/0/4 | 1/10/9 | 5/8/0 | 31 |
| `v017c_count_then_anchor` | 7/1/5 | 1/10/9 | 4/9/1 | 35 |
| `v017e_anti_span_guard` | 7/1/4 | 1/10/10 | 5/8/1 | 34 |
| `v017f_compact_visual_anchor_balance` | 8/0/6 | 1/10/9 | 5/8/0 | 33 |

Cell format for dense cases is `matches/FNs/FPs`.

## Decision Checks

- `missing_candidate_runs`: `[]`
- `older_candidate_review_triggers`: `[]`
- `precision_challenger_review_triggers`: `['v017b_group_box_rejection']`
- `v017f_displaces_v017d_by_rule`: `False`
- `v017d_vs_fresh_v014`: `{'beats_match_count': True, 'beats_false_negative_count': True, 'within_false_positive_count': True}`
- `recommendation`: `reopen_candidate_review_precision_challenger`

## Scope

- No prompt authoring.
- No holdout, all-current, or all-112 execution.
- No promotion or runtime config adoption.
- No source-truth mutation.
- No Graphify refresh or Mem0 update in this wave.
