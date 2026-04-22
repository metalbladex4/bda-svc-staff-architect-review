# Qwen Feature src AGENTS

This subtree contains tracked runtime code inside the active Qwen feature
worktree:

- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- role: active Qwen prompt/config iteration surface

This file is local-only. Keep it out of Git and do not treat it as a tracked
deliverable.

## Startup Sweep For This Subtree

Before substantial code work here, sweep:

- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/AGENTS.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/README.md`
- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/src/bda_svc/pipeline/config.yaml`
- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/src/bda_svc/pipeline/doctrine.yaml`
- `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_QWEN.md`

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
uv run pytest tests/unit/test_yamls.py bda_eval/tests
uv run bda-svc -h
```

## Source-Of-Truth Rules

- Within this worktree, current branch code is the active Qwen feature-branch
  truth.
- For active prompt claims, use the local branch-aware evidence chain and
  winner notes, not legacy labs.
- Stable product truth for the repo still lives on `main` until promotion.

## Runtime-Code Rules

- `config.yaml` here reflects the active Qwen working config and should stay
  aligned with the feature-lab evidence chain.
- If prompt/config wording changes, preserve the version/evidence trail in the
  prompt lab.
- Avoid doctrine changes unless the task actually calls for doctrinal edits.

## Boundaries

- PR `#134` is intentionally being left alone right now; do not auto-pull or
  casually reconcile the remote branch.
- Do not make tracked prompt/config changes here without updating the
  corresponding local prompt-lab docs.
