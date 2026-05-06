# Branch State Manifest

This manifest records the branch/worktree state mirrored into this review repo.

## 2026-05-06 Refresh

This snapshot is intended for ChatGPT 5.5 Pro / Deep Research collaboration on
the prompt-engineering workflow.

Current review surface:

| Surface | Source | Captured State |
| --- | --- | --- |
| Runtime code baseline | `cmu-bda/bda-svc upstream/main` | `f462ef4516b63ca1a2cd2434e75692f65d0e94cb` merged into this review repo |
| Promoted config prompt | local branch `feat/config-prompt-improved-v1` | `src/bda_svc/pipeline/config.yaml` copied from local commit `9f1079daee9d50957048860e692e6a624befe230` |
| Primary local docs | `/home/williambenitez1/Capstone/z_reference_docs/` | refreshed selected living docs and `GPT-Pro_collab/` dossier |
| Qwen prompt-lab evidence | `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/` | copied curated text/summary artifacts under `docs/prompt-lab/` |

## Current Prompt State

- `v020c_extra_box_audit` / `v020c_anchor_replay` remains the Qwen incumbent:
  `186` matches, `33` false negatives, `25` false positives, with `155`,
  `166`, and office-negative passing.
- `v024l_v023s_no_wheel_track_ablation` is high-recall learning evidence:
  `188/31/35`, controls passing, but too many false positives to replace
  `v020c`.
- `v024o_v024l_intact_building_piece_exclusion` was interrupted and is
  unscored.

## Review Scope Notes

- This repo is a review snapshot, not the active development repo.
- The primary handoff for the current collaboration is:
  `z_reference_docs/GPT-Pro_collab/chatgpt_5_5_pro_prompt_engineering_handoff.md`.
- The copied prompt-lab tree intentionally omits raw image overlays and predicted
  dumps where possible; it preserves decision packets, prompt overlays, run
  summaries, comparison matrices, and diagnoses needed for review.
- Normal development should continue in `/home/williambenitez1/Capstone` and
  `/home/williambenitez1/Capstone_worktrees/`, not in this review repo.

## Visibility Caveat

GitHub currently reports this repository as `PUBLIC`. Treat every file in this
snapshot as sanitized review material. Do not add raw credentials, private local
state, raw Codex auth/session files, or unreviewed secret-bearing artifacts.
