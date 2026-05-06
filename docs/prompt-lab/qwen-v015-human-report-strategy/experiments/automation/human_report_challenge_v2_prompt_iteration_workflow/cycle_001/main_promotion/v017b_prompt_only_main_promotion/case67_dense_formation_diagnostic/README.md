# Case 67 Dense-Formation Diagnostic

Status: `diagnostic_complete`

Generated: `2026-05-03T23:57:07Z`

This diagnostic records why case `67` remains a hard dev/no101 outlier after
the v017 candidate cycle and after `v017b_group_box_rejection` became the
parked prompt-only main promotion candidate.

It is a source-grounded diagnosis package only:

- no prompt authored
- no VLM inference run
- no dev, holdout, or all-current run
- no source report, reference truth, or evaluation data mutation
- no runtime config change
- no commit or remote push

## Finding

Case `67` is not mainly a `v017b` regression and it is not the same failure as
the old case `101` broad group/scene-box issue. It is a dense-formation,
perspective, smoke/dust, and tiny-target anchoring problem.

The source report contains `11` no-damage military-equipment references in a
receding row. The first seven references are very small `possible` objects;
the next two are small `probable` objects; the final two are larger
`confirmed` objects. Across the fresh same-image comparison set, every
candidate matches only `1` of the `11` references and misses `10`.

| Candidate | TP | FN | FP | Readout |
| --- | ---: | ---: | ---: | --- |
| `v009_control_baseline` | 1 | 10 | 12 | oldest control, highest FP count |
| `v014_weighted_building_selection` | 1 | 10 | 8 | same recall failure, lower FP |
| `v015e_individual_body_evidence` | 1 | 10 | 10 | no recall gain |
| `v016a_reference_aware_candidate_discovery` | 1 | 10 | 9 | no recall gain |
| `v017a_broad_group_box_lock` | 1 | 10 | 9 | no recall gain |
| `v017b_group_box_rejection` | 1 | 10 | 9 | parked primary; does not solve case 67 |
| `v017c_count_then_anchor` | 1 | 10 | 9 | no recall gain |
| `v017d_visual_anchor_lock` | 1 | 10 | 8 | fewer predictions, not a true solve |
| `v017e_anti_span_guard` | 1 | 10 | 10 | no recall gain |
| `v017f_compact_visual_anchor_balance` | 1 | 10 | 9 | no recall gain |

Visual review of the existing bbox overlays shows that the red predictions
mostly follow dust/smoke/top-edge row cues rather than the visible target body
centers. `v017d` reduces one false positive relative to `v017b`, but its small
row predictions are also displaced from the reference bodies; it wins one FP
by being shorter, not by fixing the anchoring behavior.

## Decision Impact

This package does not reopen the accepted `v017b` promotion recommendation by
itself. Case `67` should be treated as a known limitation of the current
prompt-only lane rather than proof that `v017d` should replace `v017b`.

If the next prompt-only cycle is authorized later, the narrow v018 axis should
be dense-formation body-center anchoring under smoke/dust and perspective:

- prefer boxes grounded on visible vehicle body evidence
- reject boxes that mainly cover dust, plume, sky, rowline, or top-edge cues
- avoid evenly spaced placeholder candidates
- preserve real separate-body recall when targets are visibly countable

No v018 prompt text is authored here.

## Artifacts

- `case67_dense_formation_diagnostic.md`
- `case67_dense_formation_diagnostic.json`
- `source_manifest.json`
