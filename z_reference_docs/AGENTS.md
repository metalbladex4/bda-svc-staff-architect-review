# Local AGENTS Spec For Capstone

This file is the maintained local source of truth for the private AGENTS
system used with this repo. It is a template/spec, not the discovered runtime
file for Codex. Keep `AGENTS_MD_GITHUB_BLOG_LESSONS.md` as the research note;
use this file as the operational reference when creating or revising the root
and worktree `AGENTS.md` files.

## Purpose

The AGENTS layer is for Codex-first local guidance that is specific to this
project and this user's working style. It should:

- add repo-specific workflow rules without duplicating base Codex behavior
- route Codex into the correct living docs quickly
- keep model/worktree distinctions explicit
- preserve local-only boundaries for prompt labs, AGENTS files, and other
  private working materials

All AGENTS files in this project are local-only and must stay out of Git.

## AGENTS Topology

The project uses three layers:

1. this canonical spec/template at
   `/home/williambenitez1/Capstone/z_reference_docs/AGENTS.md`
2. the discovered root file at
   `/home/williambenitez1/Capstone/AGENTS.md`
3. one discovered `AGENTS.md` at the root of each active worktree
4. nested specialist `AGENTS.md` files in high-value subtrees such as
   `z_reference_docs/capstone_tech_docs/`, `z_reference_docs/Prompt_Labs/`,
   and `src/`

Because each worktree is its own Codex discovery root, every active worktree
must have its own self-sufficient `AGENTS.md`. Do not rely on the main
checkout root file being inherited into worktrees.

Nested specialist files should be used to add task-specific guidance under the
nearest applicable subtree. They should supplement, not replace, the root or
worktree-root baseline.

## Shared Baseline Requirements

Every discovered AGENTS file in this project should contain, in roughly this
order:

1. Project or worktree identity
2. Mandatory startup sweep
3. Global tooling overlay
4. Key commands early
5. Source-of-truth rules
6. Worktree and branch rules
7. Documentation discipline
8. Local-only boundaries
9. Lifecycle guidance for future worktrees and model lines

The root file should stay repo-wide. Worktree files should repeat the core
baseline and then add model-line and branch-specific distinctions.
Nested specialist files should stay narrower and task-shaped.

## Mandatory Startup Sweep

Every discovered AGENTS file should require a broad startup sweep before
substantial work. The shared baseline sweep is:

- `/home/williambenitez1/Capstone/z_reference_docs/WORKING_CHANGELOG.md`
  Current state, recent decisions, and next-step context.
