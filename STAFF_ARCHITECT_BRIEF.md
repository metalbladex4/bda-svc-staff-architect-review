
# Staff Architect Brief

This brief explains local Codex environment and workflow surfaces that are not
directly visible from the GitHub repo alone.

For the current 2026-05-06 ChatGPT 5.5 Pro / Deep Research collaboration, read
this first:

```text
z_reference_docs/GPT-Pro_collab/chatgpt_5_5_pro_prompt_engineering_handoff.md
```

That dossier supersedes this brief for the latest Qwen prompt-engineering
state, including `v020c`, `v023/v024`, Graphify/project-brain, Mem0,
SequentialThinking, and the Deep Research handoff request.

## Review Intent

Please review this project as a Staff AI Systems Architect and
Prompt/Evaluation Lead for a multimodal VLM pipeline.

We want recommendations on:

- how to improve the system architecture and workflow overall
- how to improve the prompt engineering workflow
- how to improve Prompt_Labs, iterative refinement, critique/research/revise loops,
  and safe recursive self-improvement
- where agentic tooling or Codex extensibility could materially improve the work

## Hidden Local Codex Environment

### AGENTS Layering

The local workflow uses layered `AGENTS.md` files.

- global Codex rules: `~/.codex/AGENTS.md`
- project root rules: `/home/williambenitez1/Capstone/AGENTS.md`
- additional nested specialist layers inside the project, including branch-root and
  path-specific AGENTS files

Intended use:

- encode durable operating rules
- preserve documentation discipline
- route work into the right local evidence/doc system
- keep future Codex sessions grounded in the real project context

### MCP Inventory And Routing

The current local MCP/tooling stack has evolved since the original review
snapshot. Use the GPT-Pro handoff dossier and the refreshed live docs for the
newest state. High-level current surfaces include:

- `sequential-thinking`
- `filesystem`
- `context7`
- `fetch`
- `openaiDeveloperDocs`
- `arxiv`
- `playwright`
- `chrome-devtools`
- `memory`
- `mem0`
- `mcpfinder`
- `capstone-project-brain`
- `capstone-architecture-graph`
- `capstone-evidence-sqlite`
- `capstone-evidence-duckdb`
- `fiftyone`

Intended use:

- prefer source-specific and structured tool use over ad hoc browsing when that
  materially improves planning, inspection, browsing, or docs access
- use `sequential-thinking` as a compact checkpoint for complex, risky,
  evidence-sensitive, or high-blast-radius decisions
- use `filesystem` for in-root structured inspection instead of shell-by-habit when
  that is the better fit
- use browser MCPs when browser-state reasoning is actually needed rather than as a
  blanket replacement for simpler tools

### Enabled Plugins / Connectors

Current enabled plugins/connectors include:

- GitHub
- Google Drive
- Hugging Face

Intended use:

- let Codex operate directly against the real source systems when GitHub/Drive/HF are
  the actual source of truth for a task

### Installed System Skills

Current system skills:

- `imagegen`
- `openai-docs`
- `plugin-creator`
- `skill-creator`
- `skill-installer`

Intended use:

- package repeatable workflows and reusable procedural knowledge
- expand Codex’s usefulness without relying only on ad hoc instructions

### Installed Global Custom Subagents

Current globally installed subagents:

- `ai-engineer`
- `cli-developer`
- `code-mapper`
- `debugger`
- `dependency-manager`
- `devops-engineer`
- `docker-expert`
- `docs-researcher`
- `documentation-engineer`
- `knowledge-synthesizer`
- `llm-architect`
- `multi-agent-coordinator`
- `prompt-engineer`
- `python-pro`
- `research-analyst`
- `reviewer`
- `search-specialist`
- `test-automator`
- `workflow-orchestrator`

Intended use:

- selectively delegate bounded specialist tasks
- avoid bulk-installing or auto-spawning everything
- treat the vendored catalog as a selectable library, not as a universal default

### Codex Defaults And Rules

Current global defaults and conventions include:

- project trust for `/home/williambenitez1/Capstone`
- MCP-first-but-balanced routing guidance
- explicit `sequential-thinking` escalation before substantive live-doc,
  global-rule, prompt/eval, memory, Graphify, or `AGENTS.md` updates
- Graphify/project-brain is navigation memory, not source truth
- Mem0 is durable advisory memory, not source truth, and writes require
  explicit approval

## Extensibility Intent Going Forward

We are intentionally open to expanding this setup.

- willing to add more MCP servers where they genuinely improve the workflow
- willing to install or create new skills for recurring prompt/eval/review tasks
- willing to refine AGENTS layering and custom subagent selection
- willing to add better reusable automation if it improves quality without creating
  chaos or hidden state

We want your guidance on which extensibility surfaces are worth adding next and which
ones would create more complexity than value.

## Other Potential Surfaces We Want Advice On

Even where they are not currently configured here, we want recommendations on whether
we should use or avoid:

- Codex SDK / programmatic orchestration
- `codex exec` style scripted workflows
- GitHub Action based review/eval automation
- app-server style integrations
- hook-based policy or validation surfaces
- custom provider routing only if it would materially improve the workflow

## Important Boundary

This review repo is a snapshot and review surface only. After it is refreshed,
the active working context returns to `/home/williambenitez1/Capstone` and its
active worktrees. Future pushes here should happen only on explicit request.

GitHub currently reports this repo as `PUBLIC`, so treat it as sanitized review
material and do not add raw secrets, credentials, local auth/session state, or
unreviewed private machine files.
