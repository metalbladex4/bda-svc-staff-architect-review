# v026i_remove_v019c_label_only micro_pack_only Diagnosis

Generated: `2026-05-07T05:22:43+00:00`

- status: `rejected`
- hard disqualifiers: `['case_67_regression', 'case_84_regression']`
- metrics: `29/20/18/38`

## Dense Cases

| Case | M/FN/FP |
| --- | ---: |
| `66` | 8/0/4 |
| `67` | 2/9/10 |
| `84` | 6/7/2 |
| `97` | 1/0/1 |

## Interpretation

Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.

## Next Hypothesis

Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
