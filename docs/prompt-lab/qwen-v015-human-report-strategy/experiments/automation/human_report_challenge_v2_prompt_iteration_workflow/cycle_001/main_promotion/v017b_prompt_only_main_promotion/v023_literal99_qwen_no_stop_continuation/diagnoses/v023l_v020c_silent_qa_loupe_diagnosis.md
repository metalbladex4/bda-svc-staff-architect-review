# v023l_v020c_silent_qa_loupe Diagnosis

Generated: `2026-05-06T04:01:41.489474+00:00`

## Metrics

- matches: `175`
- false negatives: `44`
- false positives: `35`
- total errors: `79`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 5 |
| `67` | 1 | 10 | 11 |
| `84` | 6 | 7 | 2 |
| `97` | 1 | 0 | 1 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Reject. Even a generic final QA instruction perturbed v020c and collapsed case
`67`.

Direct image review suggests the remaining recoverable FNs are perspective-depth
targets in cases like `84` and `110`, not generic missed targets. The next
candidate should test that specific axis.
