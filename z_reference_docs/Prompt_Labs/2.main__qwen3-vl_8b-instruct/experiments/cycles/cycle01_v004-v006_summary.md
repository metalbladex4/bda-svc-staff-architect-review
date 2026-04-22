# Cycle 01 Summary

## Scope

- Cycle ID: `cycle01_v004-v006`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Problem under test: `detect_objects` bbox grounding/localization
- Baseline anchor:
  `experiments/runs/baseline/run01_2026-04-10_205704_EDT/`

## Per-Loop Results

### `v004`

- Main change:
  fire/smoke as search cues, then box the visible body segment nearest the fire
  source
- Result:
  bbox `[51, 37, 102, 61]`, `PROBABLE`
- What improved:
  tighter right edge than baseline
- What failed:
  over-shrank upward and still missed the target body
  subtype drift worsened to `locomotive or rolling stock`
- Decision:
  reject direction; keep only the lesson that fire/smoke should remain search
  cues, not box boundaries

### `v005`

- Main change:
  point-first, occlusion-aware grounding prose
- Result:
  matched baseline exactly: bbox `[51, 37, 128, 73]`, `PROBABLE`
- What improved:
  no measurable change
- What failed:
  prompt was too weak to move the model at all
- Decision:
  reject as no-effect wording family

### `v006`

- Main change:
  shorter, more direct Qwen-style detection prompt with contrastive examples
- Result:
  bbox `[46, 46, 128, 92]`, `CONFIRMED`
- What improved:
  first candidate to move the box materially onto the visible burning target
  body
  removed `locomotive` subtype drift from supporting logic
- What failed:
  confidence rose to `CONFIRMED`
  supporting logic added `consistent with a K-kill`
  summary still misread the surface as a dirt/gravel road
- Decision:
  best-so-far bbox candidate, but not yet promoted

## Research Used Across The Cycle

Online sources:

- `https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct`
- `https://qwenlm.github.io/blog/qwen2.5-vl/`
- `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#use-examples-effectively`
- `https://www.catalyzex.com/paper/visually-prompted-benchmarks-are-surprisingly`

Local references re-used:

- `z_reference_docs/Prompting/Qwen/Alibaba_Cloud_vision_docs_for_Qwen-VL.md`
- `z_reference_docs/Prompting/Qwen/Qwen3-VL-8B-Instruct_Model_Card.md`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/2d_grounding.ipynb`
- `z_reference_docs/Prompting/Anthropic_Claude/Claude Prompt engineering be-clear-and-direct.md`
- `z_reference_docs/Prompting/Anthropic_Claude/Claude multishot-prompting Use examples (multishot prompting) to guide Claude_s behavior.md`
- `z_reference_docs/Prompting/VLM-Research-Papers/Visually Prompted Benchmarks Are Surprisingly Fragile.md`
- `z_reference_docs/BDAs/CJCSI 3162.02A METHODOLOGY FOR COMBAT ASSESSMENT July 2021.md`

## What Improved Across The Cycle

- The loop structure produced a clean paper trail for every candidate:
  run -> critique -> research -> next draft.
- The cycle separated two important failure modes:
  - wrong-direction movement (`v004`)
  - no-effect wording (`v005`)
- `v006` showed that a shorter, example-driven prompt can be more salient than
  abstract grounding prose for this image/model pair.

## What Did Not Improve Enough

- None of the candidates solved bbox grounding cleanly enough to promote
  without reservation.
- `v006` improved the box, but it also changed downstream confidence and
  summary behavior.
- The seed image is still a single, very small localization case, so broader
  confidence in the tactic remains limited.

## Current Best-So-Far Version

- Best bbox candidate:
  `v006_detect_objects_short-contrastive-example.yaml`

Why:

- It is the first candidate to move the bbox materially onto the visible target
  body instead of mostly off-target terrain/context.

Why not promoted:

- downstream confidence inflation and stronger summary language still need
  review

Confirmation update:

- `v006` run02 matched `run01` exactly, so the bbox improvement is now
  confirmed on the current seed case.

## Recommended Next Step

The original bbox problem is not fully closed yet, but `v006` is strong enough
to justify one confirmation repeat before another redesign cycle.

Recommended next action:

1. shift the next prompt problem from detection localization to downstream
   confidence/summary calibration
2. keep the short, contrastive-example `v006` detection style as the current
   leading detection baseline for this seed case
3. do not promote `v006` into the live config yet until the downstream
   calibration issues are addressed
