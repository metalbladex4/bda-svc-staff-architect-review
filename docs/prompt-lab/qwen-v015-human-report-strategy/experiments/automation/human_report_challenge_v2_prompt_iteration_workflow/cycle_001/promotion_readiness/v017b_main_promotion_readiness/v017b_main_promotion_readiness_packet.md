# v017b Main Promotion Readiness Packet

## Status

`v017b_group_box_rejection` is ready for user review as the current Qwen
promotion candidate.

This packet does not perform promotion. It defines the safest next adoption
path if the user later approves moving v017b toward `main`.

## Current Evidence

The Qwen `1.2` worktree has already adopted v017b as its local default runtime
through the model-line overlay:

`src/bda_svc/pipeline/overlays/model_lines/qwen3-vl-8b-instruct.yaml`

Runtime facts:

- model line: `qwen3-vl:8b-instruct`
- detector backend: `vlm_prompt_detector`
- model-line overlay id: `qwen3-vl-8b-instruct-model-line-v017b-defaults-v1`
- resolved config hash:
  `fcbbbfa826940991b7e20cb5f4667609e3a5ecc01ee369d0c87545baf6a71998`
- experiment overlays during post-adoption replay: none
- v017b prompt hash:
  `331bf0d27d08f62f153050c9bf20ab0a2b76d63828974217a7a24d3964ab2259`

Post-adoption all-current/no-101 replay:

- pack: `human_report_challenge_v2_all_current_117_no101`
- images: `117`
- matches: `158`
- false negatives: `61`
- false positives: `18`
- delta versus pre-adoption all-current: `+0` matches, `+0` false negatives,
  `-7` false positives
- case `101`: excluded from forward evaluation
- case `155`: `2` matches, `0` false negatives, `0` false positives
- case `166`: `1` match, `0` false negatives, `0` false positives

Other post-adoption checks:

- changed-source sanity: `10` matches, `2` false negatives, `0` false positives
- updated-report smoke: `23` matches, `8` false negatives, `1` false positive
- office-negative abstention: `1/1` abstention correct and `0`
  negative-scene false positives
- hinge 11/no-101: `22` matches, `23` false negatives, `15` false positives

## Main Promotion Surface Finding

The active `main` checkout does not currently have the Qwen `1.2` worktree's
runtime-overlay machinery.

Current `main` runtime prompt surface:

- `/home/williambenitez1/Capstone/src/bda_svc/pipeline/config.yaml`
- direct prompt field: `prompts.detect_objects`
- current main prompt hash:
  `152e07ee34fb792aa79d30b8ad5dcfc194ef9932f99c60bd70a0a92b24033683`

Current Qwen `1.2` worktree runtime prompt surface:

- `src/bda_svc/pipeline/config.yaml` points at a model-line overlay
- `src/bda_svc/pipeline/overlays/model_lines/qwen3-vl-8b-instruct.yaml`
  contains the adopted v017b prompt
- worktree v017b prompt hash:
  `331bf0d27d08f62f153050c9bf20ab0a2b76d63828974217a7a24d3964ab2259`

This means there are two possible promotion paths.

## Promotion Path Options

### Option A: Prompt-Only Main Promotion

Recommended.

Change only `main`:

- `src/bda_svc/pipeline/config.yaml`

Specifically, replace the current `prompts.detect_objects` block with the exact
v017b prompt text from:

`docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/candidates/v017b/overlay.yaml`

or from the adopted worktree model-line overlay:

`src/bda_svc/pipeline/overlays/model_lines/qwen3-vl-8b-instruct.yaml`

Why this is safer:

- it keeps the promotion focused on prompt engineering
- it avoids bringing unreviewed runtime-overlay infrastructure into `main`
- it matches the current `main` runtime shape
- it is easy to inspect, test, and roll back
- it avoids mixing a prompt promotion with a platform/runtime architecture
  change

Limit:

- the exact worktree resolved config hash will not carry to `main`, because
  `main` does not resolve model-line overlays. The portable equality check is
  the v017b prompt hash and replay behavior, not the worktree resolved config
  hash.

