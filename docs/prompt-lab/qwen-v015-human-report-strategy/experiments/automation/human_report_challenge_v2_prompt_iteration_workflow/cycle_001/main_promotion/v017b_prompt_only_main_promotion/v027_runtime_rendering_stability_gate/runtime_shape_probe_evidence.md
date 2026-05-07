# v027 Runtime Shape Probe Evidence

## Purpose

v027 adds the rendered-prompt, request-shape, image-serialization, and
response/parsing instrumentation that v026 lacked. The goal is to decide
whether semantic prompt mutation is safe to resume.

## Backend

- Preferred endpoint: `http://localhost:8000/v1`
- Preferred status: unavailable, connection refused
- Fallback endpoint used: `http://localhost:11434/v1`
- Backend label: `ollama_openai_compat_fallback_11434`
- Model: `qwen3-vl:8b-instruct`
- Ollama version: `0.15.2`

These results are fallback-only. They do not establish stability or instability
for the preferred endpoint.

## Stage 1 Result

Stage 1 failed on case `67`. Stage 2 was not run, and semantic prompt mutation
did not resume.

| probe | intended shape | rendered prompt hash | request-shape hash | raw detection response hash | case 67 |
| --- | --- | --- | --- | --- | ---: |
| `v027a_case67_exact_v020c_replay_1` | exact v020c | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `8732a566584fe963574b43ea5f43d3223fa59284280dd0f8aaf816bf9c023da4` | `cc06a04e5390a9204eaec275f250dd4d25d585268e31f3e35b2e912c17a60a62` | `1/10/9` |
| `v027b_case67_exact_v020c_replay_2` | exact v020c | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `8732a566584fe963574b43ea5f43d3223fa59284280dd0f8aaf816bf9c023da4` | `91d1045212de3610ea45f214a9defc6db179cf9dbdbde88623e745b2c6bd0529` | `9/2/4` |
| `v027c_case67_exact_v020c_replay_3` | exact v020c | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `8732a566584fe963574b43ea5f43d3223fa59284280dd0f8aaf816bf9c023da4` | `91d1045212de3610ea45f214a9defc6db179cf9dbdbde88623e745b2c6bd0529` | `9/2/4` |
| `v027d_case67_blank_line_probe_1` | one blank line | `6fbf853dfef7bf71f84e826194160bf27edac9b1c73d972d335b2d84b25a5926` | `95ec81aab89890c30b58564012ca928dc500abdcad05d1e80cc3b028f91e6f60` | `cc06a04e5390a9204eaec275f250dd4d25d585268e31f3e35b2e912c17a60a62` | `1/10/9` |
| `v027e_case67_blank_line_probe_2` | one blank line | `6fbf853dfef7bf71f84e826194160bf27edac9b1c73d972d335b2d84b25a5926` | `95ec81aab89890c30b58564012ca928dc500abdcad05d1e80cc3b028f91e6f60` | `cc06a04e5390a9204eaec275f250dd4d25d585268e31f3e35b2e912c17a60a62` | `1/10/9` |
| `v027f_case67_trailing_space_probe` | one trailing space | `cc40f0dbeb7d8489e8e0cb709eb51124415ffe56a9d1823f5e4e101908142dbd` | `98d2f9b11c9768dee8f526cc1e788ca35fce1c17487f0e640938d066371126ff` | `cc06a04e5390a9204eaec275f250dd4d25d585268e31f3e35b2e912c17a60a62` | `1/10/9` |
| `v027g_case67_noop_template_roundtrip` | no-op roundtrip | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `8732a566584fe963574b43ea5f43d3223fa59284280dd0f8aaf816bf9c023da4` | `91d1045212de3610ea45f214a9defc6db179cf9dbdbde88623e745b2c6bd0529` | `9/2/4` |

## What Was Captured

- Final rendered prompt text and SHA-256.
- Placeholder substitution hashes for `{categories}`, `{detection_guidance}`,
  `{bbox_format}`, and `{bbox_scale}`.
- Sanitized request-shape hash excluding raw image base64.
- Source image SHA-256, resized PNG SHA-256, and base64 payload SHA-256.
- Raw model response text and SHA-256.
- Repaired JSON text and SHA-256.
- Pydantic validation status.
- Raw detection count, final accepted detection count, rejected detections with
  reasons, and final bbox list.

## Key Interpretation

Exact v020c/no-op probes with the same rendered prompt hash and request-shape
hash split between collapsed and stable raw response hashes. That rules out a
simple overlay-application or placeholder-rendering explanation.

The most likely current failure source is raw model response drift on the
fallback Ollama-backed OpenAI-compatible endpoint. The blank-line and
trailing-space probes are still risky, but v027 cannot honestly attribute their
failure to prompt semantics alone because one exact replay produced the same
collapsed raw response.

## Decision

Pause semantic prompt mutation. Restore or validate the preferred
`localhost:8000/v1` backend, then rerun Stage 1 with the same instrumentation
before authoring another detect prompt.
