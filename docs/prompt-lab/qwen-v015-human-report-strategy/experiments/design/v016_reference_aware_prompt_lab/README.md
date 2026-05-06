# v016 Reference-Aware Prompt-Lab Design Package

Status: `design_package_only_no_prompt_text`

This package closes the immediate v015 prompt-only loop into a reference-aware
v016 design lane. It is still prompt engineering: the goal is to improve the
next prompt authoring method by separating true prompt failures from
reference/evaluation-shape caveats before writing any new runtime prompt text.

Source-refresh note: this package was authored in the
`human_report_challenge_v1` reference context. The 2026-04-30 source correction
wave created `human_report_challenge_v2`, where `155` and `166` are positive
military-equipment cases rather than protected negative controls. Use this
package as historical design input, but build future v016 automation and gates
against the v2 source-refresh package.

## Boundary

- Worktree-only target:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`
- Main checkout artifacts remain read-only source evidence.
- No `v016` prompt text is authored in this package.
- No prompt overlay, runner session, validation manifest, run directory,
  promotion report, runtime config change, holdout run, all-112 run,
  Graphify refresh, evidence rebuild, or Mem0 update is created here.
- Source human reports, source images, and existing run outputs are not mutated.
  Challenge references may be regenerated only in a separately approved
  source-refresh lane such as `human_report_challenge_v2`.

## Source Artifacts

The design is grounded in:

- `experiments/decision_memos/v015_prompt_lane_decision_memo.md`
- `experiments/decision_memos/v015_prompt_lane_decision_summary.json`
- `experiments/runs/v015e_individual_body_evidence/executions/human_report_challenge_v1_v015e_hinge_smoke_2026-04-29_223729Z/v015e_gate_check_summary.json`
- `experiments/runs/v015e_individual_body_evidence/executions/human_report_challenge_v1_v015e_hinge_smoke_2026-04-29_223729Z/case_101_manual_review.md`
- `experiments/runs/v015e_individual_body_evidence/executions/human_report_challenge_v1_dev_56_2026-04-29_231342Z/eval/evaluation_2026-04-29_231946Z_summary.json`
- `experiments/runs/v015e_individual_body_evidence/executions/human_report_challenge_v1_dev_56_2026-04-29_231342Z/eval/evaluation_2026-04-29_231946Z.csv`
- `experiments/runs/v015e_individual_body_evidence/executions/human_report_challenge_v1_dev_56_2026-04-29_231342Z/v015e_dev_gate_summary.json`
- `stratified_split.json`
- `acceptance_gates.json`
- `experiments/diagnostics/v015_structural_output_guard_plan/`
- `experiments/diagnostics/v015_offline_structural_guard_simulator/`

## Reviewed Case Set

The reviewed set is every v015e dev case with `false_positive_count > 0` or
`false_negative_count >= 2`, plus protected/manual controls:

- Dev outliers: `66`, `67`, `69`, `84`, `86`, `97`, `100`, `101`, `103`,
  `147`, `155`
- Historical holdout protected reference-only control: `166`

In `human_report_challenge_v2`, `155` and `166` are no longer protected
negative controls.

## Design Read

v015e preserved precision but failed dev recall. It reached `61` matches and
`56` false negatives on dev against the v014 dev baseline of `70` matches and
`47` false negatives, while keeping false positives at `17`. Case `101`
remains a manual diagnostic because the hinge run still produced a broad
group/scene box and the reference shape includes known caveats.

The v016 design should not simply tighten the individual-body wording again.
The selected axis is `reference_aware_candidate_discovery_with_evidence_budget`:
first design the prompt interface around case-aware failure modes, then author a
later v016 prompt that can recover dense recall without re-opening row-fragment,
broad-box, and protected-negative failures.

## Artifacts

- `source_manifest.json`: source paths and forbidden mutations.
- `case_failure_review.md` / `case_failure_review.json`: case-level labels,
  prompt relevance, and v016 implications.
- `reference_shape_audit.md` / `reference_shape_audit.json`: reference/eval
  caveats, manual diagnostics, and protected controls.
- `prompt_vs_structural_guard_comparison.md`: why v016 remains prompting and
  why structural guards stay future scope.
- `v016_prompt_axis_recommendation.md` /
  `v016_prompt_axis_recommendation.json`: the selected v016 axis and
  constraints, with no final prompt text.

## Next Approval Gate

The next wave, if approved, should author a `v016` prompt/overlay from this
design package. It should not run holdout, all-112, promotion, runtime config
adoption, source-truth mutation, Graphify refresh, evidence rebuild, or Mem0
updates without separate approval.
