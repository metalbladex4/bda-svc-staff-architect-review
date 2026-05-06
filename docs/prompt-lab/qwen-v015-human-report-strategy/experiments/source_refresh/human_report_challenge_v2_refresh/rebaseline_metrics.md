# Human Report Challenge v2 Rebaseline Metrics

Status: `current_v2_baselines_complete`

Existing prediction JSONs were reused for unchanged cases; fresh v009/v014 baseline inference was run only for the ten updated/recovered report cases. No prompt-candidate inference was run.

| Candidate/run | Images | Matches | FNs | FPs | Negative scenes |
| --- | ---: | ---: | ---: | ---: | ---: |
| `v009_all_112_v2` | `112` | `162` | `57` | `53` | `0` |
| `v014_all_112_v2` | `112` | `149` | `70` | `23` | `0` |
| `v009_updated_report_10_v2` | `10` | `15` | `4` | `2` | `0` |
| `v014_updated_report_10_v2` | `10` | `13` | `6` | `2` | `0` |
| `v009_all_current_118_v2_adjusted` | `118` | `172` | `59` | `53` | `0` |
| `v014_all_current_118_v2_adjusted` | `118` | `157` | `74` | `24` | `0` |
| `v015e_hinge_v2` | `8` | `9` | `15` | `1` | `0` |
| `v015e_dev_v2` | `56` | `60` | `58` | `18` | `0` |
| `v016a_hinge_v2` | `12` | `26` | `31` | `34` | `0` |

## Current v2 Coverage

- `v009_all_current_118_v2_adjusted` covers `118` of `118` current v2 cases; missing: `none`
- `v014_all_current_118_v2_adjusted` covers `118` of `118` current v2 cases; missing: `none`
