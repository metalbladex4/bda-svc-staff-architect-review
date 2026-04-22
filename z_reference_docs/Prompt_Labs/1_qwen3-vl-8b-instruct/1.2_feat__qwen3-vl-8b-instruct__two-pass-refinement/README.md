# 1.2 Feature Lab

This is the active branch-aware prompt lab for:

- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- creation base commit: `28e863b`
- current upstream-aligned infra base after worktree refresh: `e7a22a9`

## Purpose

This lab restarts the active evidence chain from the clean mirrored upstream
baseline after the git/worktree reset.

It exists so new prompt and grounding work can continue in a branch-aware
structure without mixing fresh `28e863b` evidence with the preserved legacy
main-branch lab.

## Sync Status

- The prompt-evidence anchor for this lab is still the fresh branch-aware
  `28e863b` baseline.
- On `2026-04-17`, the underlying model and feature worktrees were refreshed
  through upstream `main` commit `c19940a` using the documented worktree
  refresh workflow.
- That newer upstream delta only changed `.github/workflows/ci.yml` and
  `docker/Dockerfile`, so this lab did **not** rebuild `v000` from `c19940a`.
- On `2026-04-19`, the underlying model and feature worktrees were refreshed
  again through upstream `main` commit `e7a22a9`.
- That newer delta changed live export and detect-prompt behavior, so this line
  should now treat a fresh post-`e7a22a9` baseline rebuild as the next required
  step before folding newer prompt behavior into the same evidence chain.
- Later on `2026-04-17`, branch hygiene was completed by rebasing this feature
  branch onto the hardened `model/qwen3-vl-8b-instruct` branch and rerunning
  the shared prompt-lab smoke recipe.
- Working rule:
  - keep the existing `28e863b` prompt evidence chain intact
  - treat `e7a22a9` as the current inherited repo base under the branch
  - the earlier `c19940a` move did not require a baseline rebuild
  - the newer `e7a22a9` move does change live prompt/runtime semantics, so the
    next trustworthy post-refresh Qwen prompt read should start from a rebuilt
    baseline
- Current local remote-tracking nuance:
  - this rebased feature branch now diverges from
    `origin/feat/qwen3-vl-8b-instruct/two-pass-refinement`
  - any remote refresh should therefore be a deliberate
    `git push --force-with-lease`, not an automatic follow-up

## Folder Map

- `baseline/`
  Fresh config snapshot copied from `src/bda_svc/pipeline/config.yaml` at
  `28e863b`.
- `experiments/versions/`
  Prompt-version snapshots for this branch-aware line.
- `experiments/runs/`
  Baseline and candidate run artifacts.
- `experiments/winners/`
  Only accepted winners after they clearly earn promotion.

## Working Rule

- Treat the legacy lab under
  `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/`
  as preserved history.
- Treat this branch-aware lab as the fresh active line for new work on this
  feature branch.
- Rebuild `v000` from the clean `28e863b` runtime before trusting further
  prompt conclusions from the older `21deaf5`-anchored chain.
- Do not rebuild `v000` just because the branch ancestry moved to `c19940a`
  unless the upstream delta actually changes prompt/runtime meaning.

## Debug Note

This feature branch starts from clean `upstream/main`.

That means:

- the older local temporary `--debug-export-images` helper is not assumed here
- fresh baseline runs on this branch should be recorded as clean upstream-style
  runs unless we intentionally port debugging instrumentation forward later

## Visual Review Path

For this clean branch-aware line, bbox review should now prefer the upstream
evaluation path in `bda_eval` over the older temporary `bda-svc` debug-export
helper.

Current intended flow:

1. run `bda-svc` to produce the baseline and candidate JSON reports
2. run `bda_eval` on those report folders with the source image folder
3. use the emitted overlay images, crops, and `bbox_review_sheet.jpg` for
   prompt-grounding review

This keeps the visual review workflow anchored to tracked upstream evaluation
functionality while still supporting prompt-lab iteration.

When evaluation images come from
`/home/williambenitez1/Capstone/z_reference_docs/Data_set_Storage/`, it is also
acceptable to copy them into the per-run worktree/output folders and leave them
there as part of the saved run artifacts.

## Confirmed Smoke Test

The first clean-line `bda_eval` smoke test is now recorded at:

- `experiments/runs/layout_check/run02_2026-04-15_224230_EDT/`

