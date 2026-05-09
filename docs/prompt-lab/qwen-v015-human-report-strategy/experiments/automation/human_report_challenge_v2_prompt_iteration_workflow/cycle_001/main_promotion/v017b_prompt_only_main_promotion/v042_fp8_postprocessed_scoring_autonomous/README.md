# v042 FP8 Postprocessed-Scoring Autonomous

Experiment-only FP8 vLLM prompt-refinement tranche using deployable prediction-only postprocessor `p1753` as a scoring layer.

- Raw prompt working best: `v034a = 181 / 38 / 25 / 63`.
- Composite working best: `v034a + p1753 = 181 / 38 / 24 / 62`.
- Old/product reference remains non-FP8 `v020c = 186 / 33 / 25 / 58`.

No product runtime, doctrine, assessment prompt, eval truth, or source-truth files are modified by this tranche.
