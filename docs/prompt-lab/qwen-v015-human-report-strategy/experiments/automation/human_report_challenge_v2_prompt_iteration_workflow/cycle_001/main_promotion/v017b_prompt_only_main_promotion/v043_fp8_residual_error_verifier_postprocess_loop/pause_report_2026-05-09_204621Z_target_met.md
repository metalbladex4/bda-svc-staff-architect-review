# v043 Pause Report: Target Met

Generated: `2026-05-09T20:46:21Z`

Stop reason: v043 reached the near-term reference target in offline experiment-only postprocessing.

Best composite result: `pp0157` at `181 / 38 / 20 / 58`.

Target status:

- Beat composite 62: yes.
- Reached old/product 58 reference: yes, parity.
- Reached <=1: no.

What happened:

- The residual inventory found 62 remaining combined errors after v034a + p1753.
- The best prediction-only simulation, `pp0157`, removed four false positives and zero true positives.
- All four removed boxes were very small `military_equipment` predictions in case 66.
- Matches and FNs stayed unchanged.
- Dense/control cases did not regress.

Next action:

Run visual/crop verifier review of the four case-66 removals and remaining dense/control residual classes before any experiment-only integration or new prompt candidate.

Boundaries preserved:

- No product runtime mutation.
- No source-truth mutation.
- No doctrine, assessment prompt, or eval-ground-truth mutation.
- No promotion.
- No live VLM calls in v043.
