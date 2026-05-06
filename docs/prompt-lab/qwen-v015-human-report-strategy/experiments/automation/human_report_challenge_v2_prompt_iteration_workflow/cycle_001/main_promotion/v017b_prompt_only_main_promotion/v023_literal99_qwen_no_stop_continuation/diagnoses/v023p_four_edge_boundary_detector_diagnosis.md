# v023p_four_edge_boundary_detector Diagnosis

Generated: `2026-05-06T05:20:49.373131+00:00`

## Metrics

- matches: `176`
- false negatives: `43`
- false positives: `36`
- total errors: `79`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 5 |
| `67` | 2 | 9 | 9 |
| `84` | 7 | 6 | 0 |
| `97` | 1 | 0 | 2 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 3, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 1}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Fill after comparing this candidate to the current incumbent before authoring the next prompt.
