# v039 Lessons Learned

- Containment-first simulation directly tests the duplicate class v038 missed.
- Any post-hoc duplicate rule must keep matches and FNs unchanged while preserving dense cases 66/67/84/110.
- Best decision: `B`.
- The known case-155 duplicate is removable by geometry once IoU is allowed below `0.10`.
- The metric-best rule is label-agnostic; a stricter same-label variant is slightly weaker but likely cleaner as the first experiment-only implementation.
