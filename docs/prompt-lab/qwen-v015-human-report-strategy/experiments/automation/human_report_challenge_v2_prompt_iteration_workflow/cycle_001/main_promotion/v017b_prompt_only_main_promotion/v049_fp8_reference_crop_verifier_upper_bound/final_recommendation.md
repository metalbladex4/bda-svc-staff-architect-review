# v049 Final Recommendation

Generated: `2026-05-10T00:30:04Z`

Backend ran: `true`.

FN crops available/missing: `37` / `1`.

Verifier runs: `37`.

High-confidence recoverable: `0`.

Low-confidence recoverable: `34`.

Ambiguous: `0`.

Not recoverable: `3`.

Decision: `A`.

Main lesson: Many FNs are recognizable in reference-centered crops.

Next action: Run v050 non-oracle tiling/crop pass.

## Recoverability By Class

|fn_class|total_fns|crops_available|high_confidence_recoverable|low_confidence_recoverable|ambiguous|not_recoverable|missing|runtime_invalid|recommended_next_lever_note|
|---|---|---|---|---|---|---|---|---|---|
|adjacent_target_confusion|6|6|0|6|0|0|0|0|non-oracle tiling/crop pass|
|building_or_structure_piece|20|19|0|18|0|1|1|0|building-specific crop verifier/design|
|dense_valid_target_missed|6|6|0|6|0|0|0|0|dense/small non-oracle tiling strategy|
|edge_or_boundary_target|1|1|0|1|0|0|0|0|non-oracle tiling/crop pass|
|small_valid_target_missed|1|1|0|0|0|1|0|0|visual review/FiftyOne or no action|
|smoke_or_debris_obscured|4|4|0|3|0|1|0|0|non-oracle tiling/crop pass|

## Boundary

These are reference-centered crop results. They are diagnostic upper-bound evidence only, not deployable score, not product runtime, and not a replacement for old/product v020c.
