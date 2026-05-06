# v019c_anchor_replay Diagnosis

Generated: `2026-05-05T03:28:09.889352+00:00`

## Metrics

| Candidate | Matches | FNs | FPs | Delta vs v019c |
| --- | ---: | ---: | ---: | --- |
| `v019c_anchor_replay` | 174 | 45 | 28 | 0 / 0 / 0 |

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| 66 | 8 | 0 | 6 |
| 67 | 2 | 9 | 10 |
| 84 | 6 | 7 | 0 |
| 97 | 1 | 0 | 1 |

## Controls

- 155: {'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}
- 166: {'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}
- office-negative: {'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}

## FP/FN Pattern

- false negatives: 45
- false positives: 28

## Preserve

- kept 155, 166, and office-negative safe
- preserved or improved v019c match count
- preserved or reduced v019c false positives

## Avoid

- case 67 dense formation recall remains weak
- case 66 still carries dense/row false positives
- case 84 still misses many large-scene targets

## Next Axis

preserve balanced gains and test one sharper local axis
