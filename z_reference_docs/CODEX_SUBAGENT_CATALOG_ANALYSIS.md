# Codex Subagent Catalog Analysis

## Purpose

This note captures a grounded review of the external repository:

- `https://github.com/VoltAgent/awesome-codex-subagents`

The goal is not bulk installation. The goal is:

- to understand what the repository is
- to judge which categories and subagents best fit this Capstone project
- to identify which subagents are broadly useful across projects
- to preserve a reusable local vendor copy and a GitHub fork for future review
- to define a selective-use rule instead of installing everything

## Capstone Grounding Snapshot

This project is currently best understood as:

- a local Python CLI battle damage assessment system
- using Ollama-served vision-language models
- with a strong prompt-engineering and evaluation loop
- producing structured JSON reports
- relying on local evidence trails in `z_reference_docs/`
- using worktrees and branch-aware prompt labs rather than ad hoc prompt edits

That means the best subagents for this repo are the ones that help with:

- prompt and LLM workflow design
- Python runtime and CLI work
- evaluation and regression review
- documentation fidelity
- tooling, build, and deployment support
- research and synthesis

It does not currently need a large bench of:

- frontend/mobile specialists
- app-store or consumer-product specialists
- blockchain/fintech/payment specialists
- WordPress or SEO specialists

## What This Repository Is

From the repository README and local vendored clone:

- it is a curated library of `136` Codex subagent definitions across `10`
  categories
- the subagents are stored as Codex-native `.toml` files
- they are meant to be copied selectively into either:
  - `~/.codex/agents/` for global use
  - `.codex/agents/` for project-local overrides
- the repository itself is a catalog and source library, not an auto-enabled
  runtime
- Codex does not auto-spawn these custom subagents; delegation remains explicit

Current local storage and fork state:

- local vendor clone:
  `/home/williambenitez1/.codex/vendor_imports/github.com/VoltAgent/awesome-codex-subagents`
- upstream remote:
  `https://github.com/VoltAgent/awesome-codex-subagents.git`
- personal fork:
  `https://github.com/metalbladex4/awesome-codex-subagents`

## Current Activation Status

This catalog has now moved from "prepared for later review" to a mixed
vendor-plus-selected-install state.

- the full vendor catalog remains at:
  `/home/williambenitez1/.codex/vendor_imports/github.com/VoltAgent/awesome-codex-subagents`
- the approved global subset is now copied into:
  `/home/williambenitez1/.codex/agents/`
- install provenance and refresh instructions now live at:
  `/home/williambenitez1/.codex/agents/VENDOR_MANIFEST.md`
- the global tool-routing baseline that governs how these specialists should be
  considered now lives in:
  - `/home/williambenitez1/.codex/AGENTS.md`
  - `/home/williambenitez1/.codex/MCP_USAGE_GUIDE.md`
- delegation remains explicit; install availability does not mean auto-use

## Category-By-Category Analysis

The category analysis below covers all subagents in the repository, but groups
them by practical fit instead of pretending all 136 deserve equal attention for
this repo.

### 01. Core Development (`12`)

Overall fit for Capstone: `medium`

- Strong fits:
  `backend-developer`, `code-mapper`
- Situational fits:
  `api-designer`, `fullstack-developer`
- Lower-fit for the current repo shape:
  `electron-pro`, `frontend-developer`, `graphql-architect`,
  `microservices-architect`, `mobile-developer`, `ui-designer`, `ui-fixer`,
  `websocket-engineer`

Read:
- This repo is backend-heavy and CLI-heavy, not browser-heavy.
- `code-mapper` is especially useful because this project has prompt/runtime,
  eval, docs, and worktree surfaces that often need careful ownership tracing
  before edits.

### 02. Language Specialists (`27`)

Overall fit for Capstone: `medium`, but very concentrated around Python

- Strong fits:
  `python-pro`
- Situational fits:
  `sql-pro`, `powershell-7-expert`, `powershell-5.1-expert`,
  `typescript-pro`, `javascript-pro`
- Lower-fit for the current stack:
  `angular-architect`, `cpp-pro`, `csharp-developer`, `django-developer`,
  `dotnet-core-expert`, `dotnet-framework-4.8-expert`, `elixir-expert`,
  `erlang-expert`, `flutter-expert`, `golang-pro`, `java-architect`,
  `kotlin-specialist`, `laravel-specialist`, `nextjs-developer`, `php-pro`,
  `rails-expert`, `react-specialist`, `rust-engineer`,
  `spring-boot-engineer`, `swift-expert`, `vue-expert`

Read:
- `python-pro` is one of the clearest high-value agents in the whole repo for
  this project.
- The PowerShell specialists are only situational, mainly if the work shifts
  toward Windows-specific operator tooling or administrative automation.

### 03. Infrastructure (`16`)

Overall fit for Capstone: `medium-high`

- Strong fits:
  `azure-infra-engineer`, `deployment-engineer`, `devops-engineer`,
  `docker-expert`, `security-engineer`
