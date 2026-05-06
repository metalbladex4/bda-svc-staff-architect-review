# v023g_compact_ruler_chain_veto Diagnosis

Generated: `2026-05-06T02:25:55.025086+00:00`

## Metrics

- matches: `183`
- false negatives: `36`
- false positives: `71`
- total errors: `107`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 5 |
| `67` | 1 | 10 | 11 |
| `84` | 6 | 7 | 3 |
| `97` | 1 | 0 | 2 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 4, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 2}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Reject this axis. The named geometric veto increased attention to the failure
pattern instead of suppressing it: false positives rose to `71`, case `110`
remained the top FP source, and case `155` gained extra detections.

The next candidate should stop naming forbidden patterns and instead require
positive, unique evidence for every output box.
