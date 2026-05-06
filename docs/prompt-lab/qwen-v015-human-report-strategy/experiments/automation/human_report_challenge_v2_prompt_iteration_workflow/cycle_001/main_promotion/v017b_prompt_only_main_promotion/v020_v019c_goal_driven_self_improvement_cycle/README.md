# v020 v019c Goal-Driven Self-Improvement Cycle

This worktree-only package continues the Qwen detect-prompt evidence lane from
`v019c_context_shadow_reversal`.

Anchor to replay first:

- `v019c_context_shadow_reversal`: 174 matches, 45 false negatives, 28 false
  positives on `human_report_challenge_v2_all_current_117_no101`
- controls passing: case `155`, case `166`, and
  `legacy_abstention_guard_office_negative`

Method:

- replay the v019c anchor before authoring any v020 candidate
- author exactly one candidate at a time
- run the same two tests per candidate:
  - `human_report_challenge_v2_all_current_117_no101`
  - `legacy_abstention_guard_office_negative`
- diagnose each candidate before deciding the next prompt axis
- track a balanced incumbent and a recall-ceiling near miss

Boundaries:

- detect prompt only
- preserve `{categories}`, `{detection_guidance}`, `{bbox_format}`, and
  `{bbox_scale}`
- no raw human-report text in prompts
- no case-specific hacks or case `101`
- no source-truth edits
- no doctrine edits
- no runtime adoption
- no commits, pushes, or PRs

Success target:

- controls passing
- false negatives <= 25
- false positives <= 15

Closeout:

- best stable balanced incumbent: `v020c_v019c_extra_box_audit`
- exact stability replay: `v020h`, using the same prompt as `v020c`
- stable result: `186` matches, `33` false negatives, `25` false positives
- controls passed for the incumbent and replay
- success target not reached
- recommendation packet: `final_recommendation.md`

Do not promote v020 as-is. Treat this package as local prompt-only learning
evidence and use `v020c` as the next diagnostic anchor rather than as an
automatic runtime adoption candidate.
