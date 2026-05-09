# v040 Final Recommendation

Generated: `2026-05-09T17:49:15Z`

Decision `C`: hybrid rule beats or matches r020 with safer semantics.

Best rule: `hybrid`.
Best metrics: `181/38/22/60`.

r020 reproduced: `True` at `181/38/22/60`.
r019 reproduced: `True` at `181/38/23/61`.
Hybrid tested: `True` at `181/38/22/60`.

r020's cross-label case-100 removal is numerically helpful but semantically broader. The hybrid keeps the same 60-error result while requiring same-label or zero reference IoU for cross-label removals, so it is the preferred next experiment-only integration candidate.

Prompt wording should pause while experiment-only post-processing integration is explored. This is non-promoted evidence only and does not modify product runtime, prompt text, doctrine, assessment prompt, eval truth, or source truth.
