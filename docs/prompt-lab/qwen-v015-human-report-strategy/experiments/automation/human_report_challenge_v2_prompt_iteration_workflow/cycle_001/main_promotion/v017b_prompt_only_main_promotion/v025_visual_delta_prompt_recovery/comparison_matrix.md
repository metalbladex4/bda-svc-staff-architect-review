# v025 Source Comparison Matrix

No new inference was run for this package. The rows below are source rows from
`v023_literal99_qwen_no_stop_continuation`.

| Candidate | Role | Matches | FNs | FPs | Errors | 155 | 166 | Office | v025 status |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| `v020c_anchor_replay` | incumbent | 186 | 33 | 25 | 58 | pass | pass | pass | base incumbent |
| `v024l_v023s_no_wheel_track_ablation` | high-recall learning evidence | 188 | 31 | 35 | 66 | pass | pass | pass | review-only challenger |
| `v024o_v024l_intact_building_piece_exclusion` | interrupted partial | n/a | n/a | n/a | n/a | n/a | n/a | office only | excluded; not scored |

## Priority Delta

| Case | v020c | v024l | Delta | Category |
| --- | --- | --- | --- | --- |
| `12` | `1/0/0` | `1/0/1` | `+0/+0/+1` | added FP |
| `14` | `1/1/0` | `2/0/0` | `+1/-1/+0` | recovered FN |
| `16` | `1/0/0` | `1/0/2` | `+0/+0/+2` | added FP |
| `21` | `3/0/0` | `2/1/0` | `-1/+1/+0` | recall regression |
| `42` | `1/1/0` | `2/0/0` | `+1/-1/+0` | recovered FN |
| `66` | `8/0/4` | `8/0/6` | `+0/+0/+2` | dense added FP |
| `67` | `9/2/4` | `9/2/3` | `+0/+0/-1` | dense sentinel |
| `76` | `2/1/0` | `1/2/0` | `-1/+1/+0` | recall regression |
| `77` | `1/0/0` | `1/0/1` | `+0/+0/+1` | added FP |
| `84` | `8/5/0` | `7/6/0` | `-1/+1/+0` | dense recall regression |
| `88` | `1/0/0` | `1/0/1` | `+0/+0/+1` | added FP |
| `90` | `1/0/0` | `1/0/1` | `+0/+0/+1` | added FP |
| `97` | `1/0/2` | `1/0/2` | `+0/+0/+0` | unchanged FP burden |
| `103` | `1/0/1` | `1/0/4` | `+0/+0/+3` | added FP |
| `155` | `2/0/0` | `2/0/0` | `+0/+0/+0` | positive control |
| `164` | `1/1/0` | `2/0/0` | `+1/-1/+0` | recovered FN |
| `166` | `1/0/0` | `1/0/0` | `+0/+0/+0` | positive control |
| `172` | `1/2/0` | `3/0/0` | `+2/-2/+0` | recovered FN |
