# v032 Runtime Timeout Diagnosis

Generated: `2026-05-09T00:08:00Z`

Failure point: v032d full all-current run timed out on case 110.

Trace: `runs/v032d_fp8_v019c_anchor_replay/full_all_current/human_report_challenge_v2_all_current_117_no101_2026-05-08_233834Z/traces/human-report-110.json`.

Exception: `APITimeoutError('Request timed out.')`.

Request evidence: response trace was captured before timeout. Request-shape hash was `7cabc25fc47dbcb6b16829f02547195f593d710d8741afa9c492ca5ff902fcde`; rendered prompt/user prompt hash was `aeff2baeecf7f47b14114280c26b853d072172f883e5ed495dbdbf609c4af72f`; response text and response hash are unavailable because the API request timed out.

Interpretation: this is not a scored prompt failure. It is an incomplete evaluation run. The backend endpoint remained responsive afterward, so the immediate issue is a per-request/full-run timeout rather than a confirmed backend crash.

Stop rule: because the all-current run did not complete, autonomous prompt refinement must pause rather than continue to new candidates from partial full-pack evidence.

Recommended next action: add a resume-safe timeout policy or rerun v032d full after confirming backend capacity and timeout settings. Do not score partial outputs.
