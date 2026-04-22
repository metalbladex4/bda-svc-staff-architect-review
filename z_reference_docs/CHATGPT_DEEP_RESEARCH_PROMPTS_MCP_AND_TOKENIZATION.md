# ChatGPT Deep Research Prompt Package

This file is a local support artifact for running targeted ChatGPT Deep
Research passes that are grounded in the real Capstone project context.

It is designed for two separate Deep Research runs:

1. MCP server recommendations for this project
2. Tokenization / wording / prompt-language research tied back to this project

The prompts are intentionally written to be pasted directly into ChatGPT Deep
Research with minimal or no editing.

## Shared Project Context Core

Use this when you want a reusable project description outside the full prompts.

```text
Project context:

I am working on a research-focused local CLI battle damage assessment (BDA)
system. It analyzes imagery and emits structured JSON reports. The current live
scope is Phase 1 physical damage assessment only, not broader all-source combat
assessment. The live target types are buildings and military_equipment.

The project is not trying to build a generic chatbot. It is trying to improve
prompting for visual detection and assessment in a very specific multimodal
workflow. The most important pain points are:

- detection prompts for images
- bounding box (bbox) quality
- bbox review artifacts and visual grounding review
- adjacent-building target selection
- reducing background-building false positives
- preserving reliable control-case behavior while improving localization

The team uses a local prompt-lab workflow with A/B comparisons, review
artifacts, bbox review sheets, and image-by-image analysis. The current
question is not “how do we prompt LLMs in general?” It is “what would most help
us improve prompt engineering and bbox behavior for this specific BDA
workflow?”

Useful recommendations should help with one or more of:

- better prompt engineering
- better bbox review or spatial-debug workflows
- better retrieval of technical docs, papers, model cards, and research notes
- better experiment comparison and evidence handling

Please do not optimize for:

- generic chatbot usage
- unrelated software-agent workflows
- popular tools that do not clearly help prompt or bbox work
```

## Prompt A

Paste this into ChatGPT Deep Research when you want a ranked MCP recommendation
set.

```text
I want you to perform deep research and give me a high-quality recommendation
report on the best MCP servers for my project.

First, here is the project context you must anchor to:

I am working on a research-focused local CLI battle damage assessment (BDA)
system. It analyzes imagery and emits structured JSON reports. The current live
scope is Phase 1 physical damage assessment only, not broader all-source combat
assessment. The live target types are buildings and military_equipment.

The project is not trying to build a generic chatbot. It is trying to improve
prompting for visual detection and assessment in a very specific multimodal
workflow. The most important pain points are:

- detection prompts for images
- bounding box (bbox) quality
- bbox review artifacts and visual grounding review
- adjacent-building target selection
- reducing background-building false positives
- preserving reliable control-case behavior while improving localization

The team uses a local prompt-lab workflow with A/B comparisons, review
artifacts, bbox review sheets, and image-by-image analysis. The current
question is not “how do we prompt LLMs in general?” It is “what would most help
us improve prompt engineering and bbox behavior for this specific BDA
workflow?”

Useful recommendations should help with one or more of:

- better prompt engineering
- better bbox review or spatial-debug workflows
- better retrieval of technical docs, papers, model cards, and research notes
- better experiment comparison and evidence handling

Please do not optimize for:

- generic chatbot usage
- unrelated software-agent workflows
- popular tools that do not clearly help prompt or bbox work

Now do the actual research task:

Research the best currently available MCP servers (Model Context Protocol
servers) that would help this project. I care most about MCP servers that help
with context and document access, but I also want you to surface other MCP
servers if they would materially improve prompt engineering, bbox review,
research retrieval, experiment triage, or image/vision workflow support.

Important constraints and preferences:

- prioritize mostly free or low-cost options
- local-friendly or privacy-friendly options should be favored when practical
- document/context access is the primary use case
- image, bbox, spatial-debug, or experiment-analysis tooling is valuable if it
  has clear project-specific benefit
- I want actual MCP servers or clearly MCP-compatible offerings, not generic
  SaaS recommendations that do not have a real MCP path
- do not recommend something just because it is popular
- if a category is overkill for a small research-focused local CLI project, say
  so directly

Please answer these questions explicitly:

1. Which MCP servers would most improve our prompting workflow?
2. Which MCP servers would most improve bbox review, visual grounding review,
   or spatial-debug workflows?
3. Which MCP servers would most improve research retrieval and source
   grounding?
4. Which recommended options are mostly free or low-cost?
5. Which recommended options are local-friendly or self-hostable?
6. Which options are likely overkill for this project?

When you evaluate candidates, rank them by:

- usefulness to this specific project
- cost
- ease of adoption
- privacy / local-friendliness
- likely day-to-day value during prompt engineering
- maintenance health and current relevance

I want you to prioritize MCP servers that improve:

- access to technical docs, papers, model cards, and research references
- structured retrieval across project knowledge sources
- image, vision, bbox, or artifact review workflows
- experiment comparison or evidence triage, but only if that materially helps
  prompt iteration

Research quality rules:

- prefer official documentation, primary papers, or technically credible
  implementation sources
- use recent sources where the ecosystem is fast-moving
- distinguish evidence from inference
- include direct links and concrete citations
- do not give me generic “best AI tools” fluff
- tie each recommendation back to this exact project shape

Please structure the final answer as:

1. Executive recommendation
2. Ranked shortlist table
3. Highest priority MCP servers to adopt now
4. Worth considering later
5. Not worth the complexity for this project
6. Per-server rationale with project-specific use cases
7. Adoption order
8. Risks, limitations, and open questions

For each recommended MCP server, include:

- what it is
- why it helps this project specifically
- whether it mainly helps document/context access, bbox/vision review, or
  another secondary use case
- whether it is free, low-cost, or paid
- whether it is local-friendly, privacy-friendly, or cloud-first
- how mature and actively maintained it appears to be
- whether it is a “use now,” “use later,” or “skip” recommendation

If you find that some of the best options are not MCP servers but rather
adjacent tools that influence MCP strategy, you may mention them briefly, but
the main deliverable must stay centered on actual MCP recommendations.
```

