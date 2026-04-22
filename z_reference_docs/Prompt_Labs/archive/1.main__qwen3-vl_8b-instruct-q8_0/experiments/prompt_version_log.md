# Prompt Version Log

Use one row per experiment round. Change only one prompt surface at a time.

| Version | Date | Prompt Surface | Parent | Change Summary | Intended Effect | Eval Tracks Run | Result | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `v000` | `2026-04-06` | baseline | none | Refreshed snapshot from `upstream/main:src/bda_svc/pipeline/config.yaml` after PR #124. Includes `bbox_convention`, doctrine-guided detection, `{bbox_format}`, `{bbox_scale}`, and `{detection_guidance}`. | Establish current-main baseline before further experimentation. | none | baseline refreshed | keep |
| `v001` | `2026-04-02` | `system` | pre-merge `v000` | Rewrites the shared system prompt into a shorter Qwen-specific policy prompt. | Improve format compliance, visual-only discipline, and reduce interference with task prompts. | pending | pre-merge draft | superseded by `v005` |
| `v002` | `2026-04-02` | `assess_damage` | `v001` | Rewrites the per-target assessment prompt for stricter single-target, visual-only, doctrine-consistent assessment. | Improve target focus, conservative labeling, confidence calibration, and concise evidence logic. | pending | pre-merge draft | superseded by `v006` |
| `v003` | `2026-04-02` | `detect_objects` | `v002` | Rewrites the detection prompt with direct grounding language and tighter object/bbox rules, but hardcodes the old `xyxy_1000` contract. | Improve count consistency, label discipline, bbox quality, and duplicate control. | pending | pre-merge draft | superseded by `v007` |
| `v004` | `2026-04-02` | `summarize_scene` | `v003` | Rewrites the summary prompt to stay tightly anchored to prior target assessments and plain-text output. | Improve summary consistency, reduce hallucinated claims, and keep scene summaries concise. | pending | pre-merge draft | superseded by `v008` |
| `v005` | `2026-04-06` | `system` | refreshed `v000` | Reconciles `v001` onto current-main baseline. System-only change; no placeholder, schema, or bbox contract changes. | Preserve the short policy-only system prompt while staying compatible with current main. | pending | reconciled draft | pending |
| `v006` | `2026-04-06` | `assess_damage` | `v005` | Reconciles `v002` onto current-main baseline and `v005`. Keeps `{target_type}`, `{doctrine}`, and assessment schema unchanged. | Preserve stricter single-target assessment guidance under the current runtime contract. | pending | reconciled draft | pending |
| `v007` | `2026-04-06` | `detect_objects` | `v006` | Reconciles `v003` with current parameterized detection contract by restoring `{detection_guidance}`, `{bbox_format}`, and `{bbox_scale}`. | Preserve direct Qwen-style localization while keeping doctrine-guided detection and configured bbox convention behavior. | pending | reconciled draft | pending |
| `v008` | `2026-04-06` | `summarize_scene` | `v007` | Reconciles `v004` onto the full post-merge chain. Keeps `{target_assessments}` and plain-text summary contract unchanged. | Preserve concise summary behavior while staying consistent with prior target assessments and the current prompt chain. | `2026-04-06_203823_EDT` full-pipeline seed run on `tests/data/tank.jpg` | matched baseline class/damage/confidence; bbox changed to `[51, 49, 115, 85]`; visual review found bbox off target; raw response confirms VLM localization failure | do not promote; needs detection-focused follow-up |
| `v009` | `2026-04-06` | `detect_objects` | `v008` | Adds explicit physical-target-only bbox guidance and forbids boxing fire, smoke, plume effects, shadows, terrain, or other damage effects as the target. | Improve bbox placement over the actual target object while preserving the current parameterized detection contract. | `2026-04-06_210720_EDT` full-pipeline seed run on `tests/data/tank.jpg` | bbox changed to `[51, 49, 128, 73]` but remained visually off target; assessment/summary introduced unsupported "locomotive" identity detail | reject for now |
| `v010` | `2026-04-06` | `detect_objects` | `v008` | Replaces the rejected `v009` exclusion-only detection approach with effect-cue-anchored localization: use fire, smoke, scorch marks, and debris as cues, then anchor the box to visible solid target structure. | Improve localization by giving the model a positive method for finding the physical target body while preserving the current parameterized detection contract. | `2026-04-06_212840_EDT` full-pipeline seed run on `tests/data/tank.jpg` | bbox changed to `[51, 49, 128, 85]` but remained visually off target over smoke/plume; identity wording improved vs `v009` | reject for now |

## Reconciliation Notes

- `v001` through `v004` are retained as pre-merge history.
- `v005` through `v008` are the active reconciled candidates for the current
  `upstream/main` runtime contract.
- `v003` was not directly reusable because it hardcoded `[xmin, ymin, xmax, ymax]`
  and `0-1000` instructions instead of preserving the current runtime
  placeholders.
- `v007` is the highest-risk reconciled candidate because detection is where
  the live contract changed most.
- `v009` is the first post-run follow-up after visual review of
  `2026-04-06_203823_EDT`; it changes only `detect_objects` and targets
  `DET-09 bbox_off_target`.
- `v010` is parented to `v008`, not `v009`, because `v009` was rejected; it is
  an alternative detection-only strategy rather than a continuation of the
  rejected exclusion-only prompt.

## Logging Rules

- One version per experiment round.
- One prompt surface per version.
- Record both improvements and regressions.
- If schema reliability drops, reject the version even if semantics improve.
- Accepted versions should be copied into `experiments/winners/` once they pass.
