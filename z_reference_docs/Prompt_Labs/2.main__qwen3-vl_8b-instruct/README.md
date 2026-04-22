# Qwen3-VL 8B Instruct Prompt Lab

This lab is the active working area for prompt refinement of
`qwen3-vl:8b-instruct`.

Source context:

- branch/workspace: `main`
- live runtime baseline commit: `21deaf5`
- status: active as of `2026-04-11`
- latest upstream delta: bbox/runtime hardening plus test expansion; no prompt-text or model-tag change

Legacy note:

- as of the git/worktree reset on `2026-04-15`, this lab is preserved as the
  pre-reset local working lab
- its closest git-line mapping is now
  `snapshot/2026-04-15-pre-main-reset`
- new branch-aware qwen work should be rooted under
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/`

## Goal

Improve the prompt surfaces used by the current `bda-svc` pipeline without
changing the live runtime contract:

- same placeholders
- same JSON fields
- same configured bbox contract
- same doctrine categories
- same Ollama message structure

## Prompt Surface Order

1. `system`
2. `assess_damage`
3. `detect_objects`
4. `summarize_scene`

## Folder Map

- `baseline/`
  Current prompt/config snapshot copied from the live pipeline.
- `dossier/`
  Qwen-specific prompting rules and doctrine/schema mapping.
- `evals/`
  Fresh track manifests for the current `main` runtime contract.
- `experiments/`
  Version log, failure taxonomy, version snapshots, accepted winners, and run
  artifacts.

## Experiment Output Rule

New experiment outputs belong under a version-first structure:

- `experiments/runs/baseline/run01_YYYY-MM-DD_HHMMSS_TZ/`
- `experiments/runs/v001/run01_YYYY-MM-DD_HHMMSS_TZ/`

Each run folder should include a `RUN_MANIFEST.md` and one subfolder per
compared condition when baseline and candidate outputs are run together.

## Critique / Research / Revise Rule

The active sequence now uses an iterative loop after every candidate run:

1. run the experiment
2. write `RUN_MANIFEST.md`
3. write `CRITIQUE.md` in the run folder
4. do online research for the gaps exposed by that critique
5. save the paired research note under:
   `z_reference_docs/Prompting/Research_Loops/`
6. draft the next slight prompt revision from those findings
7. if grounding still stalls after several prompt revisions, sanity-check
   backend/runtime variance before blaming the prompt YAML structure alone

This keeps each loop auditable instead of relying on memory between versions.

## Temporary Debug Artifacts

The local prompt workflow currently relies on a temporary debug-export helper on
local `main`.

When a run is executed with `--debug-export-images`, it can now export:

- per-target overlay images
- per-target crop images
- `pipeline_debug.json`

`pipeline_debug.json` is used to preserve raw pipeline debug information during
prompt work, especially for grounding failures. Its current purpose is to show:

- the active bbox convention used during detection
- whether code-level refinement was enabled for the run
- the original and model-image sizes
- the raw detection response from the model
- the repaired/parsed detection payload when available
- which detections were kept or rejected and why
- any refinement ROI, translated candidates, and refined-box selection decisions

Working rule:

- use `pipeline_debug.json` to diagnose grounding failures before drafting the
  next prompt revision
- do not treat it as part of the user-facing runtime output contract
- remove or retire this helper once prompt tuning is finalized

## Source Priority

Use sources in this order:

1. `src/bda_svc/pipeline/config.yaml`
2. `src/bda_svc/pipeline/doctrine.yaml`
3. `z_reference_docs/Prompting/Qwen/`
4. `z_reference_docs/BDAs/`
5. `z_reference_docs/Prompting/OpenAI_GPT/`
6. `z_reference_docs/Prompting/Anthropic_Claude/`
7. `z_reference_docs/Prompting/Google_Gemini/`

## Promotion Rule

No prompt text should be copied into `src/bda_svc/pipeline/config.yaml` until it
passes the local eval tracks and manual doctrinal review recorded in this lab.

## Stability Note

The frozen `v006` detection + `v009` assessment pair generalizes reasonably on
damaged-truck, operational-truck, and office scenes, but `tank.jpg` still
wobbles across repeats. Treat the tank case as a repeatability pressure test,
not the only evaluation case.

## Current Forward Path

The next work in this lab is:

1. treat `v006` detection + `v009` assessment as the current best-known
   benchmark
2. keep a small cross-image generalization sweep in the loop before treating a
   direction as done
3. use the stable baseline plus prior candidate failures as the comparison
   frame for each new loop
4. carry forward only explicitly documented lessons from each rejected version
   instead of inheriting a losing wording family wholesale
5. use the new research-loop notes under
   `z_reference_docs/Prompting/Research_Loops/` as the bridge between one run
   and the next candidate
6. treat a baseline-identical result as evidence that the prompt change was not
   salient enough, not as a neutral non-result
7. after a three-loop cycle or a generalization sweep, write a cycle summary
   before deciding whether to repeat the current best candidate or start a new
   problem area
8. keep the current top-level YAML structure stable unless prompt-surface
   tuning and backend-aware diagnosis both fail to explain the behavior
9. before starting a summary-only cycle, pressure-test one more grounding cycle
   when grounding still looks like the higher-risk blocker
10. when prompt-only grounding stalls on a pressure-test image, escalate to the
    smallest code-level grounding aid before rewriting the whole runtime

Important:

- this lab restarts the version sequence from a fresh `v000`
- the previous `q8_0` lab is archived under
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/`
- any experiment run from before `2026-04-10` is historical and should be
  treated as archive material, not active current-main evidence
