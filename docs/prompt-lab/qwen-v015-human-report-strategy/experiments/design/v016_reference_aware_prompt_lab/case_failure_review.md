# Case Failure Review

Status: `complete_for_design_only`

This review classifies the v015e dev outlier set before any v016 prompt text
is authored. The selected cases are every dev case with
`false_positive_count > 0` or `false_negative_count >= 2`, plus the protected
and manual controls.

## Aggregate Read

v015e preserved precision but failed dev recall:

- v015e dev: `61` matches, `56` false negatives, `17` false positives.
- v014 dev baseline: `70` matches, `47` false negatives, `17` false positives.
- Interpretation: v015e did not reopen the broad false-positive problem at the
  aggregate level, but it also did not generalize recall recovery.

## Reviewed Cases

| Case | Split | v015e result | Labels | v016 implication |
| --- | --- | --- | --- | --- |
| `66` | dev | 1 match, 7 FNs, 0 FPs | `true_prompt_recall_failure`, `prompt_axis_candidate` | Dense military-equipment scenes need candidate discovery beyond one confident target. |
| `67` | dev | 1 match, 10 FNs, 10 FPs | `true_prompt_recall_failure`, `true_prompt_precision_failure`, `prompt_axis_candidate` | Count recovery alone becomes misplaced enumeration without an evidence filter. |
| `69` | dev | 1 match, 0 FNs, 1 FP | `true_prompt_precision_failure`, `prompt_axis_candidate` | One-target scenes still need final unsupported-extra rejection. |
| `84` | dev | 1 match, 12 FNs, 0 FPs | `true_prompt_recall_failure`, `prompt_axis_candidate` | The largest dense-recall collapse; v016 must recover multiple clearly supported targets. |
| `86` | dev | 0 matches, 1 FN, 1 FP | `true_prompt_recall_failure`, `true_prompt_precision_failure`, `prompt_axis_candidate` | The prompt must justify object boundary and not only category choice. |
| `97` | dev | 1 match, 0 FNs, 4 FPs | `true_prompt_precision_failure`, `prompt_axis_candidate` | Building cases need adjacent-context and duplicate rejection. |
| `100` | dev | 1 match, 2 FNs, 0 FPs | `true_prompt_recall_failure`, `prompt_axis_candidate` | Secondary visible buildings cannot be hidden by scene-central logic. |
| `101` | dev | 1 match, 11 FNs, 0 FPs | `true_prompt_recall_failure`, `reference_shape_caveat`, `evaluation_shape_caveat`, `manual_diagnostic_case`, `prompt_axis_candidate`, `not_prompt_authoring_ready` | Use as manual diagnostic, not a simple metric target. |
| `103` | dev | 1 match, 0 FNs, 1 FP | `true_prompt_precision_failure`, `prompt_axis_candidate` | Requires final unsupported-extra and adjacent-context rejection. |
| `147` | dev | 1 match, 2 FNs, 0 FPs | `true_prompt_recall_failure`, `prompt_axis_candidate` | Mixed category recall needs category-aware discovery without broadening. |
| `155` | dev | protected control passed | `protected_negative_control` | Preserve object-not-found abstention. |
| `166` | holdout reference-only | not run in v015e dev | `protected_negative_control`, `not_prompt_authoring_ready` | Keep as future holdout no-regression control, not tuning evidence. |

## Failure Groups

Dense recall collapses: `66`, `84`, and `101` show that v015e can preserve
precision by under-detecting dense scenes. `100` and `147` show the same shape
at smaller scale.

Mixed recall and precision collapse: `67` is the warning case. It emitted the
same number of predictions as references, but only one matched. That means
v016 cannot simply ask for more detections or more enumeration.

Precision rebound: `69`, `86`, `97`, and `103` show that even a precision-held
aggregate can hide local unsupported extras or wrong-boundary choices.

Protected controls: `155` passed and must remain protected. `166` is a
holdout-only protected control and must not be used as prompt-authoring
evidence before a future approved holdout wave.

## v016 Design Consequence

The next prompt lane should be
`reference_aware_candidate_discovery_with_evidence_budget`. It should change
the prompt interface around candidate discovery plus final evidence filtering.
It should not merely tighten individual-body wording or ask the model to list
more boxes.
