# Raw vs Guarded Metrics

Status: `offline_simulator_complete`

No VLM inference was run. Metrics compare existing raw hinge predictions
against separate guarded copies produced by the offline simulator.

## Aggregate Metrics

Cells are `matches/false_negatives/false_positives`.

| Candidate | Raw | Guarded | Suppressed targets | Guarded gate |
| --- | --- | --- | --- | --- |
| v015a | 13/10/15 | 6/17/3 | 19 | fail |
| v015b | 11/12/30 | 4/19/2 | 35 | fail |
| v015c | 11/12/29 | 4/19/1 | 35 | fail |
| v015d | 8/15/0 | 3/20/0 | 5 | fail |

## Case 101 Metrics

Cells are `matches/false_negatives/false_positives/predicted_targets`.

| Candidate | Raw 101 | Guarded 101 |
| --- | --- | --- |
| v015a | 3/9/12/15 | 0/12/0/0 |
| v015b | 3/9/28/31 | 0/12/0/0 |
| v015c | 3/9/28/31 | 0/12/0/0 |
| v015d | 1/11/0/1 | 0/12/0/0 |

## Interpretation

The simulator catches the expected row-fragment and broad-box shapes, but the
current suppression policy is too blunt for promotion: it usually reduces false
positives by deleting broad/row outputs at the cost of additional false
negatives. This is useful diagnostic evidence, not a runtime-ready guard.
