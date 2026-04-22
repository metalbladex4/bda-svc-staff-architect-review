# AGENTS.md Multi-Source Lessons And Reference Notes

## MediaLab Working Note
- This file is a working reference for designing local instruction behavior, not a license to mirror third-party articles wholesale.
- For external source-capture tasks in this workspace, the preferred handling is:
  - preserve source order and section structure when possible
  - ask before downgrading a requested capture into a loose summary if fidelity is unclear
  - if full verbatim third-party reproduction is blocked by policy, licensing uncertainty, or another higher-priority constraint, say so immediately
  - when blocked, offer the user a manual fallback path so they can paste or save the source themselves
- This note exists because source-capture fidelity and instruction-file design are now both active workflow concerns in `K:\MediaLab`.

## Top Index

### Document 1. GitHub Blog
- Source details
- Why this matters here
- Core thesis
- Main lessons
- Example pattern the article recommends
- Useful agent types mentioned
- Practical translation for MediaLab
- Draft rules worth carrying forward
- Suggested MediaLab follow-up
- Short takeaway

### Document 2. skyzyx Gist Raw README
- Source details
- Core thesis
- What AGENTS.md is
- Why large AGENTS.md files fail
- Minimal root contents
- Progressive disclosure model
- Monorepo guidance
- Refactor prompt pattern
- Practical translation for MediaLab
- Short takeaway

### Document 3. OpenAI Codex Guide
- Source details
- Core thesis
- What this guide adds beyond the other sources
- Codex instruction discovery model
- Global and project layering
- Fallback filenames and size controls
- Verification and troubleshooting patterns
- Practical translation for MediaLab
- Short takeaway

## Document 1. GitHub Blog

### Source
- Title: `How to write a great agents.md: Lessons from over 2,500 repositories`
- Source URL: `https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/`
- Publisher: GitHub Blog
- Author: Matt Nigh
- Published: November 19, 2025
- Updated: November 25, 2025
- Captured: April 19, 2026
- 
How to write a great agents.md: Lessons from over 2,500 repositories
Learn how to write effective agents.md files for GitHub Copilot with practical tips, real examples, and templates from analyzing 2,500+ repositories.


Matt Nigh·@mattnigh
November 19, 2025
|
Updated November 25, 2025
|
5 minutes
We recently released a new GitHub Copilot feature: custom agents defined in agents.md files. Instead of one general assistant, you can now build a team of specialists: a @docs-agent for technical writing, a @test-agent for quality assurance, and a @security-agent for security analysis. Each agents.md file acts as an agent persona, which you define with frontmatter and custom instructions.

agents.md is where you define all the specifics: the agent’s persona, the exact tech stack it should know, the project’s file structure, workflows, and the explicit commands it can run. It’s also where you provide code style examples and, most importantly, set clear boundaries of what not to do.

The challenge? Most agent files fail because they’re too vague. “You are a helpful coding assistant” doesn’t work. “You are a test engineer who writes tests for React components, follows these examples, and never modifies source code” does.

I analyzed over 2,500 agents.md files across public repos to understand how developers were using agents.md files. The analysis showed a clear pattern of what works: provide your agent a specific job or persona, exact commands to run, well-defined boundaries to follow, and clear examples of good output for the agent to follow. 

Here’s what the successful ones do differently.

What works in practice: Lessons from 2,500+ repos
My analysis of over 2,500 agents.md files revealed a clear divide between the ones that fail and the ones that work. The successful agents aren’t just vague helpers; they are specialists. Here’s what the best-performing files do differently:

Put commands early: Put relevant executable commands in an early section: npm test, npm run build, pytest -v. Include flags and options, not just tool names. Your agent will reference these often.
Code examples over explanations: One real code snippet showing your style beats three paragraphs describing it. Show what good output looks like.
Set clear boundaries: Tell AI what it should never touch (e.g., secrets, vendor directories, production configs, or specific folders). “Never commit secrets” was the most common helpful constraint.
Be specific about your stack: Say “React 18 with TypeScript, Vite, and Tailwind CSS” not “React project.” Include versions and key dependencies.
Cover six core areas: Hitting these areas puts you in the top tier: commands, testing, project structure, code style, git workflow, and boundaries. 
Example of a great agent.md file
Below is an example for adding a documentation agent.md persona in your repo to .github/agents/docs-agent.md:

