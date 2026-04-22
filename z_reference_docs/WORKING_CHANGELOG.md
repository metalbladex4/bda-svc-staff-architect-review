# Working Changelog

## Purpose

This document is a running record of:

- my current understanding of the project
- the current working plan and direction of travel
- meaningful changes we have made
- open issues, risks, and decision points that may require plan changes

The main intent is to give you a fast way to review whether my understanding is
still correct and whether the current way forward still makes sense. This is not
just a raw change log. It is also a living checkpoint of project understanding
and current strategy at that moment in time.

When this document is updated, it should be framed in that spirit:

- what I think the project is doing now
- what we are trying to do next
- what changed since the last checkpoint
- what needs to be reconsidered, corrected, or promoted into the main repo

## How To Use This Document

- Read `Current Understanding` if you want the latest high-level project state.
- Read `Current Way Forward` if you want the current plan at this moment.
- Read `z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md` if you want the
  dedicated running record of prompt-development method, source usage,
  experiment rationale, and prompt decision history.
- Read `z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md` if you want
  the capability-first, teaching-grade explanation of how this prompt workflow
  works and how to reproduce it.
- Read `z_reference_docs/capstone_tech_docs/understanding_tracking.md` if you
  want the dedicated running record of capstone technical-document context,
  especially the Phase 3 deployment-procedure work.
- Read `Change Entries` if you want the sequence of concrete updates and why they
  mattered.
- If our direction changes, this document should be updated before or alongside
  the next major step.

## Current Understanding

As of `2026-04-20`, my working understanding is:

- This project is a local CLI BDA tool centered on **Phase 1 physical damage
  assessment**.
- The live runtime is based on an **Ollama dual-VLM pipeline**, not local
  Hugging Face model weights stored in the repo.
- The main live prompt/runtime files are:
  - `src/bda_svc/pipeline/config.yaml`
  - `src/bda_svc/pipeline/model.py`
  - `src/bda_svc/pipeline/interfaces.py`
  - `src/bda_svc/pipeline/doctrine.yaml`
- Detection currently asks the VLM to return doctrinal `target_type` plus a
  bounding box using the configured bbox convention in
  `src/bda_svc/pipeline/config.yaml`.
- Assessment currently uses two images for one target:
  - a full-scene image with the selected target outlined
  - a cropped image of the same target
- Assessment returns:
  - `damage_category`
  - `confidence_level`
  - `brief_supporting_logic`
- Summary returns plain text and is expected to stay consistent with prior
  target assessments.
- Current doctrine scope is narrow and practical:
  - `buildings`
  - `military_equipment`
- `upstream/main`, `origin/main`, and local `main` are now aligned at
  `e7a22a9`.
- the pre-reset local line has been preserved on
  `snapshot/2026-04-15-pre-main-reset`
- clean `main` is now intended to stay an exact mirror of `upstream/main`
- active code work should now move to worktrees instead of staying on `main`
- the first new branch/worktree line is:
  - `model/qwen3-vl-8b-instruct`
  - `/home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct`
- the first feature branch/worktree line is:
  - `feat/qwen3-vl-8b-instruct/two-pass-refinement`
  - `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`
- `z_reference_docs` remains the centralized local docs and experiment-output
  hub and is now being organized model-first, branch-second for new work
  with visible numbering prefixes for faster scanning
- after the latest hardening pass, all four active worktrees can now complete
  the practical prompt-lab smoke path:
  - `bda-svc` export
  - `bda_eval` self-check
  - artifact writeout into `z_reference_docs/Prompt_Labs/...`
- the new branch-aware feature lab now has its first fresh `v000` baseline at
  `28e863b` under:
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/`
- that fresh baseline run on `tests/data/tank.jpg` produced:
  - `DESTROYED`
  - `PROBABLE`
  - bbox `[51, 37, 102, 73]`
- that means the new branch-aware baseline is tighter than the preserved
  legacy `21deaf5` baseline `[51, 37, 128, 73]`, so future grounding work on
  this branch should compare against the fresh branch-aware `v000`, not the
  older legacy baseline
- Current live `main` now includes:
  - inference-time metadata in exported JSON
  - configurable bbox-convention handling
  - doctrine-guided detection prompt inputs
  - `think=False` in Ollama calls
  - more robust structured-output handling
  - `ollama.Client` support with `OLLAMA_HOST` and `OLLAMA_API_KEY`
  - the live model tag `qwen3-vl:8b-instruct`
- The earlier `28e863b` upstream move established the current branch-aware
  Qwen evidence anchor and the first clean numbered worktree line.
- The earlier upstream pull moved the repo baseline to `c19940a`, and that
  delta was infrastructure-only:
  - `.github/workflows/ci.yml` now forces fresh Docker pulls in the scan job
  - `docker/Dockerfile` now uses `python:3.13-slim-trixie`
  - the image build now runs `apt-get upgrade -y` and installs packages with
    `--no-install-recommends`
- Because that `c19940a` delta did **not** change live prompt text, doctrine,
  or pipeline runtime semantics, the active Qwen and Gemma prompt baselines did
  **not** need to be rebuilt from it.
- The latest upstream pull then moved the repo baseline again to `e7a22a9`
  through PR `#136` (`fix/unicode`).
- That newer delta touched:
  - `bda_eval/discovery.py`
  - `bda_eval/main.py`
  - `src/bda_svc/export.py`
  - `src/bda_svc/pipeline/config.yaml`
- We have aligned local `main` and `origin/main` to `e7a22a9`, and the active
  Qwen and Gemma worktrees have now also been rebased through this newer
  baseline.
- The `e7a22a9` delta is not infra-only. It changed:
  - JSON export encoding via `ensure_ascii=False`
  - the live detect prompt contract by explicitly allowing
    `{"detections": []}` for no-target scenes
- After the `e7a22a9` propagation:
  - both Qwen worktrees still pass the shared tests and the full practical
    prompt-lab smoke loop on `tests/data/tank.jpg`
  - both Gemma worktrees still pass the shared tests and can export reports
    against the local Gemma host
  - the initial Gemma refresh smoke had both active Gemma branches returning
    `object_not_found` / `NOT APPLICABLE` on the standard tank smoke image
- Working implication:
  - Qwen absorbed the new contract without losing the tank smoke path
  - Gemma did need a fresh post-`e7a22a9` baseline before we could trust the
    newer behavior as part of the same evidence chain
- that Gemma reset pass has now been completed under:
  - `z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/v000/run02_2026-04-19_185856_EDT/`
- the rebuilt Gemma `v000` run is now the active anchor for the current repo
  base, while the earlier `run01_2026-04-17_134308_EDT` baseline remains
  preserved as pre-refresh historical evidence
- the rebuilt reset showed that `e7a22a9` changed more than the tank smoke
  seed:
  - `tank_pressure` regressed to `object_not_found / NOT APPLICABLE`
  - `operational_tank4` regressed to `DAMAGED / PROBABLE`
  - `destroyed_building4` remained an undercalled building failure
  - `destroyed_tank15`, `operational_building7`, and `office_negative` still
    held acceptably
- working implication:
  - the old Gemma `run01` conclusions are not portable onto the current repo
    base
  - Gemma should pause before `v001` until the inherited detect-contract
    effect is reconsidered
- a follow-up two-case Gemma detection diagnostic rerun has now clarified the
  `tank_pressure` failure path:
  - Gemma returned raw `{"detections":[]}` on `tank_pressure`
  - that collapse was not caused by parse failure
  - that collapse was not caused by invalid target-type filtering
  - that collapse was not caused by invalid bbox filtering
  - `operational_tank4` still returned one valid `military_equipment`
    detection, so its regression is now localized to bbox placement and/or the
    assessment stage rather than total detect-stage collapse
- working implication:
  - the explicit empty-detections instruction is now the leading causal suspect
    for the Gemma `tank_pressure` abstention
  - the next Gemma move should be a narrow detect-contract adjustment test, not
    a broad speculative rewrite
- that narrow follow-up has now been run as `v001`, and on the two directly
  implicated tank cases it recovered both regressions:
  - `tank_pressure` returned to a real `military_equipment` detection with
    `DESTROYED / PROBABLE`
  - `operational_tank4` returned to `NO DAMAGE / CONFIRMED`
- working implication:
  - the no-target detect instruction is now confirmed as a high-leverage Gemma
    control point on the current repo base
  - a broader `v001` follow-up has now also been completed across the full
    inherited six-case pack
  - `v001` held `destroyed_tank15`, `operational_building7`, and
    `office_negative`, while keeping the tank recoveries
  - `destroyed_building4` improved target separation but still undercalls one
    building's severity
  - `v001` is now the strongest Gemma direction so far on the current repo
    base
- a focused `v002` follow-up has now improved that remaining building-severity
  problem without reopening the recovered tank behavior:
  - `destroyed_building4` moved from
    `MODERATE DAMAGE / CONFIRMED` + `DESTROYED / CONFIRMED`
    to
    `SEVERE DAMAGE / PROBABLE` + `DESTROYED / PROBABLE`
  - `tank_pressure` held at `DESTROYED / PROBABLE`
  - `operational_tank4` held at `NO DAMAGE / CONFIRMED`
  - `operational_building7` held at `NO DAMAGE / CONFIRMED`
- working implication:
  - `v002` is now the strongest Gemma candidate so far
  - that broader full-pack follow-up has now also been completed
  - `v002` held the full inherited six-case pack while preserving the
    recovered equipment behavior and the negative/intact controls
  - `v002` should now replace `v001` as the active Gemma direction
- The active branch-aware lab now has an explicit mixed-image grounding
  validation pack so future bbox changes are judged against more than
  `tests/data/tank.jpg`.
- a dedicated safe-refresh procedure now exists in:
  `z_reference_docs/GIT_WORKTREE_UPDATE_WORKFLOW.md`
  for future `upstream/main` updates across `main`, model branches, and feature
  worktrees
- a repo-specific copy-paste checklist now also exists in:
  `z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_QWEN.md`
  for the current numbered Qwen branch line
- That upstream delta did not change repo dependencies or the active live model
  tag, so it does not require `uv sync` or a new Ollama model download.
- That new `c19940a` infra delta has now also been propagated cleanly through
  the active Qwen and Gemma model/feature worktrees using that documented
  refresh workflow.
- branch hygiene is now complete on the two active feature worktrees:
  - `feat/qwen3-vl-8b-instruct/two-pass-refinement`
  - `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- that hygiene pass included:
  - rebasing each feature branch onto its newly hardened model branch
  - rerunning `uv run pytest tests/unit/test_yamls.py bda_eval/tests`
  - rerunning the practical prompt-lab smoke path
- the local Qwen feature branch still diverges from its `origin` tracking
  branch because the rebases rewrote local history, so any future remote refresh
  should remain a deliberate `git push --force-with-lease` decision
- the current Gemma feature branch now matches the hardened Gemma model branch
  in tracked code after the bootstrap commit was promoted upward
- The evaluation side is now more image-aware:
  - `bda_eval` can take an `--images` folder
  - it can emit bbox overlays
  - it copies reference/predicted report folders into the eval output
  - it logs LLMaaJ reasoning under `logs_llmaaj/`
  - it carries `inference_time` into the evaluation CSV
- The active prompt workflow now includes a structured
  critique/research/revise loop after each candidate run.
- The first run executed under that loop is `v004`, and its critique and
  paired research note now exist alongside the normal run artifacts.
- The second run in that loop is `v005`, which matched the baseline exactly and
  changed the next prompt direction toward shorter, example-driven steering.
- The third run in that loop is `v006`, which is now the best bbox candidate so
  far but still needs confirmation because downstream confidence and summary
  behavior changed too.
- The confirmation repeat for `v006` held exactly, so the bbox improvement is
  now stable on the current seed case.
- The frozen `v006` + `v009` pair is now the best-known combined direction so
  far, and a later cross-image sweep showed that it generalizes reasonably on
  truck and office scenes while the tank seed still wobbles across repeats.
- Community reports outside the official docs now suggest that Qwen grounding
  quality can vary by inference backend/runtime, so backend variance is part of
  our prompt diagnosis now.
- The current top-level YAML split still looks appropriate for the project;
  `summarize_scene` remains the loosest surface, but the main architecture is
  not the first thing to rewrite.
- The next cycle was re-opened on grounding first, and the first `_pixels`
  experiment (`v010`) has now been run and rejected after collapsing detection
  to `object_not_found` on the tank seed.
- The local temporary debug-export path now also writes `pipeline_debug.json`,
  so failed grounding runs keep the raw detection payload instead of leaving us
  to infer what happened from the fallback report alone.
- `v011` has now been run: it recovered detection on the normalized contract
  and supports the `v010` coordinate-mismatch diagnosis, but the bbox
  converged back toward the older `v001` / `v002` family rather than clearly
  improving past the frozen `v009` working baseline.
- The documentation now explicitly treats `pipeline_debug.json` as temporary
  prompt-lab instrumentation used to inspect raw detection responses, bbox
  conversion behavior, and rejected detections before choosing the next prompt
  revision.
- The cycle workflow now explicitly distinguishes:
  - valid but off-target raw bbox -> grounding wording problem
  - invalid/rejected raw bbox -> contract or validation problem
  and `v012` has been queued from that rule.
- `v012` has now been run and rejected as a bbox-improving prompt. Its raw
  debug payload kept the baseline left/right span and only moved the box
  downward, which strengthens the case that prompt-only detection tuning is
  stalling on this seed case.
- the first code-level grounding aid is now implemented locally: optional
  two-pass ROI refinement behind `detection_vlm.refinement_enabled` and
  `detection_vlm.refinement_roi_buffer_ratio`
- `pipeline_debug.json` now also captures refinement attempts so we can see
  the ROI used, translated second-pass candidates, and the final selection
- `v013` has now run as the first code-assisted grounding experiment:
  the first pass narrowed to raw `[200, 300, 400, 600]`, the ROI-local
  second pass returned no detections, and the runtime kept the narrowed box
  `[51, 37, 102, 73]`
- `v013` run02 repeated that exact same behavior, so the current two-pass ROI
  refinement setting is now confirmed as a stable non-win
- `v014` widened the ROI substantially and still produced no ROI-local
  second-pass detections, so ROI width alone does not fix the current
  refinement path
- the first branch-aware mixed grounding sweep now exists under:
  `experiments/runs/generalization_sweep/run01_2026-04-16_004938_EDT/`
- that sweep showed `v004` is still the best seed-case stack, but not yet a
  clean cross-image grounding winner
- the clearest detection/generalization regression in that sweep was
  `destroyed_building4`, where the current candidate collapsed a two-target
  building scene into one target
- the sweep also showed a current eval limitation: `bda_eval` still does not
  cleanly score negative scenes with `NOT APPLICABLE` damage labels, even
  though the underlying `bda-svc` model behavior stayed correct
- `v005` has now been run as the first detect-only post-sweep candidate
- `v005` recovered separate neighboring building targets on
  `destroyed_building4`, which is a real grounding improvement signal
- ground-truth clarification now confirms that `destroyed_building4` contains
  two different buildings, so `v005` is correct on that case and `v004`
  definitely missed one valid target there
- `v005` also introduced a fatal negative-scene regression by labeling the
  office control as a full-frame `buildings` target, so it is a reject as a
  winner and only the building-separation idea should be reused
- `v006` has now been run as the next detect-only follow-up
- `v006` preserved the correct two-building result on `destroyed_building4`
  and restored `office.jpg` to `object_not_found`
- `v006` held the tank pressure case steady and did not worsen the
  operational-tank issue
- `v006` run02 matched `run01` across the full mixed pack after removing only
  routine metadata fields
- `v006` is now the confirmed detect-only grounding leader in the current
  branch-aware line
- the main remaining mixed-pack issue is now the operational-tank assessment
  behavior rather than the detect rule
- `v007` has now been run as the first assess-only follow-up after freezing the
  confirmed `v006` detect rule
- `v007` recovered `operational_tank4` to `NO DAMAGE` / `CONFIRMED` with the
  same bbox, which confirms the remaining issue was in assessment rather than
  detection
- the destroyed building, operational building, tank pressure, and office
  controls stayed stable at the category/confidence level
- `v007` also reintroduced `K-kill` wording on `destroyed_tank15`, so the
  operational-firing fix is valid but the destroyed-case wording still needs a
  tighter visible-evidence guard
- it is now explicitly acceptable in the active workflow to copy source images
  from `z_reference_docs/Data_set_Storage/` into worktree or prompt-lab run
  folders for evaluation, and to keep those copied images there as part of the
  saved review artifacts
- `v008` has now been run as the next assess-only follow-up
- `v008` preserved the `operational_tank4` recovery to `NO DAMAGE` /
  `CONFIRMED` with the same bbox
- `v008` kept the destroyed building, operational building, tank pressure, and
  office controls stable at the category/confidence level
- `v008` removed the `K-kill` wording regression from `destroyed_tank15`
- `v008` run02 matched `run01` across the full mixed pack after removing only
  routine metadata fields
- `v008` is now the confirmed assess-only leader in the current branch-aware
  line
- the current best frozen stack is now:
  - `detect_objects` from `v006`
  - `assess_damage` from `v008`
  - `summarize_scene` from `v004`
- the broad frozen-stack sweep has now been rerun against the fresh `v000`
  baseline
- the frozen `v006 + v008 + v004` stack fixed the earlier
  `operational_tank4` regression from the old `v004` sweep
- the frozen stack also fixed the earlier `destroyed_building4` one-target
  collapse and restored two-building recall
- the office negative scene stayed clean
- the main residual caution is now building-severity calibration on
  `destroyed_building4`, not target recall
- this frozen stack is now the strongest cross-image branch-aware candidate so
  far
- that winner stack is now formalized as
  `v009_unified_best-stack.yaml`
- the staged winner note now lives in the winners area so future promotion
  work can reference one explicit packaged stack instead of reconstructing it
  from separate earlier versions
- `v009` has now also been run directly on a focused three-case comparison set
  (`tank_pressure`, `operational_tank4`, `destroyed_building4`)
- that direct `v009` run matched the frozen winner exactly after removing only
  routine metadata fields
- this confirms the unified version file is faithfully packaging the proven
  source surfaces rather than introducing new drift
- an additional baseline-vs-`v009` challenge run has now been added using
  three new images from `z_reference_docs/Data_set_Storage/`
- those three added cases were chosen to cover:
  - multi-object target separation
  - smoke/fire obscuration
  - a cluttered complex scene
- the added run does not show a giant win on every image, but it does show
  that `v009` stays stable on new hard cases and preserves the most important
  behaviors we care about
- the strongest added support is:
  - preserved three-building recall on a new multi-object scene
  - no regression on the smoke/fire destroyed-truck case
  - preserved foreground/background separation on a new complex building scene
    with a modest bbox refinement on the secondary building
- a broader 10-image blind sweep has now also been run against the clean
  `origin/main` baseline
- on that 10-image sweep:
  - `v009` preserved target-count recall on all 10 images
  - `v009` kept the same damage/confidence structure on 6 of 10 cases
  - only 2 of 10 cases changed damage category
- this strengthens the claim that `v009` is a real cross-image improvement in
  stability and recall discipline, not just a one-scene prompt demo
- the two key caution cases from that blind sweep are now:
  - `destroyed_building5`
  - `destroyed_tank37`
- deeper review now shows those are category-calibration watch cases rather
  than recall failures:
  - `destroyed_building5` likely favors the clean baseline judgment
    `SEVERE DAMAGE / PROBABLE` over `v009` `DESTROYED / PROBABLE`
  - `destroyed_tank37` is now better described as a logic/category consistency
    watch case:
    `v009` gives the cleaner bbox and its cautious `DAMAGED / PROBABLE` call is
    arguable under smoke/angle obscuration, but the current supporting logic is
    still too catastrophic for a `DAMAGED` label
- the feature branch now also preserves the current working state in tracked
  history with the first two promotion commits:
  - `566892a` — `Add prompt-lab review artifacts to bda_eval`
  - `127051a` — `Promote v009 prompt stack into pipeline config`
- the feature branch has also now been pushed to:
  - `origin/feat/qwen3-vl-8b-instruct/two-pass-refinement`
- this means the review workflow and the current best prompt stack are both now
  preserved in the tracked feature-branch codebase, not only in local lab docs
- a short team-facing summary and meeting script now also exist under:
  - `experiments/winners/v009_team_ready_summary.md`
  - `experiments/winners/v009_team_meeting_script.md`
- the current active prompt effort is now best understood as three cooperating
  capabilities:
  - a centralized local evidence/docs hub in `z_reference_docs`
  - a runtime inference pipeline in `bda-svc`
  - an evaluation and review-artifact layer in `bda_eval`
- the current unified branch-aware winner is `v009`, which packages:
  - `detect_objects` from `v006`
  - `assess_damage` from `v008`
  - `summarize_scene` from `v004`
- that `v009` stack is now promoted into the tracked feature-branch
  `src/bda_svc/pipeline/config.yaml`
- tracked history for the current branch-ready state now includes three
  preservation commits:
  - `566892a` — `Add prompt-lab review artifacts to bda_eval`
  - `127051a` — `Promote v009 prompt stack into pipeline config`
  - `ebeae30` — `Install workspace packages in CI`
- PR `#134` is now open against `upstream/main` at:
  - `https://github.com/cmu-bda/bda-svc/pull/134`
