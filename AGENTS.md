# Gemma Doctrine Alignment Worktree AGENTS

This worktree is the local-only doctrine-replacement A/B surface for the Gemma
line.

- branch: `feat/gemma4-e4b/doctrine-bda-alignment`
- parent/control branch: `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- model line: `gemma4:e4b`
- role: Phase-1 doctrine audit and candidate validation

This file is local-only. Keep it out of Git.

## Mandatory Startup Sweep

Before substantial work here, sweep:

- `/home/williambenitez1/Capstone/z_reference_docs/WORKING_CHANGELOG.md`
- `/home/williambenitez1/Capstone/z_reference_docs/REFERENCE_MASTER_INDEX.md`
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/README.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/doctrine_source_crosswalk.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/phase1_only_doctrine_rules.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/worktree_test_playbook.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.2_feat__gemma4-e4b__doctrine-bda-alignment/README.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.2_feat__gemma4-e4b__doctrine-bda-alignment/BRANCH_METADATA.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/README.md`

Open the nearer `src/AGENTS.md` too when you are editing code under `src/`.

## Global Tooling Overlay

- Also follow `/home/williambenitez1/.codex/AGENTS.md` and
  `/home/williambenitez1/.codex/MCP_USAGE_GUIDE.md` for the current global MCP
  routing, tool-choice, and installed-agent baseline.
- When the global `SequentialThinking` MCP server is available, use its
  `sequentialthinking` tool before substantive updates to live maintained docs,
  global rules, or any `AGENTS.md`, in addition to the normal complex
  planning/debugging cases.
- The selectively installed global custom agents live in
  `/home/williambenitez1/.codex/agents/`; the full vendor catalog remains at
  `/home/williambenitez1/.codex/vendor_imports/github.com/VoltAgent/awesome-codex-subagents`,
  and delegation remains explicit.

## Key Commands Early

```bash
git status --short --branch
rg --files
rg -n "doctrine|physical_damage|detection_guidance" src tests z_reference_docs
uv sync --all-packages
uv run pytest tests/unit/test_yamls.py tests/unit/test_utilities.py
OLLAMA_HOST=http://127.0.0.1:11435 uv run bda-svc -h
```

When the global `SequentialThinking` MCP server is available, use its
`sequentialthinking` tool on complex planning, root-cause debugging, and
multi-step tradeoff analysis tasks.

## Source-Of-Truth Rules

- Trust stable runtime behavior on `main` when older docs drift.
- Treat this worktree as a local experiment, not stable product truth.
- Use the parent `3.1` Gemma feature branch as the doctrine control.
- Keep the runtime doctrine schema unchanged unless the runtime contract itself
  becomes the subject of a new planned experiment.

## Doctrine-Experiment Rules

- Stay Phase-1 PDA only:
  - no FDA
  - no target-system assessment
  - no recuperation-time logic
  - no reattack or restrike guidance
- Round one is primarily about:
  - `physical_damage_definitions`
  - `physical_damage_considerations`
- Avoid broad prompt rewrites here unless the doctrine results clearly require
  them.
- Judge candidate doctrine on both:
  - doctrinal fit
  - prompt/eval fit
- Respect the current Gemma host override:
  - `OLLAMA_HOST=http://127.0.0.1:11435`

## Validation Rule

- Minimum validation after meaningful doctrine edits:
  - `uv run pytest tests/unit/test_yamls.py tests/unit/test_utilities.py`
- For behavior validation, follow:
  - `/home/williambenitez1/Capstone/z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/worktree_test_playbook.md`

## Boundaries

- This branch intentionally starts from committed tip `9ae27e9`.
- Do not absorb the dirty local `v003` Gemma edits from the active `3.1`
  worktree unless that is made into a separate deliberate plan.
- Do not treat results here as promoted doctrine until the A/B evidence is
  clear.
- Keep all AGENTS files and doctrine experiment notes local-only.
