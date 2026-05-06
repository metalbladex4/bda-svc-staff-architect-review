# False-Positive Taxonomy

These labels explain the v015a hinge failure without treating
raw FP count as the only source of truth.

| Label | Cases |
| --- | --- |
| whole_scene_or_group_box | 101 |
| pattern_fragment_row_enumeration | 101 |
| adjacent_context_false_positive | 12, 28 |
| bbox_or_reference_shape_artifact | 101 |
| duplicate_reference_target | 101 |
| valid_recall_recovery | 101, 12, 28 |
| protected_abstention_preserved | 155 |

## Definitions

- `whole_scene_or_group_box`: A broad candidate box covers a large target group or scene region instead of a single distinct object.
- `pattern_fragment_row_enumeration`: The model enumerates repeated row-like fragments as independent targets.
- `adjacent_context_false_positive`: Adjacent context, smoke, building parts, or tiny distant shapes become extra targets.
- `bbox_or_reference_shape_artifact`: Metric interpretation is affected by reference geometry or grouped boxes.
- `duplicate_reference_target`: The source reference contains duplicated target geometry.
- `valid_recall_recovery`: The candidate recovered at least one true-positive target signal.
- `protected_abstention_preserved`: Protected object-not-found abstention remained safe.
