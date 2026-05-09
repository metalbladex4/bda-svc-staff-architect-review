# v042 Lessons Learned

- p1753 reproduced v041 exactly on frozen v034a and remains a safe deployable scoring layer for this tranche.
- v042a's low-contrast/smoke-softened recall cue moved the model in the wrong direction: case 84 lost recall and case 66 gained an FP.
- v042b's mostly-context precision clause is tested as a narrower alternative that avoids the v037 same-wreck and v035 dense-fragment failure families.
- v042c tests whether the 'multiple uncertain fragments' phrase itself is load-bearing for dense recall or FP pressure.
- v042d tests whether historical version-label wording adds unwanted FP8 surface noise without changing target-validity semantics.
- v042e tests a narrow separable-small-target exception outside the audit/final-balance sections.
- Full-run target claims are reserved for full all-current/no101 results; micro-pack deltas are gate evidence only.
- v042a-e did not pass micro-pack; near-neighbor prompt wording around v034a is now showing more regression risk than closure signal.
