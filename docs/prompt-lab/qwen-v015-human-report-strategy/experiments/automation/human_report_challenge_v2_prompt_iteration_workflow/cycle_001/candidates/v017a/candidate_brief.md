# v017a Candidate Brief

Status: `planned_not_authored`

## Purpose

first v2-aware prompt candidate, to be selected from source-refresh and v016a failure lessons.

## Dependency

requires explicit later prompt-authoring approval.

## Boundaries

- Use `human_report_challenge_v2` only.
- Do not use `human_report_challenge_v1` as current gate authority.
- Do not treat `155` or `166` as protected negatives.
- Keep `166` holdout-only unless the user separately approves moving it.
- Preserve placeholders: `{categories}, {detection_guidance}, {bbox_format}, {bbox_scale}`.
- Do not include final prompt text in this brief.

## Expected Evidence After A Future Approved Run

- Hinge metrics against v2 filtered baselines.
- Changed-source sanity results.
- Legacy office-negative abstention guard result.
- Case-level notes for `101`, `155`, and any new regression cluster.
- A concise winner/near-miss/failure classification.
