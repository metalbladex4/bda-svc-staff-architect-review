# v015c Count-First Uncertainty Gate Runs

Status: `stopped_after_hinge_gate_failure`

This lane tests the next candidate after v015a/v015b both reopened the
case `101` row-fragment failure. `v015c` abandons row-enumeration
wording and instead asks the model to make a conservative count before
emitting detections.

## Sequence

1. Run only the v015c hinge-smoke manifest.
2. Check the standard hinge gate and the separate case `101` diagnostic.
3. Manually inspect case `101` and protected case `155`.
4. Do not run the 56-case dev split unless hinge smoke passes and the
   user separately approves the dev run.

## Commands

```bash
uv run python scripts/run_v015_candidate_manifest.py \
  --manifest docs/prompt-lab/qwen-v015-human-report-strategy/experiments/validation/human_report_challenge_v1_v015c_hinge_smoke.yaml \
  --overlay docs/prompt-lab/qwen-v015-human-report-strategy/experiments/overlays/qwen_1_2_v015c_detect_count_first_uncertainty_gate.yaml \
  --run-root docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015c_count_first_uncertainty_gate/executions

uv run python scripts/check_v015c_hinge_gate.py \
  --candidate-summary <candidate_manifest_run_summary.json> \
  --output <run-dir>/v015c_gate_check_summary.json
```

## Boundary

These runs create local prompt-lab evidence only. They do not promote
`v015c`, edit runtime config, update source truth, mutate human-report
data, refresh Graphify, rebuild evidence, or update Mem0.

## Hinge Smoke Result

Execution:
`executions/human_report_challenge_v1_v015c_hinge_smoke_2026-04-29_195257Z/`

Gate summary:

| Metric | v014 hinge baseline | v015c hinge result | Gate |
| --- | ---: | ---: | --- |
| matches | 8 | 11 | pass: greater than v014 |
| false negatives | 15 | 12 | pass: less than v014 |
| false positives | 1 baseline / 3 cap | 29 | fail: above cap |
| protected `155` | abstention-safe | abstention-safe | pass |
| case `101` diagnostic | manual hinge | row fragments + broad group box | fail |

`v015c` recovered some valid recall relative to `v014` but failed the
standard hinge gate because false positives rebounded well above the allowed
cap. The failure is concentrated primarily in case `101`, where the run still
produced row-fragment enumeration and one broad group/scene box:

- `101`: 3 matches, 9 false negatives, 28 false positives, 31 predicted
  targets, row-fragment enumeration present, broad group box present.
- `12`: precision guard held with 1 match and 0 false positives.
- `28`: precision guard held with 1 match and 0 false positives.
- `155`: protected abstention remained safe with 0 false positives.

Outcome: do not run the 56-case dev split for `v015c` without a separate
approval. The next natural step is to treat `v015c` as learning evidence for a
possible `v015d` design, not as a candidate ready for deeper evaluation.
