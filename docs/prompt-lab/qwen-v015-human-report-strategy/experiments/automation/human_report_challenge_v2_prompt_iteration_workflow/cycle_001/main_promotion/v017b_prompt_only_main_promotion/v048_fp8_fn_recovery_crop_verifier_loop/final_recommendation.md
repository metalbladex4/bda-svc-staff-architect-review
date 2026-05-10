# v048 Final Recommendation

Generated: `2026-05-10T00:14:31Z`

All 38 FNs inventoried: `true`.

Locked baseline remains: `fp8_composite_pp045c_baseline = 181/38/11/49`.

pp046a remains diagnostic only: `181/38/0/38`; it failed visual lock in v047.

## Dominant FN Classes

|class|count|
|---|---|
|building_or_structure_piece|20|
|adjacent_target_confusion|6|
|dense_valid_target_missed|6|
|smoke_or_debris_obscured|4|
|edge_or_boundary_target|1|
|small_valid_target_missed|1|

## Crop/Verifier Result

Local-only crops/contact sheets were generated under `review_images/` for review. `37` of `38` FN crops were generated; case `40` / `40.png` was missing from the configured source-image root. The contact sheets were sanity-reviewed locally. These image files should not be pushed to the private review repo.

Verifier/tiling strategy completed: `true`.

Prompt candidate authored: `false`.

## Recommendation

Next work should be an experiment-only verifier or tiling/crop pass. Do not resume prompt wording until crop review isolates a narrow, low-risk, prompt-addressable FN cluster.

Hard boundaries were preserved.
