# v039 Strategy State

- FP8 prompt working best remains `v034a_fp8_broad_context_scene_box_guard = 181 / 38 / 25 / 63` unless and until a non-promoted post-hoc line is separately implemented and validated.
- Best offline simulation decision: `B`.
- Next work: `v040_experiment_only_post_processing_tranche`.
- v040 should implement experiment-only post-processing, not product runtime, and compare metric-best `r020` against stricter same-label `r019`.
- Do not promote or treat this as product runtime behavior.
