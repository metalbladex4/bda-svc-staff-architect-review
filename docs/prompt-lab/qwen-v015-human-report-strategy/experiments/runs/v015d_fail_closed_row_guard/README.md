# v015d Fail-Closed Row Guard Runs

Status: `stopped_after_hinge_gate_failure`

This lane is the final approved prompt-only attempt after the
v015a/v015b/v015c hinge synthesis. It does not implement a structural
output validator. It tests whether prompt wording alone can fail closed
on row-fragment enumeration and broad group boxes while preserving the
side-guard gains from v015c.

## Sequence

1. Run only the v015d hinge-smoke manifest.
2. Check the standard hinge gate and separate case `101` diagnostic.
3. Manually inspect case `101` and protected case `155`.
4. Do not run the 56-case dev split unless hinge smoke passes and the
   user separately approves the dev run.

## Commands

```bash
uv run python scripts/run_v015_candidate_manifest.py \
  --manifest docs/prompt-lab/qwen-v015-human-report-strategy/experiments/validation/human_report_challenge_v1_v015d_hinge_smoke.yaml \
  --overlay docs/prompt-lab/qwen-v015-human-report-strategy/experiments/overlays/qwen_1_2_v015d_detect_fail_closed_row_guard.yaml \
  --run-root docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015d_fail_closed_row_guard/executions

uv run python scripts/check_v015d_hinge_gate.py \
  --candidate-summary <candidate_manifest_run_summary.json> \
  --output <run-dir>/v015d_gate_check_summary.json
```

## Boundary

These runs create local prompt-lab evidence only. They do not promote
`v015d`, edit runtime config, update source truth, implement a
structural guard, mutate human-report data, refresh Graphify, rebuild
evidence, or update Mem0.

## Hinge Smoke Result

Execution:
`executions/human_report_challenge_v1_v015d_hinge_smoke_2026-04-29_220141Z/`

Gate summary:

| Metric | v014 hinge baseline | v015d hinge result | Gate |
| --- | ---: | ---: | --- |
| matches | 8 | 8 | fail: must be greater than v014 |
| false negatives | 15 | 15 | fail: must be less than v014 |
| false positives | 1 baseline / 3 cap | 0 | pass |
| protected `155` | abstention-safe | abstention-safe | pass |
| case `101` diagnostic | manual hinge | row fragments suppressed, broad group box remains | fail |

`v015d` confirmed the prompt-only fail-closed tradeoff. It drove false
positives to zero and suppressed the case `101` row-fragment enumeration, but
it became too conservative to beat v014 recall and still emitted one broad
group/scene box on `101`.

Selected case notes:

- `101`: 1 match, 11 false negatives, 0 false positives, 1 predicted target,
  row-fragment enumeration suppressed, broad group box still present.
- `12`: precision guard held with 1 match and 0 false positives.
- `28`: precision guard held with 1 match and 0 false positives.
- `155`: protected abstention remained safe with 0 false positives.

Outcome: do not run the 56-case dev split for `v015d` without a separate
approval. As the final prompt-only attempt, this result supports planning a
structural output-shape guard/validator rather than spending another prompt-only
hinge attempt.
