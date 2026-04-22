# Capstone Tech Docs Understanding Tracking

## Purpose

This document is a living record of my understanding of the documents under
`z_reference_docs/capstone_tech_docs/`.

Its purpose is to make it easy for us to track:

- what each phase's documents appear to cover
- how those documents connect to the current project state
- where the documentation appears aligned with the codebase
- where there may be drift, ambiguity, or open questions
- what we still need to verify before writing or revising new deliverables

This is not meant to replace the deliverables themselves. It is a working
orientation document so we can quickly re-establish context and keep a running
record of how my understanding evolves as we review more of the technical
documents.

## Current Scope

The reviewed focus areas are now:

- the completed Phase 1 documents
- the completed Phase 2 documents
- the completed Phase 3 deliverables
- the Phase 4 deliverable templates, with the primary new focus on:
  - `z_reference_docs/capstone_tech_docs/Deliverables_Phase_4_(S26-P1)/User Guide Template.docx`

Per your guidance, the project team has:

- completed Phase 1 documents
- completed Phase 2 documents
- completed Phase 3 documentation work
- moved into Phase 4 documentation work

Your earlier focus was the Phase 3 deployment procedure document.
Your current focus is the Phase 4 User Guide.

Current draft status:

- an initial `.docx` deployment-procedure draft now exists
- the draft is written against the current `upstream/main` implementation
- the draft intentionally avoids local-only prompt-lab work and temporary
  debug instrumentation
- the draft now uses authoritative deployment language rather than explaining
  hardware requirements as provisional assumptions from earlier deliverables
- the project source of truth was re-synced to `upstream/main` at commit
  `28e863b` on `2026-04-15`, so future Phase 3 draft refinements should keep
  using the latest live `main` implementation rather than older deliverable
  assumptions
- the newest upstream delta is mostly evaluation-tooling work in `bda_eval/`,
  including image-backed evaluation, bbox overlay output, copied report folders
  in evaluation results, and richer LLMaaJ logging
- the live pipeline prompt surface also changed slightly in
  `src/bda_svc/pipeline/config.yaml` by adding a safeguard against all-zero
  non-null bounding boxes
- the broader local document workflow now also assumes the current global
  Codex tooling overlay in `/home/williambenitez1/.codex/AGENTS.md`, with
  detailed MCP routing guidance in
  `/home/williambenitez1/.codex/MCP_USAGE_GUIDE.md` and the selectively
  installed custom-agent subset recorded in
  `/home/williambenitez1/.codex/agents/VENDOR_MANIFEST.md`

## Current Priority Rule

For current Phase 4 User Guide writing, the source priority is now:

1. the current implementation on `main`
2. the Phase 4 deliverable template requirements
3. completed Phase 3 documents
4. Phase 1 and Phase 2 documents as supporting context

This means:

- Phase 1 and Phase 2 still matter
- Phase 3 now also matters as immediate supporting context because the User
  Guide is supposed to synthesize prior deliverables
- but older deliverables should now supplement the live implementation rather
  than override it
- if an older deliverable and the current codebase disagree, the current
  codebase on `main` should take priority unless the older deliverable is being
  cited specifically as historical rationale

## Current Documentation Workflow Overlay

For substantive document maintenance, the working support layer is now:

- use the global Codex tooling baseline as support infrastructure, not as a
  substitute for checking claims against `main`, the phase templates, and the
  completed deliverables
- prefer source-specific MCPs and connectors when they clearly fit the source
  being inspected
- use `sequentialthinking` before substantive updates to live maintained docs,
  global rules, or any `AGENTS.md`
- treat the globally installed custom agents as selective helpers, not as an
  instruction to auto-delegate every writing task

## Folder Inventory

Reviewed folder structure as of `2026-04-06`:

- `Deliverables_Phase_1_(S26-P1)/`
  Foundational project documents and end-of-phase presentation.
- `Deliverables_Phase_2_(S26-P1)/`
  Data, schema, model, and analysis deliverables plus phase presentations.
- `Deliverables_Phase_3_(S26-P1)/`
  Mid-phase presentation, API primer, and multiple templates for current
  deliverables.
