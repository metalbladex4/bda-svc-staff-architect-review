# Surface Acceptance Decision

Decision: **F. vllm_qwen3vl_8b_fp8_red_do_not_resume**.

Do not resume autonomous semantic prompt refinement on v031.

Reasons:

- SGLang official FP8 launched, but case 67 failed at `0/11/1` for exact replay, warm replay, blank-line, trailing-space, and no-op probes.
- vLLM official FP8 launched and passed case-67 and sentinel stability.
- vLLM official FP8 failed the fresh v020c baseline acceptance gate: `180 / 39 / 32 / 71`.
- Case 155 regressed to `2/0/2`, while the old v020c surface had `2/0/0`.
- Office-negative passed as a negative-scene guard, but that does not override the red all-current/control result.

Next required fix before autonomy can continue: find an official or near-official Qwen serving surface that is both stable and behaviorally acceptable, or decide explicitly to treat vLLM FP8 as a separate model line with its own baseline and target.
