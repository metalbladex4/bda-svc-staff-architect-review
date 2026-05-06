# v019f_adversarial_box_jury Diagnosis

Generated: `2026-05-04T23:04:04.921274+00:00`

Verdict: `learning_only`

## Metrics

| Candidate | Matches | FNs | FPs | Delta vs v018e |
| --- | ---: | ---: | ---: | --- |
| `v019f_adversarial_box_jury` | 171 | 48 | 36 | -2 / 2 / 7 |

## Preserve

- kept 155, 166, and office-negative safe

## Avoid

- did not improve recall over the v018e anchor
- false positives still at or above the v018e pressure point
- dense formation recall remains weak
- dense/row false positives remain concentrated

## Next Axis

tighten final veto without losing full-image sweep
