# v032d Diagnosis

Generated: `2026-05-09T00:09:09Z`

What this tested: replaying the earlier v019c anchor prompt on the FP8 vLLM model line to see whether removing the v020c extra-box audit region improves FP8-specific FP behavior.

What changed from FP8 working best: replaced the v020c prompt with the v019c anchor prompt. Rendered prompt hash changed to `aeff2baeecf7f47b14114280c26b853d072172f883e5ed495dbdbf609c4af72f`.

Micro-pack metrics: sentinel `39 / 10 / 12 / 22` versus baseline sentinel `42 / 7 / 15 / 22`. It matched baseline micro total errors but shifted the balance: case 66 improved from `n/a` to `n/a`, case 155 improved from `n/a` to `n/a`, but case 67 weakened from `10/1/2` to `8/3/2` and case 84 worsened from `n/a` to `n/a`. Case 166 stayed `n/a`. Office-negative passed.

Full all-current status: invalid/incomplete. The run timed out on case 110 before pack completion. The timeout trace is `runs/v032d_fp8_v019c_anchor_replay/full_all_current/human_report_challenge_v2_all_current_117_no101_2026-05-08_233834Z/traces/human-report-110.json`. The exception was `APITimeoutError('Request timed out.')`. No all-current score is recorded for v032d.

Decision: learning evidence only, not a new working best. It is a useful FP/recall tradeoff probe but cannot be advanced without rerunning or hardening the runtime timeout path.

Likely load-bearing change: removing the v020c extra-box audit reduces some FP pressure, especially case 155, but weakens dense recall/case-67 margin.

Lesson type: model-surface-specific plus runtime artifact. The micro-pack signal is real; the full-pack outcome is blocked by runtime timeout.

Next hypothesis: pause autonomy, diagnose/mitigate full-run timeout handling, then consider a v019c/v020c hybrid only if a clean full replay is possible.
