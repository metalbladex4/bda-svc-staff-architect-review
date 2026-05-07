# v027 Final Recommendation

Updated: `2026-05-07T20:50:17Z`

Status: `stability_failed_stage1`

Backend used: `ollama_openai_compat_fallback_11434`

Preferred backend available: `False`

## Decision

Do not resume semantic prompt mutation until backend/rendering/request-shape stability is repaired or explained.

## Stage 1 Case 67 Results

| candidate | metrics | case 67 | rendered hash | request hash | status |
| --- | ---: | ---: | --- | --- | --- |
| `v027a_case67_exact_v020c_replay_1` | `1/10/9/19` | `1/10/9` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `8732a566584fe963574b43ea5f43d3223fa59284280dd0f8aaf816bf9c023da4` | `stability_fail` |
| `v027b_case67_exact_v020c_replay_2` | `9/2/4/6` | `9/2/4` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `8732a566584fe963574b43ea5f43d3223fa59284280dd0f8aaf816bf9c023da4` | `stability_pass` |
| `v027c_case67_exact_v020c_replay_3` | `9/2/4/6` | `9/2/4` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `8732a566584fe963574b43ea5f43d3223fa59284280dd0f8aaf816bf9c023da4` | `stability_pass` |
| `v027d_case67_blank_line_probe_1` | `1/10/9/19` | `1/10/9` | `6fbf853dfef7bf71f84e826194160bf27edac9b1c73d972d335b2d84b25a5926` | `95ec81aab89890c30b58564012ca928dc500abdcad05d1e80cc3b028f91e6f60` | `stability_fail` |
| `v027e_case67_blank_line_probe_2` | `1/10/9/19` | `1/10/9` | `6fbf853dfef7bf71f84e826194160bf27edac9b1c73d972d335b2d84b25a5926` | `95ec81aab89890c30b58564012ca928dc500abdcad05d1e80cc3b028f91e6f60` | `stability_fail` |
| `v027f_case67_trailing_space_probe` | `1/10/9/19` | `1/10/9` | `cc40f0dbeb7d8489e8e0cb709eb51124415ffe56a9d1823f5e4e101908142dbd` | `98d2f9b11c9768dee8f526cc1e788ca35fce1c17487f0e640938d066371126ff` | `stability_fail` |
| `v027g_case67_noop_template_roundtrip` | `9/2/4/6` | `9/2/4` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `8732a566584fe963574b43ea5f43d3223fa59284280dd0f8aaf816bf9c023da4` | `stability_pass` |

## Diagnosis

Stage 1 failed before Stage 2. Semantic prompt refinement did not resume.

The exact `v020c` rendered prompt and request-shape hashes were captured. They
were identical for `v027a`, `v027b`, `v027c`, and `v027g`, but the raw model
response split into two stable shapes:

- collapsed response hash `cc06a04e...`: `10` detections, case `67` at `1/10/9`
- stable response hash `91d10452...`: `13` detections, case `67` at `9/2/4`

Image evidence was identical across probes: source image SHA-256
`efee332a8e66c25f3a3d10713e77e77b89386e6d1834edcd213f3bf002410ec0`, resized
PNG SHA-256 `768d17874c081728e04112d656cc4c9256b58a7a3e110120b73243946f6208b9`,
and image payload SHA-256
`7d8e4a40b0f77c06e3e97e7fde077dad483933eff73dbd0fba6a2686240c6fd8`.

Overlay application succeeded for every probe, and JSON/schema/bbox filtering
did not explain the collapse. The most likely failure source is raw model
response drift on the fallback Ollama-backed OpenAI-compatible endpoint.

## Next Step

Keep `v020c` frozen as incumbent. Restore or validate the preferred
`http://localhost:8000/v1` backend and rerun the v027 Stage 1 probe there before
any semantic prompt mutation.
