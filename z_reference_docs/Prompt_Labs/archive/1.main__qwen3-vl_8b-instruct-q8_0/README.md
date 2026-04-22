# Archived Qwen3-VL 8B Instruct Q8 Prompt Lab

This lab is the archived working area for prompt refinement of
`qwen3-vl:8b-instruct-q8_0`.

Source context:

- branch/workspace: `main`
- status: archived on `2026-04-10`

## Goal

Preserve the earlier prompt surfaces, eval manifests, run outputs, and decision
history from the `qwen3-vl:8b-instruct-q8_0` phase without
changing the runtime contract:

- same placeholders
- same JSON fields
- same configured bbox contract
- same doctrine categories
- same Ollama message structure

## Prompt Surface Order

1. `system`
2. `assess_damage`
3. `detect_objects`
4. `summarize_scene`

## Folder Map

- `baseline/`
  Current prompt/config snapshot copied from the live pipeline.
- `dossier/`
  Qwen-specific prompting rules and doctrine/schema mapping.
- `evals/`
  Separate tracks so prompt failures stay attributable.
- `experiments/`
  Version log, failure taxonomy, version snapshots, and accepted winners.

## Archive Status

This lab is no longer the active prompt workspace.

Use it for:

- historical experiment review
- prior failure-mode reference
- archived prompt/version history

Do not use it for:

- new baseline refreshes
- new active runs
- current-main promotion decisions

## Experiment Output Rule

New experiment outputs belong under:

- `experiments/runs/YYYY-MM-DD_HHMMSS_TZ/`

Each timestamped run folder should include a `RUN_MANIFEST.md` and separate
condition subfolders when comparing baseline and candidate prompts.

## Source Priority

Use sources in this order:

1. `z_reference_docs/Prompting/Qwen/`
2. `z_reference_docs/BDAs/`
3. `z_reference_docs/Prompting/OpenAI_GPT/`
4. `z_reference_docs/Prompting/Anthropic_Claude/`
5. `z_reference_docs/Prompting/Google_Gemini/`

## Promotion Rule

No prompt text should be copied into `src/bda_svc/pipeline/config.yaml` until it
passes the local eval tracks and manual doctrinal review recorded in this lab.

## Archived Highlights

- `v001` through `v004` preserve the pre-merge draft chain.
- `v005` through `v008` preserve the first reconciled post-merge chain.
- `v009` and `v010` record the first detection-localization follow-up attempts.
- April 6 run outputs remain here as historical evidence, not active
  current-main evidence.
- The live runtime has since moved to `qwen3-vl:8b-instruct`, so the active
  prompt workflow now continues in the separate current lab.
