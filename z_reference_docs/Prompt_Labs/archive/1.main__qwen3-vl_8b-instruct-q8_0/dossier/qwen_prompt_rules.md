# Qwen Prompt Rules

This note condenses the actionable guidance from the local Qwen references into
rules for `qwen3-vl:8b-instruct-q8_0` in this project.

## Primary Sources Reviewed

- `z_reference_docs/Prompting/Qwen/Qwen3-VL-8B-Instruct_Model_Card.md`
- `z_reference_docs/Prompting/Qwen/Qwen_3_Chat_template_deep_dive_Prompting_Behavior.md`
- `z_reference_docs/Prompting/Qwen/Alibaba_Cloud_vision_docs_for_Qwen-VL.md`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/2d_grounding.ipynb`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/spatial_understanding.ipynb`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/think_with_images.ipynb`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/ocr.ipynb`

## Working Rules

1. Keep the shared system prompt short and policy-only.
2. Put task mechanics in the user prompt, not the system prompt.
3. Use direct imperative wording instead of long explanatory prose.
4. Ask for output only once and keep it consistent with the actual runtime schema.
5. Preserve Qwen's 0–1000 relative coordinate convention for detection prompts.
6. Phrase localization tasks as explicit locating instructions.
7. Phrase output-only tasks with plain, narrow instructions such as “Return valid
   JSON only” or “Return plain text only.”
8. Treat multi-image input explicitly in the prompt when two images are passed.
9. Avoid tool-calling, XML wrappers, or agent-style prompts in this pipeline.
10. Avoid asking for visible reasoning traces or step-by-step analysis in the
    output.

## Prompt Surface Guidance

### System

- State only invariant operating policy.
- Enforce visual-only evidence, conservative judgment, and exact format
  compliance.
- Do not include task-specific bbox, doctrine, or summary mechanics here.

### Detect Objects

- Use direct grounding language: “Locate every instance that belongs to...”
- Keep label set explicit and closed.
- Specify one box per object, no duplicates, and valid 0–1000 integer coords.
- Avoid long internal thinking instructions unless a concrete experiment proves
  they help.

### Assess Damage

- State the target scope clearly: one selected object only.
- Refer to the two visual inputs by role, not by implementation detail.
- Keep doctrinal instruction explicit but subordinate to visible evidence.
- Require concise factual support phrases, not narrative analysis.

### Summarize Scene

- Treat target assessments as authoritative context.
- Keep the output short, plain text, and free of new unsupported claims.
- Any mention of broader impact must be conservative and anchored to the already
  assessed physical damage.

## Habits To Avoid

- Tool instructions such as “zoom,” “search,” or hidden function use.
- XML-heavy formatting patterns from unrelated tool-calling setups.
- Multiple competing schema descriptions in one prompt.
- Long “thinking process” blocks by default.
- Instructions that encourage functional, internal, or unseen-damage inference.
