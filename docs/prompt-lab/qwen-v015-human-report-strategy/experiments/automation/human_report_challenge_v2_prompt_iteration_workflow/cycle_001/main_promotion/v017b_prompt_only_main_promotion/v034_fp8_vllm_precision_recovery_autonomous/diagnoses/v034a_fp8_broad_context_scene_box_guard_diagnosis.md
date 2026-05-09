# v034a Diagnosis

What did this candidate test? A compact precision-only bad-box guard against broad context/scene boxes while preserving v020c extra-box audit discipline.

What changed from FP8 working best? One BAD FINAL BOX line was added; the v020c audit and final balance were preserved.

Micro-pack result: `{'matches': 44, 'false_negatives': 12, 'false_positives': 14, 'combined_errors': 26, 'image_count': 16}`.

Full result: `{'matches': 181, 'false_negatives': 38, 'false_positives': 25, 'combined_errors': 63, 'image_count': 117}`.

Did it beat FP8 baseline? Yes. It improved from `180 / 39 / 32 / 71` to `181 / 38 / 25 / 63`, an 8-error improvement.

Did it approach or beat old 58-error reference? It approached but did not beat it. The remaining gap is 5 combined errors.

Which cases explain the result? The main win is FP reduction without broad recall collapse. Case 110 stayed controlled at `3/4/1`, avoiding the v032d `3/4/32` explosion. Case 155 improved versus FP8 baseline but did not fully match v032d, ending at `2/0/1`. Case 67 stayed strong at `10/1/3` but added one FP versus baseline sentinel/full expectations. Case 84 recall weakened to `8/5/0`, so dense recall remains the main caution.

What happened on case 110? The candidate directly addressed the v033 lesson. It completed cleanly under the 180-second timeout policy with no retry and reduced the v032d-style FP risk to `1` FP.

What happened on case 155? It improved from the FP8 baseline pattern of `2/0/2` to `2/0/1`, but did not preserve the complete v032d `2/0/0` fix.

Dense cases 66/67/84/97: case 66 remained `8/0/5`; case 67 was `10/1/3`; case 84 was `8/5/0`; case 97 was `1/0/1`. This is acceptable for the near-term target but not yet a final continuation surface.

Did it reproduce a known failure? It did not reproduce the v025a case-67 collapse and did not reproduce the v032d case-110 FP explosion. It did preserve some FP pressure on case 66 and weakened case 84 recall.

Did it create a new FP8-specific failure class? No clear new class. The residual issue is the existing FP8 dense/fragment balance, especially case 66 FPs and case 84 FNs.

Likely load-bearing phrase: `broad context or scene boxes whose strongest support is a row, blast area, road, debris field, smoke plume, or multiple uncertain fragments rather than one visible target body`.

Lesson type: model-surface-specific signal. On FP8 vLLM, a compact broad-context rejection line can reduce false positives while preserving the v020c audit better than v019c anchor replay.

What should be preserved? Keep v020c extra-box audit discipline and the compact broad-context scene-box guard.

What should be avoided? Do not remove the v020c audit, do not use v032d/v019c wholesale as the base, and do not add broad recall language.

Next hypothesis: stop this tranche at the near-term target. If a follow-up tranche is approved, start from v034a and target the remaining 5-error gap to old v020c by reducing residual dense/fragment FPs without hurting case 84 recall.
