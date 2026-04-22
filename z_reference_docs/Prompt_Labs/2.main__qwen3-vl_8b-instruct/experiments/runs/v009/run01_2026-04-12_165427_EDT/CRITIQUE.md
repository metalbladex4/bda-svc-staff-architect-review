# v009 Critique

## Baseline Comparator

- primary comparator:
  `../v007/run02_2026-04-12_164250_EDT/`
- previous failed branch:
  `../../v008/run01_2026-04-12_165002_EDT/`

## What Improved

- Restored `DESTROYED`.
- Kept `PROBABLE`.
- Removed subtype drift from `brief_supporting_logic`.
- Kept logic focused on visible evidence instead of K-kill or repairability
  conclusions.

## What Did Not Improve

- The summary still says `dirt track`, which is not the best scene reading.
- The summary still reaches for complete loss / catastrophic framing even though
  the cycle goal was to tighten downstream moderation.
- Bbox behavior in this assessment cycle remained inherited/noisy and should not
  be treated as a signal from the `assess_damage` prompt alone.

## Main Weaknesses

1. Summary language is still the remaining weak point.
2. Assessment and summary are now out of balance: the target-level output is
   better calibrated than the scene-level text.
3. The cycle confirms that target-level calibration and summary calibration
   should now be separated.

## Research Questions

1. How should we constrain `summarize_scene` so it stays tightly bounded to the
   assessed category/confidence and avoids scene-context overreach?
2. What summary wording should be allowed for `DESTROYED` + `PROBABLE`?
3. Should the next cycle freeze `v009` as the assessment baseline and tune only
   `summarize_scene`?

## Decision

`keep direction`

- `v009` is the best target-level assessment prompt in cycle 02.
- Start the next cycle from `v009`.
- Move the active prompt surface to `summarize_scene`.
