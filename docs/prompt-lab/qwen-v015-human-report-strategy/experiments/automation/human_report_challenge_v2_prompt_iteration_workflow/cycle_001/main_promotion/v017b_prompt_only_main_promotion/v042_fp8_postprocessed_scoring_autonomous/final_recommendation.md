# v042 Final Recommendation

Generated: `2026-05-09T18:56:12Z`

Status: `backend_unavailable`.

Best raw FP8 candidate: `v034a_fp8_broad_context_scene_box_guard` at `181/38/25/63`.

Best postprocessed FP8 candidate: `v034a_fp8_broad_context_scene_box_guard+p1753` at `181/38/24/62`.

Beat composite 62 errors: `False`.
Reached or beat old 58-error reference: `False`.
Reached <=1 target: `False`.

p1753 behavior: prediction-only same-label containment-first suppression; on frozen v034a it removes one case-88 FP and zero TPs.

Next axis: Restart or repair the vLLM FP8 endpoint at http://localhost:8000/v1 before v042 autonomy can continue.

FP8 remains a separate model line. This is experiment-only scoring evidence, not product runtime or promotion.
