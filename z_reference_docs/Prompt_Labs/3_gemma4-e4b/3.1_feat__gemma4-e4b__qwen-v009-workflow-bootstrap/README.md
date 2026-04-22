# 3.1 Feature Lab

This is the active Gemma bootstrap lab for:

- branch: `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- model line: `gemma4:e4b`
- parent branch: `model/gemma4-e4b`
- parent branch head at creation: `b8fbdb3`
- current upstream-aligned infra base after worktree refresh: `e7a22a9`

## Purpose

This lab exists to answer the first Gemma question cleanly:

- can Gemma 4 E4B adopt the active Qwen `v009` workflow shape and stay inside
  the current BDA runtime contract without opening a new architecture path?

## Sync Status

- The active prompt-evidence anchor for this lab is now the rebuilt
  post-`e7a22a9` Gemma `v000` run recorded under:
  - `experiments/runs/v000/run02_2026-04-19_185856_EDT/`
- The earlier first-live Gemma `v000` run recorded under:
  - `experiments/runs/v000/run01_2026-04-17_134308_EDT/`
  is now preserved as pre-`e7a22a9` historical evidence.
- On `2026-04-17`, the Gemma model and feature worktrees were refreshed
  through upstream `main` commit `c19940a` using the documented worktree
  refresh workflow.
- That upstream delta only changed `.github/workflows/ci.yml` and
  `docker/Dockerfile`, so this lab did **not** rebuild `v000` after the
  refresh.
- On `2026-04-19`, the Gemma model and feature worktrees were refreshed again
  through upstream `main` commit `e7a22a9`.
- That newer delta changed live export and detect-prompt behavior, so the
  Gemma line can no longer assume the old `v000` evidence chain is still the
  right anchor for post-refresh behavior.
- Later on `2026-04-19`, the Gemma feature branch completed a full six-case
  `v000` reset rebuild on the current `e7a22a9` repo base.
- Later on `2026-04-17`, branch hygiene was completed by rebasing this feature
  branch onto the hardened `model/gemma4-e4b` branch and rerunning the shared
  prompt-lab smoke recipe.
- Working rule:
  - keep the first-live Gemma `run01` evidence chain intact as historical
    pre-refresh context
  - treat `e7a22a9` as the current inherited repo base
  - the earlier `c19940a` move did not require a baseline rebuild
  - the newer `e7a22a9` move did change prompt/runtime semantics, so the
    trustworthy Gemma read now starts from the rebuilt `run02` baseline
  - do not open `v001` until the reset result is digested and the current
    detect-contract effect is reconsidered
- Current local branch-shape note:
  - after the hygiene rebase, this feature branch now matches the hardened
    Gemma model branch in tracked code
  - that is expected for now because the reusable Gemma bootstrap baseline
    commit was already promoted upward into the model root

## Folder Map

- `baseline/`
  Baseline config snapshot for the Gemma bootstrap line.
- `experiments/versions/`
  Version snapshots for the Gemma line.
- `experiments/runs/`
  Baseline and candidate run artifacts.
- `experiments/validation/`
  The inherited comparison and validation pack for Gemma-vs-Qwen work.
- `experiments/winners/`
  Reserved for confirmed winners only.

## Bootstrap Rules

- Start from the active Qwen `v009` prompt semantics, not from `origin/main`
  prompt wording.
- Treat `gemma4:e4b` as the active model and `gemma4:e2b` as comparison-only.
- Keep `thinking` disabled for the first baseline.
- Reuse the Qwen seed pack for comparability instead of inventing a new test
  pack first.

## Current Active Read

- `v000` is the semantic port of the active Qwen `v009` stack into the Gemma
  4 E4B model line.
- The first goal remains contract stability and behavioral readout, not
  immediate prompt reinvention.
- The current active Gemma `v000` anchor is now the rebuilt reset run under:
  - `experiments/runs/v000/run02_2026-04-19_185856_EDT/`
- The earlier `run01_2026-04-17_134308_EDT` baseline remains preserved as
  pre-refresh history, not as the active anchor for the current repo base.
- Runtime note:
  - the system Ollama install is still `0.15.2`
  - Gemma 4 was brought up through a user-local Ollama `0.21.0` runtime on
    `127.0.0.1:11435`
  - this worked without tracked repo changes because `bda-svc` already honors
    `OLLAMA_HOST`
- Reset read on the current repo base:
  - `tank_pressure`: regressed hard from `DESTROYED / PROBABLE` to
    `object_not_found / NOT APPLICABLE`
  - `destroyed_tank15`: clean hold at `DESTROYED / PROBABLE`, matching the
    first live Gemma baseline
  - `operational_tank4`: regressed from `NO DAMAGE / CONFIRMED` to
    `DAMAGED / PROBABLE`
  - `destroyed_building4`: still unacceptable; two targets returned, but both
    are undercalled at `MODERATE DAMAGE / CONFIRMED` with overlapping left-side
    boxes
  - `operational_building7`: clean category/confidence hold at
    `NO DAMAGE / CONFIRMED`, with geometry drift only
  - `office_negative`: clean `object_not_found` negative behavior still holds
- So the rebuilt Gemma reset result is:
  - the `e7a22a9` change did not just alter the tank smoke seed
  - it materially shifted the broader Gemma behavior read
  - the old `run01` conclusions are not portable onto the current repo base
  - the next move should pause before `v001` and reconsider the inherited
    detect-contract effect first
- a follow-up two-case detection diagnostic rerun now lives under:
  - `experiments/runs/detect_diagnostics/run01_2026-04-19_193323_EDT/`
- that diagnostic rerun confirmed:
  - `tank_pressure` returned raw `{"detections":[]}` from Gemma
  - the `tank_pressure` collapse was not caused by parse failure
  - the `tank_pressure` collapse was not caused by invalid-target filtering
  - the `tank_pressure` collapse was not caused by invalid-bbox filtering
  - `operational_tank4` still returned one valid detection, so its regression
    is now localized to bbox placement and/or downstream assessment
- working implication:
  - the explicit empty-detections instruction is now the leading causal suspect
    for the Gemma tank abstention
  - the next Gemma move should be a narrow detect-contract adjustment test,
    not an immediate broad `v001` prompt cycle
- that narrow detect-only follow-up now exists under:
  - `experiments/runs/v001/run01_2026-04-19_194343_EDT/`
- `v001` changes only the no-target detection instruction and keeps the
  temporary detection debug hook active
- `v001` run01 recovered both tank cases:
  - `tank_pressure` moved from raw `{"detections":[]}` and
    `object_not_found / NOT APPLICABLE` back to a real
    `military_equipment` detection with `DESTROYED / PROBABLE`
  - `operational_tank4` recovered from `DAMAGED / PROBABLE` back to
    `NO DAMAGE / CONFIRMED`
- working implication:
  - the no-target detect instruction is not just correlated with the Gemma
    tank regression; it is now demonstrated to be a high-leverage control
    point for the line
  - `v001` is the active next candidate, but it is still narrow evidence and
    should not be promoted until it is checked against the held controls and
    known building failure cases
- that broader `v001` follow-up now exists under:
  - `experiments/runs/v001/run02_2026-04-19_195511_EDT/`
- `v001` run02 confirmed:
  - `tank_pressure` stayed recovered at `DESTROYED / PROBABLE`
  - `destroyed_tank15` held exactly
  - `operational_tank4` stayed recovered at `NO DAMAGE / CONFIRMED`
  - `operational_building7` held at `NO DAMAGE / CONFIRMED`
  - `office_negative` held cleanly as `object_not_found / NOT APPLICABLE`
  - `destroyed_building4` improved from two overlapping left-side moderate
    outputs to two separate building detections, but still undercalls the left
    building at `MODERATE DAMAGE / CONFIRMED`
- current working implication:
  - `v001` is now the strongest Gemma direction so far on the current repo
    base
  - the next Gemma move should iterate from `v001`, not from the rebuilt
    `v000`
  - the main remaining Gemma problem is now building-severity calibration,
    especially on `destroyed_building4`
- that focused building-severity follow-up now exists under:
  - `experiments/runs/v002/run01_2026-04-19_200142_EDT/`
- `v002` changed only `assess_damage` and kept the `v001` detect behavior
  intact
- `v002` run01 confirmed:
  - `destroyed_building4` improved from
    `MODERATE DAMAGE / CONFIRMED` + `DESTROYED / CONFIRMED`
    to
    `SEVERE DAMAGE / PROBABLE` + `DESTROYED / PROBABLE`
  - `tank_pressure` held at `DESTROYED / PROBABLE`
  - `operational_tank4` held at `NO DAMAGE / CONFIRMED`
  - `operational_building7` held at `NO DAMAGE / CONFIRMED`
- current working implication:
  - `v002` is now the strongest Gemma candidate so far
  - the next Gemma move should be a broader `v002` follow-up on the full
    inherited pack before deciding whether to replace `v001` as the active
    direction
- that broader `v002` follow-up now exists under:
  - `experiments/runs/v002/run02_2026-04-19_201813_EDT/`
- `v002` run02 confirmed:
  - `tank_pressure` held at `DESTROYED / PROBABLE`
  - `destroyed_tank15` held at `DESTROYED / PROBABLE`
  - `operational_tank4` held at `NO DAMAGE / CONFIRMED`
  - `operational_building7` held at `NO DAMAGE / CONFIRMED`
  - `office_negative` held exactly as `object_not_found / NOT APPLICABLE`
  - `destroyed_building4` kept two-target separation and improved to
    `SEVERE DAMAGE / PROBABLE` plus `DESTROYED / PROBABLE`
- current working implication:
  - `v002` is now the strongest Gemma direction so far on the current repo
    base
  - `v002` should now be treated as the active Gemma direction
  - the active next Gemma work should iterate from `v002`, not `v001`

## Visual Review Path

Keep the same review-artifact workflow used on the Qwen line:

1. run `bda-svc`
2. run `bda_eval`
3. inspect overlays, crops, and `bbox_review_sheet.jpg`

## Branch Hygiene Smoke Confirmation

The post-refresh, post-hardening branch-hygiene smoke run is now recorded at:

- `experiments/runs/branch_hygiene/run01_2026-04-17_231500_EDT/`

That run confirmed this rebased feature branch still completes the practical
prompt-lab loop cleanly after being rebound onto the hardened Gemma model
branch:

- `uv run pytest tests/unit/test_yamls.py bda_eval/tests`
- `bda-svc` export on `tests/data/tank.jpg` using
  `OLLAMA_HOST=http://127.0.0.1:11435`
