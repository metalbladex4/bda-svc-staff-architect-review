# Research Note: v010 prep

## Target Weakness

The current best pair (`v006` detection + `v009` assessment) is broadly useful,
but the tank seed still wobbles on grounding and bbox placement. Before we move
to summary tuning, we need to test whether the remaining grounding problem is
partly caused by the normalized `xyxy_1000` coordinate contract rather than by
prompt wording alone.

## Research Questions

1. Do Qwen grounding examples align better with image-space coordinates than
   with normalized coordinates?
2. Is `_pixels` a reasonable next experiment before more prompt-only rewrites?
3. What should the next escalation path be if `_pixels` still does not fix the
   grounding issue?

## Online Sources Used

Official/vendor sources:

- Qwen2.5-VL blog:
  <https://qwenlm.github.io/blog/qwen2.5-vl/>
- Qwen-VL paper:
  <https://arxiv.org/abs/2308.12966>
- Qwen2-VL paper:
  <https://arxiv.org/abs/2409.12191>
- Qwen2.5-VL report:
  <https://arxiv.org/abs/2502.13923>
- Ollama structured outputs:
  <https://docs.ollama.com/capabilities/structured-outputs>

Primary research:

- Set-of-Mark Prompting Unleashes Extraordinary Visual Grounding in GPT-4V:
  <https://arxiv.org/abs/2310.11441>
- Visually Prompted Benchmarks Are Surprisingly Fragile:
  <https://arxiv.org/abs/2512.17875>

Community field evidence:

- llama.cpp Qwen3-VL grounding issue:
  <https://github.com/ggml-org/llama.cpp/issues/17131>
- sglang Qwen grounding degradation issue:
  <https://github.com/sgl-project/sglang/issues/11896>
- vLLM Qwen grounding regression issue:
  <https://github.com/vllm-project/vllm/issues/29595>

## Extracted Findings

- Qwen's public grounding examples are short, direct, and use native
  `bbox_2d` or `point_2d` outputs rather than long prose-heavy localization
  instructions.
- The public Qwen grounding examples are image-space oriented, which makes a
  code-supported `_pixels` experiment more justified than another abstract
  wording-only revision on `xyxy_1000`.
- Ollama's structured-output guidance reinforces keeping the schema strong and
  the temperature low, which we already do.
- The SoM paper suggests that if prompt-only grounding stalls, a visually
  marked or two-pass strategy may unlock gains that text-only prompting does
  not.
- The fragility literature and community issue reports reinforce that grounding
  failures can be sensitive to low-level inference details, so prompt structure
  should not be treated as the only remaining variable.

## Local-Reference Reconciliation

Relevant local references re-reviewed:

- `z_reference_docs/Prompting/Qwen/Qwen3-VL-8B-Instruct_Model_Card.md`
  - stays consistent with the view that Qwen is grounding-capable, but does
    not argue for long abstract localization prompts
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/2d_grounding.ipynb`
  - remains the strongest local signal for short, direct grounding requests
- `z_reference_docs/Prompting/Qwen/Alibaba_Cloud_vision_docs_for_Qwen-VL.md`
  - remains consistent with the current multi-image chat structure
- `z_reference_docs/Prompting/VLM-Research-Papers/Visually Prompted Benchmarks Are Surprisingly Fragile.md`
  - reinforces caution about over-reading one apparent grounding win

## Prompt Implications For The Next Cycle

1. Re-open grounding as the primary problem before summary tuning.
2. Freeze `assess_damage` at `v009` while testing the next detection step.
3. Start with a code-supported `xyxy_pixels` experiment before another major
   prompt rewrite.
4. Keep the prompt short and direct; do not return to the long abstract
   grounding blocks that already underperformed.
5. If `_pixels` does not help enough, escalate next to a point-first or
   code-level grounding aid rather than another minor prose shuffle.