That run confirmed the expected prompt-lab artifact layout is working from this
feature branch:

- root `bbox_review_sheet.jpg`
- `images_bbox_both/`
- `images_bbox_reference/`
- `images_bbox_predicted/`
- `images_crop_reference/`
- `images_crop_predicted/`
- `images_bbox_review/`

It also confirmed two important integration rules:

- bbox artifact generation should not hard-fail when `OLLAMA_API_KEY` is
  absent; `bda_eval` now skips LLMaaJ logic scoring and continues
- `bda_eval` can write directly into a run root even when the predicted report
  folder already lives there

## Branch Hygiene Smoke Confirmation

The post-refresh, post-hardening branch-hygiene smoke run is now recorded at:

- `experiments/runs/branch_hygiene/run01_2026-04-17_231500_EDT/`

That run confirmed this rebased feature branch still completes the practical
prompt-lab loop cleanly after being rebound onto the hardened Qwen model
branch:

- `uv run pytest tests/unit/test_yamls.py bda_eval/tests`
- `bda-svc` export on `tests/data/tank.jpg`
- `bda_eval` self-check with saved artifacts

Working implication:

- branch ancestry is now tidy locally
- the feature branch remains prompt-lab ready
- no new prompt baseline was required just because branch hygiene completed

## `e7a22a9` Refresh Smoke Confirmation

The next post-refresh smoke run is now recorded at:

- `experiments/runs/refresh_smoke/run02_2026-04-19_173039_EDT/`

That run confirmed this refreshed feature branch still completes the practical
prompt-lab loop cleanly after absorbing the new upstream export/detect-contract
change:

- `uv run pytest tests/unit/test_yamls.py bda_eval/tests`
- `bda-svc` export on `tests/data/tank.jpg`
- `bda_eval` self-check with saved artifacts

Working implication:

- Qwen absorbed the `e7a22a9` contract change without losing the standard tank
  smoke path
- but because live prompt wording changed, the branch should still rebuild a
  fresh post-`e7a22a9` baseline before treating later prompt behavior as part
  of the old evidence chain

## Pre-PR Update Validation Check

Before updating PR `#134` from the rebased local branch, an additional
pre-push validation run was recorded at:

- `experiments/runs/pre_pr_update_check/run01_2026-04-19_175219_EDT/`

That check confirmed:

- `uv sync --all-packages` completed cleanly
- `uv run pytest tests/unit/test_yamls.py bda_eval/tests` passed
- `bda-svc` export on `tests/data/tank.jpg` still worked
- `bda_eval` self-check still completed cleanly

Normalized output comparison against the prior post-refresh smoke run showed:

- same model tags
- same target type: `military_equipment`
- same damage category: `DESTROYED`
- same confidence level: `PROBABLE`
- same scene summary
- slight bbox drift on the top edge:
  - prior post-refresh smoke: `[51, 37, 128, 73]`
  - pre-push validation: `[51, 49, 128, 73]`
- slight wording drift in `brief_supporting_logic` with the same underlying
  meaning

Working implication:

- the rebased local Qwen feature branch still behaves correctly on the
  practical smoke path
- the result is semantically aligned with the prior post-refresh run, but not a
  byte-for-byte exact replay on the tank seed
- the branch now intentionally keeps the upstream empty-detections contract
  added in `e7a22a9` rather than restoring the older all-zero-bbox guard line

## Detect Surface Inspection Read

The next active Qwen read now includes a dedicated detect-surface inspection
across the active `1.2` line, the doctrine-side `1.3` line, and the
historical detect winner `v006`.

Current conclusion:

- the active `1.2` and `1.3` `detect_objects` templates are currently
  identical
- the rendered branch-to-branch difference comes only from the injected
  doctrine block in `1.3`
- relative to historical `v006`, the active detect surface differs only
  slightly:
  - the old all-zero-bbox safeguard line is gone

## Detect Surface Candidate A Read

The first detect-only prompt-surface follow-up is now recorded at:

- `experiments/runs/detect_surface/run01_2026-04-20_200611_EDT/`

This run should be read carefully:

- it is a same-input parent-vs-candidate local A/B probe on the current
  inherited `e7a22a9` repo base
- it is **not** a rebuilt post-refresh baseline reset
- that means it is useful as a relative branch-local prompt comparison, not as
  a replacement for the missing clean rebuilt post-`e7a22a9` baseline anchor

Current result:

