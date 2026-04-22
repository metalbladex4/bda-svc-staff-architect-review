# Qwen Detect Candidate D Run 04 Review

This note summarizes the fourth mirrored detect-only follow-up after the
prompt-surface inspection packet.

## Scope

Branches used:

- active Qwen line:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`
- doctrine-side verification lane:
  `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment`

Parent:

- `v010` detect-only candidate, reused directly from detect-surface run01

Intervention:

- changed only `detect_objects`
- no doctrine edits
- no assessment edits
- no summary edits

Candidate D wording change:

- kept the `v010` adjacent-building target-body rule set
- added a top-of-prompt `BUILDING TARGET PRIORITY` decision order
- added one supporting foreground-vs-background building example

## Main Result

`v013` is not a clear upgrade over `v010`, but it produced the first genuinely
useful asymmetric signal since `v010`.

What held:

- `destroyed_building4` remained recovered as one scene-central destroyed
  building in both branches
- `office_negative` stayed clean
- `operational_tank4` stayed clean
- `tank_pressure` stayed clean

What improved:

- `1.3 destroyed_building3`
  - the background-building false positive was removed entirely
  - bbox review confirms the candidate now returns only the damaged
    scene-central building on the doctrine-side lane

What did not improve enough:

- `1.2 destroyed_building3`
  - still boxed the background building as a second target
- `destroyed_building6`
  - still returned three buildings in both branches
  - no meaningful count reduction or target-priority recovery occurred

Representative review sheets:

- `1.2 destroyed_building3`:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/detect_surface/run04_2026-04-20_233900_EDT/eval_vs_parent_control/images_bbox_review/bbox_review_destroyed_building3.jpg`
- `1.3 destroyed_building3`:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/experiments/runs/detect_surface/run04_2026-04-20_233900_EDT/eval_vs_parent_control/images_bbox_review/bbox_review_destroyed_building3.jpg`
- `1.2 destroyed_building6`:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/detect_surface/run04_2026-04-20_233900_EDT/eval_vs_parent_control/images_bbox_review/bbox_review_destroyed_building6.jpg`

## Interpretation

Candidate D is useful evidence, but not the next live state.

- a stronger hierarchy-first instruction can matter
- the effect is currently asymmetric across the active and doctrine-side lanes
- that asymmetry suggests the doctrine-injected block may be interacting with
  the hierarchy wording in a way that helps the model prioritize targets
- `v010` remains the stronger current local Qwen detect state because the
  active `1.2` line still did not beat it on the remaining failure family

Working implication:

- `v013` should be recorded and rejected for the live active line
- the asymmetric `1.3 destroyed_building3` improvement should be preserved as a
  clue for the next candidate instead of being discarded as noise
