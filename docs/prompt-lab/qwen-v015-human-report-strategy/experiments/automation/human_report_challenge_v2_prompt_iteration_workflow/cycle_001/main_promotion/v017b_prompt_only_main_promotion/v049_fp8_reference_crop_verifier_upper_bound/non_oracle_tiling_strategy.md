# Non-Oracle Tiling Strategy

Reference-centered crops cannot be deployed or counted as product score. v050 should generate crops without ground truth.

Decision: `A`.

Recommended next action: Run v050 non-oracle tiling/crop pass.

## Options

|option|crop_generation_without_ground_truth|expected_fn_classes_recovered|fp_risk|merge_strategy|stop_criteria|
|---|---|---|---|---|---|
|fixed_tile_grid|2x2 or 3x3 overlapping grid over full image; no reference boxes.|['dense_valid_target_missed', 'small_valid_target_missed', 'smoke_or_debris_obscured']|medium|map crop detections to image coordinates, require verifier BDA relevance, then run existing FP postprocessors.|any FP increase on dense/control/office-negative or JSON instability.|
|existing_detection_anchor_crops|crop around existing detections plus surrounding context to find nearby missed targets.|['adjacent_target_confusion', 'dense_valid_target_missed']|medium_high|only add candidates not contained by anchors and not duplicate-like; require high verifier confidence.|reintroduces pp046a unsafe removals or adds local artifacts.|
|high_uncertainty_zone_crops|crop low-confidence/edge/dense regions from prediction geometry and image tiling heuristics.|['edge_or_boundary_target', 'small_valid_target_missed']|high_without_verifier|candidate must pass crop verifier and not overlap intact context.|candidate generation depends on reference boxes or adds context FPs.|
