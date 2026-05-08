# Backend Feasibility Matrix

| Backend | Target model | Feasibility result | Outcome |
|---|---|---|---|
| SGLang | Qwen/Qwen3-VL-8B-Instruct-FP8 | Installed in isolated `/tmp/bda_v031_sglang_env`; required local libnuma, isolated CuDNN package, and `--disable-cuda-graph`. | Launched, but case 67 failed at `0/11/1` on every probe. |
| vLLM | Qwen/Qwen3-VL-8B-Instruct-FP8 | Existing vLLM env from v029 was usable. | Launched, passed stability, red full baseline at `180/39/32/71`. |
| Transformers debug | Qwen/Qwen3-VL-8B-Instruct-FP8 | Feasible only as debug path. | Not run because vLLM backup completed the scoring gate. |

Hardware was adequate for FP8 serving on the local RTX 5000 Ada laptop GPU.
