# v023e_v020c_stability_rail Diagnosis

Generated: `2026-05-06T01:49:14.316318+00:00`

## Metrics

- matches: `171`
- false negatives: `48`
- false positives: `35`
- total errors: `83`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 3 |
| `67` | 1 | 10 | 11 |
| `84` | 6 | 7 | 0 |
| `97` | 1 | 0 | 2 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Reject this axis. It stayed control-safe, but it regressed badly against
`v020c_anchor_replay` (`186/33/25`) and preserved the same case `67` collapse
seen in `v023a-d`.

This suggests v020c's advantage is not easily improved by appending more
constraints. The next candidate should compress the v020c idea into fewer words
instead of adding another rail.
