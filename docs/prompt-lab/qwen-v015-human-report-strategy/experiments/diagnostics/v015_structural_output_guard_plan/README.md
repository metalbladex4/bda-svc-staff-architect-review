# v015 Structural Output-Shape Guard Plan

Status: `design_only_no_runtime_change`

This package records the approved next direction after the final prompt-only
`v015d` attempt failed the hinge gate. It does not implement a guard. It
defines a future candidate-local offline simulator path for detecting the two
stable structural failures:

- regular row-fragment enumeration
- broad group/scene boxes masquerading as individual target detections

## Decision

Prompt-only tuning is now exhausted for this hinge cycle. `v015d` proved that
wording can suppress row fragments and false positives, but only by collapsing
recall back to v014 level, and it still left the case `101` broad-box failure.

The next implementation wave should be an offline structural guard simulator
against existing hinge predictions, not a runtime hook and not another prompt
candidate.

## Files

- `source_manifest.json`: evidence inputs and excluded actions.
- `guard_signal_spec.md` / `guard_signal_spec.json`: draft geometry signals.
- `integration_design.md`: candidate-local simulator and future runtime options.
- `validation_plan.md` / `validation_plan.json`: future wave checks and gates.
- `decision_record.md`: final prompt-only stop decision and next approval gate.

## Boundary

No runtime code, runtime config, source truth, reference JSON, VLM inference,
dev split, holdout, all-112 run, promotion, Graphify refresh, evidence rebuild,
or Mem0 update is performed by this package.
