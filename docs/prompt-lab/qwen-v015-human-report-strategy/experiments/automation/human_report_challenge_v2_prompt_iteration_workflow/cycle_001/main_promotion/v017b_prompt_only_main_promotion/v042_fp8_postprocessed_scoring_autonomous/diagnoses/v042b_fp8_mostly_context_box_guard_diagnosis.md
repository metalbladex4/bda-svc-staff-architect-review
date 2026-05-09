# v042b_fp8_mostly_context_box_guard Diagnosis

What did this candidate test? A precision-only BAD FINAL BOX clause for mostly-context/background boxes, from the v034a base with p1753 paired scoring.

What changed from current working best? One compact BAD FINAL BOX clause was added. The v020c extra-box audit and v034a broad-context guard were preserved.

Raw metrics: `43/16/19/35`.

Postprocessed metrics: `43/16/18/34`.

Case 66: `7/1/6 -> 7/1/6`.
Case 67: `10/1/3 -> 10/1/3`.
Case 84: `8/5/0 -> 8/5/0`.
Case 100: `1/2/1 -> 1/2/1`.
Case 110: `3/4/1 -> 3/4/1`.
Case 155: `2/0/2 -> 2/0/2`.
Case 166: `1/0/0 -> 1/0/0`.

p1753 removed `1` predictions and `0` true positives.

Main lesson: v042b failed the postprocessed micro gate: case66_fp_regression_gate_failed.

Next axis: Pivot away from mostly-context wording if it harms dense/control gates; otherwise use exact residual deltas for the next one-clause candidate.
