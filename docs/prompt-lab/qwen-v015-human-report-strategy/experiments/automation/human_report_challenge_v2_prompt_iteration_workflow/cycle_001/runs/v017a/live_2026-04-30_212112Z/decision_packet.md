# v2 Prompt-Iteration Live Decision Packet

- candidate: `v017a`
- classification: `near_miss`
- passed gates: `false`

## Recommended User Decision

review v017a failure/near-miss evidence before authoring v017b

## Gate Summary

### v2 hinge 12

- passed: `false`
- totals: `23` matches, `34` FNs, `17` FPs
- checks: `case_101_diagnostic=false`, `false_negative_count=true`, `false_positive_count=true`, `match_count=true`, `positive_control_155=true`
- positive control: `155` match_count=`2`, passed=`true`
- case `101`: detections=`1`, row_fragment_groups=`0`, broad_group_boxes=`1`, passed=`false`
- case `101` broad box: `[75, 13, 1000, 571]` area_ratio=`0.49223899841308594`

### changed-source sanity

- passed: `true`
- totals: `9` matches, `3` FNs, `0` FPs
- checks: `false_negative_count=true`, `false_positive_count=true`, `match_count=true`, `positive_control_155=true`
- positive control: `155` match_count=`2`, passed=`true`

### office-negative abstention

- passed: `true`
- totals: `1` matches, `0` FNs, `0` FPs
- checks: `negative_scene_abstention_correct_count=true`, `negative_scene_count=true`, `negative_scene_false_positive_count=true`
