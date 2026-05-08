# v029 Backend Launch Log

Successful launch:

```bash
HF_HUB_DISABLE_TELEMETRY=1 /tmp/bda_v029_vllm_env/bin/python -m vllm.entrypoints.openai.api_server   --host 127.0.0.1 --port 8000   --model SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16   --served-model-name Qwen/Qwen3-VL-8B-Instruct   --trust-remote-code --dtype auto --max-model-len 4096   --limit-mm-per-prompt.image 2 --gpu-memory-utilization 0.85   --enforce-eager --seed 42 --generation-config vllm
```

The first vLLM launch used `--limit-mm-per-prompt.image 1`; detection worked, but bda-svc assessment sent two images and vLLM returned a request-shape error. Relaunching with image limit `2` fixed the compatibility issue.
