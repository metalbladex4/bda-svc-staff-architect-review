# v032c Diagnosis

Generated: `2026-05-09T00:09:09Z`

What this tested: a short FP8 calibration sentence emphasizing visible target body center plus boundary while removing the longer v020c calibration phrase.

What changed from FP8 working best: replaced the historical calibration sentence with a compact FP8-specific one. Rendered prompt hash changed to `3266b2143aa47026c45f62d5498e966f8b9d8d90cd38346afe9a01471c97e41b`.

Metrics: sentinel `40 / 9 / 17 / 26` versus baseline sentinel `42 / 7 / 15 / 22`. Case 67 stayed `10/1/2`, but case 84 worsened from baseline `n/a` to `n/a`. Case 155 remained `n/a` and case 166 stayed `n/a`. Office-negative passed.

Decision: rejected. It worsened sentinel errors from 22 to 26 without fixing the FP8 case-155 regression.

Likely load-bearing phrase: replacing the original calibration sentence weakened recall behavior around partly visible dense targets.

Lesson type: model-surface-specific and prompt-structure signal. FP8 still depends on some of the v020c wording, even though its full baseline is worse than the old model surface.

Next hypothesis: compare earlier stable prompt anchors rather than adding new calibration text.
