# Prompt Development Methodology

## Purpose

This document is a living record of how we are developing, testing, revising,
and occasionally reverting prompts for the VLM workflows in this project.

Its purpose is to make the methodology easy to explain later in:

- a presentation
- a written project report
- a live discussion about prompt-engineering decisions
- a retrospective on what worked, what did not, and why

This is not just a list of prompt edits. It is the running explanation of:

- what sources we are using
- how those sources influence prompt decisions
- what experiments we are running
- what changes we are making
- what challenges we are encountering
- what direction we are taking at each stage

This document should be updated periodically as the work evolves. When major
changes occur, we should explicitly decide whether to update this document
immediately or wait until a slightly larger chunk of progress is complete.

If you want the teaching-grade, capability-first explanation of how this
workflow works and how to reproduce it, start with:

- `z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`

This methodology document remains the running historical record of what changed
and why.

## Current Codex Tooling Overlay

The local prompt workflow now also sits on top of a global Codex tooling
baseline in:

- `/home/williambenitez1/.codex/AGENTS.md`
- `/home/williambenitez1/.codex/MCP_USAGE_GUIDE.md`
- `/home/williambenitez1/.codex/agents/VENDOR_MANIFEST.md`

That overlay matters as support infrastructure, not as a replacement for local
evidence discipline.

Current implications:

- source-specific MCP servers and connectors are now preferred over generic web
  when they are the clearer fit
- `playwright` is the preferred browser MCP for interaction-heavy workflows,
  while `filesystem` is preferred only for in-root structured inspection
- `sequentialthinking` should now be used before substantive updates to live
  maintained docs, global rules, or any `AGENTS.md`
- the selected global custom-agent subset is now installed for explicit use,
  but those specialists still do not replace run evidence, validation, or
  promotion discipline

## Scope

This methodology currently covers prompt work for:

- the live `bda-svc` Ollama pipeline in `src/bda_svc/pipeline/config.yaml`
- the active local prompt lab in `z_reference_docs/Prompt_Labs/`
- the current Qwen-first prompt effort for `qwen3-vl:8b-instruct`
- the new Gemma bootstrap line for `gemma4:e4b`

It may later expand to other models, but each model should still have its own
lab-specific notes and experiment artifacts.

## Current Setup

### Source of Truth for Live Runtime

The live prompt/runtime contract currently comes from:

- `src/bda_svc/pipeline/config.yaml`
- `src/bda_svc/pipeline/model.py`
- `src/bda_svc/pipeline/interfaces.py`
- `src/bda_svc/pipeline/doctrine.yaml`

The current live runtime is an Ollama-based dual-VLM pipeline. The working
assumption is that prompt experimentation should not change this contract
lightly.

As of the latest synced `upstream/main`, the current runtime contract includes:

- configurable detection bbox convention through
  `detection_vlm.bbox_convention`
- explicit runtime support for `_1`, `_1000`, and `_pixels` bbox suffixes, with
  fail-safe rejection of invalid bbox-convention strings before pixel
  conversion
- parameterized detection prompt inputs:
  - `{categories}`
  - `{detection_guidance}`
  - `{bbox_format}`
  - `{bbox_scale}`
- doctrine-driven detection guidance sourced from
  `src/bda_svc/pipeline/doctrine.yaml`
- structured-output repair through `json-repair` before Pydantic validation
- `think=False` in Ollama calls to reduce unwanted reasoning output
- environment override support for detection and assessment model names
- a live detect-objects safeguard line that explicitly says not to return an
  all-zero bbox unless the target type is `object_not_found`

Method implication:

- current prompt drafts must preserve the configured placeholders and should
  not return to the older hardcoded `0-1000 xyxy only` detection wording unless
  an explicit experiment justifies that reversal
- when a candidate pair looks promising on the seed case, run a small
  cross-image generalization sweep before treating it as finished; the tank
  image is a repeatability pressure test, not the only evidence we need
- for the active branch-aware Qwen line, the current mixed grounding sweep is
  explicitly defined in:
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/validation/grounding_generalization_pack_v1.md`
- if the current working leader is already known to be wrong on a specific
  mixed-pack case, a corrective follow-up should be judged against the
  known-good per-case reference or clarified ground truth for that case, not
  blindly against the current wrong leader
- when negative scenes use `object_not_found` / `NOT APPLICABLE`, raw
  `bda-svc` JSON may be a more reliable review artifact than `bda_eval` CSV
  until the eval path handles those labels cleanly
- when evaluation images are sourced from `z_reference_docs/Data_set_Storage/`,
  it is acceptable to copy those images into per-run worktree or prompt-lab
  output folders and preserve them there as part of the run artifact set
- once individual prompt surfaces have confirmed leaders, run at least one
  broader frozen-stack sweep against the fresh branch-aware baseline before
  treating the combined stack as the current promotion candidate
- in that frozen-stack sweep, prioritize:
  - whether earlier cross-image regressions are actually resolved
  - whether the negative scene still stays clean
  - whether any remaining differences are now calibration nuances rather than
    outright recall failures
- once that frozen-stack sweep is good enough, package the winning combined
  surfaces into one explicit unified version file and stage it in the winners
  area so promotion work is traceable and does not rely on implicit
  cross-references between earlier versions
- if that unified winner will be used as the active reference stack, run it at
  least once on a small focused comparison pack so the packaged version itself
  has an explicit execution record, not just the earlier frozen-stack evidence

### Local Reference Access Provided For Prompt Work

The prompt-development process has local access to:

- BDA doctrine and combat-assessment references in `z_reference_docs/BDAs/`
- model-specific prompting material in `z_reference_docs/Prompting/`
- Qwen-specific docs and cookbooks in `z_reference_docs/Prompting/Qwen/`
- general prompting guidance from:
  - `z_reference_docs/Prompting/Anthropic_Claude/`
  - `z_reference_docs/Prompting/OpenAI_GPT/`
  - `z_reference_docs/Prompting/Google_Gemini/`
- broader VLM research papers in `z_reference_docs/Prompting/VLM-Research-Papers/`

These references were collected so prompt changes can be grounded in both:

- doctrinal output requirements
- current model/prompting best practices

Generated research notes from the active critique/research/revise workflow now
live under:

- `z_reference_docs/Prompting/Research_Loops/`

These notes are not source-of-truth references by themselves. They are the
record of how one experiment critique turned into the next prompt revision.

### Backup / Change Safety

A backup copy of the live config is kept at:

- `z_reference_docs/config.yaml.backup`

This is used as a stable reference point when prompt drafts diverge from the
current live config and we need to compare or recover prior wording.

### Working Area For Prompt Iteration

Prompt experiments are now split into:

- preserved legacy prompt history in:
  - `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/`
- new branch-structured roots in:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/`

The legacy `2.main__...` lab contains the pre-reset main-branch work and should
be treated as preserved historical working context tied to
`snapshot/2026-04-15-pre-main-reset`.

New branch-specific work should now be organized under:

- `z_reference_docs/Prompt_Labs/<model-slug>/<branch-slug>/`

where `<branch-slug>` is the git branch name with `/` replaced by `__`.

Numbering rule for new work:

- model roots use a leading integer, for example `1_qwen3-vl-8b-instruct`
- branch roots use the same model number plus a workstream number, for example
  `1_model__...` and `1.2_feat__...`
- the current second model-line example is:
  - `3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/`

The prior `qwen3-vl:8b-instruct-q8_0` lab is now archived under:

- `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/`

Each lab contains:

- baseline snapshots
- a Qwen rules dossier
- doctrine/schema crosswalk notes
- eval manifests
- versioned prompt drafts
- failure taxonomy
- winner staging notes

The lab exists so prompt experimentation can happen locally before anything is
promoted into the live repo files.

### Current Workspace Setup

A saved VS Code workspace is available at:

- `z_reference_docs/Capstone.code-workspace`

The clean mirror checkout remains at:

- `/home/williambenitez1/Capstone`

New active code work should happen in separate worktrees instead of on the
clean mirrored `main` checkout. The first two worktrees created are:

