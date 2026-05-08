# Backend Launch Attempts

- vLLM exact: launched but first BDA case-67 request timed out at client timeout
- vLLM exact: one launch rejected free-memory target, one launch failed KV cache allocation
- vLLM exact: launched, but first BDA case-67 request timed out
- HF Transformers shim: tiny multimodal JSON smoke passed; first BDA request hit meta-device error with cuda inputs; retry with CPU/no forced input device timed out

Logs:
- `backend_logs/hf_transformers_exact_input_none_launch_20260508T160242Z.log`
- `backend_logs/hf_transformers_exact_launch_20260508T155800Z.log`
- `backend_logs/vllm_exact_cpuoffload4_gpu089_launch_20260508T154756Z.log`
- `backend_logs/vllm_exact_cpuoffload4_launch_20260508T154706Z.log`
- `backend_logs/vllm_exact_cpuoffload8_launch_20260508T154925Z.log`
- `backend_logs/vllm_exact_cpuoffload_launch_20260508T153717Z.log`
- `backend_logs/vllm_exact_launch_20260508T153659Z.log`
