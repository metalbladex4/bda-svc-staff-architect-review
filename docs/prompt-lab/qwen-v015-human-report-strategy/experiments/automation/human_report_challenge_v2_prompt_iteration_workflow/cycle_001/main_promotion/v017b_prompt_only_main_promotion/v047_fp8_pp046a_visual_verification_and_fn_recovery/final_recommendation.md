# v047 Final Recommendation

Generated: `2026-05-09T23:30:21Z`

pp046a visual review passed: `False`.

pp046a locked as experiment-only composite baseline: `False`.

Selected locked baseline: `fp8_composite_pp045c_baseline = 181/38/11/49`.

Diagnostic pp046a score: `181/38/0/38`.

Reached <=1 target: `False`.

## pp046a Visual Review

Safe removals: cases `19`, `77`, `97`, `103`, `105`, and `110` looked like context artifacts or non-target structure.

Unsafe or ambiguous removals: case `66` target_4, case `67` targets 0-2, and case `92` target_1 look visually plausible as real military equipment or dense-row targets. pp046a therefore fails the visual lock gate.

## Residual FN Classes

`building_or_structure_piece, dense_valid_target_missed, small_valid_target_missed, smoke_or_debris_obscured, unknown`.

## Next Work

Do verifier/tiling/crop review before another prompt. No optional prompt candidate was authored.

Hard boundaries were preserved.