- the current GitHub checks for that PR are green after the CI fix
- the green GitHub checks should be read as branch-health evidence:
  - unit and integration checks passed
  - Docker build/run checks passed
  - the branch is reviewable from an engineering-health perspective
- those green checks do **not** mean GitHub CI is enforcing exact prompt-lab
  parity with the local `v009` winner outputs
- exact prompt-behavior evidence still lives primarily in the local prompt-lab
  runs, critique notes, sweep summaries, and winner notes under
  `z_reference_docs/Prompt_Labs/...`
- the older `v010` through `v014` grounding and ROI experiments remain
  preserved historical context from the earlier line, not the current active
  branch-aware promotion line
- the new top-level teaching companion for this workflow now lives at:
  - `z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`
- the next model-line bootstrap has now started under:
  - `model/gemma4-e4b`
  - `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- the new Gemma evidence pack now lives at:
  - `z_reference_docs/Prompting/Google_Gemma/Gemma_4/`
- the new Gemma prompt-lab root now lives at:
  - `z_reference_docs/Prompt_Labs/3_gemma4-e4b/`
- the Gemma bootstrap is intentionally local-first:
  - active target: `gemma4:e4b`
  - comparison-only size: `gemma4:e2b`
  - reference-only sizes for now: `gemma4:26b`, `gemma4:31b`
- the first Gemma feature branch now starts from a semantic port of the active
  Qwen `v009` stack rather than from the older `origin/main` prompt wording
- the Gemma bootstrap line now also has a completed first live baseline run
  under:
  - `z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/v000/run01_2026-04-17_134308_EDT/`
- that first Gemma `v000` run used a user-local Ollama `0.21.0` runtime on
  `127.0.0.1:11435` because the system Ollama install remains `0.15.2`
- the first Gemma read is now clear:
  - equipment and negative-scene behavior are promising
  - `destroyed_building4` is the first major Gemma-specific failure surface
- after the later `c19940a` upstream sync:
  - the Qwen model and feature worktrees were rebased cleanly onto the new main
  - the Gemma model and feature worktrees were rebased cleanly onto the new
    main
  - neither line needed a prompt-baseline refresh because the upstream delta
    was CI/container-only
  - the local Qwen feature branch now diverges from its `origin` branch until
    we deliberately decide whether to refresh the remote branch with
    `--force-with-lease`
- the model branches have now also been hardened so they are not just ancestry
  roots:
  - the Qwen model branch now carries:
    - `b947a3e` — `Add prompt-lab review artifacts to bda_eval`
    - `0f916de` — `Install workspace packages in CI`
  - the Gemma model branch now also carries:
    - `54a9d58` — `Bootstrap Gemma 4 E4B baseline config`
- those model-branch changes were then validated with:
  - full shared yaml/eval pytest slices
  - prompt-lab style `bda-svc` smoke exports
  - prompt-lab style `bda_eval` self-checks
- result:
  - all four active worktrees can now follow the same basic prompt-lab smoke
    workflow cleanly
- a local-only Phase-1 doctrine replacement package now exists under:
  `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/`
- that package now includes:
  - a doctrine source crosswalk
  - a preserve/adapt/exclude matrix
  - Phase-1-only scope rules
  - a first prompt-compatible runtime candidate doctrine file
  - a branch/worktree test playbook
- two new local-only doctrine experiment feature branches now exist:
  - `feat/qwen3-vl-8b-instruct/doctrine-bda-alignment`
  - `feat/gemma4-e4b/doctrine-bda-alignment`
- their worktrees are:
  - `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment`
  - `/home/williambenitez1/Capstone_worktrees/3.2_feat__gemma4-e4b__doctrine-bda-alignment`
- the first runtime candidate doctrine has now been applied only in those two
  doctrine branches and has passed local runtime contract checks in both
  worktrees:
  - `uv run pytest tests/unit/test_yamls.py tests/unit/test_utilities.py`
- the active Qwen `1.2` and active Gemma `3.1` feature branches remain the
  untouched control surfaces for doctrine A/B work
- the Gemma doctrine branch intentionally starts from committed tip `9ae27e9`
  and does not absorb the uncommitted local `v003` Gemma edits currently
  sitting in the active `3.1` worktree
- the first doctrine-sensitive guard-set runs now also exist under:
  - Qwen:
    `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/experiments/runs/doctrine_guard_set/run01_2026-04-20_182243_EDT/`
  - Gemma:
    `z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.2_feat__gemma4-e4b__doctrine-bda-alignment/experiments/runs/doctrine_guard_set/run01_2026-04-20_182243_EDT/`
- early read from those first doctrine guard-set runs:
  - Qwen held the office negative, intact building, intact tank, destroyed
    tank, and tank-pressure controls
  - the first Qwen read looked stronger at first glance, but later same-input
    parent-control review showed it was not a real win on `destroyed_building4`
  - Gemma held `tank_pressure`, `destroyed_tank15`, and `office_negative`
  - Gemma reopened two control regressions:
    - `operational_tank4` fell back to `DAMAGED / PROBABLE`
    - `operational_building7` gained a false-positive
      `military_equipment` detection
  - working implication:
    - the first doctrine candidate is operationally neutral on the reviewed
      Qwen building case so far
    - the same candidate is an early no-go for Gemma until it is revised

### 2026-04-20 — Qwen Doctrine Candidate Did Not Beat The Held `destroyed_building4` Control

What changed:
- ran the held Qwen parent branch on the exact same doctrine guard-set input
  pack used for the first `1.3` doctrine-candidate run
- generated bbox review artifacts for `destroyed_building4`
- manually reviewed the source image, the Qwen parent/candidate JSON outputs,
  and the building PDA text from the BDA corpus
- recorded that review under:
  `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_destroyed_building4_manual_review.md`

What we learned:
- the held Qwen control and the doctrine candidate both returned two
  `DESTROYED / PROBABLE` buildings on `destroyed_building4`
- the doctrine candidate only shifted the split slightly:
  - control: `[0, 18, 63, 150]` and `[63, 18, 244, 150]`
  - candidate: `[29, 18, 69, 153]` and `[69, 18, 250, 153]`
- the bbox review sheet shows that both runs still carve out the upright
  left-side neighboring structure as its own destroyed building target
- this means the doctrine candidate did not materially improve bbox quality or
  doctrinal fit on that scene
- the root problem there remains target delimitation/localization, not PDA
  wording alone

Why it mattered:
- it corrected the earlier stale read that the doctrine candidate might be a
  useful Qwen building-severity improvement
- it confirms that doctrine A/B work still needs same-input parent controls
  before we treat a semantic difference as real evidence
- it narrows the next useful Qwen doctrine lever toward target-selection
  guidance rather than another pure PDA-text rewrite

### 2026-04-20 — Qwen `v002` Building-Detection-Guidance Tightening Did Not Produce A Clear Win

What changed:
- created a Qwen-only follow-up doctrine candidate:
  - `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/runtime_candidate_doctrine.v002.yaml`
- changed only `buildings.detection_guidance` in the Qwen `1.3` worktree to
  tighten how the selected building body should be chosen in mixed
  adjacent-building scenes
- built an expanded Qwen doctrine rerun under:
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/experiments/runs/doctrine_guard_set/run02_2026-04-20_190546_EDT/`
- ran both:
  - Qwen doctrine candidate
  - held Qwen parent control
- generated `bda_eval` parent-vs-candidate review artifacts for the whole pack

What we learned:
- the candidate was mostly neutral on the added building cases
- it did not fix the background-building false split on `destroyed_building3`
- it did not improve the broad scene partitioning behavior on
  `destroyed_building6`
- it worsened `destroyed_building4` relative to the held control:
  - held control:
    - left target `SEVERE DAMAGE / PROBABLE`
    - right target `DESTROYED / PROBABLE`
  - candidate:
    - left target `DESTROYED / PROBABLE`
    - right target `DESTROYED / PROBABLE`
- clean controls still held:
  - `destroyed_building5`
  - `destroyed_building8`
  - `operational_building2`
  - `operational_building7`
  - `operational_building91`
  - `operational_tank4`
  - `destroyed_tank15`
  - `office_negative`

Why it mattered:
- it tested the narrowest plausible doctrine-only fix for the adjacency problem
- it showed that tighter building-selection language in doctrine is not, by
  itself, a strong enough lever for the current Qwen failure mode
- it gives us a cleaner stopping point before we touch Gemma again

Working implication:
- keep Gemma frozen for now
- treat the Qwen adjacency problem as still unresolved
- decide the next move between:
  - a deeper doctrine rewrite
  - a detection-prompt change
  - a runtime/detection framing change

## Current Way Forward

As of `2026-04-21`, the current working plan is:

Update on `2026-04-21` before the next session:

- the active local resume point is the dirty Qwen doctrine worktree
  `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment`,
  not the Gemma line
- the last completed logged doctrine-only Qwen checkpoint remains:
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/experiments/runs/doctrine_guard_set/run02_2026-04-20_190546_EDT/`
- there is later uncommitted local work in:
  - `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/src/bda_svc/pipeline/doctrine.yaml`
  - `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/src/bda_svc/pipeline/config.yaml`
- those dirty files do not yet have a completed validation run or a dedicated
  handoff note of their own, so the next session should start by diffing them
  against the logged `v002` doctrine checkpoint before opening any new cycle

1. Treat `v009` as the active working config for this Qwen model line going
   forward.
2. Keep the live runtime contract and doctrine file stable unless new evidence
   clearly justifies another change.
3. Keep the clean mirrored `main` boring, and keep active work on the numbered
   model/feature worktrees.
4. Use the centralized local evidence/docs hub in `z_reference_docs` as the
   canonical place for run manifests, critiques, sweeps, and teaching notes.
5. Use the tracked feature-branch config as the active working state for this
   model line unless new evidence clearly justifies another prompt cycle.
6. Use PR `#134` as the current team-review surface for that active working
   config.
7. Keep the distinction explicit between:
   - branch-health validation in GitHub CI
   - prompt-behavior validation in the local prompt-lab evidence chain
8. If another prompt cycle opens later, start from the promoted `v009` branch
   state and reuse the branch-aware workflow, mixed-pack validation gate, and
   review-artifact workflow rather than reopening the older legacy line.
9. Keep `z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md` as the historical
   method log and use the new
   `z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md` when the goal is
   to teach or reproduce the method.
10. Use `z_reference_docs/GIT_WORKTREE_UPDATE_WORKFLOW.md` and
    `z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_QWEN.md` whenever
    `upstream/main` moves again.
11. Keep the Gemma line on `gemma4:e4b` and use the rebuilt post-`e7a22a9`
    `v000` run as the active baseline anchor for the current repo base, while
    preserving the older `run01` as historical pre-refresh evidence.
