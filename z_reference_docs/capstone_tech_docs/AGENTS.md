# Capstone Tech Docs AGENTS

This subtree is for capstone deliverables, templates, draft artifacts, and the
living notes that connect those documents to the current repo state.

This file is local-only. Keep it out of Git and do not treat it as a tracked
deliverable.

## Startup Sweep For This Subtree

Before substantial writing or document-analysis work here, sweep:

- `/home/williambenitez1/Capstone/z_reference_docs/capstone_tech_docs/understanding_tracking.md`
- `/home/williambenitez1/Capstone/z_reference_docs/WORKING_CHANGELOG.md`
- `/home/williambenitez1/Capstone/z_reference_docs/REFERENCE_MASTER_INDEX.md`
- the relevant phase folder and template under
  `/home/williambenitez1/Capstone/z_reference_docs/capstone_tech_docs/`

If the task is on prompt-related content that intersects with deliverables,
route into:

- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`

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

## Source-Of-Truth Rules

- Trust the current stable implementation on `main` when older deliverables
  drift.
- Use Phase 1, 2, and 3 documents for context, continuity, terminology, and
  rationale, not to override current implementation truth.
- For Phase 4 and later synthesis writing, prefer:
  1. `main`
  2. the active template instructions
  3. the most recent completed deliverables

## Writing Rules

- Write operator-first unless the template clearly demands a more technical
  audience.
- Keep working drafts in markdown when that makes iteration easier, but keep
  the `.docx` submission path in mind.
- Avoid leaking local prompt-lab experimentation into deliverables unless it is
  explicitly being described as future work or internal evidence.
- If a deliverable sentence describes current system behavior, validate it
  against current code on `main`.

## Boundaries

- `z_reference_docs/capstone_tech_docs/` is a local doc workspace, not a
  tracked product API surface.
- Do not treat old slide or template wording as authoritative if the code has
  moved on.
- Do not silently copy stale deployment, model, or schema claims forward.

## Documentation Discipline

- After meaningful work here, update
  `/home/williambenitez1/Capstone/z_reference_docs/capstone_tech_docs/understanding_tracking.md`
  if the understanding changed.
- If the work changes cross-document routing or current project understanding,
  also consider:
  - `/home/williambenitez1/Capstone/z_reference_docs/WORKING_CHANGELOG.md`
  - `/home/williambenitez1/Capstone/z_reference_docs/REFERENCE_MASTER_INDEX.md`
