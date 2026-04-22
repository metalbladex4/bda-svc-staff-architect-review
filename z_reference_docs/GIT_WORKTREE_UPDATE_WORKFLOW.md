# Git / Worktree Update Workflow

This document defines the safe default workflow for bringing new
`upstream/main` changes into this repo **without losing or trampling the custom
work we are doing in model and feature worktrees**.

It is the operating procedure for this branch structure:

- `main`
- `snapshot/<date>-...`
- `model/<model-slug>`
- `feat/<model-slug>/<topic>`

## Why This Exists

The old pattern of doing active work on `main` made upstream syncs stressful.
Every new pull risked colliding with local experimental changes.

The new structure fixes that by separating concerns:

- `main` stays boring
- model and feature work lives in worktrees
- `z_reference_docs` stays centralized and local-only

This workflow tells us how to update that structure safely when `upstream/main`
moves again.

## What This Workflow Guarantees

Used correctly, this workflow guarantees:

- a safe refresh order:
  - `main`
  - `model/<model-slug>`
  - `feat/<model-slug>/<topic>`
- a documented gate for deciding whether branch-aware `v000` must be rebuilt
- a required post-refresh validation pass instead of treating a clean rebase as
  the end of the job
- an explicit rule for when rebased branches may be pushed remotely

This means the workflow is not only about rebasing safely. It also defines the
minimum validation needed before we call the refresh complete.

## What This Workflow Does Not Guarantee Automatically

Even if all rebases are clean, this workflow does **not** automatically
guarantee:

- workspace/environment parity
- model-branch reusable capability parity
- prompt-lab smoke parity across all active worktrees
- safe remote push timing after rebases

Those outcomes must be checked deliberately in the validation phase.

## Branch Roles

These are conventions, not special Git branch types.

### `main`

- exact mirror of `upstream/main`
- `origin/main` should match it exactly
- no active feature/model experimentation should live here

### `snapshot/<date>-...`

- one-time safety branch
- used when we need to preserve a local line before a structural change
- not the normal place to continue new work

### `model/<model-slug>`

- long-lived branch for one model line
- holds reusable customizations for that model line
- should absorb upstream changes before its child feature branches do
- is expected to remain a **smoke-capable reusable root**, not only an ancestry
  placeholder

### `feat/<model-slug>/<topic>`

- short-lived branch for one focused workstream
- branched from the relevant `model/<model-slug>`
- may contain unique experimental or implementation work not yet promoted upward

In plain language:

- **model branch** = shared line for one model family
- **feature branch** = one narrower task under that model family

## Core Rules

1. Never do active development on `main`.
2. Never update worktrees while they contain uncommitted work.
3. If a `model/...` or `feat/...` worktree has tracked changes, make a
   checkpoint commit before any rebase.
4. Refresh branches in this order:
   - `main`
   - `model/<model-slug>`
   - `feat/<model-slug>/<topic>`
5. Rebase child branches onto their parent branch, not directly onto `main`
   or `upstream/main`.
6. Only push rebased non-`main` branches with `--force-with-lease` if needed.
7. Keep `z_reference_docs` centralized at:
   - `/home/williambenitez1/Capstone/z_reference_docs`
8. Do not call a refresh complete until all active model and feature worktrees
   pass the same practical prompt-lab smoke flow, unless a branch is
   intentionally documented as non-parity.
9. For this repo, the default is now:
   - **no intentional non-parity for active model lines**

## Safe Default Update Order

When `upstream/main` has new changes:

### Step 0. Check whether any worktree is dirty

Do this first for:

- `/home/williambenitez1/Capstone`
- every active `model/...` worktree
- every active `feat/...` worktree

Command pattern:

```bash
git status --short --branch
```

If a `model/...` or `feat/...` worktree has tracked changes:

- stage and commit a checkpoint on that branch
- do not rely on stash as the normal safety mechanism

If `main` somehow has tracked changes:

