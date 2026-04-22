# Cycle 02 Summary: Assessment Confidence And Summary Calibration

## Scope

- Cycle versions: `v007` to `v009`
- Active problem entering the cycle:
  downstream calibration after the confirmed `v006` bbox win
- Main goal:
  keep a strong target-level assessment without the `CONFIRMED` / K-kill /
  subtype drift that appeared in `v006`

## Loop Results

### `v007`

- Main change:
  conservative burn/smoke-aware `assess_damage`
- Result:
  - `damage_category`: `DAMAGED`
  - `confidence_level`: `PROBABLE`
  - removed K-kill language
  - removed subtype wording
- Takeaway:
  good direction on moderation, but too conservative on category

### `v008`

- Main change:
  abstract category-guidance block added to `assess_damage`
- Result:
  - still `DAMAGED`
  - still `PROBABLE`
  - subtype drift returned
- Takeaway:
  abstract category rules did not move the model; reject this wording family

### `v009`

- Main change:
  one example-driven `assess_damage` rule plus explicit generic-target wording
- Result:
  - `damage_category`: `DESTROYED`
  - `confidence_level`: `PROBABLE`
  - subtype drift removed from target-level logic
- Takeaway:
  best assessment prompt in the cycle; example-driven framing outperformed
  abstract category guidance

## What Improved Across The Cycle

- The cycle successfully separated category from confidence more cleanly than
  `v006`.
- `v009` restored `DESTROYED` without sliding back to `CONFIRMED`.
- K-kill / unrepairable language was removed from the best-so-far target-level
  assessment output.
- Target-level subtype drift was removed in the best-so-far version.

## What Did Not Improve Enough

- Scene summary still overreaches on context:
  - terrain/track wording can drift
  - functional-impact language still reaches toward complete loss
- Bbox behavior during the assessment cycle remained noisy / inherited and
  should not be treated as a clean assessment-surface signal

## Current Best-So-Far

- Detection family:
  `v006`
- Assessment family:
  `v009`

Working interpretation:

- On this seed case, `v006` + `v009` is the strongest combined prompt direction
  we have so far.
- The next cycle should not continue adjusting `assess_damage` first.
- The next cycle should move to `summarize_scene`.

## Recommended Next Cycle

### Primary surface

- `summarize_scene`

### Freeze these

- `detect_objects` from `v006`
- `assess_damage` from `v009`

### Next prompt goal

- keep the scene summary tightly bounded to already assessed
  category/confidence
- avoid subtype inference from rails / terrain / context
- make functional-impact wording conservative enough for
  `DESTROYED` + `PROBABLE`

## Post-Cycle Generalization Check

A later frozen `v006` + `v009` sweep across `tank.jpg`,
`destroyed_truck15.jpg`, `operational_truck4.jpg`, and `office.jpg` suggested
the pair generalizes reasonably on the truck and office scenes, but the tank
seed still wobbles across repeats. That means the cycle 02 recommendation to
move on from `assess_damage` is still useful, but the original tank case should
remain a repeatability pressure test before we call the current direction
fully finished.
