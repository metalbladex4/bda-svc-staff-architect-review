# v026d_qwen_native_grounding_header micro_pack_only Diagnosis

Generated: `2026-05-07T04:46:46+00:00`

- status: `rejected`
- hard disqualifiers: `['case_67_regression']`
- metrics: `32/17/20/37`

## Dense Cases

| Case | M/FN/FP |
| --- | ---: |
| `66` | 8/0/5 |
| `67` | 1/10/11 |
| `84` | 8/5/0 |
| `97` | 1/0/2 |

## Interpretation

Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.

## Next Hypothesis

Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
