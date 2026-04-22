# Research Note

## Loop Context

- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under review: `v006`
- Run folder: `run01_2026-04-12_162217_EDT`
- Target weakness:
  `v006` improved bbox grounding, but it also raised confidence and produced
  stronger summary language.

## Research Questions

1. How should we interpret a detection-only prompt that improves grounding but
   changes downstream assessment behavior?
2. Do official/primary sources suggest requiring confirmation repeats before
   treating a single improved run as a win?
3. What problem should be next if `v006` becomes the leading bbox candidate?

## Online Sources Used

Official/vendor sources first:

- Qwen3-VL-8B-Instruct model card:
  `https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct`
- Anthropic prompt best practices:
  `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#use-examples-effectively`

Primary paper / research:

- `Visually Prompted Benchmarks Are Surprisingly Fragile` overview:
  `https://www.catalyzex.com/paper/visually-prompted-benchmarks-are-surprisingly`

## Extracted Findings

### Prompt-design finding

- The fact that `v006` is the first candidate to move the box materially after
  `v005` matched baseline supports the idea that shorter, example-driven
  steering can be more salient than abstract instruction blocks.

### Evaluation finding

- The fragility literature reinforces that a single visually improved run is
  not enough to declare victory. Small prompting changes can produce unstable
  behavior, so confirmation repeats still matter.

## Local Reference Re-Review

Relevant local references re-reviewed after the online pass:

- `z_reference_docs/Prompting/VLM-Research-Papers/Visually Prompted Benchmarks Are Surprisingly Fragile.md`
  - reinforced that visual-prompt gains should be treated cautiously until
    repeated
- `z_reference_docs/Prompting/Anthropic_Claude/Claude multishot-prompting Use examples (multishot prompting) to guide Claude_s behavior.md`
  - remained consistent with the apparent `v006` improvement from a more
    example-driven prompt
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/2d_grounding.ipynb`
  - remained consistent with the short, direct grounding style used in `v006`
- `z_reference_docs/BDAs/CJCSI 3162.02A METHODOLOGY FOR COMBAT ASSESSMENT July 2021.md`
  - reinforced caution around stronger downstream claims when the prompt change
    itself was only in detection

## Prompt Implications For The Next Step

- Treat `v006` as the current best bbox candidate, not as a promoted winner.
- If continuing immediately, run one confirmation repeat of `v006` before
  accepting the bbox improvement as stable.
- If the repeat holds, the next prompt problem should shift from detection
  localization to downstream confidence/summary calibration.