- stop
- do not refresh anything else until that is understood and cleaned up
- `main` is supposed to remain boring and mirrored

Checkpoint message pattern:

```bash
checkpoint: before upstream refresh to <new-upstream-sha>
```

Why this is mandatory:

- checkpoint commits survive rebases more predictably than ad hoc stash usage
- they make recovery easier if conflict resolution goes badly

### Step 1. Refresh the clean mirror on `main`

Use the clean main checkout:

- `/home/williambenitez1/Capstone`

Commands:

```bash
git fetch upstream origin --prune
git switch main
git merge --ff-only upstream/main
git push origin main
```

Expected result:

- local `main` == `origin/main` == `upstream/main`

If `git merge --ff-only upstream/main` fails:

- stop
- do not improvise on `main`
- inspect why the branch is not a clean fast-forward first

### Step 2. Decide whether the upstream delta changes the active baseline

Review the upstream delta before rebasing child branches.

Questions to answer:

1. Did live prompt text change?
2. Did doctrine wording change?
3. Did runtime behavior change?
4. Did only evaluation/docs/tests change?

Rule:

- if live prompt/runtime/doctrine changed materially:
  - refresh the active branch-aware `v000` baseline after rebasing
- if the delta is only eval/docs/tests/CI/container work:
  - usually no prompt-baseline reset is required

Baseline refresh gate:

- `YES` refresh branch-aware `v000` if any answer below is yes:
  - did live prompt text change?
  - did doctrine wording change?
  - did inference/runtime behavior change?
- `NO` refresh branch-aware `v000` if the delta is only:
  - eval changes
  - docs
  - tests
  - CI/workflow changes
  - Docker/container changes
  - branch-structure metadata

Important distinction:

- baseline refresh is a **prompt/runtime meaning** decision
- post-refresh parity validation is a **branch usability** decision

They are related, but they are not the same decision.

### Step 3. Rebase the model branch onto the refreshed `main`

Use the model worktree:

- `/home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct`

Commands:

```bash
git fetch upstream origin --prune
git rebase main
```

Absolute parent-child rule:

- `main` only fast-forwards from `upstream/main`
- `model/<model-slug>` rebases onto `main`
- `feat/<model-slug>/<topic>` rebases onto its `model/<model-slug>`
- feature branches do **not** rebase directly onto `main`

Why model branch first:

- this is where reusable model-line customizations should converge
- resolving conflicts here once is better than resolving the same upstream
  conflict separately in every feature branch

If conflicts happen:

1. resolve them in the model branch worktree
2. run the relevant tests
3. continue the rebase

Only after the model branch is healthy should feature branches move.

### Step 4. Rebase each feature branch onto its parent model branch

Use the feature worktree:

- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`

Commands:

```bash
git fetch upstream origin --prune
git rebase model/qwen3-vl-8b-instruct
```

Why:

- feature branches inherit both:
  - the new upstream functionality from `main`
  - the current reusable model-line customizations from `model/...`

This is the main mechanism that preserves our unique work while still pulling
new upstream behavior forward.

## Standard Post-Refresh Smoke Recipe

After the rebases finish, the default parity recipe for each active model and
feature worktree is:

1. sync workspace packages
2. run the shared yaml/eval test slice
3. run one prompt-lab style `bda-svc` export on the default seed image
4. run one `bda_eval` self-check against that exported report folder
5. confirm artifact writeout into `z_reference_docs/Prompt_Labs/...`

Default commands:

```bash
uv sync --all-packages
uv run pytest tests/unit/test_yamls.py bda_eval/tests
uv run bda-svc --input tests/data/tank.jpg --output <run-output-dir>
uv run --package bda-eval python bda_eval/main.py \
  -r <run-output-dir> \
  -p <run-output-dir> \
  -o <eval-output-dir> \
  -i tests/data
