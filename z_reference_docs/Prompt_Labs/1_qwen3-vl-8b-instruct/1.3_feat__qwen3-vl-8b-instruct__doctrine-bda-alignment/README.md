# 1.3 Doctrine Lab

This is the doctrine-alignment experiment branch for the Qwen line.

- branch: `feat/qwen3-vl-8b-instruct/doctrine-bda-alignment`
- parent branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- creation base commit: `6ab67d6`

## Purpose

This branch exists to test whether a more doctrine-faithful but
prompt-compatible Phase-1 PDA doctrine file can improve or clarify behavior
without degrading the current held Qwen cases.

## Working Rule

- do not treat this branch as the new active Qwen direction by default
- use the parent feature branch as the control
- keep the experiment scoped to doctrine replacement first, not broad prompt
  rewrites

## Audit Package

The shared doctrine audit and candidate files for this branch live under:

- `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/`

## Current Status

- the first runtime candidate doctrine is now installed in this branch
- static runtime checks passed:
  - `uv run pytest tests/unit/test_yamls.py tests/unit/test_utilities.py`
- the first doctrine-sensitive guard-set run now exists under:
  - `experiments/runs/doctrine_guard_set/run01_2026-04-20_182243_EDT/`
- a Qwen-only follow-up rerun with a building-detection-guidance-only doctrine
  revision now exists under:
  - `experiments/runs/doctrine_guard_set/run02_2026-04-20_190546_EDT/`
- early read:
  - held `office_negative`, `operational_building7`, `operational_tank4`,
    `destroyed_tank15`, and `tank_pressure`
  - returned two `DESTROYED / PROBABLE` buildings on `destroyed_building4`
  - later same-input parent-control review showed that this was not a real
    doctrine win; the held Qwen control already makes the same semantic read
- current follow-up read:
  - the `v002` building-detection-guidance-only revision did not produce a
    compelling improvement
  - it stayed mostly neutral on the added building cases
  - it still boxed a background building on `destroyed_building3`
  - it worsened the left-side `destroyed_building4` read relative to the held
    control by shifting it from `SEVERE DAMAGE` back to `DESTROYED`
- prompt-assembly read:
  - the detection path does inject doctrine, but only as a plain mid-prompt
    user-message block
  - the stronger surrounding influence is still the main detection prompt
    surface, especially the later boxing rules and examples
  - current local note:
    `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/detection_prompt_assembly_analysis.md`
- detect-surface inspection read:
  - the current `1.2` and `1.3` `detect_objects` templates are the same
  - the rendered branch-to-branch difference currently comes only from the
    injected doctrine block
  - relative to historical `v006`, the active detect surface differs only
    slightly and should be treated as an instruction-weighting / hierarchy
    problem rather than a rewrite-from-scratch problem
  - current local note:
    `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detection_prompt_surface_inspection.md`
- next gate:
  - use the manual review note at
    `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_destroyed_building4_manual_review.md`
  - treat doctrine-only building-selection wording as an insufficient lever so
    far for the Qwen adjacency problem
  - do not touch Gemma again until we decide whether the next move belongs in
    doctrine, prompt surfaces, or detection-runtime assumptions

## Active Resume Point

- the last completed logged doctrine-only checkpoint in this branch remains:
  - `experiments/runs/doctrine_guard_set/run02_2026-04-20_190546_EDT/`
- later uncommitted local work still exists in the live worktree files:
  - `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/src/bda_svc/pipeline/doctrine.yaml`
  - `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/src/bda_svc/pipeline/config.yaml`
- that dirty local pair is the intended next-session resume point
- those exact local edits do not yet have a completed validation run or a
  dedicated result note

Next-session rule:

- do not jump first to Gemma
- do not open a fresh Qwen prompt-only cycle first
- start by diffing the dirty local `doctrine.yaml` and `config.yaml` pair
  against the logged `v002` doctrine-only checkpoint and deciding whether the
  local changes are an intentional candidate worth validation

## Detect Surface Verification Read

The first doctrine-side mirrored detect-only verification run is now recorded
at:

- `experiments/runs/detect_surface/run01_2026-04-20_200611_EDT/`

This run is intentionally diagnostic, not a change in this branch’s overall
role.

It exists to answer one narrow question:

- if the next lever really belongs in the detection prompt surface, does the
  same candidate still help when the doctrine-side branch keeps its different
  injected doctrine block?

Current result:

- yes, on the main question it does
- `destroyed_building4` recovered in the same useful direction as `1.2`:
  - parent control split the scene into two destroyed buildings
  - candidate reduced the read to one scene-central destroyed building
- `destroyed_building3` still boxed the background building
- `destroyed_building6` still behaved like broad scene partitioning
- `office_negative` and `operational_tank4` remained clean

Working implication:

- doctrine-only wording was not the strongest Qwen lever here
- prompt-surface weighting is the stronger next lane
- this branch should still be treated as a local verification surface, not the
  new active Qwen direction

## Detect Surface Verification Follow-Up Read

The next mirrored detect-only verification run is now recorded at:

- `experiments/runs/detect_surface/run02_2026-04-20_204540_EDT/`

Current result:

- it agreed with `1.2`
- `destroyed_building4` stayed recovered
- `destroyed_building3` and `destroyed_building6` did not meaningfully improve
- the added scene-dominance/background-suppression wording did not beat `v010`

Working implication:

- the doctrine-side lane does not reveal a hidden win here
- `v011` should be treated as a documented rejected follow-up
- this branch’s live detect prompt has also been restored to the mirrored
  `v010` state

## Detect Surface Verification Candidate C Read

The next mirrored detect-only verification run is now recorded at:

- `experiments/runs/detect_surface/run03_2026-04-20_224812_EDT/`

Current result:

- it again agreed with `1.2`
- `destroyed_building4` stayed recovered as one scene-central destroyed
  building
- `destroyed_building3` still boxed the background building, even though the
  false-positive box tightened
- `destroyed_building6` still returned three buildings
- doctrine-side verification still does not reveal a hidden win that is absent
  in `1.2`

Working implication:

- example-heavy restructuring is not enough to beat `v010`
- `v012` should be treated as another documented rejected follow-up
- this branch’s live detect prompt has again been restored to the mirrored
  `v010` state

## Detect Surface Verification Candidate D Read

The next mirrored detect-only verification run is now recorded at:

- `experiments/runs/detect_surface/run04_2026-04-20_233900_EDT/`

Current result:

- it did **not** simply agree with `1.2`
- `destroyed_building4` stayed recovered as one scene-central destroyed
  building
- `destroyed_building3` improved materially by removing the background-building
  false positive
- `destroyed_building6` still returned three buildings

Working implication:

- `v013` is still not a promoted winner, because the active `1.2` lane did not
  beat `v010`
- but this run is now the clearest sign so far that stronger instruction
  hierarchy can help when combined with the doctrine-side prompt context
- this branch’s live detect prompt has again been restored to the mirrored
  `v010` state, but the asymmetric `destroyed_building3` gain should be
  preserved as a clue for the next iteration
