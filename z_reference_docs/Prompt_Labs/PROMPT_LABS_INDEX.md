# Prompt Labs Index

This folder contains local-only prompt iteration workspaces. These labs are for
active experiments, eval manifests, doctrine/schema crosswalks, and versioned
prompt notes before any winning prompt text is promoted into the main project.

Generated: `2026-04-21T23:52:20-04:00`

## Current Branch-Structured Roots

- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/`
  New centralized branch/model root for future `qwen3-vl:8b-instruct` work
  after the git/worktree reset.
- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1_model__qwen3-vl-8b-instruct/`
  Long-lived model-branch root created from clean mirrored `main` at
  `28e863b`, later refreshed through `c19940a`, and now refreshed again
  through `e7a22a9`. The branch still completes the standard prompt-lab smoke
  flow after the newer export/detect-contract change.
- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/`
  First feature-branch root created from the clean model branch.
  Its fresh active `v000` baseline is now recorded from `28e863b`, and its
  last confirmed staged winner is `v009`. A local detect-only `v010` candidate
  is now installed in tracked feature-branch config as an active exploratory
  follow-up after the detect-surface inspection. That candidate recovered the
  key `destroyed_building4` split in a same-input A/B run while leaving
  `destroyed_building3` and `destroyed_building6` unresolved. Two later
  detect-only follow-ups, `v011` and example-structured `v012`, have now both
  been recorded and rejected; both preserved the `destroyed_building4` gain
  but failed to resolve the remaining building-family errors cleanly. A later
  hierarchy-first `v013` follow-up also failed to beat `v010` in active `1.2`,
  although it did produce a useful doctrine-side-only `destroyed_building3`
  improvement in `1.3`. The live local Qwen detect state has therefore again
  been restored to `v010`. The branch was
  refreshed through `c19940a` without a
  `v000` rebuild because that upstream delta was infra-only, and it has now
  also been refreshed through `e7a22a9`. Qwen still passes the standard tank
  smoke loop after that newer change, but because live prompt wording changed,
  the next trustworthy post-refresh read should come from a rebuilt baseline.
- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/`
  Local-only doctrine-replacement branch created from the active Qwen feature
  line. This branch exists to A/B a Phase-1 PDA-aligned doctrine candidate
  against the untouched `1.2` control. Its first runtime candidate doctrine is
  now installed and passes the local runtime contract checks, but manual review
  now shows the first Qwen candidate did not materially improve
  `destroyed_building4` versus the held control; the main remaining issue is
  target delimitation/localization. A Qwen-only `v002` rerun that tightened
  only building `detection_guidance` also failed to produce a compelling
  improvement on the expanded building shot group. The current follow-up read
  now treats the real next lever as the actual detection prompt surface:
  the active `1.2` and `1.3` detect templates are currently the same, and the
  meaningful branch difference is the injected doctrine block rather than a
  hidden prompt-template split. The first mirrored detect-only candidate now
  shows the same `destroyed_building4` recovery in both branches, which
  strengthens the read that prompt-surface weighting is the stronger lever.
  A second mirrored follow-up (`v011`) and a third example-structured
  follow-up (`v012`) have now both been recorded and rejected; they preserved
  the `destroyed_building4` gain but did not fix `destroyed_building3` or
  `destroyed_building6`. A fourth hierarchy-first follow-up (`v013`) then
  removed the `destroyed_building3` background false positive only in this
  doctrine-side lane, which makes it useful evidence but still not a promoted
  winner. The live local Qwen state has been restored to `v010`. A later
  re-grounding pass confirmed that the active local resume point is still this
  dirty `1.3` doctrine/config worktree, whose uncommitted
  `src/bda_svc/pipeline/doctrine.yaml` + `config.yaml` pair sits beyond the
  last completed logged doctrine-only checkpoint and still needs to be
  diffed/validated before any new Gemma or fresh prompt-only cycle opens.
- `z_reference_docs/Prompt_Labs/3_gemma4-e4b/`
  New centralized branch/model root for future `gemma4:e4b` work.
- `z_reference_docs/Prompt_Labs/3_gemma4-e4b/3_model__gemma4-e4b/`
  Long-lived Gemma model-branch root created from clean mirrored `main`,
  carrying forward the reusable prompt-lab review-artifact workflow and CI fix,
  refreshed through `c19940a`, and now refreshed again through `e7a22a9`.
  It carries the tracked Gemma baseline config, but the newer detect-contract
  change now drives the standard tank smoke export to `object_not_found`, so
  the usual self-check does not currently close on that seed image.