---
name: docs_agent
description: Expert technical writer for this project
---

You are an expert technical writer for this project.

## Your role
- You are fluent in Markdown and can read TypeScript code
- You write for a developer audience, focusing on clarity and practical examples
- Your task: read code from `src/` and generate or update documentation in `docs/`

## Project knowledge
- **Tech Stack:** React 18, TypeScript, Vite, Tailwind CSS
- **File Structure:**
  - `src/` – Application source code (you READ from here)
  - `docs/` – All documentation (you WRITE to here)
  - `tests/` – Unit, Integration, and Playwright tests

## Commands you can use
Build docs: `npm run docs:build` (checks for broken links)
Lint markdown: `npx markdownlint docs/` (validates your work)

## Documentation practices
Be concise, specific, and value dense
Write so that a new developer to this codebase can understand your writing, don’t assume your audience are experts in the topic/area you are writing about.

## Boundaries
- ✅ **Always do:** Write new files to `docs/`, follow the style examples, run markdownlint
- ⚠️ **Ask first:** Before modifying existing documents in a major way
- 🚫 **Never do:** Modify code in `src/`, edit config files, commit secrets
Why this agent.md file works well
States a clear role: Defines who the agent is (expert technical writer), what skills it has (Markdown, TypeScript), and what it does (read code, write docs).
Executable commands: Gives AI tools it can run (npm run docs:build and npx markdownlint docs/). Commands come first.
Project knowledge: Specifies tech stack with versions (React 18, TypeScript, Vite, Tailwind CSS) and exact file locations.
Real examples: Shows what good output looks like with actual code. No abstract descriptions.
Three-tier boundaries: Set clear rules using always do, ask first, never do. Prevents destructive mistakes.
How to build your first agent
Pick one simple task. Don’t build a “general helper.” Pick something specific like:

Writing function documentation
Adding unit tests
Fixing linting errors
Start minimal—you only need three things:

Agent name: test-agent, docs-agent, lint-agent
Description: “Writes unit tests for TypeScript functions”
Persona: “You are a quality software engineer who writes comprehensive tests”
Copilot can also help generate one for you. Using your preferred IDE, open a new file at .github/agents/test-agent.md and use this prompt:

Create a test agent for this repository. It should:
- Have the persona of a QA software engineer.
- Write tests for this codebase
- Run tests and analyzes results
- Write to “/tests/” directory only
- Never modify source code or remove failing tests
- Include specific examples of good test structure
Copilot will generate a complete agent.md file with persona, commands, and boundaries based on your codebase. Review it, add in YAML frontmatter, adjust the commands for your project, and you’re ready to use @test-agent.

Six agents worth building
Consider asking Copilot to help generate agent.md files for the below agents. I’ve included examples with each of the agents, which should be changed to match the reality of your project. 

@docs-agent
One of your early agents should write documentation. It reads your code and generates API docs, function references, and tutorials. Give it commands like npm run docs:build and markdownlint docs/ so it can validate its own work. Tell it to write to docs/ and never touch src/. 

What it does: Turns code comments and function signatures into Markdown documentation  
Example commands: npm run docs:build, markdownlint docs/
Example boundaries: Write to docs/, never modify source code
@test-agent
This one writes tests. Point it at your test framework (Jest, PyTest, Playwright) and give it the command to run tests. The boundary here is critical: it can write to tests but should never remove a test because it is failing and cannot be fixed by the agent. 

What it does: Writes unit tests, integration tests, and edge case coverage  
Example commands: npm test, pytest -v, cargo test --coverage  
Example boundaries: Write to tests/, never remove failing tests unless authorized by user
@lint-agent
A fairly safe agent to create early on. It fixes code style and formatting but shouldn’t change logic. Give it commands that let it auto-fix style issues. This one’s low-risk because linters are designed to be safe.

