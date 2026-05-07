# v027 Runtime Rendering Stability Gate

This package tests whether the Qwen prompt-evaluation surface is stable enough
to resume semantic prompt refinement after the v026 runtime-shape pause.

The package is evidence-only until the stability gate passes. It instruments
scratch `upstream/main` runs to capture rendered prompt hashes, overlay
application state, sanitized request-shape hashes, image serialization hashes,
raw response traces, JSON repair/validation outcomes, and eval summaries.

## Current Boundary

- Product incumbent remains `v020c_anchor_replay` / `v020c_extra_box_audit`:
  `186` matches / `33` FNs / `25` FPs / `58` errors.
- `v024l_v023s_no_wheel_track_ablation` remains high-recall learning evidence
  only: `188 / 31 / 35 / 66`.
- `v025a_v020c_compact_separate_body_recovery` remains rejected:
  `176 / 43 / 35 / 78`.
- `v024o` remains partial/unscored and forbidden as scored evidence.
- No semantic prompt candidate may be authored unless Stage 1 and Stage 2
  stability gates pass.

## Gate Design

Stage 1 probes case `67` only: exact `v020c` replay repeats, blank-line probes,
trailing-space probe, and no-op template roundtrip.

Stage 2, if Stage 1 passes, probes the sentinel micro-pack:
`12, 14, 16, 42, 66, 67, 77, 84, 88, 90, 97, 103, 155, 166, 172`.

The safer hypothesis is not that a blank line semantically broke Qwen. The
safer hypothesis is that the fallback evaluation path may be unstable or
under-instrumented enough that prompt-quality attribution is unsafe.
