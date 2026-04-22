
# Staff Architect Brief

This brief explains the **local Codex environment and workflow surfaces that are not
directly visible from the GitHub repo alone**.

## Review Intent

Please review this project as a **Staff AI Systems Architect and Prompt/Evaluation
Lead for a multimodal VLM pipeline**.

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

Current configured MCP servers:

- `sequential-thinking`
- `filesystem`
- `context7`
- `fetch`
- `openaiDeveloperDocs`
- `arxiv`
- `playwright`
- `chrome-devtools`
- `memory`

Intended use:

- prefer source-specific and structured tool use over ad hoc browsing when that
  materially improves planning, inspection, browsing, or docs access
- use `sequential-thinking` heavily for complex planning, debugging, and substantive
  live-doc or AGENTS updates
- use `filesystem` for in-root structured inspection instead of shell-by-habit when
  that is the better fit
- use browser MCPs when browser-state reasoning is actually needed rather than as a
  blanket replacement for simpler tools

### Enabled Plugins / Connectors

Current enabled plugins/connectors:

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

Current global defaults:

- model: `gpt-5.4`
- reasoning effort: `xhigh`
- project trust for `/home/williambenitez1/Capstone`
- MCP-first-but-balanced routing guidance
- explicit `sequential-thinking` escalation before substantive live-doc, global-rule,
  or `AGENTS.md` updates
- local allow-rules present in `~/.codex/rules/default.rules`

## Extensibility Intent Going Forward

We are intentionally open to expanding this setup.

- willing to add more MCP servers where they genuinely improve the workflow
- willing to install or create new skills for recurring prompt/eval/review tasks
- willing to refine AGENTS layering and custom subagent selection
- willing to add better reusable automation if it improves quality without creating
  chaos or hidden state

We want your guidance on which extensibility surfaces are worth adding next and which
ones would create more complexity than value.

## Currently Not Configured Locally

At snapshot time, these surfaces were not detected as actively configured locally:

- no extra profiles or layered config overrides beyond the single `~/.codex/config.toml`
- no custom model providers configured
- no hooks detected
- no team config detected
- no managed enterprise controls visible locally
- no local automations configuration detected

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

This private review repo is a snapshot and review surface only. After it was created,
the active working context was intended to return to `/home/williambenitez1/Capstone`
and its active worktrees. Future pushes here should happen only on explicit request.
