# Qwen `destroyed_building4` Manual Review

## Purpose

This note records the manual review of the first Qwen doctrine candidate on
`destroyed_building4` against:

- the held Qwen control branch
- the source image
- the bbox review sheet
- the Phase-1 building PDA text in the BDA corpus

The goal is to decide whether the doctrine replacement candidate produced a
real doctrinal improvement or only rephrased an existing scene-partitioning
mistake.

## Compared Artifacts

- Source image:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/experiments/runs/doctrine_guard_set/run01_2026-04-20_182243_EDT/input_images/destroyed_building4.jpg`
- Held Qwen control JSON:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/experiments/runs/doctrine_guard_set/run01_2026-04-20_182243_EDT/qwen_parent_control/destroyed_building4_2026-04-20_223433Z.json`
- Qwen doctrine candidate JSON:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/experiments/runs/doctrine_guard_set/run01_2026-04-20_182243_EDT/qwen_candidate/destroyed_building4_2026-04-20_222338Z.json`
- Bbox review sheet:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/experiments/runs/doctrine_guard_set/run01_2026-04-20_182243_EDT/destroyed_building4_eval/images_bbox_review/bbox_review_destroyed_building4.jpg`
- BDA source passages:
  - `z_reference_docs/BDAs/CJCSI 3162.02A METHODOLOGY FOR COMBAT ASSESSMENT July 2021.md`
  - `z_reference_docs/BDAs/Methodology For Combat Assessment.md`

## Held Qwen Control

The held Qwen control already returns:

- two `buildings`
- both `DESTROYED / PROBABLE`
- summary text that treats the scene as two destroyed buildings

Control boxes:

- left: `[0, 18, 63, 150]`
- right: `[63, 18, 244, 150]`

## Doctrine Candidate

The first doctrine candidate also returns:

- two `buildings`
- both `DESTROYED / PROBABLE`
- effectively the same summary meaning

Candidate boxes:

- left: `[29, 18, 69, 153]`
- right: `[69, 18, 250, 153]`

## What Actually Changed

- The split line moved right.
- The left box lost the far-left image area.
- The right box expanded slightly right and down.
- The semantic read did not improve relative to the held Qwen control.

This is not a meaningful bbox win. It is a small box-shape shift on top of the
same two-building interpretation.

## Source Image Read

The source image shows:

- a heavily destroyed central/right structure
- a neighboring upright left-side apartment/office-like structure
- a shared scene with rubble and adjacent urban buildings

The bbox review sheet shows that both Qwen runs still carve out the upright
left-side structure as its own damaged building target. The doctrine candidate
does not fix that. It simply shifts the split slightly.

## BDA Text Review

The building PDA text says:

- `DESTROYED` corresponds to `>75-100 percent` of target element area damaged
- framed buildings do not need full frame collapse to reach high damage levels
- load-bearing wall buildings map more directly to visible collapse percent
- for high multistory buildings or buildings with multiple sections/wings,
  report damage to the affected section and to the whole building when the
  scene supports that distinction
- for buildings with multiple wings, report destroyed wings and damage to the
  remainder of the structure

What that means here:

- the doctrine supports section/wing-aware reporting for complex building
  structures
- it does not support casually turning an upright neighboring structure into a
  separate destroyed building just because it sits beside the collapse zone
- the first question on this scene is still "what is the correct selected
  target body?" rather than "how should already-correct target bodies be scored
  on PDA thresholds?"

## Conclusion

The first Qwen doctrine candidate does not produce a real doctrinal or bbox
improvement on `destroyed_building4`.

The most important findings are:

- it does not materially improve bbox quality
- it does not change the held Qwen severity read in a meaningful way
- it does not resolve the main scene-understanding problem
- the remaining issue is target delimitation/localization, not PDA wording
  alone

## Working Implication

Treat this doctrine candidate as:

- doctrinally cleaner as a text artifact than the live doctrine
- operationally neutral on this key Qwen review case
- not enough, by itself, to justify a broader Qwen doctrine sweep as a likely
  winner

If Qwen doctrine work continues, the next useful lever is likely tighter
building-selection or section/wing delimitation guidance rather than another
PDA-only wording rewrite.
