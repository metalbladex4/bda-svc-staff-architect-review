# v043 FP8 Residual Error Verifier/Postprocess Loop

Experiment-only residual-error inventory and offline prediction-only postprocessing simulation for the FP8 vLLM model line.

This tranche does not promote FP8, does not mutate product runtime, and does not replace the old/product v020c incumbent.

## Starting Point

- Old/product v020c reference: `186 / 33 / 25 / 58`.
- Raw FP8 prompt best, v034a: `181 / 38 / 25 / 63`.
- Composite FP8 experiment best, v034a + p1753: `181 / 38 / 24 / 62`.
- v040 hybrid oracle: `181 / 38 / 22 / 60`, documented as non-deployable.

## Outcome

The best offline prediction-only intervention is `pp0157`, a tiny dense military-equipment prediction filter applied after p1753. It reaches `181 / 38 / 20 / 58`, removes four false positives, removes zero true positives, and leaves matches/FNs unchanged.

This is experiment-only evidence. The next safe step is visual/crop verifier review of the removed case-66 predictions and the remaining residual FP/FN classes before any product integration or new prompt wording.
