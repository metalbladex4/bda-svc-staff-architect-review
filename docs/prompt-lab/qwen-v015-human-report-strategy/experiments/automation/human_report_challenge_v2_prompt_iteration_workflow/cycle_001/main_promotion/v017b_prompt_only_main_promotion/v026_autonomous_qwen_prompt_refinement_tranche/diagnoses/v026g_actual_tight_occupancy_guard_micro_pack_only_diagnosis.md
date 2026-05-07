# v026g_actual_tight_occupancy_guard micro_pack_only Diagnosis

Generated: `2026-05-07T05:15:00+00:00`

- status: `rejected`
- hard disqualifiers: `['case_67_regression', 'case_97_match_loss']`
- metrics: `30/19/17/36`

## Dense Cases

| Case | M/FN/FP |
| --- | ---: |
| `66` | 8/0/6 |
| `67` | 2/9/9 |
| `84` | 8/5/0 |
| `97` | 0/1/1 |

## Interpretation

Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.

## Next Hypothesis

Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
