# v029 New Backend v020c Baseline

Backend: `vllm_quantized_qwen3_vl_8b_local_8000`

Actual model root: `SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16`

Served model name: `Qwen/Qwen3-VL-8B-Instruct`

## All-Current

- pack: `human_report_challenge_v2_all_current_117_no101`
- image_count: `117`
- case 101 present: `False`
- metrics: `153 / 66 / 25 / 91`
- old v020c baseline: `186 / 33 / 25 / 58`
- combined-error delta: `+33`

## Controls And Sentinels

- case 67: `9/2/5`
- case 155: `2/0/0`
- case 166: `1/0/0`
- office-negative image_count: `1`
- office-negative passed: `True`

## Decision

The backend passed stability, but the fresh v020c baseline is too weak for autonomous prompt refinement. The combined error is `91`, which is `+33` over the old v020c baseline and exceeds the user-defined pause threshold of `+20`.
