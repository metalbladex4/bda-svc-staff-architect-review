# Branch Metadata

- branch_type: `model`
- git_branch: `model/qwen3-vl-8b-instruct`
- parent_branch: `main`
- creation_base_commit: `28e863b`
- current_upstream_aligned_infra_base: `e7a22a9`
- model_name: `qwen3-vl:8b-instruct`
- numbering_prefix: `1`
- worktree_path: `/home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct`
- docs_root: `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1_model__qwen3-vl-8b-instruct/`

## Notes

- Created during the git/worktree restructure on `2026-04-15`.
- This is the long-lived model line for tracked `qwen3-vl:8b-instruct`
  code/config work after `main` was reset to an exact mirror of
  `upstream/main`.
- It was first refreshed through `c19940a` without a prompt-baseline rebuild
  because that upstream delta was infra-only.
- It was later refreshed again through `e7a22a9`, which changed live export and
  detect-prompt behavior.
- It now also carries:
  - `b947a3e` — `Add prompt-lab review artifacts to bda_eval`
  - `0f916de` — `Install workspace packages in CI`
- Branch contract:
  - reusable parent for future Qwen feature branches
  - expected to stay prompt-lab smoke-capable after upstream refreshes
  - should not be treated as ancestry-only if future features depend on its
    reusable tooling/runtime shape
- Current practical status:
  - can run `bda-svc` prompt-lab smoke exports
  - can run `bda_eval` self-checks without requiring `OLLAMA_API_KEY`
  - can write prompt-lab smoke artifacts into `z_reference_docs/Prompt_Labs/...`
  - still completed the standard tank-based refresh smoke flow after the
    `e7a22a9` refresh
