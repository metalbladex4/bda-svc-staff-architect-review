# v017f Candidate Brief

Status: `authored_for_bounded_live_gate_run`

## Purpose

Run the final approved prompt-only attempt in cycle 001: a compact
visual-anchor balance based on the stronger `v017d` result, without the heavier
footprint wording that failed to improve `v017e`.

## Dependency

Depends on the `v017e` gate diagnosis.

## Prompt Axis

- compact full-image scan and body-backed filtering
- visual-anchor lock against row/group/region boxes
- no geometric interpolation or expected-count filling
- tight single-target boxing with a shorter final audit
- preserve active hinge, changed-source, and office-negative gates

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
