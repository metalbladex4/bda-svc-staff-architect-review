# v022d_compressed_context_shadow Diagnosis

Generated: `2026-05-05T23:52:01.326832+00:00`

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
| `67` | 1 | 10 | 11 |
| `84` | 8 | 5 | 0 |
| `97` | 1 | 0 | 1 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Reject compression as a replacement for v020c. It improved only one FP on
case `97`, but lost `10` matches overall and again collapsed case `67` to
`1` match / `10` FNs / `11` FPs. The next attempt should preserve v020c text
almost exactly and test only one minimal dense-formation protection sentence.