```

Locked defaults:

- default seed image:
  - `tests/data/tank.jpg`
- default purpose:
  - branch health and prompt-lab workflow parity
  - **not** winner evaluation
- if a model line needs a non-default Ollama host, the branch checklist must
  state it explicitly
- if a branch cannot complete the common smoke recipe, that is a parity defect,
  not “close enough”

## What To Do With New Reusable Work

Not every change should stay trapped inside a feature branch forever.

Use this rule:

### Keep work in the feature branch when it is:

- highly experimental
- specific to one narrow task
- not yet stable enough to become part of the whole model line

### Promote work to the model branch when it is:

- reusable across multiple feature branches for the same model
- part of the stable working environment for that model line
- something we would want all future feature branches to inherit

Examples of likely model-branch material:

- model-specific prompt-lab tooling
- stable evaluation helpers
- model-specific config/runtime support

Examples of likely feature-branch-only material:

- one grounding tactic experiment
- one temporary prompt family
- one narrow refactor under active evaluation

Promotion method:

- rebase or cherry-pick the stable feature commits into `model/<model-slug>`
- then rebase child feature branches onto the updated model branch later

Default promotion rule:

- if a feature-branch change is stable and broadly useful for that model line,
  promote it upward into `model/<model-slug>`
- do not leave reusable branch infrastructure trapped in one feature branch if
  future feature branches will need it too

Parity-specific refinement:

- if a feature branch contains reusable infrastructure required for prompt-lab
  parity, promote it into the model branch before the refresh cycle is treated
  as fully closed
- examples:
  - evaluation behavior needed for smoke checks
  - workspace-package install behavior needed for tests
  - model-line config/runtime defaults needed for smoke exports

## Conflict Strategy

If a rebase conflicts:

### Small, obvious conflict

- resolve it directly in the current branch
- run targeted verification
- continue

### Large or risky conflict

- stop and create a checkpoint branch before continuing

Example pattern:

```bash
git branch checkpoint/<branch-slug>-before-conflict-resolution
```

Then resolve carefully.

### Never do this

- never `git reset --hard` just to “get unstuck”
- never overwrite `main` history casually
- never resolve conflicts in a feature branch first when the real shared
  conflict belongs in the model branch

## Remote Push Rules

### `main`

`main` should be pushed normally:

```bash
git push origin main
```

### `model/...` and `feat/...`

If the branch has been rebased and already exists on origin:

```bash
git push --force-with-lease origin <branch-name>
```

Use `--force-with-lease`, never plain `--force`.

Push timing rule:

- do **not** push rebased model/feature branches to origin until parity
  validation has passed
- refresh success alone is not enough reason to update the remote copy

If the branch is still local-only:

- no push is required unless we intentionally want a remote copy

## Documentation Rules After Every Upstream Refresh

After a meaningful upstream refresh:

1. update `z_reference_docs/WORKING_CHANGELOG.md`
2. update `z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
3. update `z_reference_docs/REFERENCE_MASTER_INDEX.md` if the routing changed
4. update the relevant branch-aware prompt lab if the active baseline changed
5. if live prompt/runtime changed, refresh the branch-aware `v000` baseline
6. update any active checklist or model-branch metadata docs if the branch
   contract or validation expectations changed

## Post-Refresh Validation Lanes

Treat post-refresh verification as four separate lanes:

### 1. Mirror Alignment

Confirm:

- local `main` == `origin/main` == `upstream/main`

### 2. Branch Ancestry

Confirm:

- each `model/<model-slug>` rebased cleanly onto `main`
- each `feat/<model-slug>/<topic>` rebased cleanly onto its model branch

### 3. Environment And Dependency Readiness

Confirm:

- workspace packages are synced where needed
- the shared yaml/eval test slice runs successfully

### 4. Prompt-Lab Smoke Parity

Confirm:

- every active model and feature worktree can complete the standard smoke
  recipe
- each one can write artifacts into `z_reference_docs/Prompt_Labs/...`
- any model-line-specific host override is documented and used where needed

## Failure Classification Matrix

