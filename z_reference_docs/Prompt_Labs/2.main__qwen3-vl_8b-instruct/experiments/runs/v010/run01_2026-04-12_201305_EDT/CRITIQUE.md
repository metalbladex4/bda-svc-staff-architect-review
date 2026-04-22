# Critique

## What We Checked

- frozen `v009` working baseline versus `v010`
- image: `tank.jpg`
- main experiment variable: detection bbox convention switched from `xyxy_1000` to `xyxy_pixels`

## What Improved

- nothing material improved on this seed case

## What Regressed

- detection collapsed to `object_not_found`
- bbox fell back to `[0, 0, 0, 0]`
- no debug overlay/crop artifacts were produced for the candidate because no targets were detected

## Main Weaknesses

1. The `_pixels` change was too disruptive for this image/model path when paired with the current prompt family.
2. This was not a mild bbox miss; it was a full detection failure.
3. The result suggests that changing the coordinate contract alone is not a safe next step for this stack.

## Decision

`reject direction`

- Keep `v006` + `v009` as the current best-known pair.
- Do not carry the `_pixels` convention forward as the default next tactic.
- If grounding remains the priority, the next research-backed move should be point-first or another code-supported refinement path rather than this direct coordinate-contract swap.