12. Keep the new Gemma line local-first and research-first by preserving:
    - the Gemma evidence pack under
      `z_reference_docs/Prompting/Google_Gemma/Gemma_4/`
    - the new branch-aware Gemma lab under
      `z_reference_docs/Prompt_Labs/3_gemma4-e4b/`
13. Reuse the Qwen seed pack and review-artifact workflow so Gemma
    comparisons stay direct and interpretable.
14. Treat `v001` as the recovered detect-contract direction that restored the
    equipment cases on the current repo base.
15. Treat `v002` as the active Gemma direction because it improved building
    severity while preserving the recovered tank behavior and then held the
    full inherited six-case pack.
16. Keep the active Qwen `1.2` and active Gemma `3.1` feature branches stable
    as doctrine controls while the doctrine experiment runs on the new `1.3`
    and `3.2` branches.
17. Treat the doctrine replacement effort as a shadow A/B experiment, not as a
    live-file rewrite on `main`.
18. Keep the round-one doctrine runtime schema unchanged and store extra
    doctrinal traceability in the companion audit package rather than in the
    runtime file itself.
19. Judge doctrine candidates on both:
    - doctrinal fit to the BDA corpus
    - prompt/eval fit on the held Qwen and Gemma cases
20. Keep the Gemma prompt cycle paused while the doctrine-sensitive A/B branch
    work clarifies whether doctrine text, not prompt text, is part of the
    remaining building-severity gap.

### Immediate Next Steps

The practical next sequence is:

- immediate sleep-handoff priority for the next session:
  - reopen the dirty Qwen `1.3` doctrine worktree first
  - diff the local `doctrine.yaml` and `config.yaml` pair against the logged
    `v002` doctrine-only checkpoint
  - decide whether that local pair is an intentional candidate worth
    validation, or whether it should be restored/cleaned before more Qwen or
    Gemma work

1. Keep PR `#134` frozen as the current Qwen review surface and do not
   reconcile its branch-history divergence until the team’s upstream decision
   makes that necessary.
2. Keep the active Qwen `1.2` and active Gemma `3.1` feature branches as the
   control lanes for doctrine A/B comparison.
3. Use the new `1.3` and `3.2` doctrine branches for all candidate doctrine
   file testing so `origin/main` and the active feature lines stay untouched.
4. Start doctrine evaluation with the doctrine-sensitive six-case guard set:
   - `destroyed_building4`
   - `operational_building7`
   - `tank_pressure`
   - `operational_tank4`
   - `destroyed_tank15`
   - `office_negative`
5. Compare doctrine-branch outputs against:
   - the parent active branch
   - the doctrine audit notes under
     `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/`
6. Treat the first Qwen doctrine candidate as a manual-review question, not an
   automatic winner:
   - it held the control cases
   - it also made `destroyed_building4` more severe
7. Treat the first Gemma doctrine candidate as a no-go for broader sweep
   unless a revision removes the reopened control regressions.
8. Only run the broader inherited pack if a doctrine guard set preserves the
   held controls and gives a better doctrinal tradeoff on the building cases.
9. Keep the user-local Gemma host path and the committed-tip-only `3.2` branch
   boundary documented so the doctrine experiment does not accidentally absorb
   unrelated Gemma prompt edits.

### 2026-04-21 — ChatGPT Deep Research Prompt Package Added For MCP And Tokenization Work

What changed:
- added a new local support bundle at:
  - `z_reference_docs/CHATGPT_DEEP_RESEARCH_PROMPTS_MCP_AND_TOKENIZATION.md`
- the new bundle includes:
  - one reusable project-context core
  - one paste-ready ChatGPT Deep Research prompt for MCP-server research
  - one paste-ready ChatGPT Deep Research prompt for tokenization and
    prompt-language research
  - short usage notes for when to run each research pass

Why it matters:
- the project now has a reusable outside-research handoff artifact that is
  grounded in the real local prompt-lab intent instead of a generic AI-tools
  request
- the MCP research prompt is explicitly biased toward:
  - document and context access first
  - mostly free or low-cost options
  - prompt/bbox relevance rather than popularity
- the tokenization research prompt is explicitly framed as a theory test, not
  as a pre-committed conclusion, and it asks for practical guidance tied back
  to bbox-sensitive prompt writing

Current consequence:
- future ChatGPT Deep Research runs on these two topics can start from a
  better project description without rebuilding the same context each time
- the new prompt package is a local-only support artifact under
  `z_reference_docs`, not a runtime contract or GitHub deliverable

### 2026-04-21 — Global SequentialThinking MCP Was Added To Codex Tooling

What changed:
- added a new global Codex MCP server entry for Sequential Thinking in:
  - `/home/williambenitez1/.codex/config.toml`
- installed a user-local Node runtime under:
  - `/home/williambenitez1/.local/lib/node-current/`
- linked the user-local runtime entrypoints at:
  - `/home/williambenitez1/.local/bin/node`
  - `/home/williambenitez1/.local/bin/npm`
  - `/home/williambenitez1/.local/bin/npx`
- added a short AGENTS rule so the project's root and active worktree AGENTS
  layers automatically prefer `sequentialthinking` for complex planning and
  debugging tasks when the global MCP server is available

Why it matters:
- the repo now has a globally configured structured-reasoning MCP server
  available to future Codex sessions after restart
- the AGENTS layer now makes the intended usage explicit instead of leaving the
  tool as hidden optional infrastructure
- the user-local Node runtime avoids needing system package changes just to
  launch this MCP server

Current consequence:
- a Codex restart is required before the new MCP server becomes available in
  session
- after restart, the expected smoke path is:
  - the `SequentialThinking` MCP server appears
  - complex planning or debugging prompts can invoke the
    `sequentialthinking` tool

### 2026-04-21 — Codex Subagent Catalog Was Vendored, Analyzed, And Routed For Selective Use

What changed:
- cloned the external repository:
  - `https://github.com/VoltAgent/awesome-codex-subagents`
  into the new global vendor path:
  - `/home/williambenitez1/.codex/vendor_imports/github.com/VoltAgent/awesome-codex-subagents`
- confirmed the existing GitHub fork under:
  - `https://github.com/metalbladex4/awesome-codex-subagents`
  is current with upstream
- wired the local vendor clone to both remotes:
  - `origin` -> VoltAgent upstream
  - `fork` -> `metalbladex4` fork
- added a new local analysis note at:
  - `z_reference_docs/CODEX_SUBAGENT_CATALOG_ANALYSIS.md`
- added a global AGENTS rule in:
  - `/home/williambenitez1/.codex/AGENTS.md`
  so future work inspects the vendored catalog before recommending or
  activating custom subagents

Why it matters:
- the project now has a reusable local source library for Codex custom
  subagents without polluting `~/.codex/agents/` with a bulk install
- the new analysis explicitly separates:
  - which subagents best fit this Capstone repo
  - which subagents are broadly useful across projects
- the setup now matches the repo's real behavior:
  - custom subagents are not auto-spawned
  - `.toml` files need selective installation and explicit delegation

Current consequence:
- future specialist-agent work can start from a stable local vendor copy
  instead of re-finding the external repo
- the Capstone-specific highest-value candidates are now documented as:
  - prompt and LLM workflow agents
  - Python and CLI agents
  - review/debug/test agents
  - documentation and research agents
- the collection should be treated as a selective catalog, not a
  "install-everything" toolbox

### 2026-04-21 — Global MCP Routing Was Hardened And The Selected Subagent Set Was Activated

What changed:
- rewrote the global Codex rules in:
  - `/home/williambenitez1/.codex/AGENTS.md`
  so tool routing now prefers:
  - MCP first when specific and appropriate
  - source-specific MCP servers and connectors over generic web when available
  - `playwright` as the default browser MCP
  - `filesystem` for in-root structured file inspection
- strengthened the `sequentialthinking` expectation so it is now preferred for
  complex reasoning and explicitly required before substantive updates to:
  - live maintained documents
  - global rules
  - any `AGENTS.md`
- added a new companion guide at:
  - `/home/williambenitez1/.codex/MCP_USAGE_GUIDE.md`
  with server-by-server usage, fallback, and anti-pattern guidance
- created the new global custom-agent install directory:
  - `/home/williambenitez1/.codex/agents/`
- selectively copied the approved global subagent subset from the vendored
  `awesome-codex-subagents` catalog into that directory
- added a local manifest in:
  - `/home/williambenitez1/.codex/agents/VENDOR_MANIFEST.md`
  recording source path, fork/upstream references, installed subset, vendor
  commit, and refresh guidance

Why it matters:
- the global environment now has a clearer tool-choice policy that is stronger
  than "use MCP sometimes" but still avoids the bad extreme of
  "use MCP no matter what"
- the new browser-routing split is now explicit:
  - `playwright` first for interaction-heavy browser workflows
  - `chrome-devtools` for live Chrome debugging and performance work
- the selected custom subagents are now globally available for explicit use
  without turning the full vendor catalog into noisy always-on global state

Current consequence:
- future Codex sessions now have a more explicit global routing baseline for:
  - reasoning tools
  - source-specific research tools
  - browser tools
  - filesystem-vs-shell decisions
- the vendored repository remains the review catalog for additional candidates,
  while the copied subset under `~/.codex/agents/` is the active globally
  available install set
- `/home/williambenitez1/.codex/config.toml` remained unchanged in this pass,
  so `filesystem` still applies only to the current Capstone and worktree roots

### 2026-04-21 — Sleep Handoff Was Re-Anchored On The Dirty Qwen `1.3` Doctrine Worktree

What changed:
- re-grounded the current project state from the startup-sweep docs and active
  worktree status instead of relying on the broader planned-next-step notes
- confirmed that the last completed logged Qwen doctrine-only checkpoint is:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/experiments/runs/doctrine_guard_set/run02_2026-04-20_190546_EDT/`
- confirmed that there is later uncommitted local work still sitting in the
  active Qwen doctrine worktree:
  - `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/src/bda_svc/pipeline/doctrine.yaml`
  - `/home/williambenitez1/Capstone_worktrees/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/src/bda_svc/pipeline/config.yaml`
- updated the doctrine and prompt-lab living docs so that next-session routing
  points back to that dirty Qwen `1.3` pair before any new Gemma or fresh
  prompt-only cycle is opened

Why it matters:
- the current local resume point is now documented as the real last active
  thread instead of being inferred later from memory
- this separates:
  - the last completed logged doctrine-only Qwen run
  - the later in-progress local candidate that still has no completed
    validation note
- it reduces the risk that the next session restarts on Gemma or opens a fresh
  Qwen prompt cycle before resolving the active doctrine-side local state

Current consequence:
- the next session should begin by diffing the dirty Qwen `1.3`
  `doctrine.yaml` and `config.yaml` pair against the logged `v002`
  doctrine-only checkpoint
- only after that diff should we decide whether to:
  - validate the local candidate
  - refine it further
  - or deliberately restore/clean it
- Gemma remains secondary until that Qwen doctrine handoff is resolved

### 2026-04-21 — Local Living Docs And AGENTS Layers Were Brought Up To The New Global Codex Baseline

What changed:
- updated the local living docs that describe workflow, routing, and writing
  support:
  - `z_reference_docs/REFERENCE_MASTER_INDEX.md`
  - `z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
  - `z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`
  - `z_reference_docs/capstone_tech_docs/understanding_tracking.md`
  - `z_reference_docs/CODEX_SUBAGENT_CATALOG_ANALYSIS.md`
- updated the canonical local AGENTS spec at:
  - `z_reference_docs/AGENTS.md`
- refreshed the discovered root, nested, and active worktree `AGENTS.md`
  files so they now explicitly point to:
  - `/home/williambenitez1/.codex/AGENTS.md`
  - `/home/williambenitez1/.codex/MCP_USAGE_GUIDE.md`
  - `/home/williambenitez1/.codex/agents/`
  - `/home/williambenitez1/.codex/vendor_imports/github.com/VoltAgent/awesome-codex-subagents`
- made the local documentation and AGENTS guidance explicit that
  `sequentialthinking` should be used before substantive updates to:
  - live maintained documents
  - global rules
  - any `AGENTS.md`

Why it matters:
- the local doc system no longer describes the MCP/subagent baseline as if it
  were still only planned state
- future sessions can recover the active global tooling overlay from repo-local
  docs instead of reconstructing separate `~/.codex` context from memory
- the canonical AGENTS spec and the discovered AGENTS files are now aligned
  again

Current consequence:
- every active AGENTS layer now explicitly inherits the current global
  MCP/subagent overlay
- the local docs now explain that global custom agents are available, but still
  intended for selective explicit use
- document-maintenance work now has a clearer structured-reasoning gate instead
  of relying on memory or scattered references

### 2026-04-17 — Gemma 4 E4B Model Line Bootstrap Began

What changed:
- created the next model branch and feature branch for the Gemma line:
  - `model/gemma4-e4b`
  - `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- created the new local prompt-lab root:
  - `z_reference_docs/Prompt_Labs/3_gemma4-e4b/`
- created the new local Gemma evidence pack:
  - `z_reference_docs/Prompting/Google_Gemma/Gemma_4/`
- pulled local copies of:
  - core official Gemma docs
  - official Gemma 4 model-card pages
  - Gemma 4 prompting-behavior pages
  - selected official cookbook notebooks
  - Gemma 4 launch/context blog references
- added a local synthesis note capturing the operational Gemma 4 prompt rules
  that matter before the first BDA baseline

What else changed:
- the Gemma model branch inherited the reusable prompt-lab review-artifact
  workflow and CI fix from the Qwen line
- the Gemma feature branch now carries a semantic port of the active Qwen
  `v009` prompt stack into `gemma4:e4b`
- this means the first Gemma line starts from the current best-known workflow
  shape rather than from the older `origin/main` prompt wording
- the first live Gemma run was attempted immediately afterward, but the local
  runtime blocked it:
  - installed Ollama version: `0.15.2`
  - `ollama pull gemma4:e4b` currently fails because Gemma 4 requires a newer
    Ollama release
- that environment gate was later resolved with a user-local Ollama `0.21.0`
  runtime; see:
  - `### 2026-04-17 — Gemma 4 Bootstrap Reached First Live \`v000\` Run`

Why it matters:
- it keeps the next model line branch-aware from day one
- it preserves direct comparability with:
  - `origin/main`
  - active Qwen `v009`
  - the now-recorded Gemma `v000` baseline
- it keeps the Gemma work local-first and evidence-first instead of turning the
  bootstrap into a larger infrastructure project
- it also surfaced the first real environment gate early, before we had mixed
  prompt revisions with runtime-version problems

### 2026-04-15 — Fresh Branch-Aware `v000` Baseline Recorded At `28e863b`

What changed:
- created the first real branch-aware active lab under
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/`
- copied the current live `src/bda_svc/pipeline/config.yaml` into the new
  branch-aware baseline snapshot
- created a fresh `v000_baseline.prompts.yaml`, run README, winners README,
  prompt version log, and baseline run manifest for that branch line
- ran the first clean baseline from the feature worktree against
  `tests/data/tank.jpg`

Observed result:
- `target_0.target_type`: `military_equipment`
- `target_0.damage_category`: `DESTROYED`
- `target_0.confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 102, 73]`
- `metadata.inference_time`: `10.85`

Why it mattered:
- this gives the post-reset feature line a real active baseline instead of
  forcing us to keep comparing against the preserved legacy `21deaf5` lab
- the bbox is materially tighter than the older legacy baseline
  `[51, 37, 128, 73]`, so future grounding work would have been misleading if
  we had kept using the older baseline as the active comparator
- the clean feature branch also confirmed that the earlier local
  `--debug-export-images` helper is not implicitly part of this new line

Current consequence:
- the active branch-aware `v000` baseline is now established
- future branch-line prompt or grounding iterations should compare against this
  `28e863b` baseline first
- the legacy lab remains useful history, but it is no longer the active
  baseline anchor for this feature line

### 2026-04-15 — `bda_eval` Became The Clean Branch Review-Artifact Path

What changed:
- extended `bda_eval` additively in the feature branch so it now emits:
  - combined overlays
  - per-condition overlays
  - per-condition crops
  - `bbox_review_sheet.jpg` for single-image comparison runs
- kept the existing `images_bbox_both` output behavior in place
- added a focused `bda_eval` test covering the new review-artifact generation:
  - result: `1 passed`

Why it mattered:
- the clean branch-aware feature line does not implicitly include the older
  local temporary `--debug-export-images` helper
- we still need the prompt-lab visual review artifact pattern to judge bbox
  grounding sanely
- using `bda_eval` as the artifact engine lets us stay closer to upstream
  design while still supporting prompt-grounding work

Current consequence:
- for this branch line, visual bbox review should now flow through `bda_eval`
  rather than through the older temporary `bda-svc` debug-export path

### 2026-04-15 — First Clean-Line `bda_eval` Run Root Was Confirmed

What changed:
- ran the first real branch-aware `bda_eval` layout smoke test at:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/layout_check/run02_2026-04-15_224230_EDT/`
- confirmed the run root now contains:
  - `bbox_review_sheet.jpg`
  - combined/reference/predicted overlays
  - reference/predicted crops
  - per-image review sheets
  - copied report folders
  - evaluation CSV