- `/home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct`
- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`
- `/home/williambenitez1/Capstone_worktrees/3_model__gemma4-e4b`
- `/home/williambenitez1/Capstone_worktrees/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap`

`z_reference_docs` remains centralized at the main checkout path and should be
used as the canonical docs/results hub from all worktrees.

The first live Gemma bootstrap run now also exists as a concrete example of the
same branch-aware method being reused on a second model family:

- `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/v000/run01_2026-04-17_134308_EDT/`

That run used a user-local Ollama `0.21.0` runtime on `127.0.0.1:11435`
because the system Ollama install was still too old for `gemma4:e4b`. The
important methodology point is that the workflow stayed the same even when the
local runtime path needed an execution workaround.

For evaluation runs, images stored under:

- `z_reference_docs/Data_set_Storage/`

may be copied into worktree-local or prompt-lab run folders when needed for
`bda-svc` / `bda_eval` execution and review. Those copied images may remain in
the run folders as part of the saved evaluation artifact set.

The dedicated branch/worktree refresh procedure now lives in:

- `z_reference_docs/GIT_WORKTREE_UPDATE_WORKFLOW.md`

## Methodology Framework

### Core Method

The working method is:

1. understand the required doctrinal output
2. understand the target model's prompt behavior
3. keep the live runtime contract stable during exploration
4. iterate prompts locally in the prompt lab
5. evaluate against concrete seed cases and regression cases
6. revise one prompt surface at a time where possible
7. promote changes into live config only after they clearly earn it

This keeps the process structured enough to explain later and controlled enough
to avoid random prompt drift.

Runtime-contract gate:

- before applying any prompt idea from doctrine, Qwen docs, or general
  prompting references, confirm that it fits the current `upstream/main`
  placeholders, schemas, bbox convention handling, and Ollama call structure
- if a prompt idea requires changing those interfaces, treat it as a code/design
  change rather than a prompt-only experiment

### Source Hierarchy

Prompt decisions are currently guided by this source order:

0. **Current runtime contract on `upstream/main`**
   The code defines what prompt placeholders, output schemas, bbox conventions,
   and model-call behavior are actually available.
1. **BDA doctrine**
   The doctrine defines what the outputs should mean.
2. **Model-specific VLM documentation**
   The model docs define how the model is most likely to respond well.
3. **General prompting best practices**
   These help when they do not conflict with the model-specific guidance.
4. **Observed experiment results**
   Real output behavior can force adjustments when theory and practice differ.

### How Each Source Type Influences Prompt Design

#### BDA Doctrine

Doctrine is used to shape:

- the meaning of valid damage categories
- the scope of Phase 1 physical damage assessment
- what should not be inferred beyond visible evidence
- how to interpret target types such as buildings and military equipment

Doctrine is not being treated as a prompt-writing guide. It is being treated as
the semantic standard the outputs should approximate.

#### Qwen / VLM Documentation

Model-specific VLM material is used to shape:

- prompt structure
- message role separation
- wording style
- localization instructions
- coordinate conventions
- multi-image handling expectations
- behaviors to avoid, such as bloated or conflicting prompt instructions

For the current phase, the Qwen documents are the primary model-specific
authority because the active model is `qwen3-vl:8b-instruct`.

#### General Prompting Guides

Anthropic, OpenAI, and Gemini guides are being used for:

- clarity and directness principles
- instruction ordering
- consistency of output constraints
- prompt decomposition ideas
- evaluation hygiene

These are supporting references, not the main authority for Qwen behavior.

#### Experiment Results

Observed results influence:

- whether a prompt is actually usable in practice
- whether schema compliance stays reliable
- whether bbox behavior is usable for downstream cropping
- whether doctrine-aligned wording produces better or worse outputs
- whether we need to tighten, simplify, or revert a prompt draft

## Current Working Rules

The current working rules for this phase are:

- keep the live runtime contract unchanged while exploring prompt drafts
- treat Qwen docs as the primary authority for Qwen-specific tactics
- keep the shared system prompt short and policy-only
- keep task mechanics in task prompts
- prefer direct wording over bloated explanatory prose
- preserve the current output fields and configured bbox contract during Phase 1
- preserve the current detection placeholders `{detection_guidance}`,
  `{bbox_format}`, and `{bbox_scale}` unless intentionally testing a code-level
  prompt contract change
- treat doctrine-guided detection instructions as part of the current live
  baseline, not as a separate future-branch experiment
- account for `json-repair` and `think=False` when interpreting schema-validity
  results, because prompt reliability is now supported by both prompt text and
  runtime parsing behavior
- treat anything run before `2026-04-10` as archived history for the prior
  model-tag sequence, not as active evidence for the current sequence
- document material changes to method, prompt direction, or interpretation
- avoid promoting prompt changes into the live config too early
- use current `main` as the source of truth unless a future unmerged upstream
  branch needs separate review
- treat bbox localization quality as an upstream gate for interpreting
  assessment confidence, because loose detections produce looser crops and can
  soften otherwise strong damage judgments
- treat `tank.jpg` as a hard pressure test, not a sufficient promotion gate by
  itself; future detect-only grounding changes should be checked against a
  mixed validation pack that includes other target classes, intact controls,
  and a negative scene
- when bbox or grounding failures survive multiple prompt revisions, check
  community field reports for backend/runtime variance across Ollama and other
  inference stacks before concluding that prompt wording or YAML structure is
  the only root cause
- use full-stack mixed sweeps mainly to expose where regressions live, then
  move back to detect-only mixed sweeps when the goal is to improve the
  grounding rule itself; otherwise assessment/summary changes can blur the real
  detection lesson
- when a detect-only mixed-sweep candidate produces one useful recovery and one
  fatal false positive, treat it as partial-reuse evidence, not as a near-win;
  carry forward only the specific rule that helped and explicitly block the new
  failure mode in the next draft
- when later image-level clarification establishes ground truth for a sweep
  case, update the critique and promotion logic accordingly rather than leaving
  the older weaker interpretation in place
- when the next detect-only candidate preserves the validated recovery and
  removes the fatal false positive, treat that as the new leading detect rule
  and shift attention to unchanged downstream issues that remain in assessment
  or summary
- if that detect-only candidate also repeats cleanly across the same mixed pack
  aside from routine metadata fields, treat the detect rule as confirmed and
  stop reopening it unless a new regression appears on a broader dataset

## Current Branch-Handling Method

The current branch-handling method is:

1. keep local `main` as a clean mirror of `upstream/main`
2. treat that clean mirror as the source of truth for the live
   prompt/runtime/eval contract
3. do active model and feature work in dedicated worktrees instead of on
   `main`
4. keep new prompt-lab documentation under the numbered model-first,
   branch-second roots in `z_reference_docs/Prompt_Labs/`
5. when `upstream/main` moves, update branches in this order:
   - `main`
   - `model/<model-slug>`
   - `feat/<model-slug>/<topic>`
   following `z_reference_docs/GIT_WORKTREE_UPDATE_WORKFLOW.md`

## Current Active-Lab Baseline Interpretation

As of `2026-04-10`, the first fresh baseline run in the active
`qwen3-vl:8b-instruct` lab is recorded under:

- `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/experiments/runs/baseline/run01_2026-04-10_205704_EDT/`

Baseline headline result:

- `target_0.target_type`: `military_equipment`
- `target_0.damage_category`: `DESTROYED`
- `target_0.confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`

Compared with the archived `qwen3-vl:8b-instruct-q8_0` baseline:

- the bbox widened to the right from `[51, 37, 102, 73]` to
  `[51, 37, 128, 73]`
- confidence softened from `CONFIRMED` to `PROBABLE`
- subtype wording drifted toward `locomotive` inside the supporting logic

Current interpretation:

- this still looks like a model-side localization issue, not a bbox conversion
  bug
- the widened box likely increases irrelevant context in the target crop
- the softer confidence is therefore likely downstream of weaker localization,
  not the first problem to tune directly
- the subtype wording is plausibly influenced by updated doctrine guidance that
  now explicitly includes locomotives under `military_equipment`

Method implication:

- do not tune confidence first
- treat detection localization as the next prompt surface to address
- use the new active baseline as the current evidence anchor for future `v001+`
  experiments
- after the `2026-04-11` upstream sync to `21deaf5`, keep using this same
  active sequence because prompt text, model tag, and dependencies did not
  change; only the baseline metadata and config snapshot needed refresh

## Current Immediate Prompt Direction

The active detection-localization sequence has now produced four non-winning
drafts:

- `v001`
- `v002`
- `v003`
- `v004`

What those drafts established:

- `v001` and `v002` moved the box but stayed off target and inflated
  confidence
- `v003` tightened the box numerically without fixing target-body grounding
- `v004` proved that fire-source anchoring can over-shrink onto the wrong patch
  and worsen subtype drift
- `v005` proved that longer point-first prose can still be too weak to change
  the model at all
- `v006` is the first candidate to improve bbox placement materially, but it
  also changed downstream confidence and summary behavior
- `v006` run02 repeated the improved bbox exactly, which confirms the bbox gain
  on the current seed case even though downstream calibration issues remain

Current direction:

1. keep bbox grounding as the first problem
2. keep confidence tuning secondary until crops improve
3. treat subtype drift such as `locomotive` as a separate but related watch
   item
4. use a critique/research/revise loop instead of freehand version drafting
5. let each rejected version contribute only the specific lesson it earned
6. if detection progress stalls again, compare prompt behavior against possible
   backend/runtime grounding variance before redesigning the prompt YAML
   structure
7. prefer code-supported grounding tests only when they stay aligned with the
   model's native grounding regime; do not assume `_pixels` is better than
   `xyxy_1000` just because the runtime can support it
8. when a grounding run fails hard, capture and review the raw detection
   payload before inventing a new prompt hypothesis

## Current Evaluation Method

Prompt evaluation is being separated by task so failures are easier to diagnose.

Current tracks:

- `system + assess_damage`
- `detect_objects`
- `summarize_scene`

The intended evaluation criteria include:

- schema validity
- doctrinal alignment
- confidence calibration
- visual-evidence grounding
- bbox usability
- consistency between target-level outputs and scene-level summary

Output organization rule:

- baseline runs should be written under:
  `experiments/runs/baseline/runNN_YYYY-MM-DD_HHMMSS_TZ/`
- candidate runs should be written under:
  `experiments/runs/vNNN/runNN_YYYY-MM-DD_HHMMSS_TZ/`
- include a `RUN_MANIFEST.md` that records the run condition, input, command or
  run method, output artifacts, headline result, and caveats

Critique/research rule:

- every candidate run should also produce a `CRITIQUE.md` in the run folder
- the paired research note should be written to:
  `z_reference_docs/Prompting/Research_Loops/<lab>/<version>/<run_folder>/research.md`
- after the research pass, re-check the most relevant local Prompting and BDA
  references before drafting the next version
- update the main markdown trail after every loop, not only at milestones

Generalization check rule:

- do not call a detection/assessment direction finished on one seed image alone
- once a pair looks promising, test it on at least one clearly damaged vehicle,
  one operational vehicle, and one clearly negative scene
- treat the original tank case as a repeatability check because it can wobble
  even when the broader pair generalizes reasonably

## Current Challenges

The main challenges identified so far are:

- the eval set is still small
- the first manual bbox estimate was wrong
- live JSON alone was not enough for quick bbox review
- prompt quality cannot be judged cleanly if detection and assessment errors are
  mixed together
- general prompting guidance can be useful, but it can also introduce habits
  that do not fit Qwen well if applied too literally
- the earlier `q8_0` experiment sequence is still useful background, but it is
  now archive material rather than the active current-main sequence
- the new active lab needs a first fresh baseline run before its eval manifests
  can be fully populated
- schema-validity improvements may now come from both prompt wording and
  runtime support such as `json-repair`; evaluation notes should distinguish
  prompt effects from parser/runtime effects where practical
- the strongest current pair can generalize reasonably across extra scenes and
  still wobble on the original tank seed, so one-image success is not enough
- community reports outside the official docs suggest that Qwen grounding
  quality can also vary by inference backend, so prompt failures should not be
  blamed on YAML structure alone without checking runtime-side variance

## Current Direction

The current direction is:

- continue using the Qwen-first prompt lab
- use the refreshed active-lab baseline from current `main`
- archive the prior `q8_0` sequence instead of letting it steer new baseline
  conclusions
- store new experiment outputs in version-first folders under
  `experiments/runs/`
- store paired research notes under `z_reference_docs/Prompting/Research_Loops/`
- use a critique/research/revise loop after every candidate run
- expand eval coverage before promoting prompt changes
- keep the temporary live debug export only for prompt tuning
- record prompt-method changes and rationale here as they happen

## Current Forward Path

The current forward path is now:

1. use the new active lab as the only place for new current-main experiments
2. keep the current fresh baseline as the comparison anchor
3. keep the frozen `v006` detection and `v009` assessment pair as the current
   best-known benchmark
4. run a small cross-image generalization sweep before treating the current
   direction as done
5. update the full markdown trail after every loop
6. add more seed cases, especially buildings and harder multi-object scenes,
   once the current localization tactic is less brittle
7. keep the current top-level YAML structure stable unless repeated evidence
   shows that prompt-surface tuning and backend-aware diagnosis are both
   exhausted
8. re-open grounding once more before a summary-only cycle when grounding still
   looks less trustworthy than the downstream summary layer

This is now a structured loop phase rather than a reset-and-rebaseline phase.
The goal is to make each failed run more reusable by documenting why it failed
and what research directly shaped the next draft.

Active-sequence note:

- the new active lab starts from a fresh `v000`
- archived `v005` through `v010` remain useful background, but they are no
  longer the active candidate chain
- the first fresh baseline run in the new lab is now established
- `v004` is the first candidate run executed under the new
  critique/research/revise workflow
- `v005` is the second candidate run in that same loop and matched the
  baseline exactly, which now points the next draft toward a shorter,
  contrastive-example style
- `v006` is the third candidate run in that same loop and is now the
  best-so-far bbox candidate, pending repeat confirmation
- `v009` is now the best assessment candidate in the active line
- `v010` was the first `_pixels` grounding experiment and failed by collapsing
  the tank seed to `object_not_found`
- the temporary local debug-export path now also writes `pipeline_debug.json`
  so failed grounding runs keep the raw detection payload for later diagnosis
- `v011` recovered detection after `v010`, which supports the coordinate-
  mismatch diagnosis, but its bbox converged toward the older `v001` / `v002`
  family rather than clearly improving past the frozen `v009` working baseline
- `v012` preserved the corrected contract but still failed to improve the raw
  grounding choice, which is stronger evidence that prompt-only detection
  tuning is stalling on this seed case
- a code-level two-pass refinement aid is now implemented behind
  `detection_vlm.refinement_enabled`; it re-runs detection inside an expanded
  ROI around each accepted first-pass box and only accepts refined boxes that
  still overlap the original detection
- `v013` is the first run of that code-level aid; it preserved the stronger
  `DESTROYED` + `PROBABLE` behavior but did not improve bbox quality because
  the first pass narrowed and the ROI-local second pass returned no detections
- `v013` run02 repeated that exact behavior, which confirms the current
  refinement setting is a stable non-win rather than simple run-to-run wobble
- `v014` then widened the refinement ROI substantially and still got no
  ROI-local second-pass detections, which means ROI size alone is not the main
  blocker in the current two-pass design

### Temporary Debug Instrumentation

The local prompt workflow currently uses a temporary debug-export path on local
`main`.

When a run is executed with `--debug-export-images`, the debug folder may now
contain:

- overlay images
- crop images
- `pipeline_debug.json`

`pipeline_debug.json` currently exists to preserve internal detection-stage
evidence that would otherwise be lost once the final fallback report is built.

Current intended use:

- inspect the raw detection response before validation
- inspect the repaired/parsed detection payload when available
- confirm which bbox convention was active during the run
- compare raw bbox output against the final pixel bbox after conversion
- diagnose whether a failure came from prompt behavior, schema parsing, target
  filtering, or bbox validation
- inspect refinement ROI attempts, translated child candidates, and the final
  refinement selection when code-level grounding aids are enabled

Method rule:

- when a grounding experiment fails hard, review `pipeline_debug.json` before
  drafting the next prompt hypothesis
- treat this file as temporary lab instrumentation, not part of the live
  external report contract
- if `pipeline_debug.json` shows a valid raw bbox that still lands on the wrong
  area, treat that as a model-grounding-choice problem rather than a
  bbox-conversion problem
- when that happens, prefer changing the grounding wording before changing the
  runtime contract again
- once prompt-only grounding variants stall, prefer the smallest code-level aid
  first; currently that means enabling the two-pass ROI refinement path before
  attempting a larger runtime redesign
- if the first refinement run changes the first-pass raw bbox before the second
  pass helps at all, treat that as a wobble signal and confirm with a repeat
  before judging the refinement path itself too harshly
- once that repeat holds exactly, treat the current refinement setting as a
  confirmed non-win and move to parameter tuning instead of repeating again
- if a materially wider ROI still yields no second-pass detections, stop
  spending cycles on ROI-width-only tuning and change the refinement method

## Update Rule

This document should be updated when any of the following happen:

- the methodology changes
- the source hierarchy changes
- a prompt draft is promoted or reverted
- the eval method changes
- a new model becomes the active target
- a major challenge changes the direction of work

When a major change happens, we should explicitly ask:

- update the methodology document now, or
- wait until we have one more chunk of progress to record with it

## Entries

### 2026-04-03 22:48 EDT — Methodology Document Created

What was established:

- a dedicated living record for prompt-development methodology
- a requirement to track not only prompt edits, but also source usage,
  decision rationale, challenges, and directional changes
- an expectation that major method changes should trigger an explicit decision
  on whether to update this document immediately or shortly afterward

Why it matters:

- this will make it easier to explain the work clearly in a presentation,
  report, or oral discussion
- it prevents the methodology from becoming implicit knowledge that only exists
  in chat history or memory

### 2026-04-03 22:48 EDT — Initial Methodology Baseline Recorded

State recorded:

- live runtime is an Ollama dual-VLM pipeline
- prompt experimentation is currently local-first in `z_reference_docs`
- doctrine is the semantic authority
- Qwen docs are the current model-specific authority
- general prompting guides are secondary support
- `z_reference_docs/config.yaml.backup` is the fallback reference copy
- the Qwen prompt lab is the active experimentation workspace

Why it matters:

- this captures the starting methodology before additional prompt iterations,
  reversions, or directional changes are layered on top

### 2026-04-03 22:48 EDT — Existing Prompt-Development Work Summarized

Work captured so far:

- BDA doctrine references were collected, OCR'd or converted to searchable
  Markdown, and indexed locally
- prompting guides and model references were organized and indexed under
  `z_reference_docs/Prompting/`
- a Qwen-specific prompt lab was created
- the first prompt drafts `v001` through `v004` were created locally
- eval manifests were created for assessment, detection, and summary work
- a first seed case was built from `tests/test_images/01.jpg`
- a copied live JSON report was stored next to local eval assets for quick
  comparison
- a temporary live debug export path was added so bbox overlays and crops could
  be inspected more easily during prompt work

Key lesson already learned:

- prompt development needs tighter instrumentation than JSON output alone
- bbox/debug visibility changed the workflow materially because it exposed that
  the first manual annotation was not reliable enough

### 2026-04-12 16:30 EDT — Critique / Research / Revise Loop Started With `v004`

What changed:

- Began the first structured three-loop cycle focused on `detect_objects`
  bbox grounding.
- Added per-run `CRITIQUE.md` notes to the experiment workflow.
- Added `z_reference_docs/Prompting/Research_Loops/` as the home for online
  research notes paired to each run.
- Drafted and ran
  `v004_detect_objects_fire-source-object-body.yaml`.

`v004` result:

- bbox changed from baseline `[51, 37, 128, 73]` to `[51, 37, 102, 61]`
- confidence stayed `PROBABLE`
- manual review showed the box over-shrank around the wrong fire-adjacent
  patch instead of the visible target body
- subtype drift worsened to `locomotive or rolling stock`

Why it mattered:

- This was the first full test of the new loop structure.
- It proved that fire-source anchoring is too narrow as a localization tactic
  for the current seed image.
- It also produced the first paired research note for the active sequence,
  which now argues for a point-or-center-first, occlusion-aware next draft
  instead of another shrink-only variant.

### 2026-04-12 16:50 EDT — `v005` Showed No Observable Change From Baseline

What changed:

- Drafted and ran
  `v005_detect_objects_point-first-occlusion-aware.yaml`.
- Added the second paired critique and research note in the active loop.

`v005` result:

- bbox matched baseline exactly: `[51, 37, 128, 73]`
- confidence matched baseline exactly: `PROBABLE`
- subtype drift and summary text matched baseline exactly

Why it mattered:

- `v005` showed a different failure mode than `v004`: the prompt was too weak
  to move the model at all.
- That shifted the next draft away from abstract grounding prose and toward a
  shorter, more example-driven contrastive prompt.

### 2026-04-12 17:05 EDT — `v006` Became The First Promising BBox Candidate

What changed:

- Drafted and ran
  `v006_detect_objects_short-contrastive-example.yaml`.
- Closed the first three-loop critique/research/revise cycle with a cycle
  summary under `experiments/cycles/`.

`v006` result:

- bbox changed from baseline `[51, 37, 128, 73]` to `[46, 46, 128, 92]`
- confidence increased from `PROBABLE` to `CONFIRMED`
- supporting logic removed `locomotive`, but introduced stronger K-kill-style
  language

Why it mattered:

- `v006` is the first active-sequence candidate to move the bbox materially
  onto the visible burning target body.
- It suggests the shorter, contrastive-example style is more salient for this
  model/image pair than the longer abstract grounding blocks.
- It is still not a clean promotion because the bbox improvement came with
  downstream confidence and summary side effects, so repeat confirmation is now
  the most sensible next step.

### 2026-04-12 17:20 EDT — `v006` Confirmation Repeat Held Exactly

What changed:

- Ran a confirmation repeat for `v006`.

Result:

- `v006` run02 matched `v006` run01 exactly:
  - bbox `[46, 46, 128, 92]`
  - `CONFIRMED` confidence
  - same supporting logic
  - same summary text

Why it mattered:

- This confirms that the bbox improvement from `v006` is repeatable on the
  current seed case.
- The leading prompt problem now shifts from pure bbox localization to the
  downstream confidence and summary changes that came with that improved crop.

### 2026-04-12 — Cross-Image Generalization Sweep Completed

What was checked:

- frozen `v006` detection + `v009` assessment
- tank, destroyed truck, operational truck, office

What it showed:

- the pair stayed sensible on the truck and office scenes
- the tank seed remained unstable across repeats
- the pair does not look tank-only, but the tank image is still the pressure
  point

Why it matters:

- we should not overfit to one seed case
- a candidate can be broadly reasonable and still need one more stability check
  on the original image

### 2026-04-12 18:20 EDT — Backend Variance Added To Grounding Diagnosis Rule

What was established:

- outside-official community research was added as a diagnostic backstop for
  persistent grounding failures
- multiple reports across Ollama-adjacent and other inference stacks indicate
  that Qwen grounding quality can vary by backend/runtime, not just prompt
  wording
- the current top-level YAML split between `system`, `detect_objects`,
  `assess_damage`, and `summarize_scene` still looks appropriate for the
  project intent and current model

Why it matters:

- this prevents us from rewriting the YAML architecture too early when a
  grounding problem may be partly runtime-sensitive
- it adds a cleaner debugging rule: exhaust prompt-surface tuning first, then
  sanity-check backend/runtime variance before blaming structure alone

### 2026-04-12 19:00 EDT — Next Grounding Cycle Re-Prioritized Toward `_pixels`

What was established:

- although cycle 02 ended with a summary-focused recommendation, the grounding
  issue still remains the highest-risk blocker for trustworthy downstream work
- a fresh research pass pointed to native image-space coordinates as the next
  highest-value experiment because Qwen grounding examples are box/point-native
  and the current runtime already supports `xyxy_pixels`
- the next queued version is now `v010`, which keeps the best-known
  `v006`/`v009` direction but switches the detection bbox convention to
  `xyxy_pixels`

Why it matters:

- this gives us a stronger coordinate-contract test before we spend a full
  cycle polishing summary wording on top of still-shaky grounding
- it uses an existing runtime capability rather than forcing a structural YAML
  redesign

### 2026-04-12 20:45 EDT — `v010` Failure Redirected Grounding Back To The Normalized Contract

What was established:

- deeper post-run research indicates Qwen3-VL is more naturally aligned with a
  normalized `0..999` / `0..1000` grounding regime than with raw pixel output
- `v010` likely failed at the contract boundary: if the model still emitted
  normalized-style boxes while the runtime expected `_pixels`, the validator
  would reject those detections and the pipeline would fall back to
  `object_not_found`
- the next queued recovery candidate is now `v011`, which returns to
  `xyxy_1000` and rewrites detection to be more explicitly Qwen-native
- raw detection-response export is now part of the temporary debug workflow so
  future grounding failures are diagnosable without guessing

Why it matters:

- this prevents us from repeating the direct `_pixels` swap even though the
  runtime supports it
- it gives the next grounding step a cleaner target: keep the normalized
  contract and improve the prompt surface itself

### 2026-04-12 20:44 EDT — `v011` Recovered Detection But Not A Clear Bbox Win

What was established:

- `v011` successfully recovered detection after `v010` failed, which supports
  the view that `v010` was primarily a coordinate-contract mismatch
- the new raw debug export confirmed the candidate returned a valid normalized
  detection payload rather than failing at schema parsing or bbox validation
- `v011` preserved the stronger frozen `v009` assessment behavior:
  `DESTROYED` + `PROBABLE`
- the recovered bbox `[56, 46, 123, 76]` converged toward the older
  `v001` / `v002` tightened-box family instead of clearly reproducing or
  surpassing the stronger `v006` bbox win

Why it matters:

- this is useful evidence, but it is not a promotion signal
- the normalized contract looks correct, but the point-first wording still does
  not appear to be the final grounding answer

### 2026-04-12 21:05 EDT — Cycle 03 Workflow Tightened Around Raw Debug Evidence

What was established:

- the `v011` debug payload showed a valid normalized raw bbox, which means the
  runtime conversion path was not the main problem in that run
- the remaining error was the model's grounding choice itself
- the cycle workflow now needs an explicit branch:
  - invalid / rejected raw bbox -> investigate contract or validation
  - valid but off-target raw bbox -> change grounding wording, not the
    conversion logic
- the next queued candidate is `v012`, which keeps the normalized contract but
  drops the point-first method and adds a direct anti-over-shrinking rule

Why it matters:

- this keeps future grounding loops from changing the wrong layer
- it turns `pipeline_debug.json` into a real decision tool rather than just an
  extra artifact

### 2026-04-12 21:10 EDT — `v012` Strengthened The Case That Prompt-Only Grounding Is Stalling

What was established:

- `v012` stayed on the corrected normalized contract and preserved the stronger
  `v009` assessment behavior
- the raw debug payload still showed the wrong model grounding choice:
  baseline `[200, 300, 500, 600]` changed to `v012` `[200, 400, 500, 700]`
- the prompt changed the vertical placement of the box, but it did not recover
  the stronger `v006` behavior or produce a clear bbox win

Why it matters:

- this is stronger evidence that the current prompt-only detection search space
  may be near exhaustion for this seed case
- the next move should likely be either:
  - a broader control sweep with the best-known pair, or
  - a code-level grounding aid such as two-pass refinement or a visually marked
    / region-guided approach

### 2026-04-03 23:27 EDT — Parallel Inspection Worktree Added

What changed:

- created a separate temporary inspection worktree
- set it to track `upstream/feature/add-export-metrics`
- saved a temporary multi-root VS Code workspace so both the main repo and the
  inspection worktree could be viewed side by side

Why it matters:

- it prevents feature-branch inspection from polluting the active prompt
  workspace
- it gives us a stable way to compare likely future upstream changes against
  the current `main` branch while keeping the prompt lab intact

### 2026-04-03 23:27 EDT — Prompt Labs Renamed And Split By Branch Context

What changed:

- renamed the original main-branch lab to
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/`
- created a second temporary branch-specific lab

