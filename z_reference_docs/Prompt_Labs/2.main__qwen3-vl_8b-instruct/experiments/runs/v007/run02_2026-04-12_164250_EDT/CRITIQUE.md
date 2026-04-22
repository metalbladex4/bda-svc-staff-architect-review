# v007 Critique

## Baseline Comparators

- `v006` confirmed detection winner:
  `../../../../runs/v006/run02_2026-04-12_163359_EDT/`
- `v007` repaired comparison run:
  `./`
- historical reference points:
  - `v001`
  - `v002`
  - `v003`

## What Improved

- Confidence softened from the strongest `v006` outcome (`CONFIRMED`) to
  `PROBABLE`.
- `brief_supporting_logic` removed K-kill, unrepairable, and subtype-heavy
  wording.
- The summary no longer says `dirt or gravel road`; it now at least identifies a
  track context.

## What Regressed

- `damage_category` moved from `DESTROYED` to `DAMAGED`.
- The summary still says the likely functional impact is complete loss of
  operational capability, which is too strong relative to `DAMAGED` /
  `PROBABLE`.
- The `v006_working_baseline` condition again returned the older bbox despite a
  `v006` prompt-equivalent effective config, so bbox behavior should be treated
  cautiously in this loop.

## Main Weaknesses

1. The revised assessment prompt overcorrected and made the category too
   conservative for a target that is visibly engulfed in sustained fire.
2. Summary generation is still willing to restate stronger impact language than
   the target-level evidence cleanly supports.
3. Repeatability remains imperfect even when prompt text is held constant.

## Research Questions

1. How can we permit `DESTROYED` with `PROBABLE` confidence when sustained fire
   strongly suggests total loss but the target body is partially obscured?
2. What prompt pattern best keeps downstream summary impact language bounded to
   the assessed category and confidence?
3. Which repeatability guardrails are recommended when prompt-level outputs can
   vary even with temperature held at `0.0`?

## Decision

`partial reuse only`

- Reuse:
  - conservative confidence framing
  - explicit ban on K-kill/unrepairable wording unless directly visible
- Revise next:
  - restore `DESTROYED` as an allowed `PROBABLE` outcome for sustained engulfing
    fire
  - tighten the summary's allowed functional-impact spillover
