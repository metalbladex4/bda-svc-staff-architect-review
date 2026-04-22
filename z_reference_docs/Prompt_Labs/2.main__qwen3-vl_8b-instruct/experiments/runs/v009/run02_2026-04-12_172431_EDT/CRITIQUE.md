# Generalization Critique

## What We Checked

- current-main baseline versus frozen `v006` detection + `v009` assessment
- images:
  - `tank.jpg`
  - `destroyed_truck15.jpg`
  - `operational_truck4.jpg`
  - `office.jpg`

## What Improved

- The frozen pair handled the operational truck cleanly with `NO DAMAGE`.
- The frozen pair stayed sensible on the destroyed-truck scene.
- The frozen pair did not hallucinate targets in the office scene.

## What Regressed

- The tank seed did not stay stable across runs:
  - an earlier `v009` run on tank produced `DESTROYED`
  - this repeat produced `DAMAGED`
- That means we should not treat the tank result as fully settled yet.

## Main Weaknesses

1. The current prompt pair is not fully repeatable on the original seed case.
2. The cross-image sweep suggests the prompt is reasonably general, but the tank
   case remains the pressure point.
3. We still need a repeatability-oriented check before declaring the current
   detection/assessment direction finished.

## Decision

`keep direction`

- Keep the frozen pair as the best-known prompt direction for now.
- Do not make a new prompt version from this sweep alone.
- Use the sweep as evidence that the prompt is not obviously tank-only, while
  also acknowledging that the tank seed still needs one more stability check.