Method decision:

- separate prompt outputs and eval artifacts by branch context
- do not mix `main`-based prompt experiments with
  `feature/add-export-metrics`-based prompt experiments

Why it matters:

- this makes comparisons easier to explain later
- it reduces the chance of using the wrong baseline, eval asset, or prompt
  version when both branches are being explored in parallel
- this temporary split was later collapsed back to the main lab once PR `#124`
  merged into `main`

### 2026-04-03 23:27 EDT — First Inspection Pass Completed On `feature/add-export-metrics`

What was learned:

- the branch is better understood as a forward-moving candidate future version
  of `main`, not a totally different architecture
- it changes more than export metrics alone
- it affects:
  - export metadata
  - model env overrides
  - detection bbox conventions
  - doctrine-guided detection prompting
  - JSON repair and structured-output robustness
  - CI and tests

Method decision taken:

- do not merge this branch wholesale into `main`
- treat it as a donor branch
- selectively adopt useful changes later after review

Why it matters:

- this adds a repo-handling method to the prompt methodology
- it protects current prompt work from unnecessary branch churn while still
  keeping us aligned with likely upstream direction

### 2026-04-03 23:54 EDT — Baseline Prompt Comparison Completed For Export-Metrics Branch

What was compared:

- main lab baseline prompts
- export-metrics inspection-lab baseline prompts

What was learned:

- the shared `system` prompt is effectively unchanged
- `detect_objects` is the main point of divergence
- the export-metrics branch replaces the self-contained detection prompt style
  with a more parameterized contract:
  - `{detection_guidance}`
  - `{bbox_format}`
  - `{bbox_scale}`
- the main branch keeps a more explicit static detection workflow with:
  - internal counting guidance
  - explicit object rules
  - hardcoded `0–1000` xyxy box expectations
- `assess_damage` is only lightly softened on the export-metrics branch
- `summarize_scene` is also only lightly softened on the export-metrics branch

Method consequence:

- if the export-metrics branch becomes an active prompt target, the first
  prompt surface worth deeper attention is `detect_objects`
