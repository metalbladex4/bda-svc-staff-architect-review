# v020 Final Recommendation

## Outcome

The v020 goal-driven follow-up is closed as worktree-only learning evidence.
It improved the v019c baseline but did not reach the success target.

Recommended local incumbent:

- `v020c_v019c_extra_box_audit`
- `186` matches, `33` false negatives, `25` false positives
- controls passing: case `155`, case `166`, and
  `legacy_abstention_guard_office_negative`
- success target not reached: target was false negatives `<=25` and false
  positives `<=15`

Do not promote v020 as-is. Keep `v020c` as the best stable prompt-only learning
signal from this package. Exact replay `v020h` reproduced `v020c` at the same
`186 / 33 / 25` result, confirming that the gain is stable under the same
runtime and manifests.

## Comparison Matrix

| Candidate | Matches | FNs | FPs | Controls | Success | Note |
| --- | ---: | ---: | ---: | --- | --- | --- |
| `v019c_anchor_replay` | 174 | 45 | 28 | pass | no | anchor replay; matches v019c baseline |
| `v020a` | 177 | 42 | 67 | pass | no | recall up, FP explosion |
| `v020b` | 174 | 45 | 43 | pass | no | no recall gain; FP increase |
| `v020c` | 186 | 33 | 25 | pass | no | best stable balanced incumbent |
| `v020d` | 177 | 42 | 36 | pass | no | lost dense recall; FP increase |
| `v020e` | 168 | 51 | 40 | pass | no | lost recall; FP increase |
| `v020f` | 179 | 40 | 66 | pass | no | non-overlap wording caused tiling/FP explosion |
| `v020g` | 171 | 48 | 31 | pass | no | veto wording too blunt; lost dense recall |
| `v020h` | 186 | 33 | 25 | pass | no | exact v020c replay; reproduced incumbent |
| `v020i` | 172 | 47 | 30 | pass | no | scale-aware row wording collapsed case 67 |
| `v020j` | 168 | 51 | 43 | pass | no | single-target cleanup disturbed dense case 66 |
| `v020k` | 173 | 46 | 34 | pass | no | audit-only clarification still degraded case 67 |

## Dense-Case Closeout

`v020c` and the exact `v020h` replay both preserved the same dense-case profile:

| Case | Matches | FNs | FPs | Reading |
| --- | ---: | ---: | ---: | --- |
| `66` | 8 | 0 | 4 | full recall, still extra row boxes |
| `67` | 9 | 2 | 4 | major recovery versus v019c anchor |
| `84` | 8 | 5 | 0 | useful recall gain, still misses distant row vehicles |
| `97` | 1 | 0 | 2 | target found, but extra boxes remain |

Every later attempt to sharpen row, overlap, veto, scale, or single-target
cleanup disturbed the stable balance. The most important failure pattern is
that explicit cleanup language often collapses case `67` from `9` matches back
to `1` or `2` matches, and some variants create tiling or dense-row false
positive explosions.

## Recommendation

Keep `v020c` as the best v020 prompt-only evidence, but do not fold it into
runtime config, doctrine, source truth, or a promotion branch from this package.
The next productive step is no longer another near-neighbor prompt edit. Use
`v020c` as a stable diagnostic anchor and investigate non-prompt or
post-processing levers separately, especially duplicate/tiling suppression and
case-67-preserving dense-row behavior.

## Source Artifacts

- `comparison_matrix.json`
- `final_recommendation.json`
- `diagnoses/v020c_diagnosis.md`
- `diagnoses/v020h_diagnosis.md`
- `overlays/v020c_v019c_extra_box_audit.yaml`
- `runs/v020c/all_current_no101/human_report_challenge_v2_all_current_117_no101_2026-05-05_040218Z/upstream_code_manifest_run_summary.json`
- `runs/v020h/all_current_no101/human_report_challenge_v2_all_current_117_no101_2026-05-05_052931Z/upstream_code_manifest_run_summary.json`

## Limits

This package is local worktree evidence only. It does not approve runtime
adoption, source-truth edits, doctrine edits, prompt overlay edits, commits,
pushes, PRs, or Graphify/Mem0 source-truth claims.
