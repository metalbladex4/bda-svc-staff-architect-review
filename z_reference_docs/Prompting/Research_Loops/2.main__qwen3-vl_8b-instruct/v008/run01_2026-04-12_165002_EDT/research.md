# Research Note: v008 loop 2

## Target Weakness

`v008` added explicit category guidance, but it did not recover `DESTROYED` and
it reintroduced subtype drift (`locomotive`). The failure mode now looks like
prompt consistency rather than missing doctrinal rules.

## Research Questions

1. Are examples more effective than abstract rules for output consistency?
2. How should we bound the model to generic target wording instead of subtype
   inference?
3. What slight prompt change best fits the next loop without changing code or
   the live runtime contract?

## Online Sources Used

1. Claude increase output consistency
   <https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency>
2. Claude prompt engineering overview
   <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview>
3. Qwen3-VL 2D Object Grounding
   <https://mintlify.wiki/QwenLM/Qwen3-VL/examples/2d-grounding>
4. Qwen3-VL-8B-Instruct model card
   <https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct>

## Extracted Findings

- Anthropic's consistency guide explicitly recommends examples when consistency
  is the main failure mode; examples often constrain behavior better than
  abstract instructions alone.
- The same guide also recommends retrieval/context grounding and prompt chaining
  when a task has multiple related subtasks. That supports our split workflow:
  target assessment first, scene summary second.
- Anthropic's prompt overview still recommends eval-driven refinement in order,
  rather than piling up many speculative changes at once.
- Qwen's official grounding docs remain short and example-like. They do not rely
  on long doctrinal prose to demonstrate the task.

## Local-Reference Reconciliation

Relevant local references re-reviewed:

- `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/dossier/doctrine_to_schema_crosswalk.md`
  - `brief_supporting_logic` should stay generic, visible-evidence only
  - scene summary should not contradict target-level outputs
- `z_reference_docs/BDAs/CJCSI 3162.02A METHODOLOGY FOR COMBAT ASSESSMENT July 2021.md`
  - `DESTROYED` and `DAMAGED` remain the doctrinal anchors
  - confidence remains separate from category

Working interpretation:

- The problem is no longer missing doctrine.
- The problem is that the model is not mapping the doctrine consistently under
  the current assessment prompt style.
- A direct example is more promising than another abstract rule block.

## Prompt Implications For v009

1. Keep `v007` as the best assessment parent, not `v008`.
2. Stay on `assess_damage` for one more loop.
3. Replace abstract category guidance with one short example showing the exact
   desired output shape:
   - `DESTROYED`
   - `PROBABLE`
   - generic target wording
   - no subtype, no K-kill, no complete-loss claim
4. Add an explicit wording rule:
   - in `brief_supporting_logic`, refer to the object as `target`,
     `target body`, or `equipment`, not a subtype inferred from rails or scene
     context.
