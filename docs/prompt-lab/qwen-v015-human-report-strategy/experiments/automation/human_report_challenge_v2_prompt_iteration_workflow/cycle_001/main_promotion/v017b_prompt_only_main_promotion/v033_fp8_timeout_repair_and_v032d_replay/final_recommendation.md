# v033 Final Recommendation

Generated: `2026-05-09T01:30:05Z`

Status: **rejected**.

v033 successfully repaired the v032 full-run timeout path with experiment-only instrumentation. Case 110 completed for both the FP8 baseline and `v032d_fp8_v019c_anchor_replay` under the documented 180-second request timeout. The clean full replay completed all `117` all-current/no101 images with no retries.

## v032d Clean Full Replay

- Full metrics: `185 / 34 / 57 / 91`.
- FP8 baseline reference: `180 / 39 / 32 / 71`.
- Delta vs FP8 baseline: `+5` matches, `-5` FNs, `+25` FPs, `+20` combined errors.
- Old/product v020c reference remains: `186 / 33 / 25 / 58`.

## Key Cases

- Case 67: `8/3/2`.
- Case 155: `2/0/0`; the v032d micro-pack FP fix held.
- Case 166: `1/0/0`.
- Office-negative: pass.
- Case 110: `3/4/32`; v032d completed but produced severe FP explosion.

## Decision

`v032d` does **not** become the new FP8 working best. It improved recall but reopened too many false positives and worsened combined error from `71` to `91`.

Autonomous FP8 prompt refinement did **not** resume. The next candidate axis must be reviewed from this evidence; do not continue from v032d as the working prompt.

Hard boundaries were preserved: no promotion, no product source truth/runtime/doctrine/assessment/eval-truth mutation, no Graphify/Mem0 update, and no v024o scored evidence.
