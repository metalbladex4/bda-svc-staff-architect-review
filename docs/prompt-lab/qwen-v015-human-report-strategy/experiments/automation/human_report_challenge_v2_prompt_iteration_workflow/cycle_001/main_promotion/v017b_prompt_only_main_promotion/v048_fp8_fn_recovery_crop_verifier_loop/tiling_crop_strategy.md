# Tiling Crop Strategy

Recommendation: use an experiment-only crop/tiling pass before prompt wording.

Start with `2x2 overlapping tiles plus center crop` and overlap `0.2`. Merge mapped boxes only through strict verifier and postprocessing gates.

## Class Targets

|class|strategy|
|---|---|
|dense_valid_target_missed|tiling plus same-type verifier|
|small_valid_target_missed|tiling/crop pass|
|smoke_or_debris_obscured|crop verifier only, with conservative reject rules|
|building_or_structure_piece|manual visual review and verifier design, not automatic add|
|unknown|FiftyOne or contact-sheet review before live model work|
