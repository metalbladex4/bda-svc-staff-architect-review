# Gemma 4 E4B Branch Hub

This folder is the centralized branch/model routing root for local
`gemma4:e4b` work.

## Purpose

This root exists so the next model line can follow the same branch-aware,
evidence-first workflow that produced the active Qwen `v009` line, without
mixing Gemma work into the Qwen lab tree.

## Branch Layout

- `3_model__gemma4-e4b/`
  Long-lived model-branch metadata for the Gemma 4 E4B line.
- `3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/`
  First feature branch for bootstrapping Gemma 4 with the active Qwen `v009`
  workflow shape.

## Working Rule

Keep the Qwen line and the Gemma line separate, but comparable.

That means:

- reuse the same workflow
- reuse the same seed pack early
- preserve direct comparison paths to:
  - `origin/main` baseline
  - active Qwen `v009`
  - active Gemma `v000`

## Current Status

- first live Gemma `v000` run:
  - completed under the active feature lab
- active execution record:
  - `3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/v000/run01_2026-04-17_134308_EDT/`
- first read:
  - equipment and office-negative behavior held
  - `destroyed_building4` is the first clear Gemma-specific failure surface
