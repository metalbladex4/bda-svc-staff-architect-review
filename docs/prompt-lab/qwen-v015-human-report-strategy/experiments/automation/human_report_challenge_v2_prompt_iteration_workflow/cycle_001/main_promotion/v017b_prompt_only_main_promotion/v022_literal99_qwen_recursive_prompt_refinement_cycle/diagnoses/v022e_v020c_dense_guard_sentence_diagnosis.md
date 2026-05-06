# v022e_v020c_dense_guard_sentence Diagnosis

Generated: `2026-05-06T00:09:01.489826+00:00`

## Metrics

- matches: `172`
- false negatives: `47`
- false positives: `34`
- total errors: `81`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 4 |
| `67` | 2 | 9 | 10 |
| `84` | 6 | 7 | 3 |
| `97` | 1 | 0 | 1 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Reject this axis and close the prompt-only loop. This was the smallest
perturbation attempted: preserve v020c almost exactly and add one dense-formation
guard sentence. Even that moved case `67` from the anchor's `9` matches /
`2` FNs / `4` FPs to `2` matches / `9` FNs / `10` FPs, and it worsened
case `84` from `8` matches / `5` FNs / `0` FPs to `6` matches / `7` FNs /
`3` FPs. The result supports a plateau decision: keep v020c and move the next
technical investigation to non-prompt duplicate/tiling suppression or another
detector/backend lever.
