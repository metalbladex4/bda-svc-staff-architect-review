# Qwen Doctrine Alignment Worktree AGENTS

This worktree is the local-only doctrine-replacement A/B surface for the Qwen
line.

- branch: `feat/qwen3-vl-8b-instruct/doctrine-bda-alignment`
- parent/control branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
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
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/README.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/BRANCH_METADATA.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/README.md`

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
uv run bda-svc -h
```

When the global `SequentialThinking` MCP server is available, use its
`sequentialthinking` tool on complex planning, root-cause debugging, and
multi-step tradeoff analysis tasks.

## Source-Of-Truth Rules

- Trust stable runtime behavior on `main` when older docs drift.
- Treat this worktree as a local experiment, not stable product truth.
- Use the parent `1.2` Qwen feature branch as the doctrine control.
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

## Validation Rule

- Minimum validation after meaningful doctrine edits:
  - `uv run pytest tests/unit/test_yamls.py tests/unit/test_utilities.py`
- For behavior validation, follow:
  - `/home/williambenitez1/Capstone/z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/worktree_test_playbook.md`

## Documentation Discipline

- After meaningful work, update:
  - the doctrine experiment package
  - this branch README and metadata if status changed
  - broader local routing docs if the experiment structure changes

## Boundaries

- Do not disturb the active `1.2` feature branch while using this worktree.
- Do not treat results here as promoted doctrine until the A/B evidence is
  clear.
- Keep all AGENTS files and doctrine experiment notes local-only.
