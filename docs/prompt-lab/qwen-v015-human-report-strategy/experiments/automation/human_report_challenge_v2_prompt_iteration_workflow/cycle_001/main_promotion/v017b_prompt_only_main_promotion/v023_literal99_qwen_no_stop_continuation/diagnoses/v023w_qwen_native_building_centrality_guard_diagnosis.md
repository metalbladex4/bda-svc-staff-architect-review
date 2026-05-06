# v023w_qwen_native_building_centrality_guard Diagnosis

Generated: `2026-05-06T07:14:58.266898+00:00`

## Metrics

- matches: `178`
- false negatives: `41`
- false positives: `38`
- total errors: `79`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 5 |
| `67` | 2 | 9 | 10 |
| `84` | 7 | 6 | 0 |
| `97` | 1 | 0 | 3 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Fill after comparing this candidate to the current incumbent before authoring the next prompt.
