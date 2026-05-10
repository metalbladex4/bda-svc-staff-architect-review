# Recoverability By Class

|fn_class|total_fns|crops_available|high_confidence_recoverable|low_confidence_recoverable|ambiguous|not_recoverable|missing|runtime_invalid|recommended_next_lever|recommended_next_lever_note|
|---|---|---|---|---|---|---|---|---|---|---|
|adjacent_target_confusion|6|6|0|6|0|0|0|0|A|non-oracle tiling/crop pass|
|building_or_structure_piece|20|19|0|18|0|1|1|0|B|building-specific crop verifier/design|
|dense_valid_target_missed|6|6|0|6|0|0|0|0|C|dense/small non-oracle tiling strategy|
|edge_or_boundary_target|1|1|0|1|0|0|0|0|A|non-oracle tiling/crop pass|
|small_valid_target_missed|1|1|0|0|0|1|0|0|D|visual review/FiftyOne or no action|
|smoke_or_debris_obscured|4|4|0|3|0|1|0|0|A|non-oracle tiling/crop pass|
