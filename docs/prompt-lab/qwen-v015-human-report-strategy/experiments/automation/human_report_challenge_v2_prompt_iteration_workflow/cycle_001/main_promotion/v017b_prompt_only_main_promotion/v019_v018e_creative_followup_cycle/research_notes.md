# v019 Research Notes

Purpose: prompt-method inspiration only. Capstone source artifacts, manifests,
runner summaries, and review packets remain the authority for decisions.

## Online Sources Checked

- Qwen2.5-VL official blog:
  <https://qwenlm.github.io/blog/qwen2.5-vl/>
  - Useful because Qwen-VL family models are intended to support visual
    grounding and structured localization outputs. For v019, this supports
    preserving direct JSON bbox output and keeping prompt language explicit
    about coordinate/box format.
- Set-of-Mark Prompting:
  <https://arxiv.org/abs/2310.11441>
  - Useful as inspiration for spatial partitioning and attention guidance.
    v019 does not modify images or add visual markers; it borrows the idea of
    silent spatial scanning and spatially explicit candidate review.
- LVLM hallucination survey:
  <https://arxiv.org/abs/2402.00253>
  - Useful for the prompt-level idea that detections should survive a visual
    evidence check instead of being inferred from context.
- Multimodal reasoning hallucination paper:
  <https://arxiv.org/abs/2505.21523>
  - Useful for the idea that reasoning-like prompts can increase confidence in
    unsupported guesses, so v019 keeps final output terse and makes all
    internal critique silent.

## Local Evidence Used

- v018 final recommendation and comparison matrix.
- `v018d_evidence_budget_pruner` as recall ceiling.
- `v018e_contrastive_body_anchor` as precision-balanced follow-up axis.
- Graphify/project-brain recall for v018 no-adopt status.

## Prompt-Method Implications

- Keep JSON output discipline and required prompt placeholders.
- Prefer silent spatial scanning over visible chain-of-thought.
- Add adversarial/veto checks against context-only boxes.
- Do not turn the prompt into a long rule wall that suppresses ordinary recall.
