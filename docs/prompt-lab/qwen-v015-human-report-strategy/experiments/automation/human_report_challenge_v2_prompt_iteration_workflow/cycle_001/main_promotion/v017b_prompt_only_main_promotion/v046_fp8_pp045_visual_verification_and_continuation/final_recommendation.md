# v046 Final Recommendation

Generated: `2026-05-09T23:10:42Z`

pp045b visual review passed: `True`.

pp045c visual review passed: `True`.

Selected experiment-only locked baseline: `fp8_composite_pp045c_baseline = 181 / 38 / 11 / 49`.

Best simulation FP8 result after continuation: `pp046a_prediction_only_residual_fp_cleanup_probe = 181/38/0/38`.

Any intervention beat 49 errors: `True`.
Any locked intervention beat 49 errors: `False`.
Reached <=1 target: `False`.

## Visual Review Summary

pp045b case-28 removals are tiny upper-right roadway/side artifacts around distant traffic, not military-equipment targets.

pp045c removals are intact or background/adjacent building context patches in cases 105, 17, 57, and 86, not damaged target bodies.

## Continuation

`pp046a` removes all eleven remaining residual FPs and reaches `181/38/0/38` in frozen scoring with no match/FN loss and `0` after-the-fact TP removals. It is simulation-only until visually reviewed.

## Remaining Residual Classes

`building_or_structure_piece, dense_valid_target_missed, small_valid_target_missed, smoke_or_debris_confusion`.

Hard boundaries were preserved.