- `system` does not currently require branch-specific prompt treatment

Why it matters:

- this gives us a clean written explanation of where the branch is genuinely
  different at the prompt level before we start new experiments there

### 2026-04-06 16:40 EDT — `main` Became The Active Source Of Truth Again

What changed:

- PR `#124` merged the former `feature/add-export-metrics` work into
  `upstream/main`
- local `main`, `origin/main`, and `upstream/main` were resynced
- the temporary local debug-export instrumentation was merged on top of the new
  `main`

Method consequence:

- the separate export-metrics lab was retired
- prompt development should now continue from the main lab only
- at that point, the main-lab baseline needed to be refreshed so it reflected
  the current live `main` prompt/runtime contract; that refresh was completed
  in the later `2026-04-06 20:13 EDT` entry

Why it matters:

- the project crossed from parallel branch comparison into post-merge main
  reconciliation
- this simplifies the methodology, but it also means some baseline notes and
  eval assumptions now need cleanup before more prompt experiments continue

### 2026-04-06 17:05 EDT — Main-Only Prompt Workflow Confirmed

What changed:

- the temporary branch-specific prompt lab and inspection setup were retired
- the active workflow was simplified back to one lab on `main`

Method consequence:

- the next work is no longer branch comparison
- the next work is baseline refresh, eval refresh, and prompt-draft
  reconciliation on top of current `main`

Why it matters:

- this makes the prompt-development story easier to explain
- it also makes the evaluation path cleaner, because every new experiment now
  traces back to one live runtime contract

### 2026-04-06 20:05 EDT — Methodology Updated For Current Upstream/Main Runtime Contract

What changed:

- reviewed the prompt methodology against the synced `upstream/main`
  implementation
- added the current runtime-contract details that now matter for prompt work:
  - configurable detection bbox convention
  - `{detection_guidance}`, `{bbox_format}`, and `{bbox_scale}` detection
    placeholders
  - doctrine-driven detection guidance
  - `json-repair` structured-output repair
  - `think=False` Ollama call behavior
  - detection and assessment model environment overrides

Method consequence:

- the old static detection-prompt baseline is now historical context, not the
  current live contract
- refreshed prompt-lab baselines must preserve the current parameterized
  detection contract
- future schema-validity evaluation should account for both prompt wording and
  runtime parsing support

Next prompt-work step:

- refresh the main-lab baseline from current `upstream/main`, then reconcile
  `v001` through `v004` against that live contract before running new
  experiments

### 2026-04-06 20:13 EDT — Main-Lab Baseline Refreshed And Prompt Chain Reconciled

What changed:

- refreshed `baseline/config.pipeline-baseline.yaml` from
  `upstream/main:src/bda_svc/pipeline/config.yaml`
- refreshed `v000_baseline.prompts.yaml` as the current-main prompt baseline
- preserved `v001` through `v004` as pre-merge draft history
- created `v005` through `v008` as the active post-merge reconciled prompt
  chain
- updated the prompt version log and lab README

Reconciliation outcome:

- `v005` reconciles the short policy-only `system` prompt from `v001`
- `v006` reconciles the single-target `assess_damage` prompt from `v002`
- `v007` reconciles the direct grounding `detect_objects` prompt from `v003`
  while preserving `{detection_guidance}`, `{bbox_format}`, and `{bbox_scale}`
- `v008` reconciles the constrained plain-text `summarize_scene` prompt from
  `v004`

Verification:

- the refreshed baseline config body matches `upstream/main`
- the refreshed baseline and `v005` through `v008` YAML files parse correctly

Next prompt-work step:

- generate fresh current-main baseline outputs and then evaluate `v005` through
  `v008` before continuing new prompt experiments

### 2026-04-06 20:42 EDT — First Baseline vs Reconciled Chain Experiment Run

What changed:

- confirmed the prompt-lab rule that every new experiment output set should be
  written to a timestamped subfolder under `experiments/runs/`
- updated eval manifests to use the current repo image fixture
  `tests/data/tank.jpg`
- ran one timestamped comparison under
  `experiments/runs/2026-04-06_203823_EDT/`
- compared:
  - `current-main_baseline`
  - `v008_reconciled-chain`
- wrote a `RUN_MANIFEST.md` inside the timestamped run folder

Headline result:

- both conditions produced one `military_equipment` detection
- both assessed the target as `DESTROYED` with `CONFIRMED` confidence
- the current-main baseline exported bbox `[51, 37, 102, 73]`
- the `v008` reconciled chain exported bbox `[51, 49, 115, 85]`
- `v008` produced a more constrained summary that stayed closer to prior target
  assessments and avoided the baseline's stronger "zero combat capability"
  language

Method consequence:

- `v008` is not accepted or rejected from this single seed run
- the bbox difference needs manual visual review before any detection-prompt
  decision
- future runs should continue using timestamped output folders with manifests

### 2026-04-06 20:56 EDT — Bbox Visual Review Identified Detection Localization Failure

What changed:

- reviewed the baseline and `v008` debug overlays from
  `experiments/runs/2026-04-06_203823_EDT/`
- created `bbox_review_sheet.jpg` for side-by-side inspection
- captured raw VLM detection responses in `raw_detection_responses.md`
- added `DET-09 bbox_off_target` to the failure taxonomy
- updated the run manifest and prompt version log

Finding:

- both the current-main baseline and `v008` boxes are visually off target
- baseline raw bbox was `[200, 300, 400, 600]`, converted to pixel bbox
  `[51, 37, 102, 73]`
- `v008` raw bbox was `[200, 400, 450, 700]`, converted to pixel bbox
  `[51, 49, 115, 85]`
- the conversion is consistent with the configured `xyxy_1000` convention, so
  this is a VLM localization failure rather than a runtime bbox conversion bug

Method consequence:

- do not promote `v008` from this run
- the next prompt iteration should focus on detection localization before we
  judge summary improvements
- future eval notes should separate:
  - correct target class / damage label
  - bbox usability for crop generation
  - summary quality

### 2026-04-06 — `v009` Detection-Only Follow-Up Drafted

What changed:

- created
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/experiments/versions/v009_detect_objects_physical-target-only.yaml`
- parented `v009` to `v008`
- changed only the `detect_objects` prompt surface
- preserved:
  - `{categories}`
  - `{detection_guidance}`
  - `{bbox_format}`
  - `{bbox_scale}`
  - the `DetectionResponse` JSON fields
  - the configured runtime bbox convention

Why:

- both the current-main baseline and `v008` produced well-formed but visually
  off-target boxes on the tank fixture
- raw detection responses showed the model returned the off-target coordinates,
  so the failure is prompt/model localization rather than runtime conversion

Methodology update:

- `v009` adds explicit "physical target object only" guidance
- the prompt now forbids boxing flames, smoke, dust, shadows, roads, terrain,
  blast effects, or plume effects as the target
- the next experiment should compare baseline, `v008`, and `v009` overlays
  before any promotion decision

### 2026-04-06 — `v009` Experiment Run Rejected

What changed:

- ran a timestamped experiment under
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/experiments/runs/2026-04-06_210720_EDT/`
- compared:
  - current-main baseline
  - `v009_physical-target-only`
- created `bbox_review_sheet.jpg` for visual review
- updated the run manifest, failure taxonomy, prompt version log, and lab README

Finding:

- current-main baseline exported bbox: `[51, 37, 102, 73]`
- `v009` exported bbox: `[51, 49, 128, 73]`
- visual review showed the `v009` box still covered the smoke/plume region
  rather than the physical vehicle/equipment body
- `v009` also introduced unsupported "locomotive" identity detail in
  assessment/supporting logic and summary text

Method consequence:

- reject `v009` for now
- adding negative effect-exclusion wording was not sufficient to correct the
  localization failure
- the next detection candidate should use a different localization strategy,
  not just a longer list of forbidden non-target regions
- track the unsupported subtype wording separately from bbox placement using:
  - `AS-06 unsupported_identity_detail`
  - `SUM-05 unsupported_identity_detail`

### 2026-04-06 — `v010` Effect-Cue-Anchored Detection Drafted

What changed:

- created
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/experiments/versions/v010_detect_objects_effect-cue-anchored.yaml`
- parented `v010` to `v008` instead of rejected `v009`
- changed only the `detect_objects` prompt surface
- preserved:
  - `{categories}`
  - `{detection_guidance}`
  - `{bbox_format}`
  - `{bbox_scale}`
  - the `DetectionResponse` JSON fields
  - the configured runtime bbox convention

Why:

- `v009` proved that negative "do not box effects" wording was not enough
- the next strategy needs to tell the model how to use fire, smoke, scorch
  marks, and debris constructively without treating those effects as the target

Methodology update:

- `v010` treats fire, smoke, scorch marks, blast marks, and debris as cues that
  a damaged target may be nearby
- after using those cues, the prompt tells the model to anchor the box to
  visible solid target features such as hull, chassis, turret, tracks, walls,
  roofline, corners, or facade
- the next experiment should compare current-main baseline, `v008`, rejected
  `v009`, and `v010` overlay/crop behavior before any promotion decision

### 2026-04-06 — `v010` Experiment Run Rejected

What changed:

- ran a timestamped experiment under
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/experiments/runs/2026-04-06_212840_EDT/`
- compared:
  - current-main baseline
  - `v010_effect-cue-anchored`
- generated a review sheet that also included prior `v008` and rejected `v009`
  bbox outputs
- wrote `result_summary.json`
- updated the run manifest, prompt version log, and lab README

Finding:

- current-main baseline exported bbox: `[51, 37, 102, 73]`
- `v008` exported bbox: `[51, 49, 115, 85]`
- rejected `v009` exported bbox: `[51, 49, 128, 73]`
- `v010` exported bbox: `[51, 49, 128, 85]`
- visual review showed the `v010` box still covered the smoke/plume region
  rather than the physical vehicle/equipment body
- `v010` improved the unsupported "locomotive" identity detail observed in
  `v009`, but did not fix the core localization problem

Method consequence:

- reject `v010` for now
- using fire/smoke/debris as contextual cues plus solid-structure anchoring was
  still not enough on the tank fixture
- the next candidate likely needs a more concrete spatial strategy, not only
  semantic wording around effects and structure

### 2026-04-06 20:21 EDT — Current-Main Baseline Experiment Run Created

What changed:

- created the first timestamped experiment output folder:
  `experiments/runs/2026-04-06_202124_EDT/`
- ran the current live main baseline against `tests/data/tank.jpg`
- enabled the local temporary debug image export for bbox/crop inspection
- added `experiments/runs/README.md`
- added a run-specific `RUN_MANIFEST.md`

Result summary:

- detections: `1`
- target type: `military_equipment`
- damage category: `DESTROYED`
- confidence level: `CONFIRMED`
- bounding box: `[51, 37, 102, 73]`
- inference time: `13.36`

Method consequence:

- all future experiment outputs should use timestamped folders under
  `experiments/runs/`
- this run is the refreshed current-main baseline output, not an evaluation of
  the reconciled `v005` through `v008` prompt chain

### 2026-04-10 — Upstream `main` Synced Forward And Local Prompt-Tuning Tooling Reapplied

What changed:

- synced local `main` to the new `upstream/main`
- pushed the updated `main` to `origin/main`
- upstream moved from `fe12732` to `c077cd8`
- the stash-based reapply of the local temporary debug-export work produced a
  conflict in `src/bda_svc/export.py`
- the reapply also collided with a new upstream
  `tests/unit/test_export.py`
- merged the local temporary debug-export behavior forward onto the new upstream
  code and tests
- ran `uv sync --dev`, which installed `pytest-mock`
- verified the merged local state with focused tests:
  - `tests/unit/test_cli.py`
  - `tests/unit/test_main.py`
  - `tests/unit/test_export.py`
  - result: `7 passed`

Why:

- `upstream/main` is the source of truth for continued prompt work
- local prompt-tuning instrumentation must survive upstream movement without
  overwriting new team changes
- the current upstream branch now includes additional CLI/export/test coverage,
  so the local debug-export path has to coexist with that newer shape

Methodology update:

- when `upstream/main` moves while local prompt-tuning support code is sitting
  on `main`, the safe update path remains:
  - stash local tracked and untracked debug-export work
  - fast-forward `main` from `upstream/main`
  - push `main` to `origin`
  - reapply the local work and merge conflicts forward carefully
- upstream-owned tests should be preserved and extended rather than replaced
  when local prompt-tuning helpers overlap with them
- after any meaningful upstream sync, treat the prompt-lab baseline and active
  prompt assumptions as potentially stale until the new `main` config, doctrine,
  and interfaces are reviewed
- `z_reference_docs` remained safe throughout because it is local-only and
  excluded from the repo sync flow

Current consequence:

