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
  remains preserved as the first overlay-backed exploratory follow-up after the
  detect-surface inspection. The completed building-reference truth audit and
  approved executable correction now preserve one-target `destroyed_building4`
  and one-target `destroyed_building3` guard-pack truth. Corrected-truth replay
  made `v014` ready for a formal promotion package, while `v009` remains the
  promoted/tracked baseline. That promotion path is now paused and superseded
  by the approved human-report process: read `v014` as
  `promotion_paused_superseded_by_human_report_process`, not rejected and not
  promoted. The Step 1 formal package remains historical/pending evidence, but
  the next Qwen learning authority is the completed all-112
  `human_report_challenge_v1` comparison of `v009` against `v014`. That run
  showed `v014` cut false positives from `54` to `24`, but also reduced matches
  from `161` to `148` and increased false negatives from `56` to `69`; the
  first `v015` lesson is to preserve false-positive suppression while restoring
  multi-target recall. Two earlier
  detect-only follow-ups, `v011` and example-structured `v012`, have now both
  been recorded and rejected; both preserved the current-manifest
  `destroyed_building4` signal
  but failed to resolve the remaining building-family errors cleanly. A later
  hierarchy-first `v013` follow-up also failed to beat `v010` in active `1.2`,
  although it did produce a useful doctrine-side-only `destroyed_building3`
  improvement in `1.3`. The later `v014` overlay then passed the corrected
  guard and grounding packs twice after the reference correction; that evidence
  is preserved as context rather than an immediate promotion trigger. The branch was
  refreshed through `c19940a` without a
  `v000` rebuild because that upstream delta was infra-only, and it has now
  also been refreshed through `e7a22a9`. Qwen still passes the standard tank
  smoke loop after that newer change, but because live prompt wording changed,
  the next trustworthy post-refresh read should come from a rebuilt baseline.
  Later human-report v2 work produced a parked prompt-only candidate,
  `v017b_group_box_rejection`, and the latest v018 upstream/v017b
  amalgamation cycle is preserved as learning evidence only: no v018 prompt is
  adoption-ready, `v018d` is the recall-ceiling signal, `v018e` is the
  precision-balanced follow-up axis, and `v017b` remains the parked candidate.
  The later v020 v019c goal-driven follow-up is also learning evidence only:
  `v020c_v019c_extra_box_audit` is the best stable prompt-only diagnostic
  anchor at `186` matches, `33` false negatives, and `25` false positives on
  all-current/no101 with controls passing, and exact replay `v020h` reproduced
  the same result. The cycle did not reach the `FNs <=25` and `FPs <=15`
  success target, and post-`v020c` prompt refinements repeatedly disturbed
  dense case `67` or created extra-box/tiling false positives, so v020 should
  not be promoted as-is.
  The follow-on v021 OpenAI-compatible cross-model matrix is the current
  comparison evidence for this lane: using fetched `upstream/main` code through
  Ollama-backed `/v1` endpoints, Qwen's best row was
  `v020c_extra_box_audit` at `186/33/25` with controls passing, while Gemma's
  best eligible row was `v018e_contrastive_body_anchor` at `138/81/19` with
  controls passing. Local and fetched upstream `doctrine.yaml` matched exactly,
  so the matrix used one shared-doctrine row. Use
  `v021_openai_compat_cross_model_prompt_matrix/` for current Qwen-vs-Gemma
  prompt-comparison routing.
  The later v022 literal-99 Qwen cycle is now closed as prompt-only plateau
  evidence: it replayed `v020c` at `186/33/25`, then tested `v022a` through
  `v022e`; every new wording pattern regressed, usually by collapsing dense
  case `67`. Use
  `v022_literal99_qwen_recursive_prompt_refinement_cycle/` when routing to the
  current evidence that v020c should be preserved and the next improvement
  lever should move to non-prompt duplicate/tiling suppression or
  detector/backend work.
  The v023/v024 literal-99 no-stop continuation is now paused and should be
  routed through `v023_literal99_qwen_no_stop_continuation/`, especially
  `pause_report_2026-05-06.md`. It ran `v023a` through `v023z` and `v024a`
  through `v024n`; `v024o` was interrupted by user pause and is not scored.
  `v020c_anchor_replay` remains the best combined row at `186/33/25`, while
  `v024l_v023s_no_wheel_track_ablation` is the best high-recall challenger at
  `188/31/35` but still carries too many false positives for adoption. The
  next routing recommendation remains visual review plus non-prompt
  duplicate/tiling suppression or backend/post-processing rather than long
  building-only prompt rule blocks.
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
  winner. The active control-line read now treats `v014` as the strongest
  unpromoted follow-up overlay, while the doctrine shadow lane itself remains
  paused evidence debt. A later
  re-grounding pass confirmed that the active local resume point is still this
  dirty `1.3` doctrine/config worktree, whose uncommitted
  `src/bda_svc/pipeline/doctrine.yaml` + `config.yaml` pair sits beyond the
  last completed logged doctrine-only checkpoint and still needs to be
  diffed/validated before any new Gemma or fresh prompt-only cycle opens.
- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.4_feat__qwen3-vl-8b-instruct__detector-backend-pilot/`
  Durable backend-pilot branch created from the active Qwen control line for
  the first concrete detector-backend comparison. The first local-first pilot
  backend (`vlm_tiled_detector`) now runs through the same overlay, trace,
  eval, and bounded-runner contracts as the control detector, but the first
  live comparison showed it materially underperformed `vlm_prompt_detector` on
  the declared packs. This lane is therefore preserved as the first backend
  pilot record and decision surface, while the active Qwen control line keeps
  `vlm_prompt_detector` as default.
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
  current repo base. The later phase-10 architecture port has now moved this
  branch onto the same overlay-first control-line architecture used on Qwen:
  tracked Gemma control baseline `v002`, paused overlay-backed follow-up
  candidate `v003`, detector backend default `vlm_prompt_detector`, and the
  bounded runner plus promotion-integrity scaffolding now present on the Gemma
  control line too.
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
  Central archive registration:
  `z_reference_docs/zz_archive/indexed_existing_archives/Prompt_Labs_archive.md`

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
- `experiments/cycles/`
  Adaptive multi-attempt cycle protocols, active cycle briefs, and replay
  rules layered on top of fixed runner sessions.
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
- `z_reference_docs/PROGRAM_EXPERIMENT_LEDGER.md`
  Cross-lab experiment ledger that ties legacy, archived, Qwen, Gemma,
  doctrine, backend, runner, and architecture experiments together with
  expected outcomes, actual outcomes, causal confidence, and current Codex
  assessment.
- `z_reference_docs/PROGRAM_DEEP_DIVE_AND_EXTENSIBILITY_REPORT.md`
  Whole-program companion that explains how Prompt_Labs connect to runtime,
  eval, worktree governance, Codex tooling, and the current Qwen follow-up
  lane.
