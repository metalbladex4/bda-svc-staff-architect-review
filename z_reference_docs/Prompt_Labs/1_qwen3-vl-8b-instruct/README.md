# Qwen3-VL-8B-Instruct Branch Hub

This folder is the new centralized branch/model routing root for local
`qwen3-vl:8b-instruct` work after the git structure reset on `2026-04-15`.

## Purpose

This root exists so we can keep:

- one clean mirrored `main`
- one long-lived model branch
- short-lived feature branches
- one centralized local docs/output hub under
  `/home/williambenitez1/Capstone/z_reference_docs`

without mixing all branch history into one lab folder.

## Branch Layout

- `1_model__qwen3-vl-8b-instruct/`
  Long-lived model branch metadata and future model-line lab material.
- `1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/`
  First feature-branch root created from the clean model branch.
  This root now contains the fresh branch-aware `v000` baseline rebuilt from
  `28e863b`.

## Legacy Mapping

The earlier active prompt work was created before the branch/worktree reset and
still lives in the legacy lab:

- `z_reference_docs/Prompt_Labs/2.main__qwen3-vl-8b-instruct/`

That legacy lab should be treated as:

- preserved historical working context
- tied to the pre-reset local line now preserved on
  `snapshot/2026-04-15-pre-main-reset`
- not the preferred root for new branch-structured work going forward

## Working Rule

New branch-specific experiment outputs and notes should be organized here using
the model-first, branch-second layout:

- `z_reference_docs/Prompt_Labs/<model-slug>/<branch-slug>/...`

Branch slug rule:

- use the exact git branch name
- replace `/` with `__` when creating folder names
- prepend visible numbering for quick scanning
- current examples:
  - model root: `1_qwen3-vl-8b-instruct`
  - model branch folder: `1_model__qwen3-vl-8b-instruct`
  - feature branch folder: `1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`

## Central Output Rule

Even when code is run from another worktree, experiment outputs should still be
written to the canonical absolute docs path under:

- `/home/williambenitez1/Capstone/z_reference_docs/`

Do not rely on worktree-local copies of `z_reference_docs`.

Companion workflow:

- `z_reference_docs/GIT_WORKTREE_UPDATE_WORKFLOW.md`
  defines how to refresh `main`, model branches, and feature worktrees safely
  when `upstream/main` changes again
