# v038 Best Simulation Report

Best safe rule: `r001`

Metrics: `181/38/25/63`.

Rule: containment >= `0.7`, IoU >= `0.1`, area ratio <= `0.05`, center-inside `True`, same-label `True`, larger-matched-only `True`.

Removed boxes: `0`.

Interpretation: this is a no-op safe rule, not an improving duplicate-suppression rule. Every requested grid rule removed zero boxes, so the simulation did not beat v034a and did not test a live suppression effect. The known case-155 nested same-wreck FP has containment `1.0`, area ratio approximately `0.083`, and IoU approximately `0.083`; because the requested grid's minimum IoU threshold was `0.10`, the grid could not suppress that specific known duplicate.
