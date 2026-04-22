# Qwen Worktree Update Checklist

This is the copy-paste checklist for the current Qwen branch line when
`upstream/main` moves again.

Use it together with:

- `z_reference_docs/GIT_WORKTREE_UPDATE_WORKFLOW.md`

This checklist now assumes the refresh is **not** complete until the active
Qwen model and feature worktrees both pass the practical prompt-lab smoke flow.

## Current Branch Line

- clean mirror:
  - `/home/williambenitez1/Capstone`
  - branch: `main`
- model worktree:
  - `/home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct`
  - branch: `model/qwen3-vl-8b-instruct`
- feature worktree:
  - `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`
  - branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`

## 0. Preflight

Check all three worktrees first.

### clean mirror

```bash
cd /home/williambenitez1/Capstone
git status --short --branch
```

### model worktree

```bash
cd /home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct
git status --short --branch
```

### feature worktree

```bash
cd /home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement
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

## 2. Decide Whether `v000` Must Be Refreshed

Answer these:

- did live prompt text change?
- did doctrine wording change?
- did inference/runtime behavior change?

If all three answers are no, and the delta is only eval/docs/tests/CI/container
work:

- do **not** refresh branch-aware `v000`

If any answer is yes:

- refresh branch-aware `v000` after the rebase chain completes

## 3. Rebase The Model Branch

```bash
cd /home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct
git fetch upstream origin --prune
git rebase main
```

If conflicts happen:

- resolve them here first
- run the relevant checks
- continue the rebase

## 4. Rebase The Feature Branch

```bash
cd /home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement
git fetch upstream origin --prune
git rebase model/qwen3-vl-8b-instruct
```

Do not rebase this feature branch directly onto `main`.

## 5. Sync Workspace Packages Before Validation

Run this in both the model and feature worktrees:

### model branch

```bash
cd /home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct
uv sync --all-packages
```

### feature branch

```bash
cd /home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement
uv sync --all-packages
```

## 6. Run The Shared Sanity Tests

Run this in both the model and feature worktrees:

### model branch

```bash
cd /home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct
uv run pytest tests/unit/test_yamls.py bda_eval/tests
```

### feature branch

```bash
cd /home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement
uv run pytest tests/unit/test_yamls.py bda_eval/tests
```

## 7. Run The Standard Prompt-Lab Smoke Flow

Default smoke purpose:

- branch health and prompt-lab workflow parity
- **not** winner evaluation

Default seed image:

- `tests/data/tank.jpg`

Suggested output root:

- model branch:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1_model__qwen3-vl-8b-instruct/experiments/runs/refresh_smoke/runNN_<timestamp>/`
- feature branch:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/refresh_smoke/runNN_<timestamp>/`

### model branch smoke export

```bash
cd /home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct
uv run bda-svc \
  --input tests/data/tank.jpg \
  --output /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1_model__qwen3-vl-8b-instruct/experiments/runs/refresh_smoke/runNN_<timestamp>/qwen_model_candidate
```

### model branch self-check

```bash
cd /home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct
uv run --package bda-eval python bda_eval/main.py \
  -r /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1_model__qwen3-vl-8b-instruct/experiments/runs/refresh_smoke/runNN_<timestamp>/qwen_model_candidate \
  -p /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1_model__qwen3-vl-8b-instruct/experiments/runs/refresh_smoke/runNN_<timestamp>/qwen_model_candidate \
  -o /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1_model__qwen3-vl-8b-instruct/experiments/runs/refresh_smoke/runNN_<timestamp>/eval_selfcheck \
  -i tests/data
```

### feature branch smoke export

```bash
cd /home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement
uv run bda-svc \
  --input tests/data/tank.jpg \
  --output /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/refresh_smoke/runNN_<timestamp>/qwen_feature_candidate
```

### feature branch self-check

```bash
cd /home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement
uv run --package bda-eval python bda_eval/main.py \
  -r /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/refresh_smoke/runNN_<timestamp>/qwen_feature_candidate \
  -p /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/refresh_smoke/runNN_<timestamp>/qwen_feature_candidate \
  -o /home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/refresh_smoke/runNN_<timestamp>/eval_selfcheck \
  -i tests/data
```

## 8. Interpret Failures Correctly

If a smoke or test step fails, classify the failure before deciding what to do.

### Environment/dependency mismatch

Signs:

- missing Python packages
- test import failures
- branch starts working after `uv sync --all-packages`

Action:

- treat as environment sync work, not as a prompt or branch-history failure

### Branch-shape drift

Signs:

- rebase succeeded, but the branch lacks behavior expected of an active root
- example:
  - model branch cannot run the same eval/self-check path as the feature branch

Action:

- inspect whether reusable infrastructure is trapped in a feature branch

### Missing reusable capability in the model branch

Signs:

- feature branch passes the smoke flow
- model branch fails for a reusable reason

Action:

- promote that reusable work into `model/qwen3-vl-8b-instruct`
- then rerun the model-branch smoke flow

### Runtime/config mismatch

Signs:

- wrong model tag
- wrong Ollama host
- wrong tracked config for the model line

Action:

- treat as a tracked config/default problem, not just a transient smoke failure

## 9. Push Rebases Only After Parity Validation

Only if these branches already exist on origin **and** parity validation is
complete:

### model branch

```bash
git push --force-with-lease origin model/qwen3-vl-8b-instruct
```

### feature branch

```bash
git push --force-with-lease origin feat/qwen3-vl-8b-instruct/two-pass-refinement
```

Do **not** push rebased branches to origin immediately after the rebase if the
smoke flow has not been validated yet.

## 10. Refresh The Branch-Aware Baseline Only If Required

If the baseline-refresh gate says yes, update:

- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/baseline/config.pipeline-baseline.yaml`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/versions/v000_baseline.prompts.yaml`

Then run a fresh baseline and update the branch-aware run manifest/log.

## 11. Post-Refresh Verification

### verify `main`

```bash
cd /home/williambenitez1/Capstone
git rev-list --left-right --count main...origin/main
git rev-list --left-right --count main...upstream/main
git status --short --branch
```

Expected:

- both counts are `0 0`
- `main` is clean

### verify model worktree

```bash
cd /home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct
git status --short --branch
```

### verify feature worktree

```bash
cd /home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement
git status --short --branch
```

Expected completion standard:

- the rebased branches are clean
- workspace packages are synced
- the shared test slice passed
- model and feature worktrees both passed the prompt-lab smoke flow
- docs were updated
- `v000` was refreshed only if required by the baseline gate

## 12. Update Docs

Update at least:

- `z_reference_docs/WORKING_CHANGELOG.md`
- `z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
- `z_reference_docs/REFERENCE_MASTER_INDEX.md` if routing changed
- the active model/feature branch metadata docs if the branch contract changed
- the branch-aware prompt lab if the baseline changed

## Promotion Reminder

If a feature-branch customization is now stable and reusable across future
Qwen feature branches, promote it into:

- `model/qwen3-vl-8b-instruct`

Then rebase the feature branch onto the updated model branch later.
