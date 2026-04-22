# Qwen Model Worktree AGENTS

This worktree is the long-lived Qwen model root:

- branch: `model/qwen3-vl-8b-instruct`
- model line: `qwen3-vl:8b-instruct`
- role: reusable smoke-capable root for future Qwen feature branches

This file is local-only. Keep it out of Git and do not treat it as a tracked
deliverable.

## Mandatory Startup Sweep

Before substantial work in this worktree, sweep:

- `/home/williambenitez1/Capstone/z_reference_docs/WORKING_CHANGELOG.md`
- `/home/williambenitez1/Capstone/z_reference_docs/REFERENCE_MASTER_INDEX.md`
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1_model__qwen3-vl-8b-instruct/BRANCH_METADATA.md`
- `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_QWEN.md`

If the task moves into active prompt evidence or winner state, route next to:

- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/README.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/PROMPT_LABS_INDEX.md`

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
uv run pytest tests/unit/test_yamls.py bda_eval/tests
uv run bda-svc -h
```

When the global `SequentialThinking` MCP server is available, use its
`sequentialthinking` tool on complex planning, root-cause debugging, and
multi-step tradeoff analysis tasks.

For upstream refresh work or smoke parity, follow:

- `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_QWEN.md`

## Source-Of-Truth Rules

- Trust the stable implementation on `main` if older documents drift.
- Treat this branch as tracked runtime/tooling truth for the Qwen model root.
- Treat prompt-lab winner claims and run-by-run prompt conclusions as belonging
  primarily to the feature lab, not to this model root by default.

## Model-Line And Branch Rules

- This branch is a reusable parent for future Qwen feature branches.
- It should stay prompt-lab smoke-capable after upstream refreshes.
- It already carries reusable review-artifact and workspace-sync capability
  that should not be stranded back in a feature branch.
- If a reusable capability exists only in a feature branch and is needed for
  parity here, promote it upward before calling the refresh cycle complete.

## Boundaries

- Do not treat this model root as the active winner-evidence surface.
- Do not open or revise prompt winners here unless the work is intentionally
  being promoted into the reusable model root.
- Do not casually rewrite the remote branch or accept automatic pull prompts on
  rebased branches without explicit intent.

## Documentation Discipline

- After meaningful work here, update the relevant living docs unless told not
  to.
- At minimum, consider whether changes affect:
  - `WORKING_CHANGELOG.md`
  - `REFERENCE_MASTER_INDEX.md`
  - the Qwen branch metadata file
  - the Qwen prompt-lab index/README routing
