# v026j_visible_body_occupancy_phrase micro_pack_only Diagnosis

Generated: `2026-05-07T05:27:10+00:00`

- status: `rejected`
- hard disqualifiers: `['case_155_failed', 'case_67_regression']`
- metrics: `32/17/20/37`

## Dense Cases

| Case | M/FN/FP |
| --- | ---: |
| `66` | 8/0/6 |
| `67` | 2/9/10 |
| `84` | 7/6/0 |
| `97` | 1/0/1 |

## Interpretation

Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.

## Next Hypothesis

Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
