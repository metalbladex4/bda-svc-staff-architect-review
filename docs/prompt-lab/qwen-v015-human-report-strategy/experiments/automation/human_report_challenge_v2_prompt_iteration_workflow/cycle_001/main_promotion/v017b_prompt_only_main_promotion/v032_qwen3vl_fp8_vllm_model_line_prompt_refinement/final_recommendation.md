# v032 Final Recommendation

Status: paused after runtime timeout during the first full all-current semantic-candidate run.

This tranche opened `qwen3-vl-8b-instruct-fp8-vllm` as a separate model-line prompt-engineering branch. It did not promote anything and did not treat FP8 vLLM as a replacement for the old product v020c prompt.

## Baselines

- Old/product v020c reference: `186 / 33 / 25 / 58`.
- FP8 vLLM model-line baseline: `180 / 39 / 32 / 71`.
- Near-term FP8 target: `<=58` combined errors.

## Candidate Outcome

No v032 candidate produced a complete all-current score or beat the FP8 baseline.

Completed micro-pack evidence:

- `v032a_fp8_context_fragment_precision_guard`: rejected no-op; rendered hash matched baseline.
- `v032b_fp8_real_context_fragment_precision_guard`: rejected; sentinel worsened to `39 / 10 / 16 / 26`.
- `v032c_fp8_compact_calibration`: rejected; sentinel worsened to `40 / 9 / 17 / 26`.
- `v032d_fp8_v019c_anchor_replay`: learning evidence only; sentinel `39 / 10 / 12 / 22`, but full all-current timed out on case 110 and is invalid/incomplete.

## Dense And Control Behavior

Baseline sentinel dense cases:

- Case 66: `8/0/5`.
- Case 67: `10/1/2`.
- Case 84: `9/4/0`.
- Case 97: `1/0/1`.

`v032d` improved some FP pressure, especially case 66 and case 155, but weakened case 67 and case 84 recall. That tradeoff is not acceptable without a complete all-current run.

Controls:

- Case 155 baseline was `2/0/2`; `v032d` fixed it to `2/0/0` on sentinel.
- Case 166 stayed `1/0/0` in completed micro runs.
- Office-negative passed in completed office guard runs. The helper's printed `stability_fail` label for office-negative is a known status-artifact caused by the case-67-only helper status rule, not an abstention failure.

## Decision

Keep FP8 as a separate model-line research branch, paused. Do not abandon it yet, because `v032d` found a plausible FP-reduction direction. Do not advance it either, because no semantic candidate completed all-current and the best signal is only micro-pack evidence.

Before more autonomous prompt candidates, fix or explicitly handle the case-110 full-run timeout and replay the relevant full pack cleanly.

## Boundaries

Hard boundaries were preserved: no promotion, no product config mutation, no doctrine/assessment/runtime/eval-truth mutation, no Graphify/Mem0 updates, and no v024o scored evidence.
