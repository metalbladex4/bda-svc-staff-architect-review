# Qwen Feature Worktree AGENTS

This worktree is the active Qwen branch-aware prompt lab:

- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- role: active prompt iteration line and current Qwen evidence surface

This file is local-only. Keep it out of Git and do not treat it as a tracked
deliverable.

## Mandatory Startup Sweep

Before substantial work in this worktree, sweep:

- `/home/williambenitez1/Capstone/z_reference_docs/WORKING_CHANGELOG.md`
- `/home/williambenitez1/Capstone/z_reference_docs/REFERENCE_MASTER_INDEX.md`
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/README.md`
- `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_QWEN.md`

Route into these next when relevant:

- winners and active stack:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/winners/`
- experiment index:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/PROMPT_LABS_INDEX.md`
- Qwen prompting/model references:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompting/PROMPTING_MASTER_INDEX.md`

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

Use the Qwen checklist for refresh and smoke-flow command blocks:

- `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_QWEN.md`

## Source-Of-Truth Rules

- Trust stable `main` if older docs drift on product/runtime behavior.
- For active Qwen prompt claims, trust the current branch-aware evidence chain
  in this feature lab over preserved legacy labs.
- Treat prompt-lab evidence as local evidence first; only treat it as tracked
  product truth after explicit promotion.

## Model-Line And Methodology Rules

- This is the active Qwen prompt-iteration branch.
- `v009` is the active working config for this Qwen line.
- The feature lab README is the main branch-specific routing doc for current
  winner status, grounding lessons, validation packs, and smoke readiness.
- Use the branch-aware Qwen line under
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/`
  as the current evidence chain.
- Treat the legacy lab under
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/2.main__qwen3-vl-8b-instruct/`
  as preserved history, not the active line.

## PR And Remote Boundary

- This branch currently diverges from
  `origin/feat/qwen3-vl-8b-instruct/two-pass-refinement` after local rebases.
- PR `#134` is being left alone intentionally as the current remote review
  surface.
- Do not accept automatic UI "Pull" prompts on this branch.
- Do not reconcile the remote branch unless the user explicitly chooses a
  deliberate path such as `git push --force-with-lease`.

## Boundaries

- Do not treat every good seed-case result as promotable; use the mixed packs
  and branch-aware evidence chain.
- Do not promote new winners without preserving version snapshots and updating
  the relevant local docs.
- Do not confuse local prompt-lab evidence with tracked repo truth on `main`.

## Documentation Discipline

- After meaningful prompt work, update the relevant living docs unless told not
  to.
- At minimum, consider:
  - `WORKING_CHANGELOG.md`
  - `PROMPT_DEVELOPMENT_METHODOLOGY.md`
  - the Qwen feature lab README
  - winner notes and version logs
