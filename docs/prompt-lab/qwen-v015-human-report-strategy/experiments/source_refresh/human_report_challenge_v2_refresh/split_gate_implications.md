# Human Report Challenge v2 Split And Gate Implications

Status: `v1_gates_invalid_for_future_automation`

- Remove protected-negative semantics for `155` and `166`.
- Treat `155` as a positive dev/hinge diagnostic if selected.
- Treat `166` as a positive holdout-only diagnostic unless separately approved.
- Replace old protected no-object gates with v2 positive-control checks plus a separate non-human-report negative guard if needed.
- Future automation manifests must point to `human_report_challenge_v2`.
- Current v2 includes recovered report additions `40`, `65`, `106`, `125`, `172`, and `187` without moving source images.
- Fresh v009/v014 changed-report baselines now cover the ten latest updated/recovered cases.
- Autonomous prompt-cycle runs remain paused for user approval and v017b authorization, not for missing recovered-addition baselines.
