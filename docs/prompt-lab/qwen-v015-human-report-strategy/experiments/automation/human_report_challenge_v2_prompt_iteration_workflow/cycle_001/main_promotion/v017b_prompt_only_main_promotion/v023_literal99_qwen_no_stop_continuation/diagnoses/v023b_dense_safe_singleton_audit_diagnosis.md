# v023b_dense_safe_singleton_audit Diagnosis

Generated: `2026-05-06T01:00:05.029552+00:00`

## Metrics

- matches: `173`
- false negatives: `46`
- false positives: `32`
- total errors: `78`
- literal 99% target met: `False`

## Dense Cases

| Case | Matches | FNs | FPs |
| --- | ---: | ---: | ---: |
| `66` | 8 | 0 | 6 |
| `67` | 1 | 10 | 11 |
| `84` | 6 | 7 | 2 |
| `97` | 1 | 0 | 1 |

## Controls

- case 155: `{'reference_target_count': 2, 'predicted_target_count': 2, 'match_count': 2, 'false_negative_count': 0, 'false_positive_count': 0}`
- case 166: `{'reference_target_count': 1, 'predicted_target_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0}`
- office-negative: `{'image_count': 1, 'match_count': 1, 'false_negative_count': 0, 'false_positive_count': 0, 'negative_scene_abstention_correct_count': 1, 'negative_scene_false_positive_count': 0}`

## Next Diagnosis Slot

Reject this axis. The dense-safe singleton audit did not stay inactive in the
way that mattered. Overall metrics fell to `173/46/32`, and case `67` again
collapsed to `1` match / `10` FNs / `11` FPs. Direct inspection of case `67`
shows the newer prompts shifted the small-vehicle row upward/left relative to
the reference and v020c anchor boxes. The next candidate should stop adding
filters and instead attack placement drift: anchor boxes on the visible lower
body mass / body baseline rather than plume, dust, or top-edge cues.
