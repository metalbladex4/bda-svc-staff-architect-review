# v027 Stability Matrix

| candidate | stage | backend | matches | FNs | FPs | combined errors | case 67 | rendered prompt hash | request shape hash | status |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| v027a_case67_exact_v020c_replay_1 | case67_stability | ollama_openai_compat_fallback_11434 | 1 | 10 | 9 | 19 | 1/10/9 | 0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b | 8732a566584fe963574b43ea5f43d3223fa59284280dd0f8aaf816bf9c023da4 | stability_fail |
| v027b_case67_exact_v020c_replay_2 | case67_stability | ollama_openai_compat_fallback_11434 | 9 | 2 | 4 | 6 | 9/2/4 | 0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b | 8732a566584fe963574b43ea5f43d3223fa59284280dd0f8aaf816bf9c023da4 | stability_pass |
| v027c_case67_exact_v020c_replay_3 | case67_stability | ollama_openai_compat_fallback_11434 | 9 | 2 | 4 | 6 | 9/2/4 | 0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b | 8732a566584fe963574b43ea5f43d3223fa59284280dd0f8aaf816bf9c023da4 | stability_pass |
| v027d_case67_blank_line_probe_1 | case67_stability | ollama_openai_compat_fallback_11434 | 1 | 10 | 9 | 19 | 1/10/9 | 6fbf853dfef7bf71f84e826194160bf27edac9b1c73d972d335b2d84b25a5926 | 95ec81aab89890c30b58564012ca928dc500abdcad05d1e80cc3b028f91e6f60 | stability_fail |
| v027e_case67_blank_line_probe_2 | case67_stability | ollama_openai_compat_fallback_11434 | 1 | 10 | 9 | 19 | 1/10/9 | 6fbf853dfef7bf71f84e826194160bf27edac9b1c73d972d335b2d84b25a5926 | 95ec81aab89890c30b58564012ca928dc500abdcad05d1e80cc3b028f91e6f60 | stability_fail |
| v027f_case67_trailing_space_probe | case67_stability | ollama_openai_compat_fallback_11434 | 1 | 10 | 9 | 19 | 1/10/9 | cc40f0dbeb7d8489e8e0cb709eb51124415ffe56a9d1823f5e4e101908142dbd | 98d2f9b11c9768dee8f526cc1e788ca35fce1c17487f0e640938d066371126ff | stability_fail |
| v027g_case67_noop_template_roundtrip | case67_stability | ollama_openai_compat_fallback_11434 | 9 | 2 | 4 | 6 | 9/2/4 | 0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b | 8732a566584fe963574b43ea5f43d3223fa59284280dd0f8aaf816bf9c023da4 | stability_pass |
