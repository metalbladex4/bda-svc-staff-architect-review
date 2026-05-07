# v026b_audit_removal_only_lock micro_pack_only Diagnosis

Generated: `2026-05-07T04:23:00+00:00`

- status: `rejected`
- hard disqualifiers: `['case_67_regression', 'case_84_regression']`
- metrics: `28/21/17/38`

## Dense Cases

| Case | M/FN/FP |
| --- | ---: |
| `66` | 8/0/4 |
| `67` | 1/10/11 |
| `84` | 6/7/0 |
| `97` | 1/0/1 |

## Interpretation

Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.

## Next Hypothesis

Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
