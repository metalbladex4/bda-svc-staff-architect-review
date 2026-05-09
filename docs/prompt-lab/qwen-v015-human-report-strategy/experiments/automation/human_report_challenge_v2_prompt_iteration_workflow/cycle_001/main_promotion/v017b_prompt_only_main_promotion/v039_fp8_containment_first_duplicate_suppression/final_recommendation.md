# v039 Final Recommendation

Generated: `2026-05-09T17:33:06Z`

Decision `B`: Containment-first simulation beats v034a but remains above 58.

Known case-155 duplicate tested: `True`.
Known case-155 duplicate removed: `True`.

Best rule: `r020`.

Best metrics: `181/38/22/60`.

Beat v034a: `True`.
Reached or beat old 58-error reference: `False`.
Recommended next work: `v040_experiment_only_post_processing_tranche`.

Best-rule interpretation:

- `r020` removed three unmatched predictions and improved v034a by 3 combined errors without increasing FNs or reducing matches.
- The known case-155 duplicate was tested and removed.
- Dense/control cases stayed unchanged: case 66 `8/0/5`, case 67 `10/1/3`, case 84 `8/5/0`, case 110 `3/4/1`, case 155 `2/0/0`, case 166 `1/0/0`.
- Because `r020` is label-agnostic and one of its removals is cross-label, v040 should compare `r020` against the stricter same-label variant `r019`, which scores `181/38/23/61` and removes the case-155 duplicate with a narrower semantic footprint.

This is non-promoted post-hoc evidence only. It does not modify product runtime, prompt text, doctrine, assessment prompt, eval truth, or source truth.
