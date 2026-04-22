# Qwen Detect Candidate B Run 02 Review

This note summarizes the second mirrored detect-only follow-up after the
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

Candidate B wording change:

- kept the `v010` adjacent-building target-body rule
- added one scene-dominance/background-context rule
- added one explicit background-building contrastive example

## Main Result

`v011` is not a clear upgrade over `v010`.

What held:

- `destroyed_building4` remained recovered as one scene-central destroyed
  building in both branches
- `office_negative` stayed clean
- `operational_tank4` stayed clean

What did not improve:

- `destroyed_building3`
  - still boxed the background building as a second target in both branches
  - the second box got a bit tighter, but the false positive remained
- `destroyed_building6`
  - still returned three buildings in both branches
  - no meaningful count reduction or target-priority recovery occurred

Representative review sheets:

- `1.2 destroyed_building3`:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/detect_surface/run02_2026-04-20_204540_EDT/eval_vs_parent_control/images_bbox_review/bbox_review_destroyed_building3.jpg`
- `1.2 destroyed_building4`:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/detect_surface/run02_2026-04-20_204540_EDT/eval_vs_parent_control/images_bbox_review/bbox_review_destroyed_building4.jpg`
- `1.2 destroyed_building6`:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/detect_surface/run02_2026-04-20_204540_EDT/eval_vs_parent_control/images_bbox_review/bbox_review_destroyed_building6.jpg`

## Guardrail Read

No major category regressions reopened, but some incidental bbox drift returned
on non-targeted controls such as:

- `tank_pressure`
- `destroyed_tank15`
- some operational building boxes

That drift is not catastrophic by itself, but it matters because the targeted
building problems did not actually get solved.

## Interpretation

Candidate B tells us something useful even though it is not the next winner:

- preserving the `destroyed_building4` gain is possible
- simply adding more prose about scene-central versus background buildings is
  not enough to fix the remaining failure family

Working implication:

- the best current local Qwen detect state remains `v010`
- `v011` should be recorded, then rejected
- the next real lever is likely not another small prose-only background rule;
  it may need a more deliberate restructuring of examples or a different
  instruction layout altogether
