# v017b Main Promotion False-Positive Visual Review
Status: `complete_recommendation_pending_user_override_decision`
## Purpose
Review the raw `22` false positives from the v017b prompt-only main all-current/no101 replay before deciding whether to override the strict FP cap of `21`. This package does not commit, restore, edit prompt text, mutate references, refresh Graphify, or write Mem0.
## Headline
- Raw gate: `165` matches, `54` FNs, `22` FPs.
- Strict FP cap: `21`, so the raw gate fails by `1`.
- Visual/accounting review: case `125` is an `object_not_found` abstention on a positive case. That is a real recall failure, but it is not a hallucinated extra target; if treated as FN-only, effective extra-target FPs are `21`, which meets the cap.
- Dense formation remains the real behavioral caveat: cases `66` and `67` contribute `14` of `22` raw FPs.
- Recommendation: threshold override is defensible, but because raw bda_eval still says fail, commit should wait for explicit user acceptance of the one-FP semantic override.
## Visual Artifact
- Contact sheet: `artifacts/v017b_fp_visual_review_contact_sheet.jpg`
## Case Review
### Case `12`
- Metrics: `1` matches, `0` FNs, `1` FPs.
- Labels: `duplicate_or_split_building_box, reference_grouping_caveat, true_precision_error`.
- Finding: The correct large damaged building is matched, but the model adds a second left-edge building/subsection box that duplicates part of the grouped building scene rather than a separate reference target.
- Promotion impact: Counts as a real extra target, but it is a bounded duplicate/split-building precision issue, not a broad scene-box failure.
### Case `15`
- Metrics: `0` matches, `1` FNs, `1` FPs.
- Labels: `bbox_localization_miss, paired_fn_fp, not_extra_target_enumeration`.
- Finding: The model appears to look near the tank but places the box too high and labels the target as no-damage, producing a paired FN/FP.
- Promotion impact: A real localization/assessment failure, but not evidence of runaway target enumeration.
### Case `17`
- Metrics: `1` matches, `0` FNs, `1` FPs.
- Labels: `adjacent_context_false_positive, true_precision_error`.
- Finding: The main destroyed building is matched well; the model adds an intact background/adjacent building as an extra no-damage building.
- Promotion impact: A real extra target, but limited and not a group/scene box.
### Case `19`
- Metrics: `1` matches, `0` FNs, `1` FPs.
- Labels: `adjacent_context_false_positive, true_precision_error`.
- Finding: The destroyed tank is matched well; the model adds a nearby building at the upper right as an extra target.
- Promotion impact: A real adjacent-context precision error.
### Case `66`
- Metrics: `8` matches, `0` FNs, `4` FPs.
- Labels: `dense_formation_overenumeration, row_fragment_or_road_debris_boxes, recall_recovery_with_fp_cost`.
- Finding: All eight reference trucks are recovered, but the model also emits four small near-road/front-row boxes over debris or ambiguous row fragments.
- Promotion impact: This is the clearest real FP cost of the prompt: recall is excellent, but dense-row over-enumeration remains.
### Case `67`
- Metrics: `1` matches, `10` FNs, `10` FPs.
- Labels: `dense_formation_anchor_failure, smoke_cloud_or_dust_row_boxes, true_precision_and_recall_failure, known_hard_case`.
- Finding: The model locks onto a row of dust/cloud/smoke positions and only matches the large foreground vehicle; ten distant reference vehicles are missed while ten unsupported row boxes are emitted.
- Promotion impact: Largest remaining blocker and the main caution against treating v017b as solved. It is a known hard dense-formation failure, not a new broad group-box regression.
### Case `90`
- Metrics: `1` matches, `0` FNs, `1` FPs.
- Labels: `duplicate_or_split_building_box, reference_grouping_caveat, true_precision_error`.
- Finding: Same visual pattern as case 12: the grouped severe-damage building reference is matched, with an extra left-side partial building/subsection box.
- Promotion impact: Real duplicate/split-building FP, bounded to a repeated building-fire image pattern.
### Case `110`
- Metrics: `1` matches, `6` FNs, `2` FPs.
- Labels: `duplicate_partial_boxes, distant_target_recall_failure, paired_precision_recall_failure`.
- Finding: The foreground armored vehicle is detected with duplicate/partial boxes, while small distant convoy vehicles are missed.
- Promotion impact: Real mixed failure, already present in the runtime-adoption replay; not the marginal +1 cap miss.
### Case `125`
- Metrics: `0` matches, `1` FNs, `1` FPs.
- Labels: `object_not_found_on_positive_case, eval_accounting_artifact, true_recall_failure_not_hallucinated_target`.
- Finding: The model abstains with object_not_found even though the current v2 reference is a destroyed military-equipment target. bda_eval counts that placeholder as an FP in addition to the FN.
- Promotion impact: This is the decisive +1 over the FP cap under raw bda_eval accounting. Semantically, it is a recall/abstention failure already counted as an FN, not a hallucinated extra target.
## Arguments For Override
- The raw cap miss is exactly one FP.
- The extra one can be attributed to case 125 object_not_found placeholder accounting on a positive case; that is already represented by a false negative and is not an extra hallucinated target.
- The main replay improved recall materially versus the worktree adopted-runtime all-current replay: +7 matches and -7 false negatives.
- Positive controls 155 and 166 passed, and office-negative abstention passed.
- No broad group/scene-box regression was found in the FP-bearing cases.
## Arguments Against Override
- Dense-formation case 67 remains severe, with 10 FPs and 10 FNs.
- Case 66 still over-enumerates dense-row fragments/debris even while matching all references.
- Cases 12/90 show a repeated duplicate/split-building pattern.
- Raw bda_eval gate remains a fail until the user explicitly accepts semantic FP accounting or changes the cap.
## Recommendation
Approve v017b promotion only if we explicitly accept that the case `125` `object_not_found` placeholder should not count as a target-hallucination FP for the cap. With that interpretation, the effective extra-target FP total is `21`, while recall gains remain substantial. Without that override, keep promotion paused or restore the backup.
