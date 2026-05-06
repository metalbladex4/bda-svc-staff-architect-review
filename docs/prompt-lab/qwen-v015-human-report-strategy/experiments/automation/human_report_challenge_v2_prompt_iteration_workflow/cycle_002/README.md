# Cycle 002: v018 Dense-Formation Follow-Up

Status: `active_bounded_prompt_only_cycle`

Cycle 002 follows the accepted `v017b_group_box_rejection` prompt-only main
promotion recommendation. It does not replace that recommendation by default.
It tests whether one narrow prompt-only follow-up can address the preserved
case `67` dense-formation limitation without reopening the v017 broad-box or
precision-false-positive failure patterns.

## Boundary

- Active lane: `human_report_challenge_v2`
- Excluded from forward pass/fail gates: `101`
- Parked primary candidate remains: `v017b_group_box_rejection`
- This cycle is worktree-only unless later approved otherwise.

No source reports, source images, reference truth, runtime config, promotion
state, Git remotes, Graphify outputs, or Mem0 memory are changed by this
cycle.

## Candidate

- `v018a_dense_formation_body_center_anchor`

## Initial Gate

Run only:

- `human_report_challenge_v2_hinge_11_no101`
- `legacy_abstention_guard_office_negative`

The purpose is to see whether dense-formation anchoring improves or at least
does not materially worsen cases `66`, `67`, and `84`, while preserving
positive `155` and the separate office-negative abstention guard.
