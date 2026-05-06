# v018a Dense Smoke Gate Summary

Status: `failed_challenger_precision_rebound`

Generated: `2026-05-04T00:42:13.950076+00:00`

## Result

`v018a_dense_formation_body_center_anchor` is learning evidence only. It should
not replace the parked `v017b_group_box_rejection` promotion candidate.

The candidate passed the minimal formal smoke gate, but it did so at the false
positive ceiling and materially regressed against `v017b` on the same no-101
hinge scope.

## Metrics

| Candidate / Pack | Matches | FNs | FPs | Readout |
| --- | ---: | ---: | ---: | --- |
| `v017b` hinge12 minus `101` | 23 | 22 | 13 | parked primary baseline |
| `v017d` hinge11 | 22 | 23 | 13 | visual-anchor comparator |
| `v017f` hinge11 | 23 | 22 | 17 | recall comparator |
| `v018a` hinge11 | 22 | 23 | 21 | failed challenger; FP rebound |

Compared with parked `v017b`, `v018a` changed matches by
`-1`, false negatives by
`1`, and false positives by
`+8`.

## Dense Cases

| Case | v017b | v017d | v017f | v018a | Readout |
| --- | --- | --- | --- | --- | --- |
| `66` | `8/0/4` | `7/1/3` | `8/0/6` | `7/1/8` | v018a over-enumerates badly |
| `67` | `1/10/9` | `1/10/8` | `1/10/9` | `1/10/10` | no recall gain; more FPs |
| `84` | `5/8/0` | `5/8/2` | `5/8/0` | `4/9/3` | v018a loses one match and adds FPs |

Numbers in dense-case cells are `matches/FNs/FPs`.

## Controls

- Positive `155`: passed with `2` matches, `0` FNs, `0` FPs.
- Office-negative abstention: passed with `0` negative-scene false positives.

## Decision

Do not promote or deepen `v018a`. Do not run dev, holdout, or all-current for
this candidate. Keep `v017b_group_box_rejection` parked as the primary prompt
candidate. Preserve `v018a` as evidence that body-center/ground-contact wording
caused a false-positive rebound instead of solving case `67`.
