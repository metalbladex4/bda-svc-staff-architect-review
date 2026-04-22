# v008 Critique

## Baseline Comparator

- primary comparator:
  `../v007/run02_2026-04-12_164250_EDT/`
- historical target outcome to keep in view:
  `v006` detection win + downstream overconfidence

## What Improved

- Nothing material at the target-assessment level.
- The summary's functional-impact language became somewhat less absolute than
  earlier `complete loss` phrasing, but it did so by leaning harder into subtype
  inference.

## What Regressed

- `locomotive` drift returned in `brief_supporting_logic`.
- The summary again leans on a subtype-specific rail-logistics interpretation.

## Main Weaknesses

1. The new category guidance was too abstract; it did not recover
   `DESTROYED` at all.
2. The prompt gave the model room to infer a subtype again.
3. The result suggests that category calibration may need an example-based prompt
   pattern, not just more rules.

## Research Questions

1. Do official prompt guides recommend examples over abstract instructions when
   consistency is the failure mode?
2. What is the best way to forbid subtype inference while still allowing strong
   category judgments?
3. Should the next loop keep `assess_damage` as the active surface, or shift to
   `summarize_scene`?

## Decision

`reject direction`

- Do not carry forward the `CATEGORY GUIDANCE` block as written.
- Keep the broader cycle-2 direction of conservative confidence calibration.
- Next version should return to a shorter, more concrete prompt with one direct
  example and an explicit generic-target wording rule.