### Option B: Runtime-Overlay Infrastructure Promotion

Not recommended in the same wave.

This would promote the broader worktree runtime-resolution system into `main`,
including files such as:

- `src/bda_svc/pipeline/runtime_config.py`
- `src/bda_svc/pipeline/overlays/model_lines/qwen3-vl-8b-instruct.yaml`
- runtime-related edits in `src/bda_svc/pipeline/model.py`
- config/runtime metadata tests and prompt-lab integrity tests
- possibly additional worktree support files already present in the Qwen `1.2`
  branch

Why this is larger:

- it changes runtime architecture, not just the prompt
- it touches more code and tests
- it has a bigger review burden
- it needs its own source-code promotion plan and regression pass

Choose this only if the project wants model-line overlays as a product feature,
not merely because v017b won the prompt lane.

### Option C: Keep Worktree-Only

This keeps v017b as the active Qwen `1.2` worktree candidate and does not move
anything to `main`.

Use this if the team wants one more visual review, poster/report discussion, or
additional non-101 holdout review before product adoption.

## Recommended Main Promotion Plan

If the user approves main promotion, use Option A.

1. Confirm `main == origin/main` after `git fetch origin --prune`.
2. Confirm no tracked or staged diff in `/home/williambenitez1/Capstone`.
3. Back up `src/bda_svc/pipeline/config.yaml`.
4. Replace only `prompts.detect_objects` with the exact v017b prompt.
5. Preserve required placeholders:
   - `{categories}`
   - `{detection_guidance}`
   - `{bbox_format}`
   - `{bbox_scale}`
6. Run static validation:
   - YAML parse
   - `uv run pytest tests/unit/test_yamls.py`
   - `uv run pytest tests/unit/test_model.py`
   - `uv run bda-svc -h`
7. Run promotion smoke:
   - changed-source sanity
   - updated-report smoke
   - office-negative abstention
8. Run all-current/no-101 replay on `main`.
9. Compare against the worktree adopted-runtime replay:
   - expected reference: `158` matches, `61` false negatives, `18` false
     positives across `117` images
   - case `155` must remain positive-control safe
   - case `166` must remain positive-control safe
   - case `101` remains excluded from pass/fail evaluation
10. Stop for user review before commit if the main replay materially drifts:
    - matches below `156`
    - false negatives above `63`
    - false positives above `21`
    - `155` or `166` fails as a positive control
    - office-negative abstention fails
11. If gates pass, write a `main` promotion report and update appropriate live
    docs.
12. Only after user approval, commit the main prompt change.

## What Would Move Toward Main

Recommended prompt-only path:

- move: v017b prompt text into `main`
  `src/bda_svc/pipeline/config.yaml`
- do not move: Qwen `1.2` runtime-overlay files
- do not move: prompt-lab run outputs
- do not move: Graphify generated outputs
- do not move: Mem0 memory
- do not move: worktree-only helper scripts unless separately approved

## What Stays Local

- `docs/prompt-lab/` experiment packages and run outputs
- `human_report_challenge_v2` automation evidence packages
- v017b/v017d comparison artifacts
- post-adoption runtime replay outputs
- Qwen `1.2` overlay infrastructure unless separately approved
- local Graphify/project-brain outputs
- Mem0 advisory memory

## Rollback

For the recommended prompt-only promotion:

1. Restore `src/bda_svc/pipeline/config.yaml` from the backup made before the
   prompt replacement.
2. If already committed locally, use a normal revert commit.
3. Re-run YAML parse and `uv run pytest tests/unit/test_yamls.py`.
4. Re-run one office-negative abstention smoke if the failed adoption reached
   runtime testing.

For the larger runtime-overlay path:

1. Revert the full promotion commit rather than hand-removing files.
2. Re-run runtime config tests and model tests.
3. Re-run all changed runtime smoke packs.

## Current Recommendation

Proceed to a separate user-approved Option A implementation wave:

`v017b_prompt_only_main_promotion`

Do not start that wave automatically from this packet. The next approval should
explicitly allow editing `/home/williambenitez1/Capstone/src/bda_svc/pipeline/config.yaml`.