## Prompt B

Paste this into ChatGPT Deep Research when you want the tokenization / wording
research.

```text
I want you to perform deep research on a prompt-engineering theory and tie the
findings back to my project in a practical way.

First, here is the project context you must anchor to:

I am working on a research-focused local CLI battle damage assessment (BDA)
system. It analyzes imagery and emits structured JSON reports. The current live
scope is Phase 1 physical damage assessment only, not broader all-source combat
assessment. The live target types are buildings and military_equipment.

The project is not trying to build a generic chatbot. It is trying to improve
prompting for visual detection and assessment in a very specific multimodal
workflow. The most important pain points are:

- detection prompts for images
- bounding box (bbox) quality
- bbox review artifacts and visual grounding review
- adjacent-building target selection
- reducing background-building false positives
- preserving reliable control-case behavior while improving localization

The team uses a local prompt-lab workflow with A/B comparisons, review
artifacts, bbox review sheets, and image-by-image analysis. The current
question is not “how do we prompt LLMs in general?” It is “what would most help
us improve prompt engineering and bbox behavior for this specific BDA
workflow?”

Useful recommendations should help with one or more of:

- better prompt engineering
- better bbox review or spatial-debug workflows
- better retrieval of technical docs, papers, model cards, and research notes
- better experiment comparison and evidence handling

Please do not optimize for:

- generic chatbot usage
- unrelated software-agent workflows
- popular tools that do not clearly help prompt or bbox work

Now do the actual research task:

I have a theory that when prompt wording is shorter, uses simpler words, and
avoids run-on phrasing, it may help LLM performance because more of the wording
fits into cleaner or fewer tokens and is easier for the model to process. I do
not want you to assume this theory is correct. I want you to investigate it.

Please research whether shorter words or simpler phrasing materially help LLM
performance because of tokenization efficiency, or whether the real benefit is
better explained by other factors such as:

- fewer total tokens
- clearer syntax
- reduced instruction competition
- shorter dependency chains
- lower ambiguity
- lower context burden
- stronger instruction hierarchy
- better example salience

I want you to distinguish carefully between:

- tokenization mechanics
- prompt clarity
- instruction hierarchy
- model architecture / attention effects
- practical prompting outcomes

Please investigate questions like:

1. Is there evidence that shorter words being represented in one or fewer
   tokens materially helps prompt performance?
2. Is the theory overstated because modern tokenizers and models reduce that
   effect?
3. When does shorter phrasing help?
4. When does shorter phrasing hurt because it removes needed precision or
   specificity?
5. Is the real gain usually from simpler structure rather than shorter words?
6. What does the best evidence suggest for modern instruction-tuned LLMs and
   multimodal VLMs?

Tie the answer back to my actual project, especially:

- detection prompts for images
- bbox localization
- adjacent-building selection
- compact but strong instruction hierarchy
- example structure versus prose rules
- multimodal prompting for VLMs rather than text-only prompting in the abstract

I especially want practical conclusions for bbox-sensitive prompt work. For
example, I want to know whether the research supports things like:

- shorter rule lines
- less run-on phrasing
- more compact examples
- stronger instruction ordering
- smaller but sharper wording blocks
- when to compress versus when to preserve detail

Research quality rules:

- prefer official documentation, primary papers, tokenizer documentation, and
  technically credible sources
- use recent sources where model behavior may have shifted
- distinguish evidence from inference
- include direct links and concrete citations
- do not give generic prompt-engineering folklore without evaluating whether it
  is actually supported
- tie all conclusions back to this project shape

Please structure the final answer as:

1. Executive conclusion
2. Is the theory supported, unsupported, or partially supported?
3. Evidence review
4. What tokenization likely affects versus what syntax/clarity likely affects
5. What seems true for modern LLMs and VLMs
6. Practical implications for bbox-sensitive prompt writing
7. Concrete rewrite heuristics for this project
8. Example prompt-writing principles we should adopt
9. Open questions or places where the evidence is weak

In the practical section, I want you to explicitly say:

- what changes I should make if the theory is mostly true
- what changes I should make if the theory is only partially true
- what changes I should avoid if the theory is mostly folklore

Do not stop at abstract explanation. End with concrete guidance that a team
doing prompt A/B testing on bbox localization could actually use.
```

## Usage Notes

- Run **Prompt A** when you want a current shortlist of MCP servers worth
  adopting for the project.
- Run **Prompt B** when you want research-backed guidance on whether wording
  compression, shorter phrasing, and tokenization-aware prompt design are
  likely to help this repo’s bbox-sensitive prompt work.
- If both are run, compare them together by asking:
  - which recommendations change how we gather context
  - which recommendations change how we write prompts
  - which recommendations are cheap enough to adopt immediately
  - which recommendations are strong enough to justify a new prompt-lab cycle

## Working Rule

Treat this file as a local support bundle for outside research. It is not a
stable runtime spec, not a prompt-lab winner log, and not a GitHub deliverable.
