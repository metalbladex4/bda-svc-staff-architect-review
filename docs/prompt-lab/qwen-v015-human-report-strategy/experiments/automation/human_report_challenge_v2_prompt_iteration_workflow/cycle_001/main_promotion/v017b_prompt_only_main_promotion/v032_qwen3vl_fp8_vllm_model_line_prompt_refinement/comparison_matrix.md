# v032 Comparison Matrix

Generated: `2026-05-09T00:09:09Z`

| Candidate | Stage | Matches | FNs | FPs | Errors | Case 67 | Case 155 | Case 166 | Office | Status |
|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| `v020c_old_product_reference` | prior_all_current | 186 | 33 | 25 | 58 | prior stable evidence | prior stable evidence | prior stable evidence | prior stable evidence | product_incumbent_reference |
| `v020c_fp8_vllm_baseline` | v031_all_current | 180 | 39 | 32 | 71 | stable; v032 sentinel 10/1/2 | v032 sentinel 2/0/2 | v032 sentinel 1/0/0 | pass | fp8_working_baseline |
| `v032_baseline_exact_v020c_fp8_replay` | micro_pack_only | 42 | 7 | 15 | 22 | 10/1/2 | n/a | n/a | n/a | baseline_replay |
| `v032a_fp8_context_fragment_precision_guard` | micro_pack_only | 42 | 7 | 15 | 22 | 10/1/2 | n/a | n/a | pass | rejected_noop |
| `v032b_fp8_real_context_fragment_precision_guard` | micro_pack_only | 39 | 10 | 16 | 26 | 10/1/2 | n/a | n/a | pass | rejected |
| `v032c_fp8_compact_calibration` | micro_pack_only | 40 | 9 | 17 | 26 | 10/1/2 | n/a | n/a | pass | rejected |
| `v032d_fp8_v019c_anchor_replay` | micro_pack_only_full_incomplete | 39 | 10 | 12 | 22 | 8/3/2 | n/a | n/a | pass | learning_evidence_incomplete_full |

Notes:
- Micro-pack totals are not comparable to all-current totals; they are gate evidence only.
- `v032d` full all-current is invalid/incomplete because case 110 timed out before pack completion.
- `v032a` rendered as a no-op and is not semantic prompt evidence.
