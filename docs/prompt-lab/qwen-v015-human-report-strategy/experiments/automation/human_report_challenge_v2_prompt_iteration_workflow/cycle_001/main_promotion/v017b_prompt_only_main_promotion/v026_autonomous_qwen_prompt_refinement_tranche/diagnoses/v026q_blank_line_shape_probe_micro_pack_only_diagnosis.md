# v026q_blank_line_shape_probe micro_pack_only Diagnosis

Generated: `2026-05-07T05:55:33+00:00`

- status: `rejected`
- hard disqualifiers: `['case_67_regression', 'case_84_regression']`
- metrics: `29/20/16/36`

## Dense Cases

| Case | M/FN/FP |
| --- | ---: |
| `66` | 8/0/3 |
| `67` | 1/10/9 |
| `84` | 5/8/1 |
| `97` | 1/0/1 |

## Interpretation

Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.

## Next Hypothesis

Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
