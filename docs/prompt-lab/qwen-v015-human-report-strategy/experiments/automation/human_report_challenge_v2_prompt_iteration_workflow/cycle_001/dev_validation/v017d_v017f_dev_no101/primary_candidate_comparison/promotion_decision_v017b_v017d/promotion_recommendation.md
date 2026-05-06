# v017b/v017d Promotion Recommendation

Generated: `2026-05-03T20:14:09.629341+00:00`

## Recommendation

- decision: `promote_v017b_group_box_rejection`
- confidence: `high`
- runner up: `v017d_visual_anchor_lock`

## Holdout No101 Results

| candidate | matches | FNs | FPs | image_count | case 166 |
| --- | ---: | ---: | ---: | ---: | --- |
| v017b_group_box_rejection | 80 | 22 | 4 | 56 | 1 match(es) |
| v017d_visual_anchor_lock | 79 | 23 | 5 | 56 | 1 match(es) |

## Combined Dev+Holdout No101 Results

| candidate | matches | FNs | FPs | image_count |
| --- | ---: | ---: | ---: | ---: |
| v017b_group_box_rejection | 152 | 56 | 17 | 111 |
| v017d_visual_anchor_lock | 151 | 57 | 21 | 111 |
| delta v017b-v017d | 1 | -1 | -4 | 0 |

## Why

- v017b is no worse on holdout recall and is no worse on holdout precision
- v017b previously tied v017d on dev/no101 recall while reducing false positives by 3
- v017b preserves corrected positive holdout diagnostic 166

## Dev No101 Context

- v017b tied v017d on dev/no101 matches and false negatives.
- v017b reduced dev/no101 false positives by 3.
- Source: `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/dev_validation/v017d_v017f_dev_no101/primary_candidate_comparison/precision_challenger_review/v017b_vs_v017d_precision_challenger_review.json`

## Differing Holdout Cases

- `44`: delta v017b-v017d matches `1`, FNs `-1`, FPs `-1`
- `96`: delta v017b-v017d matches `1`, FNs `-1`, FPs `0`
- `152`: delta v017b-v017d matches `-1`, FNs `1`, FPs `0`

## Boundary

This artifact is a promotion recommendation only. Runtime config adoption,
source-truth edits, Graphify refresh, Mem0 writes, and actual promotion are
not performed in this wave.
