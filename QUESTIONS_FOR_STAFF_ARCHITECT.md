
# Questions For The Staff Architect

Please review this repository and the accompanying local-context material as a Staff
AI Systems Architect and Prompt/Evaluation Lead for a multimodal VLM pipeline.

## Primary Questions

1. Is the current high-level detect / assess / summarize split still the right
   architecture for this project?
2. Is the doctrine-vs-prompt experimentation structure sound, or are we mixing too
   many concerns in a way that slows progress?
3. Is the Qwen/Gemma branch strategy and evidence chain well designed for the kind of
   model-porting and prompt work being attempted here?
4. What should be promoted into stable tracked runtime code versus kept local-only as
   evidence, references, or lab infrastructure?
5. Where do you see the best leverage for improving the workflow overall, not just the
   prompts themselves?

## Prompt Workflow And Evaluation Questions

Please make concrete recommendations on improving:

- the prompt engineering workflow as a whole
- the `Prompt_Labs` structure and operating model
- the iterative refinement loop
- the critique / research / revise cycle
- evaluation design, calibration discipline, and failure-analysis loops
- promotion criteria for moving local wins into stable code/docs

## Recursive Self-Improvement Questions

Please suggest safe and bounded forms of recursive self-improvement such as:

- self-critique that produces useful next-step hypotheses instead of noise
- automated candidate generation with review gates
- evaluation-driven revision loops
- stronger branch/lab structures for preserving what was learned
- where recursion should stop and require human judgment

## Agentic Tooling And Extensibility Questions

Based on the repo plus `STAFF_ARCHITECT_BRIEF.md`, please recommend:

- which MCPs, skills, subagents, plugins, rules, or automations should be added next
- which current extensibility surfaces are being used well versus poorly
- where agentic support could make the workflow better
- where agentic complexity would likely hurt more than help

## Current Project Context To Keep In Mind

- this project is a local multimodal VLM BDA pipeline with local Ollama-served models
- the current active local problem thread at snapshot time is the Qwen `1.3` doctrine
  work and its dirty local doctrine/config pair
- `z_reference_docs/` is the local evidence/research/documentation layer and should be
  read as such
- `capstone_tech_docs/` is related context, not direct runtime code
- `BDAs/` and `Prompting/` are reference shelves, not implementation folders
- the goal is not only “better prompts,” but a better end-to-end way of working:
  architecture, prompt workflow, evaluation discipline, iterative refinement, and
  better use of agentic tooling

## Constraints And Boundaries

- local machine state, secrets, and live Ollama availability are not directly visible
  to you from the repo
- token-bearing files and raw local Codex auth/state were intentionally excluded
- this is a private personal review mirror, not a team-facing public repo

Please be opinionated where you see leverage, especially on workflow design and where
the current process is helping versus hurting.
