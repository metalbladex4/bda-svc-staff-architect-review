# v042 Final Recommendation

Generated: `2026-05-09T20:00:28Z`

Status: `rejected`.

Best raw FP8 candidate: `v034a_fp8_broad_context_scene_box_guard` at `181/38/25/63`.

Best postprocessed FP8 candidate: `v034a_fp8_broad_context_scene_box_guard+p1753` at `181/38/24/62`.

Beat composite 62 errors: `False`.
Reached or beat old 58-error reference: `False`.
Reached <=1 target: `False`.

p1753 behavior: prediction-only same-label containment-first suppression; on frozen v034a it removes one case-88 FP and zero TPs.

No live v042 prompt candidate passed the micro-pack gate. v042a, v042b, v042c, v042d, and v042e were rejected at micro-pack before full all-current/no101.

Next axis: pause near-neighbor prompt wording and move to verifier/postprocessing or visual review of remaining v034a+p1753 deltas.

FP8 remains a separate model line. This is experiment-only scoring evidence, not product runtime or promotion.
