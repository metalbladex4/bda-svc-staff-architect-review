# v026 Strategy State

Updated: `2026-05-07T06:01:04Z`

- product incumbent: `v020c_anchor_replay`
- tranche working best: `v020c_anchor_replay`
- status: `paused_runtime_shape_sensitivity`
- target met: `false`
- backend used: `ollama_openai_compat_fallback_11434`
- preferred backend: `http://localhost:8000/v1` remained unavailable
- last completed candidate: `v026q_blank_line_shape_probe`
- last candidate status: `rejected`
- last candidate micro metrics: `29/20/16`, case `67` at `1/10/9`
- fresh exact-v020c sentinel check: `38/11/11`, case `67` at `9/2/4`

## Current Working Best

`v020c_anchor_replay` remains the working best and product incumbent at
`186/33/25/58`.

## What Failed

Every rendered v026 prompt delta failed the sentinel gate. The failures were not
limited to positive split cues or bad-box cleanup language:

- audit-region negative lock
- opening grounding header
- low-salience separate-body cue
- actual tight-box occupancy guard
- calibration paragraph removal
- final-balance version-label removal
- tight-box phrase rewrite
- adjacent background-object guard
- compact Qwen-style rewrite
- target-guidance ordering ablation
- dense-row protective cue
- output-only suffix cue
- quadrant search-order cue
- blank-line-only prompt-shape probe

## What Worked

Exact v020c prompt bytes stayed stable:

- initial v020c sentinel baseline: `38/11/11`, case `67` at `9/2/4`
- fresh v020c sentinel check after v026q: `38/11/11`, case `67` at `9/2/4`
- no-op/exact-replay overlays (`v026a`, `v026c`, `v026f`) reproduced full
  `186/33/25/58`

## Next Axis

Do not author another v026 prompt candidate on the fallback endpoint by default.

Recommended next step:

1. Restore or start the preferred `http://localhost:8000/v1` backend and replay
   exact v020c plus a no-semantics shape probe.
2. If the preferred backend is stable, resume candidate authoring there.
3. If the preferred backend cannot be restored, ask whether to continue random
   micro-search on the fallback endpoint or pivot to visual-review/post-processing
   diagnostics as prompt-engineering support.

## Hard Lesson

On the fallback endpoint, v020c is a brittle exact-prompt attractor. A blank-line
only change caused the same case-67 collapse family as semantic prompt edits.
