# Best Residual Rule

`pp0157`: `181 / 38 / 20 / 58`.

## Rule

Family: `tiny_dense_prediction`

Prediction-only conditions:

- `target_type_filter = military_equipment`
- `same_label_required = true`
- `cross_label_allowed = false`
- `image_area_max = 0.001`
- `same_type_count_min = 5`
- `center_inside_required = true`
- `never_suppress_if_smaller_contains_prediction = true`

The rule does not use matched/unmatched state, reference boxes, best reference IoU, case IDs, or ground truth at inference time.

## Effect

- Starting composite: v034a + p1753 = `181 / 38 / 24 / 62`.
- Simulated result: `181 / 38 / 20 / 58`.
- Removed predictions: 4.
- Removed true positives: 0.
- Removed false positives: 4.
- Dense/control safety gates: no match loss, no FN increase, no case 67/84/110/155/166 worsening.

All four removals are very small `military_equipment` predictions in case 66:

- `[45, 282, 62, 290]`
- `[55, 280, 71, 291]`
- `[65, 276, 84, 294]`
- `[79, 273, 101, 296]`

## Interpretation

This reaches parity with the old/product 58-error reference as offline experiment-only postprocessing. It is not promotion-ready by itself: it is a narrow dense-cluster filter and should be visually reviewed against case 66 plus future FP8 outputs before any integration work.
