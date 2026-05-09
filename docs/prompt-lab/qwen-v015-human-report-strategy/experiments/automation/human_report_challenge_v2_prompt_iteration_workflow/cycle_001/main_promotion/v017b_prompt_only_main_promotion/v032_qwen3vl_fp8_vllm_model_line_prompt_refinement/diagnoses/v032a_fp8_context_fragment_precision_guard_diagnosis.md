# v032a Diagnosis

Generated: `2026-05-09T00:09:09Z`

What this tested: intended to add a compact negative-only context/fragment precision guard to the good/bad box area.

What changed from FP8 working best: nothing after rendering. The rendered prompt hash matched the baseline exactly: `0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b`.

Metrics: sentinel `42 / 7 / 15 / 22`, case 67 `10/1/2`, case 155 `n/a`, case 166 `n/a`, office-negative pass.

Decision: rejected as an unintended no-op / authoring failure. It is useful only because it confirmed the baseline sentinel replay can reproduce exactly when the rendered prompt is identical.

Next hypothesis: use an explicitly verified rendered diff before treating a prompt candidate as semantic evidence.