What it does: Formats code, fixes import order, enforces naming conventions  
Example commands: npm run lint --fix, prettier --write
Example boundaries: Only fix style, never change code logic
@api-agent
This agent builds API endpoints. It needs to know your framework (Express, FastAPI, Rails) and where routes live. Give it commands to start the dev server and test endpoints. The key boundary: it can modify API routes but must ask before touching database schemas.

What it does: Creates REST endpoints, GraphQL resolvers, error handlers  
Example commands: npm run dev, curl localhost:3000/api, pytest tests/api/
Example boundaries: Modify routes, ask before schema changes
@dev-deploy-agent
Handles builds and deployments to your local dev environment. Keep it locked down: only deploy to dev environments and require explicit approval. Give it build commands and deployment tools but make the boundaries very clear.

What it does: Runs local or dev builds, creates Docker images  
Example commands: npm run test
Example boundaries: Only deploy to dev, require user approval for anything with risk
Starter template
---
name: your-agent-name
description: [One-sentence description of what this agent does]
---

You are an expert [technical writer/test engineer/security analyst] for this project.

## Persona
- You specialize in [writing documentation/creating tests/analyzing logs/building APIs]
- You understand [the codebase/test patterns/security risks] and translate that into [clear docs/comprehensive tests/actionable insights]
- Your output: [API documentation/unit tests/security reports] that [developers can understand/catch bugs early/prevent incidents]

