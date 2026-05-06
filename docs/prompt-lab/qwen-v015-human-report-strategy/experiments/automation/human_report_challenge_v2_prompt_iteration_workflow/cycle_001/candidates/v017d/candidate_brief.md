# v017d Candidate Brief

Status: `authored_for_bounded_live_gate_run`

## Purpose

Test a visual-anchor-lock refinement after `v017c` passed the active corrected
gate but still showed row/formation placement artifacts in cases `67` and `84`.

## Dependency

Depends on the `v017c` gate diagnosis.

## Prompt Axis

- preserve evidence-named finalization
- require a visible body center and visual extent for each final box
- forbid boxes generated from row geometry, equal spacing, diagonal formation,
  road/lane alignment, or expected count
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