- `main`, `origin/main`, and `upstream/main` are aligned again
- the local temporary debug-export work is preserved on top of the new `main`
- the prompt methodology now needs a fresh review against commit `c077cd8`
  before we continue interpreting prior experiment results as current-baseline
  evidence

### 2026-04-10 — New Upstream Runtime Delta Reviewed

What changed:

- reviewed the upstream range from `fe12732` to `c077cd8`
- separated the changes into:
  - runtime-contract changes that matter for prompt work
  - docs, CI, and test-hardening changes

Runtime findings that matter for prompt work:

- the default detection and assessment model tags in
  `src/bda_svc/pipeline/config.yaml` changed from
  `qwen3-vl:8b-instruct-q8_0` to `qwen3-vl:8b-instruct`
- the `detect_objects` prompt in `src/bda_svc/pipeline/config.yaml` changed:
  - it now tells the model to identify all valid targets first
  - then produce exactly one bounding box per valid target
  - and keep the number of detections equal to the number of identified targets
- the `summarize_scene` prompt was softened:
  - functional impact is still allowed
  - but the wording is narrower and tied more explicitly to prior assessments
- the detection guidance in `src/bda_svc/pipeline/doctrine.yaml` changed:
  - `buildings` is now more scene-central and selective
  - `military_equipment` is broader and now explicitly mentions items such as
    locomotives, artillery systems, radar antennas, and fire control components
- `src/bda_svc/pipeline/interfaces.py` now uses `ollama.Client` and supports:
  - `OLLAMA_HOST`
  - `OLLAMA_API_KEY`
- `src/bda_svc/export.py` now returns the JSON path from `save_json()`

Non-runtime findings:

- `README.md` was rewritten into a cleaner quick-start document
- `docs/101-development.md` and `docs/102-container.md` were added
- CI in `.github/workflows/ci.yml` now includes:
  - unit tests with coverage
  - ARM container build-and-run
  - vulnerability scanning
  - GHCR publish on `main`
  - a pipeline summary job
- `pytest-mock` was added to the dev environment and the unit-test surface was
  expanded significantly

Methodology update:

- the prompt-lab baseline from before `c077cd8` is now stale again
- old experiment results remain useful as historical evidence, but they are no
  longer enough to describe current-main behavior without re-baselining
- before running new prompt experiments, we should refresh:
  - `baseline/config.pipeline-baseline.yaml`
  - `experiments/versions/v000_baseline.prompts.yaml`
  - any eval assumptions that depend on the old default model tag or older
    doctrine wording

### 2026-04-10 18:25 EDT — Prompt Lab Reset Around `qwen3-vl:8b-instruct`

What changed:

- archived the earlier active lab under
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/`
- created the new active lab:
  `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/`
- copied forward reusable dossier notes and failure taxonomy
- refreshed a fresh `v000` baseline from current `main` at `c077cd8`
- created fresh eval manifests for the new model-tag sequence
- reset active prompt numbering so the new sequence starts from `v000`
- changed run organization to the version-first layout:
  - `experiments/runs/baseline/runNN_YYYY-MM-DD_HHMMSS_TZ/`
  - `experiments/runs/vNNN/runNN_YYYY-MM-DD_HHMMSS_TZ/`

Method consequence:

- the archived `q8_0` runs and versions still exist, but they are now clearly
  historical background rather than active evidence
- the new active lab is now the only place where current-main prompt
  conclusions should be recorded
- the next required action is a fresh baseline run in the new lab before any
  new candidate prompt is drafted

Why it matters:

- the live model tag and live prompt/runtime surface changed enough that the
  previous active lab should no longer steer current decisions by default
- the new structure makes repeated runs easier to audit and keeps future model
  changes easier to separate cleanly

### 2026-04-11 — Qwen Localization Review Narrowed `v003` Strategy

What changed:

- reviewed the most relevant prompting references for the current failure mode:
  - `z_reference_docs/Prompting/Qwen/Alibaba_Cloud_vision_docs_for_Qwen-VL.md`
  - `z_reference_docs/Prompting/Qwen/Qwen3-VL-8B-Instruct_Model_Card.md`
  - `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/2d_grounding.ipynb`
  - `z_reference_docs/Prompting/Qwen/Qwen_3_Chat_template_deep_dive_Prompting_Behavior.md`
  - selected structure and few-shot references from
    `z_reference_docs/Prompting/OpenAI_GPT/` and
    `z_reference_docs/Prompting/Anthropic_Claude/`
- compared those references against the observed `v001` and `v002` behavior in
  the active lab

What the review suggested:

- Qwen localization examples are generally short, direct, and explicit about
  coordinate format and JSON output
- Qwen3-VL grounding guidance aligns with the existing `[0, 999]` normalized
  bbox contract, so the coordinate format itself is not the active problem
- the current failure looks more like localization behavior drift than parser,
  schema, or bbox-conversion drift
- the `v001` and `v002` prompts likely over-emphasized long negative-rule
  language without creating a genuinely new grounding behavior
- a single, highly relevant textual example may be more useful than adding
  more prohibitions

Methodology update:

- for the current `qwen3-vl:8b-instruct` sequence, prefer compact
  Qwen-aligned grounding instructions over increasingly long negative-rule
  blocks
- when repeated candidates converge to the same failure pattern, treat that as
  evidence that the wording family is exhausted and switch tactics rather than
  iterating small paraphrases
- the next detection candidate should:
  - identify the visible solid target body first
  - anchor the target center on that visible structure
  - expand to the smallest box that still contains the visible target body
  - include one targeted example for the smoke-and-rails failure mode
- keep `assess_damage` and `summarize_scene` unchanged while detection remains
  the leading uncertainty

Current consequence:

- `v003` should be drafted as a detection-only experiment rooted in this new
  center-first, example-anchored strategy
- subtype drift remains a watch item, but it should not be tuned first if bbox
  placement is still off target

### 2026-04-11 — `v003` Tightened Coordinates But Still Missed The Target Body

What changed:

- ran `v003` against the same `tests/data/tank.jpg` seed image in:
  `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/experiments/runs/v003/run01_2026-04-11_000440_EDT/`
- baseline result remained:
  - bbox `[51, 37, 128, 73]`
  - confidence `PROBABLE`
- `v003` result was:
  - bbox `[51, 37, 102, 73]`
  - confidence `PROBABLE`
- `v003` removed the more specific `locomotive` wording from
  `brief_supporting_logic`
- the live config was restored after the candidate run and post-run diff
  verification stayed clean

Manual review result:

- the side-by-side review showed that `v003` was smaller, but not more
  correct
- the tightened box still sat left of the visible target body and mostly
  captured terrain / track-side context
- the baseline was too wide, but `v003` solved that by shrinking in the wrong
  place rather than by grounding on the actual object

Methodology update:

- treat numeric bbox tightening as insufficient evidence by itself
- for detection evaluation, the promotion gate is not "smaller" or "tighter"
  but "more correctly grounded on the visible target body"
- if a candidate improves coordinates while still missing the object, treat it
  as a non-winning draft rather than a near-promotion
- the next detection tactic should move the box down/right onto the dark solid
  mass nearest the fire source instead of only shrinking the current box center

Current consequence:

- `v003` is not a winner
- the most useful parts of `v003` were:
  - it kept confidence from inflating to `CONFIRMED`
  - it reduced subtype drift in the supporting logic
- the next version should keep detection as the only changed surface but switch
  to a more object-body-specific localization strategy

### 2026-04-11 — Upstream `main` Synced To `21deaf5` Without Requiring A Prompt Reset

What changed:

- synced local and fork `main` forward from `c077cd8` to `21deaf5` while
  preserving the local temporary debug-export work
- used a temporary save branch plus cherry-pick reapply because stash behavior
  was unreliable in this sync round
- reviewed the upstream range from `c077cd8` to `21deaf5`
- refreshed the active lab config snapshot and `v000` metadata to the new live
  baseline commit
- ran the full test suite after the sync and preserved local reapply:
  - result: `51 passed`

What the upstream delta actually changed:

- `src/bda_svc/pipeline/config.yaml`
  - no prompt-text or model-tag change
  - only the bbox-convention comment wording changed
- `src/bda_svc/pipeline/model.py`
  - bbox-scale prompt formatting now explicitly supports `_pixels`
  - invalid bbox-convention suffixes now raise fail-safe errors earlier
- `src/bda_svc/pipeline/utilities.py`
  - bbox conversion now explicitly supports `_pixels`
  - invalid bbox-convention suffixes now return `None` fail-safe
- tests expanded in:
  - `tests/unit/test_interfaces.py`
  - `tests/unit/test_model.py`
  - `tests/unit/test_utilities.py`

Environment finding:

- `pyproject.toml` and `uv.lock` did not change in this upstream pull
- no `uv sync` was needed
- the active live model tag remained `qwen3-vl:8b-instruct`
- the model was already installed locally, so no new Ollama download was needed

Methodology update:

- when upstream changes runtime hardening or tests without changing prompt
  text, model tag, doctrine wording, or dependencies, refresh the active lab
  baseline metadata instead of resetting the prompt sequence
- reserve prompt-lab archival/reset for changes that materially alter the
  experiment surface, such as new prompt text, new doctrine wording, a new
  active model tag, or dependency/runtime changes that alter execution behavior

Current consequence:

- the active `v000` through `v003` sequence remains current
- the lab baseline is now refreshed to `21deaf5`
- the next prompt step can continue from the current active lab without another
  reset
- local `main` intentionally remains one commit ahead of `origin/main` and
  `upstream/main` because we preserved the temporary debug-export helper layer
  for prompt review work
- that extra local commit is repo-side instrumentation in:
  - `src/bda_svc/app.py`
  - `src/bda_svc/cli.py`
  - `src/bda_svc/export.py`
  - `tests/unit/test_cli.py`
  - `tests/unit/test_export.py`
  - `tests/unit/test_main.py`
- the prompt lab stores the artifacts produced by that helper layer, not the
  implementation itself
- keep this helper layer in place until bbox/localization tuning is complete,
  then remove or relocate it once prompt-debug image export is no longer needed

### 2026-04-12 — Cycle 02 Moved The Best Assessment Prompt To `v009`

What changed:
- started cycle 02 from the confirmed `v006` detection win and moved the active
  prompt surface to `assess_damage`
- ran and documented:
  - `v007`
  - `v008`
  - `v009`
- completed the cycle summary in:
  `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/experiments/cycles/cycle02_v007-v009_summary.md`

Observed pattern:
- `v007` was a real partial improvement:
  - kept `PROBABLE`
  - removed K-kill and subtype drift
  - but overcorrected to `DAMAGED`
- `v008` confirmed that abstract category rules were not the right lever:
  - still `DAMAGED`
  - subtype drift returned
- `v009` was the first assessment prompt in the cycle to recover:
  - `DESTROYED`
  - `PROBABLE`
  - generic target-level wording without subtype drift

Methodology update:
- for this seed case, example-driven assessment phrasing outperformed abstract
  category-guidance blocks
- when category and confidence are entangled, prefer one short example showing
  the desired combination over additional doctrine prose
- once a cycle stabilizes the target-level assessment, stop iterating that
  surface and move the next cycle to the downstream summary surface

Current consequence:
- the best current detection direction remains `v006`
- the best current assessment direction is now `v009`
- the next cycle should freeze those and tune `summarize_scene`

### 2026-04-15 — Upstream `main` Moved To `28e863b` With Evaluation-Tooling Changes

What changed:
- reviewed the upstream range from `21deaf5` to `28e863b`
- confirmed the delta is concentrated in `bda_eval/`, with only one
  live-pipeline prompt change in `src/bda_svc/pipeline/config.yaml`
- confirmed local `main`, `origin/main`, and `upstream/main` are aligned at
  `28e863b`

What the upstream delta actually changed:
- `src/bda_svc/pipeline/config.yaml`
  - detect-objects prompt gained one new safeguard line:
    - do not produce an all-zero bbox unless `target_type` is
      `object_not_found`
- `bda_eval/cli.py`
  - new `--images` / `-i` input for image-folder-backed evaluation runs
- `bda_eval/config.py`
  - new shared config module for evaluation paths
- `bda_eval/bboxes.py`
  - new bbox-overlay export path using Pillow and a bundled font
- `bda_eval/main.py`
  - now copies reference and predicted report folders into the output folder
  - now generates bbox overlay images during evaluation
- `bda_eval/export.py`
  - evaluation CSV now includes `inference_time`
  - weight columns are no longer populated in the CSV output
- `bda_eval/models.py`
  - `inference_time` is now carried in evaluation metadata parsing
  - LLMaaJ logic scoring can now return `None` instead of forcing a fake zero
  - LLMaaJ reasoning is now logged to `logs_llmaaj/`
- `bda_eval/discovery.py`
  - added shared key-partition helper
- `bda_eval/tests/reports/BDA_DATA_SCHEMA.json`
  - removed from the tree
- `bda_eval/utilities/bboxes.py`
  - removed and effectively replaced by the new top-level `bda_eval/bboxes.py`

Environment finding:
- `pyproject.toml` and `uv.lock` did not change in this upstream pull
- no `uv sync` is required from this delta alone
- no new Ollama model download is implied by this delta

Methodology update:
- this upstream pull is not just runtime hardening; it changes the live
  evaluation surface and slightly changes live detection prompt text
- because live prompt text changed, the next prompt-baseline run in the new
  branch-aware lab should be refreshed from `28e863b`, not carried forward as
  if `21deaf5` were still the live prompt baseline
- because most of the delta landed in `bda_eval/`, future experiment review
  should distinguish prompt-pipeline changes from evaluation-tooling changes
  more explicitly

Current consequence:
- the clean-mirror/worktree structure is now the right default for future syncs
- the next active baseline in the numbered branch-aware lab should be rebuilt
  from `upstream/main` at `28e863b`
- the new evaluation path is more image-aware and more useful for bbox review,
  but it should not be confused with changes to the live inference pipeline

### 2026-04-15 — Fresh Branch-Aware `v000` Baseline Established From `28e863b`

What changed:
- created the first real active branch-aware qwen lab under:
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/`
- copied the current live `config.yaml` into the branch-aware baseline snapshot
- created a fresh branch-aware `v000_baseline.prompts.yaml`
- ran the first clean baseline from the feature worktree against
  `tests/data/tank.jpg`

