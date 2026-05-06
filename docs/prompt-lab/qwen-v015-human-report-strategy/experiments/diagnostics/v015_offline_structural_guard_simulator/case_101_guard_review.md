# Case 101 Guard Review

Status: `manual_review_required`

## v015a

- raw metrics: `{'matches': 3, 'false_negatives': 9, 'false_positives': 12, 'predicted_targets': 15}`
- guarded metrics: `{'matches': 0, 'false_negatives': 12, 'false_positives': 0, 'predicted_targets': 0}`
- suppressed labels: `['target_0', 'target_1', 'target_10', 'target_11', 'target_12', 'target_13', 'target_14', 'target_2', 'target_3', 'target_4', 'target_5', 'target_6', 'target_7', 'target_8', 'target_9']`
- broad-box flags: `1`
- row-fragment flags: `14`
- tiny-context flags: `0`

## v015b

- raw metrics: `{'matches': 3, 'false_negatives': 9, 'false_positives': 28, 'predicted_targets': 31}`
- guarded metrics: `{'matches': 0, 'false_negatives': 12, 'false_positives': 0, 'predicted_targets': 0}`
- suppressed labels: `['target_0', 'target_1', 'target_10', 'target_11', 'target_12', 'target_13', 'target_14', 'target_15', 'target_16', 'target_17', 'target_18', 'target_19', 'target_2', 'target_20', 'target_21', 'target_22', 'target_23', 'target_24', 'target_25', 'target_26', 'target_27', 'target_28', 'target_29', 'target_3', 'target_30', 'target_4', 'target_5', 'target_6', 'target_7', 'target_8', 'target_9']`
- broad-box flags: `1`
- row-fragment flags: `30`
- tiny-context flags: `30`

## v015c

- raw metrics: `{'matches': 3, 'false_negatives': 9, 'false_positives': 28, 'predicted_targets': 31}`
- guarded metrics: `{'matches': 0, 'false_negatives': 12, 'false_positives': 0, 'predicted_targets': 0}`
- suppressed labels: `['target_0', 'target_1', 'target_10', 'target_11', 'target_12', 'target_13', 'target_14', 'target_15', 'target_16', 'target_17', 'target_18', 'target_19', 'target_2', 'target_20', 'target_21', 'target_22', 'target_23', 'target_24', 'target_25', 'target_26', 'target_27', 'target_28', 'target_29', 'target_3', 'target_30', 'target_4', 'target_5', 'target_6', 'target_7', 'target_8', 'target_9']`
- broad-box flags: `1`
- row-fragment flags: `30`
- tiny-context flags: `30`

## v015d

- raw metrics: `{'matches': 1, 'false_negatives': 11, 'false_positives': 0, 'predicted_targets': 1}`
- guarded metrics: `{'matches': 0, 'false_negatives': 12, 'false_positives': 0, 'predicted_targets': 0}`
- suppressed labels: `['target_0']`
- broad-box flags: `1`
- row-fragment flags: `0`
- tiny-context flags: `0`

## Review Note

The guard should not be promoted from geometry alone. Case `101` has known
reference-shape caveats, and broad-box suppression can remove a metric match
even when the model's visual output is poor. Preserve raw outputs and require
manual review before any future dev recommendation.
