# v042 Comparison Matrix

| Candidate | Stage | Raw | Postprocessed | Case 66 | Case 67 | Case 84 | Case 100 | Case 110 | Case 155 | Case 166 | Removed | Removed TPs | Status |
|---|---|---|---|---|---|---|---|---|---|---|---:|---:|---|
| `old_product_v020c_reference` | prior_non_fp8_all_current | `186/33/25/58` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | n/a | n/a | product_reference_not_replaced |
| `v034a_fp8_broad_context_scene_box_guard` | v034_full_all_current_raw | `181/38/25/63` | `n/a` | `8/0/5 -> n/a` | `10/1/3 -> n/a` | `8/5/0 -> n/a` | `n/a -> n/a` | `3/4/1 -> n/a` | `2/0/1 -> n/a` | `1/0/0 -> n/a` | n/a | n/a | raw_fp8_prompt_working_best |
| `v034a_fp8_broad_context_scene_box_guard+p1753` | v041_reproduced_postprocessed | `181/38/25/63` | `181/38/24/62` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | n/a | n/a | composite_working_best |
| `v034a_fp8_broad_context_scene_box_guard+p1753` | frozen_v034a_reproduction | `181/38/25/63` | `181/38/24/62` | `8/0/5 -> 8/0/5` | `10/1/3 -> 10/1/3` | `8/5/0 -> 8/5/0` | `1/2/1 -> 1/2/1` | `3/4/1 -> 3/4/1` | `2/0/1 -> 2/0/1` | `1/0/0 -> 1/0/0` | 1 | 0 | complete |
