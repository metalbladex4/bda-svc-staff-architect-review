# Human Report Challenge v2 Source Refresh

Status: `source_refresh_and_rebaseline_package`

This package records the current 2026-04-30 source-refresh state for
human-report challenge v2. It now includes the earlier corrections for
`141`, `152`, `154`, `155`, `156`, and `166` plus the later updated
reports `40`, `61`, `65`, `69`, `70`, `77`, `106`, `125`, `172`, and
`187`.

## Decision

- `human_report_challenge_v1` remains historical evidence only.
- `155` and `166` are no longer object-not-found protected controls.
- `human_report_challenge_v2` remains the required reference lane for future prompt gates.
- Recovered reports from the old no-report lane are now part of current v2 source truth without moving source images.
- Prompt automation must not use stale all-112 assumptions after this refresh.
- Fresh changed-report v009/v014 baselines now cover the ten latest updated/recovered cases.
- Candidate automation remains paused for user approval of the next prompt-authoring or run wave, not for missing recovered-addition baselines.

## Files

- `changed_case_audit.*`: source report and v1/v2 reference deltas.
- `reference_delta.*`: compact v1-to-v2 reference consequences.
- `rebaseline_metrics.*`: adjusted current v2 metrics from historical reuse plus fresh changed-report baselines.
- `split_gate_implications.*`: gate and split policy changes.
- `automation_readiness.*`: whether the next automation package can be built.
- `validation_manifests/`: v2 versions of existing v015e/v016a recalibration packs.

## Current Readiness

- Ready for prompt automation package: `True`
- Ready for candidate runs: `False`
- Reason: v2 source references and current v009/v014 baseline coverage are available. Candidate runs remain paused until the user approves the next prompt-authoring or automation wave; v017b is not auto-authorized.