- `Deliverables_Phase_4_(S26-P1)/`
  Present as a folder, but no reviewed files were found yet.

Important note:

- most of the files in these folders are `.docx`, `.pptx`, `.xlsx`, `.json`,
  and `.pdf`
- the understanding below is based on a first-pass review of filenames plus
  read-only extraction of key Phase 1, Phase 2, and Phase 3 document content

## Current High-Level Understanding

### Phase 1

Phase 1 appears to define the project foundation:

- vision
- requirements
- design
- plan

The strongest signal from the Phase 1 plan is that the project was designed as
a staged capstone effort moving from problem definition and design, into data
and modeling, then deployment/integration, then evaluation/redeployment.

From the reviewed `Plan Document`:

- Task 1: Requirements Gathering and Design
- Task 2: Data Engineering and Modeling
- Task 3: Deployment and Integration
- Task 4: Evaluation and Redeployment

The Plan document explicitly places deployment and integration in the Phase 3
window and describes:

- validating a VLM-only baseline first
- then integrating object detection
- then verifying end-to-end pipeline behavior
- then containerizing configurations for deployment testing
- then using Azure VM and ARL robotic-platform-aligned environments for
  operational validation

This is important because it means the deployment procedure document is not an
isolated writing exercise. It is directly tied to the planned Task 3 work in
the original project plan.

### Phase 2

Phase 2 appears to have moved the team from planning into concrete system and
data design artifacts.

The Phase 2 materials I reviewed suggest the team established:

- a formal BDA JSON schema
- data dictionary / schema support documentation
- exploratory data analysis
- model documentation
- evaluation methodology structure

From `BDA_DATA_SCHEMA.json`, the intended output structure includes:

- `metadata`
- `physical_damage`
- target-level entries with:
  - `target_type`
  - `damage_category`
  - `confidence_level`
  - `brief_supporting_logic`
  - optional `bounding_box`

This matters because the deployment procedure document will likely need to
reference what the system consumes and what it emits, even if it is not the
primary place where schema details are defined.

From the Phase 2 `Model Documentation`, my current understanding is that the
team documented the system as:

- a modular BDA pipeline
- separating localization from reasoning
- using zero-shot methods rather than fine-tuning
- running locally without external API calls at inference time
- targeting reproducible deployment via containerization
- evaluating both analytical performance and operational metrics such as
  inference time and GPU usage

That document also reinforces that deployment is expected to support:

- local runtime
- containerized packaging
- edge-oriented constraints
- evaluation across alternative model configurations

Important interpretation:

- this Phase 2 material is still useful context
- but the current repo on `main` has progressed beyond the completed Phase 1
  and Phase 2 deliverables
- so Phase 2 should be used to fill gaps and preserve continuity, not to define
  the current deployment procedure by itself

### Phase 3

Phase 3 appears to be the current documentation stage. The folder currently
contains:

- `Deployment procedure Template.docx`
- `Customer Test Requirements Verification Template.docx`
- `ETL report Template.docx`
- `Model Documentation Template.docx`
- `Specification of local tests Template.docx`
- `API Design Primer (if needed).pdf`
- `ARL Autonomous BDA - Mid Phase-3 Presentation (S26 Capstone).pptx`

My current understanding is that Phase 3 is where the team is expected to turn
the earlier planning and modeling work into deployable, testable, documented
engineering artifacts.

The Phase 3 presentation content reinforces that theme. In the extracted slide
text, the strongest recurring topics were:

- Docker runtime
- testing
- evaluation
- project plan milestones
- prompt tuning
- object detection integration
- comprehensive pipeline testing
- Docker image development

That lines up very closely with your current repo work and with your specific
focus on the deployment procedure document.

## Deployment Procedure Template Understanding

From the Phase 3 deployment template, the document is expected to cover these
sections:

- Overview
- Prerequisites
- Deployment Architecture
- Deployment Steps
- Post-Deployment Tasks
- Conclusion
- References
- Reflection
- Appendix
- Changes To Previous Deliverables

More specifically, the template expects the deployment procedure to describe:

