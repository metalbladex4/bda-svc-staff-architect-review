# v044 Final Recommendation

Generated: `2026-05-09T22:08:48Z`

pp0157 visual review passed: `True`.

pp0157 locked as experiment-only composite baseline: `True`.

Locked baseline: `fp8_composite_pp0157_baseline = 181 / 38 / 20 / 58`.

Best composite FP8 result after continuation: `pp044a_contained_military_equipment_cross_label_probe = 181/38/18/56`.

Any intervention beat 58 errors: `True`.
Reached <=1 target: `False`.

## Recommendation

Continue experiment-only postprocessing/verifier work, not prompt wording. pp044a beats the 58-error reference in offline scoring, but it uses cross-label containment and must receive visual review before deployable integration.

## Four Case-66 Removals

- `target_0` `[45.0, 282.0, 62.0, 290.0]`: tiny_duplicate_or_local_artifact; Tiny far-tail convoy/road sliver before the first annotated reference target; low-risk extra box relative to current reference scope.
- `target_1` `[55.0, 280.0, 71.0, 291.0]`: tiny_duplicate_or_local_artifact; Tiny far-tail convoy/road sliver before the first annotated reference target; low-risk extra box relative to current reference scope.
- `target_2` `[65.0, 276.0, 84.0, 294.0]`: tiny_duplicate_or_local_artifact; Tiny far-tail convoy/road sliver before the first annotated reference target; low-risk extra box relative to current reference scope.
- `target_3` `[79.0, 273.0, 101.0, 296.0]`: tiny_duplicate_or_local_artifact; Tiny far-tail convoy/road sliver before the first annotated reference target; low-risk extra box relative to current reference scope.

## Remaining Residual Classes

`adjacent_target_confusion, broad_context_scene_box, building_or_structure_piece, dense_valid_target_missed, small_valid_target_missed, smoke_or_debris_confusion, verifier_needed`.

Hard boundaries were preserved.
