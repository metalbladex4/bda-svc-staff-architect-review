# v025 Visual Delta Prompt Recovery

Created: `2026-05-06`

## Purpose

This package prepares the next Qwen prompt-engineering-first cycle without
authoring a new prompt candidate.

Operating doctrine:

`/home/williambenitez1/Capstone/z_reference_docs/GPT-Pro_collab/CODEX_QWEN_PROMPT_ENGINEERING_DIRECTION_2026-05-06.md`

The next candidate must be based on visual failure review, not metric summaries
alone. This package therefore inventories source artifacts, defines a review
plan, creates the failure taxonomy schema, and prepares the delta-review
template for `v020c` versus `v024l`.

## Source State

- Incumbent: `v020c_anchor_replay` / `v020c_extra_box_audit`
  - `186` matches / `33` false negatives / `25` false positives
  - controls passed: `155`, `166`, and office-negative
- Challenger evidence only: `v024l_v023s_no_wheel_track_ablation`
  - `188` matches / `31` false negatives / `35` false positives
  - controls passed: `155`, `166`, and office-negative
- Forbidden evidence: `v024o_v024l_intact_building_piece_exclusion`
  - interrupted before all-current completion
  - not scored here
  - must be rerun from scratch before any future use

## Package Boundary

This package is planning and visual-review scaffolding only.

It does not:

- promote any prompt
- score `v024o`
- author a new `detect_objects` prompt
- edit source truth, doctrine, assessment prompt, runtime code, or eval truth
- refresh Graphify or write Mem0

## Artifact Inventory

The existing `v023_literal99_qwen_no_stop_continuation` package contains the
source artifacts for this review:

- all-current eval summaries and CSVs for `v020c` and `v024l`
- 117 raw prediction JSON files per candidate
- 117 eval-side prediction JSON files per candidate
- full `images_bbox_review` visual sheets for 117 cases per candidate
- partial `images_bbox_both`, `images_bbox_predicted`,
  `images_bbox_reference`, `images_crop_predicted`, and
  `images_crop_reference` sets with 111 images per candidate

The first visual pass will use `images_bbox_review` as the complete visual
surface and use crops/bbox-both images where present. Cases `42` and `90` are
known priority cases where the complete review image exists but some crop/both
derivatives are absent.

## First-Pass Priority Cases

Review these cases first:

`12, 14, 16, 21, 42, 66, 67, 76, 77, 84, 88, 90, 97, 103, 155, 164, 166, 172`

These cover recovered recall, added false positives, dense sentinels, and
positive controls.

## FiftyOne Decision

Use static overlays/crops for the first pass. The visual artifacts already
exist and are enough to begin taxonomy work.

Escalate to FiftyOne only if:

- static review cannot classify the dominant FP/FN families
- the review expands beyond the priority slice
- patch-level visual browsing becomes too slow or error-prone

Plain Python import of `fiftyone` was not available during planning, while the
FiftyOne MCP entry exists. A later FiftyOne wave should first verify the active
runtime path and avoid treating FiftyOne evaluation as source truth.

## Next Gate

Before any new prompt candidate is written, complete:

- `visual_failure_taxonomy.csv`
- `v020c_v024l_delta_review.md`
- `prompt_addressability_summary` content inside the delta review

Only then choose whether the next prompt base is `v020c`, `v024l`, or a compact
hybrid.
