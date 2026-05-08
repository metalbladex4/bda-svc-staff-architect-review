# v029 Baseline Unacceptable Diagnosis

The vLLM backend stabilized the request surface, but the served quantized model does not reproduce the old v020c all-current baseline closely enough.

- Prior v020c: `186 / 33 / 25 / 58`
- v029 vLLM quantized v020c: `153 / 66 / 25 / 91`
- Delta: `+33` combined errors

This exceeds the user-defined pause threshold of `+20` combined errors. Because the baseline is model/backend-specific, prompt engineering on this backend would optimize a different model behavior profile and should not be treated as a continuation of the old Qwen v020c line.
