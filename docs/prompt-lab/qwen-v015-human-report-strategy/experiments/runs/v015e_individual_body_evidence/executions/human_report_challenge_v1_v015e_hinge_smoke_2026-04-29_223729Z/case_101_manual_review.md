# Case 101 Manual Review

Status: `review_complete_dev_requires_separate_approval`

## Source Artifacts Reviewed

- `candidate_manifest_run_summary.json`
- `v015e_gate_check_summary.json`
- `predicted/101_2026-04-29_223740Z.json`
- `eval/images_bbox_review/bbox_review_101.jpg`
- `eval/images_bbox_predicted/bbox_101.jpg`
- `eval/images_bbox_reference/bbox_101.jpg`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/human_report_challenge_v1/references/101.json`

## Finding

`v015e` successfully suppressed the previous row-fragment enumeration on case
`101`, but it did not solve the individual-object boxing problem. It produced
one predicted target with bbox `[75, 13, 1000, 571]`, which spans most of the
image width and height and includes sky, foreground tank, background vehicles,
terrain, and surrounding context.

This is not an acceptable individual-body detection under the `v015e`
prompt intent. It should be treated as a broad group/scene box, not as evidence
that the prompt has learned the desired target-enumeration behavior.

## Metric Context

- Standard hinge gate: passed.
- Aggregate hinge result: 10 matches, 13 false negatives, 0 false positives.
- Protected `155`: passed.
- Case `101`: 1 match, 11 false negatives, 0 false positives, 1 predicted target.
- Case `101` row-fragment enumeration: suppressed.
- Case `101` broad group/scene box: still present.
- Two-tier gate: failed.

The single `101` match is not a clean visual success. It matches the large
foreground-tank reference target, but the predicted box is visually inflated
well beyond one connected target body.

## Reference/Eval Shape Caveats

Case `101` also has reference-shape concerns that should stay visible during
future decisions:

- `target_1` is a very large foreground tank box: `[87, 151, 996, 534]`.
- `target_7` and `target_8` are duplicate reference boxes:
  `[531, 131, 568, 170]`.
- The large reference box can make an oversized prediction look numerically
  better than it looks visually.

These caveats do not excuse the model output. They mean case `101` should be
used as a manual diagnostic hinge rather than a purely automatic pass/fail
metric.

## Recommendation

Do not treat `v015e` as having passed the full hinge gate. Do not run the dev
split automatically.

The prompt-learning signal is still useful: `v015e` is the strongest prompt-only
candidate so far by aggregate hinge metrics and preserves the side guards.
However, a dev run should require an explicit human decision to override the
strict `101` broad-box diagnostic gate for learning purposes only.

If approved later, the dev run should be framed as:

- `v015e` is not promoted.
- `101` remains a known manual-review failure.
- dev is used only to test whether the aggregate prompt signal generalizes
  beyond the hinge pack.
- no holdout, all-112, runtime adoption, or promotion follows without a
  separate approval.
