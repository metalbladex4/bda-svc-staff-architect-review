# v017b Prompt-Only Main Promotion Gate Result

## Status

`paused_pending_user_decision`

The approved prompt-only main promotion wave replaced only
`/home/williambenitez1/Capstone/src/bda_svc/pipeline/config.yaml`
`prompts.detect_objects` with the exact v017b prompt and then ran the required
static checks and promotion smokes.

The promotion is **not committed** and should not be called complete because
the all-current/no-101 replay exceeded the pre-set false-positive cap by one.

## Main Edit

- allowed file edited:
  `/home/williambenitez1/Capstone/src/bda_svc/pipeline/config.yaml`
- edited field: `prompts.detect_objects`
- prompt hash after edit:
  `331bf0d27d08f62f153050c9bf20ab0a2b76d63828974217a7a24d3964ab2259`
- v017b source prompt hash:
  `331bf0d27d08f62f153050c9bf20ab0a2b76d63828974217a7a24d3964ab2259`
- exact prompt equality with v017b source: yes

Backup:

- `cycle_001/promotion_readiness/v017b_main_promotion_readiness/backups/main_config_yaml_pre_v017b_prompt_promotion_20260503.yaml`

## Static Validation

- YAML parse: passed
- `uv run pytest tests/unit/test_yamls.py tests/unit/test_model.py`: `18 passed`
- `uv run bda-svc -h`: passed

## Promotion Smokes

All smoke runs used main `bda-svc` inference and worktree manifest-aware
scoring for apples-to-apples comparison with the v017b evidence lane.

| Pack | Images | Matches | FNs | FPs | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| `human_report_challenge_v2_changed_source_sanity` | 5 | 10 | 2 | 0 | pass |
| `human_report_challenge_v2_updated_report_smoke` | 15 | 23 | 8 | 1 | pass |
| `legacy_abstention_guard_office_negative_v1` | 1 | 1 | 0 | 0 | pass; `1/1` abstention correct |

Positive-control check inside updated-report smoke:

- case `155`: `2` matches, `0` false negatives, `0` false positives

## All-Current/No-101 Replay

Pack:

- `human_report_challenge_v2_all_current_117_no101`

Result:

- images: `117`
- case `101`: absent
- matches: `165`
- false negatives: `54`
- false positives: `22`
- case `155`: `2` matches, `0` false negatives, `0` false positives
- case `166`: `1` match, `0` false negatives, `0` false positives

Comparison against the worktree adopted-runtime replay:

- matches: `+7`
- false negatives: `-7`
- false positives: `+4`

Gate thresholds from readiness packet:

- matches must be at least `156`: pass
- false negatives must be at most `63`: pass
- false positives must be at most `21`: **fail by 1**
- `155` must pass positive control: pass
- `166` must pass positive control: pass
- office-negative abstention must pass: pass

## Evidence Paths

- Changed-source smoke:
  `runs/human_report_challenge_v2_changed_source_sanity/human_report_challenge_v2_changed_source_sanity_2026-05-03_223209Z/main_promotion_manifest_run_summary.json`
- Office-negative smoke:
  `runs/legacy_abstention_guard_office_negative/legacy_abstention_guard_office_negative_2026-05-03_223247Z/main_promotion_manifest_run_summary.json`
- Updated-report smoke:
  `runs/human_report_challenge_v2_updated_report_smoke/human_report_challenge_v2_updated_report_smoke_2026-05-03_223251Z/main_promotion_manifest_run_summary.json`
- All-current/no-101 replay:
  `runs/human_report_challenge_v2_all_current_117_no101/human_report_challenge_v2_all_current_117_no101_2026-05-03_223526Z/main_promotion_manifest_run_summary.json`

## Decision Needed

Because the false-positive cap failed by one, the promotion is paused before
commit.

Decision options:

1. Approve threshold override and commit the prompt-only main change, accepting
   `165` matches, `54` false negatives, and `22` false positives as better
   overall than the cap expected.
2. Keep the edited main config uncommitted and run a focused visual review of
   the `22` false positives before deciding.
3. Restore the backup and keep v017b worktree-only for now.
