
# Sanitization Manifest

This private review repo intentionally excludes or redacts machine/auth/state artifacts.

## Excluded Or Redacted

- all `.git` internals and worktree-indirection files from the source workspaces
- all `.venv`, `.pytest_cache`, `.ruff_cache`, and `__pycache__` directories
- any `.codex/` directory content from the source workspace
- all raw `~/.codex` auth/state/session/memory/plugin-cache files
- local noise file `NUL` from the Capstone root checkout
- `z_reference_docs/capstone_tech_docs/APIKey.txt`
  - replaced with a placeholder note instead of raw contents

## Reason

- preserve the technical shape of the workspace without pushing secrets,
  credentials, machine-specific runtime state, or irrelevant local artifacts

## Important Note

The hidden Codex environment is summarized in `STAFF_ARCHITECT_BRIEF.md` rather than
mirrored as raw local files.
