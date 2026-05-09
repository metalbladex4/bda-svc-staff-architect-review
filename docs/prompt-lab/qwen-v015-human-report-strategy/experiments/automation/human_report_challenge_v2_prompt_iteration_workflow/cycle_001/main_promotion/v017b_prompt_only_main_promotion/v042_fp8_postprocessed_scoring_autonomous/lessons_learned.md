# v042 Lessons Learned

- p1753 is deployable prediction-only geometry and must reproduce v041 before any prompt candidate is trusted.
- Composite scoring can hide raw prompt regressions, so every candidate keeps raw and postprocessed metrics side by side.
- The next prompt gain should target residual FNs or FPs that p1753 does not touch; duplicate wording from v037 remains avoided.
- Case 67 and case 84 remain the main dense/recall safety gates.