- the local tracked `src/bda_svc/pipeline/config.yaml` now carries an
  exploratory detect-only `v010` candidate
- `v009` remains the last confirmed staged winner for this branch
- `v010` recovered the key `destroyed_building4` failure in a meaningful way:
  - parent control split the scene into two buildings
  - candidate reduced the read to one scene-central destroyed building
- `destroyed_building3` still boxes the background building as a second target
- `destroyed_building6` still behaves like broad scene partitioning
- guardrails held:
  - `office_negative`
  - `operational_tank4`
  - `tank_pressure`

Current supporting artifacts:

- version snapshot:
  - `experiments/versions/v010_detect_objects_adjacent-building-target-body-priority.yaml`
- run manifest:
  - `experiments/runs/detect_surface/run01_2026-04-20_200611_EDT/RUN_MANIFEST.md`
- cross-branch review note:
  - `/home/williambenitez1/Capstone/z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detect_candidate_a_run01_review.md`

Working implication:

- the actual detection prompt surface is now clearly the stronger Qwen lever
  for this problem
- the next detect-only iteration should preserve the `destroyed_building4`
  recovery while targeting:
  - `destroyed_building3`
  - `destroyed_building6`

## Detect Surface Candidate B Read

The next detect-only follow-up is now recorded at:

- `experiments/runs/detect_surface/run02_2026-04-20_204540_EDT/`

This run used the saved `v010` outputs from run01 as the parent control and
tested one extra scene-dominance/background-suppression step.

Current result:

- `destroyed_building4` stayed recovered as one scene-central destroyed
  building
- `destroyed_building3` still boxed the background building
- `destroyed_building6` still returned three buildings
- the candidate did not earn a real improvement on the remaining failure
  family

Working implication:

- `v011` is now recorded and rejected
- the live local tracked config for this branch has been restored to `v010`
- `v010` remains the strongest current local Qwen detect state
  - the explicit `{"detections": []}` no-target instruction is now present
- the next likely leverage point is therefore the actual detection user prompt
  surface, not another doctrine-only rewrite by itself

Current local note:

- `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detection_prompt_surface_inspection.md`

## Detect Surface Candidate C Read

The next detect-only follow-up is now recorded at:

- `experiments/runs/detect_surface/run03_2026-04-20_224812_EDT/`

This run again reused the saved `v010` outputs as the parent control, but it
changed the *example structure* instead of adding more prose rules.

Current result:

- `destroyed_building4` stayed recovered as one scene-central destroyed
  building
- `destroyed_building3` still boxed the background building as a second target
- `destroyed_building6` still returned three buildings
- `office_negative`, `operational_tank4`, and `tank_pressure` remained clean
- some bboxes tightened slightly, but not enough to count as a real fix on the
  still-open building failure family

Working implication:

- `v012` is now recorded and rejected
- the live local tracked config for this branch has again been restored to
  `v010`
- example-heavy structure can tighten presentation and some bbox edges, but it
  does not by itself solve the unresolved adjacent-building selection failures
- `v010` remains the strongest current local Qwen detect state

Current supporting artifacts:

- version snapshot:
  - `experiments/versions/v012_detect_objects_example-structure-target-selection.yaml`
- run manifest:
  - `experiments/runs/detect_surface/run03_2026-04-20_224812_EDT/RUN_MANIFEST.md`
- cross-branch review note:
  - `/home/williambenitez1/Capstone/z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detect_candidate_c_run03_review.md`

## Detect Surface Candidate D Read

The next detect-only follow-up is now recorded at:

- `experiments/runs/detect_surface/run04_2026-04-20_233900_EDT/`

This run kept the `v010` target-body rule set but moved the next lever into
instruction hierarchy by adding an explicit top-of-prompt building decision
order.

Current result:

- `destroyed_building4` stayed recovered as one scene-central destroyed
  building
- `destroyed_building3` still boxed the background building in the active
  `1.2` line
- `destroyed_building6` still returned three buildings
- `office_negative`, `operational_tank4`, and `tank_pressure` remained clean
- the doctrine-side `1.3` lane did improve `destroyed_building3`, but that
  gain did not transfer cleanly into the active branch

Working implication:

- `v013` is now recorded and rejected for the active Qwen line
- the live local tracked config for this branch has again been restored to
  `v010`
- the result is still useful, because it suggests stronger hierarchy can help,
  but not yet reliably enough in the active lane
