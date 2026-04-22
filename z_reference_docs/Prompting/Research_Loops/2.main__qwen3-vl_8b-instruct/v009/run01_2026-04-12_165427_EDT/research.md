# Research Note: v009 loop 3

## Target Weakness

`v009` fixed the target-level assessment better than `v007` and `v008`, but the
scene summary still overreaches on terrain/context and functional-impact
language. The next cycle should move to `summarize_scene`.

## Research Questions

1. What prompt pattern best keeps a summary tightly bounded to prior assessed
   category/confidence?
2. How should we phrase scene-level impact when the target-level output is
   `DESTROYED` + `PROBABLE`?
3. What should be frozen from cycle 02 before the next cycle begins?

## Online Sources Used

1. Claude prompt engineering overview
   <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview>
2. Claude reduce hallucinations
   <https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations>
3. Qwen3-VL-8B-Instruct model card
   <https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct>

## Extracted Findings

- Anthropic's prompt-engineering overview continues to reinforce the core
  workflow we are using: define success criteria, test against them, and refine
  only the prompt-controlled failure.
- Anthropic's hallucination guide explicitly recommends iterative refinement and
  repeat comparison when outputs can drift, which matches the way we should
  evaluate summary wording in the next cycle.
- The Qwen3-VL model card emphasizes evidence-based multimodal reasoning. That
  supports pushing the summary prompt harder toward evidence-bounded restatement
  of already assessed damage rather than speculative scene interpretation.

## Local-Reference Reconciliation

Relevant local references re-reviewed:

- `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/dossier/doctrine_to_schema_crosswalk.md`
  - summary must not contradict target-level assessments
  - broader impact must stay conservative and anchored to assessed physical
    damage
- `z_reference_docs/BDAs/CJCSI 3162.02A METHODOLOGY FOR COMBAT ASSESSMENT July 2021.md`
  - category and confidence remain separate analytic dimensions

Working interpretation:

- Cycle 02 did enough to stabilize the target-level assessment on this seed
  case.
- The remaining overreach is now almost entirely in `summarize_scene`.

## Prompt Implications For The Next Cycle

1. Freeze `v009` as the best target-level assessment prompt for this seed case.
2. Keep `detect_objects` unchanged from the current active line.
3. Make the next cycle `summarize_scene` only.
4. Add a tighter summary contract that:
   - restates only assessed categories/confidence
   - avoids subtype inference from scene context
   - keeps functional impact conservative and category-bounded
