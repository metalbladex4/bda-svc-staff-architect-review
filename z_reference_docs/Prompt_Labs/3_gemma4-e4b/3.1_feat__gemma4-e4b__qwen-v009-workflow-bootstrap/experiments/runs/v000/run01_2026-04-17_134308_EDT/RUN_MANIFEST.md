# Gemma `v000` Run 01

- run type: `v000 baseline`
- branch: `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- model line: `gemma4:e4b`
- purpose: execute the first live Gemma baseline against the inherited Qwen
  seed case and six-case comparison pack
- run folder: `run01_2026-04-17_134308_EDT`

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

This baseline is a semantic port of the active Qwen `v009` working stack into
Gemma 4 E4B:

- `detect_objects` semantics from the active Qwen line
- `assess_damage` semantics from the active Qwen line
- `summarize_scene` semantics from the active Qwen line
- detection model tag: `gemma4:e4b`
- assessment model tag: `gemma4:e4b`

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

Reference pack:

- active Qwen stack:
  - `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/generalization_sweep/run02_2026-04-16_122803_EDT/`

Reference subfolders per case:

- `frozen_v006_v008_v004_stack/`
- `v000_baseline/`

## Headline Result

Gemma `v000` is immediately usable as a real baseline, but it is not yet a
drop-in Qwen replacement.

What held:

- tank seed stayed doctrinally correct at `DESTROYED / PROBABLE`
- destroyed and operational equipment cases stayed sensible
- operational building stayed sensible
- office negative stayed clean

What failed:

- `destroyed_building4` drifted badly on both building separation and severity

## Important Eval Note

For the office negative case, the raw Gemma JSON is correct, but `bda_eval`
still does not emit a normal evaluation CSV for `NOT APPLICABLE` damage labels.
That case should still be judged from the raw JSON and image artifacts first.