- Situational fits:
  `cloud-architect`, `database-administrator`, `devops-incident-responder`,
  `incident-responder`, `platform-engineer`, `sre-engineer`
- Lower-fit for the current repo:
  `kubernetes-specialist`, `network-engineer`, `terraform-engineer`,
  `terragrunt-expert`, `windows-infra-admin`

Read:
- `docker-expert` matters because the repo already carries a real container
  surface.
- `azure-infra-engineer` is a better fit here than in many repos because the
  capstone documentation history explicitly touches Azure deployment context.

### 04. Quality & Security (`16`)

Overall fit for Capstone: `high`

- Strong fits:
  `code-reviewer`, `debugger`, `error-detective`, `performance-engineer`,
  `qa-expert`, `reviewer`, `security-auditor`, `test-automator`
- Situational fits:
  `architect-reviewer`, `chaos-engineer`, `compliance-auditor`,
  `penetration-tester`
- Lower-fit for the current repo:
  `accessibility-tester`, `ad-security-reviewer`, `browser-debugger`,
  `powershell-security-hardening`

Read:
- This category is a very strong match because the project is already run as an
  evidence-first engineering workflow.
- `reviewer`, `debugger`, and `test-automator` fit the day-to-day work better
  than most flashy specialty agents.

### 05. Data & AI (`12`)

Overall fit for Capstone: `very high`

- Strong fits:
  `ai-engineer`, `data-analyst`, `data-scientist`, `llm-architect`,
  `mlops-engineer`, `prompt-engineer`
- Situational fits:
  `data-engineer`, `machine-learning-engineer`, `ml-engineer`,
  `nlp-engineer`
- Lower-fit for the current repo:
  `database-optimizer`, `postgres-pro`

Read:
- This is the single most important category for this project.
- `prompt-engineer` is a direct match for the repo's real bottleneck:
  prompt-output contract quality, eval design, and prompt revision discipline.
- `llm-architect` is valuable because this project is not just prompt text; it
  is a multi-stage local VLM workflow with parsing, doctrine, and evaluation.

### 06. Developer Experience (`13`)

Overall fit for Capstone: `high`

- Strong fits:
  `build-engineer`, `cli-developer`, `dependency-manager`,
  `documentation-engineer`, `dx-optimizer`, `git-workflow-manager`,
  `refactoring-specialist`, `tooling-engineer`
- Situational fits:
  `legacy-modernizer`, `mcp-developer`
- Lower-fit for the current repo:
  `powershell-module-architect`, `powershell-ui-architect`, `slack-expert`

Read:
- This repo has a real CLI surface, a real local tooling workflow, and a real
  documentation burden, so this category is more useful than it first looks.
- `documentation-engineer` is particularly well aligned with the project's
  insistence on doc-to-code fidelity.

### 07. Specialized Domains (`12`)

Overall fit for Capstone: `low-medium`

- No clear top-tier fits for the current mainline repo
- Situational fits:
  `api-documenter`, `embedded-systems`, `iot-engineer`, `quant-analyst`,
  `risk-manager`
- Lower-fit for the current repo:
  `blockchain-developer`, `fintech-engineer`, `game-developer`, `m365-admin`,
  `mobile-app-developer`, `payment-integration`, `seo-specialist`

Read:
- There is no defense/BDA-specific agent in this collection, so this category
  is mostly adjacent rather than directly useful.
- `embedded-systems` and `iot-engineer` become more interesting only if the
  project shifts harder toward edge or robotic-platform deployment.

### 08. Business & Product (`11`)

Overall fit for Capstone: `medium`

- Strong fits:
  `business-analyst`, `project-manager`, `technical-writer`
- Situational fits:
  `legal-advisor`, `product-manager`, `scrum-master`, `ux-researcher`
- Lower-fit for the current repo:
  `content-marketer`, `customer-success-manager`, `sales-engineer`,
  `wordpress-master`

Read:
- This category is not core to the runtime, but it is relevant to capstone
  deliverables, user-guide writing, and planning work.
- `technical-writer` is more broadly useful here than `product-manager`.

### 09. Meta & Orchestration (`10` local files + the linked `pied-piper`)

Overall fit for Capstone: `high` as support infrastructure

- Strong fits:
  `agent-installer`, `agent-organizer`, `context-manager`,
  `knowledge-synthesizer`, `multi-agent-coordinator`, `task-distributor`,
  `workflow-orchestrator`
- Situational fits:
  `error-coordinator`, `performance-monitor`
- Lower-fit for the current repo:
  `it-ops-orchestrator`

Read:
- This category matters if we actually start using multiple installed custom
  subagents later.
- `agent-installer` is useful precisely because the current plan is selective
  activation, not bulk installation.

### 10. Research & Analysis (`7`)

Overall fit for Capstone: `very high`

- Strong fits:
  `data-researcher`, `docs-researcher`, `research-analyst`,
  `search-specialist`
