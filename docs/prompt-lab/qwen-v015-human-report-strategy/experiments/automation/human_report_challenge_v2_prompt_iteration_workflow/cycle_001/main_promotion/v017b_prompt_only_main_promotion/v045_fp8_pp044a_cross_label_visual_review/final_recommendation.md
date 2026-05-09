# v045 Final Recommendation

Generated: `2026-05-09T22:36:31Z`

pp044a visual review passed: `True`.

pp044a locked as experiment-only composite baseline: `True`.

Locked baseline: `fp8_composite_pp044a_baseline = 181 / 38 / 18 / 56`.

Best composite FP8 result after continuation: `pp045c_small_lower_building_context_probe = 181/38/11/49`.

Any intervention beat 56 errors: `True`.
Reached <=1 target: `False`.

## pp044a Visual Review

- Case 100: true false positive. The removed `military_equipment` box encloses a civilian-looking parked vehicle at the lower edge of a damaged building scene, not a military-equipment target. The cross-label rule is safe enough for experiment-only continuation but not deployable without further verifier/visual review.
- Case 155: duplicate/local artifact. The removed box is the known same-wreck duplicate nested inside the larger valid wreck body.

## Continuation

`pp045b` removes three case-28 tiny upper-right military-equipment false positives with zero TP removal: `181/38/15/53`.

`pp045c` then removes four small lower-building context false positives with zero TP removal: `181/38/11/49`.

Both pp045 probes are simulation-only until their removals receive visual review.

## Remaining Residual Classes

`adjacent_target_confusion, broad_context_scene_box, building_or_structure_piece, dense_valid_target_missed, small_valid_target_missed, smoke_or_debris_confusion, verifier_needed`.

Hard boundaries were preserved.
