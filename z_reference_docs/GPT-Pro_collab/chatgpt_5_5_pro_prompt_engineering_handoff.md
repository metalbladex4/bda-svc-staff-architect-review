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
`detect_objects` prompt toward a literal near-perfect target of 99 percent
improvement in measured detection errors. In this project, that target has been
operationalized as a 99 percent reduction in combined false negatives plus false
positives on the main all-current/no101 validation set. The current best prompt
does not meet that target.

Important current state:

- Current Qwen incumbent: `v020c_extra_box_audit` / `v020c_anchor_replay`.
- Current incumbent metrics: `186` matches / `33` false negatives /
  `25` false positives, `58` total FN+FP errors.
- Current best high-recall challenger: `v024l_v023s_no_wheel_track_ablation`.
- Challenger metrics: `188` matches / `31` false negatives /
  `35` false positives, `66` total FN+FP errors.
- `v024l` is not better overall because its false-positive burden is too high.
- `v024o_v024l_intact_building_piece_exclusion` was interrupted before the
  all-current run completed. It is partial and unscored. Do not treat it as
  evidence unless it is rerun fully.
- The current recommendation is to preserve `v020c` and investigate visual
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

- Do not treat local memory systems as source truth. Source artifacts, manifests,
  runner outputs, eval summaries, code, and explicit user direction win.
- Do not score partial `v024o` outputs.
- Do not assume `v024l` replaced `v020c`.
- Do not recommend source-truth mutation without explicit validation and user
  approval.
- Do not include or request credential values.
- The private GitHub review repo should not be updated unless the user gives a
  separate explicit instruction.

## Project Context

Repository root:

```text
/home/williambenitez1/Capstone
```

Primary active Qwen worktree:

```text
/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement
```

The project, `bda-svc`, is a local CLI/service workflow for battle damage
assessment. The relevant prompt surface is the detection prompt:

```yaml
prompts.detect_objects
```

The stable product config path is:

```text
src/bda_svc/pipeline/config.yaml
```

The current prompt-engineering work is mostly local prompt-lab evidence under:

```text
/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/
```

These prompt-lab packages are local evidence, not automatically promoted runtime
truth. A prompt only becomes product-facing after a separate promotion path.

## Evaluation Frame

The main recent evaluation pack is:

```text
human_report_challenge_v2_all_current_117_no101
```

Key control cases:

- `155`: positive-control case that must remain safe.
- `166`: positive-control case that must remain safe.
- `legacy_abstention_guard_office_negative`: one-case negative-scene abstention
  guard.

Key dense/pressure cases:

- `66`
- `67`
- `84`
- `97`

Case `67` has become the most important dense-row sentinel. Many prompt edits
that look reasonable globally collapse case `67` from the incumbent's useful
`9/2/4` behavior to only `1-2` matches with `9-11` false negatives and many
false positives.

The literal 99 percent target used in the latest cycles:

- Current upstream prompt baseline was treated as `74` total detection errors:
  `38` false negatives plus `36` false positives.
- Literal 99 percent reduction target means `<= 1` combined false negative plus
  false positive on the all-current/no101 set.
- Best result so far remains `58` total errors, so we are far from that target.

## Current State

The most current source-verified checkpoint says there has been no new prompt
run, code change, doctrine change, promotion, or source-truth update since the
v023/v024 pause closeout.

Current Qwen incumbent:

```text
v020c_extra_box_audit / v020c_anchor_replay
186 matches / 33 false negatives / 25 false positives
58 combined FN+FP errors
controls passed: 155, 166, office-negative
```

Best high-recall challenger:

```text
v024l_v023s_no_wheel_track_ablation
188 matches / 31 false negatives / 35 false positives
66 combined FN+FP errors
controls passed: 155, 166, office-negative
```

Why `v024l` is not the incumbent:

- It gained `+2` matches and reduced false negatives by `2` compared with
  `v020c`.
- It added `+10` false positives compared with `v020c`.
- It is useful learning evidence, but worse on the combined error objective.

Interrupted candidate:

```text
v024o_v024l_intact_building_piece_exclusion
```

`v024o` was paused before the all-current run completed. It has partial
predictions only and must not be scored. If resumed, rerun it fully from
scratch.

Config-only review branch context:

- `v020c` was selected for a config-only review branch:
  `feat/config-prompt-improved-v1`.
- The intended branch scope is only:
  `src/bda_svc/pipeline/config.yaml`.
- This dossier is not asking ChatGPT 5.5 Pro to open, update, or push that
  branch. It is context for why `v020c` is treated as the current Qwen
  config-prompt incumbent.

## Progress History

### v017b - parked prompt-only candidate

`v017b_group_box_rejection` was an accepted prompt-only candidate at one point
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

- Upstream style: concise and recall-friendly.
- v017b style: defensive and control-safe, but under-counted in some scenes.

### v018 - upstream/v017b amalgamation cycle

Package:

```text
/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/upstream_v017b_amalgamation_cycle/
```