When validation fails, classify the failure before deciding what to do next:

### Rebase conflict

- Git history or file-content conflict during rebase
- resolve in the current branch, following parent-first ordering

### Environment/dependency mismatch

- tests fail because the workspace environment is incomplete
- usually fixed with `uv sync --all-packages` or the equivalent documented sync

### Branch-shape mismatch

- the branch rebased cleanly but lacks behavior expected of an active root
- example:
  - missing `bda_eval` capability present in the active feature branch

### Model-branch missing reusable capability

- the feature branch works, but the model branch cannot complete the parity
  smoke flow
- this means reusable branch infrastructure is trapped too low and should be
  promoted upward

### Runtime host/config mismatch

- the branch points at the wrong model tag or wrong Ollama host for its line
- this is a tracked config/default problem, not just a transient test failure

## Completion Rule

The refresh is only **fully complete** when all of these are true:

1. refresh success:
   - local `main` == `origin/main` == `upstream/main`
   - model branches rebased cleanly onto `main`
   - feature branches rebased cleanly onto their parent model branches
2. validation success:
   - relevant tests passed
   - workspace/dependency sync issues are resolved
3. full parity completion:
   - every active model and feature worktree completed the standard prompt-lab
     smoke recipe
4. documentation success:
   - the required docs were updated
5. baseline correctness:
   - branch-aware `v000` was refreshed only if the baseline gate required it

Do not call the refresh “done” if rebases are clean but active worktrees still
fail parity validation.

## Post-Refresh Verification Block

The update is not complete until all of these are true:

1. local `main` == `origin/main` == `upstream/main`
2. `model/<model-slug>` rebased cleanly onto `main`
3. `feat/<model-slug>/<topic>` rebased cleanly onto its model branch
4. workspace packages were synced where needed
5. the shared yaml/eval test slice passed
6. every active model and feature worktree passed the standard prompt-lab smoke
   recipe
7. docs were updated
8. branch-aware `v000` was refreshed only if the baseline-refresh gate required
   it

## Quick Example For The Current Qwen Line

If `upstream/main` moves again, the safe sequence is:

### A. Refresh the clean mirror

In:

- `/home/williambenitez1/Capstone`

Run:

```bash
git fetch upstream origin --prune
git switch main
git merge --ff-only upstream/main
git push origin main
```

### B. Refresh the model line

In:

- `/home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct`

Run:

```bash
git status --short --branch
git rebase main
```

### C. Refresh the active feature line

In:

- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`

Run:

```bash
git status --short --branch
git rebase model/qwen3-vl-8b-instruct
```

### D. Update the branch-aware lab if needed

If upstream changed live prompt/runtime:

- refresh:
  - `baseline/config.pipeline-baseline.yaml`
  - `experiments/versions/v000_baseline.prompts.yaml`
- record a fresh baseline run in the branch-aware lab

### E. Verify the refresh

Run:

```bash
git rev-list --left-right --count main...origin/main
git rev-list --left-right --count main...upstream/main
git status --short --branch
```

And confirm:

- both `main...origin/main` and `main...upstream/main` report `0 0`
- the rebased worktree branch is clean
- `uv sync --all-packages` was run where needed
- the shared test slice passed
- the prompt-lab smoke flow passed for both the model and feature worktrees
- the docs and branch-aware baseline were updated only if needed

## Recommended Default For Us

The best default going forward is:

- keep `main` mirrored and clean
- keep model branches smoke-capable, not ancestry-only
- treat rebases, parity validation, and remote pushes as separate decisions
- keep reusable model-line work on `model/<model-slug>`
- keep active task work on `feat/<model-slug>/<topic>`
- checkpoint commit before rebasing
- rebase downward through the branch hierarchy
- refresh branch-aware `v000` only when the upstream delta actually changes the
  live baseline surface

This gives us the safest path to:

- absorb new upstream functionality
- preserve our custom work
- avoid the old confusion around local changes on `main`
