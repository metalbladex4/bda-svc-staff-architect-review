# v033 v032d Clean Replay Diagnosis

Generated: `2026-05-09T01:30:05Z`

What this tested: whether `v032d_fp8_v019c_anchor_replay` could be scored cleanly after repairing the case-110 timeout, and whether its micro-pack FP gains held on all-current.

Retry policy result: case 110 completed for both FP8 baseline and v032d under the experiment-only 180-second timeout. The full v032d replay completed all `117` images with `0` retry attempts.

Full metrics: `185 / 34 / 57 / 91`.

Compared with FP8 baseline `180 / 39 / 32 / 71`, v032d improved recall by `5` FNs but added `25` FPs, worsening combined error by `20`.

Dense/control cases:

- Case 67: `8/3/2`; within the minimum v033 gate but weaker than FP8 baseline's v032 sentinel `10/1/2`.
- Case 155: `2/0/0`; the micro-pack FP fix held.
- Case 166: `1/0/0`; passed.
- Office-negative: pass.
- Case 110: `3/4/32`; severe FP explosion.

Decision: rejected. v032d is validly scored now, but it is not a new FP8 working best and autonomous prompt refinement does not resume.

Lesson: removing the v020c extra-box audit can improve selected FP controls such as case 155, but on FP8 vLLM it opens a broad false-positive failure class across full all-current.
