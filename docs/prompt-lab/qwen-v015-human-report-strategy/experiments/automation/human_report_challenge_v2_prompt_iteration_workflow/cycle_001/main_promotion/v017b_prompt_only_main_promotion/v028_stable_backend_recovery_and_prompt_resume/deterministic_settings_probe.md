# v028 Deterministic Settings Probe

The deterministic Ollama alias was created with:

```text
FROM qwen3-vl:8b-instruct
PARAMETER temperature 0
PARAMETER top_k 1
PARAMETER top_p 1
PARAMETER seed 42
PARAMETER num_ctx 4096
```

Official Ollama Modelfile documentation states that `seed` sets the random
number seed for generation and that temperature/top-k/top-p control sampling.
Local evidence shows these settings were insufficient to make the fallback
Ollama-backed Qwen3-VL path safe for prompt optimization.
