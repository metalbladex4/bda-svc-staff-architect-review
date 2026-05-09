# v043 Strategy State

Current best composite: `pp0157` at `181 / 38 / 20 / 58`.

Raw prompt best remains v034a at `181 / 38 / 25 / 63`.

Composite path:

1. v034a raw prompt output.
2. p1753 prediction-only same-label duplicate suppression.
3. pp0157 prediction-only tiny dense military-equipment filter.

Next axis: visual/crop verifier review before further prompt changes or postprocessor integration. The next validation should inspect the four removed case-66 predictions and then test `pp0157` on future FP8 candidate outputs as an experiment-only wrapper.
