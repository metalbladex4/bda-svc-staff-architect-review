# BDA-SVC Qwen Prompt-Engineering Deep Research Bundle

Generated: 2026-05-06

## Purpose

This Markdown file is a one-attachment handoff bundle for GPT Deep Research.

It consolidates the relevant project context, repo-derived artifacts, current Qwen prompt state, evaluation metrics, prompt-engineering execution loop, source-authority rules, and an updated copy/paste Deep Research prompt.

The intent is to let GPT Deep Research understand the project without requiring many separate attachments.

## Important caveat

This bundle includes the source material available in the review repo and the user-provided execution loop. Raw prediction dumps, raw image overlays, local session state, credentials, and some visual artifacts were intentionally not copied into the review repo. If Deep Research needs those artifacts, it should ask for them or recommend how Codex should generate them.

## Current user decisions

The user has clarified:

1. The project must remain **prompt-engineering first**.
2. False negatives and false positives remain **equally weighted**.
3. `v020c` and `v024l` raw predictions, eval summaries, and visual artifacts should be made available to GPT Deep Research where possible.
4. FiftyOne has **not** been employed yet; Deep Research should recommend how to start using it from scratch.
5. Deep Research should focus primarily on Qwen-style VLM prompt workflows, but may research fringe/hybrid detection architectures, post-processing, NMS/box clustering, and active-learning loops that could help the project.

## Source authority order

Use this order:

1. Explicit user direction.
2. Source artifacts, manifests, eval summaries, runner outputs, raw predictions, overlays/crops when provided, and code.
3. Repo docs and prompt-lab evidence.
4. Graphify / project-brain / Mem0 / memory notes as navigation only.
5. General research and web sources as support, never as replacement for local eval evidence.

## Current source-verified state

* Project: `bda-svc`
* Task: multimodal VLM battle damage assessment
* Main prompt surface: `src/bda\_svc/pipeline/config.yaml` → `prompts.detect\_objects`
* Active model line: Qwen-style VLM detection
* Current incumbent: `v020c\_extra\_box\_audit` / `v020c\_anchor\_replay`
* Incumbent metrics: `186` matches / `33` false negatives / `25` false positives = `58` total FN+FP errors
* Best high-recall challenger: `v024l\_v023s\_no\_wheel\_track\_ablation`
* Challenger metrics: `188` matches / `31` false negatives / `35` false positives = `66` total FN+FP errors
* `v024l` is not incumbent because it adds `10` false positives for only `2` fewer false negatives.
* Interrupted row: `v024o\_v024l\_intact\_building\_piece\_exclusion`
* `v024o` is partial/unscored and must not be used as evidence.
* Evaluation pack: `human\_report\_challenge\_v2\_all\_current\_117\_no101`
* Objective: equal-weight `false\_negatives + false\_positives`
* Stretch target: literal 99% reduction from upstream baseline of `74` total errors, meaning `<=1` combined FN+FP.
* Current best remains `58` combined errors, so the project is far from the stretch target.

# Updated copy/paste prompt for GPT Deep Research

Paste the following prompt into GPT Deep Research together with this Markdown file attached.

```text
You are GPT Deep Research acting as a senior research partner for a Capstone project called `bda-svc`.

I am attaching one Markdown evidence bundle:

`bda\_svc\_qwen\_prompt\_engineering\_deep\_research\_bundle.md`

Purpose of the attachment:
- It consolidates the source-verified project handoff, current Qwen prompt state, current runtime prompt excerpt, latest v023/v024 pause report, key evaluation metrics, Codex execution loop, source-boundary rules, current user decisions, and the exact prompt-engineering workflow that needs improvement.
- Use it as the primary project context for this research task.
- Treat it as a consolidated handoff/evidence bundle, not as permission to mutate source truth.
- If repo artifacts or raw outputs are also available, use them to verify and deepen the bundle. If they are not available, use the bundle as the source-grounded project context and clearly identify any remaining gaps.

Your task is not to rewrite the detection prompt. Your task is to research and produce an evidence-backed improvement plan for Codex’s recursive prompt-engineering workflow for a Qwen-style VLM battle damage assessment system.

The project must remain PROMPT-ENGINEERING FIRST. You may research fringe or hybrid detection architectures, post-processing, NMS/box clustering, visual review, and active-learning loops, but those should be framed as support mechanisms, diagnostic aids, prompt-design inspiration, or future pivot options. The primary improvement target remains the Qwen VLM detection prompt workflow.

Core project facts from the attachment:

- Project: `bda-svc`
- Task: multimodal VLM battle damage assessment
- Primary prompt surface: `src/bda\_svc/pipeline/config.yaml` → `prompts.detect\_objects`
- Active model line: Qwen-style VLM detection
- Current model names:
  - local/fallback: `qwen3-vl:8b-instruct`
  - upstream config: `Qwen/Qwen3-VL-8B-Instruct`
- Current incumbent:
  - `v020c\_extra\_box\_audit` / `v020c\_anchor\_replay`
  - `186` matches / `33` false negatives / `25` false positives
  - `58` combined FN+FP errors
- Best high-recall challenger:
  - `v024l\_v023s\_no\_wheel\_track\_ablation`
  - `188` matches / `31` false negatives / `35` false positives
  - `66` combined FN+FP errors
- `v024l` is not the incumbent because it adds `+10` FPs for only `-2` FNs versus `v020c`.
- `v024o` is interrupted, partial, and unscored. Do not cite it as evaluated evidence.
- Evaluation objective:
  - FNs and FPs are weighted equally.
  - `combined\_error = false\_negatives + false\_positives`
  - long-term stretch target is a 99 percent reduction from the upstream baseline of `74` total errors, meaning `<=1` combined FN+FP.
- Current best remains `58` errors, far from target.
- FiftyOne has not yet been employed; do not assume it is already set up.
- Raw predictions, overlays/crops, and eval artifacts should be requested or generated if needed.

Source authority rules:

1. Source artifacts, manifests, eval summaries, runner outputs, raw predictions, overlays/crops when provided, code, and explicit user direction are authoritative.
2. Graphify, Mem0, memory notes, and advisory summaries are navigation only.
3. Do not score partial `v024o`.
4. Do not assume `v024l` replaced `v020c`.
5. Do not recommend source-truth mutation, prompt promotion, doctrine changes, runtime changes, or PR updates without a validation gate and explicit user approval.
6. Do not ask for secrets or credential values.
7. Do not assume Qwen prompt behavior transfers to Gemma or other VLMs.
8. Do not recommend adopting a prompt only because recall improves; false-positive burden and control cases matter.

Known failure patterns:

1. `v020c` is the stable incumbent but likely a brittle local optimum.
2. Case `67` is a dense-row sentinel. Many plausible prompt edits collapse it from `v020c`’s useful `9/2/4` behavior to roughly `1-2` matches with `9-11` false negatives and many false positives.
3. `v024l` proves a high-recall branch exists, but it remains FP-heavy.
4. Long prompt bloat tends to hurt.
5. Long building-specific de-tiling or intact-building exclusion blocks are especially dangerous.
6. `v024n\_v024l\_building\_only\_detiling` exploded to `102` false positives and should be treated as a hard warning against broad building-only prompt-rule blocks.
7. In the `v023s` branch, `silhouette` and `exterior wall/roof boundary` language were load-bearing; removing either collapsed dense case `67`.
8. Removing `wheel/track contact` produced the best v024 challenger, `v024l`, but did not fix the FP burden.
9. Metrics alone are insufficient now. Remaining errors require visual review to determine whether FPs are duplicates, nested fragments, context-only boxes, broad group boxes, building pieces, off-target adjacent objects, row-formation errors, or reference ambiguity.

Codex execution loop to improve:

Codex currently executes one prompt candidate at a time:
- parse latest user intent
- re-ground in source truth
- state boundaries
- preflight backend and manifests
- create/reuse experiment package
- replay incumbent when needed
- author exactly one prompt candidate
- run fixed packs
- parse metrics
- apply disqualifiers
- diagnose failure pattern
- update candidate ranking
- choose next move
- repeat sequentially
- close out and separate promotion from exploration

The weak point is that Codex can still over-focus on prompt wording and may author the next candidate before it has visually classified the failure mode.

Your research objective:

Produce concrete, evidence-backed ways to improve Codex’s recursive prompt-engineering workflow for Qwen-style VLM detection prompts.

Focus on methods, tactics, decision rules, and tooling that help Codex:

1. Generate better prompt candidates.
2. Diagnose failures more accurately.
3. Avoid prompt bloat and over-specific repairs.
4. Balance equal-weight false negatives and false positives.
5. Preserve dense-row recall while reducing false positives.
6. Use visual review systematically before authoring the next candidate.
7. Decide when prompt-only wording search has plateaued.
8. Continue prompt engineering first while safely using visual review, post-processing research, and hybrid architecture research as support or future pivot evidence.
9. Use tools, MCPs, memory, and experiment tracking without confusing navigation memory for source evidence.
10. Design validation protocols that reduce overfitting to case `67` while still respecting it as a sentinel.
11. Produce practical guidance Codex can apply one candidate at a time.

Research questions to answer directly:

1. What does current research and practitioner evidence say about Qwen-style VLM object localization prompt engineering, especially for bounding boxes, dense scenes, small objects, partially obscured objects, and adjacent-object confusion?

2. What compact prompt patterns are most likely to help VLM grounding without creating long brittle prompts?

3. Given the current plateau, should Codex mutate `v020c`, branch from `v024l`, hybridize `v020c` and `v024l` carefully, ablate known load-bearing phrases, or pause prompt edits until visual review classifies remaining errors?

4. What failure taxonomy should Codex apply before authoring any new candidate?

5. How should Codex perform visual failure review from scratch, assuming FiftyOne has not yet been used? Include a minimal setup/workflow using existing predictions, reference boxes, overlays, crops, and case metadata.

6. How should Codex compare `v020c` and `v024l` visually?
   - Which `v020c` FNs did `v024l` recover?
   - Which `v024l` FPs did `v020c` avoid?
   - Are added FPs duplicates, context-only boxes, building fragments, broad boxes, or true ambiguous targets?
   - Which differences are prompt-addressable?

7. What deterministic post-processing ideas should be researched as secondary support, not primary replacement?
   - duplicate suppression
   - NMS-like logic
   - same-body suppression
   - overlap clustering
   - broad-box rejection
   - dense-row-safe exceptions
   - visual verifier passes

8. How can lessons from post-processing and detection theory be converted into prompt-engineering tactics without immediately changing runtime code?

9. How should Codex distinguish local noise from general signal across iterations?

10. What plateau criteria should trigger:
   - continue from incumbent
   - continue from high-recall challenger
   - run visual review before another candidate
   - research post-processing as support
   - pause and report

11. How should Codex use external research tools, MCPs, vector memory, Graphify-like source recall, and visual analysis tools without polluting the evidence chain?

12. What should the next 3-5 prompt-engineering-first experiments be for this exact project, given that `v020c` remains incumbent and `v024l` is high-recall but FP-heavy?

Source priorities:

Prefer these source types:

- Peer-reviewed or preprint research on VLM grounding, object localization, dense detection, visual hallucination, evaluation, calibration, and prompt sensitivity.
- Official Qwen/Qwen-VL documentation, model cards, technical reports, or examples related to grounding, bounding boxes, and visual localization.
- Reputable practitioner writeups on object detection post-processing, NMS, box clustering, tiling suppression, and evaluation design.
- Documentation for visual dataset review tools such as FiftyOne, Label Studio, Roboflow, and related CV evaluation workflows.
- Documentation for Qdrant or vector memory only as support for experiment recall and not as source truth.
- Official OpenAI/Codex/Deep Research/evals/agents/tooling docs where relevant.

Avoid generic prompt-engineering advice unless it directly maps to VLM localization, dense object detection, recursive agentic improvement, or this project’s equal-weight FN+FP objective.

Desired output structure:

Produce a detailed but actionable report with citations.

Use this structure:

1. Executive summary.
2. Diagnosis of the current `bda-svc` methodology.
3. What the current evidence implies about prompt-engineering plateau.
4. Research-backed prompt-engineering techniques for Qwen-style VLM localization.
5. Candidate-generation strategy for Codex after each run.
6. Visual failure taxonomy for BDA VLM detection.
7. Visual failure-review protocol from scratch, including how to start with FiftyOne or equivalent tooling.
8. How to turn visual review findings into compact prompt candidates.
9. Deterministic post-processing and duplicate/tiling suppression concepts as secondary research support.
10. Tool/MCP/memory workflow for Codex.
11. Plateau and pivot criteria that preserve the prompt-engineering-first constraint.
12. Recommended next 3-5 experiments for this exact project.
13. A compact checklist Codex should run before authoring each new candidate.
14. Risks, unknowns, and validation gates.

For each recommendation, state:

- What problem it addresses.
- Why it might work.
- What evidence supports it.
- How to test it in `bda-svc`.
- What failure mode would invalidate it.
- Whether it is prompt-only, visual-review-assisted prompt engineering, post-processing research, backend/model research, or workflow/tooling.

Important decision pressure:

The user wants persistence toward a near-perfect target, but the evidence shows near-neighbor prompt wording may be plateauing.

Do not simply say “keep trying prompts.”

Instead, define disciplined criteria for:

- when Codex should continue prompt search,
- when it should conduct visual review before authoring another prompt,
- when it should branch from `v020c`,
- when it should branch from `v024l`,
- when it should avoid a candidate because it risks repeating `v024n`,
- and when non-prompt levers should be researched as support or future pivot paths.

Do not recommend promoting `v024l`.

Do not use `v024o` as scored evidence.

Do not recommend broad source-truth mutation.

Do not recommend long building-only prompt-rule blocks unless you explicitly explain why the approach would not repeat the `v024n` false-positive explosion.

The final answer should be useful enough that Codex can use it as operating doctrine for future recursive prompt-improvement cycles.
```

# Review repo orientation

Source path:

```text
REVIEW\_INDEX.md
```

Key facts:

