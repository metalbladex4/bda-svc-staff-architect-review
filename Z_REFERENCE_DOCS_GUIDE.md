
# `z_reference_docs` Guide

`z_reference_docs/` is the **local evidence, research, routing, and documentation
hub** for this project. It is intentionally broader than the tracked runtime code.
It should not be treated as one homogeneous source of truth.

## How To Read It

- use runtime code under `src/`, tests, and tracked branch history for actual
  implementation behavior
- use `z_reference_docs/` to understand how the project was reasoned about,
  evaluated, documented, and iterated locally
- when sources disagree, stable tracked runtime behavior should usually win unless
  a document is being consulted specifically as historical rationale or local evidence

## Main Families

### `Prompt_Labs/`

- local-only experiment workspaces, run manifests, versioned candidates, winners,
  and branch-specific prompt or doctrine evidence
- this is the primary record of prompt iteration, evaluation, and refinement history
- not every result here is promoted into stable runtime code

### `Doctrine_Experiments/`

- local-only doctrine audits, replacement candidates, crosswalks, and branch A/B
  support material
- this is experiment support material, not automatically live product behavior

### `Prompting/`

- reference shelf of model cards, cookbooks, prompting guides, research papers,
  and model-specific notes
- this is support/reference material used to inform the workflow
- it is not runtime code and not a claim that every source was adopted directly

### `BDAs/`

- doctrinal and military-methodology references used to ground BDA reasoning,
  terminology, and physical-damage interpretation
- this is a reference shelf, not implementation

### `Data_set_Storage/`

- working image/reference data used for evaluation, review artifacts, and local
  experimentation
- this is supporting evidence/input material, not product code

### `capstone_tech_docs/`

- capstone deliverables, templates, presentations, and understanding notes
- these documents are related to the project, but they are not the same thing as
  the current runtime implementation
- they provide academic/program context, reporting context, and deliverable history
- they should not be treated as the primary authority for current runtime behavior
  when they drift from the tracked code on `main`

## Top-Level Living Docs

### `WORKING_CHANGELOG.md`

- the running record of current project state, recent decisions, and the current
  way forward

### `REFERENCE_MASTER_INDEX.md`

- the main router into the rest of `z_reference_docs/`

### `PROMPT_DEVELOPMENT_METHODOLOGY.md`

- the long-form method history and lessons-learned record for the prompt workflow

### `PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`

- the teaching-grade explanation of how the prompting workflow is intended to work

## Practical Rule For Review

Use `z_reference_docs/` to understand the local research system around the codebase.
Do not collapse it into “the product,” and do not ignore it as mere notes. It is a
structured local evidence layer built to support prompt engineering, doctrine work,
evaluation, and capstone deliverables.
