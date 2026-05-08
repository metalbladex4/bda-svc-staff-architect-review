# SGLang Launch Log

Final successful launch log: `backend_logs/sglang_fp8_disable_cudagraph_launch_20260508T212359Z.log`.

Final SGLang endpoint: `http://localhost:8000/v1`.

Result: launched, accepted the bda-svc style request, returned parseable responses, but failed case 67 on every probe.

| Probe | Case 67 | Status |
|---|---:|---|
| v031a_case67_cold_exact_v020c_replay | 0/11/1 | stability_fail |
| v031b_case67_warmup_request | 0/11/1 | stability_fail |
| v031c_case67_warm_exact_v020c_replay_1 | 0/11/1 | stability_fail |
| v031d_case67_warm_exact_v020c_replay_2 | 0/11/1 | stability_fail |
| v031e_case67_warm_exact_v020c_replay_3 | 0/11/1 | stability_fail |
| v031f_case67_blank_line_probe | 0/11/1 | stability_fail |
| v031g_case67_trailing_space_probe | 0/11/1 | stability_fail |
| v031h_case67_noop_template_roundtrip | 0/11/1 | stability_fail |
