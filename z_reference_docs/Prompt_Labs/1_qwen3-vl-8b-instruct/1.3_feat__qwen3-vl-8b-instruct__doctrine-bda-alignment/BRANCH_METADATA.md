# Branch Metadata

- branch_type: `feature`
- git_branch: `feat/qwen3-vl-8b-instruct/doctrine-bda-alignment`
- parent_branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- base_commit: `6ab67d6`
- model_name: `qwen3-vl:8b-instruct`
- numbering_prefix: `1.3`
- worktree_path: `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment`
- docs_root: `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/`

## Notes

- This branch was created as a local-only doctrine A/B surface.
- It intentionally branches from the current active Qwen feature line rather
  than from the older model branch root.
- Its purpose is to test a Phase-1 PDA-aligned replacement `doctrine.yaml`
  without disturbing the active Qwen feature branch.
- The first runtime candidate doctrine is now installed here and passes:
  - `uv run pytest tests/unit/test_yamls.py tests/unit/test_utilities.py`
- Same-input parent-control review on `destroyed_building4` now shows the first
  doctrine candidate did not materially improve bbox quality or doctrinal fit
  on that scene.
- A Qwen-only `v002` doctrine candidate that changes only
  `buildings.detection_guidance` is now installed here for follow-up testing.
- That `v002` rerun did not produce a convincing improvement on the expanded
  building shot group.
