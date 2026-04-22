# Gemma Model src AGENTS

This subtree contains tracked runtime code inside the Gemma model worktree:

- branch: `model/gemma4-e4b`
- model line: `gemma4:e4b`
- role: reusable runtime/tooling root for future Gemma feature branches

This file is local-only. Keep it out of Git and do not treat it as a tracked
deliverable.

## Startup Sweep For This Subtree

Before substantial code work here, sweep:

- `/home/williambenitez1/Capstone_worktrees/3_model__gemma4-e4b/AGENTS.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3_model__gemma4-e4b/BRANCH_METADATA.md`
- `/home/williambenitez1/Capstone_worktrees/3_model__gemma4-e4b/src/bda_svc/pipeline/config.yaml`
- `/home/williambenitez1/Capstone_worktrees/3_model__gemma4-e4b/src/bda_svc/pipeline/doctrine.yaml`
- `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_GEMMA.md`

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
uv run bda-svc -h
```

## Source-Of-Truth Rules

- Within this worktree, this branch is the reusable tracked Gemma model-root
  truth.
- Trust current code here over older notes when they drift.
- Treat prompt winner claims as belonging primarily to the Gemma feature lab
  unless they have been intentionally promoted here.

## Runtime-Code Rules

- Keep tracked config aligned with the active Gemma default line:
  `gemma4:e4b`.
- Keep this branch smoke-capable after upstream refreshes.
- Reusable tooling/runtime capability should live here if future Gemma feature
  branches depend on it.
- Local Gemma validation here usually needs
  `OLLAMA_HOST=http://127.0.0.1:11435`.

## Boundaries

- Do not casually redefine the model line by changing the tracked model tag.
- Do not strand reusable infra only in a feature branch if parity here depends
  on it.
