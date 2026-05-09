# v042 Comparison Matrix

| Candidate | Stage | Raw | Postprocessed | Case 66 | Case 67 | Case 84 | Case 100 | Case 110 | Case 155 | Case 166 | Removed | Removed TPs | Status |
|---|---|---|---|---|---|---|---|---|---|---|---:|---:|---|
| `old_product_v020c_reference` | prior_non_fp8_all_current | `186/33/25/58` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | n/a | n/a | product_reference_not_replaced |
| `v034a_fp8_broad_context_scene_box_guard` | v034_full_all_current_raw | `181/38/25/63` | `n/a` | `8/0/5 -> n/a` | `10/1/3 -> n/a` | `8/5/0 -> n/a` | `n/a -> n/a` | `3/4/1 -> n/a` | `2/0/1 -> n/a` | `1/0/0 -> n/a` | n/a | n/a | raw_fp8_prompt_working_best |
| `v034a_fp8_broad_context_scene_box_guard+p1753` | v041_reproduced_postprocessed | `181/38/25/63` | `181/38/24/62` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | n/a | n/a | composite_working_best |
| `v034a_fp8_broad_context_scene_box_guard+p1753` | frozen_v034a_reproduction | `181/38/25/63` | `181/38/24/62` | `8/0/5 -> 8/0/5` | `10/1/3 -> 10/1/3` | `8/5/0 -> 8/5/0` | `1/2/1 -> 1/2/1` | `3/4/1 -> 3/4/1` | `2/0/1 -> 2/0/1` | `1/0/0 -> 1/0/0` | 1 | 0 | complete |
| `v042_baseline_exact_v034a_replay` | micro_pack_only | `45/14/15/29` | `45/14/14/28` | `8/0/5 -> 8/0/5` | `10/1/3 -> 10/1/3` | `8/5/0 -> 8/5/0` | `1/2/1 -> 1/2/1` | `3/4/1 -> 3/4/1` | `2/0/1 -> 2/0/1` | `1/0/0 -> 1/0/0` | 1 | 0 | baseline_replay |
| `v042a_fp8_case84_low_contrast_recall_probe` | micro_pack_only | `43/16/16/32` | `43/16/15/31` | `8/0/6 -> 8/0/6` | `10/1/2 -> 10/1/2` | `7/6/0 -> 7/6/0` | `1/2/1 -> 1/2/1` | `3/4/1 -> 3/4/1` | `2/0/0 -> 2/0/0` | `1/0/0 -> 1/0/0` | 1 | 0 | rejected |
| `v042b_fp8_mostly_context_box_guard` | micro_pack_only | `43/16/19/35` | `43/16/18/34` | `7/1/6 -> 7/1/6` | `10/1/3 -> 10/1/3` | `8/5/0 -> 8/5/0` | `1/2/1 -> 1/2/1` | `3/4/1 -> 3/4/1` | `2/0/2 -> 2/0/2` | `1/0/0 -> 1/0/0` | 1 | 0 | rejected |
| `v042c_fp8_uncertain_fragments_phrase_ablation` | micro_pack_only | `40/19/23/42` | `40/19/22/41` | `8/0/10 -> 8/0/10` | `8/3/3 -> 8/3/3` | `7/6/0 -> 7/6/0` | `1/2/1 -> 1/2/1` | `3/4/1 -> 3/4/1` | `2/0/2 -> 2/0/2` | `1/0/0 -> 1/0/0` | 1 | 0 | rejected |
| `v042d_fp8_final_balance_simplification` | micro_pack_only | `44/15/16/31` | `44/15/15/30` | `8/0/5 -> 8/0/5` | `10/1/1 -> 10/1/1` | `7/6/1 -> 7/6/1` | `2/1/1 -> 2/1/1` | `3/4/1 -> 3/4/1` | `2/0/1 -> 2/0/1` | `1/0/0 -> 1/0/0` | 1 | 0 | rejected |
| `v042e_fp8_separate_small_target_row_exception` | micro_pack_only | `42/17/22/39` | `42/17/21/38` | `8/0/6 -> 8/0/6` | `8/3/4 -> 8/3/4` | `8/5/0 -> 8/5/0` | `1/2/1 -> 1/2/1` | `3/4/3 -> 3/4/3` | `2/0/2 -> 2/0/2` | `1/0/0 -> 1/0/0` | 1 | 0 | rejected |