What else changed:
- `bda_eval` now skips LLMaaJ logic scoring when `OLLAMA_API_KEY` is missing
  instead of aborting bbox artifact generation
- `bda_eval` now skips copytree operations when the source report folder is
  already the same directory as the intended destination under the run root

Current consequence:
- the clean branch-aware prompt-lab line now has a working end-to-end bbox
  review path rooted in `bda_eval`

### 2026-04-15 — Branch-Aware `v001` Ran As The First Real Candidate

What changed:
- drafted and ran:
  - `v001_detect_objects_short-contrastive-grounding.yaml`
- compared it against the fresh branch-aware baseline using the confirmed
  `bda_eval` artifact path

Result:
- baseline: `[51, 37, 102, 73]`, `DESTROYED`, `PROBABLE`
- `v001`: `[46, 46, 123, 92]`, `DESTROYED`, `CONFIRMED`

Current consequence:
- `v001` is the strongest branch-aware detection improvement signal so far
- but it is not an overall winner because it reintroduced subtype/context drift
  and confidence inflation at the same time

### 2026-04-15 — Branch-Aware `v002` Preserved The Box And Softened Confidence

What changed:
- ran `v002` as an assessment-only follow-up on top of `v001`

Result:
- kept bbox `[46, 46, 123, 92]`
- pulled confidence down from `CONFIRMED` to `PROBABLE`
- removed target-level subtype drift
- but overcorrected `DESTROYED` down to `DAMAGED`

Current consequence:
- the stronger branch-aware bbox can survive downstream prompt changes
- the next assessment iteration should focus on recovering `DESTROYED` without
  losing `PROBABLE`

### 2026-04-15 — Branch-Aware `v003` Became The Best Combined Candidate

What changed:
- ran `v003` as the next assessment-only follow-up on top of the stronger
  `v001` detection behavior

Result:
- kept bbox `[46, 46, 123, 92]`
- recovered `DESTROYED`
- kept `PROBABLE`
- kept subtype drift out of target-level logic
- summary still overreaches on terrain/function wording

Current consequence:
- `v003` is now the current branch-aware working leader
- the next prompt cycle should freeze detection and target assessment, then
  focus on `summarize_scene`

### 2026-04-15 — Branch-Aware `v003` Repeat Held Exactly

What changed:
- reran `v003` unchanged as `run02`

Result:
- bbox `[46, 46, 123, 92]` repeated
- `DESTROYED` repeated
- `PROBABLE` repeated
- target-level logic repeated
- only routine metadata fields changed

Current consequence:
- `v003` is now a confirmed branch-aware working leader, not just a single-run
  result
- the next prompt cycle should move to `summarize_scene`

### 2026-04-15 — Branch-Aware `v004` Became The Provisional Full-Stack Leader

What changed:
- ran `v004` as a summary-only follow-up on top of the confirmed `v003` base

Result:
- bbox held at `[46, 46, 123, 92]`
- `DESTROYED` held
- `PROBABLE` held
- summary wording became materially more conservative and generic

Current consequence:
- `v004` is the provisional best end-to-end branch-aware candidate
- the next step should be a single confirmation repeat

### 2026-04-16 — Branch-Aware `v004` Repeat Held Exactly

What changed:
- reran `v004` unchanged as `run02`

Result:
- bbox `[46, 46, 123, 92]` repeated
- `DESTROYED` repeated
- `PROBABLE` repeated
- improved summary repeated

Current consequence:
- `v004` is now the confirmed full-stack branch-aware leader

## Current Prompt-Lab State

The preserved legacy prompt lab is:

- `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/`

The new branch-aware qwen root is:

- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/`

The previous lab is archived at:

- `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/`

Current prompt chain state:

- active lab:
  - `v000_baseline.prompts.yaml` is refreshed from current `main` at `21deaf5`
    with no prompt-text change relative to the earlier `c077cd8` active
    baseline
  - `v001` and `v002` have both been run and rejected as winning directions
  - `v003` has now been run once and is also not a winning direction
  - `v004` has now been run once as the first critique/research/revise-loop
    candidate and is also not a winning direction
  - `v005` through `v010` now cover the rest of the active prompt sequence:
    `v006` is the best bbox candidate, `v009` is the current best assessment
    candidate, and `v010` is the first rejected `_pixels` grounding experiment
- archived lab:
  - `v001` through `v004` preserve the pre-merge draft history
  - `v005` through `v010` preserve the first reconciled and follow-up sequence

Current local eval assets include:

- a current seed case from `tests/data/tank.jpg`
- archived timestamped overlay and crop images from earlier live experiment
  runs
- archived timestamped JSON reports stored under the archived lab
- a fresh baseline run recorded in the active lab under
  `experiments/runs/baseline/run01_2026-04-10_205704_EDT/`
- active eval manifests updated with the first fresh baseline report, bbox, and
  debug image references

Interpretation note:
- anything run before `2026-04-10` is now explicitly historical and should not
  be treated as active evidence for the `qwen3-vl:8b-instruct` sequence
- the first fresh active baseline now becomes the evidence anchor for the new
  sequence
- the latest upstream sync did not invalidate the active sequence, so `v000`
  through `v004` remain the current working evidence
- the active prompt workflow now has a parallel research tree at
  `z_reference_docs/Prompting/Research_Loops/`
- `v009` is the current best assessment candidate, and the frozen `v006` +
  `v009` pair is the best-known combined prompt direction so far
- `v010` has now been run and rejected, so the next move should stay
  grounding-first but shift to a different tactic than the direct `_pixels`
  contract swap
- the cross-image sweep suggests the pair is not obviously tank-only, but the
  tank seed still needs repeatability attention
- a later cross-image generalization sweep on frozen `v006` + `v009`
  generalized reasonably on truck and office scenes, but the tank seed still
  remained the pressure point

## Current Live Debugging State

The live CLI now supports a **temporary** debug export flag:

- `--debug-export-images`

This saves:

- the JSON report
- one overlay image per target
- one crop image per target

It exists only to support prompt tuning and bbox inspection and should be
removed after the prompt work is complete.

It is now layered on top of the newer upstream export behavior that adds
`metadata.inference_time`, so the local temporary instrumentation and upstream
runtime changes currently overlap in `app.py` and `export.py`.

## Current Capstone Documentation State

As of `2026-04-06`, we have started Phase 3 deployment-procedure drafting under:

- `z_reference_docs/capstone_tech_docs/Deliverables_Phase_3_(S26-P1)/Deployment procedure Draft.docx`

Current interpretation:

- current `upstream/main` is the technical source of truth for the deployment
  procedure
- the Phase 3 deployment template provides the expected section structure
- Phase 1 and Phase 2 materials remain useful internal context, but the draft
  itself should sound authoritative and should not explain requirements as
  provisional assumptions from older deliverables
- the draft intentionally excludes local prompt-lab work and temporary
  debug-export instrumentation
- the next documentation refinements should come after code verification and
  teammate Phase 3 documents become available

## Active Risks / Watch Items

- The first manual seed bbox was wrong and had to be corrected by comparing it
  to the live output.
- The first seed case is only one `military_equipment` example, so the current
  eval base is too small to support broad prompt decisions yet.
- The current summary prompt still allows some broader impact language, so it
  needs careful review to avoid drifting beyond Phase 1 physical damage.
- Prompt versions exist in the lab, but none have been promoted into the live
  `src/bda_svc/pipeline/config.yaml` yet.
- The new active prompt lab has a refreshed `v000` baseline, but the first new
  baseline run under the reorganized structure has now happened and needs
  manual visual review.
- The first fresh active baseline still shows bbox-localization weakness, so
  new prompt work should focus on detection grounding before confidence tuning.
- The confidence drop from `CONFIRMED` to `PROBABLE` may be downstream of the
  widened bbox and looser crop, not an isolated assessment problem.
- The updated doctrine wording now explicitly mentions locomotives under
  `military_equipment`, so subtype drift should be monitored during prompt
  review.
- `v003` showed that a tighter numeric bbox can still be semantically wrong, so
  overlay review remains mandatory before promoting any detection draft.
- `v004` showed that anchoring to the nearest fire-adjacent body patch can make
  the box smaller while still missing the real target body.
- `v005` showed that a longer point-first grounding prompt can be too weak to
  change the model at all.
- `v006` showed that a shorter, contrastive-example prompt can improve bbox
  placement, but that a detection-only change can still shift downstream
  confidence and summary behavior.
- Some stubborn grounding failures may be partly backend-sensitive, so repeated
  prompt misses should be checked against runtime variance before we conclude
  that the YAML architecture itself is wrong.
- The current summary problem is real, but grounding is still the higher-risk
  blocker; the next experiment should therefore test a native pixel-coordinate
  path before spending a full cycle on summary wording.
- The temporary debug-export changes overlap active upstream runtime/export
  files, so future syncs or rebases may continue to require careful conflict
  resolution until that temporary instrumentation is removed.

## Change Entries

### 2026-04-20 — Phase-1 Doctrine Replacement Was Staged As A Local-Only Shadow Experiment

What changed:

- created a local-only doctrine audit package under:
  `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/`
- recorded:
  - a doctrine source crosswalk
  - a preserve/adapt/exclude matrix
  - Phase-1-only scope rules
  - a first prompt-compatible runtime candidate doctrine file
  - a branch/worktree test playbook
- created two new doctrine experiment worktrees from the active feature lines:
  - Qwen:
    `feat/qwen3-vl-8b-instruct/doctrine-bda-alignment`
  - Gemma:
    `feat/gemma4-e4b/doctrine-bda-alignment`
- applied the first runtime candidate doctrine only in those doctrine branches
- ran local runtime contract checks in both doctrine branches:
  - `uv run pytest tests/unit/test_yamls.py tests/unit/test_utilities.py`

Observed result:

- the first doctrine candidate keeps the current runtime schema intact
- both new doctrine branches passed the static runtime checks cleanly
- the active Qwen and Gemma feature branches remain untouched as control lanes
- the Gemma doctrine branch was intentionally created from committed tip
  `9ae27e9` rather than absorbing the dirty active `3.1` worktree state

Why it matters:

- doctrine can now be tested as an isolated A/B surface instead of being mixed
  into live prompt or runtime changes on `main`
- the experiment now has a clear evidence trail:
  - doctrinal audit
  - candidate rationale
  - controlled worktree testbeds
  - staged evaluation plan

### 2026-04-20 — The First Doctrine Guard-Set Run Produced A Split Qwen/Gemma Read

What changed:

- staged a standardized six-case doctrine guard-set input pack in both doctrine
  branch labs
- ran the first candidate doctrine on that six-case pack in:
  - Qwen `1.3`
  - Gemma `3.2`
- restored the user-local Gemma host on `127.0.0.1:11435`
- pulled `gemma4:e4b` into that user-local host so the Gemma doctrine branch
  could execute cleanly again

Observed result:

- Qwen held the intact, destroyed-equipment, negative, and tank-pressure
  controls
- Qwen returned two destroyed buildings on `destroyed_building4`, making the
  building-severity question sharper rather than resolving it automatically
- Gemma held `tank_pressure`, `destroyed_tank15`, and `office_negative`
- Gemma reopened two control regressions:
  - `operational_tank4` returned to `DAMAGED / PROBABLE`
  - `operational_building7` gained a false-positive
    `military_equipment` detection

Why it matters:

- the doctrine candidate is not behaving uniformly across model families
- the first candidate is worth deeper manual review on Qwen because it may be
  surfacing a real doctrinal tradeoff on building severity
- the same candidate should not advance to a broader inherited Gemma sweep in
  its current form because it reopened control-case behavior we had already
  recovered

### 2026-04-03 — Working Changelog Created

Purpose of this entry:
- establish one place to track project understanding, current direction, and
  meaningful changes as the project evolves

State captured:
- live runtime understanding
- current prompt-lab strategy
- current prompt draft status
- current debug-export status
- current risks and open issues

### 2026-04-03 — Prompt Methodology Record Added

What changed:
- Added `z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md` as the dedicated
  living document for prompt-development method, source usage, experiment
  rationale, and directional changes.

Why it mattered:
- The working changelog is good for overall project state, but we also needed a
  prompt-specific record that can support a presentation, write-up, or verbal
  explanation of methodology later.
- This creates a stable place to document how doctrine, model docs, and general
  prompting guides are actually influencing prompt decisions over time.

Status:
- created
- seeded with current methodology baseline and work completed so far
- should be revisited periodically during major prompt-method changes

### 2026-04-03 — Separate Inspection Worktree Added For Upstream Feature Branch

What changed:
- Added a separate worktree at
  a temporary inspection workspace for `upstream/feature/add-export-metrics`.
- Saved a temporary multi-root VS Code workspace so the main repo and
  inspection worktree could be opened together.

Why it mattered:
- The active prompt workspace already has local work in progress.
- A separate worktree gives us a safe way to inspect feature-branch changes
  without disturbing prompt-lab work on `main`.

Status:
- inspection workspace created
- safe side-by-side review enabled
- later retired after PR `#124` merged into `main`

### 2026-04-03 — First Inspection Pass Completed On `feature/add-export-metrics`

What changed:
- Completed a first pass comparing the feature branch against `main`.

### 2026-04-10 — First Fresh Baseline Run Recorded In The New Active Lab

What changed:
- Ran the first baseline experiment in
  `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/`.
- Recorded the run under the new version-first structure at:
  `experiments/runs/baseline/run01_2026-04-10_205704_EDT/`
- Updated the active eval manifests with the baseline JSON, overlay, crop, and
  reference bbox.

Headline baseline result:
- `target_0.target_type`: `military_equipment`
- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `bounding_box`: `[51, 37, 128, 73]`

Why it mattered:
- This establishes the first true evidence anchor for the restarted
  `qwen3-vl:8b-instruct` sequence.
- It confirms that the new active lab is operational and the bookkeeping
  structure works as intended.
- It also shows that bbox localization remains the primary quality problem in
  the new sequence.

Interpretation:
- Compared with the archived baseline, the box widened to the right while
  staying anchored to the same general region.
- This still looks like a model localization behavior issue, not a conversion
  bug.
- The confidence drop from `CONFIRMED` to `PROBABLE` is likely downstream of
  weaker localization and a looser crop.
- The appearance of `locomotive` in the supporting logic is plausibly
  influenced by updated doctrine wording that now explicitly includes
  locomotives under `military_equipment`.

Decision:
- Start the next prompt sequence with a detection-localization change first.
- Do not tune confidence in isolation yet.

### 2026-04-10 — `v001` Drafted For Detection-Only Tightening

What changed:
- Drafted the first new active-sequence prompt candidate:
  `v001_detect_objects_visible-boundary-tightening.yaml`
- Kept `v000` as the parent and changed only `detect_objects`.

