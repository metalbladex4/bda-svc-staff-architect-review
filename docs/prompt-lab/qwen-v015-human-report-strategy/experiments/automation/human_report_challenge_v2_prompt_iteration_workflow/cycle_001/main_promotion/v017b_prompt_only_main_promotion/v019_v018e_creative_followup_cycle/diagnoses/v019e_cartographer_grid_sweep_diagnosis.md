# v019e_cartographer_grid_sweep Diagnosis

Generated: `2026-05-04T22:49:26.733315+00:00`

Verdict: `learning_only`

## Metrics

| Candidate | Matches | FNs | FPs | Delta vs v018e |
| --- | ---: | ---: | ---: | --- |
| `v019e_cartographer_grid_sweep` | 177 | 42 | 31 | 4 / -4 / 2 |

## Preserve

- kept 155, 166, and office-negative safe
- improved recall over the v018e anchor

## Avoid

- false positives still at or above the v018e pressure point
- dense formation recall remains weak

## Next Axis

tighten final veto without losing full-image sweep
