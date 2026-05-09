# v042d_fp8_final_balance_simplification Diagnosis

What did this candidate test? a semantic-neutral simplification of FINAL BALANCE that removes historical version wording while preserving target-validity semantics.

What changed from current working best? Only the FINAL BALANCE sentence was simplified; the v020c extra-box audit and v034a broad-context guard were preserved.

Raw metrics: `44/15/16/31`.

Postprocessed metrics: `44/15/15/30`.

Case 66: `8/0/5 -> 8/0/5`.
Case 67: `10/1/1 -> 10/1/1`.
Case 84: `7/6/1 -> 7/6/1`.
Case 100: `2/1/1 -> 2/1/1`.
Case 110: `3/4/1 -> 3/4/1`.
Case 155: `2/0/1 -> 2/0/1`.
Case 166: `1/0/0 -> 1/0/0`.

p1753 removed `1` predictions and `0` true positives.

Main lesson: v042d failed the postprocessed micro gate: case84_recall_regression_gate_failed.

Next axis: Pivot using exact residual deltas; avoid wording families that have already harmed dense/control gates.
