# Stability Matrix

| Backend | Stage | Probe | Case 67 | Totals | Status |
|---|---|---|---:|---:|---|
| sglang_qwen3vl_8b_fp8_local_8000 | case67_stability | v031a_case67_cold_exact_v020c_replay | 0/11/1 | 0/11/1 | stability_fail |
| sglang_qwen3vl_8b_fp8_local_8000 | case67_stability | v031b_case67_warmup_request | 0/11/1 | 0/11/1 | stability_fail |
| sglang_qwen3vl_8b_fp8_local_8000 | case67_stability | v031c_case67_warm_exact_v020c_replay_1 | 0/11/1 | 0/11/1 | stability_fail |
| sglang_qwen3vl_8b_fp8_local_8000 | case67_stability | v031d_case67_warm_exact_v020c_replay_2 | 0/11/1 | 0/11/1 | stability_fail |
| sglang_qwen3vl_8b_fp8_local_8000 | case67_stability | v031e_case67_warm_exact_v020c_replay_3 | 0/11/1 | 0/11/1 | stability_fail |
| sglang_qwen3vl_8b_fp8_local_8000 | case67_stability | v031f_case67_blank_line_probe | 0/11/1 | 0/11/1 | stability_fail |
| sglang_qwen3vl_8b_fp8_local_8000 | case67_stability | v031g_case67_trailing_space_probe | 0/11/1 | 0/11/1 | stability_fail |
| sglang_qwen3vl_8b_fp8_local_8000 | case67_stability | v031h_case67_noop_template_roundtrip | 0/11/1 | 0/11/1 | stability_fail |
| vllm_qwen3vl_8b_fp8_local_8000 | case67_stability | v031a_case67_cold_exact_v020c_replay | 10/1/2 | 10/1/2 | stability_pass |
| vllm_qwen3vl_8b_fp8_local_8000 | case67_stability | v031b_case67_warmup_request | 10/1/2 | 10/1/2 | stability_pass |
| vllm_qwen3vl_8b_fp8_local_8000 | case67_stability | v031c_case67_warm_exact_v020c_replay_1 | 10/1/2 | 10/1/2 | stability_pass |
| vllm_qwen3vl_8b_fp8_local_8000 | case67_stability | v031d_case67_warm_exact_v020c_replay_2 | 10/1/2 | 10/1/2 | stability_pass |
| vllm_qwen3vl_8b_fp8_local_8000 | case67_stability | v031e_case67_warm_exact_v020c_replay_3 | 10/1/2 | 10/1/2 | stability_pass |
| vllm_qwen3vl_8b_fp8_local_8000 | case67_stability | v031f_case67_blank_line_probe | 8/3/5 | 8/3/5 | stability_pass |
| vllm_qwen3vl_8b_fp8_local_8000 | case67_stability | v031g_case67_trailing_space_probe | 10/1/2 | 10/1/2 | stability_pass |
| vllm_qwen3vl_8b_fp8_local_8000 | case67_stability | v031h_case67_noop_template_roundtrip | 10/1/2 | 10/1/2 | stability_pass |
| vllm_qwen3vl_8b_fp8_local_8000 | sentinel_stability | v031i_sentinel_exact_v020c_replay_1 | 10/1/2 | 42/7/15 | stability_pass |
| vllm_qwen3vl_8b_fp8_local_8000 | sentinel_stability | v031j_sentinel_exact_v020c_replay_2 | 10/1/2 | 42/7/15 | stability_pass |
| vllm_qwen3vl_8b_fp8_local_8000 | sentinel_stability | v031k_sentinel_blank_line_probe | 8/3/5 | 38/11/19 | stability_pass |
| vllm_qwen3vl_8b_fp8_local_8000 | sentinel_stability | v031l_sentinel_trailing_space_probe | 10/1/2 | 40/9/21 | stability_pass |
| vllm_qwen3vl_8b_fp8_local_8000 | sentinel_stability | v031m_sentinel_noop_template_roundtrip | 10/1/2 | 42/7/15 | stability_pass |
| vllm_qwen3vl_8b_fp8_local_8000 | full_v020c_baseline | v031a_case67_cold_exact_v020c_replay | 10/1/2 | 180/39/32 | stability_pass |
| vllm_qwen3vl_8b_fp8_local_8000 | office_negative_guard | v031a_case67_cold_exact_v020c_replay | n/a | 1/0/0 | stability_fail |

Interpretation: SGLang was repeatable but behaviorally unusable on case 67. vLLM FP8 was stable enough for attribution, but the surface was not acceptable after full all-current baseline.
