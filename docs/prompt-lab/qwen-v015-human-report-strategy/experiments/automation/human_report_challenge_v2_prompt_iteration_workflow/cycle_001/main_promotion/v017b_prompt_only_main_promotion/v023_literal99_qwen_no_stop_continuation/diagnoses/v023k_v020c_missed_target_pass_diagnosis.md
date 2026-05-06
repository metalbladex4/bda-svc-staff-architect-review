# v023k_v020c_missed_target_pass Diagnosis

Generated: `2026-05-06T03:30:25.507342+00:00`

## Metrics

- matches: `172`
- false negatives: `47`
- false positives: `35`
- total errors: `82`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 5 |
| `67` | 1 | 10 | 11 |
| `84` | 6 | 7 | 0 |
| `97` | 0 | 1 | 1 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Reject. The missed-target pass damaged the stable v020c balance and did not
recover the known FN pockets.

The fresh exact v020c replay remains `186/33/25`, so the next candidate should
make the smallest possible addition: a silent final QA check rather than any
new target-selection or recall rule.
