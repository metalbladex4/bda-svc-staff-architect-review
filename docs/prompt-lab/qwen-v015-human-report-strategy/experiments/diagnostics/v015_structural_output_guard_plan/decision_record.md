# Decision Record

Status: `structural_guard_planning_approved`

## Accepted Evidence

- v015a recovered recall but reopened false positives.
- v015b amplified the case `101` row-fragment failure.
- v015c repaired side guards but still failed `101` with row fragments and a
  broad group box.
- v015d suppressed row fragments and drove false positives to zero, but recall
  collapsed to v014 level and one broad group box remained on `101`.

## Decision

Stop prompt-only attempts for this hinge cycle. Plan a structural output-shape
guard/validator experiment as a candidate-local offline simulator first.

## Not Approved Yet

- runtime guard implementation
- post-processing adoption in product flow
- source-truth/reference edits
- dev split, holdout, or all-112 execution
- promotion or runtime config adoption

## Next Approval Request

Approve or revise the offline guard simulator wave. That wave should apply the
guard to existing hinge predictions only and report raw-vs-guarded metrics
before any further runtime work.
