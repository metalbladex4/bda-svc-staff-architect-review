# Phase-1-Only Doctrine Rules

This rule set constrains the doctrine replacement effort so it stays compatible
with the current pipeline and the prompt-engineering method already in use.

## Scope Rules

The candidate doctrine file may support only:

- visible target identification under existing doctrinal categories
- visible physical damage categorization
- short doctrinal considerations that help interpret visible evidence

It must not introduce:

- functional damage assessment
- target-system assessment
- recuperation estimates
- restrike or reattack logic
- MEA logic
- intelligence conclusions beyond what is visible

## Runtime Rules

- Keep the existing top-level doctrine categories:
  - `buildings`
  - `military_equipment`
- Keep the existing per-category keys:
  - `detection_guidance`
  - `physical_damage_definitions`
  - `physical_damage_considerations`
- Do not change the prompt placeholders or the doctrine formatting utilities in
  round one.

## Prompt-Fit Rules

- The doctrine file is not a place for all-source reasoning.
- The doctrine file should help the model interpret visible evidence, not
  replace the visual-only guardrails already in the prompts.
- Shorter, clearer, doctrine-faithful paraphrase is acceptable when it improves
  prompt behavior.
- Detection guidance may remain practical and operational, but PDA text should
  stay doctrinally grounded.

## Confidence Rules

The broader doctrine includes confidence concepts, but in the current runtime:

- confidence is enforced mainly by prompt text, not by `doctrine.yaml`
- the doctrine candidate should therefore avoid inserting broad confidence
  frameworks that are not already supported by the live prompt contract

## Replacement Rule

The candidate doctrine can only replace the live doctrine if it is both:

- more faithful to the Phase-1 PDA sources that matter for this runtime
- at least as safe on the known prompt/eval controls
