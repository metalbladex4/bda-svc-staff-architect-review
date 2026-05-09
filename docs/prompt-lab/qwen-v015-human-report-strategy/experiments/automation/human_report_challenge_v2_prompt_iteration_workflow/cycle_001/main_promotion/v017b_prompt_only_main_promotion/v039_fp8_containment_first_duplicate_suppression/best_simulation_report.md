# v039 Best Simulation Report

Best safe rule: `r020`

Metrics: `181/38/22/60`.

Rule: containment >= `0.8`, IoU >= `0.0`, area ratio <= `0.1`, same-label `False`.

Removed boxes: `3`.

Removed predictions: `[{'image_filename': '88.jpg', 'case_id': '88', 'removed_label': 'target_1', 'kept_larger_label': 'target_0', 'removed_target_type': 'military_equipment', 'kept_larger_target_type': 'military_equipment', 'removed_bbox': [1308.0, 699.0, 1438.0, 816.0], 'kept_larger_bbox': [0.0, 466.0, 2468.0, 1674.0], 'iou': 0.005101725933002029, 'containment_ratio': 1.0, 'area_ratio': 0.005101725933002029, 'removed_matched': False, 'larger_matched': True, 'removed_best_ref_iou': 0.004877775016235198, 'larger_best_ref_iou': 0.9478025478418899, 'reason_removed': 'smaller_unmatched_box_contained_in_larger_matched_prediction'}, {'image_filename': '100.jpg', 'case_id': '100', 'removed_label': 'target_2', 'kept_larger_label': 'target_1', 'removed_target_type': 'military_equipment', 'kept_larger_target_type': 'buildings', 'removed_bbox': [830.0, 476.0, 962.0, 542.0], 'kept_larger_bbox': [181.0, 37.0, 1075.0, 531.0], 'iou': 0.01638500704149063, 'containment_ratio': 0.8333333333333334, 'area_ratio': 0.01972665271852838, 'removed_matched': False, 'larger_matched': True, 'removed_best_ref_iou': 0.0, 'larger_best_ref_iou': 0.6713325425069198, 'reason_removed': 'smaller_unmatched_box_contained_in_larger_matched_prediction'}, {'image_filename': '155.jpg', 'case_id': '155', 'removed_label': 'target_1', 'kept_larger_label': 'target_0', 'removed_target_type': 'military_equipment', 'kept_larger_target_type': 'military_equipment', 'removed_bbox': [18.0, 111.0, 48.0, 143.0], 'kept_larger_bbox': [13.0, 93.0, 153.0, 176.0], 'iou': 0.08261617900172118, 'containment_ratio': 1.0, 'area_ratio': 0.08261617900172118, 'removed_matched': False, 'larger_matched': True, 'removed_best_ref_iou': 0.07224563515954245, 'larger_best_ref_iou': 0.8325485579752796, 'reason_removed': 'smaller_unmatched_box_contained_in_larger_matched_prediction'}]`

Interpretation:

- The best metric rule `r020` is containment-first and label-agnostic. It removes three unmatched small boxes without changing matches or FNs.
- The case-155 duplicate is explicitly removed.
- Cases 66, 67, 84, and 110 stay unchanged from v034a.
- One removal is cross-label (`military_equipment` inside a matched `buildings` box in case 100). That is safe under frozen eval, but it is broader than a strict same-wreck duplicate rule.
- The best stricter same-label rule is `r019`, with `181/38/23/61`; it removes two FPs, including the known case-155 duplicate, and may be the lower-risk implementation candidate if v040 prioritizes semantic narrowness over the extra case-100 FP reduction.
