# v022b_sparse_scene_proxy_filter Diagnosis

Generated: `2026-05-05T23:17:46.998607+00:00`

## Metrics

- matches: `173`
- false negatives: `46`
- false positives: `33`
- total errors: `79`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 6 |
| `67` | 2 | 9 | 10 |
| `84` | 7 | 6 | 0 |
| `97` | 1 | 0 | 2 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Reject this axis. Even the sparse-scene filter bled into dense behavior:
case `67` fell from the anchor's `9` matches / `2` FNs / `4` FPs to `2`
matches / `9` FNs / `10` FPs. The next candidate should stop adding audit or
filter clauses to v020c and instead change the decision sequence so dense
formation preservation happens before pruning.
