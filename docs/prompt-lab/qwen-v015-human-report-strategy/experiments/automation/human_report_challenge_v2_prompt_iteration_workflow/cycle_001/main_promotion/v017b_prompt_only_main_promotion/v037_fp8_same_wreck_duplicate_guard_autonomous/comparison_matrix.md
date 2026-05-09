# v037 Comparison Matrix

| Candidate | Stage | Metrics | Case 66 | Case 67 | Case 84 | Case 97 | Case 110 | Case 155 | Case 166 | Office | Status | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `v020c_old_product_reference` | prior_all_current | `186/33/25/58` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | n/a | old_product_reference_not_fp8_replacement | Prior non-FP8 product-reference evidence only. |
| `v020c_fp8_vllm_baseline` | v031_full_all_current | `180/39/32/71` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | n/a | fp8_baseline |  |
| `v032d_fp8_v019c_anchor_replay` | v033_clean_full | `185/34/57/91` | `n/a` | `8/3/2` | `n/a` | `n/a` | `3/4/32` | `2/0/0` | `1/0/0` | pass | rejected | Fixed case 155 but exploded FPs, especially case 110. |
| `v034a_fp8_broad_context_scene_box_guard` | v034_full_all_current | `181/38/25/63` | `8/0/5` | `10/1/3` | `8/5/0` | `1/0/1` | `3/4/1` | `2/0/1` | `1/0/0` | pass | fp8_working_best |  |
| `v037_baseline_exact_v034a_replay` | v037_baseline_micro | `44/12/14/26` | `8/0/5` | `10/1/3` | `8/5/0` | `1/0/1` | `3/4/1` | `2/0/1` | `1/0/0` | pass | baseline_replay | Exact v034a replay before v037 prompt mutations. |
| `v037a_fp8_same_wreck_duplicate_local_guard` | micro_pack_only | `41/15/30/45` | `8/0/6` | `9/2/2` | `8/5/0` | `0/1/1` | `2/5/16` | `2/0/0` | `1/0/0` | pass | rejected | Case 155 improved to 2/0/0 but case 110 exploded to 16 FPs and case 66 worsened. |
| `v037b_fp8_same_wreck_inside_box_guard` | micro_pack_only | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | pass | runtime_invalid | Case 110 hit the 4096-token context cap after three attempts. |
| `v037c_fp8_same_wreck_inner_duplicate_guard` | micro_pack_only | `43/13/17/30` | `8/0/6` | `9/2/3` | `8/5/0` | `1/0/1` | `3/4/1` | `2/0/1` | `1/0/0` | pass | rejected | Shortened same-wreck wording avoided runtime failure but did not improve case 155 and worsened case 66. |
| `v037d_fp8_low_contrast_body_recall_cue` | micro_pack_only | `42/14/18/32` | `8/0/7` | `8/3/6` | `8/5/0` | `1/0/1` | `3/4/1` | `2/0/0` | `1/0/0` | pass | rejected | Low-contrast recall cue fixed case 155 but did not improve case 84 and worsened dense precision. |
