# Gemma Feature src AGENTS

This subtree contains tracked runtime code inside the active Gemma feature
worktree:

- branch: `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- model line: `gemma4:e4b`
- role: active Gemma bootstrap prompt/config surface

This file is local-only. Keep it out of Git and do not treat it as a tracked
deliverable.

## Startup Sweep For This Subtree

Before substantial code work here, sweep:

- `/home/williambenitez1/Capstone_worktrees/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/AGENTS.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/README.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/operational_prompt_rules.md`
- `/home/williambenitez1/Capstone_worktrees/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/src/bda_svc/pipeline/config.yaml`
- `/home/williambenitez1/Capstone_worktrees/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/src/bda_svc/pipeline/doctrine.yaml`

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
rg --files src
uv sync --all-packages
env OLLAMA_HOST=http://127.0.0.1:11435 uv run pytest tests/unit/test_yamls.py bda_eval/tests
env OLLAMA_HOST=http://127.0.0.1:11435 uv run bda-svc -h
```

## Source-Of-Truth Rules

- Within this worktree, current branch code is the active Gemma bootstrap
  truth.
- For active Gemma prompt claims, use the local evidence chain and run notes.
- Stable repo truth still lives on `main` until promotion.

## Runtime-Code Rules

- `config.yaml` here is the semantic port of the active Qwen `v009` stack into
  the Gemma line.
- Keep `gemma4:e4b` as the active model and `thinking` disabled unless there is
  an explicit decision to open a new behavior.
- Local Gemma validation here usually needs
  `OLLAMA_HOST=http://127.0.0.1:11435`.
- If prompt/config wording changes here, preserve the version/evidence trail in
  the Gemma prompt lab.

## Boundaries

- Do not move into Gemma `v001` or later iterations unless the user explicitly
  asks.
- Do not treat Gemma bootstrap findings as stable product truth on `main`.