- `/home/williambenitez1/Capstone/z_reference_docs/REFERENCE_MASTER_INDEX.md`
  Main router into the rest of `z_reference_docs`.
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
  Running historical method record and experiment lessons.
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`
  Capability-first teaching guide for the active prompt workflow.
- `/home/williambenitez1/Capstone/z_reference_docs/capstone_tech_docs/understanding_tracking.md`
  Phase deliverable understanding and tech-doc context.

Worktree AGENTS files should add the specific lab README, branch metadata, and
model-line references that matter for that branch.

## Required Source-Of-Truth Rules

All discovered AGENTS files should encode these rules:

- Trust the stable implementation on `main` when older documents drift.
- Use older documents for context, rationale, and terminology, not to override
  current implementation truth.
- Treat prompt-lab results and worktree-local experimentation as local
  evidence, not stable product truth, unless explicitly promoted.
- When branch ancestry or sync state matters, inspect current git state; do not
  assume the clean mirror is fully current just because that is its intended
  role.

## Required Workflow Rules

All discovered AGENTS files should encode these rules:

- `main` is intended to remain a clean upstream mirror.
- Real prompt/code iteration happens in model and feature worktrees.
- Model branches are reusable smoke-capable roots, not ancestry-only
  placeholders.
- Rebase/refresh work is not complete until post-refresh parity validation
  passes.
- Do not casually rewrite PR history, reconcile remote divergence, or accept
  VS Code "Pull" prompts on rebased branches without explicit intent.
- When the global `SequentialThinking` MCP server is available, use its
  `sequentialthinking` tool on complex planning, root-cause debugging,
  multi-step tradeoff analysis tasks, and before substantive updates to live
  maintained docs, global rules, or any `AGENTS.md`.

## Required Global Tooling Overlay

All discovered AGENTS files should encode these rules:

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

## Required Documentation Discipline

All discovered AGENTS files should encode these rules:

- After meaningful work, update the relevant living docs unless explicitly told
  not to.
- Use the right living doc for the task instead of dumping everything into one
  file.
- When a new worktree or model line is introduced, update the broader local
  docs so its existence is discoverable.

## Required Local-Only Boundary

All discovered AGENTS files should encode these rules:

- Do not treat local-only docs, prompt-lab materials, AGENTS files, or
  unmerged experiments as GitHub deliverables unless explicitly asked.
- Keep AGENTS infrastructure private and excluded from Git.
- Keep prompt-lab evidence local unless the user explicitly asks to surface it
  elsewhere.

## Root File Template Guidance

The discovered root file at `/home/williambenitez1/Capstone/AGENTS.md` should:

- describe the repo as a local CLI BDA service using Ollama VLMs and structured
  JSON output
- include the shared startup sweep and explain what each living doc is for
- include a compact global-tooling overlay that points to
  `/home/williambenitez1/.codex/AGENTS.md`,
  `/home/williambenitez1/.codex/MCP_USAGE_GUIDE.md`, and the installed-agent
  versus vendor-catalog paths
- include the most important recurring commands near the top
- explain worktree discipline, source-of-truth rules, and local-only boundaries
- explain the lifecycle rule for new worktrees and new model lines

## Worktree File Template Guidance

Each worktree root `AGENTS.md` should be self-sufficient and include:

- worktree identity:
  - branch name
  - model line
  - worktree role
- worktree-specific routing into:
  - the relevant prompt-lab docs under
    `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/...`
  - the relevant prompting/model docs under
    `/home/williambenitez1/Capstone/z_reference_docs/Prompting/...`
  - the relevant update checklist
- the shared global-tooling overlay that points to the current global Codex
  baseline and the installed-agent versus vendor-catalog paths
- model/methodology distinctions:
  - Qwen vs Gemma
  - model root vs feature branch
  - active baseline/winner rules for that line
- key commands for that worktree
- boundaries around promotion, PR history, and what counts as stable truth

## Nested Specialist File Guidance

Nested specialist files should exist where the task context narrows enough that
more specific rules are worth the instruction budget. The current intended
specialist scopes are:

- `/home/williambenitez1/Capstone/z_reference_docs/capstone_tech_docs/AGENTS.md`
  for capstone deliverable synthesis and template-driven writing
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/AGENTS.md`
  for local-only prompt experimentation, evidence preservation, and promotion
  discipline
- `/home/williambenitez1/Capstone/src/AGENTS.md`
  for stable runtime/code conventions in the main checkout

When useful, `src/AGENTS.md` may also be mirrored into active worktrees so code
edits under those worktrees inherit both the worktree root guidance and a
branch-aware code-specific layer.

## Current Active Worktrees

At the moment, distinct discovered `AGENTS.md` files should exist at:

- `/home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct/AGENTS.md`
- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/AGENTS.md`
- `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/AGENTS.md`
- `/home/williambenitez1/Capstone_worktrees/3_model__gemma4-e4b/AGENTS.md`
- `/home/williambenitez1/Capstone_worktrees/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/AGENTS.md`
- `/home/williambenitez1/Capstone_worktrees/3.2_feat__gemma4-e4b__doctrine-bda-alignment/AGENTS.md`

## Lifecycle Rule For New Worktrees And Model Lines

Whenever a new worktree or new model line is introduced:

1. create a new specialized worktree-root `AGENTS.md`
2. build it from this canonical spec
3. tailor it to the branch identity, model line, and relevant methodology
4. update the main checkout root `AGENTS.md` so the new worktree/model is
   acknowledged there too
5. update relevant living docs so the broader local doc system reflects the new
   existence:
   - `WORKING_CHANGELOG.md`
   - `REFERENCE_MASTER_INDEX.md`
   - `PROMPT_LABS_INDEX.md`
   - branch metadata or model-line docs as appropriate

This rule exists so new worktrees do not become isolated side paths with no
shared grounding.

## Key Commands To Prefer In Discovered Files

These should appear near the top of the discovered files when relevant:

```bash
uv sync --all-packages
uv run pytest tests/unit/test_yamls.py bda_eval/tests
uv run bda-svc -h
git status --short --branch
git worktree list
rg --files
```

For refresh and smoke-flow commands, discovered files should route to the
current checklist docs instead of trying to embed every long command block.

## Local Ignore Rule

The local AGENTS layer should be excluded through
`/home/williambenitez1/Capstone/.git/info/exclude`, not through tracked
`.gitignore`.
