
# Staff Architect Review Index

This repository is a **private review snapshot** of the local Capstone multimodal
VLM workspace. It exists so ChatGPT Pro 5.4 can review the code, local evidence,
prompt labs, doctrine experiments, and supporting context as a Staff AI Systems
Architect and Prompt/Evaluation Lead.

Current branch review surface: `feat/qwen3-vl-8b-instruct/doctrine-bda-alignment`

## What This Repo Is

- a branch-preserving private mirror of the active local Capstone branch line
- a snapshot of local-only evidence that is not present in the public repo
- a review surface for architectural, prompt-workflow, evaluation-workflow,
  and agentic-tooling recommendations

## What This Repo Is Not

- not the day-to-day development repo going forward
- not the public team repo
- not a destination for routine future pushes unless explicitly requested

## Reading Order

1. `REVIEW_INDEX.md`
2. `Z_REFERENCE_DOCS_GUIDE.md`
3. `z_reference_docs/WORKING_CHANGELOG.md`
4. `z_reference_docs/REFERENCE_MASTER_INDEX.md`
5. the relevant branch-specific prompt-lab root under `z_reference_docs/Prompt_Labs/`
6. `STAFF_ARCHITECT_BRIEF.md`
7. `QUESTIONS_FOR_STAFF_ARCHITECT.md`

## Branch Context

- Source workspace path: `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment`
- Base commit captured here: `6ab67d6`
- Dirty tracked files captured in this private snapshot:
  `src/bda_svc/pipeline/config.yaml`, `src/bda_svc/pipeline/doctrine.yaml`

## Important Orientation Rule

Read `Z_REFERENCE_DOCS_GUIDE.md` before drawing conclusions from `z_reference_docs/`.
That tree is a layered local evidence/research/documentation hub, not a flat folder
of equally authoritative runtime sources.

## Focus Reset Rule

After this private mirror was created, normal work is intended to return to the
real Capstone workspace under `/home/williambenitez1/Capstone` and its active
worktrees. This review repo should only be updated again on explicit request.
