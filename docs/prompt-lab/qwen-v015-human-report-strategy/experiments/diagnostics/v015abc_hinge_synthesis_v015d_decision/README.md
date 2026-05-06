# v015a/v015b/v015c Hinge Synthesis And v015d Decision

Status: `diagnostic_complete_no_prompt_text`

This package compares the existing v015a, v015b, and v015c hinge-smoke
artifacts before any future v015d prompt work.

## Conclusion

The v015 line has a real recall-recovery signal, but the current prompt-only
approach has not controlled the case `101` structural failure. v015c improved
the side precision guards (`12`, `28`) and preserved protected abstention
(`155`), yet it still produced row-fragment enumeration and a broad group box
on `101`.

The next decision should be whether to approve:

- one final prompt-only fail-closed `v015d` hinge attempt, or
- a structural output-shape guard/validator plan before spending more prompt
  attempts or dev budget.

## Files

- `source_manifest.json`: read-only evidence inputs and excluded actions.
- `hinge_comparison.md` / `hinge_comparison.json`: aggregate and per-case
  v015a/v015b/v015c metrics.
- `failure_pattern_synthesis.md` / `failure_pattern_synthesis.json`: shared
  failure pattern and prompt-only risk assessment.
- `v015d_decision_brief.md`: constraints and decision framing only; no final
  prompt text.

## Boundary

No prompt text, overlay, runtime config, VLM inference, dev split, holdout,
all-112 run, source-truth mutation, Graphify refresh, evidence rebuild, Mem0
update, or promotion artifact is created by this package.
