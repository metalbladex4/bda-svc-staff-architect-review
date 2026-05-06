# v020k Diagnosis

Generated: `2026-05-05T06:34:56.383458+00:00`

## Metrics

| Candidate | Matches | FNs | FPs | Delta vs v019c |
| --- | ---: | ---: | ---: | --- |
| `v020k` | 173 | 46 | 34 | -1 / 1 / 6 |

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| 66 | 8 | 0 | 4 |
| 67 | 2 | 9 | 11 |
| 84 | 6 | 7 | 2 |
| 97 | 1 | 0 | 1 |

## Controls

- 155: {'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}
- 166: {'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}
- office-negative: {'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}

## FP/FN Pattern

- false negatives: 46
- false positives: 34

## Preserve

- kept 155, 166, and office-negative safe

## Avoid

- lost matches versus v019c
- raised false positives versus v019c
- case 67 dense formation recall remains weak
- case 84 still misses many large-scene targets

## Next Axis

tighten FP veto while preserving full-image recall
