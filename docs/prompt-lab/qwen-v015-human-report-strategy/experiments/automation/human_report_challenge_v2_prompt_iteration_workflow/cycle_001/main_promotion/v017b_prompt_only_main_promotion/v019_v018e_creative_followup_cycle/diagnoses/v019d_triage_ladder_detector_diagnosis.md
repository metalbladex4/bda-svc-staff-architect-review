# v019d_triage_ladder_detector Diagnosis

Generated: `2026-05-04T22:34:51.422590+00:00`

Verdict: `learning_only`

## Metrics

| Candidate | Matches | FNs | FPs | Delta vs v018e |
| --- | ---: | ---: | ---: | --- |
| `v019d_triage_ladder_detector` | 175 | 44 | 48 | 2 / -2 / 19 |

## Preserve

- kept 155, 166, and office-negative safe
- improved recall over the v018e anchor

## Avoid

- false positives still at or above the v018e pressure point
- dense formation recall remains weak
- dense/row false positives remain concentrated

## Next Axis

tighten final veto without losing full-image sweep
