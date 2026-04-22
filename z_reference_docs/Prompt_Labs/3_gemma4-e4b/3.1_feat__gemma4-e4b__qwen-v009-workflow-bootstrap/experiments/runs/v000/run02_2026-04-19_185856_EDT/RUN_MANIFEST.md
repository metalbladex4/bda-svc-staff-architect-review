# Gemma `v000` Run 02

- run type: `v000 baseline reset`
- branch: `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- model line: `gemma4:e4b`
- purpose: rebuild the Gemma baseline on the current `e7a22a9` repo base
  after the upstream detect-contract change altered the old evidence chain
- run folder: `run02_2026-04-19_185856_EDT`

## Runtime Method

The machine still had a system Ollama install at `0.15.2`, which is too old
for `gemma4:e4b`.

So this run used:

- user-local Ollama binary:
  - `/home/williambenitez1/.local/lib/ollama-local/bin/ollama`
- user-local Ollama version:
  - `0.21.0`
- user-local server:
  - `127.0.0.1:11435`
- model storage:
  - `/home/williambenitez1/.ollama-gemma4-models`

No tracked runtime code changes were required because `bda-svc` already
supports `OLLAMA_HOST`.

## Config Under Test

- tracked feature-branch config:
  - `src/bda_svc/pipeline/config.yaml`
- saved effective config for this run:
  - `v000_effective_config.yaml`

This reset intentionally made no prompt edits. It reran the current tracked
Gemma config as-is on the newer repo base.

## Validation Pack

- `tank_pressure`
- `destroyed_tank15`
- `operational_tank4`
- `destroyed_building4`
- `operational_building7`
- `office_negative`

## Per-Case Artifact Pattern

Each case folder contains:

- `images/`
- `gemma_v000_candidate/`
- `bda_svc.stdout.txt`
- `bda_svc.stderr.txt`
- `bda_svc_exit_code.txt`
- `eval_vs_qwen_v009/`
- `eval_vs_origin_main_baseline/`

## Comparison References

Historical Gemma reference:

- pre-refresh Gemma baseline:
  - `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/v000/run01_2026-04-17_134308_EDT/`

Reference pack:

- active Qwen stack:
  - `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/generalization_sweep/run02_2026-04-16_122803_EDT/`

Reference subfolders per case:

- `frozen_v006_v008_v004_stack/`
- `v000_baseline/`

Important note:

- there is not yet a fresh six-case post-`e7a22a9` Qwen comparison pack
- for this reset, the established frozen Qwen `v009` sweep remains the active
  six-case comparison reference

## Headline Result

The rebuilt post-`e7a22a9` Gemma baseline is not a clean continuation of the
first live Gemma run.

What held:

- `destroyed_tank15`
- `operational_building7`
- `office_negative`

What regressed:

- `tank_pressure` collapsed to `object_not_found / NOT APPLICABLE`
- `operational_tank4` regressed to `DAMAGED / PROBABLE`
- `destroyed_building4` still undercalled severity and remained unreliable

## Important Eval Note

- the office negative case still does not produce a normal evaluation CSV
  because `bda_eval` logs `NOT_APPLICABLE` as unknown
- however, the eval lanes now still exit `0` and emit review artifacts for that
  case
- `tank_pressure` also logs the predicted `NOT_APPLICABLE` path during
  evaluation, so its CSVs should be interpreted alongside the raw JSON and
  review images, not on CSV alone

## Reset Decision

- `run02` becomes the active Gemma `v000` anchor for the current repo base
- `run01` remains preserved as pre-refresh historical evidence
- do not open `v001` yet
- first reconsider the inherited detect-contract effect before deciding
  whether prompt iteration should continue
