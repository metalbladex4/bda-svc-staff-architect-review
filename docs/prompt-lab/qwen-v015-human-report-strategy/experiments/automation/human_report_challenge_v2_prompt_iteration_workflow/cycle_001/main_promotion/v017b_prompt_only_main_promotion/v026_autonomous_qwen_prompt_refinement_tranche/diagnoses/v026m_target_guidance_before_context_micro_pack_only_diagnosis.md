# v026m_target_guidance_before_context micro_pack_only Diagnosis

Generated: `2026-05-07T05:39:56+00:00`

- status: `rejected`
- hard disqualifiers: `['case_155_failed', 'case_67_regression', 'case_84_regression']`
- metrics: `29/20/23/43`

## Dense Cases

| Case | M/FN/FP |
| --- | ---: |
| `66` | 8/0/5 |
| `67` | 1/10/11 |
| `84` | 5/8/0 |
| `97` | 1/0/2 |

## Interpretation

Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.

## Next Hypothesis

Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
