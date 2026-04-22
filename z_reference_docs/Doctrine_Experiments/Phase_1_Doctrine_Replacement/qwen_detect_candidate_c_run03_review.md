# Qwen Detect Candidate C Run 03 Review

This note summarizes the third mirrored detect-only follow-up after the
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

Candidate C wording change:

- kept the `v010` adjacent-building target-body rule set
- replaced the broader mixed contrastive block with:
  - one dedicated building target-selection example block
  - one shorter general contrastive block

## Main Result

`v012` is not a clear upgrade over `v010`.

What held:

- `destroyed_building4` remained recovered as one scene-central destroyed
  building in both branches
- `office_negative` stayed clean
- `operational_tank4` stayed clean
- `tank_pressure` stayed clean

What did not improve:

- `destroyed_building3`
  - still boxed the background building as a second target in both branches
  - the false-positive box tightened, especially in `1.3`, but the wrong
    detection remained
- `destroyed_building6`
  - still returned three buildings in both branches
  - no meaningful count reduction or target-priority recovery occurred

Representative review sheets:

- `1.2 destroyed_building3`:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/detect_surface/run03_2026-04-20_224812_EDT/eval_vs_parent_control/images_bbox_review/bbox_review_destroyed_building3.jpg`
- `1.2 destroyed_building4`:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/detect_surface/run03_2026-04-20_224812_EDT/eval_vs_parent_control/images_bbox_review/bbox_review_destroyed_building4.jpg`
- `1.2 destroyed_building6`:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/detect_surface/run03_2026-04-20_224812_EDT/eval_vs_parent_control/images_bbox_review/bbox_review_destroyed_building6.jpg`

## Guardrail Read

No major category regressions reopened.

Observed caveat:

- some bboxes tightened modestly on a few controls
- that tightening was not enough to outweigh the fact that the targeted
  adjacent-building errors remained substantively unchanged

## Interpretation

Candidate C is useful evidence, but not the next live state.

- example-heavy structure can affect box shape
- it did not materially change target count or target selection on the two
  still-open building failures
- `v010` remains the stronger current local Qwen detect state

Working implication:

- the next real Qwen detect move likely needs either a stronger instruction
  hierarchy shift or a more surgical example pattern tied directly to the
  unresolved `destroyed_building3` and `destroyed_building6` behaviors
