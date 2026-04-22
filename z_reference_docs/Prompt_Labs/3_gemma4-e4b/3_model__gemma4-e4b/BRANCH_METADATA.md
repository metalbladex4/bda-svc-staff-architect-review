# Branch Metadata

- branch_type: `model`
- git_branch: `model/gemma4-e4b`
- parent_branch: `main`
- creation_base_commit: `28e863b`
- current_upstream_aligned_infra_base: `e7a22a9`
- model_name: `gemma4:e4b`
- numbering_prefix: `3`
- worktree_path: `/home/williambenitez1/Capstone_worktrees/3_model__gemma4-e4b`
- docs_root: `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3_model__gemma4-e4b/`

## Notes

- This is the long-lived Gemma 4 E4B model line.
- It inherits the reusable prompt-lab review-artifact workflow from the Qwen
  line through:
  - `0102a27` — `Add prompt-lab review artifacts to bda_eval`
  - `3dc5f3e` — `Install workspace packages in CI`
- It was first refreshed through `c19940a` without a prompt-baseline rebuild
  because that upstream delta was infra-only.
- It was later refreshed again through `e7a22a9`, which changed live export and
  detect-prompt behavior.
- It now also carries:
  - `54a9d58` — `Bootstrap Gemma 4 E4B baseline config`
- Branch contract:
  - reusable parent for future Gemma feature branches
  - expected to stay prompt-lab smoke-capable after upstream refreshes
  - expected to keep tracked config aligned with the active Gemma line defaults
    unless we intentionally open a new Gemma model line
- Current practical status:
  - defaults to `gemma4:e4b` in tracked config
  - can run `bda-svc` prompt-lab smoke exports against the local Gemma host
  - can write prompt-lab smoke artifacts into
    `z_reference_docs/Prompt_Labs/...`
  - after the `e7a22a9` refresh, the standard tank smoke export now falls to
    `object_not_found`, so the usual `bda_eval` self-check does not currently
    close on that seed image