Why it mattered:
- The first fresh baseline showed the bbox widening on the right edge while the
  target stayed anchored to the same general region.
- That made detection localization the clearest next prompt surface to test in
  the restarted sequence.

What `v001` is trying to do:
- make the model anchor the bbox to visible solid target boundaries
- stop the box at the last clearly visible physical edge
- avoid extending the box through smoke, plume, rails, road, ground, or other
  scene context
- preserve the current runtime contract, schema, placeholders, and code

Status:
- later run twice against the active baseline
- useful as evidence, but not a clean enough win to promote

What was learned from `v001` runs:
- The baseline repeated exactly across `run01` and `run02`.
- `v001` did not repeat exactly:
  - `run01` bbox: `[56, 46, 123, 79]`
  - `run02` bbox: `[56, 46, 123, 85]`
- `v001` stayed only directionally similar rather than cleanly stable.
- Confidence rose to `CONFIRMED`, but the box was still visually off target.
- Subtype drift toward `locomotive` remained, and summary text still became too
  specific.

Decision:
- Keep `v001` as evidence, not as a winner.
- Continue to a different detection-localization tactic rather than refining
  `v001` directly.

### 2026-04-10 — `v002` Drafted As An Alternative Detection Tactic

What changed:
- Drafted
  `v002_detect_objects_edge-by-edge-grounding.yaml`
- Used `v000` as the parent and treated `v002` as an alternative to `v001`,
  not a continuation of it.

Why it mattered:
- `v001` showed that prompt wording could move the box, but the improvement was
  marginal and not stable enough.
- That suggested the next attempt should use a more explicit spatial rule
  rather than another general tightening instruction.

What `v002` is trying to do:
- force each bbox edge to land on visible solid target structure
- move any edge inward if it falls on smoke, rails, ground, shadow, or other
  scene context
- prefer a slightly too-tight structure-grounded box over a broader context box
- preserve the current runtime contract, schema, placeholders, and code

Status:
- drafted
- not yet run
- should be evaluated directly against the same seed image and compared against
  both baseline and `v001`

### 2026-04-12 — Critique / Research / Revise Loop Started

What changed:
- Added a structured loop workflow for the active prompt lab:
  run -> critique -> research -> revise.
- Added `CRITIQUE.md` as a required run-level artifact.
- Added `z_reference_docs/Prompting/Research_Loops/` as the paired research
  tree for active prompt experiments.

Why it mattered:
- This turns each failed version into reusable evidence instead of a one-off
  experiment.
- It creates a cleaner bridge between run review and the next candidate draft.

### 2026-04-12 — `v004` Rejected As A Fire-Source Anchoring Tactic

What changed:
- Drafted and ran
  `v004_detect_objects_fire-source-object-body.yaml`.
- Recorded the first paired critique and research note for the active loop.

Headline result:
- baseline bbox: `[51, 37, 128, 73]`
- `v004` bbox: `[51, 37, 102, 61]`
- confidence stayed `PROBABLE`

What was learned:
- `v004` kept the tighter right edge but also cut the bottom edge upward,
  making the crop less aligned with the target body than `v003`.
- The prompt over-focused on the fire-adjacent patch instead of recovering the
  visible attached object body.
- Subtype drift worsened to `locomotive or rolling stock` in supporting logic
  and `likely a locomotive or heavy transport` in the summary.

Decision:
- reject `v004` as a direction
- keep only the narrower lesson that fire/smoke should remain search cues, not
  bbox boundaries
- use the next draft to test point-or-center-first, occlusion-aware grounding

### 2026-04-12 — `v005` Rejected As A No-Effect Wording Family

What changed:
- Drafted and ran
  `v005_detect_objects_point-first-occlusion-aware.yaml`.
- Recorded the second paired critique and research note for the active loop.

Headline result:
- baseline bbox: `[51, 37, 128, 73]`
- `v005` bbox: `[51, 37, 128, 73]`
- confidence stayed `PROBABLE`
- supporting logic and summary matched the baseline wording exactly

What was learned:
- The point-first, occlusion-aware idea may be conceptually sound, but the
  wording was too weak to become salient.
- When the model ignores a longer grounding block, the next move should be a
  shorter and more example-driven prompt, not more abstract prose.

Decision:
- reject `v005` as a no-effect wording family
- draft `v006` from `v000` with a shorter, contrastive-example detection prompt

### 2026-04-12 — `v006` Became The Best BBox Candidate In Cycle 01

What changed:
- Drafted and ran
  `v006_detect_objects_short-contrastive-example.yaml`.
- Completed `cycle01_v004-v006_summary.md`.

Headline result:
- baseline bbox: `[51, 37, 128, 73]`
- `v006` bbox: `[46, 46, 128, 92]`
- confidence changed from `PROBABLE` to `CONFIRMED`

What was learned:
- `v006` is the first active-sequence candidate to move the box materially onto
  the visible burning target body.
- The shorter, contrastive-example style appears more salient than the longer
  abstract grounding prompts used in `v004` and `v005`.
- The bbox improvement is not yet a clean promotion because downstream
  confidence and summary behavior also shifted.

Decision:
- treat `v006` as best-so-far, not yet promoted
- recommend one confirmation repeat of `v006` before moving on to the next
  prompt problem

### 2026-04-12 — `v006` BBox Win Confirmed On Repeat

What changed:
- Ran `v006` confirmation `run02`.

Headline result:
- `v006` run02 matched `run01` exactly:
  - bbox `[46, 46, 128, 92]`
  - confidence `CONFIRMED`
  - same supporting logic
  - same summary

What was learned:
- The bbox improvement is repeatable on the current seed case.
- The next prompt issue is no longer basic bbox placement for this case.
- The next prompt issue is downstream calibration:
  - confidence inflation
  - stronger summary/impact language

Decision:
- treat `v006` as a confirmed bbox win for this seed case
- do not promote it yet as a full winner until downstream assessment/summary
  behavior is handled

### 2026-04-03 — Prompt Labs Renamed And Split By Branch Context

What changed:
- Renamed the original main-branch prompt lab to
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/`.
- Added a temporary second prompt lab for the inspection branch.

Why it mattered:
- We needed outputs, eval assets, and experiment notes to stay separated by
  branch source instead of only by model name.
- This makes future comparisons between `main` and
  `feature/add-export-metrics` much cleaner.

Retirement note:
- This temporary second lab was later removed once PR `#124` landed in `main`
  and the active prompt workflow collapsed back to the main lab only.

Status:
- main lab renamed
- export-metrics lab scaffolded
- documentation updated to point to the new main-lab path

### 2026-04-03 — Main vs Export-Metrics Baseline Prompt Comparison Completed

What changed:
- Compared the baseline prompt set in the main lab against the baseline prompt
  set in the export-metrics inspection lab before running any new branch
  experiments.

What was learned:
- The shared `system` prompt is effectively the same.
- The main prompt difference is in `detect_objects`.
- The export-metrics branch moves detection toward:
  - doctrine-guided detection instructions
  - runtime-configured bbox formatting and scaling
- The main branch keeps a more self-contained detection prompt with explicit
  counting, consistency, and `0–1000` xyxy box instructions.
- `assess_damage` and `summarize_scene` only changed lightly in wording on the
  export-metrics branch.

Why it mattered:
- This gave us a clean prompt-level map of the branch before starting new
  branch-specific experiments.
- It also clarified that `detect_objects` should be the first branch-specific
  prompt surface to watch closely if we needed to work on that branch.

### 2026-04-06 — `main` Absorbed PR `#124` And Prompt Work Recentered On Main

What changed:
- `upstream/main` absorbed the former `feature/add-export-metrics` work via
  PR `#124`.
- Local `main`, `origin/main`, and `upstream/main` were resynced.
- The temporary local debug-export changes were reapplied and merged on top of
  the new `main`.

What it means:
- The former export-metrics branch is no longer a separate active prompt target.
- The live `main` prompt/runtime contract now includes the changes we had been
  inspecting in parallel.
- Prompt work should now focus on the main lab only.

Follow-on action completed:
- retired the export-metrics-specific prompt lab and inspection setup
- restored the saved workspace to the main repo only
- kept the next prompt-work step focused on refreshing the main-lab baseline
  against the new live `main`

### 2026-04-06 — Forward Path Simplified To Main-Only Prompt Development

What changed:
- The active prompt-development path is now fully centered on current `main`.
- The old branch-comparison phase is complete.
- The remaining work is now baseline refresh, eval refresh, and continued prompt
  iteration from the main lab.

What we are doing next:
- refresh main-lab baseline files
- regenerate current-main baseline outputs
- update stale eval assumptions
- adapt the drafted prompt chain to the current live contract before new prompt
  experiments continue

Why it matters:
- this gives the project one clear source of truth again
- it reduces workflow overhead and makes the methodology easier to explain
- it turns the next stage into prompt refinement on top of the merged runtime,
  rather than prompt work across competing branch contexts
  prompt surface we focus on later.

### 2026-04-06 — Phase 3 Deployment Procedure Draft Created

What changed:
- Created the initial deployment procedure draft at
  `z_reference_docs/capstone_tech_docs/Deliverables_Phase_3_(S26-P1)/Deployment procedure Draft.docx`.
- Structured the draft around the Phase 3 deployment-procedure template while
  keeping the tone close to the earlier capstone deliverables.
- Anchored technical content to `upstream/main`.
- Removed local-only prompt-lab and temporary debug-export references from the
  draft.
- Rewrote hardware requirements to read authoritatively instead of as
  provisional assumptions.

Why it mattered:
- This gives the team a usable first draft for the Phase 3 deployment
  deliverable.
- It creates a clean separation between team-facing documentation and our local
  prompt-development workspace.
- It lets us return to implementation/testing with the documentation state
  captured and ready for the next teammate-context pass.

Next documentation checkpoint:
- revisit the draft after commands, runtime assumptions, and target deployment
  environment details are verified against the current code
- refine the draft again after teammates provide the local tests, customer
  verification, and model documentation updates

### 2026-04-06 — Environment Resynced After Upstream/Main Update

What changed:
- Confirmed local `main`, `origin/main`, and `upstream/main` are aligned.
- Ran `uv sync --dev` after the upstream update so the local environment
  matches the updated `uv.lock`.
- Confirmed the new upstream dependency `json-repair==0.58.7` is installed.
- Ran the full test suite with `uv run pytest`.

Verification:
- test result: `35 passed`

Current local state:
- upstream/main is synced locally
- implementation tests are passing
- the remaining working-tree changes are the local temporary debug-export files:
  `src/bda_svc/app.py`, `src/bda_svc/cli.py`,
  `src/bda_svc/export.py`, and `tests/unit/test_export.py`
- those temporary debug-export changes remain separate from team-facing
  deployment documentation and prompt-lab artifacts

Why it mattered:
- this confirms the local environment is consistent with the merged upstream
  runtime before we return to project testing and prompt work
- it also confirms that the temporary debug-export work still coexists with the
  updated upstream runtime after the earlier conflict resolution

### 2026-04-06 — Prompt Methodology Updated For Current Runtime Contract

What changed:
- Reviewed `PROMPT_DEVELOPMENT_METHODOLOGY.md` against the synced
  `upstream/main` prompt/runtime files.
- Updated the methodology to reflect the current parameterized detection
  contract:
  - `{detection_guidance}`
  - `{bbox_format}`
  - `{bbox_scale}`
  - configurable `detection_vlm.bbox_convention`
- Added notes for current runtime support that now affects prompt evaluation:
  - `json-repair`
  - `think=False`
  - model environment overrides

Why it mattered:
- the former static detection-prompt baseline is now historical context
- future prompt experiments should preserve the current live detection
  placeholders unless intentionally testing a code-level prompt-contract change
- schema-validity results now need to account for both prompt wording and
  runtime parsing behavior

Next prompt-work step:
- refresh the main-lab baseline from current `upstream/main`
- reconcile `v001` through `v004` against the current live contract before new
  experiments continue

### 2026-04-06 — Main Prompt Lab Baseline Refreshed And Reconciled

What changed:
- Refreshed
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/baseline/config.pipeline-baseline.yaml`
  from `upstream/main:src/bda_svc/pipeline/config.yaml`.
- Refreshed `v000_baseline.prompts.yaml` as the current-main prompt baseline.
- Preserved `v001` through `v004` as pre-merge draft history.
- Added the post-merge reconciled prompt chain:
  - `v005_system_short-policy_postmerge.yaml`
  - `v006_assess_damage_single-target_postmerge.yaml`
  - `v007_detect_objects_parameterized-grounding.yaml`
  - `v008_summarize_scene_consistent-plaintext_postmerge.yaml`
- Updated the prompt version log and lab README.

Verification:
- refreshed baseline config body matches `upstream/main`
- refreshed baseline and `v005` through `v008` parse as valid YAML

Why it mattered:
- the prompt lab now matches the current live detection/runtime contract before
  new experiments continue
- the old hardcoded `xyxy_1000` detection draft remains preserved as history,
  but the active reconciled detection candidate now keeps
  `{detection_guidance}`, `{bbox_format}`, and `{bbox_scale}`

Next prompt-work step:
- regenerate current-main baseline outputs
- update stale eval references and seed assumptions
- evaluate `v005` through `v008` against the refreshed baseline

### 2026-04-06 — First Timestamped Baseline vs Reconciled Chain Run

What changed:
- Updated prompt-lab eval manifests to use the current repo fixture
  `tests/data/tank.jpg`.
- Ran a timestamped prompt-lab experiment under
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/experiments/runs/2026-04-06_203823_EDT/`.
- Compared two conditions:
  - `current-main_baseline`
  - `v008_reconciled-chain`
- Added a `RUN_MANIFEST.md` for the run.

Headline result:
- both conditions produced one `military_equipment` detection
- both assessed the target as `DESTROYED` with `CONFIRMED` confidence
- current-main baseline bbox: `[51, 37, 102, 73]`
- `v008` reconciled-chain bbox: `[51, 49, 115, 85]`
- `v008` produced a more constrained summary and avoided the baseline's
  stronger "zero combat capability" phrase

Decision:
- no prompt accepted or rejected from this single seed run
- next step is manual visual review of the saved overlay/crop images and then
  more eval coverage before promotion decisions

### 2026-04-06 — Bbox Visual Review Found Off-Target Localization

What changed:
- Reviewed the saved overlay/crop images from
  `experiments/runs/2026-04-06_203823_EDT/`.
- Created a side-by-side `bbox_review_sheet.jpg`.
- Captured raw VLM detection responses in
  `experiments/runs/2026-04-06_203823_EDT/raw_detection_responses.md`.
- Added `DET-09 bbox_off_target` to the prompt-lab failure taxonomy.
- Updated the run manifest and prompt version log.

Finding:
- both the baseline and `v008` bboxes are visually off target
- baseline raw bbox: `[200, 300, 400, 600]`, exported pixel bbox:
  `[51, 37, 102, 73]`
- `v008` raw bbox: `[200, 400, 450, 700]`, exported pixel bbox:
  `[51, 49, 115, 85]`
- the runtime conversion is consistent with `xyxy_1000`, so this is a VLM
  localization failure rather than a conversion/export bug

Decision:
- do not promote `v008` from this run
- next prompt work should focus on detection localization and bbox/crop
  reliability before evaluating summary improvements

### 2026-04-06 — `v009` Detection-Only Candidate Drafted

What changed:
- Created
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/experiments/versions/v009_detect_objects_physical-target-only.yaml`.
- Updated the prompt version log and lab README.
- Updated the prompt methodology record with the new detection-focused follow-up.

Current understanding:
- `v009` is parented to `v008`, but changes only `detect_objects`.
- The intended fix is to steer Qwen toward boxing the physical target object,
  not fire, smoke, plume effects, terrain, roads, shadows, or other damage
  effects.
- The runtime contract is unchanged: `{detection_guidance}`, `{bbox_format}`,
  `{bbox_scale}`, and the `DetectionResponse` JSON fields are preserved.

Current way forward:
- Run a new timestamped experiment comparing the refreshed current-main
  baseline and `v009`.
- Visually compare the `v009` overlay/crop against the prior baseline and
  `v008` outputs from `2026-04-06_203823_EDT`.
- Do not revisit summary-prompt promotion until detection bbox reliability is
  improved.

### 2026-04-06 — `v009` Experiment Run Completed And Rejected

What changed:
- Ran a new timestamped experiment under
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/experiments/runs/2026-04-06_210720_EDT/`.
- Compared current-main baseline against `v009_physical-target-only` on
  `tests/data/tank.jpg`.
