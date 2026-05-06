# v015a Recall Recovery Runs

Status: `stopped_after_hinge_gate_failure`

This run lane is for the first human-report-informed Qwen `v015a`
candidate. The candidate is `v014`-derived and uses compact principles
to recover valid target enumeration while preserving false-positive
suppression.

## Sequence

1. Run the hinge-smoke manifest first.
2. Review case `101` for recall recovery and case `155` for protected
   out-of-scope abstention.
3. If the smoke run is not obviously broken, run the full 56-case dev
   split.
4. Do not run holdout or all-112 in this wave.

## Commands

```bash
uv run python scripts/run_v015_candidate_manifest.py \
  --manifest docs/prompt-lab/qwen-v015-human-report-strategy/experiments/validation/human_report_challenge_v1_hinge_smoke.yaml \
  --overlay docs/prompt-lab/qwen-v015-human-report-strategy/experiments/overlays/qwen_1_2_v015a_detect_recall_recovery.yaml

uv run python scripts/check_v015_strategy_gates.py \
  --candidate-summary <candidate_manifest_run_summary.json>
```

## Hinge Smoke Result

Run:
`executions/human_report_challenge_v1_hinge_smoke_2026-04-29_171438Z/`

Gate result: `failed`.

The candidate recovered recall pressure relative to the v014 hinge baseline,
but reopened too many false positives and therefore must not proceed to the
56-case dev split in this wave.

| Metric | v014 hinge baseline | v015a hinge smoke |
| --- | ---: | ---: |
| Matches | 8 | 13 |
| False negatives | 15 | 10 |
| False positives | 1 | 15 |

Gate checks:

- `matches_above_v014`: passed
- `false_negatives_below_v014`: passed
- `false_positives_within_limit`: failed
- protected case `155`: passed

Manual hinge case `101` remains the main tradeoff signal:

- reference targets: 12
- predicted targets: 15
- matches: 3
- false negatives: 9
- false positives: 12

Conclusion: `v015a_recall_recovery` is useful learning evidence, not a
promotion candidate. The next candidate should keep the enumeration recovery
idea but add a tighter distinct-target confidence/filtering rule before any
dev split is attempted.

## Boundary

These runs create local prompt-lab evidence only. They do not promote
`v015a`, edit runtime config, update source truth, mutate human-report
data, refresh Graphify, or update Mem0.
