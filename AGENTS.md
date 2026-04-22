# Capstone AGENTS

This repo is a research-focused, local CLI battle damage assessment system that
uses Ollama-served VLMs to analyze imagery and emit structured JSON reports.

This file is Codex-first and local-only. It adds project-specific guidance on
top of the base Codex behavior. Keep it private and do not push it to GitHub.
When a nearer worktree-root or nested specialist `AGENTS.md` exists under the
current path, treat that nearer file as additive and more specific guidance.

## Mandatory Startup Sweep

Before substantial work, sweep these files in this order and use them to route
into the rest of the local docs:

- `/home/williambenitez1/Capstone/z_reference_docs/WORKING_CHANGELOG.md`
  Current project state, recent changes, and what we were doing most recently.
- `/home/williambenitez1/Capstone/z_reference_docs/REFERENCE_MASTER_INDEX.md`
  Main routing document for the rest of `z_reference_docs`.
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
  Historical method record, major experiment lessons, and prompt workflow
  decisions.
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`
  Capability-first teaching guide for how prompt work is done in this project.
- `/home/williambenitez1/Capstone/z_reference_docs/capstone_tech_docs/understanding_tracking.md`
  Phase deliverable context and document-understanding notes.

If the task is more specific, route from there:

- prompt/model evidence:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/PROMPT_LABS_INDEX.md`
- prompting/model references:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompting/PROMPTING_MASTER_INDEX.md`
- safe upstream refresh work:
  `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_WORKFLOW.md`
- copy-paste refresh commands:
  `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_QWEN.md`
  and
  `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_GEMMA.md`

Specialist nested AGENTS layers also exist for:

- `/home/williambenitez1/Capstone/z_reference_docs/capstone_tech_docs/`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/`
- `/home/williambenitez1/Capstone/src/`

When working inside those paths, open the nearer specialist file too.

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

Use these early and often:

```bash
git status --short --branch
git worktree list
rg --files
rg -n "<pattern>" z_reference_docs src tests bda_eval
uv sync --all-packages
uv run pytest tests/unit/test_yamls.py bda_eval/tests
uv run bda-svc -h
```

When the task is about upstream refreshes or smoke parity, prefer the checklist
docs over retyping long command sequences from memory.

## Source-Of-Truth Rules

- Trust the stable implementation on `main` when older documents drift.
- Use older Phase 1/2/3 docs and older prompt notes for context, rationale, and
  continuity, not to override current repo truth.
- Treat prompt-lab work, worktree-only experiments, and local evaluation
  artifacts as local evidence unless explicitly promoted into tracked runtime
  code/config.
- When branch ancestry or sync state matters, inspect current git state. `main`
  is intended to be a clean upstream mirror, but do not assume it is already
  fully synced.

## Worktree Rules

- `main` is the clean mirror and general reference checkout.
- Real model-line work happens in model and feature worktrees.
- Model branches are reusable smoke-capable roots, not ancestry-only
  placeholders.
- Rebase/refresh work is not complete until the documented post-refresh parity
  validation passes.
- Do not casually reconcile remote divergence or rewrite PR history.
- If VS Code or GitHub tooling offers to "Pull" a rebased PR branch, stop and
  inspect first. Do not auto-pull just because the UI offers it.

Active worktree roots currently include:

- `/home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct`
- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`
- `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment`
- `/home/williambenitez1/Capstone_worktrees/3_model__gemma4-e4b`
- `/home/williambenitez1/Capstone_worktrees/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap`
- `/home/williambenitez1/Capstone_worktrees/3.2_feat__gemma4-e4b__doctrine-bda-alignment`

Each active worktree must have its own distinct root `AGENTS.md`. When working
from a worktree root, that file is the nearest project instruction layer and
should be treated as primary for that branch.

For code work, a nearer `src/AGENTS.md` may exist inside the current checkout
or worktree. Use it as the code-specific layer on top of the root file.

## Documentation Discipline

- After meaningful work, update the relevant living docs unless explicitly told
  not to.
- Use the right living doc for the task:
  - `WORKING_CHANGELOG.md` for current state and recent decisions
  - `REFERENCE_MASTER_INDEX.md` for routing
  - `PROMPT_DEVELOPMENT_METHODOLOGY.md` for method history and lessons
  - prompt-lab READMEs and branch metadata for branch-specific state
  - `understanding_tracking.md` for capstone deliverable understanding
- Prefer explicit cross-links and purpose-based routing over isolated notes.

## Local-Only Boundary

- Do not treat `z_reference_docs`, prompt-lab materials, AGENTS files, or other
  local-only evidence as tracked GitHub deliverables unless explicitly asked.
- Do not push AGENTS files or any local AGENTS-support infrastructure.
- Keep prompt-lab evidence separate from stable product claims unless the user
  explicitly asks to surface or promote it.

## Collaboration Preferences

- Plan before major structural changes.
- When the global `SequentialThinking` MCP server is available, use its
  `sequentialthinking` tool on complex planning, root-cause debugging, and
  multi-step tradeoff analysis tasks.
- Prefer explicit reasoning over silent assumptions.
- When a decision has non-obvious consequences, pause and surface the tradeoffs
  before committing.
- Preserve evidence trails and route into the local docs instead of making the
  next person reconstruct context from scratch.

## Lifecycle Rule For New Worktrees And Model Lines

Whenever a new worktree or new model line is introduced:

1. create a new specialized worktree-root `AGENTS.md`
2. build it from the canonical spec at
   `/home/williambenitez1/Capstone/z_reference_docs/AGENTS.md`
3. tailor it to the new branch identity, model line, and methodology
4. update this root file so the new worktree/model is acknowledged here too
5. update the broader local doc system so the new existence is discoverable:
   - `WORKING_CHANGELOG.md`
   - `REFERENCE_MASTER_INDEX.md`
   - `PROMPT_LABS_INDEX.md`
   - relevant branch metadata or model-line docs

This prevents new worktrees from becoming hidden side paths with no shared
grounding.