- Created `bbox_review_sheet.jpg`.
- Updated the run manifest, failure taxonomy, prompt version log, methodology,
  and lab README.

Result:
- current-main baseline bbox: `[51, 37, 102, 73]`
- `v009` bbox: `[51, 49, 128, 73]`
- `v009` remained visually off target and still emphasized the smoke/plume
  region rather than the physical target body
- `v009` introduced unsupported "locomotive" identity detail in the assessment
  and summary

Decision:
- reject `v009` for now
- keep detection localization as the active blocker
- next prompt candidate should use a different localization strategy rather
  than only adding more forbidden-effect wording

### 2026-04-06 — `v010` Effect-Cue-Anchored Detection Candidate Drafted

What changed:
- Created
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/experiments/versions/v010_detect_objects_effect-cue-anchored.yaml`.
- Updated the prompt version log, lab README, and prompt methodology record.

Current understanding:
- `v010` is parented to `v008`, not rejected `v009`.
- It still changes only `detect_objects`.
- The new strategy treats fire, smoke, scorch marks, blast marks, and debris as
  cues that a damaged target may be nearby, then anchors bbox placement to
  visible solid target structure.
- The runtime contract is unchanged: `{detection_guidance}`, `{bbox_format}`,
  `{bbox_scale}`, and the `DetectionResponse` JSON fields are preserved.

Current way forward:
- Run a new timestamped experiment comparing the refreshed current-main
  baseline and `v010`.
- Visually compare `v010` against the prior baseline, `v008`, and rejected
  `v009` overlay/crop outputs before making any promotion decision.

### 2026-04-06 — `v010` Experiment Run Completed And Rejected

What changed:
- Ran a new timestamped experiment under
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/experiments/runs/2026-04-06_212840_EDT/`.
- Compared current-main baseline against `v010_effect-cue-anchored` on
  `tests/data/tank.jpg`.
- Built a combined `bbox_review_sheet.jpg` with source, current baseline,
  `v008`, rejected `v009`, and `v010`.
- Wrote `result_summary.json`.
- Updated the run manifest, prompt version log, methodology, and lab README.

Result:
- current-main baseline bbox: `[51, 37, 102, 73]`
- `v008` bbox: `[51, 49, 115, 85]`
- rejected `v009` bbox: `[51, 49, 128, 73]`
- `v010` bbox: `[51, 49, 128, 85]`
- `v010` no longer introduced the unsupported "locomotive" identity detail
  from `v009`
- `v010` still boxed the smoke/plume region rather than the physical target
  body

Decision:
- reject `v010` for now
- detection localization remains the active blocker
- next prompt work should test a more concrete spatial localization strategy
  rather than only semantic cue/effect wording

### 2026-04-06 — Current-Main Baseline Experiment Run Created

What changed:
- Created a timestamped experiment output folder:
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/experiments/runs/2026-04-06_202124_EDT/`.
- Ran the current live main baseline against `tests/data/tank.jpg`.
- Stored the JSON report and temporary debug overlay/crop images under the
  timestamped run folder.
- Added a run manifest and a reusable `experiments/runs/README.md`.
- Established the standing convention that future experiment outputs go into
  timestamped subfolders.

Headline result:
- detections: `1`
- target type: `military_equipment`
- damage category: `DESTROYED`
- confidence level: `CONFIRMED`
- bounding box: `[51, 37, 102, 73]`
- inference time: `13.36`

Why it mattered:
- this gives us a fresh current-main baseline output after the upstream/runtime
  sync
- it keeps experiment artifacts auditable by timestamp
- it gives us a clean baseline before evaluating the reconciled `v005` through
  `v008` prompt chain

### 2026-04-02 — Temporary Live Debug Export Added

What changed:
- Added an optional live-side debug export path so each run can save overlay and
  crop images automatically.

Files changed:
- `src/bda_svc/cli.py`
- `src/bda_svc/app.py`
- `src/bda_svc/export.py`
- `tests/unit/test_export.py`

Why it mattered:
- We needed a fast way to inspect the model’s actual detected bbox and crop
  behavior during prompt tuning.
- The normal live pipeline only exported JSON, which made bbox review slower and
  more error-prone.

Status:
- implemented
- tested
- intentionally temporary

### 2026-04-02 — First Seed Eval Case Annotated

What changed:
- Annotated the first seed case using `tests/test_images/01.jpg`.
- Created local overlay/crop assets for the seed case.
- Copied the live debug JSON report into the same prompt-lab asset folder for
  quick reference.

Files/areas involved:
- `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/evals/system_assess_track.yaml`
- `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/evals/detect_track.yaml`
- `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/evals/summarize_track.yaml`
- `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/evals/assets/system_assess/`

Why it mattered:
- This gave us the first concrete baseline case for prompt comparisons.
- It also exposed that the original manual bbox estimate was wrong.

Status:
- seed case available
- still needs companion cases before we can trust broader prompt judgments

### 2026-04-10 — Prompt Labs Reorganized Around Current `qwen3-vl:8b-instruct`

What changed:
- Archived the earlier active lab under
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/`.
- Created the new active lab at
  `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/`.
- Refreshed a fresh active `v000` baseline from current `main` at `c077cd8`.
- Created fresh eval manifests for the new active sequence.
- Reset active version numbering so new prompt work will resume from `v001`
  after the first fresh baseline run.
- Switched run organization to the version-first structure:
  `experiments/runs/baseline/runNN_...` and
  `experiments/runs/vNNN/runNN_...`.

Why it mattered:
- The live model tag and prompt/runtime surface changed enough that the earlier
  `q8_0` lab should no longer act as the active source of truth.
- Archiving the earlier work keeps the history available without letting it
  blur current-main decisions.
- The new run layout should make repeated experiments easier to audit and much
  easier to explain later.

Current consequence:
- New prompt work should happen only in
  `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/`.
- Anything run before `2026-04-10` is now explicitly historical.
- The next prompt step is a fresh baseline run in the new active lab, not a new
  candidate draft.

### 2026-04-02 — Qwen Prompt Lab Created

What changed:
- Built a local-only prompt lab for `qwen3-vl:8b-instruct-q8_0`.
- Added baseline snapshots, Qwen-specific rules, doctrine/schema crosswalk,
  eval manifests, failure taxonomy, and prompt version log.
- Drafted the first Qwen-focused prompt chain `v001` through `v004`.

Why it mattered:
- We needed a controlled place to iterate on prompts without touching the live
  config too early.
- We also needed a model-specific workflow instead of mixing general prompting
  advice into the live file directly.

Status:
- lab scaffolding complete
- prompt drafts complete
- evaluation and promotion work still pending

### 2026-04-10 — `main` Synced To New Upstream And Local Debug-Export Work Merged Forward

What changed:
- Stashed the local temporary debug-export work before syncing `main`.
- Fetched the new `upstream/main` and fast-forwarded local `main` from
  `fe12732` to `c077cd8`.
- Pushed the updated `main` to `origin/main`.
- Reapplied the local debug-export work from stash.
- Resolved the resulting merge conflict in `src/bda_svc/export.py`.
- Merged the local debug-export behavior forward into the newer upstream tests:
  - `tests/unit/test_cli.py`
  - `tests/unit/test_export.py`
  - `tests/unit/test_main.py`
- Ran `uv sync --dev`, which installed `pytest-mock`.
- Ran focused verification tests and got `7 passed`.

Why it mattered:
- We needed to bring in the new team changes on `upstream/main` without losing
  the local temporary tooling we use for prompt tuning.
- Upstream now has more export and CLI test coverage, so the local prompt-tuning
  helpers needed to be merged forward instead of reapplied blindly.

Current state:
- `main`, `origin/main`, and `upstream/main` are aligned at `c077cd8`.
- The local temporary debug-export work is preserved and currently staged in:
  - `src/bda_svc/app.py`
  - `src/bda_svc/cli.py`
  - `src/bda_svc/export.py`
  - `tests/unit/test_cli.py`
  - `tests/unit/test_export.py`
  - `tests/unit/test_main.py`
- The stash safety copy was dropped after the merged state and tests looked
  correct.

Current way forward:
- Review the new upstream `main` prompt/runtime surface before trusting the
  existing prompt-lab baseline as current.
- Refresh the main-lab baseline again if the new upstream config/doctrine
  changes materially affect prompt behavior.
- Keep the local temporary debug-export path separate from any future upstream
  merges by repeating the stash, sync, reapply, and focused-test pattern.

### 2026-04-10 — New Upstream Pull Analyzed

What changed:
- Reviewed the new upstream range from `fe12732` to `c077cd8`.
- Identified the runtime changes that affect prompt work, separate from the new
  docs, CI, and test coverage.

Runtime changes that matter:
- `src/bda_svc/pipeline/config.yaml`
  - default model tag changed from `qwen3-vl:8b-instruct-q8_0` to
    `qwen3-vl:8b-instruct`
  - detection prompt wording changed to:
    - identify valid targets first
    - then produce exactly one bbox per target
    - keep detection count aligned with identified targets
  - summary wording was softened around likely functional impact
- `src/bda_svc/pipeline/doctrine.yaml`
  - `buildings` detection guidance is more selective
  - `military_equipment` detection guidance is broader and now explicitly names
    things like locomotives and radar/fire-control components
- `src/bda_svc/pipeline/interfaces.py`
  - now uses `ollama.Client`
  - now supports `OLLAMA_HOST` and `OLLAMA_API_KEY`
- `src/bda_svc/export.py`
  - `save_json()` now returns the written path

Broader repo changes:
- `README.md` was rewritten
- `docs/101-development.md` and `docs/102-container.md` were added
- CI was expanded significantly
- unit-test coverage increased substantially

Current understanding:
- our April 6 prompt-lab baseline is no longer current-main truth
- prior prompt experiments are still useful historically, but they are now
  stale as current-baseline evidence
- the doctrine wording change, especially the explicit mention of locomotives,
  may be relevant to the subtype wording drift we saw in prior experiments

Current way forward:
- refresh the main prompt-lab baseline from `c077cd8`
- re-review the active prompt candidates against the new live prompt and
  doctrine wording before drawing new conclusions
- verify the local Ollama model tag matches the new live config before running
  more experiments

### 2026-04-10 — Reference Master Index Expanded Into A Detailed Routing Guide

What changed:
- Reworked `z_reference_docs/REFERENCE_MASTER_INDEX.md` from a light top-level
  directory summary into a more detailed routing document.
- Added an explicit "Index Routing Guide" that says which detailed index to open
  first for:
  - BDA doctrine
  - prompting references
  - PDF-derived prompting Markdown
  - prompt-lab state
  - prompt methodology
  - current project/changelog context
  - capstone-document context
- Expanded the BDA section so it now lists the main doctrine files by function
  instead of only pointing generally at the BDA folder.
- Expanded the prompting section so it now routes by topic, including:
  - system prompt design
  - directness and task framing
  - examples and chained prompting
  - output shaping
  - grounding / boxes / detection
  - multimodal input formatting
  - evaluation / fragility references

Why it mattered:
- The previous master index worked as a high-level entrypoint, but it was too
  coarse for repeated day-to-day reference work.
- The more granular routing should make it easier to quickly choose the right
  source family and the right sub-index without guessing.

Current consequence:
- `REFERENCE_MASTER_INDEX.md` is now the main routing layer.
- `BDAs_INDEX.md`, `PROMPTING_MASTER_INDEX.md`, and `PROMPTING_PDFS_INDEX.md`
  remain the deeper detailed indexes underneath it.

### 2026-04-10 — Reference Master Index Refined Into A Question-To-Document Map

What changed:
- Refined the prompting portion of `z_reference_docs/REFERENCE_MASTER_INDEX.md`
  so it now routes by question type instead of only by document family.
- Added question-oriented entrypoints for:
  - system-prompt design
  - directness and task wording
  - examples / chain prompts / reasoning scaffolds
  - output-format control
  - Qwen-specific multimodal behavior
  - grounding / boxes / detection
  - image roles / OCR / document-style inputs
  - evaluation and failure-analysis context

Why it mattered:
- A detailed index is more useful when it helps answer "what should I open for
  this exact problem?" rather than only "what files exist in this area?"
- This should make reference navigation faster during active prompt work and
  reduce the need to remember the right vendor or folder before starting.

Current consequence:
- `REFERENCE_MASTER_INDEX.md` is now both a top-level routing guide and a
  question-to-document map.
- The deeper indexes remain the source for exhaustive listings, while the
  master index now does a better job of helping us decide where to start.

### 2026-04-10 — BDA Section Of The Master Index Refined By Question Type

What changed:
- Refined the BDA portion of `z_reference_docs/REFERENCE_MASTER_INDEX.md` so it
  now routes by doctrine question type instead of only by doctrine category.
- Added question-oriented BDA entrypoints for:
  - combat assessment methodology and terminology
  - physical-damage versus broader-effects framing
  - broader targeting context
  - analyst workflow and fused reporting
  - dynamic targeting / strike-support / recon context

Why it mattered:
- The BDA section is more useful when it helps answer "which doctrine source
  should I open for this exact kind of assessment question?" rather than only
  listing the files by family.
- This should make it easier to choose the right doctrine source quickly while
  we are writing prompts, interpreting outputs, or documenting methodology.

Current consequence:
- The master index now routes both the prompting section and the BDA section by
  question type.
- `BDAs_INDEX.md` remains the detailed catalog underneath that higher-level
  routing layer.

### 2026-04-11 — Prompting Reference Review Redirected `v003`

What changed:
- Did a focused pass through the most relevant prompting references for the
  current bbox failure mode, with emphasis on:
  - Qwen localization and grounding docs
  - Qwen cookbooks for 2D grounding
  - a small set of general prompt-structure and few-shot references
- Compared those references to the observed behavior of `v001` and `v002`,
  which converged to the same off-target bbox and subtype/summary drift.
- Drafted:
  - `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/experiments/versions/v003_detect_objects_center-first-example-anchored.yaml`

Key conclusion:
- `v001` and `v002` did not fail because they were too weak; they failed
  because they remained in the same long negative-rule wording family.
- The Qwen references suggest a better next move is a shorter, more direct,
  format-explicit grounding prompt with one targeted example, not more
  prohibition blocks.

Current way forward:
- Run `v003` as the next detection-only candidate.
- Judge it primarily on whether the bbox lands on the visible solid target
  body.
- Continue holding assessment and summary constant until detection behavior is
  more trustworthy.

### 2026-04-11 — `v003` Run Reviewed And Rejected As A Winner

What changed:
- Ran `v003` in:
  `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/experiments/runs/v003/run01_2026-04-11_000440_EDT/`
- Compared it directly against the fresh baseline using the same seed image.
- Reviewed:
  - the JSON outputs
  - the overlay/crop debug images
  - `bbox_review_sheet.jpg`

Observed result:
- baseline bbox stayed `[51, 37, 128, 73]` with `PROBABLE`
- `v003` changed the bbox to `[51, 37, 102, 73]` and kept `PROBABLE`
- `v003` also removed the more specific `locomotive` wording from supporting
  logic
- despite the tighter coordinates, visual review showed the box still sat left
  of the actual target body and mostly covered terrain / track-side context

Why it mattered:
- `v003` confirmed that a numerically tighter box is not enough if the box is
  still not grounded on the actual object
- this gives us a clearer standard for the next round: stop rewarding shrinkage
  unless it is paired with visibly better object-body grounding

Current way forward:
- treat `v003` as another useful but non-winning detection draft
- keep detection as the only surface to change next
- next candidate should try a more object-body-specific localization tactic,
  especially shifting the box onto the dark solid mass nearest the fire source
  rather than just reducing width

