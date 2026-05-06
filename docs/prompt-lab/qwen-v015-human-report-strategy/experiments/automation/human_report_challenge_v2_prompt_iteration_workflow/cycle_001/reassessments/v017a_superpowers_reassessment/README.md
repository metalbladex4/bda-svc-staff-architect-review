# v017a Superpowers Reassessment

Status: `complete_reassessment_package`

## Purpose

This package reassesses the first live `human_report_challenge_v2` automation
candidate, `v017a_body_backed_candidate_filter`, after the Superpowers
operating contract was added to the Qwen `1.2` prompt-cycle lane.

It does not author `v017b`, run inference, change gates, change runtime config,
or promote any candidate. It records why `v017a` is a near miss and how the
automation workflow should use Superpowers before another prompt attempt.

## Source Evidence

Primary source artifacts:

- `../../runs/v017a/live_2026-04-30_212112Z/decision_packet.md`
- `../../runs/v017a/live_2026-04-30_212112Z/gate_check_candidate_summary.json`
- `../../runs/v017a/live_2026-04-30_212112Z/human_report_challenge_v2_hinge_12_2026-04-30_212112Z/predicted/101_2026-04-30_212126Z.json`
- `../../runs/v017a/live_2026-04-30_212112Z/human_report_challenge_v2_hinge_12_2026-04-30_212112Z/eval/evaluation_2026-04-30_212329Z_summary.json`
- `../../../cycle_controller_operating_contract.md`
- `../../../gate_policy.json`

## Reassessment Verdict

`v017a` remains `near_miss_not_winner`.

What held:

- changed-source sanity passed: `9` matches, `3` false negatives, `0` false
  positives
- positive control `155` passed with `2` matches
- legacy `office-negative` abstention guard passed
- aggregate v2 hinge checks passed numerically: `23` matches, `34` false
  negatives, `17` false positives
- row-fragment enumeration on case `101` was suppressed

What blocked advancement:

- the manual case `101` diagnostic failed
- `v017a` emitted one broad group/scene military-equipment box:
  `[75, 13, 1000, 571]`
- that box has area ratio about `0.4922`
- the broad group/scene box is distinct from the earlier row-fragment failure
  pattern; the model avoided row fragments but still accepted a scene-scale
  span as one target

## Workflow Decision

Superpowers improves the process by adding a mandatory diagnosis step before
another prompt is written. A near miss should not immediately trigger another
prompt attempt.

New cycle discipline for this lane:

1. Record the failed or near-miss result against source artifacts.
2. Diagnose the failure class using a `systematic-debugging` style artifact.
3. Recommend one narrow next prompt axis.
4. Stop for user review before authoring or running the next candidate.

## Next Gate

The next candidate, `v017b`, is not authorized by this package. The recommended
next action is to review `v017b_prompt_axis_recommendation.md` and approve or
revise the axis before any prompt text, overlay, runner session, validation
manifest, or VLM run is created.