* The repo `metalbladex4/bda-svc-staff-architect-review` is a review snapshot of the local Capstone multimodal VLM workspace.
* It exists so GPT-style reviewers can inspect code, local evidence, prompt labs, doctrine experiments, and supporting context as a Staff AI Systems Architect / Prompt-Evaluation Lead.
* GitHub currently reports the repository as `PUBLIC`, so the review surface should be treated as sanitized.
* Do not add raw credentials, raw local Codex state, private auth/session files, or unreviewed secret-bearing artifacts.
* Current branch review surface: `main`.
* Latest refresh: `2026-05-06`.
* Primary current handoff:

  * `z\_reference\_docs/GPT-Pro\_collab/chatgpt\_5\_5\_pro\_prompt\_engineering\_handoff.md`
* Runtime code baseline captured:

  * `cmu-bda/bda-svc upstream/main`
  * `f462ef4516b63ca1a2cd2434e75692f65d0e94cb`
* Prompt config overlay captured:

  * `feat/config-prompt-improved-v1`
  * `9f1079daee9d50957048860e692e6a624befe230`
* Current prompt incumbent:

  * `v020c\_extra\_box\_audit` / `v020c\_anchor\_replay`
  * `186` matches / `33` false negatives / `25` false positives
* Important orientation rule:

  * Read `Z\_REFERENCE\_DOCS\_GUIDE.md` before drawing conclusions from `z\_reference\_docs/`.
  * That tree is a layered local evidence/research/documentation hub, not a flat folder of equally authoritative runtime sources.
* Focus reset:

  * Normal work should return to `/home/williambenitez1/Capstone` and its active worktrees after this review mirror is used.
  * This review repo should only be updated again on explicit request.

# Review repo refresh state

Source path:

```text
REVIEW\_REFRESH\_2026-05-06.md
```

Verified refresh facts:

* The review repo was refreshed on `2026-05-06`.
* It merged current `cmu-bda/bda-svc upstream/main` at `f462ef4516b63ca1a2cd2434e75692f65d0e94cb`.
* It overlaid the promoted Qwen config prompt from local branch `feat/config-prompt-improved-v1`.
* It added the ChatGPT 5.5 Pro handoff dossier:

  * `z\_reference\_docs/GPT-Pro\_collab/chatgpt\_5\_5\_pro\_prompt\_engineering\_handoff.md`
* It refreshed current living docs:

  * `z\_reference\_docs/WORKING\_CHANGELOG.md`
  * `z\_reference\_docs/REFERENCE\_MASTER\_INDEX.md`
  * `z\_reference\_docs/PROMPT\_DEVELOPMENT\_METHODOLOGY.md`
  * `z\_reference\_docs/PROMPT\_CRAFTING\_INSTRUCTIONAL\_GUIDE.md`
  * `z\_reference\_docs/PROJECT\_BRAIN.md`
  * `z\_reference\_docs/Prompt\_Labs/PROMPT\_LABS\_INDEX.md`
* It added the active Qwen prompt-lab evidence tree under:

  * `docs/prompt-lab/qwen-v015-human-report-strategy/`
* Sanitization note:

  * raw credentials, local auth/session state, Codex state, raw image overlays, and predicted-output dumps were not copied.
* Current prompt incumbent:

  * `v020c\_extra\_box\_audit` / `v020c\_anchor\_replay`
  * `186` matches / `33` false negatives / `25` false positives
* Best high-recall challenger:

  * `v024l\_v023s\_no\_wheel\_track\_ablation`
  * `188/31/35`
  * FP-heavy and does not replace `v020c`.
* Interrupted row:

  * `v024o\_v024l\_intact\_building\_piece\_exclusion`
  * partial and unscored.

# Current Qwen runtime prompt/config excerpt

Source path in review repo:

```text
src/bda\_svc/pipeline/config.yaml
```

Current relevant backend state:

```yaml
detection\_vlm:
  model: Qwen/Qwen3-VL-8B-Instruct
  bbox\_convention: xyxy\_1000
  temperature: 0.0
  max\_image\_size: 1024
  crop\_buffer\_ratio: 0.2

assessment\_vlm:
  model: Qwen/Qwen3-VL-8B-Instruct
  temperature: 0.0
  max\_image\_size: 1024
```

Current `prompts.detect\_objects`:

```yaml
prompts:
  detect\_objects: |
    Perform a VISUAL-ONLY object detection.

    TASK
    Detect targets whose doctrinal target\_type is one of:
    {categories}

    Calibration from prior runs: broad recall additions raised false positives. Return to the v019c context-shadow balance and improve only the final cleanup of extra boxes.

    CONTEXT SHADOW REVERSAL
    Use context to search, then mentally remove context to decide.

    1. Find possible targets across the full image.
    2. For each candidate, imagine removing smoke, dust, flame, shadow, road, debris, row alignment, blast texture, tracks, terrain marks, and repeated spacing.
    3. Keep the candidate only if a target body, wreck body, or exterior structure remains visible enough to draw a tight box after those context cues are removed.
    4. If the candidate disappears when context is ignored, reject it.
    5. If a broad box contains several possible targets, split only when distinct bodies are visible; otherwise reject the broad box.

    GOOD FINAL BOX
    - one connected target body, wreck body, or exterior building structure
    - tight enough that the target occupies most of the box
    - not a proxy for damage effects, row position, nearby roads, repeated spacing, or debris

    BAD FINAL BOX
    - context-only cue
    - group, row, convoy, cluster, or scene region
    - duplicate fragment of one connected body
    - interior/facade/debris subsection of one continuous building
    - extra neighboring box whose distinct body boundary is not visible

    EXTRA-BOX AUDIT
    Before output, silently inspect every detection that sits near another detection or near a strong context cue. Remove it unless it has its own visible body center and at least one visible body edge or exterior-structure boundary. If two boxes describe the same connected body or the same continuous exterior building, keep only the tighter whole-body box.

    FINAL BALANCE
    Keep v019c recall behavior: small, damaged, crowded, or partly obscured targets are valid when their own target body remains visible after context is removed. The audit removes extras; it should not remove a true separable target body.

    TARGET-TYPE SPECIFIC DETECTION GUIDANCE
    {detection\_guidance}

    BOUNDING BOX FORMAT
    - Format: {bbox\_format}
    - Coordinate scale: {bbox\_scale}

    OUTPUT
    Return valid JSON only.
    Return a JSON object with a top-level detections field.
    If no valid target is visible, return {"detections": \[]}.

    OUTPUT SCHEMA
    {
      "detections": \[
        {
          "target\_type": string,
          "bbox": {bbox\_format}
        }
      ]
    }
```

# Latest v023/v024 pause and recommendation facts

Source paths:

```text
docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human\_report\_challenge\_v2\_prompt\_iteration\_workflow/cycle\_001/main\_promotion/v017b\_prompt\_only\_main\_promotion/v023\_literal99\_qwen\_no\_stop\_continuation/pause\_report\_2026-05-06.md

docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human\_report\_challenge\_v2\_prompt\_iteration\_workflow/cycle\_001/main\_promotion/v017b\_prompt\_only\_main\_promotion/v023\_literal99\_qwen\_no\_stop\_continuation/final\_recommendation.md
```

## Pause status

* User paused the loop before `v024o\_v024l\_intact\_building\_piece\_exclusion` all-current run completed.
* `v024o` has partial predictions only.
* `v024o` must not be scored or treated as evidence.
* If resumed, rerun `v024o` from scratch.
* No prompt from the continuation was promoted or adopted.

## Current champion

```text
v020c\_anchor\_replay
186 matches / 33 false negatives / 25 false positives
58 total errors
```

Controls:

```text
case 155 = 2/0/0
case 166 = 1/0/0
office-negative = 1/1
```

Literal 99 target:

```text
target <= 1 combined FN+FP
best row remains 58 combined errors
target not met
```

Backend note:

* Preferred `http://localhost:8000/v1` was unavailable after retry.
* Rows used authorized Ollama-backed OpenAI-compatible fallback:

  * `http://localhost:11434/v1`

## Best challenger

```text
v024l\_v023s\_no\_wheel\_track\_ablation
188 matches / 31 false negatives / 35 false positives
66 total errors
```

Interpretation:

* Improved recall versus `v020c`.
* Added `+10` FPs versus `v020c`.
* Worse overall under equal FN+FP objective.
* High-recall learning evidence only.

Dense behavior:

```text
v020c: 66=8/0/4, 67=9/2/4, 84=8/5/0, 97=1/0/2
v023s: 66=8/0/6, 67=8/3/4, 84=6/7/3, 97=1/0/2
v024l: 66=8/0/6, 67=9/2/3, 84=7/6/0, 97=1/0/2
v024n: 66=8/0/6, 67=2/9/10, 84=6/7/3, 97=1/0/2
```

Key lessons:

* `v020c` remains the stable prompt incumbent.
* Case `67` is a brittle dense-row sentinel.
* Exact wording and order are load-bearing.
* `v023s` and `v024l` define a useful high-recall branch but are FP-heavy.
* In the `v023s` support phrase ablations:

  * `silhouette` was load-bearing for dense row behavior.
  * `exterior wall/roof boundary` was load-bearing for dense row behavior.
  * removing `wheel/track contact` produced the best v024 challenger but did not solve FP burden.
* Broad BDA-salience wording has some signal for building/background FPs but globally harms dense-vehicle behavior.
* Long building-specific de-tiling sections are dangerous:

  * `v024n\_v024l\_building\_only\_detiling` exploded to `102` FPs.
* Next high-leverage work should favor visual review plus duplicate/tiling/post-processing research rather than more long building-only prompt rules, while the user has clarified that the project must remain prompt-engineering first.

# v023/v024 iteration matrix

The latest pause report includes this score matrix. `Errors = FNs + FPs`.

