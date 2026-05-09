# v037a Diagnosis

What did this candidate test? A compact same-wreck duplicate/local-context guard for the case-155-style nested box identified in v036.

What changed from v034a? One BAD FINAL BOX line was added after the v034a broad-context/scene-box guard. The v034a guard, v020c audit, and final balance were preserved.

Micro-pack result: `{'matches': 41, 'false_negatives': 15, 'false_positives': 30, 'combined_errors': 45, 'image_count': 16}`.

Full result: `not run`.

Known failure focus: case 155 same-wreck duplicate FP, case 66/67 dense-row safety, case 84 recall, case 110 broad FP explosion, and controls 166/office-negative.

Next hypothesis: Use the v037a failure deltas to decide whether to refine same-wreck overlap wording or pivot away from prompt-only duplicate suppression.
