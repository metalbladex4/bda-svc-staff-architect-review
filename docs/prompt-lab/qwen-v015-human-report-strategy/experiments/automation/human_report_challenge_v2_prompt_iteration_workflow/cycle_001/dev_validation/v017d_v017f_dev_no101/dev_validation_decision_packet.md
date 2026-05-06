# v017d/v017f Dev Validation Decision Packet

- mode: `bounded_dev_validation`
- pack: `human-report-challenge-v2-dev-55-no101`
- primary candidate: `v017d_visual_anchor_lock`
- comparator: `v017f_compact_visual_anchor_balance`
- recommendation: `v017d_remains_primary`
- comparator note: `v017f_recall_advantage`

## Metrics

| Candidate/baseline | Images | Matches | FNs | FPs | 155 matches |
| --- | ---: | ---: | ---: | ---: | ---: |
| `v009 adjusted baseline` | `55` | `74` | `32` | `27` | `n/a` |
| `v014 adjusted baseline` | `55` | `69` | `37` | `17` | `n/a` |
| `v015e dev baseline` | `55` | `59` | `47` | `18` | `n/a` |
| `v017d primary` | `55` | `72` | `34` | `16` | `2` |
| `v017f comparator` | `55` | `73` | `33` | `18` | `2` |

## Readout

- `101` is not in this forward dev split; it remains diagnostic-only.
- `166` is absent and remains holdout-only.
- `155` remains a positive-control case.
- This validation does not promote a candidate or adopt runtime config.
- Focused visual review: `visual_review/v017d_dev_outlier_visual_review.md`