### 2026-04-11 — Upstream `main` Synced To `21deaf5` And Active Lab Refreshed Without Reset

What changed:
- Preserved the local temporary debug-export work by saving it to a temporary
  branch when stash behavior was unreliable.
- Fast-forwarded local `main`, `upstream/main`, and `origin/main` from
  `c077cd8` to `21deaf5`.
- Cherry-picked the preserved local debug-export commit back onto local `main`
  cleanly.
- Reviewed the upstream delta and refreshed the active prompt-lab baseline
  snapshot/metadata to the new live commit.
- Ran the full test suite after the sync and preserved reapply:
  - result: `51 passed`

Why it mattered:
- We needed to keep the fork aligned with new team changes without losing the
  local prompt-tuning instrumentation.
- We also needed to decide whether the upstream changes were big enough to
  force another prompt-lab reset.
- The answer this time was "no": the upstream pull changed runtime hardening
  and tests, not the actual prompt text or model tag.

What the new upstream pull changed:
- `src/bda_svc/pipeline/config.yaml`
  - comment-level clarification for bbox-convention wording
- `src/bda_svc/pipeline/model.py`
  - explicit `_pixels` bbox-scale support
  - fail-safe rejection of invalid bbox-convention suffixes
- `src/bda_svc/pipeline/utilities.py`
  - explicit `_pixels` bbox conversion support
  - fail-safe handling for invalid bbox-convention suffixes
- tests expanded in:
  - `tests/unit/test_interfaces.py`
  - `tests/unit/test_model.py`
  - `tests/unit/test_utilities.py`

Environment consequence:
- `pyproject.toml` and `uv.lock` did not change, so no `uv sync` was needed.
- The active live model tag stayed `qwen3-vl:8b-instruct`.
- The model was already installed locally, so no new Ollama download was
  needed.

Current consequence:
- `origin/main` and `upstream/main` are aligned at `21deaf5`.
- Local `main` preserves the temporary debug-export work on top of that synced
  upstream state.
- The active prompt lab was refreshed, not reset.
- The current active evidence chain remains `v000` through `v003`.

### 2026-04-11 — Local `main` Intentionally Left One Commit Ahead For Prompt Debugging

What changed:
- Confirmed that local `main` is intentionally one commit ahead of both
  `origin/main` and `upstream/main`.
- Confirmed that the extra local commit is:
  - `aec6441` — `WIP: local debug export before syncing main`
- Confirmed that the temporary safety branch used during the sync was deleted
  after the preserved commit was back on `main`.

What that extra local commit contains:
- repo-side prompt-debug instrumentation in:
  - `src/bda_svc/app.py`
  - `src/bda_svc/cli.py`
  - `src/bda_svc/export.py`
  - `tests/unit/test_cli.py`
  - `tests/unit/test_export.py`
  - `tests/unit/test_main.py`
- the temporary CLI flag:
  - `--debug-export-images`
- optional export of per-target:
  - overlay images
  - crop images

Why it mattered:
- We needed to distinguish between:
  - prompt-lab artifacts
  - the local repo code that generates those artifacts
- The prompt labs contain the JSON, overlay, crop, manifest, and analysis
  outputs, but not the implementation of the debug-export helper itself.
- Upstream did not replace this specific helper behavior; it only changed
  adjacent runtime/export/test surfaces.

Current consequence:
- The active prompt workflow still depends on this helper layer for bbox review.
- We are intentionally leaving it on local `main` for now.
- Remove or relocate it only after bbox/localization prompt tuning is finished.

### 2026-04-12 — Cycle 02 Completed For Assessment Confidence And Summary Calibration

What changed:
- started cycle 02 after the confirmed `v006` bbox win
- shifted the active prompt surface from `detect_objects` to `assess_damage`
- ran and documented:
  - `v007`
  - `v008`
  - `v009`
- wrote the cycle summary:
  `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/experiments/cycles/cycle02_v007-v009_summary.md`

Key outcomes:
- `v007` was a partial improvement:
  - kept `PROBABLE`
  - removed K-kill language
  - removed subtype drift
  - but overcorrected to `DAMAGED`
- `v008` did not help:
  - still `DAMAGED`
  - subtype drift returned
  - confirmed that abstract category rules were not the right prompt lever
- `v009` became the cycle winner:
  - restored `DESTROYED`
  - kept `PROBABLE`
  - removed subtype drift from target-level logic

What remains open:
- the summary stage still overreaches on terrain/context and functional-impact
  wording
- the next cycle should freeze the current best detection/assessment direction
  and move to `summarize_scene`

### 2026-04-12 — Cross-Image Generalization Sweep Completed

What changed:
- re-ran the frozen `v006` detection + `v009` assessment pair across:
  - `tank.jpg`
  - `destroyed_truck15.jpg`
  - `operational_truck4.jpg`
  - `office.jpg`

What we learned:
- the pair stayed sensible on the truck and office scenes
- the tank seed remained unstable across repeats
- the prompt direction does not look tank-only, but the tank image is still the
  pressure point

Why it mattered:
- we now know the current best pair is reasonably general across a small
  cross-image sweep
- we also know the original tank seed still needs repeatability attention

### 2026-04-12 — Cross-Image Generalization Sweep Completed

What changed:
- re-ran the frozen `v006` detection + `v009` assessment pair across:
  - `tank.jpg`
  - `destroyed_truck15.jpg`
  - `operational_truck4.jpg`
  - `office.jpg`

What we learned:
- the pair stayed sensible on the truck and office scenes
- the tank seed remained unstable across repeats
- the prompt direction does not look tank-only, but the tank image is still the
  pressure point

Why it mattered:
- we now know the current best pair is reasonably general across a small cross-
  image sweep
- we also know the original tank seed still needs repeatability attention

### 2026-04-12 — Backend Variance Added To Grounding Diagnosis

What changed:
- reviewed non-official community sources alongside the local prompting docs to
  sanity-check whether the current prompt YAML structure was the main problem
- added a new diagnostic rule: if grounding stalls after multiple prompt
  revisions, check backend/runtime variance before blaming YAML structure alone
- kept the current top-level YAML split in place because the evidence still
  points more strongly to prompt-surface and runtime-behavior issues than to a
  bad overall architecture

Why it mattered:
- this keeps us from rewriting the prompt layout too early
- it adds a cleaner escalation path when grounding remains stubborn: prompt
  surface first, backend/runtime variance second, architecture rewrite only
  after both have been pressure-tested

### 2026-04-17 — Gemma 4 Bootstrap Reached First Live `v000` Run

What changed:
- stood up the first Gemma model-line worktree and prompt lab around:
  - `model/gemma4-e4b`
  - `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- built the Gemma `v000` baseline as a semantic port of the active Qwen
  `v009` working stack
- pulled the Gemma 4 research pack into:
  - `z_reference_docs/Prompting/Google_Gemma/Gemma_4/`
- added a normalized markdown layer for the Gemma sources
- resolved the local runtime blocker by using a user-local Ollama `0.21.0`
  runtime on `127.0.0.1:11435` while the system Ollama install remained
  `0.15.2`
- ran the inherited six-case comparison pack under:
  - `z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/v000/run01_2026-04-17_134308_EDT/`

What we learned:
- Gemma `v000` held the contract cleanly on:
  - `tank_pressure`
  - `destroyed_tank15`
  - `operational_tank4`
  - `operational_building7`
  - `office_negative`
- the office negative remained clean at raw `bda-svc` level, but `bda_eval`
  still cannot score `NOT APPLICABLE` damage labels cleanly
- the first major Gemma weakness is now visible on `destroyed_building4`:
  - multi-building grounding drifted
  - severity undercalled badly relative to both the active Qwen stack and the
    `origin/main` baseline

Why it mattered:
- we now have a real Gemma execution baseline instead of only a research pack
  and tracked config stub
- the next Gemma work should start from a concrete read:
  - equipment and negative-scene behavior are promising
  - destroyed-building grounding and severity need focused Gemma-specific work

### 2026-04-19 — `main` And `origin/main` Were Advanced To `e7a22a9`

What changed:
- confirmed `upstream/main` had advanced from `c19940a` to `e7a22a9`
- fast-forwarded local `main` from `c19940a` to `e7a22a9`
- pushed that same fast-forward to `origin/main`
- verified afterward that:
  - local `main` == `origin/main` == `upstream/main` == `e7a22a9`

What we learned:
- the newer upstream delta came from PR `#136` (`fix/unicode`)
- it touched:
  - `bda_eval/discovery.py`
  - `bda_eval/main.py`
  - `src/bda_svc/export.py`
  - `src/bda_svc/pipeline/config.yaml`
- the first push attempt did not move `origin/main` because it raced the
  fast-forward merge; rerunning the push sequentially resolved that cleanly

Why it mattered:
- the clean mirror and the fork are now both current at the latest upstream
  baseline
- that puts us in the right state to analyze the new delta and decide whether
  it should be propagated through the active Qwen and Gemma worktrees next

### 2026-04-19 — `e7a22a9` Was Propagated Through The Active Qwen And Gemma Worktrees

What changed:
- rebased the active worktrees in the documented parent-to-child order:
  - `model/qwen3-vl-8b-instruct`
  - `feat/qwen3-vl-8b-instruct/two-pass-refinement`
  - `model/gemma4-e4b`
  - `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- resolved the expected reusable `bda_eval/main.py` conflict on both model
  branches by keeping the prompt-lab review-artifact behavior and the newer
  upstream structure together
- merged the new upstream empty-detections rule into the active Qwen and Gemma
  tracked configs while preserving the branch-specific winner/bootstrap wording
- ran `uv sync --all-packages` and
  `uv run pytest tests/unit/test_yamls.py bda_eval/tests` on all four active
  worktrees
- recorded fresh `refresh_smoke` runs under:
  - Qwen model:
    `Prompt_Labs/1_qwen3-vl-8b-instruct/1_model__qwen3-vl-8b-instruct/experiments/runs/refresh_smoke/run03_2026-04-19_173039_EDT/`
  - Qwen feature:
    `Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/refresh_smoke/run02_2026-04-19_173039_EDT/`
  - Gemma model:
    `Prompt_Labs/3_gemma4-e4b/3_model__gemma4-e4b/experiments/runs/refresh_smoke/run03_2026-04-19_173039_EDT/`
  - Gemma feature:
    `Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/refresh_smoke/run02_2026-04-19_173039_EDT/`

What we learned:
- this upstream move is not another infra-only refresh; it changes live prompt
  semantics and export behavior
- Qwen still completed the full practical smoke loop after the refresh
- Gemma did not lose basic runtime viability, but the new detect contract now
  drives both active Gemma branches to:
  - `object_not_found`
  - `damage_category = NOT APPLICABLE`
  on `tests/data/tank.jpg`
- because `bda_eval` still cannot score `NOT APPLICABLE` cleanly, the Gemma
  self-check fails on that smoke image once detection falls to the no-target
  path
- the user-local Gemma Ollama `0.21.0` host on `127.0.0.1:11435` had to be
  brought back up during the validation pass; the failure there was
  environmental first, then semantic after the host was restored

Why it mattered:
- the branch ancestry is now current across both active model lines
- Qwen remains practically usable after the new upstream contract change
- Gemma now clearly requires a fresh post-`e7a22a9` baseline and follow-on
  analysis before the refresh cycle can be treated as fully closed for that
  line

### 2026-04-19 — Pre-Push Validation Confirmed The Rebasing Did Not Break The Qwen Feature Branch

What changed:
- ran a dedicated pre-push validation pass on
  `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- recorded the run under:
  `Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/pre_pr_update_check/run01_2026-04-19_175219_EDT/`
- completed:
  - `uv sync --all-packages`
  - `uv run pytest tests/unit/test_yamls.py bda_eval/tests`
  - `bda-svc` export on `tests/data/tank.jpg`
  - `bda_eval` self-check

What we learned:
- the refreshed/rebased Qwen feature branch still works on the practical smoke
  path
- compared with the prior post-refresh smoke run, the new output kept:
  - `military_equipment`
  - `DESTROYED`
  - `PROBABLE`
  - the same scene summary
- the new run was not byte-for-byte identical:
  - bbox drifted from `[51, 37, 128, 73]` to `[51, 49, 128, 73]`
  - `brief_supporting_logic` wording changed slightly while preserving the same
    meaning

Why it mattered:
- this gives us a grounded pre-push check on the exact branch we would use to
  update PR `#134`
- the local branch still looks operational and semantically aligned, but the
  tank smoke output is not a strict exact replay

### 2026-04-19 — Gemma `v000` Was Rebuilt After `e7a22a9`

What changed:
- rebuilt the active Gemma `v000` baseline on the current `e7a22a9` repo base
  using the active feature worktree and the inherited six-case comparison pack
- brought the user-local Gemma Ollama `0.21.0` host back up on
  `127.0.0.1:11435`
- completed:
  - `uv sync --all-packages`
  - `uv run pytest tests/unit/test_yamls.py bda_eval/tests`
  - the full six-case Gemma baseline rerun
  - `bda_eval` comparison lanes against active Qwen `v009` and the
    `origin/main` baseline where evaluable
- recorded the rebuilt baseline under:
  `Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/v000/run02_2026-04-19_185856_EDT/`
- preserved the older first-live baseline under:
  `Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/v000/run01_2026-04-17_134308_EDT/`
  as pre-refresh historical evidence

What we learned:
- `e7a22a9` changed more than the standard tank smoke seed for Gemma
- `destroyed_tank15` held exactly
- `operational_building7` held category/confidence with geometry drift only
- `office_negative` still held as `object_not_found / NOT APPLICABLE`
- `tank_pressure` regressed from `DESTROYED / PROBABLE` to
  `object_not_found / NOT APPLICABLE`
- `operational_tank4` regressed from `NO DAMAGE / CONFIRMED` to
  `DAMAGED / PROBABLE`
- `destroyed_building4` remained an undercalled building failure, now with two
  `MODERATE DAMAGE / CONFIRMED` outputs and overlapping left-side boxes
- `bda_eval` still does not emit a normal CSV for `NOT_APPLICABLE` office
  negatives, even though it now exits `0` and still emits review artifacts

Why it mattered:
- the rebuilt `run02` baseline is now the active Gemma `v000` anchor for the
  current repo base
- the older `run01` conclusions are no longer portable onto the current repo
  base
- the next Gemma move should pause before `v001`
- the first issue to reconsider is the inherited detect-contract effect, not a
  new prompt iteration by default

### 2026-04-19 — Gemma Tank Diagnostics Confirmed An Explicit Empty-Detections Abstention

What changed:
- added a minimal env-gated detection debug dump in the active Gemma feature
  worktree at:
  `src/bda_svc/pipeline/model.py`
- enabled that debug path with:
  `BDA_DEBUG_DETECTION_PATH`
- reran only the two tank cases under:
  `Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/detect_diagnostics/run01_2026-04-19_193323_EDT/`
  - `tank_pressure`
  - `operational_tank4`

What we learned:
- `tank_pressure` returned raw `{"detections":[]}` from Gemma
- that `tank_pressure` collapse was not caused by:
  - JSON parse failure
  - invalid target-type filtering
  - invalid bbox filtering
- `operational_tank4` still returned one valid `military_equipment` detection
  and the pipeline kept it
- this means the two current Gemma tank failures have now separated cleanly:
  - `tank_pressure` is a true detect-stage abstention under the current
    contract
  - `operational_tank4` is bbox/assessment drift, not total detect collapse

Why it mattered:
- we no longer need to guess whether `tank_pressure` was failing because of
  bbox rejection or parse fallout
- the explicit empty-detections instruction is now the leading causal suspect
  for the Gemma tank abstention
- the next Gemma move should be a narrow detect-contract adjustment test before
  any broader `v001` cycle opens

### 2026-04-19 — Gemma `v001` Recovered The Two Tank Regressions On A Narrow Probe

What changed:
- changed only the `detect_objects` no-target instruction in the active Gemma
  feature worktree