- `v010` remains the strongest current local Qwen detect state

Current supporting artifacts:

- version snapshot:
  - `experiments/versions/v013_detect_objects_building-priority-decision-order.yaml`
- run manifest:
  - `experiments/runs/detect_surface/run04_2026-04-20_233900_EDT/RUN_MANIFEST.md`
- cross-branch review note:
  - `/home/williambenitez1/Capstone/z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detect_candidate_d_run04_review.md`

## Grounding Generalization Rule

We now treat `tests/data/tank.jpg` as a **pressure test**, not as the only
proof that a bbox change is good.

To reduce overfitting, future detect-only grounding changes should be checked
against the mixed validation pack at:

- `experiments/validation/grounding_generalization_pack_v1.md`

That pack intentionally includes:

- the hard burning-tank pressure case
- another destroyed tank
- an operational tank
- destroyed and operational building controls
- a negative office scene

Working implication:

- a grounding rule is only interesting if it helps or preserves the tank case
  **and** still behaves reasonably across the mixed controls
- detection changes should be promoted only after that broader check, not from
  the seed image alone

## Current Active Read

- fresh branch-aware baseline `v000`:
  - bbox `[51, 37, 102, 73]`
  - `DESTROYED`, `PROBABLE`
- first real candidate `v001`:
  - bbox `[46, 46, 123, 92]`
  - `DESTROYED`, `CONFIRMED`
- `v002` follow-up:
  - bbox `[46, 46, 123, 92]`
  - `DAMAGED`, `PROBABLE`
- `v003` follow-up:
  - bbox `[46, 46, 123, 92]`
  - `DESTROYED`, `PROBABLE`

Current interpretation:

- `v001` looks like a real detection improvement signal on the clean baseline
- but it also reintroduces the older downstream regression pattern
  (`CONFIRMED`, subtype drift, and scene-context drift)
- `v002` shows the better `v001` box can survive an assessment-only change
- but the current safer assessment wording overcorrects `DESTROYED` down to
  `DAMAGED`
- `v003` is the first branch-aware version to combine:
  - the stronger `v001` bbox
  - `DESTROYED`
  - `PROBABLE`
  - cleaner target-level logic
- `v003` also repeated exactly on run02 aside from routine metadata fields
- `v004` preserved all of that while materially improving the summary wording
- `v004` repeated exactly on run02 aside from routine metadata fields
- `v004` is now the confirmed best end-to-end branch-aware candidate

## First Mixed Sweep Read

The first mixed grounding sweep is now recorded at:

- `experiments/runs/generalization_sweep/run01_2026-04-16_004938_EDT/`

That sweep compared the fresh branch-aware `v000` baseline against the
confirmed `v004` stack across:

- the tank pressure test
- another destroyed tank
- an operational tank
- destroyed and operational building controls
- a negative office scene

Current read:

- `v004` is still the best **seed-case** candidate
- but it is **not yet** a clean cross-image grounding winner
- the strongest regression signal in the sweep is `destroyed_building4`, where
  the current candidate collapsed a two-target building scene into one target
- `operational_tank4` also showed that the current full stack still overreads
  muzzle flash / smoke as damage, though that is more an assessment issue than
  a grounding issue

Ground-truth clarification:

- `destroyed_building4` contains two different buildings
- so the sweep result there is a confirmed `v004` detection miss, not just an
  uncertain interpretation

Working implication:

- the next bbox cycle should be detect-only and should use the mixed pack as
  the promotion gate

## First Detect-Only Post-Sweep Read

The first detect-only post-sweep follow-up is now recorded at:

- `experiments/runs/v005/run01_2026-04-16_112937_EDT/`

Current read:

- `v005` recovered separate neighboring building targets on
  `destroyed_building4`
- ground-truth clarification confirms that this is the correct result for that
  image
- `v005` stayed stable on the tank pressure case and most non-negative controls
- but `v005` introduced a fatal full-frame `buildings` false positive on the
  office negative scene

Working implication now:

- keep the multi-target separation lesson from `v005`
- reject the broadened intact-target wording from `v005`
- the next bbox candidate should stay detect-only and add a stronger non-target
  guard for indoor / non-BDA scenes

## Second Detect-Only Post-Sweep Read

The next detect-only follow-up is now recorded at:

- `experiments/runs/v006/run01_2026-04-16_114425_EDT/`

Current read:

- `v006` preserved the correct two-building result on `destroyed_building4`
- `v006` restored `office.jpg` to `object_not_found`
- `v006` kept the tank pressure case steady relative to the fixed `v005`
  reference
- `v006` did not worsen the operational-tank issue, which now looks more
  clearly like an assessment-layer problem

Working implication now:

- `v006` is the best detect-only grounding candidate so far
- it repeated exactly on `run02` across the mixed pack aside from routine
  metadata fields
- `v006` is now the confirmed detect-only grounding leader in this branch-aware
  line
- the next unresolved mixed-pack problem is the operational-tank assessment
  behavior, not the detect rule

## First Assess-Only Post-v006 Read

The next assessment-only follow-up is now recorded at:

- `experiments/runs/v007/run02_2026-04-16_120212_EDT/`

Current read:

- `v007` kept detection frozen at the confirmed `v006` rule and kept summary
  frozen at the confirmed `v004` wording
- `v007` recovered `operational_tank4` from `DAMAGED` / `PROBABLE` to
  `NO DAMAGE` / `CONFIRMED` without changing the bbox
- the destroyed building, operational building, tank pressure, and office
  controls stayed stable at the category/confidence level
- `destroyed_tank15` reintroduced `K-kill` wording in `brief_supporting_logic`,
  which is a target-level wording regression

Working implication now:

- the firing-signature fix is valid
- the next candidate should remain `assess_damage`-only
- the next change should preserve the `operational_tank4` recovery while
  tightening destroyed-case logic wording back down to visible evidence only

## Second Assess-Only Post-v006 Read

The next assessment-only follow-up is now recorded at:

- `experiments/runs/v008/run01_2026-04-16_121637_EDT/`

Current read:

- `v008` kept the valid `v007` operational-firing fix
- `v008` preserved `NO DAMAGE` / `CONFIRMED` on `operational_tank4`
- `v008` removed the `K-kill` wording regression from `destroyed_tank15`
- the destroyed building, operational building, tank pressure, and office
  controls stayed stable at the category/confidence level

Working implication now:

- `v008` is the strongest assess-only candidate so far
- it repeated exactly on `run02` across the mixed pack aside from routine
  metadata fields
- `v008` is now the confirmed assess-only leader in this branch-aware line
- the current best frozen stack is:
  - `detect_objects` from `v006`
  - `assess_damage` from `v008`
  - `summarize_scene` from `v004`

## Broad Validation Sweep Read

The next broad sweep is now recorded at:

- `experiments/runs/generalization_sweep/run02_2026-04-16_122803_EDT/`

Current read:

- the frozen `v006 + v008 + v004` stack is now the strongest cross-image
  candidate in this branch-aware line so far
- it fixes the earlier `operational_tank4` regression
- it fixes the earlier `destroyed_building4` one-target collapse
- it keeps the office negative scene clean
- the main remaining nuance is building-severity calibration on
  `destroyed_building4`, not detection recall

Working implication now:

- the current active branch-aware working stack is:
  - `detect_objects` from `v006`
  - `assess_damage` from `v008`
  - `summarize_scene` from `v004`
- that frozen winner is now formalized as:
  - `experiments/versions/v009_unified_best-stack.yaml`
- the staged-winner note now lives at:
  - `experiments/winners/v009_current_best_stack.md`

## Unified `v009` Focused Comparison Read

The first direct `v009` execution is now recorded at:

- `experiments/runs/v009/run01_2026-04-16_124434_EDT/`

Current read:

- `v009` is behaving as a faithful unified packaging of the proven source
  surfaces, not as a new behavior fork
- on the focused three-case comparison:
  - `tank_pressure`
  - `operational_tank4`
  - `destroyed_building4`
  the `v009_candidate` JSON matched the `v008 run02` reference exactly after
  removing only routine metadata fields
- `v009` also preserves the representative inheritance we expected:
  - `v006` detection geometry on the tank and destroyed-building cases
  - `v008` target-level assessment behavior on all three focused cases
  - `v004` conservative summary wording on the seed tank case

Working implication now:

- `v009` should be treated as the single explicit winner version for future
  comparisons and further work on this model line
- we no longer need to mentally reconstruct the frozen stack from `v006`,
  `v008`, and `v004` every time we want to reference the current best combined
  behavior

## Additional Baseline Comparison Read

An extra baseline-vs-`v009` challenge run is now recorded at:

