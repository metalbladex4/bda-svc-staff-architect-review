# v020a Diagnosis

Generated: `2026-05-05T03:45:16.185380+00:00`

## Metrics

| Candidate | Matches | FNs | FPs | Delta vs v019c |
| --- | ---: | ---: | ---: | --- |
| `v020a` | 177 | 42 | 67 | 3 / -3 / 39 |

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| 66 | 8 | 0 | 5 |
| 67 | 2 | 9 | 10 |
| 84 | 6 | 7 | 2 |
| 97 | 1 | 0 | 2 |

## Controls

- 155: {'reference_target_count': 2, 'predicted_target_count': 3, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 1}
- 166: {'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}
- office-negative: {'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}

## FP/FN Pattern

- false negatives: 42
- false positives: 67

## Preserve

- kept 155, 166, and office-negative safe
- preserved or improved v019c match count

## Avoid

- raised false positives versus v019c
- case 67 dense formation recall remains weak
- case 66 still carries dense/row false positives
- case 84 still misses many large-scene targets

## Next Axis

tighten FP veto while preserving full-image recall
