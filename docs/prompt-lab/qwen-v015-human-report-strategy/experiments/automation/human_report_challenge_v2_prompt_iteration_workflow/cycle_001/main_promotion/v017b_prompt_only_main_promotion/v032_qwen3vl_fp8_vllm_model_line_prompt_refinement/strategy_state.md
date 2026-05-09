# v032 Strategy State

Current product incumbent: old `v020c_anchor_replay / v020c_extra_box_audit` under prior evidence, `186 / 33 / 25 / 58`.

Current FP8 model-line working best: `v020c_fp8_vllm_baseline`, `180 / 39 / 32 / 71` from v031 full all-current.

Best completed v032 evidence: sentinel micro-pack only. No v032 semantic candidate produced a valid full all-current score.

What worked:
- vLLM FP8 endpoint stayed available for baseline and micro-pack runs.
- Rendered-prompt and request-shape hashes were captured.
- Office-negative, case 166, and case 67 remained stable in completed micro runs.
- `v032d` reduced sentinel FPs and fixed case 155, though with recall tradeoffs.

What failed:
- `v032a` was an unintended no-op.
- `v032b` and `v032c` worsened sentinel errors.
- `v032d` full all-current timed out on case 110 and is unscored.

Next axis after runtime recovery:
- First, resolve the full-run timeout/retry policy and replay `v032d` or exact FP8 baseline full enough to verify runtime robustness.
- Only after a complete full run, consider a small v019c/v020c hybrid that tries to preserve v020c dense recall while removing the FP8 case-155 FP pressure.
