# Failure Taxonomy For Qwen v015 Human-Report Strategy

Status: `analysis_only`

This taxonomy groups all 112 per-image deltas from the v009/v014
human-report comparison. It is prompt-learning evidence, not a promotion
decision and not final prompt text.

## Aggregate

- `v009`: 161 matches, 56 false negatives, 54 false positives.
- `v014`: 148 matches, 69 false negatives, 24 false positives.
- Strategy: balanced recovery, not direct v014 promotion.

## Categories

### `precision_recall_tradeoff`

- Definition: v014 reduced false positives versus v009 but also lost matches or increased false negatives.
- Case count: `1`
- Top cases: `101`
- Design implication: Preserve v014's abstention discipline while restoring target enumeration.

### `v014_recall_loss`

- Definition: v014 lost matches or increased false negatives without a false-positive reduction tradeoff.
- Case count: `7`
- Top cases: `147, 100, 11, 13, 42, 152, 169`
- Design implication: Repair target discovery and multi-target recall without relaxing object-existence rules globally.

### `v014_fp_suppression`

- Definition: v014 reduced false positives without increasing false negatives.
- Case count: `13`
- Top cases: `67, 28, 84, 66, 77, 12, 17, 18, 88, 90, 92, 97`
- Design implication: Keep these behaviors as positive evidence for precision guardrails.

### `persistent_recall_gap`

- Definition: v014 still has false negatives, even when not worse than v009.
- Case count: `21`
- Top cases: `44, 110, 160, 21, 53, 76, 91, 144, 154, 156, 14, 20`
- Design implication: Use as recall pressure only after separating model limitation from prompt wording.

### `persistent_false_positive_gap`

- Definition: v014 still has false positives.
- Case count: `4`
- Top cases: `19, 51, 69, 141`
- Design implication: Use as regression guard for hallucinated adjacent/background targets.

### `stable_or_clean`

- Definition: No material v014-v009 delta and no v014 false positive/false negative gap.
- Case count: `66`
- Top cases: `22, 93, 68, 70, 75, 82, 95, 99, 159, 3, 6, 7`
- Design implication: Preserve baseline behavior; do not over-tune against these cases.

### `protected_out_of_scope_negative`

- Definition: Object-not-found/out-of-scope controls.
- Case count: `2`
- Top cases: `155, 166`
- Design implication: Never optimize recall in a way that breaks abstention behavior.

### `qualitative_bbox_caveat`

- Definition: User-accepted bbox/schema caveat cases retained for qualitative interpretation.
- Case count: `6`
- Top cases: `160, 154, 159, 164, 142, 163`
- Design implication: Use for manual review; do not over-weight deterministic bbox metrics alone.
