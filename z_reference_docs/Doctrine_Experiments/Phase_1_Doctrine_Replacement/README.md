# Phase-1 Doctrine Replacement

This package captures the first local-only doctrine audit and shadow-replacement
experiment for `src/bda_svc/pipeline/doctrine.yaml`.

## Purpose

The intent is to answer two questions without touching `origin/main`:

1. How well does the current live `doctrine.yaml` already capture the Phase-1
   physical damage doctrine in `z_reference_docs/BDAs/`?
2. Can a more prompt-compatible Phase-1 doctrine file improve model behavior
   without reopening known control-case failures?

## Current Read

The live doctrine file already does several things well:

- it preserves the core building PDA percentage bands
- it preserves the framed-building versus load-bearing distinction
- it preserves the military-equipment PDA category set
- it fits the current runtime contract exactly

The main weaknesses are not raw doctrinal absence. They are translation and
scope issues:

- some all-source or non-visual implications leak into a visual-only workflow
- PDA meaning is not clearly separated from broader BDA / FDA / target-system
  concepts
- some building guidance is not translated cleanly for a per-target
  crop-and-scene runtime
- the file mixes doctrinal meaning with practical detection heuristics

## Worktree Testbeds

Two new local-only doctrine branches/worktrees were created from the current
active feature lines:

- Qwen:
  - branch: `feat/qwen3-vl-8b-instruct/doctrine-bda-alignment`
  - worktree:
    `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment`
- Gemma:
  - branch: `feat/gemma4-e4b/doctrine-bda-alignment`
  - worktree:
    `/home/williambenitez1/Capstone_worktrees/3.2_feat__gemma4-e4b__doctrine-bda-alignment`

Important Gemma note:

- the doctrine branch was intentionally created from committed tip `9ae27e9`
- it does **not** absorb the uncommitted local `v003` Gemma experiment edits
  from the active `3.1` worktree

## Files In This Package

- `current_live_doctrine.snapshot.yaml`
  Snapshot of the current live doctrine before replacement work.
- `doctrine_source_crosswalk.md`
  Source-to-runtime mapping of what the live doctrine keeps, misses, or mixes.
- `preserve_adapt_exclude_matrix.md`
  What should be preserved, adapted, or excluded in the candidate doctrine.
- `phase1_only_doctrine_rules.md`
  The scope rules for this replacement effort.
- `runtime_candidate_doctrine.v001.yaml`
  First drop-in runtime candidate.
- `runtime_candidate_doctrine.v001.notes.md`
  Why the candidate differs from the live doctrine.
- `worktree_test_playbook.md`
  Exact local test flow for the Qwen and Gemma doctrine branches.
- `qwen_detect_candidate_a_run01_review.md`
  Cross-branch review note for the first mirrored detect-only prompt-surface
  candidate after the doctrine-only path stalled.
- `qwen_detect_candidate_c_run03_review.md`
  Cross-branch review note for the example-structured detect-only follow-up
  after the prose-heavy background-suppression step stalled.
- `qwen_detect_candidate_d_run04_review.md`
  Cross-branch review note for the hierarchy-first detect-only follow-up that
  produced an asymmetric doctrine-side gain.

## Working Rule

This package is local-only and intentionally separate from tracked repo runtime
state on `main`.

Nothing here should be treated as a promoted doctrine change until:

- the candidate passes runtime contract checks
- the candidate survives doctrine-sensitive guard cases
- the candidate improves or at least clarifies the building-severity problem
  without degrading held controls

## Current Status

- `runtime_candidate_doctrine.v001.yaml` is now installed only in:
  - `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment`
  - `/home/williambenitez1/Capstone_worktrees/3.2_feat__gemma4-e4b__doctrine-bda-alignment`
- the candidate passed the local runtime contract checks in both doctrine
  branches:
  - `uv run pytest tests/unit/test_yamls.py tests/unit/test_utilities.py`
- the next evaluation gate is the doctrine-sensitive six-case guard set, not a
  broad inherited sweep yet
- that first guard-set run is now recorded for both doctrine branches:
  - Qwen:
    `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/experiments/runs/doctrine_guard_set/run01_2026-04-20_182243_EDT/`
  - Gemma:
    `z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.2_feat__gemma4-e4b__doctrine-bda-alignment/experiments/runs/doctrine_guard_set/run01_2026-04-20_182243_EDT/`
