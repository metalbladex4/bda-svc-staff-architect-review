# Qwen v015 Human-Report Strategy Package

Status: `v2_source_refresh_complete_automation_pending`

This worktree-local package converts the all-112 human-report comparison
into prompt-engineering strategy and local candidate evidence for Qwen
`v015`. It now also records the completed `v015a` through `v015e`
prompt-lane decision. No `v015` candidate is promoted or adopted into
runtime config.

## 2026-04-30 Source Refresh Note

The six corrected source reports `141`, `152`, `154`, `155`, `156`, and
`166` supersede the old `human_report_challenge_v1` gate semantics for future
prompt work. `v1` remains historical evidence for runs that were scored against
old references. Future prompt automation and candidate gates should use
`human_report_challenge_v2` and the source-refresh package at
`experiments/source_refresh/human_report_challenge_v2_refresh/`.

Current v2 eval-only all-112 baselines from reused predictions:

- `v009`: `162` matches, `57` false negatives, `53` false positives.
- `v014`: `149` matches, `70` false negatives, `23` false positives.

`155` and `166` are no longer protected object-not-found controls; both are
positive military-equipment cases in `v2`. Treat earlier `v015` and `v016a`
claims as `v1_reference_context` unless they have been explicitly rescored
against `v2`.

## Boundary

- Target worktree: `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`
- Main checkout source images and source reports remain source evidence.
- Approved source-derived docs and challenge references may be refreshed only
  under an explicitly approved source-refresh wave.
- Human-report source images and source reports are not mutated.

## v1 Historical Read

- `v009`: `161` matches, `56` false negatives, `54` false positives.
- `v014`: `148` matches, `69` false negatives, `24` false positives.
- Interpretation: `v014` suppresses false positives but loses recall.
- First `v015` direction: preserve `v014`-style false-positive suppression while restoring `v009`-style multi-target recall.

## Files

- `source_manifest.json`: source paths, hashes, counts, and write boundary.
- `failure_taxonomy.md` / `failure_taxonomy.json`: deterministic case grouping and design implications.
- `stratified_split.md` / `stratified_split.json`: 56-case dev and 56-case holdout split.
- `example_bank.md` / `example_bank.json`: offline exemplar bank; not runtime prompt stuffing.
- `candidate_hypotheses.md`: initial hypothesis-only candidate directions.
- `acceptance_gates.json`: balanced-recovery gates for later approved runs.
- `experiments/decision_memos/v015_prompt_lane_decision_memo.md`: closes the
  `v015` prompt lane and points the next prompting experiment at
  `v016_reference_aware_prompt_lab`.
- `experiments/decision_memos/v015_prompt_lane_decision_summary.json`:
  machine-readable companion summary for the decision memo.
- `experiments/design/v016_reference_aware_prompt_lab/`: design-only package
  for the next reference-aware v016 prompt-lab axis; no v016 prompt text,
  overlay, runner session, runtime change, holdout, all-112 run, or promotion
  artifact is created there.
- `experiments/runs/v016a_reference_aware_candidate_discovery/`: prompt-only
  v016a candidate run. The expanded hinge recovered recall but failed precision
  and case `101` diagnostics, so it is blocked from dev.
- `experiments/source_refresh/human_report_challenge_v2_refresh/`: records the
  corrected-source v2 refresh, v1-to-v2 deltas, eval-only rebaselines, split/gate
  implications, and automation readiness decision.
- `experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/`:
  dry-run-validated workflow for future `v017` prompt-iteration cycles against
  `human_report_challenge_v2`; no prompt text, VLM inference, or promotion is
  created there.

## v1 Split Summary

- Dev cases: `56`
- Holdout cases: `56`
- Case `101` is pinned to dev as the hinge precision/recall tradeoff case.
- Historical v1 protected out-of-scope controls were split: `155` in dev,
  `166` in holdout. This is no longer valid for v2 gates.

## Current Decision

The `v015a` through `v015e` sequence is closed as learning evidence.
`v015e` preserved precision on the 56-case dev split but failed recall
relative to the `v014` dev baseline, so it is not promoted and should not
advance to holdout or all-112 without a new approval.

The first authored v016 prompt candidate,
`v016a_reference_aware_candidate_discovery`, tested the selected
reference-aware candidate-discovery/evidence-budget axis. It improved expanded
hinge recall but failed the strict precision cap and repeated case `101`
row-fragment/broad-group behavior. Treat it as learning evidence only; no dev,
holdout, all-112, promotion, or runtime config adoption is approved from this
result.

After the 2026-04-30 source refresh, the next prompt-automation work should
build against `human_report_challenge_v2` only. Automation is package-ready, but
candidate runs remain blocked until a separate approved implementation wave.
