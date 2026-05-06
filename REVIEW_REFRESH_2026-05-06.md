# Review Refresh 2026-05-06

This refresh updates the Staff Architect review surface for the ChatGPT 5.5 Pro
and GPT Deep Research collaboration.

## What Changed

- Merged current `cmu-bda/bda-svc upstream/main` into this review repo:
  `f462ef4516b63ca1a2cd2434e75692f65d0e94cb`.
- Overlaid the promoted Qwen config prompt from local branch
  `feat/config-prompt-improved-v1`:
  `src/bda_svc/pipeline/config.yaml`.
- Added the ChatGPT 5.5 Pro handoff dossier:
  `z_reference_docs/GPT-Pro_collab/chatgpt_5_5_pro_prompt_engineering_handoff.md`.
- Refreshed the current living docs:
  - `z_reference_docs/WORKING_CHANGELOG.md`
  - `z_reference_docs/REFERENCE_MASTER_INDEX.md`
  - `z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
  - `z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`
  - `z_reference_docs/PROJECT_BRAIN.md`
  - `z_reference_docs/Prompt_Labs/PROMPT_LABS_INDEX.md`
- Added the active Qwen prompt-lab evidence tree under:
  `docs/prompt-lab/qwen-v015-human-report-strategy/`.
- Updated review orientation files so ChatGPT 5.5 Pro starts with the new
  handoff and understands the current `v020c` / `v023` / `v024` state.

## Current Prompt State

- Incumbent: `v020c_extra_box_audit` / `v020c_anchor_replay`.
- Incumbent metrics: `186` matches / `33` false negatives / `25` false
  positives.
- Best high-recall challenger: `v024l_v023s_no_wheel_track_ablation` at
  `188/31/35`, but it is FP-heavy and does not replace `v020c`.
- Interrupted row: `v024o_v024l_intact_building_piece_exclusion` is partial and
  unscored.

## Sanitization Notes

- Raw credentials, local auth/session state, and Codex state were not copied.
- Recent prompt-lab raw image overlays and predicted-output dumps were not
  copied.
- The review repo currently appears as `PUBLIC` on GitHub, so future updates
  should keep the same public-safe sanitization stance unless repository
  visibility is corrected.

## Primary Reading Path

1. `REVIEW_INDEX.md`
2. `z_reference_docs/GPT-Pro_collab/chatgpt_5_5_pro_prompt_engineering_handoff.md`
3. `z_reference_docs/WORKING_CHANGELOG.md`
4. `z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
5. `docs/prompt-lab/qwen-v015-human-report-strategy/`
