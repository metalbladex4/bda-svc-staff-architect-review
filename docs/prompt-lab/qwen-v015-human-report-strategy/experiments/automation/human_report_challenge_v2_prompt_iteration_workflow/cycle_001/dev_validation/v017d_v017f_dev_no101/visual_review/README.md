# v017d Dev Outlier Visual Review

Status: `visual_review_complete`

This package reviews the visually important `v017d_visual_anchor_lock` dev
outliers from the bounded `human_report_challenge_v2_dev_55_no101` validation.
It does not rerun inference, alter source truth, alter references, author a new
prompt, or promote a candidate.

## Scope

- Candidate: `v017d_visual_anchor_lock`
- Split: `human_report_challenge_v2_dev_55_no101`
- Run: `../runs/v017d_visual_anchor_lock/human_report_challenge_v2_dev_55_no101_2026-05-03_063205Z/`
- Reviewed cases: `66`, `67`, `84`, `100`, `103`, `147`, `155`, `97`
- Excluded from forward evaluation: `101`
- Holdout-only and absent: `166`

The selected cases cover every dev case with a false positive, every dev case
with at least two false negatives, and the important positive/control cases
from the v017 lane.

## Readout

The main failure concentration is not a general collapse. It is a dense-target
visual anchoring problem:

- `67`, `84`, and `66` account for `33` of the `50` v017d dev error units.
- `67` is the largest blocker: many missed references plus many misaligned or
unsupported boxes in a receding row of military equipment.
- `84` shows broad row/span boxes over formation targets instead of clean
individual target boxes.
- `66` recovers all reference targets but over-enumerates extra dense-row
vehicle candidates.

The secondary pattern is building/background recall undersegmentation:

- `100` and `147` each miss two reference targets while selecting the dominant
foreground or central object.
- `103` adds a duplicate/broad building-complex prediction against one large
reference.
- `97` passes, but the reference is itself broad and scene-scale, so it should
not be treated as proof that broad building boxes are generally safe.

## Recommendation

Keep `v017d_visual_anchor_lock` as the primary candidate, but do not move to
holdout or promotion from metrics alone. The next prompt-engineering decision
should focus on dense formation anchoring: suppress unsupported row/stripe boxes
and evenly spaced placeholder candidates while preserving real separate body
recall.

Details:

- `v017d_dev_outlier_visual_review.md`
- `v017d_dev_outlier_visual_review.json`
- `source_manifest.json`
- `dense_formation_comparison/`
