# v023d_dust_row_antidrift_calibration Diagnosis

Generated: `2026-05-06T01:33:00.223356+00:00`

## Metrics

- matches: `175`
- false negatives: `44`
- false positives: `34`
- total errors: `78`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 6 |
| `67` | 1 | 10 | 11 |
| `84` | 5 | 8 | 1 |
| `97` | 0 | 1 | 1 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

`v023d` is not an incumbent candidate. It improved over `v023b/c` slightly but
remained far behind `v020c_anchor_replay` (`186/33/25`) and still collapsed the
critical dense row case `67` to `1/10/11`.

The failed family is now clear: `v023a-d` all added new selection, anchoring, or
calibration rituals, and all shifted dense dusty rows away from the known v020c
pattern. The next prompt should be almost v020c, with only a tiny final
coordinate-stability rail.
