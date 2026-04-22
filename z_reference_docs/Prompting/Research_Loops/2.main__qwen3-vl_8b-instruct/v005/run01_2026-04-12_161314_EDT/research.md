# Research Note

## Loop Context

- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under review: `v005`
- Run folder: `run01_2026-04-12_161314_EDT`
- Target weakness:
  the point-first, occlusion-aware prompt matched the baseline output exactly
  and did not change localization behavior.

## Research Questions

1. When a longer grounding prompt is ignored, do official guides recommend
   shorter, more direct instructions plus examples?
2. Would contrastive examples make the desired bbox behavior more salient than
   abstract grounding prose alone?
3. How can example-driven steering help suppress subtype drift from rail or
   rolling-stock context?

## Online Sources Used

Official/vendor sources first:

- Qwen3-VL-8B-Instruct model card:
  `https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct`
- Qwen2.5-VL official blog:
  `https://qwenlm.github.io/blog/qwen2.5-vl/`
- Anthropic prompt best practices:
  `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#use-examples-effectively`

## Extracted Findings

### Official Qwen findings

- Official Qwen localization examples stay compact and concrete:
  `Locate ... Report bbox coordinates in JSON format.`
- Qwen already supports multi-target grounding and point-based localization, so
  the lack of movement in `v005` does not point to a missing capability. It
  points to our prompt not being salient enough.
- The smaller-than-recommended seed image still means prompt-only gains may be
  modest, so sharper prompt steering matters.

### Official prompting finding

- Anthropic's official best-practices page emphasizes that examples are one of
  the most reliable ways to steer output structure and behavior, and that
  instructions should be clear, specific, and sequential when order matters.

## Local Reference Re-Review

Relevant local references re-reviewed after the online pass:

- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/2d_grounding.ipynb`
  - confirmed official Qwen grounding prompts are short and direct
  - confirmed point-format and bbox-format are both supported grounding styles
- `z_reference_docs/Prompting/Qwen/Alibaba_Cloud_vision_docs_for_Qwen-VL.md`
  - reinforced that Qwen supports both bbox and point localization and warns
    about drift outside the robust resolution range
- `z_reference_docs/Prompting/Anthropic_Claude/Claude Prompt engineering be-clear-and-direct.md`
  - reinforced that bloated or hedged instruction phrasing can reduce steering
    strength
- `z_reference_docs/Prompting/Anthropic_Claude/Claude multishot-prompting Use examples (multishot prompting) to guide Claude_s behavior.md`
  - reinforced that examples are a strong way to steer edge cases and desired
    output behavior

## Prompt Implications For The Next Version

- Keep `detect_objects` as the only changed surface.
- Parent the next draft from `v000`, not from `v005`.
- Make the prompt shorter and more direct than `v005`.
- Add one or two contrastive examples that explicitly separate:
  - correct bbox behavior on the visible connected body
  - incorrect bbox behavior on plume, rail bed, or empty ground
- Keep the explicit rule that only the doctrinal `target_type` should be
  returned, never a finer subtype.
