# v017d/v017f Dense Formation Visual Comparison

Status: `comparison_complete`

This package compares `v017d_visual_anchor_lock` and
`v017f_compact_visual_anchor_balance` on the three dense-formation cases that
dominate the remaining `v017d` dev errors: `66`, `67`, and `84`.

## Scope

- Split: `human_report_challenge_v2_dev_55_no101`
- Candidates:
  - `v017d_visual_anchor_lock`
  - `v017f_compact_visual_anchor_balance`
- Cases: `66`, `67`, `84`
- Mode: visual comparison only

No prompt was authored, no inference was run, no source truth changed, no
reference truth changed, and no promotion decision was made.

## Result

`v017f` does not solve the dense-formation failure surface. Across `66`, `67`,
and `84`, both candidates produce `33` total error units:

| Case | v017d | v017f | Readout |
| --- | --- | --- | --- |
| `66` | `8` matches, `0` FNs, `6` FPs | `8` matches, `0` FNs, `6` FPs | unchanged dense-row over-enumeration |
| `67` | `1` match, `10` FNs, `8` FPs | `1` match, `10` FNs, `9` FPs | v017f adds one FP, no recall gain |
| `84` | `5` matches, `8` FNs, `1` FP | `5` matches, `8` FNs, `0` FPs | v017f removes one FP, but recall remains stuck |

The global v017f recall advantage therefore does not come from fixing the
dense-formation blocker. It is not a better primary candidate for this failure
surface.

## Recommendation

Keep `v017d_visual_anchor_lock` as the main candidate. If another prompt attempt
is authorized, the narrow axis should be dense-formation anchor discipline:

- keep real separate-body recall
- reject row/stripe/span boxes
- reject unsupported evenly spaced placeholders
- suppress duplicate or extra row candidates after an initial candidate pass

Do not choose `v017f` as primary merely because its aggregate dev score has one
additional match.

Details:

- `v017d_v017f_dense_formation_visual_comparison.md`
- `v017d_v017f_dense_formation_visual_comparison.json`
- `source_manifest.json`
