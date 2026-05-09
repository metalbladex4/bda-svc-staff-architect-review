# v042e_fp8_separate_small_target_row_exception Diagnosis

What did this candidate test? a narrow GOOD FINAL BOX exception for a separate small target near other targets when its own body can be boxed tightly.

What changed from current working best? One compact GOOD FINAL BOX clause was added outside EXTRA-BOX AUDIT and FINAL BALANCE; v020c audit and v034a guard were preserved.

Raw metrics: `42/17/22/39`.

Postprocessed metrics: `42/17/21/38`.

Case 66: `8/0/6 -> 8/0/6`.
Case 67: `8/3/4 -> 8/3/4`.
Case 84: `8/5/0 -> 8/5/0`.
Case 100: `1/2/1 -> 1/2/1`.
Case 110: `3/4/3 -> 3/4/3`.
Case 155: `2/0/2 -> 2/0/2`.
Case 166: `1/0/0 -> 1/0/0`.

p1753 removed `1` predictions and `0` true positives.

Main lesson: v042e failed the postprocessed micro gate: case66_fp_regression_gate_failed.

Next axis: Pivot using exact residual deltas; avoid wording families that have already harmed dense/control gates.
