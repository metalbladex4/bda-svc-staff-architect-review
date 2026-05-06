# v022a_micro_target_sweep Diagnosis

Generated: `2026-05-05T23:00:58.914801+00:00`

## Metrics

- matches: `183`
- false negatives: `36`
- false positives: `84`
- total errors: `120`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 19 |
| `67` | 1 | 10 | 11 |
| `84` | 8 | 5 | 0 |
| `97` | 1 | 0 | 2 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Reject this axis. The left-to-right/top-to-bottom micro-target sweep created
row tiling and destroyed the dense-case balance: case `66` stayed at `8`
matches but jumped from `4` to `19` FPs, and case `67` collapsed from `9`
matches / `2` FNs / `4` FPs to `1` match / `10` FNs / `11` FPs. The next
candidate should not add a broad discovery sweep. It should preserve v020c and
target only sparse-scene extra boxes.
