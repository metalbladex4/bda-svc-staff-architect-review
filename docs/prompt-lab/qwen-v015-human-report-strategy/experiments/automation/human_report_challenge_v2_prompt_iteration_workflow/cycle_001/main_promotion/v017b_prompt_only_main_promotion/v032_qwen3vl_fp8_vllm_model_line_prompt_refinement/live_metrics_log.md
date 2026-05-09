
## v032_baseline_exact_v020c_fp8_replay

- backend: `vllm_qwen3vl_8b_fp8_local_8000`
- stage: `baseline_sentinel_replay`
- metrics: `42/7/15/22`
- case 67: `10/1/2`
- rendered prompt hash: `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b`
- request shape hash: `2f6019492aea6726860a6d34acaa49020c4f8c47d740ab973640a4b5efc2f6c1`
- status: `stability_pass`

## v032a_fp8_context_fragment_precision_guard

- backend: `vllm_qwen3vl_8b_fp8_local_8000`
- stage: `micro_pack_only`
- metrics: `42/7/15/22`
- case 67: `10/1/2`
- rendered prompt hash: `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b`
- request shape hash: `2f6019492aea6726860a6d34acaa49020c4f8c47d740ab973640a4b5efc2f6c1`
- status: `stability_pass`

## v032a_fp8_context_fragment_precision_guard

- backend: `vllm_qwen3vl_8b_fp8_local_8000`
- stage: `office_negative_guard`
- metrics: `1/0/0/0`
- case 67: `n/a`
- rendered prompt hash: `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b`
- request shape hash: `c02a2fe43bacbb1c90c200add7eb4c25bcb3460920858e9ae063da1b25661fc4`
- status: `stability_fail`

## v032b_fp8_real_context_fragment_precision_guard

- backend: `vllm_qwen3vl_8b_fp8_local_8000`
- stage: `micro_pack_only`
- metrics: `39/10/16/26`
- case 67: `10/1/2`
- rendered prompt hash: `0cd29a82d8c002e540ba8c5d61238eb6689ddba69bdbccb1ea1cc45d0da6d015`
- request shape hash: `84af36c07e16c484125dc780e4e5ffcd94dbe3e0601c8c5dbf3326164907ef0e`
- status: `stability_pass`

## v032b_fp8_real_context_fragment_precision_guard

- backend: `vllm_qwen3vl_8b_fp8_local_8000`
- stage: `office_negative_guard`
- metrics: `1/0/0/0`
- case 67: `n/a`
- rendered prompt hash: `0cd29a82d8c002e540ba8c5d61238eb6689ddba69bdbccb1ea1cc45d0da6d015`
- request shape hash: `ce85c32c24d798c7bfe74811d504d04595d6ceb62afb6cd476f8d15340b9967e`
- status: `stability_fail`

## v032c_fp8_compact_calibration

- backend: `vllm_qwen3vl_8b_fp8_local_8000`
- stage: `micro_pack_only`
- metrics: `40/9/17/26`
- case 67: `10/1/2`
- rendered prompt hash: `3266b2143aa47026c45f62d5498e966f8b9d8d90cd38346afe9a01471c97e41b`
- request shape hash: `b3db2f38e9e06e0cf81de547d5ca97bace146f5f94a90edd1e09bb9e98b93bb1`
- status: `stability_pass`

## v032c_fp8_compact_calibration

- backend: `vllm_qwen3vl_8b_fp8_local_8000`
- stage: `office_negative_guard`
- metrics: `1/0/0/0`
- case 67: `n/a`
- rendered prompt hash: `3266b2143aa47026c45f62d5498e966f8b9d8d90cd38346afe9a01471c97e41b`
- request shape hash: `8cde55e2748d373a943a49cabedb7f8af380d50ba34009880e5170fe460309af`
- status: `stability_fail`

## v032d_fp8_v019c_anchor_replay

- backend: `vllm_qwen3vl_8b_fp8_local_8000`
- stage: `micro_pack_only`
- metrics: `39/10/12/22`
- case 67: `8/3/2`
- rendered prompt hash: `aeff2baeecf7f47b14114280c26b853d072172f883e5ed495dbdbf609c4af72f`
- request shape hash: `5dae1eea84303081acbbe463b67865834928354dace58c391683e2ce6c1f73d3`
- status: `stability_pass`

## v032d_fp8_v019c_anchor_replay

- backend: `vllm_qwen3vl_8b_fp8_local_8000`
- stage: `office_negative_guard`
- metrics: `1/0/0/0`
- case 67: `n/a`
- rendered prompt hash: `aeff2baeecf7f47b14114280c26b853d072172f883e5ed495dbdbf609c4af72f`
- request shape hash: `c866d9f09a1e6baad12821265a633f6ad388b060b26f4564c5cd52e10eb4259d`
- status: `stability_fail`

=== V032 CANDIDATE COMPLETE ===
candidate: v032d_fp8_v019c_anchor_replay
backend: vllm_qwen3vl_8b_fp8
stage: micro_pack_only_full_all_current_incomplete
matches: 39
false_negatives: 10
false_positives: 12
combined_errors: 22
vs_fp8_baseline_delta: n/a micro-pack; full incomplete
vs_old_v020c_58_delta: n/a micro-pack; full incomplete
case_67: 8/3/2
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: learning_evidence
main_lesson: v019c anchor reduced FP pressure and fixed case 155 on sentinel, but weakened dense recall and timed out during full all-current.
next_axis: Pause semantic iteration and resolve full-run timeout before more prompt work.
===============================