- Situational fits:
  `competitive-analyst`, `trend-analyst`
- Lower-fit for the current repo:
  `market-researcher`

Read:
- This repo already works like a research program with runnable evidence, so
  research-oriented agents are a natural fit.
- `docs-researcher` is especially valuable whenever prompting, Ollama, model,
  or dependency behavior needs official verification.

## Best To Have For This Project

If I were choosing a first selective install list for this repo later, these
are the highest-value candidates:

1. `prompt-engineer`
   Best direct fit for prompt revision, output-contract tightening, and
   eval-oriented prompt comparison.
2. `llm-architect`
   Best fit when the issue is bigger than one prompt and involves the whole
   multi-step VLM workflow.
3. `ai-engineer`
   Best fit for code-level fixes in model-backed paths, parsing, orchestration,
   and evaluation hooks.
4. `python-pro`
   Best language specialist for the actual runtime, tests, packaging, and CLI.
5. `reviewer`
   Best general safety net for correctness, regressions, and missing tests.
6. `debugger`
   Best deep root-cause specialist when a prompt/config/runtime regression is
   not yet localized.
7. `code-mapper`
   Best early exploration agent before making changes in a repo with multiple
   runtime and docs surfaces.
8. `cli-developer`
   Best fit for the user-facing `bda-svc` command surface and shell workflow.
9. `documentation-engineer`
   Best fit for keeping user guides, deployment docs, and local instructions
   faithful to the code.
10. `docs-researcher`
    Best fit when version-specific model, API, or tool behavior needs primary
    source verification.
11. `search-specialist`
    Best fit for fast repo-wide and source-wide discovery before deeper work.
12. `test-automator`
    Best fit when a regression needs durable coverage instead of one more
    manual run.
13. `docker-expert`
    Best fit when container packaging or runtime behavior becomes the focus.
14. `devops-engineer`
    Best fit when CI, release automation, or environment wiring becomes the
    bottleneck.
15. `knowledge-synthesizer`
    Best fit when multiple specialist outputs need one clean synthesis.

If you want the tightest practical future shortlist, the first eight I would
reach for are:

- `prompt-engineer`
- `llm-architect`
- `ai-engineer`
- `python-pro`
- `reviewer`
- `code-mapper`
- `documentation-engineer`
- `docs-researcher`

## Best To Have In General Across Projects

These are the most reusable choices from the whole repository for mixed
software work, regardless of stack:

1. `code-mapper`
   Useful almost everywhere because understanding ownership and execution flow
   is the first blocker in most real tasks.
2. `reviewer`
   Strong default review specialist for correctness, regressions, and test
   gaps.
3. `debugger`
   Strong default specialist for deep issue isolation.
4. `docs-researcher`
   Useful whenever framework or API behavior needs official verification.
5. `search-specialist`
   Good front-door agent for narrowing the search space quickly.
6. `research-analyst`
   Good for structured investigations where the answer is not obvious.
7. `test-automator`
   Broadly useful because regression coverage is valuable in almost every code
   base.
8. `documentation-engineer`
   Useful in almost every repo that has operator or developer docs.
9. `dependency-manager`
   Useful across stacks because dependency drift and upgrade risk are universal.
10. `knowledge-synthesizer`
    Useful whenever several other specialists have already produced findings.
11. `multi-agent-coordinator`
    Useful when tasks are complex enough to split safely across multiple roles.
12. `workflow-orchestrator`
    Useful for turning broad requests into a concrete staged execution plan.

General rule:
- after those cross-project agents, add one language specialist that matches
  the repo's real implementation language
- for this repo, that language pick is `python-pro`

## Operating Model We Should Keep

The right operating model for this collection is:

- keep the full repository vendored under `~/.codex/vendor_imports/`
- keep the GitHub fork as a personal mirror and update target
- do not bulk copy the full catalog into `~/.codex/agents/`
- inspect the vendored category files first when a specialist role is needed
- activate only the specific `.toml` files that match the task
- prefer project-local installation only when a project truly needs an override

This avoids turning a good catalog into a noisy global install.

## Practical Update Commands

Refresh the local vendor clone from upstream:

```bash
git -C /home/williambenitez1/.codex/vendor_imports/github.com/VoltAgent/awesome-codex-subagents pull --ff-only origin main
```

Sync the GitHub fork to upstream:

```bash
gh repo sync metalbladex4/awesome-codex-subagents --source VoltAgent/awesome-codex-subagents
```

Inspect candidate subagents before any selective install:

```bash
find /home/williambenitez1/.codex/vendor_imports/github.com/VoltAgent/awesome-codex-subagents/categories -name '*.toml' | sort
```

## Bottom Line

For this Capstone repo, the collection is worth keeping, but mainly as a
vendor catalog and future selective-install source for:

- prompt and LLM workflow specialists
- Python and CLI specialists
- review/debug/test specialists
- documentation and research specialists

The repository is useful. Installing all of it would not be.
