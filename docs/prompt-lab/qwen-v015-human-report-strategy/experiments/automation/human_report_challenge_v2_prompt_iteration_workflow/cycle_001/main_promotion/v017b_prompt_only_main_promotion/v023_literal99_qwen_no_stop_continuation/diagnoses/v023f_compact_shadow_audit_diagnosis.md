# v023f_compact_shadow_audit Diagnosis

Generated: `2026-05-06T02:06:40.434814+00:00`

## Metrics

- matches: `182`
- false negatives: `37`
- false positives: `66`
- total errors: `103`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 6 |
| `67` | 1 | 10 | 11 |
| `84` | 8 | 5 | 0 |
| `97` | 1 | 0 | 2 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Reject as a promotion candidate, but preserve the lesson. `v023f` recovered some
recall compared with other v023 attempts, including case `84` (`8/5/0`), but it
blew up false positives to `66`.

The dominant new failure is geometric hallucination: case `110` produced 19
predicted boxes, including a staircase of adjacent top-edge boxes, and case `67`
again produced a shifted regular row. The next candidate should keep compact
recall but add an explicit non-extrapolation/ruler-chain veto.
