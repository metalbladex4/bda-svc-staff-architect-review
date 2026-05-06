# v017b vs v017d Precision Challenger Review

## Bottom Line

`v017b_group_box_rejection` is a real precision challenger to
`v017d_visual_anchor_lock`.

On the same fresh `human_report_challenge_v2_dev_55_no101` rerun:

| Candidate | Matches | FNs | FPs | Positive 155 |
| --- | ---: | ---: | ---: | --- |
| `v017d_visual_anchor_lock` | 72 | 34 | 16 | pass |
| `v017b_group_box_rejection` | 72 | 34 | 13 | pass |

The aggregate comparison is not just noise: v017b preserves v017d recall while
removing three total false positives. The review should reopen the primary
candidate decision rather than treating v017d as locked.

## Review Scope

The candidates differ on four dev cases:

| Case | v017d | v017b | Delta v017b - v017d | Visual read |
| --- | --- | --- | --- | --- |
| `66` | 8 / 0 / 6 | 8 / 0 / 4 | 0 / 0 / -2 | v017b trims two smallest far-row/fragment outputs while preserving matches. Both still over-enumerate the convoy row. |
| `67` | 1 / 10 / 8 | 1 / 10 / 9 | 0 / 0 / +1 | v017b adds one extra false positive and still anchors many boxes around smoke/row fragments. |
| `84` | 5 / 8 / 1 | 5 / 8 / 0 | 0 / 0 / -1 | v017b removes one extra row-span output, but the remaining outputs are still broad horizontal row-span boxes. |
| `103` | 1 / 0 / 1 | 1 / 0 / 0 | 0 / 0 / -1 | v017b removes the duplicate/secondary building output and keeps the single matched broad building target. |
| `155` | 2 / 0 / 0 | 2 / 0 / 0 | 0 / 0 / 0 | corrected positive control remains safe for both. |

Cell format is `matches / false negatives / false positives`.

## Case Notes

### Case 66

v017b reduces predicted targets from `14` to `12` and false positives from `6`
to `4`, without losing any of the `8` matches. The saved false positives are
mostly from the smallest far-row or fragment-like outputs at the left side of
the convoy line.

This is a real improvement, but it is not a clean solution. Both candidates
still over-enumerate the row and still produce large/front boxes whose shape is
partly governed by the reference geometry.

Evidence:

- v017d review image:
  `../runs/v017d_visual_anchor_lock/human_report_challenge_v2_dev_55_no101_2026-05-03_173618Z/eval/images_bbox_review/bbox_review_66.jpg`
- v017b review image:
  `../runs/v017b_group_box_rejection/human_report_challenge_v2_dev_55_no101_2026-05-03_181508Z/eval/images_bbox_review/bbox_review_66.jpg`

### Case 67

This is the main caution against automatically replacing v017d. v017b adds one
false positive: `9` FPs versus v017d's `8`, with no recall gain. Visually, both
candidates still struggle with smoke-obscured distant vehicles and row
fragments. v017b changes the anchor pattern but does not fix the underlying
dense/smoke case.

Evidence:

- v017d review image:
  `../runs/v017d_visual_anchor_lock/human_report_challenge_v2_dev_55_no101_2026-05-03_173618Z/eval/images_bbox_review/bbox_review_67.jpg`
- v017b review image:
  `../runs/v017b_group_box_rejection/human_report_challenge_v2_dev_55_no101_2026-05-03_181508Z/eval/images_bbox_review/bbox_review_67.jpg`

### Case 84

v017b removes one false positive while preserving the same `5` matches and `8`
false negatives. The visual improvement is modest: the remaining predictions
are still broad row-span boxes rather than clean individual vehicle boxes.

So this counts as a precision gain, but not as evidence that v017b has solved
the dense-row failure mode.

Evidence:

- v017d review image:
  `../runs/v017d_visual_anchor_lock/human_report_challenge_v2_dev_55_no101_2026-05-03_173618Z/eval/images_bbox_review/bbox_review_84.jpg`
- v017b review image:
  `../runs/v017b_group_box_rejection/human_report_challenge_v2_dev_55_no101_2026-05-03_181508Z/eval/images_bbox_review/bbox_review_84.jpg`

### Case 103

This is the cleanest v017b win. v017d emits two building detections, one matched
and one false positive. v017b emits only the matched broad building target,
cutting the extra FP without recall loss.

Evidence:

- v017d review image:
  `../runs/v017d_visual_anchor_lock/human_report_challenge_v2_dev_55_no101_2026-05-03_173618Z/eval/images_bbox_review/bbox_review_103.jpg`
- v017b review image:
  `../runs/v017b_group_box_rejection/human_report_challenge_v2_dev_55_no101_2026-05-03_181508Z/eval/images_bbox_review/bbox_review_103.jpg`

### Case 155

No change: both candidates preserve the corrected positive-control behavior
with `2` matches, `0` false negatives, and `0` false positives.

## Decision

The safest read is:

- v017b is no longer just an old near-miss; it is a credible precision
  challenger.
- v017d should not be treated as automatically locked as the primary candidate.
- v017b should not be auto-promoted either, because its advantage is partly
  concentrated in cases where the visual failure mode remains unresolved, and
  it worsens case `67`.

Recommended status:

`v017b_and_v017d_candidate_pair_pending_user_decision`

Recommended next move:

review v017b as a possible primary replacement before any holdout or promotion.
Do not run holdout, all-current, runtime adoption, or promotion until that
decision is explicit.
