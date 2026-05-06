# v020h Diagnosis

Generated: `2026-05-05T05:45:31.891679+00:00`

## Metrics

| Candidate | Matches | FNs | FPs | Delta vs v019c |
| --- | ---: | ---: | ---: | --- |
| `v020h` | 186 | 33 | 25 | 12 / -12 / -3 |

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| 66 | 8 | 0 | 4 |
| 67 | 9 | 2 | 4 |
| 84 | 8 | 5 | 0 |
| 97 | 1 | 0 | 2 |

## Controls

- 155: {'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}
- 166: {'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}
- office-negative: {'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}

## FP/FN Pattern

- false negatives: 33
- false positives: 25

## Preserve

- kept 155, 166, and office-negative safe
- preserved or improved v019c match count
- preserved or reduced v019c false positives

## Avoid


## Next Axis

preserve balanced gains and test one sharper local axis
