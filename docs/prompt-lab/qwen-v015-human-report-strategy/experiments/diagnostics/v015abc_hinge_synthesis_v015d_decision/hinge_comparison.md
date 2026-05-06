# v015a/v015b/v015c Hinge Comparison

Status: `diagnostic_only_no_prompt_text`

This comparison uses existing hinge-smoke run artifacts only. It does not run
new inference, author a v015d prompt, edit runtime config, mutate source truth,
or advance any candidate to dev.

## Aggregate Gate Comparison

| Candidate | Strategy | Gate | Matches | FN | FP | 101 preds | 101 FP | 101 row fragments | 101 broad box |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v015a | recall recovery | fail | 13 | 10 | 15 | 15 | 12 | yes | yes |
| v015b | distinct object guard | fail | 11 | 12 | 30 | 31 | 28 | yes | yes |
| v015c | count-first uncertainty gate | fail | 11 | 12 | 29 | 31 | 28 | yes | yes |

Gate thresholds: matches must be greater than `8`, false negatives must be
less than `15`, false positives must be no more than `3`, and protected case
`155` must remain abstention-safe.

## Per-Case Metrics

Cells are `matches/false_negatives/false_positives`.

| Case | v015a | v015b | v015c |
| --- | --- | --- | --- |
| 101.jpg | 3/9/12 | 3/9/28 | 3/9/28 |
| 13.jpg | 2/0/0 | 2/0/0 | 2/0/0 |
| 42.png | 1/1/0 | 1/1/0 | 1/1/0 |
| 147.jpg | 3/0/0 | 1/2/0 | 1/2/0 |
| 12.jpg | 1/0/1 | 1/0/1 | 1/0/0 |
| 28.jpg | 1/0/2 | 1/0/0 | 1/0/0 |
| 19.jpg | 1/0/0 | 1/0/1 | 1/0/1 |
| 155.jpg | 1/0/0 | 1/0/0 | 1/0/0 |

## Interpretation

- All three candidates recovered some recall compared with the v014 hinge
  baseline, but none kept false positives within the gate.
- v015a had the broadest mixed regression: `101`, `12`, and `28` all added
  false positives.
- v015b reduced some non-101 noise but amplified the `101` row-fragment failure.
- v015c fixed the visible `12`/`28` precision-guard regressions and preserved
  `155`, but still produced `31` detections and `28` false positives on `101`.
- The stable blocker is not general abstention or all precision guards. It is
  the model's failure to reject row-like fragments and broad group boxes on
  the `101` hinge case.
