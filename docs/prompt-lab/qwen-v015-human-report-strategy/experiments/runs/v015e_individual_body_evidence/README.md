# v015e Individual Body Evidence Runs

Status: `learning_dev_run_failed_recall_gate`

This lane is a user-approved prompt-only follow-up after the v015d
fail-closed result and the offline guard simulator. It does not
implement a structural output validator. It tests whether prompt
wording can focus the model on visible individual target-body evidence:
recover clear small/distant targets while still rejecting row
fragments, repeated pattern pieces, and broad group/scene boxes.

## Sequence

1. Run only the v015e hinge-smoke manifest.
2. Check the standard hinge gate and separate case `101` diagnostic.
3. Manually inspect case `101` and protected case `155`.
4. The user separately approved one learning-only 56-case dev run after the
   hinge result; do not run holdout, all-112, promotion, or runtime adoption
   from this evidence without separate approval.

## Commands

```bash
uv run python scripts/run_v015_candidate_manifest.py \
  --manifest docs/prompt-lab/qwen-v015-human-report-strategy/experiments/validation/human_report_challenge_v1_v015e_hinge_smoke.yaml \
  --overlay docs/prompt-lab/qwen-v015-human-report-strategy/experiments/overlays/qwen_1_2_v015e_detect_individual_body_evidence.yaml \
  --run-root docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015e_individual_body_evidence/executions

uv run python scripts/check_v015e_hinge_gate.py \
  --candidate-summary <candidate_manifest_run_summary.json> \
  --output <run-dir>/v015e_gate_check_summary.json

uv run python scripts/run_v015_candidate_manifest.py \
  --manifest docs/prompt-lab/qwen-v015-human-report-strategy/experiments/validation/human_report_challenge_v1_dev_56.yaml \
  --overlay docs/prompt-lab/qwen-v015-human-report-strategy/experiments/overlays/qwen_1_2_v015e_detect_individual_body_evidence.yaml \
  --run-root docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015e_individual_body_evidence/executions
```

## Boundary

These runs create local prompt-lab evidence only. They do not promote
`v015e`, edit runtime config, update source truth, implement a
structural guard, mutate human-report data, refresh Graphify, rebuild
evidence, update Mem0, run holdout, run all-112, or change runtime config.

## Hinge Smoke Result

Execution:
`executions/human_report_challenge_v1_v015e_hinge_smoke_2026-04-29_223729Z/`

Gate summary:

| Metric | v014 hinge baseline | v015e hinge result | Gate |
| --- | ---: | ---: | --- |
| matches | 8 | 10 | pass: greater than v014 |
| false negatives | 15 | 13 | pass: less than v014 |
| false positives | 1 baseline / 3 cap | 0 | pass |
| protected `155` | abstention-safe | abstention-safe | pass |
| case `101` diagnostic | manual hinge | row fragments suppressed, broad group box remains | fail |

`v015e` is the strongest prompt-only hinge result so far by aggregate metrics:
it beats the v014 hinge baseline on matches and false negatives while keeping
false positives at zero. However, the two-tier gate blocks a dev run because
case `101` still emits one broad group/scene box.

Selected case notes:

- `101`: 1 match, 11 false negatives, 0 false positives, 1 predicted target,
  row-fragment enumeration suppressed, broad group box still present.
- `13`: 2 matches, 0 false negatives, 0 false positives.
- `42`: 2 matches, 0 false negatives, 0 false positives.
- `147`: 1 match, 2 false negatives, 0 false positives.
- `12`: precision guard held with 1 match and 0 false positives.
- `28`: precision guard held with 1 match and 0 false positives.
- `19`: 1 match, 0 false negatives, 0 false positives.
- `155`: protected abstention remained safe.

Outcome: do not run the 56-case dev split without a separate manual decision
about whether the persistent case `101` broad-box failure should block all
prompt-only progress or be handled as a reference/eval-shape diagnostic caveat.

## Manual Case 101 Review

Review artifact:
`executions/human_report_challenge_v1_v015e_hinge_smoke_2026-04-29_223729Z/case_101_manual_review.md`

The manual review confirms the two-tier gate failure. `v015e` suppressed the
row-fragment enumeration, but the single predicted `101` target remains a broad
group/scene box rather than a tight individual-body detection. The match is
numerically helped by a very large foreground-tank reference box, and the
reference also contains a duplicated small target box, so `101` should remain a
manual diagnostic hinge rather than a purely automatic metric.

Recommendation: keep dev blocked unless the user explicitly approves a learning
run that treats `101` as a known manual-review failure and tests only whether
the stronger aggregate prompt signal generalizes beyond the hinge pack.

## Learning-Only Dev Result

Execution:
`executions/human_report_challenge_v1_dev_56_2026-04-29_231342Z/`

Artifacts:

- `candidate_manifest_run_summary.json`
- `eval/evaluation_2026-04-29_231946Z_summary.json`
- `eval/evaluation_2026-04-29_231946Z.csv`
- `v015e_dev_gate_summary.json`

Gate summary:

| Metric | v014 dev baseline | v015e dev result | Gate |
| --- | ---: | ---: | --- |
| matches | 70 | 61 | fail: not greater than v014 |
| false negatives | 47 | 56 | fail: not less than v014 |
| false positives | 17 baseline / 21 cap | 17 | pass: within cap and equal to v014 |
| protected `155` | abstention-safe | abstention-safe | pass |
| protected `166` | holdout control | not run | not applicable |

Interpretation: `v015e` preserved precision on the dev split but did not
generalize the hinge recall recovery. It produced fewer matches and more false
negatives than `v014`, while keeping false positives at the `v014` dev level.

Selected case notes:

- `101`: 1 match, 11 false negatives, 0 false positives, 1 predicted target.
  This preserves the same manual diagnostic caveat from hinge: case `101`
  remains too reference/eval-shape-sensitive to treat as an automatic win.
- `155`: protected object-not-found control remained abstention-safe.
- `67`: largest precision/recall stress case in dev, with 1 match, 10 false
  negatives, and 10 false positives.
- `84`: largest recall miss in dev, with 1 match and 12 false negatives.

Outcome: do not promote `v015e`, do not adopt it into runtime config, and do
not run holdout or all-112 from this candidate without a new decision. The
prompt-only lane has now produced useful evidence but not a dev-passing
candidate.