|Prompt|Matches|FNs|FPs|Errors|155|166|Office|Status|
|-|-:|-:|-:|-:|-|-|-|-|
|`v020c\_anchor\_replay`|186|33|25|58|2/0/0|1/0/0|1/1|`champion`|
|`v023a\_visible\_center\_pin\_map`|177|42|33|75|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023b\_dense\_safe\_singleton\_audit`|173|46|32|78|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023c\_body\_baseline\_anchor`|174|45|38|83|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023d\_dust\_row\_antidrift\_calibration`|175|44|34|78|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023e\_v020c\_stability\_rail`|171|48|35|83|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023f\_compact\_shadow\_audit`|182|37|66|103|2/0/0|1/0/0|1/1|`fp\_explosion`|
|`v023g\_compact\_ruler\_chain\_veto`|183|36|71|107|2/0/2|1/0/0|1/1|`fp\_explosion`|
|`v023h\_unique\_body\_signature\_ledger`|173|46|49|95|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023i\_official\_style\_count\_lock`|178|41|40|81|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023j\_v020c\_no\_history\_clean`|174|45|30|75|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023k\_v020c\_missed\_target\_pass`|172|47|35|82|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023l\_v020c\_silent\_qa\_loupe`|175|44|35|79|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023m\_v020c\_perspective\_depth\_recall`|171|48|32|80|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023n\_v020c\_locked\_policy\_header`|173|46|32|78|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023o\_v020c\_output\_contract\_first`|177|42|53|95|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023p\_four\_edge\_boundary\_detector`|176|43|36|79|2/0/1|1/0/0|1/1|`learning\_only`|
|`v023q\_v020c\_edge\_support\_audit\_swap`|173|46|32|78|2/0/1|1/0/0|1/1|`learning\_only`|
|`v023r\_dense\_row\_exception\_precision\_audit`|175|44|36|80|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023s\_qwen\_native\_conservative\_json`|190|29|37|66|2/0/0|1/0/0|1/1|`high\_recall\_branch`|
|`v023t\_qwen\_native\_duplicate\_collapse`|178|41|41|82|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023u\_qwen\_native\_sparse\_only\_cleanup`|180|39|34|73|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023v\_qwen\_native\_nested\_overlap\_guard`|182|37|42|79|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023w\_qwen\_native\_building\_centrality\_guard`|178|41|38|79|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023x\_qwen\_native\_connected\_body\_only`|180|39|48|87|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023y\_qwen\_native\_row\_count\_discipline`|180|39|42|81|2/0/0|1/0/0|1/1|`learning\_only`|
|`v023z\_qwen\_native\_high\_confidence\_filter`|178|41|37|78|2/0/0|1/0/0|1/1|`learning\_only`|
|`v024a\_coco\_instance\_annotator`|184|35|44|79|2/0/0|1/0/0|1/1|`learning\_only`|
|`v024b\_v020c\_imagewide\_scan\_first`|175|44|40|84|2/0/2|1/0/0|1/1|`learning\_only`|
|`v024c\_official\_style\_ground\_all\_targets`|166|53|37|90|2/0/0|1/0/0|1/1|`learning\_only`|
|`v024d\_v020c\_recall\_balance\_before\_audit`|173|46|31|77|2/0/0|1/0/0|1/1|`learning\_only`|
|`v024e\_v020c\_bbox\_physical\_extent\_calibration`|168|51|30|81|2/0/0|1/0/0|1/1|`learning\_only`|
|`v024f\_silent\_three\_role\_arbiter`|183|36|44|80|2/0/0|1/0/0|1/1|`learning\_only`|
|`v024g\_v020c\_visual\_sequence\_output`|182|37|39|76|2/0/1|1/0/0|1/1|`learning\_only`|
|`v024h\_v020c\_dust\_base\_vehicle\_body`|174|45|30|75|2/0/0|1/0/0|1/1|`learning\_only`|
|`v024i\_v023s\_body\_mass\_only`|183|36|40|76|2/0/0|1/0/0|1/1|`learning\_only`|
|`v024j\_v023s\_no\_silhouette\_ablation`|179|40|39|79|2/0/0|1/0/0|1/1|`learning\_only`|
|`v024k\_v023s\_no\_wall\_roof\_boundary\_ablation`|182|37|39|76|2/0/0|1/0/0|1/1|`learning\_only`|
|`v024l\_v023s\_no\_wheel\_track\_ablation`|188|31|35|66|2/0/0|1/0/0|1/1|`best\_challenger, high\_recall\_branch`|
|`v024m\_v024l\_bda\_salience\_gate`|173|46|37|83|2/0/0|1/0/0|1/1|`learning\_only`|
|`v024n\_v024l\_building\_only\_detiling`|181|38|102|140|2/0/0|1/0/0|1/1|`fp\_explosion`|
|`v024o\_v024l\_intact\_building\_piece\_exclusion`|n/a|n/a|n/a|n/a|office-negative passed|n/a|1/1|`interrupted\_partial\_by\_user\_pause`|

# Codex execution loop supplied by user

# Codex Prompt-Engineering Execution Process

When the user says “execute the prompt-engineering plan,” Codex follows this operational loop.

## 1\. Parse The User’s Latest Intent

First, Codex extracts the exact execution contract from the latest user message.

It identifies:

* target model line, usually Qwen or Gemma
* target prompt surface, usually `prompts.detect\_objects`
* current incumbent prompt
* candidate scope
* required backend
* required validation packs
* stop rules
* whether candidates must be sequential or can be batched
* whether promotion is allowed
* whether live docs / Graphify / Mem0 updates are in scope

Most recent standard:

```text
Sequential, one prompt at a time.
Do not prewrite all final prompts.
Run, diagnose, learn, then author the next prompt.
```

## 2\. Re-Ground In Current State

Before editing or running anything, Codex rechecks the current source of truth.

Typical grounding sources:

```text
z\_reference\_docs/WORKING\_CHANGELOG.md
z\_reference\_docs/PROMPT\_DEVELOPMENT\_METHODOLOGY.md
z\_reference\_docs/PROJECT\_BRAIN.md
Prompt-lab final\_recommendation.md files
comparison\_matrix.md/json files
candidate diagnosis files
Graphify recall, as navigation only
```

Purpose:

* confirm current incumbent
* confirm latest pause state
* confirm which candidates are scored or unscored
* avoid accidentally resuming from stale chat memory
* avoid treating partial runs as evidence

Example current state:

```text
v020c is incumbent.
v024l is high-recall but FP-heavy.
v024o is partial/unscored.
```

## 3\. Establish Non-Negotiable Boundaries

Codex writes down, mentally or in a run note, what must not change.

Common boundaries:

```text
Do not edit source truth.
Do not edit doctrine unless explicitly approved.
Do not change assessment prompt.
Do not change runtime code.
Do not include case 101 in no101 manifests.
Do not promote unless user explicitly approves.
Do not use partial runs as scored results.
Do not treat Graphify/Mem0 as evidence.
```

For prompt comparison, only this should change:

```text
prompts.detect\_objects
```

## 4\. Preflight The Runtime

Codex checks that the backend and model path are available.

Preferred current backend:

```text
OPENAI\_BASE\_URL=http://localhost:8000/v1
```

Authorized fallback:

```text
OPENAI\_BASE\_URL=http://localhost:11434/v1
```

If fallback is used, Codex labels it clearly as:

```text
Ollama-backed OpenAI-compatible endpoint
```

Preflight checks:

* endpoint reachable
* model visible
* manifest exists
* manifest case count matches expectation
* case `101` excluded
* cases `155` and `166` included
* office-negative pack exists
* prompt placeholders preserved

Required placeholders:

```text
{categories}
{detection\_guidance}
{bbox\_format}
{bbox\_scale}
```

## 5\. Create Or Reuse An Experiment Package

Codex creates a dedicated evidence folder for the cycle.

Typical contents:

```text
README.md
source\_manifest.json
candidate\_registry.json
backend\_preflight.json
recovery\_log.md/json
comparison\_matrix.md/json
final\_recommendation.md/json
overlays/
diagnoses/
runs/
scripts/
```

This matters because each cycle must be reproducible and reviewable later.

## 6\. Replay The Incumbent When Needed

Before testing new candidates, Codex often replays the incumbent.

Purpose:

* confirm runtime stability
* confirm metrics did not drift
* make comparison fair
* avoid judging new candidates against stale evidence

If incumbent replay drifts badly, Codex should stop and diagnose runtime drift before continuing.

## 7\. Author Exactly One Candidate

Codex authors one prompt candidate based on the previous diagnosis.

It should have one main hypothesis, not ten.

Example candidate hypothesis:

```text
Reduce false positives from context-only boxes while preserving dense-row recall.
```

Codex then writes the candidate as an overlay or scratch config prompt.

It must preserve:

```text
categories placeholder
detection guidance placeholder
bbox format placeholder
bbox scale placeholder
JSON schema instructions
```

Codex avoids changing anything else.

## 8\. Run The Candidate On Fixed Tests

Each candidate is run against the same packs.

Main pack:

```text
human\_report\_challenge\_v2\_all\_current\_117\_no101
```

Guard pack:

```text
legacy\_abstention\_guard\_office\_negative
```

The run produces:

```text
predictions
eval summary
candidate manifest run summary
logs
possibly bbox/eval artifacts
```

Codex does not judge from vibe. It waits for metrics.

## 9\. Parse Results

Codex extracts the core metrics:

```text
matches
false negatives
false positives
combined FN+FP
image\_count
case 155 behavior
case 166 behavior
office-negative behavior
dense cases 66/67/84/97
JSON/runtime validity
```

Then it compares the candidate against:

```text
current incumbent
previous candidate
upstream baseline if relevant
historical key candidates if needed
```

## 10\. Gate The Candidate

Before considering whether it is good, Codex checks disqualifiers.

Disqualifiers:

```text
155 fails
166 fails
office-negative fails
invalid JSON/runtime failure
case 101 appears in active no101 eval
manifest count wrong
candidate did not complete
```

If any disqualifier happens, the candidate is learning evidence only or discarded.

## 11\. Diagnose The Failure Pattern

This is the most important step.

Codex writes a diagnosis for the candidate before authoring the next one.

The diagnosis asks:

* What improved?
* What regressed?
* Did recall improve?
* Did FPs rise?
* Did dense case `67` collapse?
* Did the prompt become too conservative?
* Did it create duplicate boxes?
* Did it box smoke/debris/context?
* Did it box building fragments?
* Did it miss small but valid targets?
* Did one phrase appear load-bearing?
* What should the next candidate preserve?
* What should the next candidate avoid?

The diagnosis becomes the input to the next candidate.

## 12\. Update The Candidate Ranking

Codex updates the comparison matrix.

Candidates are classified as:

```text
incumbent
strong challenger
high-recall learning evidence
precision learning evidence
disqualified
unscored / interrupted
```

Example:

```text
v020c = incumbent
v024l = high-recall learning evidence, FP-heavy
v024o = interrupted/unscored
```

## 13\. Decide The Next Move

Codex chooses one of four actions:

```text
continue from incumbent
continue from challenger
pivot candidate axis
pause and report
```

If the last few candidates failed similarly, Codex should pivot rather than keep tweaking the same idea.

Example pivot:

```text
Stop adding building-only rules.
Try visual review or duplicate/tiling suppression instead.
```

## 14\. Repeat Sequentially

The loop repeats:

```text
author one candidate
run fixed packs
parse results
diagnose
update matrix
learn
author next candidate
```

The key is that the next prompt is shaped by the previous result. Codex should not write six final prompts in advance unless explicitly told to batch.

## 15\. Recovery Behavior

If something breaks, Codex tries to recover before stopping.

Common recovery attempts:

```text
retry endpoint check
verify model list
check manifest path
check output directory
rerun failed candidate once
repair YAML once or twice
rerun eval from existing predictions
rerun full candidate if summary malformed
```

But Codex should stop for:

```text
source-truth contradiction
manifest semantics invalid
case 101 contaminating no101 pack
positive controls missing
backend repeatedly unavailable
candidate surface no longer fixed
baseline replay drift
```

## 16\. Closeout

When interrupted, plateaued, or finished, Codex writes a closeout packet.

Closeout includes:

```text
best candidate
incumbent
all candidate metrics
controls
dense-case behavior
what worked
what failed
what to try next
what not to try again
whether anything should be promoted
```

If approved, Codex updates:

```text
WORKING\_CHANGELOG.md
PROMPT\_DEVELOPMENT\_METHODOLOGY.md
PROMPT\_LABS\_INDEX.md
PROJECT\_BRAIN / verified notes
Graphify
Mem0 advisory memory
```

## 17\. Promotion Is Separate

Prompt exploration does not automatically become product config.

Promotion requires explicit user approval.

When approved, Codex creates a clean branch from upstream/main and changes only:

```text
src/bda\_svc/pipeline/config.yaml
```

Then it validates:

```text
only intended file changed
placeholders preserved
YAML tests pass
git diff --check passes
```

## 18\. The Actual Recursive Self-Improvement Loop

The real recursive loop is not just “make another prompt.”

It is:

```text
observe result
explain why it happened
extract a reusable lesson
adjust the next hypothesis
adjust tool use if needed
run again
document the lesson
```

Codex is supposed to improve both:

1. the prompt through iterative refinement
2. the process used to invent the next prompt through recursive self improvement

The weak point is that Codex can still over-focus on wording. The process now needs stronger visual failure review and better pivot rules when prompt-only search plateaus.

# Original uploaded handoff dossier

# ChatGPT 5.5 Pro Prompt-Engineering Handoff Dossier

Generated: 2026-05-06

## Copy/Paste Mission Prompt For ChatGPT 5.5 Pro

You are being brought in as a research partner for a local Capstone project
called `bda-svc`. The project is a battle damage assessment workflow that uses
vision-language models to detect damaged military-relevant targets in imagery
and produce structured BDA reports.

Your job is not to immediately rewrite the prompt. Your job is to first
understand the repository, the prompt-engineering history, the evaluation
artifacts, and the current limits of our iterative method. After you understand
the context, ask follow-up questions if anything important is missing. Once you
have enough context, craft a strong prompt for GPT Deep Research. That Deep
Research prompt should research ways to improve Codex's prompt-engineering
techniques, tactics, procedures, tool use, and recursive self-improvement loop
so that Codex can autonomously create better prompt versions after each
iteration.

The final objective is intentionally extreme: keep improving the
`detect\_objects` prompt toward a literal near-perfect target of 99 percent
improvement in measured detection errors. In this project, that target has been
operationalized as a 99 percent reduction in combined false negatives plus false
positives on the main all-current/no101 validation set. The current best prompt
does not meet that target.

Important current state:

* Current Qwen incumbent: `v020c\_extra\_box\_audit` / `v020c\_anchor\_replay`.
* Current incumbent metrics: `186` matches / `33` false negatives /
`25` false positives, `58` total FN+FP errors.
* Current best high-recall challenger: `v024l\_v023s\_no\_wheel\_track\_ablation`.
* Challenger metrics: `188` matches / `31` false negatives /
`35` false positives, `66` total FN+FP errors.
* `v024l` is not better overall because its false-positive burden is too high.
* `v024o\_v024l\_intact\_building\_piece\_exclusion` was interrupted before the
all-current run completed. It is partial and unscored. Do not treat it as
evidence unless it is rerun fully.
* The current recommendation is to preserve `v020c` and investigate visual
review plus non-prompt duplicate/tiling suppression or backend/post-processing
before more long prompt-only building rules.

Please analyze the local repo and this handoff. Then produce:

1. Your understanding of the task and current state.
2. Follow-up questions required before Deep Research, if any.
3. A Deep Research prompt that asks for concrete, research-backed ways to
improve Codex's recursive prompt-engineering workflow, including candidate
generation, diagnosis, evaluation, tool use, visual review, benchmark design,
failure taxonomy, and stopping/pivot criteria.

Boundaries:

* Do not treat local memory systems as source truth. Source artifacts, manifests,
runner outputs, eval summaries, code, and explicit user direction win.
* Do not score partial `v024o` outputs.
* Do not assume `v024l` replaced `v020c`.
* Do not recommend source-truth mutation without explicit validation and user
approval.
* Do not include or request credential values.
* The private GitHub review repo should not be updated unless the user gives a
separate explicit instruction.

## Project Context

Repository root:

```text
/home/williambenitez1/Capstone
```

Primary active Qwen worktree:

```text
/home/williambenitez1/Capstone\_worktrees/1.2\_feat\_\_qwen3-vl-8b-instruct\_\_two-pass-refinement
```

The project, `bda-svc`, is a local CLI/service workflow for battle damage
assessment. The relevant prompt surface is the detection prompt:

```yaml
prompts.detect\_objects
```

The stable product config path is:

```text
src/bda\_svc/pipeline/config.yaml
```

The current prompt-engineering work is mostly local prompt-lab evidence under:

```text
/home/williambenitez1/Capstone\_worktrees/1.2\_feat\_\_qwen3-vl-8b-instruct\_\_two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human\_report\_challenge\_v2\_prompt\_iteration\_workflow/cycle\_001/
```

These prompt-lab packages are local evidence, not automatically promoted runtime
truth. A prompt only becomes product-facing after a separate promotion path.

## Evaluation Frame

The main recent evaluation pack is:

```text
human\_report\_challenge\_v2\_all\_current\_117\_no101
```

Key control cases:

* `155`: positive-control case that must remain safe.
* `166`: positive-control case that must remain safe.
* `legacy\_abstention\_guard\_office\_negative`: one-case negative-scene abstention
guard.

Key dense/pressure cases:

* `66`
* `67`
* `84`
* `97`

Case `67` has become the most important dense-row sentinel. Many prompt edits
that look reasonable globally collapse case `67` from the incumbent's useful
`9/2/4` behavior to only `1-2` matches with `9-11` false negatives and many
false positives.

The literal 99 percent target used in the latest cycles:

* Current upstream prompt baseline was treated as `74` total detection errors:
`38` false negatives plus `36` false positives.
* Literal 99 percent reduction target means `<= 1` combined false negative plus
false positive on the all-current/no101 set.
* Best result so far remains `58` total errors, so we are far from that target.

## Current State

The most current source-verified checkpoint says there has been no new prompt
run, code change, doctrine change, promotion, or source-truth update since the
v023/v024 pause closeout.

Current Qwen incumbent:

```text
v020c\_extra\_box\_audit / v020c\_anchor\_replay
186 matches / 33 false negatives / 25 false positives
58 combined FN+FP errors
controls passed: 155, 166, office-negative
```

Best high-recall challenger:

```text
v024l\_v023s\_no\_wheel\_track\_ablation
188 matches / 31 false negatives / 35 false positives
66 combined FN+FP errors
controls passed: 155, 166, office-negative
```

Why `v024l` is not the incumbent:

* It gained `+2` matches and reduced false negatives by `2` compared with
`v020c`.
* It added `+10` false positives compared with `v020c`.
* It is useful learning evidence, but worse on the combined error objective.

Interrupted candidate:

```text
v024o\_v024l\_intact\_building\_piece\_exclusion
```

`v024o` was paused before the all-current run completed. It has partial
predictions only and must not be scored. If resumed, rerun it fully from
scratch.

Config-only review branch context:

* `v020c` was selected for a config-only review branch:
`feat/config-prompt-improved-v1`.
* The intended branch scope is only:
`src/bda\_svc/pipeline/config.yaml`.
* This dossier is not asking ChatGPT 5.5 Pro to open, update, or push that
branch. It is context for why `v020c` is treated as the current Qwen
config-prompt incumbent.

## Progress History

### v017b - parked prompt-only candidate

`v017b\_group\_box\_rejection` was an accepted prompt-only candidate at one point
because it improved control safety and false-positive discipline relative to
some earlier rows. It remained parked after additional comparison showed that
the current upstream prompt had stronger recall in ordinary multi-target scenes.

The lesson was that stricter defensive wording can reduce false positives and
protect controls, but it can also under-count clean multi-object scenes.

### Upstream/main comparison

The upstream/main detect prompt performed better than expected because it was
short, permissive, and recall-friendly. It did well on ordinary visible-target
recall, but it failed important control behavior, especially around case `155`
in earlier comparisons.

This produced the first major tension:

* Upstream style: concise and recall-friendly.
* v017b style: defensive and control-safe, but under-counted in some scenes.

### v018 - upstream/v017b amalgamation cycle

Package:

```text
/home/williambenitez1/Capstone\_worktrees/1.2\_feat\_\_qwen3-vl-8b-instruct\_\_two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human\_report\_challenge\_v2\_prompt\_iteration\_workflow/cycle\_001/main\_promotion/v017b\_prompt\_only\_main\_promotion/upstream\_v017b\_amalgamation\_cycle/
```

Baselines:

|Row|Matches|FNs|FPs|155|
|-|-:|-:|-:|-|
|upstream prompt-controlled|169|50|24|fail|
|v017b local Qwen|165|54|22 raw / 21 effective|pass|
|v017b upstream-code compat|166|53|26|pass|

Best v018 signals:

* `v018d\_evidence\_budget\_pruner`: `180/39/39`, recall ceiling but too many FPs.
* `v018e\_contrastive\_body\_anchor`: `173/46/29`, best precision-balanced
follow-up axis.

Outcome:

* No v018 prompt was adoption-ready.
* All improved recall over upstream/v017b in some way, but all exceeded the
false-positive ceiling.

### v019 - v018e creative follow-up

Package:

```text
/home/williambenitez1/Capstone\_worktrees/1.2\_feat\_\_qwen3-vl-8b-instruct\_\_two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human\_report\_challenge\_v2\_prompt\_iteration\_workflow/cycle\_001/main\_promotion/v017b\_prompt\_only\_main\_promotion/v019\_v018e\_creative\_followup\_cycle/
```

Fresh anchor:

```text
v018e\_anchor\_replay: 173 / 46 / 29, controls pass
```

Best v019 row:

```text
v019c\_context\_shadow\_reversal: 174 / 45 / 28, controls pass
```

Outcome:

* `v019c` was a strong next-primary candidate compared with `v018e`.
* It improved recall and slightly reduced false positives, but still did not
approach the later target.

### v020 - goal-driven self-improvement cycle

Package:

```text
/home/williambenitez1/Capstone\_worktrees/1.2\_feat\_\_qwen3-vl-8b-instruct\_\_two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human\_report\_challenge\_v2\_prompt\_iteration\_workflow/cycle\_001/main\_promotion/v017b\_prompt\_only\_main\_promotion/v020\_v019c\_goal\_driven\_self\_improvement\_cycle/
```

Started from:

```text
v019c\_context\_shadow\_reversal: 174 / 45 / 28
```

Best row:

```text
v020c\_v019c\_extra\_box\_audit: 186 / 33 / 25
```

Exact replay:

```text
v020h: 186 / 33 / 25
```

Outcome:

* `v020c` was the first stable prompt-only breakthrough.
* Exact replay reproduced the result.
* Success target for that cycle (`FNs <=25`, `FPs <=15`) was not reached.
* Later v020 variants mostly hurt dense rows or increased false positives.

Dense-case `v020c` profile:

|Case|Matches|FNs|FPs|Read|
|-|-:|-:|-:|-|
|`66`|8|0|4|full recall, extra row boxes remain|
|`67`|9|2|4|major recovery versus v019c|
|`84`|8|5|0|useful recall, misses distant row vehicles|
|`97`|1|0|2|target found, extra boxes remain|

### v021 - OpenAI-compatible cross-model matrix

Package:

```text
/home/williambenitez1/Capstone\_worktrees/1.2\_feat\_\_qwen3-vl-8b-instruct\_\_two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human\_report\_challenge\_v2\_prompt\_iteration\_workflow/cycle\_001/main\_promotion/v017b\_prompt\_only\_main\_promotion/v021\_openai\_compat\_cross\_model\_prompt\_matrix/
```

Purpose:

* Compare `upstream/main`, `v009`, `v017b`, `v018e`, `v019c`, and `v020c`
through the fetched upstream/main OpenAI-compatible runtime path.
* Test both Qwen and Gemma rows.
* Confirm doctrine diff gate.

Key result:

* Qwen winner: `v020c\_extra\_box\_audit` at `186/33/25`, controls passing.
* Gemma winner among eligible rows: `v018e\_contrastive\_body\_anchor` at
`138/81/19`, controls passing.
* Gemma `v020c` lowered false positives to `18`, but failed positive control
`155`, so it was disqualified for Gemma.
* Local and fetched upstream `doctrine.yaml` matched exactly, so there was one
shared-doctrine matrix.

Major process lesson:

* Future prompt comparisons should default to the upstream OpenAI-compatible
`OPENAI\_BASE\_URL` code path.
* If the backing server is Ollama's `/v1` endpoint, label it honestly as
OpenAI-compatible Ollama, not pure upstream vLLM/server.

### v022 - literal-99 Qwen prompt-only plateau

Package:

```text
/home/williambenitez1/Capstone\_worktrees/1.2\_feat\_\_qwen3-vl-8b-instruct\_\_two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human\_report\_challenge\_v2\_prompt\_iteration\_workflow/cycle\_001/main\_promotion/v017b\_prompt\_only\_main\_promotion/v022\_literal99\_qwen\_recursive\_prompt\_refinement\_cycle/
```

Literal target:

```text
upstream baseline errors: 74 = 38 FNs + 36 FPs
target: <= 1 combined FN+FP
```

Best row:

```text
v020c\_anchor\_replay: 186 / 33 / 25, 58 total errors
```

All new v022 variants regressed.

Important failure:

Even adding one dense-guard sentence to v020c disturbed case `67` and worsened
case `84`. This made `v020c` look like a brittle local optimum, not a general
prompt pattern that can be safely expanded.

### v023/v024 - no-stop continuation and pause

Package:

```text
/home/williambenitez1/Capstone\_worktrees/1.2\_feat\_\_qwen3-vl-8b-instruct\_\_two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human\_report\_challenge\_v2\_prompt\_iteration\_workflow/cycle\_001/main\_promotion/v017b\_prompt\_only\_main\_promotion/v023\_literal99\_qwen\_no\_stop\_continuation/
```

Pause report:

```text
pause\_report\_2026-05-06.md
```

What happened:

* Replayed `v020c`.
* Ran `v023a` through `v023z`.
* Ran `v024a` through `v024n`.
* Started `v024o`, but it was paused before all-current completion.

Current champion:

```text
v020c\_anchor\_replay: 186 / 33 / 25, 58 total errors
```

Best challenger:

```text
v024l\_v023s\_no\_wheel\_track\_ablation: 188 / 31 / 35, 66 total errors
```

Important v024 lessons:

* `v024l` proves there is a high-recall branch, but it is still FP-heavy.
* `silhouette` and `exterior wall/roof boundary` were load-bearing in the
v023s branch. Removing either collapsed dense case `67`.
* Removing `wheel/track contact` created the best challenger, but still did not
fix false positives.
* Long building-only de-tiling prompt sections are dangerous. `v024n` exploded
to `102` false positives.

## What Has Worked

### Sequential author-run-diagnose loops

The best progress came when Codex authored one candidate, ran it, diagnosed the
metrics and failure slices, wrote a diagnosis note, then used that diagnosis to
shape the next prompt. This prevented blind batch generation.

### Compact recall-friendly prompt style

The upstream prompt performed well partly because it was short and permissive.
Qwen-family grounding examples also tend to favor direct JSON/bbox grounding
instructions over very long negative-rule blocks.

### Targeted extra-box audit

`v020c` worked because it kept enough recall while adding a final audit against
unsupported extra boxes. It emphasized visible connected target bodies, tighter
single-target boxes, and rejecting boxes supported mainly by context such as
smoke, debris, terrain, shadows, or broad groups.

### OpenAI-compatible upstream-code path

The current comparison standard is the fetched upstream/main OpenAI-compatible
runtime path controlled by `OPENAI\_BASE\_URL`. This better matches how the
upstream project expects VLM calls to run than the old direct Ollama path.

Relevant endpoint conventions:

```text
preferred: http://localhost:8000/v1
fallback used in recent cycles: http://localhost:11434/v1
Qwen model: qwen3-vl:8b-instruct
upstream config model name: Qwen/Qwen3-VL-8B-Instruct
```

When using Ollama's `/v1` endpoint, reports must label it as
OpenAI-compatible Ollama.

### Control gates

The cycles became much safer when every row had to preserve:

* case `155`
* case `166`
* office-negative abstention
* valid JSON/runtime behavior
* no case `101` in active no101 manifests

### Source-verified memory and recall

Graphify/project-brain worked well as a navigation layer. It helped recover
the current state after crashes/restarts, but every important claim still had
to be verified against source artifacts.

## What Has Not Worked

### Long prompt bloat

Longer prompts with many defensive rules often made the model worse. They
increased instruction burden, reduced ordinary recall, or caused the model to
mis-handle dense rows.

### Broad building-only prompt rules

Attempts to add long building-specific de-tiling or intact-building exclusion
rules were especially risky. `v024n\_v024l\_building\_only\_detiling` reached
`102` false positives, a major FP explosion.

### Dense-case cleanup language

Many variants that tried to reduce duplicates or overlap collapsed case `67`.
This is the clearest sign that prompt-only wording is brittle around dense
formations.

### High-recall branches without FP control

`v023s` and `v024l` improved matches and false negatives but still carried too
many false positives. They are useful evidence, not adoption candidates.

### Assuming Qwen prompt behavior transfers to Gemma

The v021 matrix showed model-specific behavior matters. Qwen's `v020c` winner
did not transfer cleanly to Gemma because Gemma failed positive control `155`
with that prompt.

### Treating partial runs as evidence

`v024o` is the current warning here. It had partial predictions and
office-negative passed, but it did not finish all-current. It is not scored and
must not be used as an evaluated result.

## What Codex Has Struggled With

### Knowing when to stop prompt-only exploration

The user explicitly challenged Codex to keep going until perfect, interrupted,
or out of usage. Codex continued many iterations, but the results increasingly
showed a prompt-only plateau. The tension is between persistence and recognizing
that another prompt edit may be the wrong lever.

Deep Research should help define better plateau criteria and pivot policies
that still respect the user's desire for autonomous persistence.

### Balancing recall and precision in dense scenes

Qwen can find more targets with permissive wording, but precision deteriorates.
When wording tightens precision, dense case `67` often collapses. We need better
techniques for separating "duplicate/tiling false positives" from "legitimate
dense individual targets."

### Translating visual failure patterns into prompt changes

Many failures need visual interpretation. Metrics alone can say "case 67
collapsed" or "case 103 exploded," but the next prompt tactic requires knowing
whether the false positives are duplicate boxes, smoke/context boxes, building
pieces, broad group boxes, or off-target rows.

Codex has optional FiftyOne/visual-review tooling available but has not yet
made visual review the primary next lever after the plateau.

### Avoiding over-specific prompt repairs

When a candidate fails on one failure family, it is tempting to add a specific
rule. But long specific rule blocks can shift model behavior globally and cause
new failures. Deep Research should look for disciplined ways to use failure
taxonomies without bloating prompts.

### Tool use discipline

The workflow uses many tools and memory layers. The challenge is using them in
the right order:

1. Source artifacts first.
2. Graphify/project-brain for navigation.
3. Mem0 for durable advisory lessons only.
4. Visual review when metrics are insufficient.
5. Web/official docs only when a prompt tactic needs outside grounding.

## Tools, MCPs, And Memory Lanes Used

### Local repo and worktrees

Main checkout:

```text
/home/williambenitez1/Capstone
```

Qwen `1.2` worktree:

```text
/home/williambenitez1/Capstone\_worktrees/1.2\_feat\_\_qwen3-vl-8b-instruct\_\_two-pass-refinement
```

Gemma `3.1` worktree:

```text
/home/williambenitez1/Capstone\_worktrees/3.1\_feat\_\_gemma4-e4b\_\_qwen-v009-workflow-bootstrap
```

Useful live docs:

```text
z\_reference\_docs/WORKING\_CHANGELOG.md
z\_reference\_docs/PROMPT\_DEVELOPMENT\_METHODOLOGY.md
z\_reference\_docs/PROMPT\_CRAFTING\_INSTRUCTIONAL\_GUIDE.md
z\_reference\_docs/PROJECT\_BRAIN.md
z\_reference\_docs/Prompt\_Labs/PROMPT\_LABS\_INDEX.md
```

### Prompt-lab runners and artifacts

Recent cycle packages:

```text
.../upstream\_v017b\_amalgamation\_cycle/
.../v019\_v018e\_creative\_followup\_cycle/
.../v020\_v019c\_goal\_driven\_self\_improvement\_cycle/
.../v021\_openai\_compat\_cross\_model\_prompt\_matrix/
.../v022\_literal99\_qwen\_recursive\_prompt\_refinement\_cycle/
.../v023\_literal99\_qwen\_no\_stop\_continuation/
```

Common artifact types:

```text
candidate\_registry.json
comparison\_matrix.json
comparison\_matrix.md
diagnoses/<candidate>\_diagnosis.md
final\_recommendation.md
recovery\_log.md
research\_notes.md
runs/<candidate>/<pack>/...
source\_manifest.json
```

### Graphify/project-brain

Entry document:

```text
z\_reference\_docs/PROJECT\_BRAIN.md
```

Project-brain command:

```bash
/home/williambenitez1/Capstone/.graphify\_project\_brain/capstone\_graphify.py recall "v023 v024 refresh checkpoint current state v020c v024o"
```

Refresh and validation commands:

```bash
/home/williambenitez1/Capstone/.graphify\_project\_brain/capstone\_graphify.py update
/home/williambenitez1/Capstone/.graphify\_project\_brain/capstone\_graphify.py doctor --strict-stale
/home/williambenitez1/Capstone/.graphify\_project\_brain/capstone\_graphify.py recall-benchmark
/home/williambenitez1/Capstone/.graphify\_project\_brain/capstone\_graphify.py verify-memory --strict --json
```

Graphify is a navigation and recall layer, not source truth. It has source
verified notes and semantic seeds that point back to source artifacts.

### Mem0

Mem0 is durable advisory memory. It is not source truth.

It was used to store concise lessons such as:

* v020c remains incumbent.
* v024l is high-recall but FP-heavy.
* v024o is interrupted/unscored.
* case `67` is brittle.
* long building-only prompt rules can cause FP tiling.
* next axis should favor visual review plus non-prompt duplicate/tiling
suppression or backend/post-processing.

Mem0 writes require explicit user approval.

### SequentialThinking

SequentialThinking is used as a compact planning checkpoint for risky or
branchy work. It is not evidence and does not replace source inspection or eval
artifacts.

### Web and official-doc research

Research has been used selectively, especially around Qwen-family grounding
behavior. The useful lesson so far is that Qwen grounding examples tend to be
short, direct, and JSON/bbox oriented. This helped motivate compact prompt
variants, but local evaluation still decides.

### FiftyOne visual review path

FiftyOne is available as a local visual dataset review aid for BDA image cases,
predicted/reference bounding boxes, and failure slices. It should not replace
eval artifacts or source truth. It is a likely next tool for examining the
remaining `v020c` FP/FN slices and `v024l` high-recall false positives.

## Recommended Deep Research Themes

Ask Deep Research to investigate the following, with concrete recommendations
and citations:

1. How to design recursive prompt-improvement loops for VLM object localization
without overfitting to local validation cases.
2. How to balance recall and precision for dense object detection when prompts
are the only immediate lever.
3. How to detect when prompt-only search has plateaued and a non-prompt lever
should take over.
4. How to combine metric-driven evaluation with visual failure review in a
repeatable agent workflow.
5. How to use failure taxonomies without causing prompt bloat.
6. How to structure candidate generation so each candidate tests one clear
hypothesis.
7. How to use model-specific prompt patterns for Qwen3-VL-style grounding.
8. How to compare cross-model transferability without assuming prompt behavior
transfers from Qwen to Gemma.
9. How to add lightweight post-processing or duplicate/tiling suppression while
preserving dense-row recall.
10. What additional tools could help Codex: visual analytics, experiment
tracking, prompt diffing, bbox clustering diagnostics, active learning,
dataset slicing, or automated visual review.

## Specific Questions For ChatGPT 5.5 Pro To Answer Before Deep Research

1. Does the current evidence support stopping prompt-only search and pivoting to
non-prompt duplicate/tiling suppression?
2. If prompt-only search continues, what is the most disciplined next candidate
strategy from `v020c` or `v024l`?
3. What failure taxonomy should Codex use before authoring each new candidate?
4. Which slices should receive visual review first?
5. How should the recursive loop decide whether a lesson is local noise,
general signal, or source-truth conflict?
6. How should Codex use Graphify, Mem0, SequentialThinking, web research, and
FiftyOne without blurring navigation memory into evidence?
7. What should be added to the evaluation protocol to prevent overfitting to
dense case `67` while still respecting it as a sentinel?
8. What should the Deep Research prompt ask for that a normal coding agent
might miss?

## Desired Deep Research Output

The Deep Research output should give Codex an actionable improvement package,
not just generic prompt-engineering advice.

Preferred output structure:

1. Diagnosis of the current methodology.
2. Risks and blind spots.
3. Recommended recursive prompt-improvement protocol.
4. Candidate generation patterns for VLM detection prompts.
5. Visual-review protocol for FP/FN slices.
6. Plateau and pivot rules.
7. Tooling recommendations using existing tools first.
8. Optional new tool recommendations, with low-risk setup ideas.
9. Concrete next 3-5 experiments for this project.
10. A compact checklist Codex can apply before each new candidate.

## Important Source Artifacts To Inspect

Core live docs:

```text
/home/williambenitez1/Capstone/z\_reference\_docs/WORKING\_CHANGELOG.md
/home/williambenitez1/Capstone/z\_reference\_docs/PROMPT\_DEVELOPMENT\_METHODOLOGY.md
/home/williambenitez1/Capstone/z\_reference\_docs/PROJECT\_BRAIN.md
/home/williambenitez1/Capstone/z\_reference\_docs/Prompt\_Labs/PROMPT\_LABS\_INDEX.md
```

Current pause report:

```text
/home/williambenitez1/Capstone\_worktrees/1.2\_feat\_\_qwen3-vl-8b-instruct\_\_two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human\_report\_challenge\_v2\_prompt\_iteration\_workflow/cycle\_001/main\_promotion/v017b\_prompt\_only\_main\_promotion/v023\_literal99\_qwen\_no\_stop\_continuation/pause\_report\_2026-05-06.md
```

Recent final recommendations:

```text
.../upstream\_v017b\_amalgamation\_cycle/final\_recommendation.md
.../v019\_v018e\_creative\_followup\_cycle/final\_recommendation.md
.../v020\_v019c\_goal\_driven\_self\_improvement\_cycle/final\_recommendation.md
.../v021\_openai\_compat\_cross\_model\_prompt\_matrix/final\_recommendation.md
.../v022\_literal99\_qwen\_recursive\_prompt\_refinement\_cycle/final\_recommendation.md
.../v023\_literal99\_qwen\_no\_stop\_continuation/final\_recommendation.md
```

Current comparison matrices:

```text
.../v020\_v019c\_goal\_driven\_self\_improvement\_cycle/comparison\_matrix.md
.../v021\_openai\_compat\_cross\_model\_prompt\_matrix/cross\_model\_comparison\_matrix.md
.../v022\_literal99\_qwen\_recursive\_prompt\_refinement\_cycle/comparison\_matrix.md
.../v023\_literal99\_qwen\_no\_stop\_continuation/comparison\_matrix.md
```

Graphify recall command:

```bash
/home/williambenitez1/Capstone/.graphify\_project\_brain/capstone\_graphify.py recall "v023 v024 refresh checkpoint current state v020c v024o"
```

## Boundaries For The Collaboration

* Do not update `metalbladex4/bda-svc-staff-architect-review` yet. The user
will give explicit instructions later.
* Do not assume local-only prompt-lab artifacts are already product truth.
* Do not treat Graphify or Mem0 as authoritative evidence.
* Do not use partial `v024o` outputs as metrics.
* Do not recommend storing credential values in docs, prompts, memory, or tool
inventories.
* Do not recommend broad source-truth changes without a clear validation gate.
* Do not recommend adopting a prompt only because it improves recall. Positive
controls and false-positive burden matter.

## The Core Ask

Help us make Codex better at the process itself.

We are not merely asking for one more prompt. We are asking for a stronger
recursive improvement system where Codex can:

* inspect evidence,
* generate one candidate at a time,
* run the candidate,
* diagnose results,
* update its lessons,
* decide whether to continue, pivot, or escalate to visual/non-prompt tools,
* and use each loop to become better at the next loop.

The goal is still near perfection, but the current evidence says prompt-only
edits are plateauing. The best research contribution may be a better decision
system for when and how to move beyond prompt wording while preserving the
successful `v020c` behavior.

Citations · 21



•



1

bda\_svc\_qwen\_prompt\_engineering\_deep\_research\_bundle.md



bda\_svc\_qwen\_prompt\_engineering\_deep\_research\_bundle.md

raw.githubusercontent.com

raw.githubusercontent.com



2

https://raw.githubusercontent.com/metalbladex4/bda-svc-staff-architect-review/main/REVIEW\_REFRESH\_2026-05-06.md

https://raw.githubusercontent.com/metalbladex4/bda-svc-staff-architect-review/main/REVIEW\_REFRESH\_2026-05-06.md



3

https://raw.githubusercontent.com/metalbladex4/bda-svc-staff-architect-review/main/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human\_report\_challenge\_v2\_prompt\_iteration\_workflow/cycle\_001/main\_promotion/v017b\_prompt\_only\_main\_promotion/v023\_literal99\_qwen\_no\_stop\_continuation/pause\_report\_2026-05-06.md

https://raw.githubusercontent.com/metalbladex4/bda-svc-staff-architect-review/main/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human\_report\_challenge\_v2\_prompt\_iteration\_workflow/cycle\_001/main\_promotion/v017b\_prompt\_only\_main\_promotion/v023\_literal99\_qwen\_no\_stop\_continuation/pause\_report\_2026-05-06.md



12

https://raw.githubusercontent.com/metalbladex4/bda-svc-staff-architect-review/main/src/bda\_svc/pipeline/config.yaml

https://raw.githubusercontent.com/metalbladex4/bda-svc-staff-architect-review/main/src/bda\_svc/pipeline/config.yaml



21

https://raw.githubusercontent.com/metalbladex4/bda-svc-staff-architect-review/main/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human\_report\_challenge\_v2\_prompt\_iteration\_workflow/cycle\_001/main\_promotion/v017b\_prompt\_only\_main\_promotion/v023\_literal99\_qwen\_no\_stop\_continuation/final\_recommendation.md

https://raw.githubusercontent.com/metalbladex4/bda-svc-staff-architect-review/main/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human\_report\_challenge\_v2\_prompt\_iteration\_workflow/cycle\_001/main\_promotion/v017b\_prompt\_only\_main\_promotion/v023\_literal99\_qwen\_no\_stop\_continuation/final\_recommendation.md

qwenlm.github.io

qwenlm.github.io



4

https://qwenlm.github.io/blog/qwen2.5-vl/

https://qwenlm.github.io/blog/qwen2.5-vl/

developers.openai.com

developers.openai.com



5

https://developers.openai.com/api/docs/guides/evals

https://developers.openai.com/api/docs/guides/evals



10

https://developers.openai.com/blog/eval-skills

https://developers.openai.com/blog/eval-skills



16

https://developers.openai.com/codex/concepts/customization

https://developers.openai.com/codex/concepts/customization



17

https://developers.openai.com/learn/docs-mcp

https://developers.openai.com/learn/docs-mcp



19

https://developers.openai.com/api/docs/guides/evaluation-best-practices

https://developers.openai.com/api/docs/guides/evaluation-best-practices

arxiv.org

arxiv.org



6

https://arxiv.org/html/2504.09480v1

https://arxiv.org/html/2504.09480v1



7

https://arxiv.org/abs/2404.13013

https://arxiv.org/abs/2404.13013



8

https://arxiv.org/html/2603.23455v1

https://arxiv.org/html/2603.23455v1



9

https://arxiv.org/html/2503.12799v2

https://arxiv.org/html/2503.12799v2



11

Self-Refine: Iterative Refinement with Self-Feedback

https://arxiv.org/abs/2303.17651?utm\_source=chatgpt.com



14

https://arxiv.org/abs/2403.02325

https://arxiv.org/abs/2403.02325



15

https://arxiv.org/abs/2303.05499

https://arxiv.org/abs/2303.05499

docs.voxel51.com

docs.voxel51.com



13

https://docs.voxel51.com/getting\_started/object\_detection/04\_evaluating\_detections.html

https://docs.voxel51.com/getting\_started/object\_detection/04\_evaluating\_detections.html

github.com

github.com



18

https://github.com/qdrant/mcp-server-qdrant

https://github.com/qdrant/mcp-server-qdrant

docs.pytorch.org

docs.pytorch.org



20

https://docs.pytorch.org/vision/main/generated/torchvision.ops.nms.html

https://docs.pytorch.org/vision/main/generated/torchvision.ops.nms.html

Sources scanned · 237



huggingface.co

huggingface.co

Qwen/Qwen3-VL-8B-Instruct





Instructions to use Qwen/Qwen3-VL-8B-Instruct with libraries, inference providers, notebooks, and local apps. Follow these links to get started. · Install from ...Read more



Qwen/Qwen2.5-VL-3B-Instruct





5-VL can accurately localize objects in an image by generating bounding boxes or points, and it can provide stable JSON outputs for coordinates and attributes.Read more



Hugging Face MCP Server





The Hugging Face MCP Server includes several built-in tools that connect your AI assistant to the Hugging Face ecosystem. You can enable or disable each tool ...Read more



MCP Client





An MCPClient, designed to empower Large Language Models (LLMs) with the ability to interact with external Tools via the Model Context Protocol (MCP).Read more



Welcome to the 🤗 Model Context Protocol (MCP) Course





MCP Course documentation. Welcome to the Model Context ... Build a deployed MCP application using the Hugging Face ecosystem and partners' services.Read more



MCP Server Settings





The Hugging Face MCP Server provides seamless access to Hugging Face's vast ecosystem of Models, Datasets, Research Papers and state-of-the-art AI tools. This ...Read more



Building the Hugging Face MCP Server





Jul 10, 2025 — The Hugging Face Official MCP Server offers unique customization options for AI Assistants accessing the Hub, along with access to thousands of AI applications ...Read more



Documentation





Explore demos, models, and datasets for any ML tasks. Dataset viewer API for metadata, stats, and content of HF Hub datasets.Read more



Ultralytics





At Ultralytics, we are dedicated to creating the best artificial intelligence models in the world. Our open source works offer cutting-edge solutions.Read more



Daily Papers





Large vision language models (LVLMs) often suffer from object hallucination, producing objects not present in the given images. While current benchmarks for ...Read more



docs.voxel51.com

docs.voxel51.com

FiftyOne Brain — FiftyOne 1.15.0 documentation





The FiftyOne Brain provides powerful machine learning techniques that are designed to transform how you curate your data from an art into a measurable science.Read more



Step 4: Evaluating Detections — FiftyOne 1.14.2 documentation





This step demonstrates how to use FiftyOne to perform hands-on evaluation of your detection model. It covers the following concepts: Evaluating your model using ...Read more



fiftyone.brain.similarity





Base class for similarity factories. Methods: Initializes a similarity index. Gets the fields that were involved in the given run. Cleans up the results of the ...Read more



Understanding and Using Embeddings - FiftyOne - Voxel51





Embeddings play a crucial role in image search, clustering, anomaly detection, and representation learning. In this notebook, we will learn how to generate, ...Read more



fiftyone.brain — FiftyOne 1.15.0 documentation





The brains behind FiftyOne: a powerful package for dataset curation, analysis, and visualization. See https://github.com/voxel51/fiftyone for more information.Read more



Evaluating Object Detections with FiftyOne





This walkthrough demonstrates how to use FiftyOne to perform hands-on evaluation of your detection model.Read more



developers.openai.com

developers.openai.com

Customization – Codex





Skills plus MCP is where it all comes together: skills define repeatable workflows, and MCP connects them to external tools and systems. If a skill depends on ...Read more



Agent Skills – Codex | OpenAI Developers





Use agent skills to extend Codex with task-specific capabilities. A skill packages instructions, resources, and optional scripts so Codex can follow a ...Read more



Config basics – Codex





Configure approval policies and sandbox settings. Configure MCP servers. Configuration precedence. Codex resolves values in this order (highest precedence first):.Read more



Evaluation best practices | OpenAI API





Learn best practices for designing evals to test and improve model performance in production.



Docs MCP





OpenAI hosts a public Model Context Protocol (MCP) server for developer documentation on developers.openai.com and platform.openai.com.Read more



Evals





Best practices for designing and running evals. guide. Getting Started with Evals.Read more



Model Context Protocol – Codex





Model Context Protocol (MCP) connects models to tools and context. Use it to give Codex access to third-party documentation, or to let it interact with ...Read more



Building MCP servers for ChatGPT Apps and API integrations





In this guide, we'll cover how to build a remote MCP server that reads data from a private data source (a vector store) and makes it available in ChatGPT as a ...Read more



MCP and Connectors | OpenAI API





This guide will show how to use both remote MCP servers and connectors to give the model access to new capabilities. Quickstart. Check out the examples below to ...Read more



Using skills to accelerate OSS maintenance





Mar 9, 2026 — The Codex customization docs describe skills as a way to give Codex richer instructions, scripts, and references for repeatable workflows ...Read more



Working with evals | OpenAI API





Describe the task to be done as an eval · Run your eval with test inputs (a prompt and input data) · Analyze the results, then iterate and improve on your prompt.Read more



Configuration Reference – Codex





Use this page as a searchable reference for Codex configuration files. For conceptual guidance and examples, start with Config basics and Advanced Config.Read more



Subagents – Codex





You can also include other supported config.toml keys in a custom agent file, such as model , model\_reasoning\_effort , sandbox\_mode , mcp\_servers , and skills.Read more



Testing Agent Skills Systematically with Evals





Jan 22, 2026 — 1. Define success before you write the skill · 2. Create the skill · 3. Manually trigger the skill to expose hidden assumptions · 4. Use a small, ...Read more



Advanced Configuration – Codex





Use these options when you need more control over providers, policies, and integrations. For a quick start, see Config basics.Read more



OpenAI API Platform Documentation





Explore guides, API docs, and examples for the OpenAI API ... Docs MCP. Categories. Demo apps · Videos. Topics. Agents · Audio \& Voice · Computer ...Read more



Use Codex with the Agents SDK





Start by turning Codex CLI into an MCP server that the Agents SDK can call. The server exposes two tools ( codex() to start a conversation and codex-reply() to ...Read more



Codex App Server





Supported item types include config, skills, AGENTS.md , plugins, MCP server config, subagents, hooks, commands, and sessions; plugin imports emit ...Read more



MCP – Apps SDK





What is MCP? The Model Context Protocol (MCP) is an open specification for connecting large language model clients to external tools and resources.Read more



OpenAI for Developers in 2025





Dec 30, 2025 — At the same time, support for AGENTS.md and MCP made Codex easier to adapt to your repo, extend with third-party tools and context, and even ...Read more



Reasoning best practices | OpenAI API





When to use our reasoning models · 1. Navigating ambiguous tasks · 2. Finding a needle in a haystack · 3. Finding relationships and nuance across a large dataset.Read more



Codex CLI





Codex CLI is OpenAI's coding agent that you can run locally from your terminal. It can read, change, and run code on your machine in the selected directory.Read more



Build your MCP server – Apps SDK





By the end of this guide, you'll know how to connect your backend MCP server to ChatGPT, define tools, register UI templates, and tie everything together ...Read more



arxiv.org

arxiv.org

Prompt Sensitivity in Vision-Language Grounding: How Small Changes in Wording Affect Object Detection





by DJ Deka · 2026 — Vision-language models enable open-vocabulary object grounding through natural language queries, under the implicit assumption that semantically ...Read more



Prompt Sensitivity in Vision-Language Grounding





Apr 18, 2026 — Vision-language models enable open-vocabulary object grounding through natural language queries, under the implicit assumption that ...Read more



\[2502.13923] Qwen2.5-VL Technical Report





by S Bai · 2025 · Cited by 6039 — A standout feature of Qwen2.5-VL is its ability to localize objects using bounding boxes or points accurately. It provides robust structured ...Read more



A Benchmark for Evaluating Object Hallucination in Large ...





Dec 29, 2024 — In this work, we introduce Hallucinogen, a novel benchmark for evaluating object hallucination in Large Vision-Language Models (LVLMs).Read more



Grounding Everything in Tokens for Multimodal Large ...





Apr 2, 2026 — Multimodal large language models (MLLMs) have made significant advancements in vision understanding and reasoning.Read more



Self-Refine: Iterative Refinement with Self-Feedback





https://arxiv.org/abs/2303.17651



Reflexion: Language Agents with Verbal Reinforcement Learning





by N Shinn · 2023 · Cited by 4621 — We propose Reflexion, a novel framework to reinforce language agents not by updating weights, but instead through linguistic feedback.Read more



When Text Hijacks Vision: Benchmarking and Mitigating ...





Apr 19, 2026 — 2024. Mitigating object hallucinations in large vision-language models through visual contrastive decoding. In Proceedings of the IEEE/CVF ...Read more



Towards Visual Text Grounding of Multimodal Large ...





Sep 23, 2025 — For text-rich document images, we mainly focus on the visual texts on them as the main grounding target. Considering the supreme performance of ...Read more



arXiv:2303.17651v2 \[cs.CL] 25 May 2023





by A Madaan · 2023 · Cited by 4000 — We present SELF-REFINE: a novel approach that allows large language models to iteratively provide self-feedback and refine their own outputs.Read more



Reflexion: Language Agents with Verbal Reinforcement ...





by N Shinn · 2023 · Cited by 4621 — In this paper, we propose an alternative approach called Reflexion that uses verbal reinforcement to help agents learn from prior failings.Read more



LLM-as-Judge Framework for Evaluating Tone-Induced ...





Apr 20, 2026 — Vision-Language Models (VLMs) are increasingly deployed in settings where reliable visual grounding carries operational consequences, yet their ...Read more



Grounding Multimodal LLMs to Embodied Agents that Ask ...





Oct 1, 2025 — To address this challenge, we propose a novel approach that fine-tunes multi-modal large language models (MLLMs) as vision-language-action (VLA) ...Read more



A Stitch in Time Saves Nine: Proactive Self-Refinement for ...





Aug 18, 2025 — We propose PASR, a novel method that enables large language models to proactively self-refine their responses during generation. ... Self-refine: ...Read more



One STEP at a time: Language Agents are Stepwise ...





Nov 13, 2024 — Rather than relying on traditional reinforcement learning methods that update model parameters, Reflexion enhances agents through verbal ...Read more



Mitigating Object Hallucination in Large Vision-Language ...





by L Zhao · 2024 · Cited by 24 — MARINE effectively and efficiently reduces object hallucinations during inference by introducing image-grounded guidance to LVLMs.Read more



A Holistic Benchmark for Multi-level Visual Grounding in ...





We assess a range of state‐of‐the‐art 3D visual grounding methods alongside large language models (LLMs) and multimodal LLMs (MLLMs) on Anywhere3D-Bench.Read more



Meta-RL Induces Exploration in Language Agents





Mar 8, 2026 — In this paper, we present LaMer, a general Meta-RL framework ... Yao (2023) Reflexion: language agents with verbal reinforcement learning.Read more



Multi-Object Hallucination in Vision-Language Models





Jul 8, 2024 — This work systematically investigates multi-object hallucination, examining how models misperceive (eg, invent nonexistent objects or become distracted)Read more



LENS: Multi-level Evaluation of Multimodal Reasoning with ...





May 21, 2025 — Contextual object detection with multimodal large language models. International Journal of Computer Vision, 133(2):825–843, 2025. \[13]Read more



Self Iterative Label Refinement via Robust Unlabeled ...





Feb 18, 2025 — We introduce an iterative refinement pipeline that employs the Unlabeled-Unlabeled learning framework to improve LLM-generated pseudo-labels for classification ...Read more



ReAct Meets ActRe: When Language Agents Enjoy ...





Reflexion: language agents with verbal reinforcement learning. In Thirty-seventh Conference on Neural Information Processing Systems, 2023. URL https ...Read more



Contextual Object Detection with Multimodal Large ...





Aug 12, 2024 — In this paper, we study a new research problem—contextual object detection—that is understanding visible objects within human-AI interactive ...Read more



Vision-Language Model for Object Detection and ...





Apr 13, 2025 — In this work, we present the systematic review of VLM-based detection and segmentation, view VLM as the foundational model and conduct comprehensive ...Read more



Grounding Multimodal Large Language Models in Actions





by A Szot · 2024 · Cited by 41 — In this work, we study how to best ground a MLLM into different embodiments and their associated action spaces, with the goal of leveraging the multimodal ...Read more



Object Detection with Multimodal Large Vision-Language Models: An In-depth Review





https://arxiv.org/abs/2508.19294



Think, Act, Build: An Agentic Framework with Vision ...





Apr 1, 2026 — 3D Visual Grounding (3D-VG) aims to localize objects in 3D scenes via natural language descriptions. While recent advancements leveraging ...Read more



BoxTuning: Directly Injecting the Object Box for Multimodal ...





Apr 13, 2026 — We propose BoxTuning, which resolves this mismatch by injecting object spatial-temporal information directly into the visual modality. Colored ...Read more



Object Detection with Multimodal Large Vision-Language ...





This in-depth review presents a structured exploration of the state-of-the-art in LVLMs, systematically organized through a three-step research review process.Read more



N3D-VLM: Native 3D Grounding Enables Accurate Spatial ...





Dec 18, 2025 — To this end, we propose N3D-VLM, a unified vision-language model that integrates 3D detection, grounding, and CoT reasoning. The model is ...Read more



SPARROW : Learning Spatial Precision and Temporal ...





Mar 12, 2026 — Groma: Localized visual tokenization for grounding multimodal large language models. In Computer Vision – ECCV 2024, pages 417–435, Cham ...Read more



DetPO: In-Context Learning with Multi-Modal LLMs for Few ...





Mar 24, 2026 — Multi-Modal LLMs (MLLMs) demonstrate strong visual grounding capabilities on popular object detection benchmarks like OdinW-13 and RefCOCO.Read more



GIST: Multimodal Knowledge Extraction and Spatial ...





Apr 16, 2026 — We present GIST (Grounded Intelligent Semantic Topology), a multimodal knowledge extraction pipeline that transforms a consumer-grade mobile ...Read more



Multimodal Large Language Models for MUlti-Subject In ...





Apr 8, 2026 — We propose MUSIC, the first MLLM designed for multi-subject in-context image generation, integrating vision reasoning capabilities for multi- ...Read more



Reasoning-Guided Grounding: Elevating Video Anomaly ...





Apr 7, 2026 — While Vision-Language Models (VLMs) offer rich scene understanding, they struggle with reliable spatial grounding—often producing ...Read more



arXiv:2503.10596v2 \[cs.CV] 21 Apr 2025





by R Hu · 2025 · Cited by 6 — Specifically, GSEval-BBox is designed to evaluate the vi- sual grounding capabilities of multimodal large language models. GSEval-BBox converts ...Read more



ADAPTIVE GUIDANCE SEMANTICALLY ENHANCED VIA ...





Sep 24, 2025 — Multimodal Large Language Model (MLLM) demonstrates potential for open-word detection and contextual reasoning by integrating visual and ...Read more



Groma: Localized Visual Tokenization for Grounding Multimodal Large Language Models





https://arxiv.org/abs/2404.13013



Thinking With Bounding Boxes: Enhancing Spatio ...





Nov 26, 2025 — We propose STVG-o1, the first framework that enables off-the-shelf multimodal large language models (MLLMs) to perform spatio-temporal video ...Read more



Groma: Localized Visual Tokenization for Grounding ...





Groma is a multimodal large language model with exceptional region understanding and visual grounding capabilities.Read more



BBox-DocVQA: A Large-Scale Bounding-Box–Grounded ...





Nov 19, 2025 — To address this gap, we introduce BBox-DocVQA—a large-scale, bounding-box–grounded dataset designed to enhance spatial reasoning and evidence ...Read more



arXiv:2404.13013v1 \[cs.CV] 19 Apr 2024





by C Ma · 2024 · Cited by 149 — We introduce Groma, a Multimodal Large Language Model. (MLLM) with grounded and fine-grained visual perception ability. Be- yond holistic image ...Read more



MedMO: Grounding and Understanding Multimodal Large ...





Feb 6, 2026 — These models unify vision and language comprehension, achieving near-human performance on tasks such as image captioning, visual question ...Read more



GLaMM: Pixel Grounding Large Multimodal Model





In this work, we present Grounding LMM (GLaMM), the first model that can generate natural language responses seamlessly intertwined with corresponding object ...Read more



RefChartQA: Grounding Visual Answer on Chart Images ...





Mar 29, 2025 — We propose an instruction-tuning strategy that adapts multimodal large language models (LLMs) to simultaneously handle question-answering and ...Read more



Multi-Turn Approach to GUI Grounding with Visual Feedback





Apr 14, 2026 — Early work such as SeeClick demonstrates that large multimodal models can ground instructions to UI targets across heterogeneous screens Cheng ...Read more



Towards Understanding Visual Grounding in Vision ...





Sep 12, 2025 — Groma: Localized visual tokenization for grounding multimodal large language models. In European Conference on Computer Vision, pages 417 ...Read more



Improving Grounding in Vision-Language Models without ...





Mar 4, 2024 — We introduce Contrastive Region Guidance (CRG), a training-free guidance method that enables open-source VLMs to respond to visual prompts.Read more



Contrastive Region Guidance: Improving Grounding in Vision-Language Models without Training





https://arxiv.org/abs/2403.02325



Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection





https://arxiv.org/abs/2303.05499



Mitigating Object Hallucinations in Large Vision-Language ...





by S Leng · 2023 · Cited by 682 — We introduce Visual Contrastive Decoding (VCD), a simple and training-free method that contrasts output distributions derived from original and distorted ...Read more



Grounding DINO 1.5: Advance the "Edge" of Open-Set Object Detection





https://arxiv.org/abs/2405.10300



An Open and Comprehensive Pipeline for Unified Object ...





by X Zhao · 2024 · Cited by 90 — Grounding-DINO is a state-of-the-art open-set detection model that tackles multiple vision tasks including Open-Vocabulary Detection (OVD), ...Read more



Delve into Visual Contrastive Decoding for Hallucination ...





Dec 9, 2024 — In this paper, we delve into visual contrastive decoding with various visually changed samples to mitigate hallucinations for large vision- ...Read more



Bootstrapping Grounded Chain-of-Thought in Multimodal ...





Jul 3, 2025 — Our idea is to inject grounding information, i.e., bounding boxes, into CoT, which allows the model to perform self-verification, thereby ...



Roboflow100-VL: A Multi-Domain Object Detection ...





These (often multi-modal) labeling instructions provide rich contextual information not provided by class names alone. We argue that aligning foundation ...Read more



Grounded Chain-of-Thought for Multimodal Large ...





Mar 24, 2025 — In this paper, we propose a new learning task for multimodal large langauge models (MLLMs) termed grounded chain-of-thought (GCoT). GCoT aims to ...



Point What You Mean: Visually Grounded Instruction Policy





Mar 24, 2026 — In this study, we introduce the Point-VLA, a plug-and-play policy that augments language instructions with explicit visual cues (e.g., bounding ...Read more



Large Multimodal Models as General In-Context Classifiers





by M Garosi · 2026 — Thus, this finding prompts a fundamental question: are LMMs worse than VLMs at classification, or are they not properly conditioned for the task ...Read more



Visual Grounding Methods for Efficient Interaction with ...





Jul 18, 2025 — We propose two main methods: (1) IVGocr, which combines a Large Language Model (LLM), an object detection model, and an Optical Character ...Read more



FewMMBench: A Benchmark for Multimodal Few-Shot ...





Feb 25, 2026 — In this paper, we introduce FewMMBench, a comprehensive benchmark designed to evaluate MLLMs under few-shot conditions, with a focus on In- ...Read more



VGR: Visual Grounded Reasoning





Jun 13, 2025 — This paper introduces VGR, a novel reasoning multimodal large language model (MLLM) with enhanced fine-grained visual perception capabilities.



User Prompting Strategies and Prompt Enhancement ...





Jan 30, 2026 — Advancing the understanding and evaluation of AR-generated scenes: When vision-language models shine and stumble. In 2025 IEEE Conference on ...Read more



RynnEC: Bringing MLLMs into Embodied World





Aug 19, 2025 — We categorize embodied cognitive abilities into two essential components: object cognition and spatial cognition. Object cognition necessitates ...Read more



GRIT: Teaching MLLMs to Think with Images





May 21, 2025 — Our GRIT method enables MLLMs to perform grounded reasoning with only 20 training samples, realizing a clear and reliable process of thinking with images.



Weighted boxes fusion: Ensembling boxes from different object detection models





https://arxiv.org/abs/1910.13302



A Study on Real-time Object Detection using Deep Learning





Feb 17, 2026 — Post-processing techniques, such as Non-Maximum Suppression (NMS), filter overlapping predictions, ensuring only the most confident detections ...Read more



Confidence Aware SSD Ensemble with Weighted Boxes Fusion for Weapon Detection





https://arxiv.org/abs/2509.23697



Open World Object Detection: A Survey





Oct 15, 2024 — This survey paper offers a thorough review of the OWOD domain, covering essential aspects, including problem definitions, benchmark datasets, source codes, ...Read more



Semi-Supervised Object Detection: A Survey on Progress ...





Jul 16, 2024 — By utilizing non maximum suppression \[106] to combine detection outcomes from different iterations and employing multiple detection heads to ...Read more



Confidence‑Aware SSD Ensemble with Weighted Boxes ...





by A Jadhav · 2025 — The predictions from these models are combined using the Weighted. Boxes Fusion (WBF) method, an ensemble technique designed to optimize bounding box accuracy.Read more



YOLOv1 to YOLOv11: A Comprehensive Survey of Real- ...





Aug 4, 2025 — NMS-Free and End-to-End Architectures: YOLOv10 has initiated a shift toward eliminating non-maximum suppression via consistent assignment ...Read more



Accelerating Non-Maximum Suppression:A Graph Theory ...





This paper systematically analyzes NMS from a graph theory perspective for the first time, revealing its intrinsic structure.Read more



Generate, but Verify: Reducing Hallucination in Vision- ...





May 29, 2025 — The Polling-based Object Probing Evaluation (POPE) \[29] is a benchmark designed to assess object hallucination in vision-language models (VLMs).Read more



Evolving LLMs' Self-Refinement Capability via Iterative ...





We propose EVOLVE, a novel post-training and inference framework that iteratively integrates preference training with self-refinement-driven data collection.Read more



Meta-Policy Reflexion: Reusable Reflective Memory and ...





Sep 4, 2025 — Reflexion introduces verbal reinforcement learning, where agents use textual self-reflection to refine behavior without fine-tuning \[6] . ReAct ...Read more



Mitigating Object Hallucinations in Large Vision-Language ...





Mar 24, 2026 — We propose Dynamic Attention Calibration (DAC), a lightweight, learnable, and plug-and-play module that dynamically adjusts vision token ...Read more



MiMo-Embodied: X-Embodied Foundation Model ...





Nov 20, 2025 — It covers the following five task categories: (1) Visual Captioning: generating contextual descriptions of scenes and objects; (2) Visual ...Read more



Socratic Self-Refine for Large Language Model Reasoning





In this paper, we propose Socratic Self-Refine (SSR), a novel framework for fine-grained evaluation and precise refinement of LLM reasoning. Our proposed SSR ...Read more



QLASS: Boosting Language Agent Inference via Q-Guided ...





Feb 4, 2025 — Reflexion: language agents with verbal reinforcement learning. In Thirty-seventh Conference on Neural Information Processing Systems, 2023 ...Read more



Unveiling Hallucination in Text, Image, Video, and Audio ...





May 20, 2024 — This survey paper presents a comprehensive overview of recent developments that aim to identify and mitigate the problem of hallucination in FMs.Read more



Grasp Any Region: Towards Precise, Contextual Pixel ...





Mar 5, 2026 — While Multimodal Large Language Models (MLLMs) excel at holistic understanding, they struggle in capturing the dense world with complex scenes, ...Read more



ARIES: Stimulating Self-Refinement of Large Language ...





Feb 8, 2025 — In this paper, we explore how to cultivate LLMs with the self-refinement capability through iterative preference training, and how this ability can be ...Read more



Language Agent Meets Offline Reinforcement Learning Critic





In this paper, we implement RL Critic with a lightweight neural network, thus providing little inference overhead compared to using only LLMs for action ...Read more



Mitigating Hallucinations in Large Vision-Language ...





Oct 17, 2024 — Through experiments, we demonstrate that SGD achieves state-of-the-art performance on object hallucination benchmarks. Furthermore, in terms ...Read more



MARS2 2025 Challenge on Multimodal Reasoning





Sep 17, 2025 — Track #1 Visual Grounding in Real-world Scenarios (VG-RS) evaluates the model's scene perception, object localization, and spatial reasoning ...Read more



Self-Critique and Refinement for Faithful Natural Language ...





by Y Wang · 2025 · Cited by 5 — We introduce Self-critique and Refinement for Natural Language Explanations (SR-NLE), a framework that enables models to improve the faithfulness of their own ...Read m...



Retrospective Large Language Agents with Policy Gradient ...





This paper introduces a principled framework for reinforcing large language agents by learning ... Reflexion: Language agents with verbal reinforcement learning.Read more



Towards Mitigating Hallucinations in Large Vision- ...





Nov 7, 2025 — This subset probes whether models falsely affirm the presence of common yet incorrect objects, revealing object-level hallucinations driven by ...Read more



\[2508.06585] CountQA: How Well Do MLLMs Count in the Wild?





Our dataset features scenes with high object density, significant visual clutter, occlusion, and unusual objects not typically found in standard counting ...



Small Language Models Need Strong Verifiers to Self ...





We decompose the task of self-correction into two phases: (Self-)Verify and Self-Refine. The LM first generates an initial solution for a reasoning question. A ...Read more



Causal Reflection with Language Models





Sep 25, 2025 — While Reflexion improves agent behavior through verbal reinforcement and meta-cognitive feedback, its reflection process remains heuristic and ...Read more



github.com

github.com

Qwen3-VL is the multimodal large language model ...





Meet Qwen3-VL — the most powerful vision-language model in the Qwen series to date. This generation delivers comprehensive upgrades across the board: ...Read more



SKILL.md - OpenAI Docs





Use when the user asks how to build with OpenAI products or APIs and needs up-to-date official documentation with citations, help choosing the latest model for ...Read more



NishilBalar/Awesome-LVLM-Hallucination





This repository will provide an organized list of state-of-the-art research papers, relevant code, and a brief description related to hallucinations of the ...Read more



VCD: Mitigating Object Hallucinations in Large Vision- ...





This is the official repo for Visual Contrastive Decoding, a simple, training-free method for mitigating hallucinations in LVLMs during decoding without ...Read more



IDEA-Research/GroundingDINO: \[ECCV 2024] Official ...





\[ECCV 2024] Official implementation of the paper "Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection" ...



An official Qdrant Model Context Protocol (MCP) server ...





This repository is an example of how to create a MCP server for Qdrant, a vector search engine. Overview. An official Model Context Protocol server for keeping ...Read more



GitHub - qdrant/qdrant: Qdrant - High-performance ...





Qdrant (read: quadrant) is a vector similarity search engine and vector database. It provides a production-ready service with a convenient API to store, search ...Read more



Releases · qdrant/mcp-server-qdrant





This release introduces major changes to the architecture and the usage patterns of the server. Features. #39 - the server is now represented by a class ...Read more



Context7 Platform - Up-to-date Code Docs For Any Prompt





Context7 fetches up-to-date code examples and documentation right into your LLM's context. No tab-switching, no hallucinated APIs that don't exist, no outdated ...



Issues · qdrant/mcp-server-qdrant





An official Qdrant Model Context Protocol (MCP) server implementation - Issues · qdrant/mcp-server-qdrant. ... Status: Open. #130 In qdrant/mcp-server-qdrant;. · ...Read more



Releases · qdrant/mcp-for-docs





MCP server for accessing documentation and code snippets of dev tools. Based on `mcp-server-qdrant` - Releases · qdrant/mcp-for-docs.



Hugging Face Official MCP Server





Welcome to the official Hugging Face MCP Server . Connect your LLM to the Hugging Face Hub and thousands of Gradio AI Applications. Installing the MCP Server.Read more



Pull requests · qdrant/mcp-server- ...





An official Qdrant Model Context Protocol (MCP) server implementation - Pull requests · qdrant/mcp-server-qdrant.



qdrant mcp-server-qdrant · Discussions





Explore the GitHub Discussions forum for qdrant mcp-server-qdrant. Discuss code, ask questions \& collaborate with the developer community.



Ultralytics YOLO





Ultralytics creates cutting-edge, state-of-the-art (SOTA) YOLO models built on years of foundational research in computer vision and AI.Read more



Ultralytics · GitHub





At Ultralytics, we are dedicated to creating the best artificial intelligence models in the world. Our open source works here on GitHub offer cutting-edge ...Read more



vision/torchvision/csrc/ops/nms.cpp at main





Datasets, Transforms and Models specific to Computer Vision - vision/torchvision/csrc/ops/nms.cpp at main · pytorch/vision.



sciencedirect.com

sciencedirect.com

Unifying Multi-object 3D Visual Grounding and Dense ...





8 days ago — 3D visual grounding and 3D dense captioning are two fundamental yet traditionally isolated tasks in multimodal scene understanding, ...Read more



Ensembling boxes from different object detection models





by R Solovyev · 2021 · Cited by 653 — In this work, we present a novel method for fusing predictions from different object detection models: weighted boxes fusion. Our algorithm utilizes confidence ...Read more



qwenlm.github.io

qwenlm.github.io

Qwen2.5 VL! Qwen2.5 VL! Qwen2.5 VL!





Jan 26, 2025 — Capable of visual localization in different formats: Qwen2.5-VL can accurately localize objects in an image by generating bounding boxes or ...Read more



researchgate.net

researchgate.net

GroundSight: Augmenting Vision-Language Models with ...





Oct 3, 2025 — We propose a method to improve Visual Question Answering (VQA) with Retrieval-Augmented Generation (RAG) by introducing text-grounded object ...Read more



reddit.com

reddit.com

OpenAI Codex: Guide to Creating and Using Custom Skills





OpenAI Codex: Guide to Creating and Using Custom Skills · What are Skills? · How to Create a Skill · Example Skill in Action · Best Practices.Read more



"Referring" vs. "Referencing?" : r/linguistics





"Referring" means "pointing to," in general, whereas "referencing" has the additional implication that the thing being referred to is a verifiable, material ...



Curated list of 150+ tools for OpenAI Codex CLI — ...





Curated list of 150+ tools for OpenAI Codex CLI — subagents, MCP servers, cross-agent bridges, and a Codex vs Claude Code vs Gemini CLI ...Read more



Qwen3-VL - Bounding Box Coordinate : r/LocalLLaMA





Hey everyone, I've been exploring open source models that can take an image and output bounding boxes for a specific object.



qwen.ai

qwen.ai

Qwen2.5-VL 7B





Jan 26, 2025 — Capable of visual localization in different formats: Qwen2.5-VL can accurately localize objects in an image by generating bounding boxes or ...Read more



ar5iv.labs.arxiv.org

ar5iv.labs.arxiv.org

\[2303.17651] \\ours: Iterative Refinement with Self-Feedback





Motivated by how humans refine their written text, we introduce \\ours, an approach for improving initial outputs from LLMs through iterative feedback and ...



\[1905.05055] Object Detection in 20 Years: A Survey - ar5iv





Van Gool, “Non-maximum suppression for object detection by passing messages between windows,” in Asian Conference on Computer Vision. Springer, 2014, pp ...Read more



merriam-webster.com

merriam-webster.com

REFERRING Synonyms: 41 Similar Words





Synonyms for REFERRING: alluding, indicative, allusive, telltale, reflective, denoting, symptomatic, denotative, signifying, characteristic.



REFER Definition \& Meaning





4 days ago — referred; referring. 1. : to explain in terms of a general cause. referred the defeat to poor training. 2. : to go, send, or guide to some ...



FERRET Definition \& Meaning





Apr 13, 2026 — 1. a : a domesticated usually albino, brownish, or silver-gray animal (Mustela furo synonym Mustela putorius furo) that is descended from the European polecat.Read more



VISUAL Definition \& Meaning





1\. of, relating to, or used in vision; visual organs. 2. attained or maintained by sight; visual impressions. 3. visible; visual objects. 4. producing mental ...Read more



oed.com

oed.com

referring, adj. meanings, etymology and more





There is one meaning in OED's entry for the adjective referring. See 'Meaning \& use' for definition, usage, and quotation evidence.



en.wiktionary.org

en.wiktionary.org

referring - Wiktionary, the free dictionary





English · Alternative forms · Verb · Noun.



petco.com

petco.com

Pet Ferrets for Sale





Ferrets are incredibly social \& intelligent mammals that can easily be taught tricks just like a dog. Come see live pet ferrets for sale at a Petco near ...



Pet Ferrets for Sale





Ferrets are incredibly social \& intelligent mammals that can easily be taught tricks just like a dog. Come see live pet ferrets for sale at a Petco near ...



healthline.com

healthline.com

Grounding: Can Walking Barefoot on the Earth Heal You?





Feb 28, 2025 — Grounding, also called earthing, is a technique that involves doing activities that “ground” or electrically reconnect you to the earth.Read more



en.wikipedia.org

en.wikipedia.org

Ferret





The ferret (Mustela furo) is a small, domesticated species belonging to the family Mustelidae. The ferret is most likely a domesticated form of the wild ...Read more



Grounding





Other uses · Grounding (discipline technique), restrictions placed on movement, privileges, or both as punishment · Grounding, or earthing, a pseudoscientific ...Read more



pmc.ncbi.nlm.nih.gov

pmc.ncbi.nlm.nih.gov

The effects of grounding (earthing) on inflammation, the ... - PMC





by JL Oschman · 2015 · Cited by 240 — Grounding reduces or even prevents the cardinal signs of inflammation following injury: redness, heat, swelling, pain, and loss of function (Figures 1 and 2).Read more



cdc.gov

cdc.gov

Ferrets | Healthy Pets, Healthy People





Jan 30, 2025 — Although ferrets can make good pets, they can sometimes carry germs that can make people sick. Ferrets are also not recommended for homes with children under 5 ...Read more



wellcats.arizona.edu

wellcats.arizona.edu

Grounding Strategies - WellCats - The University of Arizona





Grounding Basics. Grounding helps you find calm and stay present when you're feeling overwhelmed or triggered. It activates your body's relaxation response, ...Read more



animalhumanesociety.org

animalhumanesociety.org

Ferret care





Ferrets are inquisitive, lively, and charming little creatures. Relatives to mink and weasles, ferrets are especially active and need lots of exercise.Read more



health.clevelandclinic.org

health.clevelandclinic.org

13 Grounding Techniques To Help Calm Anxiety





Nov 25, 2024 — Grounding techniques that focus on sight, sound, taste and touch can help you find the calm you need when you feel overwhelmed.



webmd.com

webmd.com

Grounding: Techniques and Benefits





Grounding, also known as earthing, is when you stand on the earth or have contact with a product that's grounded into the earth. This is thought to connect ...Read more



chewy.com

chewy.com

A Beginner's Guide To Keeping a Ferret as a Pet





Jan 20, 2026 — From behavior and dietary needs to setting up a safe living space and maintaining their health, we're walking you through all the essential details.Read more



openaccess.thecvf.com

openaccess.thecvf.com

Mitigating Object Hallucinations in Large Vision-Language ...





by S Leng · 2024 · Cited by 682 — To mitigate this is- sue, we introduce Visual Contrastive Decoding (VCD), a simple and training-free method that contrasts output dis- tributions derived from ...Read more



ecva.net

ecva.net

Contrastive Region Guidance: Improving Grounding in ...





by D Wan · Cited by 75 — CRG: Improving Grounding in Vision-Language Models without Training. 5 inputs \[50,57,61]. Our work falls into to the third category, using visual guidance.Read more



dl.acm.org

dl.acm.org

Improving Grounding in Vision-Language Models Without ...





Contrastive Region Guidance: Improving Grounding in Vision-Language Models Without Training. Authors: David Wan. David Wan. UNC Chapel Hill, Chapel Hill, USA.Read more



youtube.com

youtube.com

Object Detection Part 8: Grounding DINO, Open-Set Object ...





In this video we explore how we can perform open-set object detection in computer by studying the Grounding DINO architecture.



Find Your Most Similar Samples with FiftyOne Brain





You can search by image similarity by clicking the button under the sample tab defines more similar samples of the one that you have selected.



semanticscholar.org

semanticscholar.org

Improving Grounding in Vision-Language Models without ...





Mar 4, 2024 — Contrastive Region Guidance: Improving Grounding in Vision-Language Models without Training · 60 Citations · 59 References.Read more



Ensembling boxes from different object detection models





Weighted boxes fusion: Ensembling boxes from different object detection models ... This paper proposes a novel SFOD framework that leverages VFMs as ...Read more



bibbase.org

bibbase.org

Improving Grounding in Vision-Language Models without Training.





Contrastive Region Guidance: Improving Grounding in Vision-Language Models without Training. Wan, D., Cho, J., Stengel-Eskin, E., \& Bansal, M. CoRR, 2024.



openai.com

openai.com

How evals drive the next chapter in AI for businesses





Nov 19, 2025 — Learn how evals help businesses define, measure, and improve AI performance—reducing risk, boosting productivity, and driving strategic ...



community.openai.com

community.openai.com

Best practices for eval-driven development \[brainstorming]





Nov 15, 2025 — I'm looking for best practices regarding building evals for the MCP apps. So far, we have used the Evals API to individually evaluate tool ...Read more



qdrant.tech

qdrant.tech

Qdrant - Vector Search Engine





Qdrant helps you build the AI retrieval you want. Ship high performance, full-feature vector search at any scale and with any deployment model. Start Free ...Read more



Qdrant Documentation





Qdrant is an Open-Source Vector Search Engine written in Rust. It provides fast and scalable vector similarity search service with convenient API.



Local Quickstart





Qdrant is an Open-Source Vector Search Engine written in Rust. It provides fast and scalable vector similarity search service with convenient API.



context7.com

context7.com

Context7 - Up-to-date documentation for LLMs and AI code ...





Pull up-to-date, version-specific documentation and code examples for any library directly into Cursor, Claude Code, Windsurf, and other AI coding tools.



augmentcode.com

augmentcode.com

mcp-server-qdrant





Author: qdrant ; Description: Official Model Context Protocol (MCP) server that uses Qdrant as a semantic-memory backend (vector store). It exposes two MCP tools ...Read more



pulsemcp.com

pulsemcp.com

Official Qdrant MCP Server





A standardized, official file format that defines how to use this MCP server. View the file to see installation instructions, configuration options, and usage ...Read more



thoughtworks.com

thoughtworks.com

Context7 | Technology Radar





Nov 5, 2025 — Context7 is an MCP server that addresses inaccuracies in AI-generated code. While LLMs rely on outdated training data, Context7 ensures they ...



medium.com

medium.com

I Built a Context7 Local-First Alternative With Claude Code





So I built my own. It took about a week, most of it pair-programming with Claude Code. The result is Context — a local-first documentation tool ...



\[Complete Guide] Is OpenAI Codex's New “Skill” Feature a ...





OpenAI's AI agent, “Codex,” has introduced a new experimental feature called “Skill.” “I want AI agents to act autonomously, but complex ...Read more



Exploring Your Visual Dataset with Embeddings in FiftyOne





We'll work with a real dataset to show you how to visualize hidden patterns, find similar images, detect duplicates, identify unique samples, ...Read more



code.visualstudio.com

code.visualstudio.com

Visual Studio Code - The open source AI code editor | Your ...





Visual Studio Code redefines AI-powered coding with GitHub Copilot for building and debugging modern web and cloud applications. Visual Studio Code is free ...



visualcomfort.com

visualcomfort.com

Signature Designer Light Fixtures | Experience Visual Comfort ...





Visual Comfort \& Co. is a premier resource of designer lighting, with an array of light fixtures including pendant lighting and chandeliers.



dictionary.cambridge.org

dictionary.cambridge.org

VISUAL | definition in the Cambridge English Dictionary





8 days ago — something such as a picture, photograph, or piece of film used to give a particular effect or to explain something.Read more



instagram.com

instagram.com

Visual (@visual) • Instagram photos and videos





Our collectible skateboards make for Great Wall Art. You can view all of our offerings. Our collectible skateboards make for ...



docs.pytorch.org

docs.pytorch.org

nms — Torchvision main documentation





Performs non-maximum suppression (NMS) on the boxes according to their intersection-over-union (IoU). NMS iteratively removes lower scoring boxes.Read more



Operators — Torchvision 0.15 documentation





nms (boxes, scores, iou\_threshold). Performs non-maximum suppression (NMS) on the boxes according to their intersection-over-union (IoU). roi\_align (input ...Read more



torchvision.ops





Performs non-maximum suppression (NMS) on the boxes according to their intersection-over-union (IoU). NMS iteratively removes lower scoring boxes which have an ...Read more



ultralytics.com

ultralytics.com

Ultralytics | Revolutionizing the World of Computer Vision





End-to-end computer vision platform. Annotate data, train YOLO models, and deploy to 43 global regions. Trusted by Siemens, Intel, Shell \& more.



mindspore.cn

mindspore.cn

Differences with torchvision.ops.nms





The latest document version has been released. Please check 2.8.0 to the latest documentation. Differences with torchvision.ops.nms . View Source ...Read more



deepnote.com

deepnote.com

Ultimate guide to torchvision library in Python





Aug 22, 2025 — Official resources. Torchvision Documentation (latest version) – The official docs for torchvision are hosted on the PyTorch website. This ...Read more



catalyzex.com

catalyzex.com

ensembling boxes for object detection models





Abstract:In this work, we introduce a novel Weighted Box Fusion (WBF) ensembling algorithm that boosts the performance by ensembling predictions from ...Read more



raw.githubusercontent.com

raw.githubusercontent.com

raw.githubusercontent.com





Total lines: 9



voxel51.com

voxel51.com

FiftyOne 1.14.2 documentation





Evaluating Detections · Guide Summary · Medical Imaging Guide · Getting Started with ... fiftyone.brain.similarity · fiftyone.brain.visualization · fiftyone.core.Read more



FiftyOne — FiftyOne 1.15.0 documentation





Everything you need to build, evaluate, and ship better computer vision models. Visualize. Explore your data in the FiftyOne App. Browse images, videos, and 3D ...Read more



learnopencv.com

learnopencv.com

Object Detection and Spatial Understanding with VLMs ft. ...





Aug 5, 2025 — A guide to Object Detection with VLMs using Qwen2.5-VL. Go beyond simple boxes to true Spatial Understanding, Object Counting, ...



facebook.com

facebook.com

Open vocabulary object detection with qwen3-vl model





Qwen2-VL's ability to understand diverse visual inputs and multilingual requests could lead to more sophisticated, globally accessible AI ...Read more



openreview.net

openreview.net

Multi-Object Hallucination in Vision Language Models





Sep 25, 2024 — This work systematically investigates multi-object hallucination, examining how models misperceive (eg, invent nonexistent objects or become distracted)Read more



ollama.com

ollama.com

qwen2.5vl





Capable of visual localization in different formats: Qwen2.5-VL can accurately localize objects in an image by generating bounding boxes or points, and it ...Read more



authorea.com

authorea.com

Browse Preprints - Authorea





This survey reviews recent efforts to strengthen compositionality in CLIP-style vision-language models. We propose a taxonomy with four primary method ...



Connector sources scanned



No connector sources scanned

