# v015b Distinct Object Guard Runs

Status: `stopped_after_hinge_gate_failure`

This lane tests the next natural candidate after the v015a hinge
diagnostic. `v015b` keeps the recall-recovery direction but adds a
distinct-object filter intended to prevent row-fragment enumeration,
broad group boxes, adjacent context false positives, and tiny ambiguous
distant detections.

## Sequence

1. Run only the v015b hinge-smoke manifest.
2. Check the gate summary.
3. Manually inspect case `101` and protected case `155`.
4. Do not run the 56-case dev split unless hinge smoke passes and the
   user separately approves the dev run.

## Commands

```bash
uv run python scripts/run_v015_candidate_manifest.py \
  --manifest docs/prompt-lab/qwen-v015-human-report-strategy/experiments/validation/human_report_challenge_v1_v015b_hinge_smoke.yaml \
  --overlay docs/prompt-lab/qwen-v015-human-report-strategy/experiments/overlays/qwen_1_2_v015b_detect_distinct_object_guard.yaml \
  --run-root docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015b_distinct_object_guard/executions

uv run python scripts/check_v015_strategy_gates.py \
  --candidate-summary <candidate_manifest_run_summary.json> \
  --output <run-dir>/v015b_gate_check_summary.json
```

## Hinge Smoke Result

Run:
`executions/human_report_challenge_v1_v015b_hinge_smoke_2026-04-29_190631Z/`

Gate result: `failed`.

`v015b` preserved some recall recovery relative to v014, but the distinct-object
guard did not stop the case `101` row-fragment failure. It amplified that
pattern: case `101` produced one broad group/scene box plus a tightly regular
row of small military-equipment boxes across the image.

| Metric | v014 hinge baseline | v015a hinge smoke | v015b hinge smoke |
| --- | ---: | ---: | ---: |
| Matches | 8 | 13 | 11 |
| False negatives | 15 | 10 | 12 |
| False positives | 1 | 15 | 30 |

Gate checks:

- `matches_above_v014`: passed
- `false_negatives_below_v014`: passed
- `false_positives_within_limit`: failed
- protected case `155`: passed

Case `101` remained the blocking failure:

- reference targets: 12
- predicted targets: 31
- matches: 3
- false negatives: 9
- false positives: 28

Conclusion: `v015b_distinct_object_guard` is learning evidence, not a candidate
to advance. Do not run the 56-case dev split from this candidate. The next
candidate should abandon the "scan repeated rows" framing and instead use a
stricter count-first or cap/uncertainty strategy for case `101` before any
enumeration expansion.

## Boundary

These runs create local prompt-lab evidence only. They do not promote
`v015b`, edit runtime config, update source truth, mutate human-report
data, refresh Graphify, rebuild evidence, or update Mem0.
