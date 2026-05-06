# v015 Offline Structural Guard Simulator

Status: `offline_simulator_complete_no_runtime_change`

This package applies the draft structural output-shape guard to existing
v015a/v015b/v015c/v015d hinge predictions only. It writes separate guarded
prediction copies and raw-vs-guarded metrics.

## Boundary

- No VLM inference was run.
- Raw predictions were not modified.
- Source references and human-report data were not modified.
- Runtime code/config was not adopted.
- Dev, holdout, and all-112 were not run.
- Graphify, evidence indexes, Mem0, and MCPfinder were not updated or called.

## Files

- `guarded_predicted/<candidate>/`: guarded report copies.
- `eval/<candidate>/guarded_evaluation_summary.json`: guarded metrics.
- `guard_diagnostics.json`: per-case guard signals and suppressions.
- `raw_vs_guarded_metrics.json` / `raw_vs_guarded_metrics.md`: comparison.
- `case_101_guard_review.md`: manual-review summary for the hinge case.

## Result

The simulator detects the targeted structural shapes. It is not runtime-ready:
the first suppression policy is intentionally blunt and exposes recall loss.
