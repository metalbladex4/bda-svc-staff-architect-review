# v043 Final Recommendation

Generated: `2026-05-09T20:45:10Z`

Best composite FP8 result: `pp0157` at `181 / 38 / 20 / 58`.

Any intervention beat 62 errors: `true`.
Reached or beat old 58-error reference: `true`.
Reached <=1 target: `false`.

Winning intervention type: `postprocess_simulation`.

## Recommendation

Continue the FP8 model line as experiment-only postprocessed scoring, but pause near-neighbor prompt wording. `pp0157` reaches the old/product 58-error reference by removing four residual case-66 false positives with zero true-positive removals and no match/FN regression.

The result is not a product promotion and not runtime integration evidence. The next tranche should visually review the four case-66 removals and design a crop/verifier check before any wider integration against future FP8 outputs.

## Residual Classes

Remaining residual error classes: `adjacent_target_confusion`, `broad_context_scene_box`, `building_or_structure_piece`, `contained_duplicate_prediction`, `dense_valid_target_missed`, `oversized_group_box`, `small_valid_target_missed`, `smoke_or_debris_confusion`, `verifier_needed`.

## Controls

- Case 66 improved from `8 / 0 / 5` to `8 / 0 / 1`.
- Case 67 stayed `10 / 1 / 3`.
- Case 84 stayed `8 / 5 / 0`.
- Case 100 stayed `1 / 2 / 1`.
- Case 110 stayed `3 / 4 / 1`.
- Case 155 stayed `2 / 0 / 1`.
- Case 166 stayed `1 / 0 / 0`.
- Office-negative was not rerun because v043 was offline-only over frozen outputs.
