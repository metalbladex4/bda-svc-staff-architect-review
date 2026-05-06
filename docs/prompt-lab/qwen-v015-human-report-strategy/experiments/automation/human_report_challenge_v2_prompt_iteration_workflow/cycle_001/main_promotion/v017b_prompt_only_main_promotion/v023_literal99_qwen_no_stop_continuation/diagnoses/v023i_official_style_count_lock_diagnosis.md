# v023i_official_style_count_lock Diagnosis

Generated: `2026-05-06T02:58:48.406471+00:00`

## Metrics

- matches: `178`
- false negatives: `41`
- false positives: `40`
- total errors: `81`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 6 |
| `67` | 2 | 9 | 10 |
| `84` | 8 | 5 | 0 |
| `97` | 1 | 0 | 2 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Reject this axis as a win. It improved case `67` slightly compared with the
other v023 attempts and preserved case `84` recall, but overall it remains well
behind `v020c_anchor_replay`.

The next candidate should stop inventing new behavior and instead clean v020c's
wording: preserve the winning logic, remove local experiment-history phrasing,
and see whether the incumbent can be made cleaner without breaking it.