- the ML model or system being deployed
- the purpose, audience, and benefits
- minimum hardware requirements
- software dependencies and versions
- data requirements and preprocessing expectations
- security and access-control expectations
- the high-level deployment architecture
- how the model is served
- scalability, performance, monitoring, and logging considerations
- environment setup
- model packaging
- model serving configuration
- deployment scripts or commands
- testing and validation steps
- rollback and version-control strategy
- post-deployment maintenance and update procedures

It also gives strong formatting guidance:

- brief and easy to understand
- roughly 1 to 3 paragraphs per section
- approximately 2 to 5 pages excluding references and appendix

## What This Means For Your Deployment Procedure Work

My current understanding is that your deployment procedure document should not
just explain "how to run the code." It should likely explain:

- what is being deployed
- where it is expected to run
- what prerequisites must be satisfied
- how the containerized/runtime environment is set up
- how the pipeline is invoked
- how outputs are validated
- how to recover if deployment fails
- how to maintain or update the deployed system afterward

For this project specifically, I expect the deployment procedure document will
need to reconcile:

- the capstone template requirements
- the actual current implementation on `main`, which is now the primary
  authority
- the team’s stated deployment and integration goals from the Phase 1 plan
- the operational constraints discussed in Phase 2 model documentation

## Important Cross-Document Connections

These are the most important links I currently see between documents:

### 1. Phase 1 Plan -> Phase 3 Deployment Procedure

The Phase 1 `Plan Document` explicitly defines a deployment and integration
task. That gives the deployment procedure document a strong planning anchor.

Current understanding:

- the deployment document should probably describe how the team actually
  executed Task 3, or how the system is now meant to be deployed in line with
  that task definition

### 2. Phase 2 Model Documentation -> Phase 3 Deployment Procedure

The Phase 2 `Model Documentation` describes the pipeline architecture, runtime
approach, modularity, and deployment intent.

Current understanding:

- the deployment procedure should use the system architecture and runtime
  assumptions from that document where they still reflect current reality
- but it should not blindly inherit old assumptions if the implementation on
  `main` has changed

Working rule:

- use Phase 2 model documentation to explain intent and architecture
- use current `main` to describe the actual deployment procedure we are writing

### 3. Phase 2 Data Schema -> Phase 3 Deployment Procedure

The JSON schema defines what the system is supposed to emit.

Current understanding:

- the deployment procedure should likely summarize expected inputs and outputs
- the schema and deployment doc should agree on what a successful run produces

Priority note:

- the Phase 2 schema remains an important contract reference
- but current runtime behavior on `main` should be checked first when writing
  Phase 3 deployment details

### 4. Phase 3 Local Testing + Customer Verification Templates -> Deployment Procedure

The Phase 3 templates are complementary, not isolated.

Current understanding:

- deployment procedure = how to stand up and run the system
- specification of local tests = how to test it locally
- customer test requirements verification = how to demonstrate it meets agreed
  expectations

That means the deployment procedure should probably mention validation or smoke
checks, but not try to absorb the entire local testing document.

## Current Document-Specific Understanding For Deployment

If we draft the deployment procedure against the current codebase, I expect the
most likely technical areas we will need to describe are:

- runtime environment
  - Linux environment
  - GPU availability and constraints
  - container runtime
  - model/runtime dependencies
- system packaging
  - Docker image or equivalent deployment artifact
  - what is bundled vs what is expected to already exist
- pipeline invocation
  - how input imagery is provided
  - how configuration is selected
  - how output is written
- operational verification
  - how to confirm the pipeline ran correctly
  - what artifacts a successful run produces
- update / rollback path
  - how to revert to a known-good version
  - how to handle model/config changes safely

## Important Open Questions / Risks

These are the main things I believe we should verify before treating my current
understanding as final:

### 1. Implementation Drift Between Deliverables And Current `main`

I already see a likely risk that some older technical assumptions in the
deliverables may not perfectly match the current repo implementation.

Current concern:

- the Phase 2 model documentation describes one runtime picture
- the current live repo may now reflect a somewhat different operational stack

This is especially important for the deployment procedure document, because it
should describe the system you actually intend to deploy, not only the system
described in earlier planning docs.

Decision rule:

- if Phase 1 or Phase 2 and current `main` differ, write the Phase 3 document
  around current `main`
