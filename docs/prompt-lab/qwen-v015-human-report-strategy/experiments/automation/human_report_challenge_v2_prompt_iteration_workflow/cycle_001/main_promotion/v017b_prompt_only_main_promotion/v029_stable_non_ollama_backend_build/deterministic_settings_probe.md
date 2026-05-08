# v029 Deterministic Settings Probe

v029 did not use Ollama deterministic aliases for prompt optimization.

The vLLM launch used:

- `--seed 42`
- `--enforce-eager`
- `--generation-config vllm`
- request temperature from bda-svc: captured in request traces
- OpenAI-compatible endpoint: `http://localhost:8000/v1`

The backend passed stability gates, but the full v020c baseline was
unacceptable:

```text
old v020c: 186 / 33 / 25 / 58
vLLM quantized v020c: 153 / 66 / 25 / 91
```

Therefore semantic prompt mutation remained paused for baseline quality, not
for repeatability failure.
