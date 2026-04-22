
    # Branch State Manifest

    This manifest records the local branch/worktree line that was mirrored into this
    private review repo.

    ## Branch Map

    | Branch | Base Commit | Source Workspace | Dirty Tracked Files Captured |
    | --- | --- | --- | --- |
    | `main` | `e7a22a9` | `/home/williambenitez1/Capstone` | none |
| `model/qwen3-vl-8b-instruct` | `bf12f40` | `/home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct` | none |
| `feat/qwen3-vl-8b-instruct/two-pass-refinement` | `6ab67d6` | `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement` | src/bda_svc/pipeline/config.yaml |
| `feat/qwen3-vl-8b-instruct/doctrine-bda-alignment` | `6ab67d6` | `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment` | src/bda_svc/pipeline/config.yaml, src/bda_svc/pipeline/doctrine.yaml |
| `model/gemma4-e4b` | `9ae27e9` | `/home/williambenitez1/Capstone_worktrees/3_model__gemma4-e4b` | none |
| `feat/gemma4-e4b/qwen-v009-workflow-bootstrap` | `9ae27e9` | `/home/williambenitez1/Capstone_worktrees/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap` | src/bda_svc/pipeline/config.yaml, src/bda_svc/pipeline/model.py |
| `feat/gemma4-e4b/doctrine-bda-alignment` | `9ae27e9` | `/home/williambenitez1/Capstone_worktrees/3.2_feat__gemma4-e4b__doctrine-bda-alignment` | src/bda_svc/pipeline/doctrine.yaml |

    ## Notes

    - Every mirrored branch carries the same review-context payload so the reviewer can
      orient themselves without relying on default-branch behavior.
    - `z_reference_docs/` was copied from `/home/williambenitez1/Capstone/z_reference_docs`
      onto every branch because that tree is the shared local evidence and routing hub.
    - The active Qwen local resume point at snapshot time remained the dirty
      `feat/qwen3-vl-8b-instruct/doctrine-bda-alignment` worktree.
    - The public repositories remained unchanged; this private repo is the separate
      review surface.
