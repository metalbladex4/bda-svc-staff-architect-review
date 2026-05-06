# v017c Candidate Brief

Status: `authored_for_bounded_live_gate_run`

## Purpose

Test an evidence-named finalization interface after case `101` was moved to
diagnostic-only status. The candidate keeps `v017b` single-target discipline but
requires each final detection to be backed by silently named visible body
evidence before it survives into JSON.

## Dependency

Depends on the `v017b` old-gate near-miss diagnosis and the active
`human_report_challenge_v2_hinge_11_no101` gate.

## Prompt Axis

- discover candidates across the full image
- silently name the visible connected body evidence
- reject candidates whose evidence is only region/context/row/group/fragment
- finalize only tight single-target boxes
- retain the office-negative abstention guard

## Boundaries

- Use `human_report_challenge_v2` only.
- Do not use `human_report_challenge_v1` as current gate authority.
- Do not treat `155` or `166` as protected negatives.
- Keep `166` holdout-only unless the user separately approves moving it.
- Preserve placeholders: `{categories}, {detection_guidance}, {bbox_format}, {bbox_scale}`.
- Keep `101` diagnostic-only and out of forward pass/fail metrics.

## Expected Evidence After A Future Approved Run

- Hinge metrics against v2 filtered baselines.
- Changed-source sanity results.
- Legacy office-negative abstention guard result.
- Case-level notes for `101`, `155`, and any new regression cluster.
- A concise winner/near-miss/failure classification.
