
# Questions For The Staff Architect

Please review this repository and the accompanying local-context material as a
Staff AI Systems Architect and Prompt/Evaluation Lead for a multimodal VLM
pipeline.

For the current ChatGPT 5.5 Pro collaboration, start with:

```text
z_reference_docs/GPT-Pro_collab/chatgpt_5_5_pro_prompt_engineering_handoff.md
```

The immediate goal is no longer only a broad architect review. We also need
ChatGPT 5.5 Pro to understand the prompt-engineering history and then craft a
strong GPT Deep Research prompt that can improve Codex's recursive prompt
engineering process.

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

## Current Deep Research Handoff Questions

1. Given the `v020c` incumbent and the `v023/v024` plateau, should prompt-only
   search continue, or should the workflow pivot to visual review plus
   duplicate/tiling suppression or backend/post-processing?
2. What failure taxonomy should Codex apply before authoring each new prompt
   candidate?
3. How should Codex decide when a lesson is true signal, local noise, overfit
   behavior, or source-truth conflict?
4. What concrete Deep Research prompt should be sent to improve Codex's
   techniques, tactics, procedures, tool use, and recursive self-improvement
   loop?
5. Which existing tools should Codex use more effectively before adding new
   tools: Graphify/project-brain, SequentialThinking, Mem0, FiftyOne, prompt-lab
   runners, GitHub, or structured evidence indexes?
6. What low-risk additional tools or automation would materially improve
   prompt iteration, visual failure review, bbox diagnostics, experiment
   tracking, or candidate comparison?

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
- the current active local prompt thread is the Qwen v020c/v023/v024 prompt
  plateau and handoff to ChatGPT 5.5 Pro / Deep Research
- `v020c` is the Qwen incumbent; `v024l` is high-recall learning evidence only;
  `v024o` is partial and unscored
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
- GitHub currently reports this review repo as `PUBLIC`; treat it as a
  sanitized review surface, not a place for raw secrets or machine state

Please be opinionated where you see leverage, especially on workflow design and where
the current process is helping versus hurting.
