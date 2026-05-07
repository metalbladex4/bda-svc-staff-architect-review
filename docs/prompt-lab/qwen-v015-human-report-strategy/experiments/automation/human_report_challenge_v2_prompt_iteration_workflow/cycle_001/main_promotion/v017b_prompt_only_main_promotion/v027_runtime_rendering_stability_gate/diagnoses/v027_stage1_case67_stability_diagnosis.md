# v027 Stage 1 Case 67 Stability Diagnosis

Generated: `2026-05-07T20:55:00Z`

## Verdict

Stage 1 failed. Do not resume semantic prompt mutation.

The strongest evidence is not a blank-line semantic effect. It is that an exact
`v020c` replay produced two different raw detection responses while the rendered
prompt hash, request-shape hash, source image hash, resized image PNG hash, and
overlay application state were identical.

## Backend

- Preferred endpoint: `http://localhost:8000/v1`
- Preferred status: unavailable, connection refused
- Fallback endpoint used: `http://localhost:11434/v1`
- Fallback label: `ollama_openai_compat_fallback_11434`
- Model: `qwen3-vl:8b-instruct`
- Ollama version: `0.15.2`

These findings are fallback-only. They do not prove the preferred
`localhost:8000/v1` backend is unstable.

## Probe Results

| candidate | rendered prompt hash | request-shape hash | raw response hash | case 67 | status |
| --- | --- | --- | --- | ---: | --- |
| `v027a_case67_exact_v020c_replay_1` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `8732a566584fe963574b43ea5f43d3223fa59284280dd0f8aaf816bf9c023da4` | `cc06a04e5390a9204eaec275f250dd4d25d585268e31f3e35b2e912c17a60a62` | `1/10/9` | fail |
| `v027b_case67_exact_v020c_replay_2` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `8732a566584fe963574b43ea5f43d3223fa59284280dd0f8aaf816bf9c023da4` | `91d1045212de3610ea45f214a9defc6db179cf9dbdbde88623e745b2c6bd0529` | `9/2/4` | pass |
| `v027c_case67_exact_v020c_replay_3` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `8732a566584fe963574b43ea5f43d3223fa59284280dd0f8aaf816bf9c023da4` | `91d1045212de3610ea45f214a9defc6db179cf9dbdbde88623e745b2c6bd0529` | `9/2/4` | pass |
| `v027d_case67_blank_line_probe_1` | `6fbf853dfef7bf71f84e826194160bf27edac9b1c73d972d335b2d84b25a5926` | `95ec81aab89890c30b58564012ca928dc500abdcad05d1e80cc3b028f91e6f60` | `cc06a04e5390a9204eaec275f250dd4d25d585268e31f3e35b2e912c17a60a62` | `1/10/9` | fail |
| `v027e_case67_blank_line_probe_2` | `6fbf853dfef7bf71f84e826194160bf27edac9b1c73d972d335b2d84b25a5926` | `95ec81aab89890c30b58564012ca928dc500abdcad05d1e80cc3b028f91e6f60` | `cc06a04e5390a9204eaec275f250dd4d25d585268e31f3e35b2e912c17a60a62` | `1/10/9` | fail |
| `v027f_case67_trailing_space_probe` | `cc40f0dbeb7d8489e8e0cb709eb51124415ffe56a9d1823f5e4e101908142dbd` | `98d2f9b11c9768dee8f526cc1e788ca35fce1c17487f0e640938d066371126ff` | `cc06a04e5390a9204eaec275f250dd4d25d585268e31f3e35b2e912c17a60a62` | `1/10/9` | fail |
| `v027g_case67_noop_template_roundtrip` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `8732a566584fe963574b43ea5f43d3223fa59284280dd0f8aaf816bf9c023da4` | `91d1045212de3610ea45f214a9defc6db179cf9dbdbde88623e745b2c6bd0529` | `9/2/4` | pass |

## What The Instrumentation Rules Out

- Overlay application failure: every probe reported `overlay_actually_applied: true`.
- Scratch config mismatch: every probe reported an empty diff between intended overlay and scratch `detect_objects`.
- Case 67 image drift: every probe used source image SHA-256 `efee332a8e66c25f3a3d10713e77e77b89386e6d1834edcd213f3bf002410ec0`.
- Resized image drift: every probe used resized PNG SHA-256 `768d17874c081728e04112d656cc4c9256b58a7a3e110120b73243946f6208b9`.
- Image payload drift: every probe used base64 payload SHA-256 `7d8e4a40b0f77c06e3e97e7fde077dad483933eff73dbd0fba6a2686240c6fd8`.
- JSON repair/schema/filtering failure: every detection response validated, and no target-type or bbox-conversion rejects occurred.

## Most Likely Failure Source

The failure appears to originate in raw model response drift on the fallback
OpenAI-compatible Ollama endpoint.

Exact `v020c` runs with identical rendered prompt and request-shape hashes split
between:

- collapsed raw response hash `cc06a04e...`, 10 detections, case `67` at `1/10/9`
- stable raw response hash `91d10452...`, 13 detections, case `67` at `9/2/4`

The blank-line and trailing-space probes consistently returned the collapsed
raw response shape, but because exact v020c also returned that shape once, v027
cannot safely attribute the failure to prompt semantics alone.

## Remaining Uncertainty

- The preferred `localhost:8000/v1` backend was unavailable, so preferred-backend
  stability remains untested.
- The scratch instrumentation reimplemented the upstream `VLMBackend.generate`
  request construction to capture hashes. It follows upstream code shape, but
  the preferred follow-up is to add a production-equivalent request tap or run
  the same probe on the preferred backend.
- Backend internals, chat-template behavior, and model-cache state are not
  observable from the captured OpenAI-compatible request alone.

## Decision

Do not author semantic prompt candidates. The next move is backend/rendering
stability repair or deeper request instrumentation, preferably on the preferred
`localhost:8000/v1` backend, before another prompt-refinement tranche.
