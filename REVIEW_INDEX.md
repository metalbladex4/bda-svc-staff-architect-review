
# Staff Architect Review Index

This repository is a review snapshot of the local Capstone multimodal VLM
workspace. It exists so ChatGPT 5.5 Pro can review the code, local evidence,
prompt labs, doctrine experiments, and supporting context as a Staff AI Systems
Architect and Prompt/Evaluation Lead.

Important visibility caveat: GitHub currently reports this repository as
`PUBLIC`. Treat this as a sanitized review surface. Do not add raw credentials,
raw local Codex state, private auth/session files, or unreviewed
secret-bearing artifacts.

Current branch review surface: `main`

Latest refresh: `2026-05-06`

Primary current handoff:

- `z_reference_docs/GPT-Pro_collab/chatgpt_5_5_pro_prompt_engineering_handoff.md`

## What This Repo Is

- a review mirror of the active local Capstone workspace and selected worktree
  evidence
- a snapshot of local-only evidence that is not present in the team repo
- a review surface for architectural, prompt-workflow, evaluation-workflow,
  and agentic-tooling recommendations

## What This Repo Is Not

- not the day-to-day development repo going forward
- not the public team repo
- not a destination for routine future pushes unless explicitly requested

## Reading Order

1. `REVIEW_INDEX.md`
2. `z_reference_docs/GPT-Pro_collab/chatgpt_5_5_pro_prompt_engineering_handoff.md`
3. `Z_REFERENCE_DOCS_GUIDE.md`
4. `z_reference_docs/WORKING_CHANGELOG.md`
5. `z_reference_docs/REFERENCE_MASTER_INDEX.md`
6. `z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
7. `docs/prompt-lab/qwen-v015-human-report-strategy/`
8. `STAFF_ARCHITECT_BRIEF.md`
9. `QUESTIONS_FOR_STAFF_ARCHITECT.md`

## Branch Context

- Source workspace path: `/home/williambenitez1/Capstone`
- Runtime code baseline captured here:
  `cmu-bda/bda-svc upstream/main`
  `f462ef4516b63ca1a2cd2434e75692f65d0e94cb`
- Prompt config overlay captured here:
  `feat/config-prompt-improved-v1`
  `9f1079daee9d50957048860e692e6a624befe230`
- Current prompt incumbent:
  `v020c_extra_box_audit` / `v020c_anchor_replay`
  at `186` matches / `33` false negatives / `25` false positives

## Important Orientation Rule

Read `Z_REFERENCE_DOCS_GUIDE.md` before drawing conclusions from `z_reference_docs/`.
That tree is a layered local evidence/research/documentation hub, not a flat folder
of equally authoritative runtime sources.

## Focus Reset Rule

After this review mirror is updated, normal work is intended to return to the
real Capstone workspace under `/home/williambenitez1/Capstone` and its active
worktrees. This review repo should only be updated again on explicit request.
