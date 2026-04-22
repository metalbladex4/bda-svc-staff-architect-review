# Qwen Detect Candidate A Run 01 Review

This note summarizes the first mirrored detect-only follow-up after the prompt
surface inspection packet.

## Scope

Branches used:

- active Qwen line:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`
- doctrine-side verification lane:
  `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment`

Intervention:

- changed only `detect_objects`
- no doctrine edits
- no assessment edits
- no summary edits

Candidate A wording change:

- added one top-level building-selection rule in `RULES`
- tightened one later building boxing rule

## Main Result

The first detect-only prompt-surface intervention produced a real,
cross-branch improvement on `destroyed_building4`.

In both `1.2` and `1.3`:

- the parent control boxed the damaged scene as two buildings
- the candidate collapsed the read to one scene-central destroyed building
- bbox review suggests this is the intended adjacent-building target-body
  recovery, not arbitrary box drift

Key review sheets:

- `1.2`:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/detect_surface/run01_2026-04-20_200611_EDT/eval_vs_parent_control/images_bbox_review/bbox_review_destroyed_building4.jpg`
- `1.3`:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/experiments/runs/detect_surface/run01_2026-04-20_200611_EDT/eval_vs_parent_control/images_bbox_review/bbox_review_destroyed_building4.jpg`

## What Did Not Improve

The candidate did not solve the whole adjacent-building family.

- `destroyed_building3`
  - still boxes the background building as a second target
  - the second false-positive box remains visible in both branches
- `destroyed_building6`
  - still behaves like broad scene partitioning
  - no meaningful target-delimitation recovery yet

Representative review sheets:

- `1.2 destroyed_building3`:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/detect_surface/run01_2026-04-20_200611_EDT/eval_vs_parent_control/images_bbox_review/bbox_review_destroyed_building3.jpg`
- `1.2 destroyed_building6`:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/detect_surface/run01_2026-04-20_200611_EDT/eval_vs_parent_control/images_bbox_review/bbox_review_destroyed_building6.jpg`

## Guardrail Read

Held or effectively held:

- `office_negative`
- `operational_tank4`
- `tank_pressure`
- `destroyed_tank15`
- `destroyed_building5`
- `destroyed_building8`
- `operational_building7`

Observed caveat:

- some minor bbox drift remains on a few non-targeted controls
- the doctrine-side lane shows slightly more incidental drift than `1.2`, but
  not a reopened regression on the main guardrails

## Interpretation

This run strengthens the earlier inspection conclusion:

- doctrine injection is not the strongest lever for this Qwen problem
- the actual detection user prompt surface matters more
- prompt salience can move the key adjacent-building behavior in a way the
  doctrine-only rewrites did not

Working implication:

- Candidate A is a promising partial win
- it is not ready to call solved
- the next prompt move should preserve the `destroyed_building4` recovery while
  targeting the persistent `destroyed_building3` false-positive background
  building and the `destroyed_building6` scene-partition pattern
