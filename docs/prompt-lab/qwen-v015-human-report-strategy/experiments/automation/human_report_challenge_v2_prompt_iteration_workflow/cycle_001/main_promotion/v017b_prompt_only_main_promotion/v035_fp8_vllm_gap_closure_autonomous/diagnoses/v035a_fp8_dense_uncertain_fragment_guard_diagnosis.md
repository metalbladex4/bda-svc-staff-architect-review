# v035a Diagnosis

What did this candidate test? A compact precision-only guard against isolated dense-scene marks or partial fragments when target body center and exterior boundary are not both visible.

What changed from v034a? One BAD FINAL BOX line was added after the v034a broad-context/scene-box guard. The v034a guard, v020c audit, and final balance were preserved.

Micro-pack result: `{'matches': 41, 'false_negatives': 15, 'false_positives': 19, 'combined_errors': 34, 'image_count': 16}`.

Full result: `not run`.

What improved? Case 155 improved from v034a `2/0/1` to `2/0/0`. Case 110 did not explode; it moved from `3/4/1` to `4/3/2`, trading one FN for one FP.

What regressed? Case 67 collapsed from v034a `10/1/3` to `7/4/5`, and case 66 worsened from `8/0/5` to `8/0/6`. Overall sentinel worsened from `44 / 12 / 14 / 26` to `41 / 15 / 19 / 34`.

Did it beat v034a? No. It failed micro-pack and full all-current was not run.

Did it approach or beat old 58-error reference? No full-pack score exists, and micro-pack direction was negative.

Which cases explain the result? The rejection is explained primarily by case 67 dense-row collapse and increased dense FP pressure on case 66. The useful local signal is case 155 FP removal.

What happened on case 66? It retained all matches but added one FP: `8/0/6`.

What happened on case 67? It failed the hard dense gate: `7/4/5`.

What happened on case 84? It stayed at v034a's already-weak `8/5/0`.

What happened on case 110? It remained controlled relative to v032d, but shifted to `4/3/2`.

What happened on case 155? It improved to `2/0/0`, suggesting the fragment wording can suppress one residual local FP.

What happened on case 166 and office-negative? Case 166 passed at `1/0/0`; office-negative passed.

Did it reproduce a known failure? Yes. It reproduced the old dense-case warning: wording that rejects uncertain fragments can push the model away from valid crowded targets, especially case 67.

Did it create a new FP8-specific failure class? No new class; it amplified the known FP8 dense-fragment precision/recall instability.

Likely load-bearing phrase: `isolated dense-scene marks or partial fragments when the target body center and exterior boundary are not both visible`.

Lesson type: model-surface-specific prompt sensitivity. The phrase was too strict for dense/crowded targets even though it helped case 155.

What should be preserved? Preserve v034a as working best and preserve the idea that case 155 may benefit from more local FP language.

What should be avoided? Avoid broad or dense-scene fragment rejection language that mentions partial fragments without a stronger dense-target exception.

Next hypothesis: Visual/eval artifact synthesis for residual dense fragments before another prompt candidate. Any next candidate should isolate the case-155 benefit without applying the rule to dense rows like case 67.
