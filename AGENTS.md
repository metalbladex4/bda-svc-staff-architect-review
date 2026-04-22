# Gemma Model Worktree AGENTS

This worktree is the long-lived Gemma model root:

- branch: `model/gemma4-e4b`
- model line: `gemma4:e4b`
- role: reusable smoke-capable root for future Gemma feature branches

This file is local-only. Keep it out of Git and do not treat it as a tracked
deliverable.

## Mandatory Startup Sweep

Before substantial work in this worktree, sweep:

- `/home/williambenitez1/Capstone/z_reference_docs/WORKING_CHANGELOG.md`
- `/home/williambenitez1/Capstone/z_reference_docs/REFERENCE_MASTER_INDEX.md`
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3_model__gemma4-e4b/BRANCH_METADATA.md`
- `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_GEMMA.md`

Route next to:

- Gemma feature lab:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/README.md`
- Gemma evidence pack:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/README.md`

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
uv sync --all-packages
env OLLAMA_HOST=http://127.0.0.1:11435 uv run pytest tests/unit/test_yamls.py bda_eval/tests
uv run bda-svc -h
```

When the global `SequentialThinking` MCP server is available, use its
`sequentialthinking` tool on complex planning, root-cause debugging, and
multi-step tradeoff analysis tasks.

Use the Gemma checklist for refresh and smoke-flow commands:

- `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_GEMMA.md`

## Source-Of-Truth Rules

- Trust stable `main` if older docs drift on product/runtime behavior.
- Treat this model root as the tracked reusable Gemma default line.
- Treat prompt-lab conclusions and run-by-run behavior reads as belonging
  primarily to the Gemma feature lab unless explicitly promoted upward.

## Model-Line And Branch Rules

- This branch should keep tracked config aligned with the active Gemma default:
  `gemma4:e4b`.
- It should stay prompt-lab smoke-capable after upstream refreshes.
- It inherits the reusable review-artifact workflow and workspace sync support
  needed to keep future Gemma feature branches healthy.
- For local Gemma runs here, use
  `OLLAMA_HOST=http://127.0.0.1:11435` unless the Gemma host setup changes.

## Boundaries

- Do not treat this model root as the active prompt-iteration surface.
- Do not change the tracked model tag casually; doing so effectively opens a
  different model line.
- Do not rewrite remote history or accept automatic pull prompts without
  explicit intent.

## Documentation Discipline

- After meaningful work here, update the relevant living docs unless told not
  to.
- At minimum, consider:
  - `WORKING_CHANGELOG.md`
  - `REFERENCE_MASTER_INDEX.md`
  - the Gemma branch metadata file
  - the Gemma prompt-lab routing docs