- use the earlier documents only to explain intent, continuity, or prior
  assumptions where useful

### 2. Output / Schema Alignment

The Phase 2 schema establishes a formal output contract.

Current concern:

- we should verify how closely the current runtime output still aligns with the
  submitted schema and related Phase 2 documents before writing deployment
  steps that describe expected outputs

### 3. Target Deployment Environment

The planning documents mention:

- local workstations
- Azure VM testing
- edge robotic deployment / ARL platform alignment

Current concern:

- we should clarify which environment the deployment procedure document is
  really meant to target first:
  - developer local environment
  - validation VM
  - final robotic / edge runtime

### 4. API vs CLI Emphasis

The Phase 3 folder includes an API design primer, but the current project may
still be CLI-first.

Current concern:

- we should verify whether the deployment procedure is expected to document an
  API-serving workflow, a batch/CLI workflow, or both

## Most Relevant Files For The Next Step

If our next task is to work on the deployment procedure document, the most
relevant files appear to be:

- `z_reference_docs/capstone_tech_docs/Deliverables_Phase_3_(S26-P1)/Deployment procedure Template.docx`
- `z_reference_docs/capstone_tech_docs/Deliverables_Phase_3_(S26-P1)/ARL Autonomous BDA - Mid Phase-3 Presentation (S26 Capstone).pptx`
- `z_reference_docs/capstone_tech_docs/Deliverables_Phase_1_(S26-P1)/4. Plan Document.docx`
- `z_reference_docs/capstone_tech_docs/Deliverables_Phase_2_(S26-P1)/Model Documentation.docx`
- `z_reference_docs/capstone_tech_docs/Deliverables_Phase_2_(S26-P1)/BDA_DATA_SCHEMA.json`

And on the code side, I expect these to matter once we start drafting:

- `README.md`
- `docker/`
- `src/bda_svc/app.py`
- `src/bda_svc/cli.py`
- `src/bda_svc/export.py`
- `src/bda_svc/pipeline/config.yaml`
- `src/bda_svc/pipeline/model.py`

## Phase 3 Dependency Map For Deployment Procedure

My current view of the deployment-procedure document dependency order is:

### Primary Authority

1. current implementation on `main`

Reason:

- this is the real deployable system
- it defines the actual runtime behavior we need to describe in Phase 3

### Strongest Phase 3 Companion Documents

2. `Specification of local tests Template.docx`

Expected role:

- defines how a deployment is validated locally
- helps establish smoke checks, expected results, and testable post-deployment
  behavior

3. `Customer Test Requirements Verification Template.docx`

Expected role:

- defines what successful deployment needs to support from an acceptance
  perspective
- helps frame what evidence the deployment should make possible to gather

4. `Model Documentation Template.docx`

Expected role:

- supports hardware/software/runtime requirement sections
- supports model packaging and platform assumptions
- supports explanation of model-specific operational constraints

### Secondary Phase 3 Support

5. `ETL report Template.docx`

Expected role:

- supports any parts of deployment that depend on data preparation, ingestion,
  preprocessing, or staging

6. `API Design Primer (if needed).pdf`

Expected role:

- only relevant if the deployment procedure ends up needing an API-serving or
  service-contract framing
- likely secondary if the actual system remains CLI/container-first

### Supporting Earlier Deliverables

7. `Deliverables_Phase_1_(S26-P1)/4. Plan Document.docx`

Expected role:

- preserves original deployment/integration intent
- explains why deployment exists as a Phase 3 responsibility

8. `Deliverables_Phase_2_(S26-P1)/Model Documentation.docx`

Expected role:

- provides architectural and runtime context
- helps explain why the system is shaped the way it is

9. `Deliverables_Phase_2_(S26-P1)/BDA_DATA_SCHEMA.json`

Expected role:

- defines the intended output structure
- helps align deployment validation with expected system outputs

## Compact Dependency Map

```text
Deployment Procedure
├── Primary source of truth
│   └── current main codebase
├── Phase 3 direct companions
│   ├── Specification of local tests
│   ├── Customer test requirements verification
│   └── Model documentation
├── Phase 3 conditional / secondary support
│   ├── ETL report
│   └── API design primer (if API framing is needed)
└── Earlier supporting context
    ├── Phase 1 Plan document
    ├── Phase 2 Model documentation
    └── Phase 2 BDA data schema
```

