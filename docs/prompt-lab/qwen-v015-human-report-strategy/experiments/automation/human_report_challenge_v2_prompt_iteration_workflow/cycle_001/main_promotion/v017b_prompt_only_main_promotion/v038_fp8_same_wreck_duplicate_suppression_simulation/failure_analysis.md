# v038 Failure Analysis

Safe rules: `512`. Unsafe rules: `0`.

Rules were marked unsafe if they increased FNs, reduced matches, worsened key dense/control cases, or failed office-negative.

All 512 safe rules were no-op rules: no simulated rule removed any box. This means the grid did not establish that duplicate suppression is unsafe in principle; it established that the requested IoU-bounded sweep is too narrow to catch the v036-isolated case-155 duplicate. The relevant case-155 pair is `target_1` nested inside `target_0` with containment `1.0`, center-inside `true`, same target type, smaller unmatched, larger matched, area ratio about `0.083`, and IoU about `0.083`. The minimum swept IoU threshold was `0.10`, so the known local duplicate falls just outside the grid.

Recommended implication: do not author prompt wording from this no-op grid. The next evidence step should be a second offline simulation or visual review that explicitly tests containment-first rules with IoU below `0.10` or no IoU floor, while preserving the same no-TP-removal and dense-case safety gates.
