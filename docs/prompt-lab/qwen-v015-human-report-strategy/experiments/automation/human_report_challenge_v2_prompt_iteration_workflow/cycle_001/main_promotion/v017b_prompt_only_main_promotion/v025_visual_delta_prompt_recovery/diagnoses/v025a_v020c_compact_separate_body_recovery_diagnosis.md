# v025a_v020c_compact_separate_body_recovery Diagnosis

Generated: `2026-05-07T01:26:05+00:00`

## Decision

- status: `rejected`
- hard disqualifiers: `['case_67_below_v020c']`
- reopened FP classes: `['adjacent_off_target_object', 'nested_fragment_box']`
- case 67 preserved: `False`

## Metrics

| Candidate | Matches | FNs | FPs | Errors |
| --- | ---: | ---: | ---: | ---: |
| `v020c_anchor_replay` | 186 | 33 | 25 | 58 |
| `v024l_v023s_no_wheel_track_ablation` | 188 | 31 | 35 | 66 |
| `v025a_v020c_compact_separate_body_recovery` | 176 | 43 | 35 | 78 |

## Dense Cases

| Case | v020c | v025a |
| --- | ---: | ---: |
| `66` | 8/0/4 | 8/0/6 |
| `67` | 9/2/4 | 1/10/9 |
| `84` | 8/5/0 | 8/5/0 |
| `97` | 1/0/2 | 0/1/1 |

## Target Visual Cases

| Case | v025a M/FN/FP |
| --- | ---: |
| `14` | 1/1/0 |
| `42` | 1/1/0 |
| `172` | 3/0/0 |

## FP-Risk Cases

| Case | v025a M/FN/FP |
| --- | ---: |
| `12` | 1/0/0 |
| `16` | 1/0/2 |
| `66` | 8/0/6 |
| `77` | 1/0/0 |
| `88` | 1/0/0 |
| `90` | 1/0/0 |
| `97` | 0/1/1 |
| `103` | 1/0/1 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Interpretation

`v025a` is rejected for this wave because a hard disqualifier or reopened false-positive class appeared. Stop and return to the v020c branch base.
