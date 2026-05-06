# v023y_qwen_native_row_count_discipline Diagnosis

Generated: `2026-05-06T07:48:55.696223+00:00`

## Metrics

- matches: `180`
- false negatives: `39`
- false positives: `42`
- total errors: `81`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 6 |
| `67` | 1 | 10 | 11 |
| `84` | 8 | 5 | 0 |
| `97` | 1 | 0 | 1 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Fill after comparing this candidate to the current incumbent before authoring the next prompt.
