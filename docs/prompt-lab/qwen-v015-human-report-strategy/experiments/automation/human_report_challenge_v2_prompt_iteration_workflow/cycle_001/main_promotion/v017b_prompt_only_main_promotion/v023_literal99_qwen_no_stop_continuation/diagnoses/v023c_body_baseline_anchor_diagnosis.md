# v023c_body_baseline_anchor Diagnosis

Generated: `2026-05-06T01:16:54.637104+00:00`

## Metrics

- matches: `174`
- false negatives: `45`
- false positives: `38`
- total errors: `83`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 7 |
| `67` | 1 | 10 | 11 |
| `84` | 6 | 7 | 2 |
| `97` | 1 | 0 | 1 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Reject this axis. The placement-anchor wording did not correct the row drift.
It scored `174/45/38`, increased false positives, and kept case `67` at
`1` match / `10` FNs / `11` FPs. This completes a three-candidate
non-improving block. Pivot away from generic filters, pin maps, and placement
anchors. The next candidate should test explicit anti-drift calibration for
dusty moving rows: when plume or roadline cues pull the box upward/left, bias
the final box toward the visible solid vehicle body lower/right of those cues.