- `z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/`
  First Gemma feature-branch root created from the Gemma model branch.
  This line starts as a semantic port of the active Qwen `v009` workflow into
  `gemma4:e4b`. Its rebuilt post-`e7a22a9` `v000` baseline is now recorded
  under the branch-specific lab as the active anchor, while the earlier first
  live `run01` remains preserved as pre-refresh historical evidence. The Gemma
  line still holds `destroyed_tank15`, `operational_building7`, and the office
  negative control. `v001` recovered the tank regressions, and `v002` has now
  improved building severity while preserving those recoveries across the full
  inherited six-case pack. `v002` is now the active Gemma direction on the
  current repo base.
- `z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.2_feat__gemma4-e4b__doctrine-bda-alignment/`
  Local-only doctrine-replacement branch created from the committed tip of the
  active Gemma feature line. This branch exists to A/B a Phase-1 PDA-aligned
  doctrine candidate against the untouched `3.1` control. Its first runtime
  candidate doctrine is now installed and passes the local runtime contract
  checks. It intentionally excludes the dirty local `v003` edits from the
  active `3.1` worktree.

Companion refresh docs:

- `z_reference_docs/GIT_WORKTREE_UPDATE_WORKFLOW.md`
  Defines the full-parity completion standard after upstream refreshes.
- `z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_QWEN.md`
  Copy-paste Qwen refresh plus smoke-validation checklist.
- `z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_GEMMA.md`
  Copy-paste Gemma refresh plus smoke-validation checklist.

## Legacy And Archived Labs

- `z_reference_docs/Prompt_Labs/2.main__qwen3-vl-8b-instruct/`
  Preserved legacy working lab from before the git/worktree reset.
  This now maps to the pre-reset local line preserved on
  `snapshot/2026-04-15-pre-main-reset`.

- `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/`
  Historical prompt lab for the earlier `qwen3-vl:8b-instruct-q8_0` sequence.
  Runs and versions created before `2026-04-10` now live here for reference
  only.

## Naming Convention

Prompt labs now use two conventions:

Legacy convention:

- `2.main__...`

Archived convention:

- `archive/1.main__...`

Current canonical convention for new work:

- `<model-slug>/<branch-slug>/`

Where:

- `<model-slug>` uses a leading model number, for example
  `1_qwen3-vl-8b-instruct`
- `<branch-slug>` is the git branch name with `/` replaced by `__` and a
  visible numbering prefix, for example `1_model__...` or `1.2_feat__...`

## Standard Lab Layout

Each branch-specific lab root should record:

- exact git branch name
- parent branch
- base commit
- model name
- worktree path
- branch type (`model` or `feature`)

Experiment subfolders can then use the same familiar structure:

- `baseline/`
  Snapshot of the current live config/prompts used by the repo.
- `dossier/`
  Model-specific prompting rules, source review notes, and doctrine/schema
  crosswalks.
- `evals/`
  Track-specific manifests for detection, assessment, and summary evaluation.
- `experiments/`
  Prompt version log, failure taxonomy, working versions, and accepted winners.
- `experiments/runs/`
  Version-first output folders for live experiment runs and their manifests.

## Working Rule

Prompt experimentation happens here first. The live repo prompt file at
`src/bda_svc/pipeline/config.yaml` should only change after a prompt version
clearly wins on schema reliability and doctrinal quality.

Output convention:

- baseline runs should be written to
  `experiments/runs/baseline/runNN_YYYY-MM-DD_HHMMSS_TZ/`
- candidate runs should be written to
  `experiments/runs/vNNN/runNN_YYYY-MM-DD_HHMMSS_TZ/`
- repeated runs should increment `runNN` and get a new timestamped folder
  instead of reusing an older run directory

Related companion document:

- `z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
  Living record of prompt-development method, source usage, experiment
  rationale, and significant directional changes across the prompt effort.
- `z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`
  Capability-first teaching guide for reproducing the branch-aware prompt
  workflow in this repo or another repo with similar capabilities.
- `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/README.md`
  Local-only doctrine audit, replacement candidate, and A/B test routing for
  the current Phase-1 doctrine experiment.
