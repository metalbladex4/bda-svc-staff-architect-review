# Research Note

## Loop Context

- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under review: `v004`
- Run folder: `run01_2026-04-12_155635_EDT`
- Target weakness:
  `v004` shrank around the fire-adjacent patch instead of recovering the
  visible target body.

## Research Questions

1. What do official Qwen grounding references suggest about point-first or
   center-first localization for partially occluded objects?
2. How should occlusion-aware localization be phrased so the model recovers the
   visible attached body segment instead of the nearest burning patch?
3. What prompt wording helps keep the output at doctrinal `target_type` rather
   than drifting into a subtype like `locomotive`?

## Online Sources Used

Official/vendor sources first:

- Qwen3-VL-8B-Instruct model card:
  `https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct`
- Alibaba Cloud Model Studio Qwen-VL vision docs:
  `https://www.alibabacloud.com/help/en/model-studio/qwen-vl-compatible-with-openai`
- Qwen2.5-VL official blog:
  `https://qwenlm.github.io/blog/qwen2.5-vl/`

Primary paper / research:

- `Visually Prompted Benchmarks Are Surprisingly Fragile` overview:
  `https://www.catalyzex.com/paper/visually-prompted-benchmarks-are-surprisingly`

## Extracted Findings

### Official Qwen findings

- Qwen3-VL emphasizes stronger 2D grounding and better spatial reasoning under
  occlusion, so the next draft should use language that makes the object body
  recovery step explicit rather than hoping the model infers it.
- Official Qwen localization examples are short, direct, and format-specific.
  They ask the model to locate a target and return coordinates in a fixed
  format rather than layering long negative-rule prose.
- Qwen documentation supports both bounding-box localization and point-based
  localization. That makes a point-or-center-first grounding strategy a
  reasonable prompt move even though the pipeline still needs bbox output.
- Qwen2.5-VL docs warn that localization is most robust in the rough
  `480x480` to `2560x2560` range. Our `tank.jpg` seed image is smaller than
  that, so prompt-only improvements may be real but limited.

### Research finding

- Visually prompted evaluation can be fragile to seemingly small changes.
  That reinforces the need to compare against baseline every time and to avoid
  treating a single numeric bbox shift as a win without overlay review.

## Local Reference Re-Review

Relevant local references re-reviewed after the online pass:

- `z_reference_docs/Prompting/Qwen/Alibaba_Cloud_vision_docs_for_Qwen-VL.md`
  - confirmed 2D bbox plus center-point localization support
  - confirmed Qwen3-VL uses normalized `[0, 999]` coordinates
  - confirmed the resolution warning about bbox drift outside the robust range
- `z_reference_docs/Prompting/Qwen/Qwen3-VL-8B-Instruct_Model_Card.md`
  - confirmed stronger 2D grounding and occlusion handling are part of the
    model positioning
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/2d_grounding.ipynb`
  - confirmed official examples stay concise and use direct localization asks
  - confirmed point-based grounding is an official usage pattern
- `z_reference_docs/Prompting/VLM-Research-Papers/Visually Prompted Benchmarks Are Surprisingly Fragile.md`
  - reinforced that prompt/image localization behavior can shift on small
    design changes and should be checked with repeated visual review

## Prompt Implications For The Next Version

- Keep `detect_objects` as the only changed surface.
- Parent the next draft from `v000`, not from `v004`.
- Use a point-or-center-first grounding instruction:
  identify the visible object body center first, then expand to the smallest
  bbox that covers the attached visible man-made body segment.
- Make occlusion handling explicit:
  if fire or smoke obscures part of the target, recover the attached visible
  body segment rather than the nearest burning patch.
- Add one short, direct example instead of a long block of negative rules.
- Explicitly forbid subtype guesses from rail context in the detection task so
  later assessment and summary text have less room to drift toward
  `locomotive`.