- `experiments/runs/baseline_vs_v009_additional/run04_2026-04-16_130409_EDT/`

This run used three new images from `z_reference_docs/Data_set_Storage/` chosen
to pressure different behaviors:

- a multi-object building scene
- a smoke/fire-obscured destroyed truck
- a cluttered complex building scene with foreground/background separation

Current read:

- `v009` did not produce a dramatic win on every new image
- but it stayed stable across all three new cases
- the strongest added evidence is:
  - preserved three-building recall on a new multi-object scene
  - no regression on the smoke/fire-obscured truck case
  - preserved foreground/background building separation on the complex scene,
    with a modest bbox improvement on the secondary building

Working implication now:

- the current best stack has stronger evidence for genuine generalization than
  a single seed-case success
- the latest added value is strongest in:
  - cross-image stability
  - multi-target recall discipline
  - wording consistency
  - modest bbox refinement on some harder scenes

## 10-Image Blind Sweep Read

A broader baseline-vs-`v009` blind sweep is now recorded at:

- `experiments/runs/baseline_vs_v009_blind_sweep/run01_2026-04-16_135924_EDT/`

This run compared the clean `origin/main` baseline stack against `v009` on ten
additional images spanning:

- destroyed / operational buildings
- destroyed / operational tanks
- destroyed / operational trucks

Current read:

- `v009` preserved target-count recall on all 10 added images
- `v009` kept the same damage/confidence structure on 6 of 10 cases
- only 2 of 10 cases changed damage category at all
- the strongest broad signal is:
  - stability
  - preserved recall
  - cleaner wording discipline
  - more conservative confidence calibration

Important caution:

- two images remain judgment-change watch cases:
  - `destroyed_building5`
  - `destroyed_tank37`

Deeper review of those two watch cases now says:

- `destroyed_building5` is likely a real `v009` severity overcall
  - the bbox change is minor
  - the bigger issue is category calibration
  - under the local doctrine for high multistory buildings, baseline
    `SEVERE DAMAGE / PROBABLE` is more defensible than `v009`
    `DESTROYED / PROBABLE`
- `destroyed_tank37` is more mixed
  - `v009` gives the cleaner bbox
  - the cautious `DAMAGED / PROBABLE` read is arguable given the angle and
    smoke obscuration
  - but the current `v009` supporting logic is still too catastrophic for a
    `DAMAGED` label and should be softened if that category is retained

So the remaining blind-sweep caution is now better described as:

- category-calibration watch cases, not recall failures
- one building overcall and one burning-equipment logic/category consistency
  case

Working implication now:

- the current stack has materially stronger support for “real improvement”
  rather than “quick mockup”
- the current evidence base is now broad enough to support a team-facing claim
  of cross-image generalization, while still being honest about a small number
  of unresolved judgment differences

## Promotion Status

The feature branch promotion step is now complete.

Tracked branch history now preserves:

- `566892a` — `Add prompt-lab review artifacts to bda_eval`
- `127051a` — `Promote v009 prompt stack into pipeline config`
- `ebeae30` — `Install workspace packages in CI`

That means:

- the `bda_eval` review-sheet workflow is no longer just a local working-tree
  convenience
- the historical promotion of the `v009` best stack into tracked
  `src/bda_svc/pipeline/config.yaml` is now preserved in branch history
- `v009` remains the last confirmed staged winner for this model line
- the current local tracked config has since moved forward to an exploratory
  detect-only `v010` candidate; see the later "Detect Surface Candidate A Read"
  section for the current active local state
- the feature branch is pushed to:
  - `origin/feat/qwen3-vl-8b-instruct/two-pass-refinement`
- PR `#134` is now open against `upstream/main`:
  - `https://github.com/cmu-bda/bda-svc/pull/134`
- GitHub CI is currently green after the workspace-package install fix

Important review note:

- the green GitHub checks should be read as branch-health evidence
- they confirm the tracked branch is testable and runnable
- they do **not** currently enforce exact parity with the local prompt-lab
  `v009` winner outputs
- exact prompt-behavior evidence still lives in the local prompt-lab runs,
  critique notes, sweep summaries, and winner notes under this branch-aware lab

Team-ready summary note:

- `experiments/winners/v009_team_ready_summary.md`
- `experiments/winners/v009_team_meeting_script.md`

Teaching companion:

- `/home/williambenitez1/Capstone/z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`
  explains this workflow in a capability-first, teaching-grade format
