# v025 Final Recommendation

Review timestamp: `2026-05-07T01:26:05+00:00`

## Status

`v025a_v020c_compact_separate_body_recovery` has been authored and evaluated as a single-candidate evidence wave.

## Current Recommendation

- Keep `v020c_anchor_replay` / `v020c_extra_box_audit` as the Qwen incumbent.
- Reject `v025a_v020c_compact_separate_body_recovery` for this wave because it collapses case `67` below the v020c baseline.
- Treat `v024l_v023s_no_wheel_track_ablation` as high-recall learning evidence only.
- Do not branch from `v024l`.
- Do not use `v024o` unless it is rerun from scratch.
- Do not attempt another positive separate-body cue in the audit/final-balance region.
- Do not author `v025b` until the prompt delta autopsy and case `67` collapse autopsy are reviewed.

## v025a Result

| Candidate | Matches | FNs | FPs | Errors | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| `v020c_anchor_replay` | 186 | 33 | 25 | 58 | incumbent |
| `v024l_v023s_no_wheel_track_ablation` | 188 | 31 | 35 | 66 | learning evidence |
| `v025a_v020c_compact_separate_body_recovery` | 176 | 43 | 35 | 78 | rejected |

## Boundary

No source truth, doctrine, assessment prompt, runtime code, eval ground truth, Graphify refresh, Mem0 write, promotion, or `v025b` authoring is adopted by this package.

## Autopsy Decision

The exact v025a delta was one added sentence inside `EXTRA-BOX AUDIT`. That
sentence likely made the final audit act like a split-recovery instruction
instead of a pure extra-box rejection gate. The next candidate, if later
approved, must be decided from the autopsy rather than from the original v025a
hypothesis.

Recommended next direction:

```text
D. Run a targeted replay/micro-ablation pack before all-current.
```
