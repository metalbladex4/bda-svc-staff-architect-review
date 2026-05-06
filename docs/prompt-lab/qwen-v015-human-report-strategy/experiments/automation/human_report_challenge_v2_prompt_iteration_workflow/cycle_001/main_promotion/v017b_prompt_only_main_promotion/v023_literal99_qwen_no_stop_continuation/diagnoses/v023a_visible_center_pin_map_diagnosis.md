# v023a_visible_center_pin_map Diagnosis

Generated: `2026-05-06T00:43:59.159463+00:00`

## Metrics

- matches: `177`
- false negatives: `42`
- false positives: `33`
- total errors: `75`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 4 |
| `67` | 1 | 10 | 11 |
| `84` | 6 | 7 | 1 |
| `97` | 1 | 0 | 2 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Reject this axis. The visible-center pin map did not preserve v020c's dense
formation balance. It repeated the v022 failure mode on case `67`: anchor
v020c held `9` matches / `2` FNs / `4` FPs, but v023a fell to `1` match /
`10` FNs / `11` FPs. It also worsened case `84` from `8` matches / `5` FNs /
`0` FPs to `6` matches / `7` FNs / `1` FP. The next prompt should not add a
new decision ritual. It should preserve v020c almost verbatim and make any
extra precision check explicitly inactive in dense, row, or cluster scenes.
