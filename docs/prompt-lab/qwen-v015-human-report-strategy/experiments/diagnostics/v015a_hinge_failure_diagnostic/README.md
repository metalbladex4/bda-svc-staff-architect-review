# v015a Hinge-Failure Diagnostic

Status: `diagnostic_complete_no_prompt_text`

This package explains why `v015a_recall_recovery` failed the
hinge smoke gate before any `v015b` prompt work. It reviews
only cases `101`, `12`, `28`, and `155` from the existing
v015a hinge run.

## Conclusion

`v015a` recovered some true-positive signal, but failed because
false positives rebounded. Case `101` is a mixed failure:
the model emitted row-like fragment targets and a broad
group/scene box, while the reference truth also contains a
duplicated target box and one large grouped target. Cases `12`
and `28` are cleaner precision-guard regressions. Case `155`
remained protected.

## Files

- `source_manifest.json` records read-only source/run evidence.
- `case_review.md` / `case_review.json` summarize selected cases.
- `false_positive_taxonomy.md` / `false_positive_taxonomy.json`
  define the diagnostic labels and FP instances.
- `reference_truth_audit.md` / `reference_truth_audit.json`
  record the narrow source-truth caveat audit.
- `v015b_design_constraints.md` lists constraints only; it does
  not author prompt text.

## Boundary

No prompt text, overlay, runtime config, VLM inference, dev split,
holdout, all-112 run, source-truth mutation, Graphify refresh,
evidence rebuild, or promotion artifact is created by this package.
