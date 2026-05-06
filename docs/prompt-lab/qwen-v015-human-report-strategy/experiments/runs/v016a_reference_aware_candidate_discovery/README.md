# v016a Reference-Aware Candidate Discovery

Status: `hinge_failed_blocked_no_dev`

This worktree-only prompt candidate implements the selected v016 axis:
`v016_reference_aware_candidate_discovery_with_evidence_budget`.

Source-refresh note: the original hinge run below was scored in the
`human_report_challenge_v1` reference context. The 2026-04-30
`human_report_challenge_v2` refresh reclassifies `155` as a positive
military-equipment case, so the old protected-abstention claim is historical
only. The v2 eval-only recalibration keeps `v016a` blocked.

## Boundary

- Prompt-only overlay; no runtime config adoption.
- No dev, holdout, all-112, promotion, source-truth mutation, Graphify refresh,
  evidence rebuild, or Mem0 update occurs until the hinge result and approved
  closeout.
- Source human-report images, source reports, and generated run artifacts remain
  read-only.

## Candidate Intent

The prompt uses a two-stage interface:

- Candidate discovery across the whole image, including secondary, distant, or
  off-center visible targets.
- Evidence-budget self-filter before final JSON, rejecting broad group/scene
  boxes, row fragments, adjacent context, duplicate unsupported extras, and
  protected-negative violations.

## Hinge Pack

Expanded 12-case hinge pack:

- Original controls: `101`, `13`, `42`, `147`, `12`, `28`, `19`, `155`
- v016 pressure cases: `66`, `67`, `84`, `97`

Expanded baselines:

- v014: `22` matches, `34` false negatives, `16` false positives
- v009: `31` matches, `25` false negatives, `39` false positives

Strict gate:

- matches must be greater than `22`
- false negatives must be less than `34`
- false positives must be no more than `16`
- historical v1 protected case `155` had to remain abstention-safe
- case `101` must have no row-fragment enumeration and no broad group/scene box
- case `101` receives manual review regardless of aggregate metrics

## Result

Execution:

- Run directory: `executions/human_report_challenge_v1_v016a_hinge_smoke_2026-04-30_015313Z/`
- Candidate manifest summary: `executions/human_report_challenge_v1_v016a_hinge_smoke_2026-04-30_015313Z/candidate_manifest_run_summary.json`
- Gate summary: `executions/human_report_challenge_v1_v016a_hinge_smoke_2026-04-30_015313Z/v016a_gate_check_summary.json`
- Case `101` manual review: `executions/human_report_challenge_v1_v016a_hinge_smoke_2026-04-30_015313Z/case_101_manual_review.md`
- Expanded hinge notes: `executions/human_report_challenge_v1_v016a_hinge_smoke_2026-04-30_015313Z/expanded_hinge_notes.md`

Aggregate result:

- Matches: `27`, which beats the v014 expanded hinge baseline of `22`.
- False negatives: `29`, which improves on the v014 expanded hinge baseline of
  `34`.
- False positives: `33`, which fails the `<=16` cap.
- Historical v1 protected case `155`: passed abstention-safe.

Two-tier diagnostic result:

- Case `101` still produced row-fragment enumeration.
- Case `101` still produced a broad group/scene box.
- Dev-run recommendation: `blocked`.

Interpretation:

`v016a` recovered hinge recall, but did so by reopening the precision failure
that the v015 sequence was trying to avoid. It is useful learning evidence, not
a dev candidate. Do not run dev, holdout, all-112, promotion, or runtime config
adoption without a later explicit approval.

v2 recalibration from existing predictions:

- Manifest context: `human_report_challenge_v2_v016a_hinge`.
- Matches: `26`
- False negatives: `31`
- False positives: `34`
- Negative scenes: `0`

The v2 result is still blocked: precision remains far over the cap, and `155`
is now a positive target case rather than an abstention control.
