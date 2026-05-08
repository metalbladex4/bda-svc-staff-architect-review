# v020c Baseline Comparison

| Surface | Matches | FNs | FPs | Combined errors |
|---|---:|---:|---:|---:|
| Old product v020c evidence | 186 | 33 | 25 | 58 |
| v031 vLLM official FP8 v020c baseline | 180 | 39 | 32 | 71 |

Delta versus old product v020c: `13` combined errors.

All-current image_count: `117`. Case 101 excluded: `True`.

## Key Cases

| Case | v031 vLLM FP8 | Old v020c selected metric |
|---|---:|---:|
| 12 | 1/0/0 | n/a |
| 14 | 1/1/0 | n/a |
| 16 | 1/0/0 | n/a |
| 66 | 8/0/5 | 8/0/4 |
| 67 | 10/1/2 | 9/2/4 |
| 77 | 1/0/1 | n/a |
| 84 | 9/4/0 | 8/5/0 |
| 88 | 1/0/1 | n/a |
| 97 | 1/0/1 | 1/0/2 |
| 103 | 1/0/3 | n/a |
| 155 | 2/0/2 | 2/0/0 |
| 166 | 1/0/0 | 1/0/0 |
| 172 | 3/0/0 | n/a |

Office-negative: image_count `1`, negative-scene FPs `0`, abstention correct `1`.

Acceptance: **red**, because combined errors were `71` and case 155 regressed from old v020c `2/0/0` to `2/0/2`.
