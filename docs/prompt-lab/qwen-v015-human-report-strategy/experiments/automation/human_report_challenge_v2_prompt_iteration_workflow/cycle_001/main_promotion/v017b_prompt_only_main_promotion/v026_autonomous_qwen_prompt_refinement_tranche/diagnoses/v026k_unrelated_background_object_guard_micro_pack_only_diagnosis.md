# v026k_unrelated_background_object_guard micro_pack_only Diagnosis

Generated: `2026-05-07T05:31:30+00:00`

- status: `rejected`
- hard disqualifiers: `['case_155_failed', 'case_67_regression', 'nested_fragment_or_context_fp_reopened']`
- metrics: `33/16/25/41`

## Dense Cases

| Case | M/FN/FP |
| --- | ---: |
| `66` | 8/0/10 |
| `67` | 2/9/11 |
| `84` | 8/5/0 |
| `97` | 1/0/2 |

## Interpretation

Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.

## Next Hypothesis

Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
