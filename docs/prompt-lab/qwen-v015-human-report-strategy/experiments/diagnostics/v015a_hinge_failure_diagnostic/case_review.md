# Case Review

| Case | Role | Refs | Preds | TP | FN | FP | Diagnostic labels |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 101 | main hinge tradeoff case | 12 | 15 | 3 | 9 | 12 | valid_recall_recovery, whole_scene_or_group_box, pattern_fragment_row_enumeration, bbox_or_reference_shape_artifact, duplicate_reference_target |
| 12 | building precision guard | 1 | 2 | 1 | 0 | 1 | valid_recall_recovery, adjacent_context_false_positive |
| 28 | military-equipment precision guard | 1 | 3 | 1 | 0 | 2 | valid_recall_recovery, adjacent_context_false_positive |
| 155 | protected out-of-scope control | 1 | 1 | 1 | 0 | 0 | protected_abstention_preserved |

## Findings

- `101`: v015a created partial recall recovery but also produced a regular row of small military-equipment boxes plus one broad scene/group box. The output failure is mixed with reference shape caveats.
- `12`: v015a preserved the main building match but split adjacent fire/smoke/building context into an extra building target.
- `28`: v015a preserved the main equipment match but added two tiny top-right context boxes as military equipment.
- `155`: v015a preserved the object-not-found abstention behavior with no false positive rebound.

## Existing Visual Review Links

- `101`: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015a_recall_recovery/executions/human_report_challenge_v1_hinge_smoke_2026-04-29_171438Z/eval/images_bbox_review/bbox_review_101.jpg`
- `12`: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015a_recall_recovery/executions/human_report_challenge_v1_hinge_smoke_2026-04-29_171438Z/eval/images_bbox_review/bbox_review_12.jpg`
- `28`: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015a_recall_recovery/executions/human_report_challenge_v1_hinge_smoke_2026-04-29_171438Z/eval/images_bbox_review/bbox_review_28.jpg`
- `155`: `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015a_recall_recovery/executions/human_report_challenge_v1_hinge_smoke_2026-04-29_171438Z/eval/images_bbox_review/bbox_review_155.jpg`
