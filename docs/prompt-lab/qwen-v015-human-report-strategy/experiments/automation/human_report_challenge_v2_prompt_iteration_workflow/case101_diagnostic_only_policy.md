# Case 101 Diagnostic-Only Policy

Status: `active_for_forward_v017_cycle`

Case `101` is removed from forward pass/fail evaluation use for the
`human_report_challenge_v2` prompt-iteration automation lane.

## Why

Across v015 through v017, case `101` repeatedly acted as a gate-distorting
outlier. It exposed useful behavior, especially row-fragment enumeration and
broad group/scene-box collapse, but it also has reference/eval-shape caveats
that make it a poor pass/fail gate for iterative prompt selection.

The latest examples:

- `v017a`: suppressed row-fragment enumeration but emitted broad box
  `[75, 13, 1000, 571]`
- `v017b`: preserved row-fragment suppression and stronger aggregate metrics
  but emitted broad box `[75, 58, 1000, 547]`

## Forward Rule

Starting with `v017c`, active pass/fail gates use:

`validation_manifests/human_report_challenge_v2_hinge_11_no101.yaml`

The old 12-case hinge manifest remains available for historical/manual
diagnostic context only. It should not block candidate classification or
automation continuation.

## What This Does Not Change

- It does not mutate source report `101.txt`, source image `101.jpg`, or
  historical reference JSON.
- It does not rewrite v017a/v017b historical run outputs.
- It does not authorize dev, holdout, all-112, promotion, runtime adoption,
  structural guards, source-truth mutation, MCP config changes, hook edits, or
  tool installs.
- It does not mean the broad-box failure is irrelevant. It remains a diagnostic
  lesson for prompt design.

## Forward Continuation

Near-miss diagnosis remains mandatory, but it is not a human approval gate
inside the approved `v017a` through `v017f` cycle. Continue through `v017f`
unless a hard stop triggers:

- abstention guard failure
- source or manifest integrity failure
- scope violation
- runtime or tool-boundary violation
- candidate budget exhausted
- explicit user stop