Baselines:

| Row | Matches | FNs | FPs | 155 |
| --- | ---: | ---: | ---: | --- |
| upstream prompt-controlled | 169 | 50 | 24 | fail |
| v017b local Qwen | 165 | 54 | 22 raw / 21 effective | pass |
| v017b upstream-code compat | 166 | 53 | 26 | pass |

Best v018 signals:

- `v018d_evidence_budget_pruner`: `180/39/39`, recall ceiling but too many FPs.
- `v018e_contrastive_body_anchor`: `173/46/29`, best precision-balanced
  follow-up axis.

Outcome:

- No v018 prompt was adoption-ready.
- All improved recall over upstream/v017b in some way, but all exceeded the
  false-positive ceiling.

### v019 - v018e creative follow-up

Package:

```text
/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v019_v018e_creative_followup_cycle/
```

Fresh anchor:

```text
v018e_anchor_replay: 173 / 46 / 29, controls pass
```

Best v019 row:

```text
v019c_context_shadow_reversal: 174 / 45 / 28, controls pass
```

Outcome:

- `v019c` was a strong next-primary candidate compared with `v018e`.
- It improved recall and slightly reduced false positives, but still did not
  approach the later target.

### v020 - goal-driven self-improvement cycle

Package:

```text
/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v020_v019c_goal_driven_self_improvement_cycle/
```

Started from:

```text
v019c_context_shadow_reversal: 174 / 45 / 28
```

Best row:

```text
v020c_v019c_extra_box_audit: 186 / 33 / 25
```

Exact replay:

```text
v020h: 186 / 33 / 25
```

Outcome:

- `v020c` was the first stable prompt-only breakthrough.
- Exact replay reproduced the result.
- Success target for that cycle (`FNs <=25`, `FPs <=15`) was not reached.
- Later v020 variants mostly hurt dense rows or increased false positives.

Dense-case `v020c` profile:

| Case | Matches | FNs | FPs | Read |
| --- | ---: | ---: | ---: | --- |
| `66` | 8 | 0 | 4 | full recall, extra row boxes remain |
| `67` | 9 | 2 | 4 | major recovery versus v019c |
| `84` | 8 | 5 | 0 | useful recall, misses distant row vehicles |
| `97` | 1 | 0 | 2 | target found, extra boxes remain |

### v021 - OpenAI-compatible cross-model matrix

Package:

```text
/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v021_openai_compat_cross_model_prompt_matrix/
```

Purpose:

- Compare `upstream/main`, `v009`, `v017b`, `v018e`, `v019c`, and `v020c`
  through the fetched upstream/main OpenAI-compatible runtime path.
- Test both Qwen and Gemma rows.
- Confirm doctrine diff gate.

Key result:

- Qwen winner: `v020c_extra_box_audit` at `186/33/25`, controls passing.
- Gemma winner among eligible rows: `v018e_contrastive_body_anchor` at
  `138/81/19`, controls passing.
- Gemma `v020c` lowered false positives to `18`, but failed positive control
  `155`, so it was disqualified for Gemma.
- Local and fetched upstream `doctrine.yaml` matched exactly, so there was one
  shared-doctrine matrix.

Major process lesson:

- Future prompt comparisons should default to the upstream OpenAI-compatible
  `OPENAI_BASE_URL` code path.
- If the backing server is Ollama's `/v1` endpoint, label it honestly as
  OpenAI-compatible Ollama, not pure upstream vLLM/server.

### v022 - literal-99 Qwen prompt-only plateau

Package:

```text
/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v022_literal99_qwen_recursive_prompt_refinement_cycle/
```

Literal target:

```text
upstream baseline errors: 74 = 38 FNs + 36 FPs
target: <= 1 combined FN+FP
```

Best row:

```text
v020c_anchor_replay: 186 / 33 / 25, 58 total errors
```

All new v022 variants regressed.

Important failure:

Even adding one dense-guard sentence to v020c disturbed case `67` and worsened
case `84`. This made `v020c` look like a brittle local optimum, not a general
prompt pattern that can be safely expanded.

### v023/v024 - no-stop continuation and pause

Package:

```text
/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v023_literal99_qwen_no_stop_continuation/
```

Pause report:

```text
pause_report_2026-05-06.md
```

What happened:

- Replayed `v020c`.
- Ran `v023a` through `v023z`.
- Ran `v024a` through `v024n`.
- Started `v024o`, but it was paused before all-current completion.

Current champion:

```text
v020c_anchor_replay: 186 / 33 / 25, 58 total errors
```

Best challenger:

```text
v024l_v023s_no_wheel_track_ablation: 188 / 31 / 35, 66 total errors
```

Important v024 lessons:

- `v024l` proves there is a high-recall branch, but it is still FP-heavy.
- `silhouette` and `exterior wall/roof boundary` were load-bearing in the
  v023s branch. Removing either collapsed dense case `67`.
- Removing `wheel/track contact` created the best challenger, but still did not
  fix false positives.
