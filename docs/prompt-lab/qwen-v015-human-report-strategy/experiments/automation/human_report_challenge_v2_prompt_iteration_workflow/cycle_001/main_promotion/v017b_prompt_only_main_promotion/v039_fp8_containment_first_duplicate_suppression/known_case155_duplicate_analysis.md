# v039 Known Case-155 Duplicate Analysis

- v034a case 155 metrics: `2/0/1`
- Known duplicate reconstructed: `True`
- Smaller box: `target_1` bbox `[18.0, 111.0, 48.0, 143.0]`
- Larger box: `target_0` bbox `[13.0, 93.0, 153.0, 176.0]`
- Containment: `1.0`
- IoU: `0.08261617900172118`
- Area ratio: `0.08261617900172118`
- Center-inside: `True`
- Smaller is FP/unmatched: `True`
- Larger is TP/matched: `True`

v038 missed this pair because its minimum IoU threshold was `0.10`, while this nested duplicate's IoU is about `0.083`.
