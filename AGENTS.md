# Gemma Feature Worktree AGENTS

This worktree is the active Gemma bootstrap prompt lab:

- branch: `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- model line: `gemma4:e4b`
- role: active Gemma bootstrap and prompt-evidence surface

This file is local-only. Keep it out of Git and do not treat it as a tracked
deliverable.

## Mandatory Startup Sweep

Before substantial work in this worktree, sweep:

- `/home/williambenitez1/Capstone/z_reference_docs/WORKING_CHANGELOG.md`
- `/home/williambenitez1/Capstone/z_reference_docs/REFERENCE_MASTER_INDEX.md`
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/README.md`
- `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_GEMMA.md`

Route next to:

- Gemma evidence pack:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/README.md`
- Gemma operational rules:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/operational_prompt_rules.md`
- prompt-lab index:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/PROMPT_LABS_INDEX.md`

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
env OLLAMA_HOST=http://127.0.0.1:11435 uv run bda-svc -h
```

When the global `SequentialThinking` MCP server is available, use its
`sequentialthinking` tool on complex planning, root-cause debugging, and
multi-step tradeoff analysis tasks.

Use the Gemma checklist for refresh and smoke-flow commands:

- `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_GEMMA.md`

## Source-Of-Truth Rules

- Trust stable `main` if older docs drift on product/runtime behavior.
- For active Gemma prompt claims, trust the current Gemma feature lab evidence
  chain over older planning notes.
- Treat prompt-lab results as local evidence first; promote them deliberately
  before treating them as tracked truth.

## Model-Line And Methodology Rules

- This is the active Gemma bootstrap line.
- `v000` is the first live Gemma baseline and remains the active evidence
  anchor until a later version is intentionally created.
- The Gemma line starts from the active Qwen `v009` prompt semantics and tests
  whether Gemma can stay inside the same BDA runtime contract.
- Keep `gemma4:e4b` as the active model and `gemma4:e2b` as comparison-only
  unless the line is intentionally redefined.
- Keep `thinking` disabled unless there is an explicit decision to open that
  behavior.
- Gemma local runs currently require
  `OLLAMA_HOST=http://127.0.0.1:11435`.

## Boundaries

- Do not move into Gemma `v001` or later iterations unless the user explicitly
  asks for that next phase.
- Do not treat Gemma bootstrap findings as stable product truth on `main`.
- Do not change the model line, host assumptions, or evaluation path casually.
- Use the same tracked `bda_eval` review-artifact workflow instead of ad hoc
  side helpers.

## Documentation Discipline

- After meaningful Gemma work, update the relevant living docs unless told not
  to.
- At minimum, consider:
  - `WORKING_CHANGELOG.md`
  - `PROMPT_DEVELOPMENT_METHODOLOGY.md`
  - the Gemma feature lab README
  - the Gemma prompt version log and run manifests
