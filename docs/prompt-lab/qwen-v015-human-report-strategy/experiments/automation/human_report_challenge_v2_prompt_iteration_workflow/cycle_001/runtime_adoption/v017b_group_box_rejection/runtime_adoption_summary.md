# v017b Runtime Adoption Summary

## Decision

`v017b_group_box_rejection` is adopted as the current Qwen `1.2`
worktree-local runtime default by folding its detect prompt into the Qwen
model-line overlay:

`src/bda_svc/pipeline/overlays/model_lines/qwen3-vl-8b-instruct.yaml`

This is a worktree-local adoption. It does not promote to `main`, does not edit
source truth, does not run holdout after adoption, and does not change MCP,
hook, Graphify, or Mem0 state.

## Adopted Runtime Surface

- Model-line overlay id:
  `qwen3-vl-8b-instruct-model-line-v017b-defaults-v1`
- Runtime model line: `qwen3-vl:8b-instruct`
- Detector backend: `vlm_prompt_detector`
- Resolved config hash:
  `fcbbbfa826940991b7e20cb5f4667609e3a5ecc01ee369d0c87545baf6a71998`
- Experiment overlays during runtime smoke: none
- Detect prompt SHA-256:
  `331bf0d27d08f62f153050c9bf20ab0a2b76d63828974217a7a24d3964ab2259`

## Promotion Evidence

The adoption is based on the approved v017b/v017d decision package and the
pre-adoption smoke/all-current package:

- Promotion decision:
  `cycle_001/dev_validation/v017d_v017f_dev_no101/primary_candidate_comparison/promotion_decision_v017b_v017d/promotion_recommendation.md`
- Pre-adoption summary:
  `cycle_001/pre_adoption/v017b_group_box_rejection/pre_adoption_summary.md`
- Worktree promotion report:
  `experiments/promotion_reports/qwen_1_2_v017b_group_box_rejection_promotion.yaml`

Key pre-adoption broad evidence:

- All-current/no-101: `158` matches, `61` false negatives, `25` false positives
  across `117` images.
- Changed-source sanity: `10` matches, `2` false negatives, `0` false positives.
- Updated-report smoke: `23` matches, `8` false negatives, `1` false positive.
- Office-negative abstention: `1` match, `0` false negatives, `0` false
  positives, `0` negative-scene false positives.
- Positive controls: `155` and `166` remained positive-control safe.
- `101` remains excluded from forward evaluation and diagnostic-only.

## Post-Adoption Runtime Smoke

These runs used `scripts/run_runtime_manifest.py`, which calls the default
resolved runtime without passing an experiment overlay.

| Manifest | Images | Matches | FNs | FPs | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| `human_report_challenge_v2_changed_source_sanity.yaml` | 5 | 10 | 2 | 0 | Matches pre-adoption changed-source sanity shape. |
| `legacy_abstention_guard_office_negative.yaml` | 1 | 1 | 0 | 0 | `1/1` negative-scene abstention correct; `0` negative-scene FPs. |
| `human_report_challenge_v2_updated_report_smoke.yaml` | 15 | 23 | 8 | 1 | Matches pre-adoption updated-report smoke shape; `155` clean. |
| `human_report_challenge_v2_hinge_11_no101.yaml` | 11 | 22 | 23 | 15 | Compact hinge regression guard under adopted runtime. |

All post-adoption smoke runs resolved to:

`fcbbbfa826940991b7e20cb5f4667609e3a5ecc01ee369d0c87545baf6a71998`

and recorded empty `experiment_overlay_ids`.

## Runtime Smoke Outputs

- `runs/changed_source_sanity/human_report_challenge_v2_changed_source_sanity_2026-05-03_210203Z/runtime_manifest_run_summary.json`
- `runs/office_negative/legacy_abstention_guard_office_negative_2026-05-03_210301Z/runtime_manifest_run_summary.json`
- `runs/updated_report_smoke/human_report_challenge_v2_updated_report_smoke_2026-05-03_210319Z/runtime_manifest_run_summary.json`
- `runs/hinge_11_no101/human_report_challenge_v2_hinge_11_no101_2026-05-03_210519Z/runtime_manifest_run_summary.json`

## Post-Adoption All-Current Replay

The full `human_report_challenge_v2_all_current_117_no101` replay was run after
adoption with the default resolved runtime and no experiment overlays.

| Pack | Images | Matches | FNs | FPs | Delta vs pre-adoption |
| --- | ---: | ---: | ---: | ---: | --- |
| `human_report_challenge_v2_all_current_117_no101` | 117 | 158 | 61 | 18 | `+0` matches, `+0` FNs, `-7` FPs |

Checks:

- case `101` absent from the replay
- case `155`: `2` matches, `0` false negatives, `0` false positives
- case `166`: `1` match, `0` false negatives, `0` false positives
- resolved config hash:
  `fcbbbfa826940991b7e20cb5f4667609e3a5ecc01ee369d0c87545baf6a71998`
- experiment overlays: none

Output:

- `runs/all_current_117_no101/human_report_challenge_v2_all_current_117_no101_2026-05-03_214944Z/runtime_manifest_run_summary.json`

## Boundaries Preserved

- Main checkout tracked files: unchanged.
- Source reports/reference truth: unchanged.
- Runtime base `config.yaml`: not adopted into main.
- Holdout post-adoption execution: not run.
- All-current/no-101 post-adoption replay: run as this follow-up validation.
- Promotion to `main`: not performed.
- Graphify refresh: not performed in this wave.
- Mem0 write: not performed in this wave.
- MCP config/hooks: unchanged.
