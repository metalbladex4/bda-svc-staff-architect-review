# v043 Residual Visual Review Plan

The next review should inspect the four `pp0157` removed case-66 predictions against the reference and raw/postprocessed overlays, then sample remaining FP clusters in cases 67, 97, 100, 103, 110, and 155.

Review questions:

- Are the four removed case-66 predictions visually separate valid targets or tiny local over-splits?
- Would the `image_area_max <= 0.001` and `same_type_count_min >= 5` rule be unsafe on another dense military-equipment image?
- Can a crop verifier reject these four FPs without suppressing the valid small missed targets in cases 67, 84, 110, 141, and 146?
- Should `pp0157` be tested as an experiment-only wrapper on the next FP8 candidate output before any product-runtime discussion?

Do not use this plan as source truth or promotion evidence; it is a review queue for the next experiment tranche.
