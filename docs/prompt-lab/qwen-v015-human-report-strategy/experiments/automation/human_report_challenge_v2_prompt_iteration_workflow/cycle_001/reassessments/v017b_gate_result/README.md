# v017b Gate Result Reassessment

Status: `old_gate_near_miss_case101_now_diagnostic_only`

This package records the required post-run diagnosis for
`v017b_single_target_box_span_self_filter`. It exists because the automation
contract requires a diagnosis artifact after a failed or near-miss candidate
before any next prompt is authored.

## Source Artifacts

- v017b live run summary:
  `../../runs/v017b/live_2026-05-03_032920Z/candidate_cycle_live_run_summary.json`
- v017b gate summary:
  `../../runs/v017b/live_2026-05-03_032920Z/gate_check_candidate_summary.json`
- v017b decision packet:
  `../../runs/v017b/live_2026-05-03_032920Z/decision_packet.md`
- case `101` prediction:
  `../../runs/v017b/live_2026-05-03_032920Z/human_report_challenge_v2_hinge_12_2026-05-03_032920Z/predicted/101_2026-05-03_032933Z.json`

## Outcome

Under the old 12-case gate, `v017b` was a near miss, not a winner. It improved
the aggregate hinge totals and kept the important v2 controls, but it did not
solve the `101` broad-box blocker.
The model still emitted one broad military-equipment box:

```text
[75, 58, 1000, 547]
```

After user direction, case `101` is removed from forward pass/fail evaluation
and retained as diagnostic-only evidence. This package remains historical
diagnosis for the old gate; it should not block `v017c` through `v017f` unless a
future run fails a hard stop such as abstention, source integrity, scope, or
tool-boundary safety.
