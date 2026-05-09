# v034a vs v035a Delta Review

- v034a micro-pack: `{'155': {'matches': 2, 'false_negatives': 0, 'false_positives': 1}, '66': {'matches': 8, 'false_negatives': 0, 'false_positives': 5}, '67': {'matches': 10, 'false_negatives': 1, 'false_positives': 3}, '84': {'matches': 8, 'false_negatives': 5, 'false_positives': 0}, '97': {'matches': 1, 'false_negatives': 0, 'false_positives': 1}, '110': {'matches': 3, 'false_negatives': 4, 'false_positives': 1}, '166': {'matches': 1, 'false_negatives': 0, 'false_positives': 0}}`
- v035a micro-pack: `{'155': {'matches': 2, 'false_negatives': 0, 'false_positives': 0}, '66': {'matches': 8, 'false_negatives': 0, 'false_positives': 6}, '67': {'matches': 7, 'false_negatives': 4, 'false_positives': 5}, '84': {'matches': 8, 'false_negatives': 5, 'false_positives': 0}, '97': {'matches': 0, 'false_negatives': 1, 'false_positives': 1}, '110': {'matches': 4, 'false_negatives': 3, 'false_positives': 2}, '166': {'matches': 1, 'false_negatives': 0, 'false_positives': 0}}`

Priority deltas:

- Case 155 improved from `2/0/1` to `2/0/0`; the removed box was v034a target_1 `{'target_1': [18, 111, 48, 143]}`.
- Case 67 regressed from `10/1/3` to `7/4/5`; valid dense/crowded targets became FNs.
- Case 66 worsened from `8/0/5` to `8/0/6`.
- Case 84 stayed `8/5/0`; no recall repair.
- Case 110 stayed controlled relative to v032d, changing from `3/4/1` to `4/3/2`.
- Case 166 and office-negative passed.