## Deployment Procedure Dependency Interpretation

The main practical takeaway is:

- the deployment procedure should not wait on every other Phase 3 document to
  be perfect before work starts
- but once the other Phase 3 documents are completed, the strongest documents
  to cross-check against are:
  - local tests
  - customer verification
  - model documentation

These will likely be the most useful for tightening:

- prerequisites
- deployment validation
- expected outputs
- operational success criteria
- post-deployment maintenance expectations

## Current Deployment Procedure Draft Status

As of `2026-04-06 19:35 EDT`, the active draft is:

- `z_reference_docs/capstone_tech_docs/Deliverables_Phase_3_(S26-P1)/Deployment procedure Draft.docx`

Current interpretation:

- the draft is an initial Phase 3 deployment-procedure document, not a final
  submission
- it is written in the style of the completed capstone documents while using
  the Phase 3 deployment template as its structural guide
- it is anchored to `upstream/main`, not to local prompt-lab artifacts or
  uncommitted local-only debug changes
- it presents deployment requirements directly and authoritatively
- hardware requirements currently state the working deployment expectation:
  Linux-compatible machine, modern multi-core CPU, at least 32 GB system RAM,
  enough storage for the repo, environment, container image, Ollama model files,
  and artifacts, plus GPU support for local multimodal inference
- development-oriented deployments state at least 16 GB VRAM
- edge-target-aligned testing and deployment state compatibility with
  environments capped at 64 GB VRAM

Current disclosure boundary:

- do not include the prompt-lab workflow in the Phase 3 deployment draft unless
  you explicitly decide later that some part of it should become team-facing
- do not include temporary local debug-export behavior in the deployment draft
  unless it is promoted into the shared upstream implementation
- when describing technical behavior, prefer current `upstream/main` over local
  uncommitted work

## Recommended Next Step

The next deployment-document step is:

1. review the current draft for tone, section coverage, and team-facing
   correctness
2. verify any commands, model names, and deployment assumptions against
   `upstream/main`
3. update the draft after teammates provide the local tests, customer
   verification, and model documentation context
4. keep the draft authoritative and implementation-focused rather than
   explaining internal working assumptions

That should give us a deployment procedure that is both:

- aligned with the course template
- credible relative to the real implementation

## Entries

### 2026-04-06 18:10 EDT — Initial Review Recorded

What I reviewed:

- folder structure for all capstone tech docs phases
- Phase 3 template set
- API primer
- selected Phase 1 and Phase 2 documents for project context
- selected Phase 3 presentation content

What I currently believe:

- Phase 1 established the project foundation and task schedule
- Phase 2 established the structured data/model/evaluation picture
- Phase 3 is where deployment, testing, and operational documentation are
  being turned into concrete deliverables
- your deployment procedure work should be tied both to the template and to the
  actual current code on `main`

### 2026-04-06 18:18 EDT — Phase 3 Source Priority Clarified

What changed:

- clarified that the project has progressed beyond the completed Phase 1 and
  Phase 2 deliverables
- established that current `main` is the primary source of truth for Phase 3
  document writing

What this means:

- Phase 1 and Phase 2 are still important supporting references
- but they should now supplement and fill gaps for Phase 3 writing rather than
  define the current system behavior on their own
- this is especially important for the deployment procedure document, which
  should describe the deployable system as it exists now

### 2026-04-06 18:24 EDT — Deployment Procedure Dependency Map Added

What changed:

- added a dependency view for how the deployment procedure should relate to the
  rest of the capstone technical documents

Current understanding:

- current `main` remains the primary source of truth
- among Phase 3 deliverables, the strongest companion documents for deployment
  are expected to be:
  - specification of local tests
  - customer test requirements verification
  - model documentation
- ETL and API materials are secondary or conditional dependencies
- Phase 1 and Phase 2 documents remain supporting context

What still needs verification:

- exact deployment target and runtime assumptions
- code/document alignment for the current implementation
- how much of the deployment document should emphasize CLI flow versus broader
  service/API concepts

### 2026-04-06 19:35 EDT — Deployment Procedure Initial Draft Created And Tightened

What changed:

- created `Deployment procedure Draft.docx` in the Phase 3 deliverables folder
- structured it to match the Phase 3 deployment template while staying close to
  the tone and organization of the prior capstone documents
- wrote the technical content against `upstream/main`
- sanitized the draft so it does not disclose local prompt-lab work or temporary
  debug-export instrumentation
- revised the hardware section so it reads as a direct deployment requirement
  rather than a provisional assumption traced back to earlier deliverables

Current understanding:

- the draft is ready for an initial human review
- the strongest next refinements will come from verifying commands and runtime
  assumptions against the code, then incorporating teammate Phase 3 documents
  once they are available
- until then, the draft should remain focused on the current CLI-first,
  container-compatible deployment path backed by local Ollama model serving

### 2026-04-06 19:51 EDT — Main Environment Sync And Test Baseline Confirmed

What changed:

- confirmed local `main`, `origin/main`, and `upstream/main` are aligned
- ran `uv sync --dev` after the upstream update
- confirmed the local environment installed the upstream dependency
  `json-repair==0.58.7`
- ran the full test suite with `uv run pytest`

Verification:

- `35 passed`

Documentation impact:

- the deployment procedure draft can continue to treat current `upstream/main`
  as the implementation baseline
- the local environment is now consistent with the updated lockfile and current
  runtime dependencies
- the remaining local temporary debug-export work should still be kept out of
  the team-facing deployment draft unless it is later promoted into the shared
  upstream implementation

### 2026-04-17 23:55 EDT — Phase 4 User Guide Sources And Drift Risks Were Mapped

What changed:

- reviewed the completed Phase 3 documents as a finished documentation set
  instead of only as companion material for the deployment procedure
- reviewed the Phase 4 templates with special attention to:
  - `User Guide Template.docx`
  - `Maintenance and Monitoring Plan Template.docx`
  - `Model Training Evaluation Template.docx`
  - the two Phase 4 instruction documents
- compared those deliverables against the current `origin/main`
  implementation, including:
  - `README.md`
  - `src/bda_svc/cli.py`
  - `src/bda_svc/app.py`
  - `src/bda_svc/inputs.py`
  - `src/bda_svc/export.py`
  - `src/bda_svc/pipeline/config.yaml`
  - `src/bda_svc/pipeline/doctrine.yaml`
  - `src/bda_svc/pipeline/model.py`
  - `src/bda_svc/pipeline/interfaces.py`
  - `docker/Dockerfile`
  - the current unit tests
- created two new Phase 4 working artifacts:
  - `Deliverables_Phase_4_(S26-P1)/User Guide Source Crosswalk.md`
  - `Deliverables_Phase_4_(S26-P1)/User Guide Working Draft.md`

Current understanding:

- the Phase 4 User Guide is not meant to be a narrow add-on; it is supposed to
  function as the synthesis document that future users can rely on as a
  one-stop reference
- the best source rule for that guide is:
  1. current `main`
  2. Phase 4 template
  3. completed Phase 3 docs
  4. Phase 1 and Phase 2 supporting context
- the first three sections of the User Guide can be drafted now from stable
  repo truth without waiting on future Gemma or prompt-lab work

Important drift risks identified:

- older Phase 2 schema material describes `bounding_box` differently than the
  current export code; current `main` emits `[xmin, ymin, xmax, ymax]`
- older Phase 1/2/3 docs sometimes describe broader target coverage, optional
  object-detector architectures, or optional Phase 2 damage flows that should
  not be presented as the stable user-facing system on `main`
- current doctrine on `main` is narrower and currently centered on
  `buildings` and `military_equipment`
- Phase 4 writing must avoid treating local worktrees, prompt labs, and
  unmerged experimentation as if they are part of the stable system

Why it matters:

- this keeps the User Guide honest to the current implementation instead of
  accidentally turning it into a collage of outdated project descriptions
- it also makes it easier to draft the first three sections now while still
  leaving a coherent backbone for your partner to finish later