Observed result:
- `target_0.target_type`: `military_equipment`
- `target_0.damage_category`: `DESTROYED`
- `target_0.confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 102, 73]`
- `metadata.inference_time`: `10.85`

Methodology update:
- the active baseline for this branch line is now the fresh `28e863b`-anchored
  branch-aware `v000`, not the older preserved `21deaf5` legacy baseline
- future grounding or prompt work in this branch line should compare against
  this new `v000` before borrowing lessons from the preserved legacy sequence
- when a clean branch line is started from mirrored upstream, do not assume the
  older local prompt-debug helper layer is present unless it is deliberately
  ported forward

Current consequence:
- the new branch-aware lab now has a real active baseline instead of just
  branch metadata
- the tighter `[51, 37, 102, 73]` bbox now becomes the correct baseline anchor
  for new work in this feature line

### 2026-04-15 — `bda_eval` Extended To Produce Prompt-Lab Review Artifacts

What changed:
- kept the upstream `bda_eval` bbox overlay path intact
- extended it additively so it can now also emit:
  - reference-only overlays
  - predicted-only overlays
  - reference-driven crops
  - predicted-driven crops
  - a side-by-side `bbox_review_sheet.jpg` for single-image comparison runs

Why it mattered:
- the clean branch-aware feature line no longer carries the older temporary
  `--debug-export-images` helper by default
- prompt-grounding work still needs the familiar side-by-side visual review
  artifact
- using `bda_eval` as the review-artifact engine keeps that workflow anchored
  to tracked upstream evaluation functionality instead of reviving a separate
  local-only export path

Methodology update:
- on the clean branch-aware line, the preferred bbox-review workflow is now:
  1. run `bda-svc` to create baseline/candidate JSON reports
  2. run `bda_eval` against those report folders plus the source image folder
  3. review the emitted overlays, crops, and `bbox_review_sheet.jpg`

Current consequence:
- clean branch-aware prompt work can keep doing visual grounding review without
  depending on the old temporary `bda-svc` debug helper

### 2026-04-15 — Clean-Line `bda_eval` Smoke Test Confirmed Real Prompt-Lab Layout

What changed:
- ran the first real branch-aware `bda_eval` smoke test at:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/layout_check/run02_2026-04-15_224230_EDT/`
- confirmed the run-root artifact layout now works end-to-end:
  - root `bbox_review_sheet.jpg`
  - `images_bbox_both/`
  - `images_bbox_reference/`
  - `images_bbox_predicted/`
  - `images_crop_reference/`
  - `images_crop_predicted/`
  - `images_bbox_review/`
  - copied report folders and evaluation CSV

Why it mattered:
- this was the first proof that the clean branch-aware line can reproduce the
  old prompt-lab visual review workflow without reviving the temporary
  `bda-svc` debug-export helper
- it also exposed and resolved two real integration blockers:
  - `bda_eval` should not hard-fail when `OLLAMA_API_KEY` is missing during an
    artifact-only review run
  - `bda_eval` should not fail when the predicted report folder already lives
    inside the run output root

Methodology update:
- on the clean branch-aware line, `bda_eval` review runs are now expected to
  degrade gracefully when LLMaaJ credentials are unavailable
- prompt-lab run roots may safely be used as the `bda_eval --output` location
  even when the predicted report folder already exists inside that run root

### 2026-04-15 — First Real Branch-Aware Candidate (`v001`)

What changed:
- drafted and ran the first real branch-aware candidate:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/versions/v001_detect_objects_short-contrastive-grounding.yaml`
- changed only `detect_objects`
- compared it against the fresh `28e863b` branch-aware baseline using the new
  `bda_eval` review path

Observed result:
- baseline: `[51, 37, 102, 73]`, `DESTROYED`, `PROBABLE`
- `v001`: `[46, 46, 123, 92]`, `DESTROYED`, `CONFIRMED`

Interpretation:
- the short contrastive detection style still appears to improve the bbox on
  the clean baseline
- but the same shift also reintroduced the older downstream regression pattern:
  - confidence inflation to `CONFIRMED`
  - unsupported subtype wording (`locomotive`)
  - unsupported scene-context wording (`railway track`)

Methodology update:
- on this clean branch-aware line, detection improvements should now be judged
  jointly against downstream regression reappearance, not in isolation
- a larger/better-looking box is not enough by itself if it predictably causes
  unsupported identity or confidence overreach

### 2026-04-15 — Branch-Aware `v002` Held The Better Box But Overcorrected Damage

What changed:
- drafted and ran the first assessment-only follow-up on the clean branch-aware
  line:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/versions/v002_assess_damage_example-anchored-generic-target.yaml`
- kept `v001` detection behavior intact
- changed only `assess_damage`

Observed result:
- `v001` parent behavior: `[46, 46, 123, 92]`, `DESTROYED`, `CONFIRMED`
- `v002`: `[46, 46, 123, 92]`, `DAMAGED`, `PROBABLE`

Interpretation:
- this is an important branch-aware result because it shows the stronger
  `v001` bbox is not inherently tied to `CONFIRMED`
- the safer assessment framing can preserve the improved box
- but the current wording is too conservative and pushes the target back to
  `DAMAGED`

Methodology update:
- when a detection gain is promising, the next assessment iteration should be
  evaluated first for whether it preserves the improved bbox and only then for
  damage/confidence calibration
- if `PROBABLE` is recovered at the cost of collapsing `DESTROYED` to
  `DAMAGED`, treat the version as partial reuse only

### 2026-04-15 — Branch-Aware `v003` Became The Working Leader

What changed:
- drafted and ran:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/versions/v003_assess_damage_destroyed-probable-recovery.yaml`
- kept the stronger `v001` detection prompt
- strengthened the `v002` assessment prompt with an explicit anti-downgrade
  rule and stronger `DESTROYED` + `PROBABLE` example

Observed result:
- baseline: `[51, 37, 102, 73]`, `DESTROYED`, `PROBABLE`
- `v003`: `[46, 46, 123, 92]`, `DESTROYED`, `PROBABLE`

Interpretation:
- this is the first branch-aware version that combines the stronger detection
  behavior with the desired target-level assessment behavior
- target-level subtype drift also stayed out
- the remaining overreach is now concentrated in `summarize_scene`, not in
  `detect_objects` or `assess_damage`

Methodology update:
- after a branch-aware version preserves the improved bbox and restores the
  desired target-level assessment behavior, freeze those two prompt surfaces
  and move the next cycle to `summarize_scene`

### 2026-04-15 — Branch-Aware `v003` Repeated Cleanly

What changed:
- reran `v003` with no prompt changes as `run02`
- compared `run02` directly against `run01`

Observed result:
- `v003` run02 matched run01 exactly once normal metadata fields were ignored:
  - `image_id`
  - `date_created`
  - `inference_time`

Interpretation:
- the branch-aware working leader is no longer just a one-off positive run
- detection and target-level assessment are now stable enough on this seed case
  to treat as the frozen base for the next prompt cycle

Methodology update:
- when a branch-aware working leader repeats cleanly, stop spending more cycles
  on the already-confirmed prompt surfaces and move the next cycle to the
  remaining unresolved surface

### 2026-04-15 — Branch-Aware `v004` Improved The Remaining Summary Problem

What changed:
- drafted and ran:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/versions/v004_summarize_scene_conservative-generic-terrain.yaml`
- froze:
  - `detect_objects` from `v001`
  - `assess_damage` from `v003`
- changed only `summarize_scene`

Observed result:
- bbox still: `[46, 46, 123, 92]`
- target-level assessment still: `DESTROYED`, `PROBABLE`
- summary improved from:
  - `military vehicle on a dirt track`
  - `complete loss of the vehicle's operational capability due to destruction`
- to:
  - `burning target in open terrain with dense black smoke`
  - `severe degradation or loss of capability for the assessed target`

Interpretation:
- the remaining prompt problem was in fact concentrated in `summarize_scene`
- the summary-only cycle can improve the report without destabilizing the
  confirmed detection and assessment behavior

Methodology update:
- once detection and target-level assessment are confirmed, summary-only cycles
  are the right next step
- if a summary-only version preserves the confirmed target outputs and produces
  a materially more conservative summary, treat it as the provisional full-stack
  leader and run one confirmation repeat next

### 2026-04-16 — Branch-Aware `v004` Repeated Cleanly

What changed:
- reran `v004` unchanged as `run02`
- compared `run02` directly against `run01`

Observed result:
- `v004` run02 matched run01 exactly once normal metadata fields were ignored:
  - `image_id`
  - `date_created`
  - `inference_time`
- the improved summary text repeated exactly as well

Interpretation:
- `v004` is no longer only a promising summary improvement
- it is now the confirmed branch-aware full-stack working leader on the seed
  case

Methodology update:
- after a summary-only candidate repeats cleanly while preserving the frozen
  detection and assessment behavior, treat the whole prompt stack as confirmed
  for that branch line on the current seed case

### 2026-04-16 — Mixed-Pack Validation Reframed Grounding As A Generalization Problem

What changed:
- ran the first branch-aware mixed grounding sweep against the fresh `v000`
  baseline instead of trusting the tank seed case alone
- used the explicit mixed pack that includes:
  - the tank pressure case
  - another destroyed tank
  - an operational tank
  - destroyed and operational building controls
  - a negative office scene

Observed result:
- `v004` remained the best seed-case full-stack candidate
- but `v004` was not yet a clean cross-image grounding winner
- `destroyed_building4` exposed a real two-building miss
- `operational_tank4` exposed an assessment-layer false-damage problem
- the office negative case also confirmed that raw `bda-svc` JSON may be a
  more reliable review artifact than `bda_eval` CSV when `NOT APPLICABLE`
  damage labels are involved

Interpretation:
- this was the point where the active question changed from
  "can we improve the tank box?" to
  "can we improve the grounding rule without hurting other image types?"

Methodology update:
- treat the seed tank case as a repeatability pressure test, not the only proof
- require mixed-pack validation before promoting any new grounding rule
- when a current leader is already known to be wrong on a mixed-pack case,
  compare follow-ups against clarified per-case ground truth rather than
  blindly inheriting the earlier mistake

### 2026-04-16 — Detect-Only Recovery Produced Confirmed `v006`

What changed:
- ran `v005` and `v006` as detect-only follow-ups after the first mixed sweep
- `v005` recovered the second building on `destroyed_building4` but hallucinated
  a full-frame building in the office negative scene
- `v006` kept the valid multi-target separation lesson and added the indoor /
  non-target guard that restored the negative scene
- reran `v006` unchanged as `run02`

Observed result:
- `v006` preserved the correct two-building read on `destroyed_building4`
- `v006` restored `office.jpg` to `object_not_found`
- `v006` held the tank pressure case steady
- `v006` did not worsen the operational-tank problem
- `v006` repeated cleanly across the full mixed pack after ignoring routine
  metadata fields

Interpretation:
- the correct reusable lesson from `v005` was target separation, not the whole
  broadened detection wording
- `v006` became the first detect-only rule in this clean branch-aware line that
  both generalized and repeated

Methodology update:
- when a detect-only candidate fixes a real cross-image miss, pressure it with
  a negative-scene control before calling it safe
- if a detect-only candidate repeats cleanly across the mixed pack, freeze it
  and move the next cycle to the downstream prompt surface instead of tweaking
  detection again

### 2026-04-16 — Assess-Only Recovery Produced Confirmed `v008`

