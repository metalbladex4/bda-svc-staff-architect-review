
# Sanitization Manifest

This review repo intentionally excludes or redacts machine/auth/state artifacts.

GitHub currently reports this repository as `PUBLIC`, so the sanitization bar is
public-safe rather than private-only.

## Excluded Or Redacted

- all `.git` internals and worktree-indirection files from the source workspaces
- all `.venv`, `.pytest_cache`, `.ruff_cache`, and `__pycache__` directories
- any `.codex/` directory content from the source workspace
- all raw `~/.codex` auth/state/session/memory/plugin-cache files
- local noise file `NUL` from the Capstone root checkout
- all Windows `:Zone.Identifier` metadata sidecar files copied from the local docs snapshot
- `z_reference_docs/capstone_tech_docs/APIKey.txt`
  - replaced with a placeholder note instead of raw contents
- raw prompt-lab image overlays, large image review sheets, and predicted-output
  dumps from recent Qwen cycles
  - recent runs are represented with decision packets, overlays, comparison
    matrices, run summaries, eval summaries, diagnoses, and final
    recommendations instead

## Reason

- preserve the technical shape of the workspace without pushing secrets,
  credentials, machine-specific runtime state, or irrelevant local artifacts

## Important Note

The hidden Codex environment is summarized in `STAFF_ARCHITECT_BRIEF.md` rather than
mirrored as raw local files.
