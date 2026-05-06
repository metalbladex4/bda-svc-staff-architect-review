# v020e Diagnosis

Generated: `2026-05-05T04:50:38.062644+00:00`

## Metrics

| Candidate | Matches | FNs | FPs | Delta vs v019c |
| --- | ---: | ---: | ---: | --- |
| `v020e` | 168 | 51 | 40 | -6 / 6 / 12 |

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| 66 | 8 | 0 | 6 |
| 67 | 1 | 10 | 11 |
| 84 | 6 | 7 | 0 |
| 97 | 0 | 1 | 1 |

## Controls

- 155: {'reference_target_count': 2, 'predicted_target_count': 5, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 3}
- 166: {'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}
- office-negative: {'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}

## FP/FN Pattern

- false negatives: 51
- false positives: 40

## Preserve

- kept 155, 166, and office-negative safe

## Avoid

- lost matches versus v019c
- raised false positives versus v019c
- case 67 dense formation recall remains weak
- case 66 still carries dense/row false positives
- case 84 still misses many large-scene targets

## Next Axis

tighten FP veto while preserving full-image recall
