# v038 Final Recommendation

Generated: `2026-05-09T17:10:56Z`

Decision `D`: Simulation shows same-wreck duplicate suppression is unsafe or too local.

Best rule: `r001`.

Best metrics: `181/38/25/63`.

Beat v034a: `False`.
Reached or beat old 58-error reference: `False`.

Clarification: the requested grid produced no suppressions. The best rule is a safe no-op, and every swept rule left v034a unchanged. The known case-155 same-wreck duplicate has containment `1.0` but IoU approximately `0.083`, below the grid's minimum IoU threshold of `0.10`, so this tranche did not invalidate duplicate suppression as a post-processing idea. It only shows that the requested IoU-bounded grid cannot capture the v036-isolated duplicate class.

Next work should remain offline and experiment-only: run a containment-first simulation with lower or disabled IoU floors, or review the affected pairs in FiftyOne before any prompt wording or product runtime change.

This is non-promoted post-hoc evidence only. It does not modify product runtime, prompt text, doctrine, assessment prompt, eval truth, or source truth.