- `bda_eval` self-check with saved artifacts

Working implication:

- the Gemma bootstrap line remains ready for prompt-lab work
- branch hygiene by itself did not require a new prompt baseline
- the later `e7a22a9` repo-base change was the event that forced the rebuilt
  `run02` baseline

## `e7a22a9` Refresh Smoke Result

The next post-refresh smoke run is now recorded at:

- `experiments/runs/refresh_smoke/run02_2026-04-19_173039_EDT/`

That run confirmed:

- `uv run pytest tests/unit/test_yamls.py bda_eval/tests` still passed
- `bda-svc` export on `tests/data/tank.jpg` still worked against
  `OLLAMA_HOST=http://127.0.0.1:11435`
- but the refreshed detect contract now drove the Gemma export to:
  - `target_type = object_not_found`
  - `damage_category = NOT APPLICABLE`
  on the standard tank smoke seed
- because `bda_eval` still does not cleanly score `NOT APPLICABLE`, the
  usual self-check did not close on that smoke run

Working implication:

- this is not just an infra refresh for the Gemma line
- the line did need a fresh post-`e7a22a9` baseline, and that reset is now
  recorded under `experiments/runs/v000/run02_2026-04-19_185856_EDT/`
- the older `run01` baseline now remains preserved as historical pre-refresh
  evidence only

## Post-`e7a22a9` `v000` Reset Result

The rebuilt reset run is now recorded at:

- `experiments/runs/v000/run02_2026-04-19_185856_EDT/`

That run confirmed:

- `uv sync --all-packages` completed cleanly
- `uv run pytest tests/unit/test_yamls.py bda_eval/tests` still passed
- the full six-case inherited comparison pack reran successfully against the
  current tracked Gemma config
- `destroyed_tank15`, `operational_building7`, and `office_negative` held
  acceptably
- `tank_pressure` collapsed to `object_not_found / NOT APPLICABLE`
- `operational_tank4` regressed to `DAMAGED / PROBABLE`
- `destroyed_building4` still undercalled severity and is not yet trustworthy

Additional eval note:

- the office negative case still does not produce a normal evaluation CSV
  because `bda_eval` logs `NOT_APPLICABLE` as unknown, even though it now
  exits `0` and still emits review artifacts

Working implication:

- the reset run becomes the active Gemma `v000` anchor for the current repo
  base
- the older `run01` remains preserved for historical comparison only
- the next Gemma move should not be `v001` yet
- first reconsider the inherited detect-contract effect, because the current
  Gemma line lost two of the stronger equipment behaviors that originally held
