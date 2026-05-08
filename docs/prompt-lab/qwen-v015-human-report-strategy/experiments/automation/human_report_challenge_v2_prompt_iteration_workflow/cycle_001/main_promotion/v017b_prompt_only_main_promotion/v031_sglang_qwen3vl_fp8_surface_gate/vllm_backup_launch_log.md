# vLLM Backup Launch Log

vLLM backup endpoint: `http://localhost:8000/v1`.

Launch log: `backend_logs/vllm_fp8_launch_20260508T212746Z.log`.

vLLM launched official `Qwen/Qwen3-VL-8B-Instruct-FP8`, passed case-67 stability and sentinel stability, then failed the full baseline acceptance gate.

## Case 67 Probes

| Probe | Case 67 | Status |
|---|---:|---|
| v031a_case67_cold_exact_v020c_replay | 10/1/2 | stability_pass |
| v031b_case67_warmup_request | 10/1/2 | stability_pass |
| v031c_case67_warm_exact_v020c_replay_1 | 10/1/2 | stability_pass |
| v031d_case67_warm_exact_v020c_replay_2 | 10/1/2 | stability_pass |
| v031e_case67_warm_exact_v020c_replay_3 | 10/1/2 | stability_pass |
| v031f_case67_blank_line_probe | 8/3/5 | stability_pass |
| v031g_case67_trailing_space_probe | 10/1/2 | stability_pass |
| v031h_case67_noop_template_roundtrip | 10/1/2 | stability_pass |

## Sentinel Probes

| Probe | Case 67 | Totals | Status |
|---|---:|---:|---|
| v031i_sentinel_exact_v020c_replay_1 | 10/1/2 | 42/7/15 | stability_pass |
| v031j_sentinel_exact_v020c_replay_2 | 10/1/2 | 42/7/15 | stability_pass |
| v031k_sentinel_blank_line_probe | 8/3/5 | 38/11/19 | stability_pass |
| v031l_sentinel_trailing_space_probe | 10/1/2 | 40/9/21 | stability_pass |
| v031m_sentinel_noop_template_roundtrip | 10/1/2 | 42/7/15 | stability_pass |
