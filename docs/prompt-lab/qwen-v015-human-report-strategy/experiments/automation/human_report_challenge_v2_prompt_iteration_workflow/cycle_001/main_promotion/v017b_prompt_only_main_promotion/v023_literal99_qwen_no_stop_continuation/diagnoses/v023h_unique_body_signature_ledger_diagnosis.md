# v023h_unique_body_signature_ledger Diagnosis

Generated: `2026-05-06T02:42:20.334404+00:00`

## Metrics

- matches: `173`
- false negatives: `46`
- false positives: `49`
- total errors: `95`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 5 |
| `67` | 1 | 10 | 11 |
| `84` | 6 | 7 | 6 |
| `97` | 1 | 0 | 2 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Reject this axis. The unique-body ledger fixed the worst case `110` explosion
compared with `v023f/g`, but it became recall-hostile overall and did not solve
case `67`.

The next candidate should keep the useful idea, but make it Qwen-grounding
native: concise, JSON-oriented, and count-locked instead of ledger-heavy.
