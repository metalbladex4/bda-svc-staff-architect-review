# v023j_v020c_no_history_clean Diagnosis

Generated: `2026-05-06T03:14:29.583765+00:00`

## Metrics

- matches: `174`
- false negatives: `45`
- false positives: `30`
- total errors: `75`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 5 |
| `67` | 2 | 9 | 10 |
| `84` | 6 | 7 | 1 |
| `97` | 1 | 0 | 2 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Reject this cleanup axis. Removing local history wording reduced false
positives but also damaged recall, especially dense rows and multi-target
scenes. v020c's exact phrasing appears behaviorally load bearing.

The next prompt should preserve v020c exactly and test a single recall addition:
a missed-target pass for multi-target scenes after the audit.