- saved the config snapshot as:
  `experiments/versions/v001_detect_objects_no-target-tightening.yaml`
- kept the temporary env-gated detection debug hook active in the Gemma
  feature worktree
- ran the focused two-case `v001` probe under:
  `Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/v001/run01_2026-04-19_194343_EDT/`
  - `tank_pressure`
  - `operational_tank4`
- ran `eval_vs_qwen_v009` on both cases

What we learned:
- `tank_pressure` no longer returned raw `{"detections":[]}`
- `tank_pressure` now returned one valid `military_equipment` detection and
  finished at `DESTROYED / PROBABLE`
- `operational_tank4` now returned one valid `military_equipment` detection
  with a higher box and finished at `NO DAMAGE / CONFIRMED`
- both tank cases remained true positives against the active Qwen references
  in `bda_eval`

Why it mattered:
- the no-target detect instruction is now confirmed as a high-leverage control
  point for Gemma on the current repo base
- `v001` is now the active next candidate rather than a speculative idea
- this is still narrow evidence only, so the right next step is broader
  `v001` validation before any promotion or replacement of the active Gemma
  `v000` anchor

### 2026-04-19 — Gemma `v001` Held Across The Broader Six-Case Follow-Up

What changed:
- ran the full inherited six-case Gemma comparison pack under:
  `Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/v001/run02_2026-04-19_195511_EDT/`
- kept the same narrow `v001` detect-only prompt adjustment
- kept the temporary detection debug hook active
- ran both:
  - `eval_vs_qwen_v009`
  - `eval_vs_origin_main_baseline`

What we learned:
- `tank_pressure` stayed recovered at `DESTROYED / PROBABLE`
- `destroyed_tank15` held exactly
- `operational_tank4` stayed recovered at `NO DAMAGE / CONFIRMED`
- `operational_building7` held at `NO DAMAGE / CONFIRMED`
- `office_negative` held exactly as `object_not_found / NOT APPLICABLE`
- `destroyed_building4` improved meaningfully:
  - it now returns two separate buildings rather than two overlapping left-side
    boxes
  - one building is now `DESTROYED / CONFIRMED`
  - the left building is still undercalled at `MODERATE DAMAGE / CONFIRMED`

Why it mattered:
- `v001` is now the strongest Gemma direction so far on the current repo base
- the recovery is not just a narrow two-case tank effect
- the main remaining Gemma problem is now building-severity calibration rather
  than the detect-contract abstention on equipment cases

### 2026-04-17 — `c19940a` Was Propagated Through The Active Qwen And Gemma Worktrees

What changed:
- confirmed `upstream/main`, `origin/main`, and local `main` are all aligned at
  `c19940a`
- reviewed the upstream delta and confirmed it only touched:
  - `.github/workflows/ci.yml`
  - `docker/Dockerfile`
- ran the documented branch/worktree refresh flow across:
  - `model/qwen3-vl-8b-instruct`
  - `feat/qwen3-vl-8b-instruct/two-pass-refinement`
  - `model/gemma4-e4b`
  - `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
- completed that refresh with clean rebases and no content conflicts

What we learned:
- this upstream move is an infra/security update, not a prompt or doctrine
  update
- the active Qwen prompt evidence anchor remains the fresh branch-aware
  `28e863b` baseline
- the active Gemma prompt evidence anchor remains the first live `v000` run
  recorded before this refresh
- the Gemma feature rebase reported skipped already-applied commits, which is
  normal duplicate-detection behavior rather than a conflict
- the local Qwen feature branch now diverges from
  `origin/feat/qwen3-vl-8b-instruct/two-pass-refinement` because of the rebase
  and should only be refreshed remotely with a deliberate
  `git push --force-with-lease`

Why it mattered:
- both active model lines are now based on the current repo baseline without
  unnecessarily resetting their prompt evidence chains
- this keeps the worktrees current with upstream infra changes while preserving
  the integrity of the existing prompt-lab comparisons
- it also confirms the refresh workflow is working the way it was designed to:
  update branch ancestry when infra changes land, but avoid baseline rebuilds
  when prompt/runtime semantics have not changed

### 2026-04-17 — The Model Branches Were Hardened To Match The Prompt-Lab Smoke Workflow

What changed:
- hardened the Qwen model branch by cherry-picking:
  - `b947a3e` — `Add prompt-lab review artifacts to bda_eval`
  - `0f916de` — `Install workspace packages in CI`
- hardened the Gemma model branch by cherry-picking:
  - `54a9d58` — `Bootstrap Gemma 4 E4B baseline config`
- reran the shared sanity tests on the hardened model branches
- reran prompt-lab style smoke runs on the hardened model branches:
  - `bda-svc` export
  - `bda_eval` self-check against the exported report folder

What we learned:
- the earlier Qwen model-branch limitation was not a rebase bug; it was simply
  missing the newer `bda_eval` skip-without-API-key behavior
- the earlier Gemma model-branch limitation was not a Gemma runtime failure; it
  was still pointing at the Qwen model tag in tracked config
- after the hardening pass, both model branches now complete the same practical
  smoke path as the feature branches

Why it mattered:
- this removes a confusing split where the feature branches behaved like real
  prompt-lab workspaces but the model branches did not
- future branch-level validation can now use the same baseline smoke recipe
  across all four active worktrees
- it makes the long-lived model branches safer as reusable starting points for
  additional feature branches

### 2026-04-17 — Branch Hygiene Was Completed On The Active Feature Worktrees

What changed:
- rebased `feat/qwen3-vl-8b-instruct/two-pass-refinement` onto the hardened
  `model/qwen3-vl-8b-instruct`
- rebased `feat/gemma4-e4b/qwen-v009-workflow-bootstrap` onto the hardened
  `model/gemma4-e4b`
- reran the shared sanity suite on both feature branches:
  - `uv run pytest tests/unit/test_yamls.py bda_eval/tests`
- reran the practical prompt-lab smoke flow on both feature branches:
  - `bda-svc` export on `tests/data/tank.jpg`
  - `bda_eval` self-check against the fresh export folder
  - artifact writeout into each branch lab under
    `experiments/runs/branch_hygiene/run01_2026-04-17_231500_EDT/`

What we learned:
- the Qwen feature rebase skipped already-applied commits because reusable
  infrastructure had already been promoted into the model branch
- the Gemma feature branch now resolves to the same tracked-code state as the
  hardened Gemma model branch, which is expected at this stage because the
  bootstrap baseline commit was promoted upward
- both active feature branches still complete the same practical prompt-lab
  smoke loop after the ancestry cleanup

Why it mattered:
- this closes the branch-hygiene loop instead of stopping at “model branches
  are now capable”
- it confirms that future prompt work can resume from tidy parent/child branch
  relationships rather than from partially refreshed ancestry
- it leaves the Qwen and Gemma feature lines in a cleaner local state before
  any separate decision about remote pushes

### 2026-04-20 — Detection Prompt Assembly Review Lowered Confidence In A Doctrine-Only Fix

What changed:
- traced the full Qwen `1.3` detection prompt assembly path from:
  - `config.yaml`
  - `doctrine.yaml`
  - prompt formatting helpers
  - the Ollama chat wrapper
- rendered the exact assembled detection prompt with the current doctrine block
  injected in place

Observed result:
- doctrine is definitely part of the detection prompt
- but it is injected only as plain text inside the `user` prompt body under
  `TARGET-TYPE SPECIFIC DETECTION GUIDANCE`
- it is not promoted into the `system` prompt
- it is followed by a longer generic `BOXING RULE` block and contrastive
  examples that likely carry stronger behavioral weight
- the current assembled prompt is approximately:
  - system prompt: 8 lines / 350 chars
  - detection prompt: 70 lines / 4511 chars
  - doctrine block inside detection prompt: 13 lines / 1330 chars

Methodology update:
- do not assume that editing `doctrine.yaml` changes a model habit with the
  same force as editing the main detection prompt surface
- if doctrine is only injected as a mid-prompt reference block, treat it as a
  weaker lever than the higher-salience global rules and examples around it
- when doctrine-sensitive cases stay stuck after doctrine wording changes,
  inspect prompt assembly before concluding that the doctrine content itself is
  wrong

Current consequence:
- the Qwen adjacency/localization issue now looks more like a detection-prompt
  weighting problem than a doctrine-semantics problem
- if this line continues, the next likely leverage point is the detection
  prompt surface rather than another doctrine-only rewrite

### 2026-04-20 — Cross-Branch Detect Surface Inspection Confirmed The Next Lever

What changed:
- built a Qwen-only detect-surface inspection packet across:
  - active `1.2`
  - doctrine-side `1.3`
  - historical detect winner `v006`
- re-reviewed the local Qwen source pack and the earlier `v004`, `v005`, and
  `v006` research-loop notes
- did one targeted official current Qwen check to test whether system-vs-user
  instruction placement is a live hypothesis worth carrying forward

Observed result:
- the active `1.2` and `1.3` `detect_objects` templates are currently
  identical
- the rendered branch-to-branch detect difference comes only from the injected
  doctrine block in `1.3`
- relative to historical `v006`, the active detect surface differs only
  slightly:
  - the old all-zero-bbox safeguard line is gone
  - the explicit `{"detections": []}` no-target instruction is now present
- that means the current problem is not “we lost `v006` and need to rewrite the
  detect prompt from scratch”
- the targeted current Qwen check was enough to justify keeping a later
  system-role hypothesis lane, but not enough to justify broader new web
  research right now

Methodology update:
- when current behavior looks close to a previously confirmed winner, compare
  the exact rendered surfaces before assuming a large prompt drift
- separate:
  - template-level differences
  - doctrine-injected rendered differences
  - message-hierarchy hypotheses
- if those layers show only small drift, treat the next cycle as an
  instruction-weighting problem, not a clean-sheet rewrite problem

Current consequence:
- the next Qwen lever should be the actual detection user prompt surface
- Gemma remains untouched
- no broader new online research is needed before the next Qwen detect-only
  cycle

### 2026-04-20 — Qwen Detect Candidate A Produced A Real `destroyed_building4` Recovery

What changed:
- created a mirrored Qwen detect-surface A/B run on both:
  - `1.2` active Qwen line
  - `1.3` doctrine-side verification lane
- captured parent-control exports first on both branches using the same 12-image
  building-heavy pack
- changed only `detect_objects` in both branches:
  - added one higher-salience adjacent-building target-body rule in the top
    `RULES` block
  - tightened the later building boxing sentence
- recorded:
  - `1.2` version snapshot
    `v010_detect_objects_adjacent-building-target-body-priority.yaml`
  - branch run manifests
  - cross-branch review note

Observed result:
- `destroyed_building4` improved in both branches:
  - parent control split the scene into two buildings
  - candidate collapsed the read to one scene-central destroyed building
- `destroyed_building3` still boxed the background building as a second target
- `destroyed_building6` remained a broad scene-partitioning read
- `office_negative`, `operational_tank4`, and `tank_pressure` held
- only minor incidental bbox drift appeared on some non-targeted controls

Methodology update:
- the actual detection user prompt is a stronger lever than doctrine-only
  wording for the current Qwen adjacent-building problem
- same-input parent-vs-candidate A/B runs are still useful on the current
  inherited repo base even before a formal rebuilt post-refresh baseline,
  as long as the comparison is framed as a local relative probe rather than a
  promoted baseline reset
- when a candidate improves the key failure in both the active branch and a
  doctrine-side verification lane, that is stronger evidence than a one-branch
  win

Current consequence:
- `v009` remains the last confirmed staged Qwen winner
- the local tracked `1.2` feature-branch config now carries an exploratory
  detect-only `v010` candidate
- `v010` is a promising partial win, not yet a promoted replacement
- the next Qwen detection cycle should preserve the `destroyed_building4`
  recovery while directly targeting:
  - `destroyed_building3`
  - `destroyed_building6`

### 2026-04-20 — Qwen Detect Candidate B Failed To Improve The Remaining Building Gaps

What changed:
- ran a second mirrored detect-only Qwen follow-up from the live `v010` state
- reused the `run01` `qwen_candidate_a` outputs as the parent control for both
  branches so the comparison stayed anchored on `v010`
- changed only `detect_objects` again:
  - kept the `v010` adjacent-building target-body rule
  - added one scene-dominance/background-context rule
  - added one explicit background-building contrastive example

Observed result:
- `destroyed_building4` remained recovered as one scene-central destroyed
  building
- `destroyed_building3` still boxed the background building as a second target
- `destroyed_building6` still returned three buildings
- `office_negative` and `operational_tank4` stayed clean
- some incidental bbox drift returned on non-targeted controls without a
  compensating win

Methodology update:
- once a promising partial win exists, the next follow-up must beat it on the
  intended failure family, not just preserve it
- adding more prose about background or scene-central buildings is not enough
  by itself to fix the remaining Qwen failures here
- when a follow-up fails to beat the current best local state, record it and
  restore the stronger candidate rather than leaving the weaker wording live

Current consequence:
- `v011` is now recorded as a completed but rejected detect-only follow-up
- `v010` remains the strongest current local Qwen detect state
- both live Qwen worktrees were restored from `v011` back to `v010`

### 2026-04-20 — Example Structure Tightened Some Boxes But Still Did Not Beat `v010`

What changed:
- ran a third mirrored detect-only Qwen follow-up from the live `v010` state
- again reused the saved `v010` outputs as the parent control for both
  branches
- changed only `detect_objects` again, but this time by restructuring the
  building guidance around an explicit example-heavy target-selection block
  rather than adding more prose rules

Observed result:
- `destroyed_building4` stayed recovered as one scene-central destroyed
  building
- `destroyed_building3` still boxed the background building as a second target
- `destroyed_building6` still returned three buildings
- `office_negative`, `operational_tank4`, and `tank_pressure` stayed clean
- some bbox edges tightened slightly, especially in the doctrine-side `1.3`
  lane, but the core wrong detections remained

Methodology update:
- changing *how* examples are grouped and surfaced can influence box shape, but
  not every example-heavy rewrite is strong enough to change target count or
  scene-partition behavior
- once a candidate preserves the key recovery but leaves the same failure
  family intact, slight bbox tightening alone is not enough to justify keeping
  it live
- rejected follow-ups should still be fully documented, because they tell us
  which kinds of prompt changes are too weak for this model/problem pair

Current consequence:
- `v012` is now recorded as a completed but rejected detect-only follow-up
- `v010` remains the strongest current local Qwen detect state
- both live Qwen worktrees were restored from `v012` back to `v010`

### 2026-04-20 — Stronger Hierarchy Helped In `1.3`, But Not Enough In Active `1.2`

What changed:
- ran a fourth mirrored detect-only Qwen follow-up from the live `v010` state
- again reused the saved `v010` outputs as the parent control for both
  branches
- changed only `detect_objects` again, this time by adding a top-of-prompt
  `BUILDING TARGET PRIORITY` decision order instead of relying on looser rule
  placement or example-only structure

Observed result:
- `destroyed_building4` stayed recovered in both branches
- active `1.2` still boxed the `destroyed_building3` background building and
  still returned three buildings on `destroyed_building6`
- doctrine-side `1.3` **did** remove the `destroyed_building3`
  background-building false positive
- `destroyed_building6` still remained unresolved in both branches
- guardrails held:
  - `office_negative`
  - `operational_tank4`
  - `tank_pressure`

Methodology update:
- stronger instruction hierarchy can matter more than example reshuffling alone
- but a gain that appears only in the doctrine-side verification lane is not
  enough to replace the active working state
- asymmetric wins are still valuable because they tell us which prompt factors
  may be interacting, in this case hierarchy plus doctrine-side context

Current consequence:
- `v013` is now recorded as a completed but rejected detect-only follow-up for
  the active line
- `v010` remains the strongest current local Qwen detect state
- both live Qwen worktrees were restored from `v013` back to `v010`
- the next useful clue is now explicit:
  hierarchy matters, but the active line may need a hierarchy change that is
  even more tightly coupled to the building-selection language around
  `destroyed_building3`
