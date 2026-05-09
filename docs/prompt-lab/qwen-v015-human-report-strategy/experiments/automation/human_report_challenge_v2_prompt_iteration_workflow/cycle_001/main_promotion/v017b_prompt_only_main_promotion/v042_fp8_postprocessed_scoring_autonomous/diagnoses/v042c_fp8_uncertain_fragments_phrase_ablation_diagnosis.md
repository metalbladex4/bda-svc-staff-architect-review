# v042c_fp8_uncertain_fragments_phrase_ablation Diagnosis

What did this candidate test? a micro-gated ablation of only the 'multiple uncertain fragments' phrase inside the v034a broad-context guard, from the v034a base with p1753 paired scoring.

What changed from current working best? Only the risky phrase was removed; the rest of the v034a guard and v020c extra-box audit were preserved.

Raw metrics: `40/19/23/42`.

Postprocessed metrics: `40/19/22/41`.

Case 66: `8/0/10 -> 8/0/10`.
Case 67: `8/3/3 -> 8/3/3`.
Case 84: `7/6/0 -> 7/6/0`.
Case 100: `1/2/1 -> 1/2/1`.
Case 110: `3/4/1 -> 3/4/1`.
Case 155: `2/0/2 -> 2/0/2`.
Case 166: `1/0/0 -> 1/0/0`.

p1753 removed `1` predictions and `0` true positives.

Main lesson: v042c failed the postprocessed micro gate: case66_fp_regression_gate_failed.

Next axis: Pivot using exact residual deltas; avoid wording families that have already harmed dense/control gates.
