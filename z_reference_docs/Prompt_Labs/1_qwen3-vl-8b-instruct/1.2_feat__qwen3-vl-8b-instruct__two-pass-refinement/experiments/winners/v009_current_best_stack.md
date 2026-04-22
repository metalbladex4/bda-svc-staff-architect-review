# Current Best Stack

- winner version: `v009_unified_best-stack`
- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- status: `active_working_config`

## Unified Components

- `detect_objects` from `v006`
- `assess_damage` from `v008`
- `summarize_scene` from `v004`

## Primary Evidence

- `v006` confirmation repeat:
  - `experiments/runs/v006/run02_2026-04-16_114848_EDT/`
- `v008` confirmation repeat:
  - `experiments/runs/v008/run02_2026-04-16_122021_EDT/`
- broad frozen-stack sweep:
  - `experiments/runs/generalization_sweep/run02_2026-04-16_122803_EDT/`
- direct unified-stack comparison run:
  - `experiments/runs/v009/run01_2026-04-16_124434_EDT/`

## Why This Is The Current Winner

- fixes the operational firing false-damage regression
- fixes the destroyed-building one-target collapse
- keeps the office negative scene clean
- keeps the tank pressure case in the stronger branch-aware direction
- the direct `v009` run confirms the packaged winner behaves exactly like the
  already validated frozen stack on the focused comparison cases

## Residual Caution

- `destroyed_building5` still looks like a real building-severity overcall
- `destroyed_tank37` still looks like a logic/category consistency watch case
  under smoke/angle obscuration
- these are calibration watch cases, not recall failures

## Promotion Note

This stack is now promoted into tracked feature-branch config at:

- `src/bda_svc/pipeline/config.yaml`

It should now be treated as the active working config for this model line
going forward unless a later prompt cycle clearly outperforms it.

Tracked branch preservation now includes:

- `566892a` — `Add prompt-lab review artifacts to bda_eval`
- `127051a` — `Promote v009 prompt stack into pipeline config`
- `ebeae30` — `Install workspace packages in CI`

Review status:

- pushed to `origin/feat/qwen3-vl-8b-instruct/two-pass-refinement`
- PR `#134` is open against `upstream/main`
- GitHub CI is green
- exact prompt-behavior evidence still comes from the local prompt-lab runs,
  not from GitHub CI alone
