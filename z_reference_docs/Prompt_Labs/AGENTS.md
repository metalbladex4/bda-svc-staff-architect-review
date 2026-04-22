# Prompt Labs AGENTS

This subtree is the local-only prompt experimentation workspace. It contains
branch-structured labs, version snapshots, run artifacts, validation packs,
winner notes, and supporting evidence for prompt decisions before anything is
promoted into tracked runtime config.

This file is local-only. Keep it out of Git and do not treat it as a tracked
deliverable.

## Startup Sweep For This Subtree

Before substantial prompt-lab work here, sweep:

- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/PROMPT_LABS_INDEX.md`
- `/home/williambenitez1/Capstone/z_reference_docs/WORKING_CHANGELOG.md`
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`
- the branch-specific lab README or branch metadata file relevant to the line
  you are touching

Route into these when needed:

- prompting/model references:
  `/home/williambenitez1/Capstone/z_reference_docs/Prompting/PROMPTING_MASTER_INDEX.md`
- worktree refresh rules:
  `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_WORKFLOW.md`
- Qwen or Gemma refresh checklists:
  `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_QWEN.md`
  and
  `/home/williambenitez1/Capstone/z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_GEMMA.md`

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

- Prompt labs are local evidence first, not stable product truth.
- Trust `main` for current runtime behavior when prompt-lab notes drift from
  tracked code.
- Trust the active branch-specific evidence chain over preserved legacy labs
  when evaluating the current model line.

## Experiment Rules

- Preserve the evidence chain. Do not overwrite old run folders or recycle old
  run timestamps.
- Keep baseline, candidate, and repeat-run structure legible.
- Use run manifests, version logs, and winner notes so later promotion
  decisions stay auditable.
- Treat `tests/data/tank.jpg` as a pressure test, not the only validation case.
- Do not promote a winner from a narrow seed-case improvement alone when the
  relevant mixed validation pack says otherwise.

## Promotion Rules

- Prompt changes should prove themselves here before moving into tracked
  runtime config.
- Promotion should preserve:
  - version snapshots
  - run artifacts
  - summary notes explaining why the change won
- Reusable infrastructure that becomes necessary for parity should not remain
  trapped in a feature branch.

## Boundaries

- Do not confuse prompt-lab winners with GitHub-reviewed tracked truth.
- Do not surface local-only prompt-lab artifacts outside local docs unless the
  user explicitly asks.
- Keep legacy and archive labs clearly distinct from the current active line.

## Documentation Discipline

- After meaningful prompt-lab work, update the relevant local docs unless told
  not to.
- At minimum, consider:
  - the branch-specific lab README
  - `PROMPT_DEVELOPMENT_METHODOLOGY.md`
  - `WORKING_CHANGELOG.md`
  - winner notes, version logs, and run manifests
