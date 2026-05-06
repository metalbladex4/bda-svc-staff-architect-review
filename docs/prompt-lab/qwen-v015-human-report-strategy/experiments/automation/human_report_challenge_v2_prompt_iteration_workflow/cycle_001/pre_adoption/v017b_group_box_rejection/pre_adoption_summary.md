# v017b Pre-Adoption Summary

Generated: `2026-05-03T20:40:14.107449+00:00`

## Recommendation

- decision: `approve_v017b_runtime_adoption_plan`
- confidence: `high`
- reason: v017b passed final smoke guards and all-current/no101 with positive controls 155 and 166 preserved.

## Final Smoke

| pack | images | matches | FNs | FPs | negative FP |
| --- | ---: | ---: | ---: | ---: | ---: |
| changed_source_sanity | 5 | 10 | 2 | 0 | 0 |
| updated_report_smoke | 15 | 23 | 8 | 1 | 0 |
| office_negative | 1 | 1 | 0 | 0 | 0 |

## All-Current No101

| pack | images | matches | FNs | FPs |
| --- | ---: | ---: | ---: | ---: |
| human_report_challenge_v2_all_current_117_no101 | 117 | 158 | 61 | 25 |

## Positive Controls

- `155`: 2 match(es), 0 FN, 0 FP
- `166`: 1 match(es), 0 FN, 0 FP

## Checks

- `changed_source_sanity_no_false_positives`: `true`
- `updated_report_smoke_runs_clean`: `true`
- `office_negative_abstention`: `true`
- `all_current_image_count_117`: `true`
- `case_101_excluded`: `true`
- `positive_155_safe`: `true`
- `positive_166_safe`: `true`

## Boundary

This is pre-adoption evidence only. Runtime config adoption, source-truth
edits, Graphify refresh, Mem0 writes, and actual promotion were not
performed in this wave.