What changed:
- froze `detect_objects` at the confirmed `v006` rule
- ran `v007` and `v008` as assessment-only follow-ups with summary frozen to
  the confirmed `v004` wording
- `v007` fixed the operational firing false-damage issue but reintroduced
  `K-kill` wording on a destroyed-tank control
- `v008` preserved the firing-signature fix and removed that destroyed-case
  wording regression
- reran `v008` unchanged as `run02`

Observed result:
- `operational_tank4` stayed `NO DAMAGE` / `CONFIRMED` with the same bbox
- `destroyed_tank15` lost the `K-kill` wording regression
- destroyed-building, operational-building, tank-pressure, and office controls
  stayed stable at the category/confidence level
- `v008` repeated cleanly across the full mixed pack after ignoring routine
  metadata fields

Interpretation:
- the operational-tank problem was assessment behavior, not detection
- once the right firing-signature guard was found, the remaining work was
  wording discipline on destroyed cases, not more bbox tuning

Methodology update:
- once the detect surface is frozen, assess-only cycles should be judged on
  whether they preserve bbox behavior while improving calibration and logic
- if a follow-up fixes a real downstream regression but reintroduces doctrinal
  overreach in supporting logic, keep the valid behavior and tighten the logic
  wording in the next assess-only version

### 2026-04-16 — The Frozen Stack Was Packaged And Validated As `v009`

What changed:
- froze the best confirmed surfaces as:
  - `detect_objects` from `v006`
  - `assess_damage` from `v008`
  - `summarize_scene` from `v004`
- reran that frozen stack in the broader branch-aware sweep
- packaged the combined surfaces into
  `v009_unified_best-stack.yaml`
- ran `v009` directly on a focused comparison pack

Observed result:
- the broad frozen-stack sweep became the strongest cross-image candidate in
  the branch-aware line so far
- the direct `v009` run matched the expected inherited behavior on:
  - `tank_pressure`
  - `operational_tank4`
  - `destroyed_building4`

Interpretation:
- `v009` behaved as a faithful unified packaging of already-proven surfaces,
  not as a new fork with hidden drift

Methodology update:
- once individual prompt surfaces have confirmed leaders, package them into one
  explicit unified version file
- do not rely on mental cross-references between earlier versions when a stack
  is ready for serious comparison or promotion work
- run the packaged winner directly at least once so the unified version has its
  own execution record

### 2026-04-16 — Additional Challenge Runs And The Blind Sweep Strengthened The Claim

What changed:
- ran an extra three-image baseline-vs-`v009` challenge comparison using
  additional cases from `z_reference_docs/Data_set_Storage/`
- ran a broader 10-image blind-style baseline-vs-`v009` sweep
- reviewed the two caution cases in depth afterward

Observed result:
- the extra challenge run showed:
  - preserved three-building recall on a new multi-object scene
  - no smoke/fire truck regression
  - preserved complex-scene building separation with a modest secondary-box
    improvement
- the blind sweep showed:
  - `10 / 10` preserved target-count recall
  - `6 / 10` preserved the same damage/confidence structure
  - only `2 / 10` changed damage category at all
- the remaining caution cases were:
  - `destroyed_building5`
  - `destroyed_tank37`

Interpretation:
- the strongest honest claim is now cross-image stability and cleaner behavior,
  not dramatic improvement on every single unseen image
- the two remaining watch cases are calibration issues, not recall failures

Methodology update:
- when presenting a prompt winner to other people, emphasize:
  - recall preservation
  - negative-scene discipline
  - multi-target separation
  - cross-image stability
- keep caution cases visible instead of hiding them, especially when the
  remaining disagreement is calibration rather than outright detection failure

### 2026-04-16 — `v009` Was Promoted Into Tracked Branch State

What changed:
- committed the tracked `bda_eval` review-artifact workflow as:
  - `566892a` — `Add prompt-lab review artifacts to bda_eval`
- promoted the unified `v009` prompt stack into tracked pipeline config as:
  - `127051a` — `Promote v009 prompt stack into pipeline config`
- validated the branch state with:
  - `uv run pytest tests/unit/test_yamls.py bda_eval/tests`

Observed result:
- the review-sheet workflow is no longer only a local working-tree convenience
- the branch candidate is no longer only a prompt-lab winner note
- the tracked feature-branch config now carries the promoted `v009` stack

Interpretation:
- this is the point where the work became a real branch candidate rather than
  only a local experiment

Methodology update:
- once a prompt stack clearly earns promotion, preserve it in tracked branch
  history instead of leaving it only in local docs
- keep the local prompt-lab as the evidence chain, but use tracked branch state
  as the reviewable promotion target

### 2026-04-16 — CI Fix Clarified The Difference Between Branch Health And Prompt Evidence

What changed:
- pushed the feature branch to
  `origin/feat/qwen3-vl-8b-instruct/two-pass-refinement`
- opened PR `#134` against `upstream/main`
- GitHub Actions initially failed because the CI workflow installed only the
  root package set and did not include workspace-member dependencies needed for
  `bda_eval`
- fixed that with:
  - `ebeae30` — `Install workspace packages in CI`
- reran the PR checks successfully

Observed result:
- the PR is now open with green checks
- the branch is reviewable from an engineering-health perspective
- the CI `build-and-run` job still serves as a runtime-health check, not as a
  full prompt-behavior regression test for the exact `v009` winner outputs

Interpretation:
- there are now two different validation lanes:
  - branch health in GitHub CI
  - exact prompt-behavior evidence in the local prompt-lab artifacts

Methodology update:
- do not overclaim what green CI means for prompt work
- GitHub CI proves the branch is healthy and runnable
- exact prompt-behavior claims should still point back to the local evidence
  chain under `z_reference_docs/Prompt_Labs/...`

### 2026-04-17 — Upstream `main` Moved To `c19940a` And The Active Worktrees Were Refreshed

What changed:
- reviewed the upstream move from `28e863b` to `c19940a`
- confirmed the delta is limited to:
  - `.github/workflows/ci.yml`
  - `docker/Dockerfile`
- confirmed the practical effect of that delta is CI/container security
  hardening, not prompt/runtime/doctrine behavior change
- refreshed the active branch structure in the documented order:
  1. `main`
  2. `model/qwen3-vl-8b-instruct`
  3. `feat/qwen3-vl-8b-instruct/two-pass-refinement`
  4. `model/gemma4-e4b`
  5. `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`

Observed result:
- `main`, `origin/main`, and `upstream/main` are now aligned at `c19940a`
- the Qwen and Gemma model/feature worktrees all rebased cleanly
- the Gemma feature branch reported skipped already-applied commits during the
  rebase, which is normal when equivalent commits already exist upstream in the
  rebase chain
- the local Qwen feature branch now diverges from its `origin` tracking branch
  because the rebase rewrote local history

Methodology update:
- when an upstream sync changes only CI, Docker, or other infrastructure
  surfaces, propagate the ancestry change through the model/feature worktrees
  but do **not** rebuild the active prompt baseline automatically
- only refresh a branch-aware `v000` baseline when the upstream delta changes
  live prompt text, doctrine wording, pipeline behavior, model tags, or other
  runtime semantics that affect inference meaning
- after any feature-branch rebase, treat remote branch updates as a separate,
  deliberate decision; do not blur “refreshed locally” with “safe to push
  remotely” when `--force-with-lease` may be required

Current consequence:
- the active Qwen line keeps its `28e863b` prompt-evidence anchor while now
  sitting on top of the newer `c19940a` infra base
- the active Gemma bootstrap line keeps its first live `v000` evidence anchor
  while also inheriting the newer `c19940a` infra base
- the documented worktree refresh workflow is now validated on both the Qwen
  and Gemma model lines

### 2026-04-17 — Model Branches Were Hardened Until They Matched The Practical Prompt-Lab Smoke Flow

What changed:
- promoted the Qwen model branch from a clean ancestry root to a smoke-testable
  root by adding:
  - `b947a3e` — `Add prompt-lab review artifacts to bda_eval`
  - `0f916de` — `Install workspace packages in CI`
- promoted the Gemma model branch from a generic inherited root to a
  smoke-testable Gemma root by adding:
  - `54a9d58` — `Bootstrap Gemma 4 E4B baseline config`
- reran both:
  - `uv run pytest tests/unit/test_yamls.py bda_eval/tests`
  - prompt-lab style `bda-svc` + `bda_eval` smoke runs

Observed result:
- all four active worktrees can now complete the same practical smoke recipe
- the Qwen model branch now skips logic scoring gracefully when
  `OLLAMA_API_KEY` is absent, matching the feature-branch evaluation behavior
- the Gemma model branch now points at `gemma4:e4b` in tracked config, so it
  can run against the local Gemma host without failing immediately on a Qwen
  model lookup

Methodology update:
- if a long-lived model branch is intended to be reused as the parent for
  future feature branches, it is worth hardening it until it can complete the
  same minimal prompt-lab smoke flow as the active feature branches
- that minimal smoke flow is now:
  1. `bda-svc` export on a known seed image
  2. `bda_eval` self-check with saved artifacts
  3. successful artifact writeout into `z_reference_docs/Prompt_Labs/...`
- a branch root that cannot do that is still usable as ancestry, but it is not
  yet a fully practical prompt-lab starting point

Current consequence:
- the Qwen and Gemma model branches are now both reusable ancestry roots and
  usable prompt-lab smoke-test roots
- future feature branches can be opened from those model branches with fewer
  branch-shape surprises

### 2026-04-17 — The Refresh Workflow Needed A Stronger Documentation Contract

What changed:
- reviewed the actual `c19940a` refresh experience against the documented
  workflow
- confirmed the documented refresh order worked as intended
- also confirmed that a clean rebase alone did not guarantee that all active
  worktrees were equally usable for prompt-lab work

Observed result:
- the workflow was already strong on:
  - ancestry safety
  - baseline-refresh gating
  - remote-push caution
- the missing clarity was in what “done” meant after the rebase
- extra troubleshooting was needed because the docs did not yet distinguish
  clearly between:
  - refresh success
  - validation success
  - full prompt-lab parity

Methodology update:
- a safe rebase workflow and a full functional parity workflow are related but
  not identical
- model branches that are meant to spawn future feature branches should be kept
  smoke-capable, not just rebased
- refresh decisions and baseline-refresh decisions are different decisions:
  - rebase question:
    - did the branch ancestry update safely?
  - baseline-refresh question:
    - did prompt/runtime meaning change enough to require a new `v000`?
  - parity question:
    - can every active worktree still complete the practical prompt-lab smoke
      loop?

Current consequence:
- the workflow docs should now define full parity as the completion standard,
  not only a clean rebase
- branch checklists should include workspace sync, smoke validation, and remote
  push timing rules rather than stopping at rebase commands

### 2026-04-17 — Branch Hygiene Should Finish By Rebinding Feature Branches To Hardened Model Roots

What changed:
- after hardening the Qwen and Gemma model branches, rebased the active feature
  branches onto those hardened model roots
- reran the shared sanity suite on both feature branches
- reran the practical prompt-lab smoke flow on both feature branches and saved
  the results under each lab’s `experiments/runs/branch_hygiene/` area

Observed result:
- both active feature branches still passed:
  - `uv run pytest tests/unit/test_yamls.py bda_eval/tests`
  - `bda-svc` export on `tests/data/tank.jpg`
  - `bda_eval` self-check against the fresh report folder
- the Qwen feature rebase skipped already-applied commits because the reusable
  infra work had already been promoted into the model branch
- the Gemma feature branch now matches the hardened Gemma model branch in
  tracked code, which is acceptable because the bootstrap baseline commit has
  already been lifted into the reusable model root

Methodology update:
- once model branches are hardened for parity, branch hygiene is not done until
  the active feature branches are rebound onto those hardened roots and the
  same smoke recipe is rerun there
- this extra step is what turns “all branches are individually capable” into a
  clean reusable branch tree
- a feature branch ending up identical to its model parent is not automatically
  a problem; it can be the correct outcome when the feature’s reusable changes
  have already been promoted upward

Current consequence:
- the active Qwen and Gemma feature branches now have both:
  - current ancestry
  - confirmed practical prompt-lab readiness
- the remaining remote-push question for the Qwen feature branch is still a
  separate collaboration decision because the local rebase rewrote history

### 2026-04-20 — Doctrine Replacement Should Be Tested As A Shadow A/B, Not A Live Rewrite

What changed:
- audited the current live `src/bda_svc/pipeline/doctrine.yaml` against the
  searchable BDA corpus under `z_reference_docs/BDAs/`
- created a local-only doctrine replacement package under:
  `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/`
- created two doctrine experiment branches from the active feature lines:
  - Qwen `1.3`
  - Gemma `3.2`
- drafted the first prompt-compatible Phase-1 doctrine candidate and applied it
  only in those doctrine branches
