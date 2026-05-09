# p1753 Postprocessing Rule Spec

Experiment-only deployable prediction-only duplicate suppression rule.

- containment >= 0.8
- IoU >= 0.0
- area ratio <= 0.03
- center-inside required
- same-label required
- cross-label disabled
- keep-largest-only enabled
- never suppress if the smaller prediction contains another prediction
- no reference/eval/oracle fields used at inference time
