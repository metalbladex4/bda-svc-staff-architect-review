# Guard Signal Spec

Status: `candidate_guard_spec_only`

These signals are draft geometry diagnostics for a future offline simulator.
They are not runtime behavior and are not approval to suppress detections in
production.

| Signal | Purpose | Draft rule | Offline simulator action |
| --- | --- | --- | --- |
| `broad_group_or_scene_box` | flag boxes too large to represent one distinct target body | area_ratio >= 0.25 OR width_ratio >= 0.70 and height_ratio >= 0.30 | flag_and_optionally_suppress |
| `regular_row_fragment_enumeration` | flag many small boxes aligned in a regular row pattern | at least 5 small boxes in a narrow y-band with regular x gaps | flag_group_and_optionally_suppress_member_boxes |
| `tiny_ambiguous_context_box` | flag tiny boxes likely to be distant context, debris, smoke edge, or texture | small area plus no nearby standalone-body evidence; diagnostic-only in first simulator | flag_only |

## Guard Principles

- Preserve raw model outputs and write guarded copies separately.
- Emit diagnostics before suppressing or flagging detections.
- Treat broad-box suppression as risky because a large reference target can
  score as a match while still being visually poor.
- Treat row-fragment suppression as promising because the repeated pattern has
  been stable across v015b and v015c.
- Do not use geometry-only signals to claim source truth.
