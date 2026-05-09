# v032 Pause Report: Runtime Timeout On Case 110

Pause reason: runtime/API timeout during `v032d_fp8_v019c_anchor_replay` full all-current.

The run had produced partial outputs but did not complete the pack. The result is invalid and unscored.

Trace file:

`runs/v032d_fp8_v019c_anchor_replay/full_all_current/human_report_challenge_v2_all_current_117_no101_2026-05-08_233834Z/traces/human-report-110.json`

Exception:

`APITimeoutError('Request timed out.')`

Resume recommendation:

1. Confirm the vLLM FP8 backend is healthy.
2. Decide whether to increase the experiment-only client timeout or add a safe retry wrapper for full-pack runs.
3. Rerun a clean full all-current for either exact FP8 baseline or `v032d` before authoring another semantic prompt.
4. Do not score partial outputs.
