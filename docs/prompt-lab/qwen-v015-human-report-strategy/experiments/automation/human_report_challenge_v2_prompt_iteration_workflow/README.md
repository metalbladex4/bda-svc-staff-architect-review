# Human Report Challenge v2 Prompt-Iteration Workflow

Status: `case101_diagnostic_only_forward_cycle_active`

This package defines the worktree-only automation workflow for future Qwen
`v017` prompt cycles against `human_report_challenge_v2`. It is deliberately a
framework and dry-run package: no real v017 prompt text, overlay, VLM inference,
promotion, holdout run, all-112 run, source-truth mutation, Graphify refresh, or
Mem0 update is performed here.

## Current Source Boundary

- `human_report_challenge_v2` is the prompt-gate authority for future human-report runs.
- `human_report_challenge_v1` remains historical evidence only.
- `155` is a positive military-equipment case, not a protected negative.
- `166` is a positive military-equipment holdout-only diagnostic unless a later approval moves it.
- Abstention is guarded separately by the legacy `office-negative` case.
- The current v2 source lane includes recovered report additions from the old
  no-report image lane; future automation must read the current v2 manifest,
  not the stale historical all-112 assumption.
- Fresh v009/v014 changed-report baselines now cover the ten latest
  updated/recovered reports.
- Case `101` is diagnostic-only moving forward. It remains historical evidence
  and may be reviewed manually, but it is excluded from forward pass/fail
  evaluation gates because its persistent broad-box behavior and
  reference/eval-shape caveats were distorting prompt-cycle decisions.

## Automation Shape

- Cycle lane: `v017`
- Candidate budget: `6` candidates (`v017a` through `v017f`)
- Main Codex remains cycle owner and final decision-maker.
- Sidecar subagents may be used only for bounded read-only critique, research,
  review, test coverage review, and result synthesis.
- Forward cycle continuation is approved through the remaining `v017c` through
  `v017f` budget unless a hard stop triggers. Near-miss diagnosis is required
  before each next candidate, but case `101` no longer blocks forward gate
  classification.

## Gate Packs

- `validation_manifests/human_report_challenge_v2_hinge_11_no101.yaml`
- `validation_manifests/human_report_challenge_v2_changed_source_sanity.yaml`
- `validation_manifests/human_report_challenge_v2_updated_report_smoke.yaml`
- `validation_manifests/legacy_abstention_guard_office_negative.yaml`

Diagnostic-only context:

- `diagnostic_manifests/human_report_challenge_v2_case101_diagnostic_only.yaml`
- `validation_manifests/human_report_challenge_v2_hinge_12.yaml` remains
  historical/manual-diagnostic context only and is superseded by
  `human_report_challenge_v2_hinge_11_no101` for forward gates.

## Workflow Scripts

- `scripts/build_v2_prompt_iteration_workflow.py`: builds this package.
- `scripts/run_v2_prompt_iteration_cycle.py`: creates a dry-run cycle plan.
- `scripts/check_v2_prompt_iteration_gates.py`: validates policies and dry-run gate readiness.
- `scripts/summarize_v2_prompt_iteration_cycle.py`: emits a decision packet for user review.

## Decision Rule

At the end of a real approved cycle, Codex should provide a brief decision
packet: potential winners, near misses, failures, what was learned, and the
smallest next user decision. The user remains the central decision maker; Codex
may handle bounded candidate-level decisions inside the approved cycle budget.
