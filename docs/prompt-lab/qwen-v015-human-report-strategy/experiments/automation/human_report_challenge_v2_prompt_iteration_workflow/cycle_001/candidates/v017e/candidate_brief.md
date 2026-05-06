# v017e Candidate Brief

Status: `authored_for_bounded_live_gate_run`

## Purpose

Test footprint/contact alignment after `v017d` became a stronger potential
winner but still showed case `67` row-target boxes drifting high/left relative
to the reference target footprints.

## Dependency

Depends on the `v017d` gate diagnosis.

## Prompt Axis

- preserve visual-anchor lock
- set equipment boxes from visible body footprint/contact cues
- avoid dust/motion/road/row geometry as the box anchor
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