- ran runtime contract checks in both doctrine branches and confirmed they
  still pass

Observed result:
- the current live doctrine already preserves much of the core Phase-1 PDA
  content for buildings and military equipment
- the larger problem is translation, not absence:
  - some all-source implications leak into a visual-only workflow
  - PDA semantics and prompt-operational guidance are mixed together
  - building PDA text is not always optimized for the selected-target
    crop-plus-scene runtime
- the first replacement candidate can keep the runtime schema intact while
  still:
  - tightening Phase-1-only scope
  - removing non-visual cues from prompt-facing doctrine text
  - making the building PDA notes more explicit for the current runtime

Methodology update:
- doctrine experiments should begin as controlled shadow replacements, not as
  edits to the live file on `main`
- the first doctrine iteration should keep the runtime interface unchanged and
  store extra doctrinal traceability in companion notes instead of the runtime
  YAML itself
- the first editable surface should be PDA definitions and considerations
  before broad detection-guidance rewrites
- doctrine candidates should be judged on two tracks at once:
  - doctrinal fit to the corpus
  - prompt/eval fit on the held control cases

Current consequence:
- the active Qwen `1.2` and active Gemma `3.1` branches remain the doctrine
  controls
- the new Qwen `1.3` and Gemma `3.2` branches are now the only places where
  doctrine replacement work should happen until a winner is clear

### 2026-04-20 — Same-Input Parent Controls Matter In Doctrine A/B Work

What changed:
- ran the held Qwen parent branch on the exact same six-case doctrine guard-set
  input pack as the `1.3` doctrine candidate
- built bbox review artifacts for `destroyed_building4`
- manually reviewed the source image and the building PDA text against the two
  Qwen outputs

Observed result:
- the held Qwen control and the doctrine candidate both returned two
  `DESTROYED / PROBABLE` buildings on `destroyed_building4`
- the doctrine candidate only shifted the split line to the right:
  - control: `[0, 18, 63, 150]` and `[63, 18, 244, 150]`
  - candidate: `[29, 18, 69, 153]` and `[69, 18, 250, 153]`
- the bbox review sheet showed that both runs still carve out the upright
  left-side neighboring structure as its own destroyed building target
- that means the doctrine candidate did not materially improve bbox quality or
  doctrinal fit on this scene

Methodology update:
- do not treat an apparent severity change in a doctrine candidate as evidence
  of improvement until the same-input parent control has been run
- if the parent control already makes the same semantic read, the doctrine
  change is operationally neutral for that case even if the wording is cleaner
- when the model keeps selecting the wrong target body, the next lever is
  target delimitation/localization guidance, not another PDA-only rewrite

Current consequence:
- the first Qwen doctrine candidate is not a convincing building-severity win
- the key unresolved Qwen problem on `destroyed_building4` remains scene
  partitioning rather than PDA thresholds alone

### 2026-04-20 — Tightening Building `detection_guidance` Alone Was Not Enough

What changed:
- created `runtime_candidate_doctrine.v002.yaml` as a Qwen-only follow-up
  doctrine candidate
- changed only `buildings.detection_guidance`
- reran the Qwen doctrine guard set against the held parent control with an
  expanded building shot group:
  - `destroyed_building3`
  - `destroyed_building4`
  - `destroyed_building5`
  - `destroyed_building6`
  - `destroyed_building8`
  - `operational_building2`
  - `operational_building7`
  - `operational_building91`
  - plus the existing tank and negative controls

Observed result:
- most added cases were operationally neutral
- `destroyed_building5`, `destroyed_building8`, `operational_building2`,
  `operational_tank4`, and `office_negative` effectively held
- `destroyed_building3` still boxed a background building as a second target
- `destroyed_building6` remained a broad scene-partitioning read with only
  small bbox shifts
- `destroyed_building4` got worse relative to the held control:
  - held control: left target `SEVERE DAMAGE`, right target `DESTROYED`
  - `v002` candidate: both targets `DESTROYED`

Methodology update:
- doctrine-only wording that tells the model how to choose the selected
  building body is weaker than it looks when the underlying detection habit is
  already stable
- if a targeted doctrine wording change stays neutral across most scenes but
  still preserves the same background-building selection failure, that is a
  sign the next lever may belong in prompt surfaces or runtime framing rather
  than doctrine text alone
- expanding the shot group before iterating again was useful here because it
  showed that a seemingly sensible adjacency rule did not generalize into a
  clear win

Current consequence:
- the Qwen `v002` building-detection-guidance-only doctrine revision is not a
  winning direction
- Gemma should remain untouched until we decide whether the next move should be
  a deeper doctrine rewrite or a non-doctrine detection intervention

### 2026-04-20 — Prompt Assembly Can Make Doctrine A Weaker Lever Than It Looks

What changed:
- traced the exact Qwen `1.3` detection prompt assembly from doctrine source to
  final Ollama request
- rendered the full assembled detection prompt and measured the relative size
  of:
  - the shared `system` prompt
  - the full detection `user` prompt
  - the injected doctrine block

Observed result:
- detection doctrine is formatted by `format_detection_doctrine()` as raw
  per-category prose and inserted into the detection prompt under
  `TARGET-TYPE SPECIFIC DETECTION GUIDANCE`
- the detection request to Ollama is a simple two-message structure:
  - one short `system` message
  - one large `user` message with the image attached
- doctrine is not elevated into the system layer and is followed by a longer
  generic boxing section plus contrastive examples

Methodology lesson:
- a doctrine file can be present in the runtime and still be a weaker practical
  lever than the main prompt surface that surrounds it
- when a doctrine rewrite only produces small behavioral drift, inspect where
  the doctrine text sits in the assembled prompt before assuming the doctrine
  content itself is the problem
- if the model keeps the same localization habit across doctrine changes, the
  next step may belong in prompt hierarchy and instruction weighting rather than
  in doctrinal wording alone

Current consequence:
- this strengthens the case that the unresolved Qwen adjacent-building failure
  is primarily a detection-prompt weighting and scene-partition issue
- future interventions should be careful about whether they are testing
  doctrine semantics or prompt authority

### 2026-04-20 — Compare Rendered Prompt Surfaces Before Designing The Next Detect Cycle

What changed:
- assembled a dedicated detect-surface inspection across:
  - active `1.2`
  - doctrine-side `1.3`
  - historical detect winner `v006`
- compared:
  - current `1.2` template vs current `1.3` template
  - rendered `1.2` vs rendered `1.3`
  - current active detect surface vs historical `v006`
- explicitly classified the detection instructions by authority level:
  - shared system prompt
  - top-level detection task/rules
  - doctrine-injected guidance
  - generic boxing rules
  - contrastive examples
  - output/schema rules

Observed result:
- current `1.2` and `1.3` `detect_objects` templates are the same
- the meaningful branch-to-branch rendered difference is only the injected
  doctrine block
- the active detect surface is still very close to historical `v006`
- the current live difference from `v006` is mostly the inherited no-target
  contract change rather than a wholesale grounding rewrite

Methodology lesson:
- before starting a new prompt cycle, compare the current rendered prompt
  surface against the last confirmed winner
- if the current surface is still near the confirmed winner, the next cycle
  should aim at salience and hierarchy, not a large prompt rewrite
- official online checks are most useful when they surface one concrete live
  hypothesis; once they do, return to local A/B evidence instead of widening
  the web-search scope prematurely

Current consequence:
- the next Qwen detect cycle should explicitly test:
  - user-prompt weighting first
  - system-role placement as a secondary hypothesis lane
- there is no need for broad additional online research before that next
  detect-only Qwen cycle

### 2026-04-20 — A Small User-Prompt Weighting Change Can Beat A Larger Doctrine Rewrite

What changed:
- ran the first mirrored Qwen detect-only follow-up after the prompt-surface
  inspection
- branches used:
  - active `1.2`
  - doctrine-side `1.3`
- changed only `detect_objects` in both branches:
  - one stronger top-level adjacent-building target-body rule
  - one tighter supporting building boxing sentence
- left doctrine, assessment, summary, and runtime interfaces unchanged

Observed result:
- both branches recovered `destroyed_building4` in the same useful direction:
  - parent control split the scene into two buildings
  - candidate collapsed the read to one scene-central destroyed building
- the candidate did **not** solve the full family:
  - `destroyed_building3` still boxed the background building
  - `destroyed_building6` stayed a broad scene-partitioning read
- core guardrails held:
  - `office_negative`
  - `operational_tank4`
  - `tank_pressure`

Methodology lesson:
- if doctrine-only rewrites stay neutral but a small salience change in the
  actual prompt surface moves the critical failure cleanly, prioritize the
  prompt surface
- cross-branch mirrored runs are especially useful when one branch carries a
  doctrine difference; they tell us whether the candidate depends on one narrow
  branch context or reflects a more general instruction-weighting effect
- a partial win is still valuable when it improves the key failure surface
  without reopening known controls

Current consequence:
- the working Qwen read is now:
  - doctrine was not the strongest lever
  - detect-surface weighting is the right lane
  - `destroyed_building4` now has a viable recovery direction to preserve
- `v009` remains the last confirmed staged winner
- the local tracked `1.2` config is now an exploratory `v010` detect-only
  candidate rather than the frozen `v009` winner

### 2026-04-20 — Not Every Follow-Up On A Partial Win Is Worth Keeping Live

What changed:
- tested one more detect-only follow-up after `v010`
- the new idea tried to elevate scene-central versus background-building
  selection more explicitly without changing any non-detection prompt surface

Observed result:
- `v011` kept the useful `destroyed_building4` one-box recovery
- but it did not actually fix the targeted remaining failures:
  - `destroyed_building3`
  - `destroyed_building6`
- it also introduced more incidental bbox drift than the targeted gain
  justified

Methodology lesson:
- once a candidate becomes the best current local state, the next follow-up
  must be judged against that candidate, not just against older failures
- preserving one recovered case is not enough if the new wording does not move
  the still-open cases
- when a follow-up fails to beat the current best local state, restore the
  stronger candidate into the live worktree and treat the failed follow-up as
  documented evidence, not as the new default

Current consequence:
- `v011` is recorded and rejected
- `v010` remains the live local Qwen detect state to build from

### 2026-04-20 — Example Structure Alone Also Was Not Strong Enough To Resolve The Remaining Qwen Building Failures

What changed:
- tested one more detect-only follow-up after `v011`, but instead of adding
  more rules, rewrote the building guidance into:
  - one dedicated target-selection example block
  - one shorter general contrastive block
- kept the `v010` target-body rule set intact
- mirrored the same candidate into both:
  - active `1.2`
  - doctrine-side `1.3`

Observed result:
- `destroyed_building4` remained recovered in both branches
- `destroyed_building3` still boxed the background building in both branches
- `destroyed_building6` still returned three buildings in both branches
- some bbox tightening occurred, especially in `1.3`, but the core bad
  detections stayed alive

Methodology lesson:
- example-heavy structure is not automatically stronger than prose-heavy rules;
  it depends on whether the examples actually change the model’s target
  prioritization behavior instead of merely tightening box placement
- once the main failure mode is about *which* targets exist rather than the
  precise box edge, we should judge candidates primarily on target-count and
  target-selection recovery, not on modest bbox neatness
- a candidate can be informative and still not be worth keeping live

Current consequence:
- `v012` is recorded and rejected
- `v010` remains the strongest current local Qwen detect state
- the next worthwhile Qwen detect move likely needs either a stronger
  instruction hierarchy shift or a more surgical example pattern tied directly
  to the unresolved `destroyed_building3` and `destroyed_building6` behaviors

### 2026-04-20 — A Stronger Hierarchy Shift Produced The First Useful Asymmetric Signal

What changed:
- tested one more detect-only follow-up after `v012`
- kept the `v010` target-body rule set intact
- added a top-of-prompt `BUILDING TARGET PRIORITY` decision order so the model
  must count building targets before boxing them
- mirrored the same candidate into both:
  - active `1.2`
  - doctrine-side `1.3`

Observed result:
- `destroyed_building4` remained recovered in both branches
- `destroyed_building6` remained unresolved in both branches
- active `1.2` still boxed the `destroyed_building3` background building
- doctrine-side `1.3` removed the `destroyed_building3` background-building
  false positive entirely

Methodology lesson:
- stronger hierarchy can matter more than example-only reshaping
- when the same candidate helps in a verification lane but not in the active
  lane, treat that as an interaction clue rather than a promotion candidate
- doctrine-side asymmetry can reveal that the surrounding injected guidance is
  amplifying or stabilizing the intended prompt behavior

Current consequence:
- `v013` is recorded and rejected for the active Qwen line
- `v010` remains the strongest current local Qwen detect state
- the next worthwhile move should probably borrow the *shape* of this stronger
  hierarchy while making the active-line building-selection wording even more
  tightly coupled to the specific `destroyed_building3` background-building
  failure