- Long building-only de-tiling prompt sections are dangerous. `v024n` exploded
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
runtime path controlled by `OPENAI_BASE_URL`. This better matches how the
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

- case `155`
- case `166`
- office-negative abstention
- valid JSON/runtime behavior
- no case `101` in active no101 manifests

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
rules were especially risky. `v024n_v024l_building_only_detiling` reached
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
/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement
```

Gemma `3.1` worktree:

```text
/home/williambenitez1/Capstone_worktrees/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap
```

Useful live docs:

```text
z_reference_docs/WORKING_CHANGELOG.md
z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md
z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md
z_reference_docs/PROJECT_BRAIN.md
z_reference_docs/Prompt_Labs/PROMPT_LABS_INDEX.md
```

### Prompt-lab runners and artifacts

Recent cycle packages:

```text
.../upstream_v017b_amalgamation_cycle/
.../v019_v018e_creative_followup_cycle/
.../v020_v019c_goal_driven_self_improvement_cycle/
.../v021_openai_compat_cross_model_prompt_matrix/
.../v022_literal99_qwen_recursive_prompt_refinement_cycle/
.../v023_literal99_qwen_no_stop_continuation/
```

Common artifact types:

```text
candidate_registry.json
comparison_matrix.json
comparison_matrix.md
diagnoses/<candidate>_diagnosis.md
final_recommendation.md
recovery_log.md
research_notes.md
runs/<candidate>/<pack>/...
source_manifest.json
```

### Graphify/project-brain

Entry document:

```text
z_reference_docs/PROJECT_BRAIN.md
```

Project-brain command:

```bash
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py recall "v023 v024 refresh checkpoint current state v020c v024o"
```

Refresh and validation commands:

```bash
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py update
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py doctor --strict-stale
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py recall-benchmark
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py verify-memory --strict --json
```

Graphify is a navigation and recall layer, not source truth. It has source
verified notes and semantic seeds that point back to source artifacts.

### Mem0

Mem0 is durable advisory memory. It is not source truth.

It was used to store concise lessons such as:

- v020c remains incumbent.
- v024l is high-recall but FP-heavy.
- v024o is interrupted/unscored.
- case `67` is brittle.
- long building-only prompt rules can cause FP tiling.
- next axis should favor visual review plus non-prompt duplicate/tiling
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
/home/williambenitez1/Capstone/z_reference_docs/WORKING_CHANGELOG.md
/home/williambenitez1/Capstone/z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md
/home/williambenitez1/Capstone/z_reference_docs/PROJECT_BRAIN.md
/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/PROMPT_LABS_INDEX.md
```

Current pause report:

```text
/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v023_literal99_qwen_no_stop_continuation/pause_report_2026-05-06.md
```

Recent final recommendations:

```text
.../upstream_v017b_amalgamation_cycle/final_recommendation.md
.../v019_v018e_creative_followup_cycle/final_recommendation.md
.../v020_v019c_goal_driven_self_improvement_cycle/final_recommendation.md
.../v021_openai_compat_cross_model_prompt_matrix/final_recommendation.md
.../v022_literal99_qwen_recursive_prompt_refinement_cycle/final_recommendation.md
.../v023_literal99_qwen_no_stop_continuation/final_recommendation.md
```

Current comparison matrices:

```text
.../v020_v019c_goal_driven_self_improvement_cycle/comparison_matrix.md
.../v021_openai_compat_cross_model_prompt_matrix/cross_model_comparison_matrix.md
.../v022_literal99_qwen_recursive_prompt_refinement_cycle/comparison_matrix.md
.../v023_literal99_qwen_no_stop_continuation/comparison_matrix.md
```

Graphify recall command:

```bash
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py recall "v023 v024 refresh checkpoint current state v020c v024o"
```

## Boundaries For The Collaboration

- Do not update `metalbladex4/bda-svc-staff-architect-review` yet. The user
  will give explicit instructions later.
- Do not assume local-only prompt-lab artifacts are already product truth.
- Do not treat Graphify or Mem0 as authoritative evidence.
- Do not use partial `v024o` outputs as metrics.
- Do not recommend storing credential values in docs, prompts, memory, or tool
  inventories.
- Do not recommend broad source-truth changes without a clear validation gate.
- Do not recommend adopting a prompt only because it improves recall. Positive
  controls and false-positive burden matter.

## The Core Ask

Help us make Codex better at the process itself.

We are not merely asking for one more prompt. We are asking for a stronger
recursive improvement system where Codex can:

- inspect evidence,
- generate one candidate at a time,
- run the candidate,
- diagnose results,
- update its lessons,
- decide whether to continue, pivot, or escalate to visual/non-prompt tools,
- and use each loop to become better at the next loop.

The goal is still near perfection, but the current evidence says prompt-only
edits are plateauing. The best research contribution may be a better decision
system for when and how to move beyond prompt wording while preserving the
successful `v020c` behavior.
