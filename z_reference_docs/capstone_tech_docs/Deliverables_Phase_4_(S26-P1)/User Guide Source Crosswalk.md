# Phase 4 User Guide Source Crosswalk

## Purpose

This crosswalk maps each Phase 4 User Guide section to:

- the prior deliverables that provide historical or explanatory context
- the current `origin/main` implementation that provides usage truth
- the known drift points we must avoid copying forward

This document exists so the User Guide can function as the Phase 4
"one-place stop" synthesis document without inheriting stale details from
earlier phases.

## Source Priority

For Phase 4 User Guide writing, use sources in this order:

1. current stable implementation on `origin/main`
2. Phase 4 template requirements
3. completed Phase 3 documents
4. supporting Phase 1 and Phase 2 documents

Working rule:

- if an older deliverable conflicts with the current repo behavior, document the
  current repo behavior
- use older deliverables for context, rationale, audience, and terminology
- do not document local worktree, prompt-lab, or unmerged experimental behavior
  as if it were part of the stable system

## Section Mapping

| User Guide Section | Primary Prior Docs | Current Repo Truth | Writing Notes |
| --- | --- | --- | --- |
| Introduction | Phase 1 Vision, Phase 1 Requirements, Phase 3 Deployment Procedure, Phase 3 Model Documentation | `README.md` | Explain mission, operator-facing purpose, and the fact that this is a research-focused automated BDA system rather than a fielded product. |
| System Overview | Phase 1 Design, Phase 2 Model Documentation, Phase 3 Model Documentation | `README.md`, `src/bda_svc/pipeline/config.yaml`, `src/bda_svc/pipeline/model.py`, `src/bda_svc/pipeline/interfaces.py` | Describe the stable CLI-first architecture and model roles in prose. Reuse an existing architecture figure only if it still matches `main`. |
| Using the System | Phase 2 Data Dictionary, Phase 2 Data Schema, Phase 3 Deployment Procedure, Phase 3 Customer Verification, Phase 3 Specification of Local Tests | `src/bda_svc/cli.py`, `src/bda_svc/app.py`, `src/bda_svc/inputs.py`, `src/bda_svc/export.py`, `README.md`, tests | Treat current CLI behavior and output structure as authoritative. |
| Deployment and Integration | Phase 3 Deployment Procedure | `README.md`, `docker/Dockerfile`, current CLI/runtime assumptions | Keep this section aligned to the stable local and containerized paths only. |
| Monitoring and Maintenance | Phase 4 Maintenance and Monitoring Plan Template, Phase 3 Specification of Local Tests, Phase 3 Customer Verification | tests, `CONTRIBUTING.md`, current repo structure | Focus on operator-visible checks, logging expectations, dependency/model upkeep, and where to find deeper maintenance guidance. |
| Troubleshooting and Support | Phase 3 Deployment Procedure, Phase 3 Specification of Local Tests | `src/bda_svc/inputs.py`, `src/bda_svc/pipeline/interfaces.py`, `README.md`, tests | Use real current failure modes from the stable implementation. |
| Appendices | Phase 1 Requirements, Phase 2 Data Dictionary, Phase 2 Data Schema | `README.md`, tests, current JSON/output shape | Good place for glossary, command examples, and a sample JSON fragment. |

## Stable User-Facing Interface To Document

The User Guide should describe only the current public-facing interface on
`origin/main`:

- CLI:
  - `bda-svc [-h] [-i INPUT] [-o OUTPUT]`
- user-relevant environment/runtime assumptions:
  - local Ollama server
  - optional `BDA_INPUT`
  - optional `OLLAMA_HOST`
- stable output shape at a high level:
  - `metadata`
  - `physical_damage`
  - `summary`

## Known Drift And Guardrails

### 1. Current runtime is narrower than some older documents

Older Phase 1/2/3 documents sometimes describe:

- optional object-detector-plus-VLM architectures
- optional Phase 2 functional damage assessment
- broader target sets

Current `origin/main` should instead be described as:

- a CLI-first BDA service
- using locally served Ollama VLMs
- performing target detection, Phase 1 physical damage assessment, and scene
  summarization

### 2. Current doctrine categories are narrower than the older schema

The older Phase 2 schema enumerates a much broader set of possible target types.
Current `origin/main` doctrine is narrower and currently centers on:

- `buildings`
- `military_equipment`

User Guide implication:

- do not copy the older full target-type enumeration into the main user-facing
  sections
- describe the stable system in terms of the current doctrinal categories and
  stable output behavior

### 3. Current bounding-box representation differs from the older schema doc

Older Phase 2 schema material describes `bounding_box` as an object with named
fields. Current `origin/main` export behavior emits the bounding box in list
form:

- `[xmin, ymin, xmax, ymax]`

User Guide implication:

- when giving an output example or interpretation note, follow the current code
  path, not the older schema wording

### 4. Python/runtime wording should follow stable repo truth

Some earlier docs were written against older container/runtime assumptions.
Current stable repo truth is:

- project requirement: Python `>=3.12`
- local workflow uses `uv`
- container path exists via `docker/Dockerfile`
- Ollama serves the runtime model separately from the application package

User Guide implication:

- keep operator language broad and accurate:
  - local CLI path
  - local Ollama runtime
  - container-compatible deployment path
- avoid overcommitting to stale version wording copied from older deliverables

## Explicit Exclusions

Do not treat any of the following as part of the stable User Guide system
description:

- prompt-lab runs under `z_reference_docs/Prompt_Labs/`
- Qwen or Gemma worktree experimentation
- local-only instrumentation or debug helpers
- unmerged branch behavior
- evaluation-only workflows unless they are discussed as supporting context
rather than normal user operation

## Deliverables To Maintain In Parallel

The Phase 4 User Guide work should stay synchronized across:

- `User Guide Working Draft.md`
- `User Guide Working Draft.docx`

The markdown file is the review and iteration surface.
The `.docx` file is the submission-aligned parallel draft.
