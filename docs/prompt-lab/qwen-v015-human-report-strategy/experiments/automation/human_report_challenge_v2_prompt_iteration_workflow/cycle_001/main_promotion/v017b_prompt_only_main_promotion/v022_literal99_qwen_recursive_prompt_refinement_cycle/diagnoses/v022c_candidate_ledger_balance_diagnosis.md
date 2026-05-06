# v022c_candidate_ledger_balance Diagnosis

Generated: `2026-05-05T23:34:59.093116+00:00`

## Metrics

- matches: `172`
- false negatives: `47`
- false positives: `41`
- total errors: `88`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 6 |
| `67` | 2 | 9 | 10 |
| `84` | 7 | 6 | 0 |
| `97` | 1 | 0 | 2 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 3, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 1}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Reject this axis. The candidate-ledger structure still harmed the same dense
formation pattern as v022b: case `67` stayed at only `2` matches with `9` FNs
and `10` FPs, while case `155` gained an extra FP. This completes the first
three-candidate plateau block. The next pivot should stop adding explicit
filter/audit/ledger structure and test a compressed v020c-style prompt.
