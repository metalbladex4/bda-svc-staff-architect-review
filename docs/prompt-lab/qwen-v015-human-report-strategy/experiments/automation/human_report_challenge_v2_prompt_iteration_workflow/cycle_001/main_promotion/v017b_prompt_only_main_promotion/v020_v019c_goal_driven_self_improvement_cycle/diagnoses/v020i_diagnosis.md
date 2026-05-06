# v020i Diagnosis

Generated: `2026-05-05T06:02:10.672681+00:00`

## Metrics

| Candidate | Matches | FNs | FPs | Delta vs v019c |
| --- | ---: | ---: | ---: | --- |
| `v020i` | 172 | 47 | 30 | -2 / 2 / 2 |

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| 66 | 8 | 0 | 5 |
| 67 | 1 | 10 | 10 |
| 84 | 6 | 7 | 1 |
| 97 | 0 | 1 | 1 |

## Controls

- 155: {'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}
- 166: {'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}
- office-negative: {'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}

## FP/FN Pattern

- false negatives: 47
- false positives: 30

## Preserve

- kept 155, 166, and office-negative safe

## Avoid

- lost matches versus v019c
- raised false positives versus v019c
- case 67 dense formation recall remains weak
- case 66 still carries dense/row false positives
- case 84 still misses many large-scene targets

## Next Axis

pivot with systematic debugging and artifact review before the next candidate
