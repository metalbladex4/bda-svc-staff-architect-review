# Gemma Worktree Update Checklist

This is the copy-paste checklist for the current Gemma branch line when
`upstream/main` moves again.

Use it together with:

- `z_reference_docs/GIT_WORKTREE_UPDATE_WORKFLOW.md`

This checklist assumes the refresh is **not** complete until the active Gemma
model and feature worktrees both pass the practical prompt-lab smoke flow.

## Current Branch Line

- clean mirror:
  - `/home/williambenitez1/Capstone`
  - branch: `main`
- model worktree:
  - `/home/williambenitez1/Capstone_worktrees/3_model__gemma4-e4b`
  - branch: `model/gemma4-e4b`
- feature worktree:
  - `/home/williambenitez1/Capstone_worktrees/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap`
  - branch: `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`

## Model-Line Defaults

- Ollama host override:
  - `OLLAMA_HOST=http://127.0.0.1:11435`
- expected tracked model tag in active config:
  - `gemma4:e4b`

The model and feature branches should both keep tracked config aligned with
that model-line default unless we intentionally open a different Gemma line.

## 0. Preflight

Check all three worktrees first.

### clean mirror

```bash
cd /home/williambenitez1/Capstone
git status --short --branch
```

### model worktree

```bash
cd /home/williambenitez1/Capstone_worktrees/3_model__gemma4-e4b
git status --short --branch
```

### feature worktree

```bash
cd /home/williambenitez1/Capstone_worktrees/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap
git status --short --branch
```

If `model/...` or `feat/...` is dirty:

```bash
git add -A
git commit -m "checkpoint: before upstream refresh to <new-upstream-sha>"
```

If `main` is dirty:

- stop and inspect before doing anything else

## 1. Refresh `main`

```bash
cd /home/williambenitez1/Capstone
git fetch upstream origin --prune
git switch main
git merge --ff-only upstream/main
git push origin main
```

## 2. Decide Whether The Active Gemma Baseline Must Be Rebuilt

Answer these:

- did live prompt text change?
- did doctrine wording change?
- did inference/runtime behavior change?

If all three answers are no, and the delta is only eval/docs/tests/CI/container
work:

- do **not** rebuild the active Gemma baseline

If any answer is yes:

- rebuild the active Gemma baseline after the rebase chain completes

## 3. Rebase The Model Branch

```bash
cd /home/williambenitez1/Capstone_worktrees/3_model__gemma4-e4b
git fetch upstream origin --prune
git rebase main
```

## 4. Rebase The Feature Branch

```bash
cd /home/williambenitez1/Capstone_worktrees/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap
git fetch upstream origin --prune
git rebase model/gemma4-e4b
```

Do not rebase this feature branch directly onto `main`.

## 5. Sync Workspace Packages Before Validation

### model branch

```bash
cd /home/williambenitez1/Capstone_worktrees/3_model__gemma4-e4b
uv sync --all-packages
```

### feature branch

```bash
cd /home/williambenitez1/Capstone_worktrees/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap
uv sync --all-packages
```

## 6. Run The Shared Sanity Tests

### model branch

```bash
cd /home/williambenitez1/Capstone_worktrees/3_model__gemma4-e4b
env OLLAMA_HOST=http://127.0.0.1:11435 uv run pytest tests/unit/test_yamls.py bda_eval/tests
```

### feature branch

```bash
cd /home/williambenitez1/Capstone_worktrees/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap
env OLLAMA_HOST=http://127.0.0.1:11435 uv run pytest tests/unit/test_yamls.py bda_eval/tests
```

## 7. Run The Standard Prompt-Lab Smoke Flow

Default smoke purpose:

- branch health and prompt-lab workflow parity
- **not** winner evaluation

Default seed image:

- `tests/data/tank.jpg`

Suggested output root:

- model branch:
  - `z_reference_docs/Prompt_Labs/3_gemma4-e4b/3_model__gemma4-e4b/experiments/runs/refresh_smoke/runNN_<timestamp>/`
- feature branch:
  - `z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/refresh_smoke/runNN_<timestamp>/`

### model branch smoke export

```bash
cd /home/williambenitez1/Capstone_worktrees/3_model__gemma4-e4b
env OLLAMA_HOST=http://127.0.0.1:11435 uv run bda-svc \
  --input tests/data/tank.jpg \
  --output /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3_model__gemma4-e4b/experiments/runs/refresh_smoke/runNN_<timestamp>/gemma_model_candidate
```

### model branch self-check

```bash
cd /home/williambenitez1/Capstone_worktrees/3_model__gemma4-e4b
uv run --package bda-eval python bda_eval/main.py \
  -r /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3_model__gemma4-e4b/experiments/runs/refresh_smoke/runNN_<timestamp>/gemma_model_candidate \
  -p /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3_model__gemma4-e4b/experiments/runs/refresh_smoke/runNN_<timestamp>/gemma_model_candidate \
  -o /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3_model__gemma4-e4b/experiments/runs/refresh_smoke/runNN_<timestamp>/eval_selfcheck \
  -i tests/data
```

### feature branch smoke export

```bash
cd /home/williambenitez1/Capstone_worktrees/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap
env OLLAMA_HOST=http://127.0.0.1:11435 uv run bda-svc \
  --input tests/data/tank.jpg \
  --output /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/refresh_smoke/runNN_<timestamp>/gemma_feature_candidate
```

### feature branch self-check

```bash
cd /home/williambenitez1/Capstone_worktrees/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap
uv run --package bda-eval python bda_eval/main.py \
  -r /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/refresh_smoke/runNN_<timestamp>/gemma_feature_candidate \
  -p /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/refresh_smoke/runNN_<timestamp>/gemma_feature_candidate \
  -o /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/refresh_smoke/runNN_<timestamp>/eval_selfcheck \
  -i tests/data
```

## 8. Interpret Failures Correctly

Use the same failure classes as the main workflow:

- environment/dependency mismatch
- branch-shape drift
- missing reusable capability in the model branch
- runtime host/config mismatch

For Gemma specifically:

- if the branch points at `qwen3-vl:8b-instruct` during a Gemma smoke run, that
  is a tracked config/default problem
- if the host override is omitted and the branch fails because Gemma 4 is not
  available on the default Ollama port, that is a checklist/host-usage error,
  not a prompt regression

## 9. Push Rebases Only After Parity Validation

Only if these branches already exist on origin **and** parity validation is
complete:

### model branch

```bash
git push --force-with-lease origin model/gemma4-e4b
```

### feature branch

```bash
git push --force-with-lease origin feat/gemma4-e4b/qwen-v009-workflow-bootstrap
```

## 10. Refresh The Active Gemma Baseline Only If Required

If the baseline-refresh gate says yes, refresh the active Gemma baseline files
and rerun the first baseline in the Gemma prompt lab.

Current active lab root:

- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/`

## 11. Post-Refresh Verification

Expected completion standard:

- `main` mirror is aligned
- model and feature worktrees are clean after the rebase
- workspace packages are synced
- the shared test slice passed
- model and feature worktrees both passed the prompt-lab smoke flow
- docs were updated
- the baseline was rebuilt only if required by the baseline gate

## 12. Update Docs

Update at least:

- `z_reference_docs/WORKING_CHANGELOG.md`
- `z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
- `z_reference_docs/REFERENCE_MASTER_INDEX.md` if routing changed
- the Gemma model/feature branch metadata docs if the branch contract changed
- the active Gemma prompt-lab README if the baseline changed