- future model changes should create new lab contexts rather than reusing this
  sequence
- the active baseline snapshot was refreshed again after the upstream sync to
  `21deaf5`; prompt text and model tag remained unchanged, so the current
  `v000` through `v009` sequence remains the active line of evidence
- the frozen `v006` + `v009` pair looks broadly usable, but the tank seed is
  still the repeatability pressure point after the cross-image sweep
- the overlay/crop artifacts reviewed in this lab are currently generated by a
  temporary local repo commit on `main`, and the same temporary debug path now
  also exports `pipeline_debug.json` so failed detections can be diagnosed from
  the raw detection payload and bbox-validation path
- `v003` is the first active-sequence draft created after a focused review of
  Qwen localization references and general prompt-structure guidance
- `v003` tightened the box numerically, but manual review still found it off
  the actual target body
- `v004` showed that fire-source anchoring can over-shrink the box around the
  wrong patch, so the next candidate should recover the visible attached body
  segment more explicitly rather than the nearest fire-adjacent fragment
- `v005` showed that point-first, occlusion-aware prose can still be too weak
  to override the baseline behavior, so the next candidate should be shorter
  and more example-driven
- `v006` is the first active-sequence candidate to move the bbox materially
  onto the visible burning target body, but it also raised downstream
  confidence and summary strength, so it should be treated as best-so-far
  rather than promoted
- `v006` run02 repeated the improved bbox exactly, but later review still kept
  grounding as the higher-risk blocker before a summary-only cycle
- cycle 02 (`v007` to `v009`) tested assessment-only revisions while holding the
  current detection family steady
- `v007` was the first useful moderation step: it kept `PROBABLE` and removed
  K-kill / subtype drift, but it downgraded the category to `DAMAGED`
- `v008` confirmed that abstract category guidance was not the right lever
- `v009` is the current best assessment candidate because it restored
  `DESTROYED` + `PROBABLE` while keeping target-level wording generic
- the next cycle was re-opened on detection grounding first, and the first
  `_pixels` bbox-convention experiment (`v010`) then failed by collapsing to
  `object_not_found` on the tank seed
- `v011` is now the queued grounding recovery candidate: it returns to the
  normalized `xyxy_1000` contract and makes the detection prompt more
  explicitly Qwen-native instead of repeating the direct `_pixels` swap
- `v011` run01 recovered detection and preserved the stronger `v009`
  assessment behavior, but the recovered bbox converged back toward the older
  `v001` / `v002` tightened-box family instead of clearly improving past the
  frozen `v009` working baseline
- `v012` is now the queued follow-on grounding candidate: keep the normalized
  contract, drop the point-first method, return to the stronger contrastive
  style, and explicitly resist over-shrinking around the most salient burn
  patch
- `v012` run01 showed that this prompt-only refinement still did not produce a
  bbox win: the raw debug payload kept the baseline left/right span and only
  moved the box downward, which suggests prompt-only grounding is stalling on
  this seed case
- a code-level two-pass refinement path now exists behind
  `detection_vlm.refinement_enabled` and
  `detection_vlm.refinement_roi_buffer_ratio`
- that refinement path re-runs detection inside an expanded ROI around each
  accepted first-pass box, then maps the best overlapping same-label child box
  back to scene coordinates
- `v013` run01 is the first code-assisted grounding experiment:
  it preserved `DESTROYED` + `PROBABLE`, but the first pass narrowed to the
  older `[51, 37, 102, 73]` family and the ROI-local second pass found no
  detections, so refinement kept the narrower first-pass box
- `v013` run02 repeated that exact same behavior, so the current refinement
  parameterization is now confirmed as a stable non-win rather than a one-off
  wobble
- the immediate next step should be refinement-parameter tuning, most likely a
  larger ROI buffer, not promotion
- `v014` tested that larger ROI-buffer hypothesis directly, and it still
  produced no ROI-local second-pass detections
- that means ROI width alone is not enough; the next code-level step likely
  needs a different refinement method, not just a wider crop
