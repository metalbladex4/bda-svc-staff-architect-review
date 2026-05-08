# v029 Backend Stability Matrix

| Candidate | Stage | Case 67 | Status | Rendered Prompt Hash | Request Shape Hash |
| --- | --- | --- | --- | --- | --- |
| `v029a_case67_exact_v020c_replay_1` | `case67_stability` | `8/3/7` | `stability_pass` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `9bf71a69f61ab2a9518b8abec8bee7a779c8c597f1d21033a719b51cdd8c9dc4` |
| `v029b_case67_exact_v020c_replay_2` | `case67_stability` | `8/3/7` | `stability_pass` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `9bf71a69f61ab2a9518b8abec8bee7a779c8c597f1d21033a719b51cdd8c9dc4` |
| `v029c_case67_exact_v020c_replay_3` | `case67_stability` | `8/3/7` | `stability_pass` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `9bf71a69f61ab2a9518b8abec8bee7a779c8c597f1d21033a719b51cdd8c9dc4` |
| `v029d_case67_blank_line_probe_1` | `case67_stability` | `9/2/7` | `stability_pass` | `6fbf853dfef7bf71f84e826194160bf27edac9b1c73d972d335b2d84b25a5926` | `a221a5ff1acfbcd79e27100b901d67c634379f5a61e3a4cd05fe5f0b0bc41e30` |
| `v029e_case67_blank_line_probe_2` | `case67_stability` | `9/2/8` | `stability_pass` | `6fbf853dfef7bf71f84e826194160bf27edac9b1c73d972d335b2d84b25a5926` | `a221a5ff1acfbcd79e27100b901d67c634379f5a61e3a4cd05fe5f0b0bc41e30` |
| `v029f_case67_trailing_space_probe` | `case67_stability` | `8/3/7` | `stability_pass` | `cc40f0dbeb7d8489e8e0cb709eb51124415ffe56a9d1823f5e4e101908142dbd` | `966d5e86b46d971c8498229683efaaca52156c3bc15b9a19ae4b0cc9d2eda2cd` |
| `v029g_case67_noop_template_roundtrip` | `case67_stability` | `9/2/8` | `stability_pass` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `9bf71a69f61ab2a9518b8abec8bee7a779c8c597f1d21033a719b51cdd8c9dc4` |
| `v029h_sentinel_exact_v020c_replay_1` | `sentinel_stability` | `9/2/5` | `stability_pass` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `dd4fc604e4ac0b9c3cd59b414e97b5c0ded3857751a0f2c2fe6abbe1fceef474` |
| `v029i_sentinel_exact_v020c_replay_2` | `sentinel_stability` | `9/2/5` | `stability_pass` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `dd4fc604e4ac0b9c3cd59b414e97b5c0ded3857751a0f2c2fe6abbe1fceef474` |
| `v029j_sentinel_blank_line_shape_probe` | `sentinel_stability` | `9/2/9` | `stability_pass` | `6fbf853dfef7bf71f84e826194160bf27edac9b1c73d972d335b2d84b25a5926` | `c1efcd98973e833fc3bc2900b07272d205dca51bb2069ce34c79030104cb6439` |
| `v029k_sentinel_trailing_space_shape_probe` | `sentinel_stability` | `9/2/4` | `stability_pass` | `cc40f0dbeb7d8489e8e0cb709eb51124415ffe56a9d1823f5e4e101908142dbd` | `a5427cc2c3b91374e71d3fa32b36873a992dc84c5b18391b03730d110c113936` |
| `v029l_sentinel_noop_template_roundtrip` | `sentinel_stability` | `9/2/5` | `stability_pass` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `dd4fc604e4ac0b9c3cd59b414e97b5c0ded3857751a0f2c2fe6abbe1fceef474` |
| `v020c_vllm_quantized_baseline` | `full_v020c_baseline` | `9/2/5` | `stability_pass` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `fb2cf0f7aa0f34453f7d593db93af42bf529b97155fe91e3e155ee12017f5685` |
| `v020c_vllm_quantized_office_negative` | `office_negative_guard` | `n/a` | `stability_fail` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `c8d043f62d59021ab0f98f167b1c2b555bf9010e6d01859fc2f2667e49385f62` |
| `v020c_vllm_quantized_baseline` | `full_v020c_baseline` | `9/2/5` | `baseline_completed` | `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b` | `fb2cf0f7aa0f34453f7d593db93af42bf529b97155fe91e3e155ee12017f5685` |