- early read from that guard-set run:
  - Qwen held the control cases, but later same-input parent-control review
    showed no meaningful improvement on `destroyed_building4`
  - Gemma reopened intact-control regressions, so the first candidate is a
    no-go for broader Gemma sweep without revision
- focused follow-up note:
  - `qwen_destroyed_building4_manual_review.md`
    Manual review against the BDA text, source image, held Qwen control, and
    bbox review artifacts. Current conclusion: the doctrine candidate did not
    materially improve bbox quality or doctrinal fit on that scene; the main
    remaining issue is target delimitation/localization rather than PDA wording
    alone.
- prompt-assembly follow-up note:
  - `detection_prompt_assembly_analysis.md`
    Detection-path trace showing that doctrine is injected into the detection
    user prompt as a mid-prompt reference block rather than as a high-authority
    system-level instruction. Current conclusion: doctrine is real in the
    assembly, but probably not strong enough by itself to be the main lever for
    the Qwen adjacent-building localization problem.
- prompt-surface inspection note:
  - `qwen_detection_prompt_surface_inspection.md`
    Cross-branch detect-surface packet covering:
    - current rendered `1.2` prompt
    - current rendered `1.3` prompt
    - historical `v006` comparison
    - exact template and rendered diffs
    - instruction authority classification
    - the next detect-only A/B lanes
- Qwen-only follow-up candidate:
  - `runtime_candidate_doctrine.v002.yaml`
  - `runtime_candidate_doctrine.v002.notes.md`
    This revision changes only `buildings.detection_guidance` to tighten how
    the selected building body should be chosen in mixed adjacent-building
    scenes.
- Qwen rerun status:
  - `run02_2026-04-20_190546_EDT`
    Expanded same-input parent-control rerun against additional building cases
    showed no compelling improvement. The candidate stayed mostly neutral on
    most added scenes, still boxed a background building on
    `destroyed_building3`, and worsened the left-side building read on
    `destroyed_building4` relative to the held control.
- detect-surface follow-up status:
  - `qwen_detect_candidate_a_run01_review.md`
    The first mirrored detect-only prompt-surface candidate produced a real
    `destroyed_building4` recovery in both `1.2` and `1.3`, while leaving
    `destroyed_building3` and `destroyed_building6` unresolved. Current
    conclusion: the actual detection prompt surface is a stronger lever than
    doctrine-only wording for the Qwen adjacent-building problem.
  - `qwen_detect_candidate_b_run02_review.md`
    The second mirrored detect-only follow-up preserved the
    `destroyed_building4` recovery but did not fix `destroyed_building3` or
    `destroyed_building6`. Current conclusion: simple scene-dominance
    background-suppression prose is not enough to beat the stronger local
    `v010` state.
  - `qwen_detect_candidate_c_run03_review.md`
    The next mirrored detect-only follow-up restructured the building guidance
    around explicit target-selection examples instead of more prose rules. It
    preserved the useful `destroyed_building4` recovery and tightened some
    boxes slightly, but it still did not remove the `destroyed_building3`
    background-building false positive or the `destroyed_building6`
    scene-partitioning behavior. Current conclusion: example structure alone is
    also not enough to beat the stronger local `v010` state.
  - `qwen_detect_candidate_d_run04_review.md`
    The next mirrored detect-only follow-up added an explicit building priority
    decision order. It still did not beat `v010` in active `1.2`, but it did
    remove the `destroyed_building3` background-building false positive in the
    doctrine-side `1.3` lane. Current conclusion: stronger hierarchy can help,
    but the gain is currently asymmetric and not yet good enough to promote.

## Active Qwen Handoff

- the last completed logged doctrine-only Qwen checkpoint in this package
  remains:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/experiments/runs/doctrine_guard_set/run02_2026-04-20_190546_EDT/`
- later uncommitted local Qwen work still exists outside the logged run notes
  in:
  - `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/src/bda_svc/pipeline/doctrine.yaml`
  - `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/src/bda_svc/pipeline/config.yaml`
- that dirty local pair should be treated as the active next-session resume
  point before any new Gemma or fresh prompt-only Qwen cycle is opened
- next-session start rule:
  - diff the dirty `1.3` worktree files against the logged `v002`
    doctrine-only checkpoint first
  - only then decide whether to validate, refine, or discard the local
    candidate
