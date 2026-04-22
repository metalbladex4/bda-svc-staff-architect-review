# Research Note: v007 loop 1

## Target Weakness

`v007` successfully removed confidence inflation and K-kill wording, but it
overcorrected by downgrading the target from `DESTROYED` to `DAMAGED`. The
summary also still overstates likely impact relative to the target-level
assessment.

## Research Questions

1. How should we phrase a prompt so `DESTROYED` can remain available at
   `PROBABLE` confidence when fire and smoke strongly suggest total loss but do
   not make every structural detail visible?
2. How should we constrain downstream wording so scene-level impact claims do
   not outrun the assessed category/confidence?
3. How should we interpret output drift when prompt text is unchanged and
   temperature is already `0.0`?

## Online Sources Used

1. Qwen3-VL 2D Object Grounding
   <https://mintlify.wiki/QwenLM/Qwen3-VL/examples/2d-grounding>
2. Qwen3-VL-8B-Instruct model card
   <https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct>
3. Claude prompt engineering overview
   <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview>
4. Claude reduce hallucinations
   <https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations>

## Extracted Findings

- Qwen's official 2D grounding examples stay short, direct, and task-specific.
  The examples focus on locating objects with bounding boxes/points rather than
  long prose rules.
- The Qwen3-VL model card emphasizes stronger 2D grounding, spatial perception,
  occlusion handling, and evidence-based answers. That supports keeping the
  assessment prompt concrete and evidence-led rather than speculative.
- Anthropic's prompt-engineering overview recommends treating prompt work as an
  eval-driven refinement process: define success first, then adjust only the
  controllable prompt failure.
- Anthropic's hallucination guide recommends explicit uncertainty, iterative
  refinement, and best-of-N verification when outputs can drift across runs. For
  our workflow, that supports documenting repeats instead of treating a single
  run as final truth.

## Local-Reference Reconciliation

Relevant local references reviewed after online research:

- `z_reference_docs/BDAs/CJCSI 3162.02A METHODOLOGY FOR COMBAT ASSESSMENT July 2021.md`
  - confidence definitions:
    `CONFIRMED (>=95%)`, `PROBABLE (50 to 94%)`, `POSSIBLE (<50%)`
  - equipment damage definitions:
    `DAMAGED` = visible deformation with major components still intact
    `DESTROYED` = unrepairable, catastrophic damage (K-kill)
- `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/dossier/doctrine_to_schema_crosswalk.md`
  - scene summary must not contradict target-level assessments
  - broader impact must stay conservative and anchored to assessed physical
    damage

Working interpretation:

- `v007` got the confidence behavior closer to the doctrine, but it made the
  category rule too strict for this seed case.
- The next prompt should explicitly separate:
  - category selection
  - confidence selection
- In particular, it should allow:
  - `DESTROYED` + `PROBABLE`
  when visible sustained engulfing fire strongly suggests catastrophic loss but
  some body details remain obscured.

## Prompt Implications For v008

1. Keep the `v007` caution that fire/smoke alone should not force
   `CONFIRMED`.
2. Add a category rule that sustained engulfing fire plus heavy smoke over the
   target body can still justify `DESTROYED` at `PROBABLE` confidence when the
   visible evidence strongly suggests catastrophic loss.
3. Keep `DAMAGED` for cases where major components remain visibly intact or the
   fire/damage looks limited.
4. Do not touch `detect_objects` yet.
5. Let summary remain unchanged for one more loop so we can see whether a better
   target-level assessment is enough to reduce downstream inconsistency.