## Project knowledge
- **Tech Stack:** [your technologies with versions]
- **File Structure:**
  - `src/` – [what's here]
  - `tests/` – [what's here]

## Tools you can use
- **Build:** `npm run build` (compiles TypeScript, outputs to dist/)
- **Test:** `npm test` (runs Jest, must pass before commits)
- **Lint:** `npm run lint --fix` (auto-fixes ESLint errors)

## Standards

Follow these rules for all code you write:

**Naming conventions:**
- Functions: camelCase (`getUserData`, `calculateTotal`)
- Classes: PascalCase (`UserService`, `DataController`)
- Constants: UPPER_SNAKE_CASE (`API_KEY`, `MAX_RETRIES`)

**Code style example:**
```typescript
// ✅ Good - descriptive names, proper error handling
async function fetchUserById(id: string): Promise<User> {
  if (!id) throw new Error('User ID required');
  
  const response = await api.get(`/users/${id}`);
  return response.data;
}

// ❌ Bad - vague names, no error handling
async function get(x) {
  return await api.get('/users/' + x).data;
}
Boundaries
- ✅ **Always:** Write to `src/` and `tests/`, run tests before commits, follow naming conventions
- ⚠️ **Ask first:** Database schema changes, adding dependencies, modifying CI/CD config
- 🚫 **Never:** Commit secrets or API keys, edit `node_modules/` or `vendor/`
Key takeaways
Building an effective custom agent isn’t about writing a vague prompt; it’s about providing a specific persona and clear instructions.

My analysis of over 2,500 agents.md files shows that the best agents are given a clear persona and, most importantly, a detailed operating manual. This manual must include executable commands, concrete code examples for styling, explicit boundaries (like files to never touch), and specifics about your tech stack. 

When creating your own agents.md cover the six core areas: Commands, testing, project structure, code style, git workflow, and boundaries. Start simple. Test it. Add detail when your agent makes mistakes. The best agent files grow through iteration, not upfront planning.

Now go forth and build your own custom agents to see how they level up your workflow first-hand!



## Document 2. skyzyx Gist Raw README

### Source
- Title: `A Complete Guide To AGENTS.md`
- Source URL: `https://gist.githubusercontent.com/skyzyx/c91d9be9e5050c85e81ccbcca022ff6b/raw/f81bcdaec7665a76b5d26b1d8d296eab76606d3d/README.md`
- Source host: GitHub Gist raw content
- Captured: April 19, 2026
- Attribution note: The raw file itself does not expose a visible publication date or byline in the captured text.

#### A Complete Guide To AGENTS.md

Have you ever felt concerned about the size of your `AGENTS.md` file?

Maybe you should be. A bad `AGENTS.md` file can confuse your agent, become a maintenance nightmare, and cost you tokens on every request.

So you'd better know how to fix it.

## What is AGENTS.md?

An `AGENTS.md` file is a markdown file you check into Git that customizes how AI coding agents behave in your repository. It sits at the top of the conversation history, right below the system prompt.

Think of it as a configuration layer between the agent's base instructions and your actual codebase. The file can contain two types of guidance:

- **Personal scope**: Your commit style preferences, coding patterns you prefer
- **Project scope**: What the project does, which package manager you use, your architecture decisions

The `AGENTS.md` file is an open standard supported by many - though not all - tools.

<details>
  <summary>CLAUDE.md</summary>

Notably, Claude Code doesn't use `AGENTS.md` - it uses `CLAUDE.md` instead. You can symlink between them to keep all your tools working the same way:

```bash
# Create a symlink from AGENTS.md to CLAUDE.md
ln -s AGENTS.md CLAUDE.md
```

</details>

## Why Massive `AGENTS.md` Files are a Problem

There's a natural feedback loop that causes `AGENTS.md` files to grow dangerously large:

1. The agent does something you don't like
2. You add a rule to prevent it
3. Repeat hundreds of times over months
4. File becomes a "ball of mud"

Different developers add conflicting opinions. Nobody does a full style pass. The result? An unmaintainable mess that actually hurts agent performance.

Another culprit: auto-generated `AGENTS.md` files. Never use initialization scripts to auto-generate your `AGENTS.md`. They flood the file with things that are "useful for most scenarios" but would be better progressively disclosed. Generated files prioritize comprehensiveness over restraint.

### The Instruction Budget

Kyle from Humanlayer's [article](https://www.humanlayer.dev/blog/writing-a-good-claude-md) mentions the concept of an "instruction budget":

> Frontier thinking LLMs can follow ~ 150-200 instructions with reasonable consistency. Smaller models can attend to fewer instructions than larger models, and non-thinking models can attend to fewer instructions than thinking models.

Every token in your `AGENTS.md` file gets loaded on **every single request**, regardless of whether it's relevant. This creates a hard budget problem:

| Scenario                   | Impact                                                |
| -------------------------- | ----------------------------------------------------- |
| Small, focused `AGENTS.md` | More tokens available for task-specific instructions  |
| Large, bloated `AGENTS.md` | Fewer tokens for the actual work; agent gets confused |
| Irrelevant instructions    | Token waste + agent distraction = worse performance   |

Taken together, this means that **the ideal `AGENTS.md` file should be as small as possible.**

### Stale Documentation Poisons Context

Another issue for large `AGENTS.md` files is staleness.

Documentation goes out of date quickly. For human developers, stale docs are annoying, but the human usually has enough built-in memory to be skeptical about bad docs. For AI agents that read documentation on every request, stale information actively _poisons_ the context.

This is especially dangerous when you document file system structure. File paths change constantly. If your `AGENTS.md` says "authentication logic lives in `src/auth/handlers.ts`" and that file gets renamed or moved, the agent will confidently look in the wrong place.

Instead of documenting structure, describe capabilities. Give hints about where things _might_ be and the overall shape of the project. Let the agent generate its own just-in-time documentation during planning.

Domain concepts (like "organization" vs "group" vs "workspace") are more stable than file paths, so they're safer to document. But even these can drift in fast-moving AI-assisted codebases. Keep a light touch.

## Cutting Down Large `AGENTS.md` Files

Be ruthless about what goes here. Consider this the absolute minimum:

- **One-sentence project description** (acts like a role-based prompt)
- **Package manager** (if not npm; or use `corepack` for warnings)
- **Build/typecheck commands** (if non-standard)

That's honestly it. Everything else should go elsewhere.

### The One-Liner Project Description

This single sentence gives the agent context about _why_ they're working in this repository. It anchors every decision they make.

Example:

```markdown
This is a React component library for accessible data visualization.
```

That's the foundation. The agent now understands its scope.

### Package Manager Specification

If you're In a JavaScript project and using anything other than npm, tell the agent explicitly:

```markdown
This project uses pnpm workspaces.
```

Without this, the agent might default to `npm` and generate incorrect commands.

<details>
  <summary>Corepack is also great</summary>
You could also use [`corepack`](https://github.com/nodejs/corepack) to let the system handle warnings automatically, saving you precious instruction budget.
</details>

### Use Progressive Disclosure

Instead of cramming everything into `AGENTS.md`, use **progressive disclosure**: give the agent only what it needs right now, and point it to other resources when needed.

Agents are fast at navigating documentation hierarchies. They understand context well enough to find what they need.

#### Move Language-Specific Rules to Separate Files

If your `AGENTS.md` currently says:

```markdown
Always use const instead of let.
Never use var.
Use interface instead of type when possible.
Use strict null checks.
...
```

Move that to a separate file instead. In your root `AGENTS.md`:

```markdown
For TypeScript conventions, see docs/TYPESCRIPT.md
```

Notice the light touch, no "always," no all-caps forcing. Just a conversational reference.

The benefits:

- TypeScript rules only load when the agent writes TypeScript
- Other tasks (CSS debugging, dependency management) don't waste tokens
- File stays focused and portable across model changes

#### Nest Progressive Disclosure

You can go even deeper. Your `docs/TYPESCRIPT.md` can reference `docs/TESTING.md`. Create a discoverable resource tree:

```
docs/
├── TYPESCRIPT.md
│   └── references TESTING.md
├── TESTING.md
│   └── references specific test runners
└── BUILD.md
    └── references esbuild configuration
```

You can even link to external resources, Prisma docs, Next.js docs, etc. The agent will navigate these hierarchies efficiently.

#### Use Agent Skills

Many tools support "agent skills" - commands or workflows the agent can invoke to learn how to do something specific. These are another form of progressive disclosure: the agent pulls in knowledge only when needed.

We'll cover agent skills in-depth in a separate article.

## `AGENTS.md` in Monorepos

You're not limited to a single `AGENTS.md` at the root. You can place `AGENTS.md` files in subdirectories, and they **merge with the root level**.

This is powerful for monorepos:

### What Goes Where

| Level       | Content                                                                    |
| ----------- | -------------------------------------------------------------------------- |
| **Root**    | Monorepo purpose, how to navigate packages, shared tools (pnpm workspaces) |
| **Package** | Package purpose, specific tech stack, package-specific conventions         |

Root `AGENTS.md`:

```markdown
This is a monorepo containing web services and CLI tools.
Use pnpm workspaces to manage dependencies.
See each package's AGENTS.md for specific guidelines.
```

Package-level `AGENTS.md` (in `packages/api/AGENTS.md`):

```markdown
This package is a Node.js GraphQL API using Prisma.
Follow docs/API_CONVENTIONS.md for API design patterns.
```

**Don't overload any level.** The agent sees all merged `AGENTS.md` files in its context. Keep each level focused on what's relevant at that scope.

## Fix A Broken `AGENTS.md` With This Prompt

If you're starting to get nervous about the `AGENTS.md` file in your repo, and you want to refactor it to use progressive disclosure, try copy-pasting this prompt into your coding agent:

```txt
I want you to refactor my AGENTS.md file to follow progressive disclosure principles.

Follow these steps:

1. **Find contradictions**: Identify any instructions that conflict with each other. For each contradiction, ask me which version I want to keep.

2. **Identify the essentials**: Extract only what belongs in the root AGENTS.md:
   - One-sentence project description
   - Package manager (if not npm)
   - Non-standard build/typecheck commands
   - Anything truly relevant to every single task

3. **Group the rest**: Organize remaining instructions into logical categories (e.g., TypeScript conventions, testing patterns, API design, Git workflow). For each group, create a separate markdown file.

4. **Create the file structure**: Output:
   - A minimal root AGENTS.md with markdown links to the separate files
   - Each separate file with its relevant instructions
   - A suggested docs/ folder structure

5. **Flag for deletion**: Identify any instructions that are:
   - Redundant (the agent already knows this)
   - Too vague to be actionable
   - Overly obvious (like "write clean code")
```

## Don't Build A Ball Of Mud

When you're about to add something to your `AGENTS.md`, ask yourself where it belongs:

| Location                  | When to use                                        |
| ------------------------- | -------------------------------------------------- |
| Root `AGENTS.md`          | Relevant to every single task in the repo          |
| Separate file             | Relevant to one domain (TypeScript, testing, etc.) |
| Nested documentation tree | Can be organized hierarchically                    |

The ideal `AGENTS.md` is small, focused, and points elsewhere. It gives the agent just enough context to start working, with breadcrumbs to more detailed guidance.

Everything else lives in progressive disclosure: separate files, nested `AGENTS.md` files, or skills.

This keeps your instruction budget efficient, your agent focused, and your setup future-proof as tools and best practices evolve.

## Document 3. OpenAI Codex Guide

### Source
- Title: `Custom instructions with AGENTS.md`
- Source URL: `https://developers.openai.com/codex/guides/agents-md`
- Publisher: OpenAI Developers
- Product area: Codex documentation
- Captured: April 19, 2026
- Note: This is an official product guide describing how Codex actually discovers and merges instruction files.
# Custom instructions with AGENTS.md

Codex reads `AGENTS.md` files before doing any work. By layering global guidance with project-specific overrides, you can start each task with consistent expectations, no matter which repository you open.

## How Codex discovers guidance

Codex builds an instruction chain when it starts (once per run; in the TUI this usually means once per launched session). Discovery follows this precedence order:

1. **Global scope:** In your Codex home directory (defaults to `~/.codex`, unless you set `CODEX_HOME`), Codex reads `AGENTS.override.md` if it exists. Otherwise, Codex reads `AGENTS.md`. Codex uses only the first non-empty file at this level.
2. **Project scope:** Starting at the project root (typically the Git root), Codex walks down to your current working directory. If Codex cannot find a project root, it only checks the current directory. In each directory along the path, it checks for `AGENTS.override.md`, then `AGENTS.md`, then any fallback names in `project_doc_fallback_filenames`. Codex includes at most one file per directory.
3. **Merge order:** Codex concatenates files from the root down, joining them with blank lines. Files closer to your current directory override earlier guidance because they appear later in the combined prompt.

Codex skips empty files and stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default). For details on these knobs, see [Project instructions discovery](https://developers.openai.com/codex/config-advanced#project-instructions-discovery). Raise the limit or split instructions across nested directories when you hit the cap.

## Create global guidance

Create persistent defaults in your Codex home directory so every repository inherits your working agreements.

1. Ensure the directory exists:

   ```bash
   mkdir -p ~/.codex
   ```

2. Create `~/.codex/AGENTS.md` with reusable preferences:

   ```md
   # ~/.codex/AGENTS.md

   ## Working agreements

   - Always run `npm test` after modifying JavaScript files.
   - Prefer `pnpm` when installing dependencies.
   - Ask for confirmation before adding new production dependencies.
   ```

3. Run Codex anywhere to confirm it loads the file:

   ```bash
   codex --ask-for-approval never "Summarize the current instructions."
   ```

   Expected: Codex quotes the items from `~/.codex/AGENTS.md` before proposing work.

Use `~/.codex/AGENTS.override.md` when you need a temporary global override without deleting the base file. Remove the override to restore the shared guidance.

## Layer project instructions

Repository-level files keep Codex aware of project norms while still inheriting your global defaults.

1. In your repository root, add an `AGENTS.md` that covers basic setup:

   ```md
   # AGENTS.md

   ## Repository expectations

   - Run `npm run lint` before opening a pull request.
   - Document public utilities in `docs/` when you change behavior.
   ```

2. Add overrides in nested directories when specific teams need different rules. For example, inside `services/payments/` create `AGENTS.override.md`:

   ```md
   # services/payments/AGENTS.override.md

   ## Payments service rules

   - Use `make test-payments` instead of `npm test`.
   - Never rotate API keys without notifying the security channel.
   ```

3. Start Codex from the payments directory:

   ```bash
   codex --cd services/payments --ask-for-approval never "List the instruction sources you loaded."
   ```

   Expected: Codex reports the global file first, the repository root `AGENTS.md` second, and the payments override last.

Codex stops searching once it reaches your current directory, so place overrides as close to specialized work as possible.

Here is a sample repository after you add a global file and a payments-specific override:

<FileTree
  class="mt-4"
  tree={[
    {
      name: "AGENTS.md",
      comment: "Repository expectations",
      highlight: true,
    },
    {
      name: "services/",
      open: true,
      children: [
        {
          name: "payments/",
          open: true,
          children: [
            {
              name: "AGENTS.md",
              comment: "Ignored because an override exists",
            },
            {
              name: "AGENTS.override.md",
              comment: "Payments service rules",
              highlight: true,
            },
            { name: "README.md" },
          ],
        },
        {
          name: "search/",
          children: [{ name: "AGENTS.md" }, { name: "…", placeholder: true }],
        },
      ],
    },
  ]}
/>

## Customize fallback filenames

If your repository already uses a different filename (for example `TEAM_GUIDE.md`), add it to the fallback list so Codex treats it like an instructions file.

1. Edit your Codex configuration:

   ```toml
   # ~/.codex/config.toml
   project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]
   project_doc_max_bytes = 65536
   ```

2. Restart Codex or run a new command so the updated configuration loads.

Now Codex checks each directory in this order: `AGENTS.override.md`, `AGENTS.md`, `TEAM_GUIDE.md`, `.agents.md`. Filenames not on this list are ignored for instruction discovery. The larger byte limit allows more combined guidance before truncation.

With the fallback list in place, Codex treats the alternate files as instructions:

<FileTree
  class="mt-4"
  tree={[
    {
      name: "TEAM_GUIDE.md",
      comment: "Detected via fallback list",
      highlight: true,
    },
    {
      name: ".agents.md",
      comment: "Fallback file in root",
    },
    {
      name: "support/",
      open: true,
      children: [
        {
          name: "AGENTS.override.md",
          comment: "Overrides fallback guidance",
          highlight: true,
        },
        {
          name: "playbooks/",
          children: [{ name: "…", placeholder: true }],
        },
      ],
    },
  ]}
/>

Set the `CODEX_HOME` environment variable when you want a different profile, such as a project-specific automation user:

```bash
CODEX_HOME=$(pwd)/.codex codex exec "List active instruction sources"
```

Expected: The output lists files relative to the custom `.codex` directory.

## Verify your setup

- Run `codex --ask-for-approval never "Summarize the current instructions."` from a repository root. Codex should echo guidance from global and project files in precedence order.
- Use `codex --cd subdir --ask-for-approval never "Show which instruction files are active."` to confirm nested overrides replace broader rules.
- Check `~/.codex/log/codex-tui.log` (or the most recent `session-*.jsonl` file if you enabled session logging) after a session if you need to audit which instruction files Codex loaded.
- If instructions look stale, restart Codex in the target directory. Codex rebuilds the instruction chain on every run (and at the start of each TUI session), so there is no cache to clear manually.

## Troubleshoot discovery issues

- **Nothing loads:** Verify you are in the intended repository and that `codex status` reports the workspace root you expect. Ensure instruction files contain content; Codex ignores empty files.
- **Wrong guidance appears:** Look for an `AGENTS.override.md` higher in the directory tree or under your Codex home. Rename or remove the override to fall back to the regular file.
- **Codex ignores fallback names:** Confirm you listed the names in `project_doc_fallback_filenames` without typos, then restart Codex so the updated configuration takes effect.
- **Instructions truncated:** Raise `project_doc_max_bytes` or split large files across nested directories to keep critical guidance intact.
- **Profile confusion:** Run `echo $CODEX_HOME` before launching Codex. A non-default value points Codex at a different home directory than the one you edited.

## Next steps

- Visit the official [AGENTS.md](https://agents.md) website for more information.
- Review [Prompting Codex](https://developers.openai.com/codex/prompting) for conversational patterns that pair well with persistent guidance.