# v028 Final Recommendation

Updated: `2026-05-07T23:32:12Z`

Status: `stability_failed_stage1`

Decision: `D. no_stable_backend_available_stop_prompt_mutation`

## Summary

No stable backend was recovered. The original preferred `localhost:8000/v1`
backend was unavailable before recovery. v028 created a deterministic
Ollama-backed Qwen model alias from cached local model files and launched an
experiment-only Ollama endpoint on `localhost:8000/v1`, but that endpoint still
failed the case-67 stability gate.

Semantic prompt refinement did not resume.

## Backend Tested

- backend label: `ollama_deterministic_local_8000`
- endpoint: `http://localhost:8000/v1`
- model: `qwen3-vl:8b-instruct-v028-deterministic`
- local model source: `cached Ollama model`
- public/HF model download: `not performed`
- product runtime/config mutation: `none`

## Stage 1 Case 67 Results

| probe | case 67 | raw response | rendered prompt | request shape | status |
| --- | ---: | --- | --- | --- | --- |
| `v028a_case67_exact_v020c_replay_1` | `1/10/9` | `cc06a04e5390a9204eaec275f250dd4d25d585268e31f3e35b2e912c17a60a62` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `65885b0141a326abbaeae72f97494c47c92e6925e5652cfc3e48b0276ffc8cd7` | `stability_fail` |
| `v028b_case67_exact_v020c_replay_2` | `9/2/4` | `91d1045212de3610ea45f214a9defc6db179cf9dbdbde88623e745b2c6bd0529` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `65885b0141a326abbaeae72f97494c47c92e6925e5652cfc3e48b0276ffc8cd7` | `stability_pass` |
| `v028c_case67_exact_v020c_replay_3` | `9/2/4` | `91d1045212de3610ea45f214a9defc6db179cf9dbdbde88623e745b2c6bd0529` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `65885b0141a326abbaeae72f97494c47c92e6925e5652cfc3e48b0276ffc8cd7` | `stability_pass` |
| `v028d_case67_blank_line_probe_1` | `1/10/9` | `cc06a04e5390a9204eaec275f250dd4d25d585268e31f3e35b2e912c17a60a62` | `6fbf853dfef7bf71f84e826194160bf27edac9b1c73d972d335b2d84b25a5926` | `765dcf5b111ff17b4646070d0e576b42485f67196ca457a83f6893c4b91a3a0f` | `stability_fail` |
| `v028e_case67_blank_line_probe_2` | `1/10/9` | `cc06a04e5390a9204eaec275f250dd4d25d585268e31f3e35b2e912c17a60a62` | `6fbf853dfef7bf71f84e826194160bf27edac9b1c73d972d335b2d84b25a5926` | `765dcf5b111ff17b4646070d0e576b42485f67196ca457a83f6893c4b91a3a0f` | `stability_fail` |
| `v028f_case67_trailing_space_probe` | `1/10/9` | `cc06a04e5390a9204eaec275f250dd4d25d585268e31f3e35b2e912c17a60a62` | `cc40f0dbeb7d8489e8e0cb709eb51124415ffe56a9d1823f5e4e101908142dbd` | `3b2e472c0baad457c35bb06c84ec0987e1a1fefad6b6bfa88295bf48efaaa650` | `stability_fail` |
| `v028g_case67_noop_template_roundtrip` | `9/2/4` | `91d1045212de3610ea45f214a9defc6db179cf9dbdbde88623e745b2c6bd0529` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `65885b0141a326abbaeae72f97494c47c92e6925e5652cfc3e48b0276ffc8cd7` | `stability_pass` |

## Interpretation

The deterministic Ollama alias used `temperature 0`, `top_k 1`, `top_p 1`,
`seed 42`, and `num_ctx 4096`. Even with those settings, the first exact
`v020c` replay collapsed while later exact/no-op replays returned the known
stable case-67 behavior. The blank-line and trailing-space probes collapsed
consistently.

This is enough to keep prompt mutation paused. The strongest remaining
hypothesis is a backend/model-serving instability or cold-start/request-shape
sensitivity in the Ollama-backed path, not a trustworthy prompt-quality signal.

## Required Next Fix Before Autonomy

Restore a genuinely stable OpenAI-compatible multimodal backend, preferably a
vLLM/SGLang/Transformers server that supports the bda-svc request shape and can
pass exact replay plus blank-line/trailing-space probes before any semantic
prompt work resumes.
