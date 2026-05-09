# v035 Comparison Matrix

| Candidate | Stage | Matches | FNs | FPs | Errors | Case 66 | Case 67 | Case 84 | Case 110 | Case 155 | Case 166 | Office | Status |
|---|---|---:|---:|---:|---:|---|---|---|---|---|---|---|---|
| `v020c_old_product_reference` | prior_all_current | 186 | 33 | 25 | 58 | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | n/a | product_reference |
| `v020c_fp8_vllm_baseline` | v031_all_current | 180 | 39 | 32 | 71 | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | n/a | fp8_working_baseline |
| `v032d_fp8_v019c_anchor_replay` | v033_clean_full | 185 | 34 | 57 | 91 | `n/a` | `8/3/2` | `n/a` | `3/4/32` | `2/0/0` | `1/0/0` | pass | rejected |
| `v034a_fp8_broad_context_scene_box_guard` | v034_full_all_current | 181 | 38 | 25 | 63 | `8/0/5` | `10/1/3` | `8/5/0` | `3/4/1` | `2/0/1` | `1/0/0` | pass | fp8_working_best |
| `v035_baseline_exact_v034a_replay` | micro_pack_only | 44 | 12 | 14 | 26 | `8/0/5` | `10/1/3` | `8/5/0` | `3/4/1` | `2/0/1` | `1/0/0` | pass | baseline_replay |
| `v035a_fp8_dense_uncertain_fragment_guard` | micro_pack_only | 41 | 15 | 19 | 34 | `8/0/6` | `7/4/5` | `8/5/0` | `4/3/2` | `2/0/0` | `1/0/0` | pass | rejected |
