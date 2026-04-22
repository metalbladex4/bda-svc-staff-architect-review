# Main Checkout src AGENTS

This subtree contains the tracked runtime code for the stable `main` checkout.
Use this file when working under `src/` in the main checkout.

This file is local-only. Keep it out of Git and do not treat it as a tracked
deliverable.

## Startup Sweep For This Subtree

Before substantial code work here, sweep:

- `/home/williambenitez1/Capstone/README.md`
- `/home/williambenitez1/Capstone/z_reference_docs/WORKING_CHANGELOG.md`
- `/home/williambenitez1/Capstone/z_reference_docs/REFERENCE_MASTER_INDEX.md`
- `/home/williambenitez1/Capstone/src/bda_svc/pipeline/config.yaml`
- `/home/williambenitez1/Capstone/src/bda_svc/pipeline/doctrine.yaml`

Route next as needed:

- worktree/update rules:
  `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_WORKFLOW.md`
- capstone deliverable context:
  `/home/williambenitez1/Capstone/z_reference_docs/capstone_tech_docs/understanding_tracking.md`
- prompt-method context:
  `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`

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
rg -n "<pattern>" src tests bda_eval
uv sync --all-packages
uv run pytest tests/unit/test_yamls.py bda_eval/tests
uv run bda-svc -h
```

## Source-Of-Truth Rules

- Under this subtree, the code on `main` is the runtime truth.
- If older docs drift from code, trust code.
- CLI, input handling, export behavior, config, and doctrine together define
  most user-visible behavior.

## Runtime-Code Rules

- Treat `src/bda_svc/cli.py`, `app.py`, `inputs.py`, and `export.py` as
  user-facing behavior surfaces.
- Treat `src/bda_svc/pipeline/config.yaml` and `doctrine.yaml` as
  contract-sensitive files. Change them deliberately, not casually.
- If a change affects prompt/config behavior, think through whether it belongs
  on `main` at all or whether it should first live as worktree-local evidence.
- Keep stable runtime code distinct from local-only prompt-lab materials.

## Boundaries

- Do not pull local-only AGENTS or prompt-lab infrastructure into tracked code
  changes.
- Do not treat branch-local experiments as if they already define `main`.
- Avoid doctrine or config changes unless the task actually requires them.

## Validation Rule

- After meaningful code work here, run the appropriate validation slice.
- At minimum, consider:
  - `uv run pytest tests/unit/test_yamls.py bda_eval/tests`
  - `uv run bda-svc -h`

## Documentation Discipline

- After meaningful runtime-code work, update the relevant living docs unless
  told not to.
- At minimum, consider whether the change affects:
  - `WORKING_CHANGELOG.md`
  - `REFERENCE_MASTER_INDEX.md`
  - capstone deliverable drafts that describe current behavior
