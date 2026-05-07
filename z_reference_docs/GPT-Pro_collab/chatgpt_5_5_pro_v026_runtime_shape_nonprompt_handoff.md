# ChatGPT 5.5 Pro Handoff: v026 Runtime Shape Sensitivity And Next Research Pivot

Generated: 2026-05-07

## Copy/Paste Mission Prompt For ChatGPT 5.5 Pro

You are being brought back in as a research partner for the Capstone `bda-svc`
Qwen prompt-engineering workflow.

Please read this handoff together with:

```text
z_reference_docs/GPT-Pro_collab/chatgpt_5_5_pro_prompt_engineering_handoff.md
z_reference_docs/GPT-Pro_collab/CODEX_QWEN_PROMPT_ENGINEERING_DIRECTION_2026-05-06.md
z_reference_docs/GPT-Pro_collab/bda_svc_qwen_prompt_engineering_deep_research_bundle.md
z_reference_docs/GPT-Pro_collab/V026_RUNTIME_SHAPE_REVIEW_POINTER.md
z_reference_docs/WORKING_CHANGELOG.md
z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md
z_reference_docs/PROJECT_BRAIN.md
```

Published v026 evidence package:

```text
docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v026_autonomous_qwen_prompt_refinement_tranche/
```

Runtime-shape probe evidence:

```text
docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v026_autonomous_qwen_prompt_refinement_tranche/runtime_shape_probe_evidence.md
```

The new task is not to write another detection prompt immediately. The new task
is to understand why the latest autonomous prompt-refinement tranche stopped,
evaluate Codex's decision process, and craft a Deep Research prompt focused on
what should come after prompt-only refinement appears unreliable.

The central question:

```text
If prompt engineering has reached a brittle local optimum for Qwen detection,
what research-backed system design, verifier, post-processing, visual-review,
backend-stability, or hybrid workflow should we explore next while preserving
the current best prompt and evaluation discipline?
```

## Executive Summary

The latest Qwen autonomous tranche, `v026`, did not stop because Codex got tired
or because one candidate failed. It stopped because the evaluation surface became
untrustworthy for prompt-quality learning.

Current incumbent:

```text
v020c_anchor_replay / v020c_extra_box_audit
186 matches / 33 false negatives / 25 false positives
58 combined errors
controls passed: 155, 166, office-negative
```

The v026 tranche attempted sequential prompt candidates from `v020c` using a
sentinel micro-pack before all-current. The preferred upstream OpenAI-compatible
backend at:

```text
http://localhost:8000/v1
```

was unavailable. The authorized fallback was Ollama's OpenAI-compatible endpoint:

```text
http://localhost:11434/v1
```

On that fallback endpoint:

- exact `v020c` replay remained stable
- no-op/exact replay artifacts reproduced `v020c`
- every rendered prompt delta failed the sentinel gate
- the strongest warning was `v026q_blank_line_shape_probe`, which changed only
  prompt shape by adding one blank line, but still collapsed dense case `67`
  from the stable `9/2/4` behavior to `1/10/9`

That means continued prompt mutation was no longer testing:

```text
Is this prompt idea better?
```

It was increasingly testing:

```text
Does this backend/prompt-rendering path behave unpredictably when prompt bytes
or shape change?
```

Codex therefore paused under the runtime-validity / evaluation-surface
stability stop rule.

## What Happened In v026

Package:

```text
/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v026_autonomous_qwen_prompt_refinement_tranche/
```

Key source artifacts:

```text
final_recommendation.md
pause_report_2026-05-07_runtime_shape_sensitivity.md
strategy_state.md
lessons_learned.md
live_metrics_log.md
```

The tranche used a two-tier evaluation pattern:

1. Sentinel micro-pack first.
2. Full all-current run only if the sentinel passed.

The sentinel pack was designed to cheaply catch:

- dense-row collapse, especially case `67`
- controls `155` and `166`
- office-negative abstention
- false-positive reopening patterns
- invalid JSON/runtime failures

This gate worked. It prevented many bad prompt deltas from wasting full
all-current runs.

## Candidate Pattern

The following prompt deltas failed the sentinel gate:

```text
v026b_audit_removal_only_lock
v026d_qwen_native_grounding_header
v026e_low_salience_separate_body_good_box
v026g_actual_tight_occupancy_guard
v026h_remove_calibration_preamble
v026i_remove_v019c_label_only
v026j_visible_body_occupancy_phrase
v026k_unrelated_background_object_guard
v026l_compact_context_shadow_schema
v026m_target_guidance_before_context
v026n_dense_row_body_safety_cue
v026o_output_only_no_extra_keys
v026p_quadrant_scan_search_cue
v026q_blank_line_shape_probe
```

Several no-op or incorrectly rendered exact-replay artifacts reproduced
`v020c`:

```text
v026a_fragment_context_precision_guard: 186/33/25/58
v026c_vehicle_body_anchor_not_rowline: 186/33/25/58
v026f_tight_box_occupancy_guard: 186/33/25/58
```

The important distinction:

- exact/no-op prompt shape stayed stable
- rendered prompt changes collapsed the sentinel
- even a no-semantics shape probe collapsed the sentinel

That pattern suggests backend/rendering/prompt-byte sensitivity, not just bad
prompt semantics.

## Codex Decision Process

Codex used the following decision ladder:

1. Preserve the product/current incumbent unless a candidate beats it on
   combined FN+FP while passing controls.
2. Treat failed semantic candidates as learning evidence, not as a reason to
   quit.
3. Continue after ordinary candidate failures.
4. Pivot when repeated candidate families fail.
5. Stop only when a hard stop appears.
6. Classify no-semantics prompt-shape failure as a hard stop because it means
   the evaluation surface itself is not trustworthy.

The key inference:

```text
Candidate failure means the idea failed.
Shape-probe failure means the measuring surface failed.
```

In v026, the blank-line-only probe was the decisive event. It showed that the
fallback backend could turn an almost meaningless prompt-shape change into a
major dense-case collapse.

Codex therefore stopped semantic prompt mutation and recommended:

1. Restore or verify the preferred `localhost:8000/v1` backend.
2. Replay exact `v020c`.
3. Run a no-semantics prompt-shape probe.
4. Author new semantic prompt candidates only if both probes are stable.

## Plain-English Explanation

The system had a good "spotter" prompt: `v020c`.

We tried to make the spotter better with tiny wording changes. But the test
setup started acting like a weird oven: exact `v020c` cooked correctly, but
moving a blank line on the recipe card made the oven behave differently.

At that point, continuing to test recipes would not be smart. We needed to stop
and ask whether the oven/test setup was stable.

The conclusion was:

```text
Do not keep rewriting the prompt on this unstable surface.
Freeze v020c.
Fix/verify the backend.
Then explore non-prompt cleanup or verifier layers that preserve v020c's recall.
```

## Current Recommendation

The next high-leverage move is not another near-neighbor prompt edit.

Recommended direction:

```text
Freeze v020c as the detector prompt.
Treat it as the candidate generator / spotter.
Add research and experiments around a separate referee layer:
post-processing, box verification, crop-based validation, duplicate/tiling
suppression, visual review, or hybrid detector-verifier workflows.
```

Why:

- `v020c` is the stable best prompt-only incumbent.
- Later prompt variants repeatedly failed to beat its total error.
- Cleanup/row/non-overlap wording is fragile, especially for dense case `67`.
- Prompt-shape sensitivity on the fallback backend makes more prompt mutation
  hard to trust.
- The remaining errors look like they may be better handled by a box-level
  verifier or deterministic suppression layer than by more prose in the main
  detection prompt.

## What To Research Next

Please craft a Deep Research prompt around these questions.

### 1. Backend And Prompt-Shape Stability

Research how OpenAI-compatible local VLM serving stacks can introduce
prompt-serialization sensitivity.

Questions:

- What practical differences exist between vLLM, SGLang, Ollama
  OpenAI-compatible endpoints, Transformers servers, and other local serving
  paths for Qwen3-VL or Qwen2.5-VL style models?
- How can we verify that prompt serialization, chat templates, image token
  handling, whitespace, stop tokens, JSON constraints, and system/user message
  boundaries are stable?
- What minimum replay/shape-probe suite should be run before trusting a prompt
  optimization loop?

### 2. Detection Post-Processing For VLM Boxes

Research post-processing methods that can reduce false positives without
destroying dense-row recall.

Questions:

- Which methods are safest for VLM-predicted boxes: NMS, soft-NMS,
  weighted boxes fusion, containment suppression, duplicate-fragment filters,
  row/group-box filters, or crop-level revalidation?
- How should thresholds be calibrated when the VLM has no native confidence
  scores?
- Can lexical label, bbox geometry, IoU, containment, area ratio, aspect ratio,
  and crop evidence be combined without turning this into brittle hand-coded
  source-truth overfitting?

### 3. Crop-Based Verifier / Referee Pass

Research a second-stage verifier pass that evaluates each predicted box/crop.

Questions:

- Should the verifier be the same Qwen model, a smaller VLM, a classical image
  heuristic, or a hybrid?
- What prompt design works best for crop-level validation:
  "is this a visible target body?" vs "reject smoke/debris/building context"
  vs yes/no JSON?
- How can the verifier reject duplicate/nested/context-only boxes while
  preserving valid small, crowded, partially obscured, or smoke-obscured target
  bodies?
- What evaluation design avoids leaking case-specific source truth into the
  verifier?

### 4. Visual Failure Taxonomy And Tooling

Research how to organize visual review so the next intervention is based on
classified failure modes rather than metric summaries.

Current relevant failure classes:

```text
duplicate_same_body_box
nested_fragment_box
broad_row_or_group_box
context_only_smoke_debris_terrain
building_piece_facade_roof_section
adjacent_off_target_object
missed_small_valid_object
missed_obscured_valid_object
under_split_dense_valid_targets
over_split_one_continuous_target
reference_ambiguity
schema_or_runtime_artifact
visual_artifact_missing
other
```

Questions:

- How should FiftyOne or another visual inspection layer be used to compare
  v020c predictions, reference boxes, false positives, false negatives, and
  crop-level evidence?
- How should a small review set be chosen so it is useful without overfitting?
- What fields should be logged so lessons are reusable by Codex and GPT-5.5
  Pro?

### 5. Prompt Engineering After Plateau

Research when prompt engineering should stop or become secondary.

Questions:

- What signs indicate a prompt-only local optimum?
- What signs indicate evaluation-surface instability rather than prompt
  failure?
- How should an autonomous prompt-refinement agent decide between:
  - prompt mutation
  - exact replay
  - shape probe
  - visual review
  - post-processing simulation
  - verifier design
  - backend repair
  - source-truth audit

## Suggested Deep Research Prompt

Use this as the starting prompt for Deep Research:

```text
We are working on a local battle damage assessment project called bda-svc. The
current task is detecting damaged or military-relevant target objects in images
using Qwen-style vision-language models. The main prompt surface is
prompts.detect_objects in src/bda_svc/pipeline/config.yaml. The current best
Qwen prompt, v020c_extra_box_audit / v020c_anchor_replay, scores 186 matches,
33 false negatives, 25 false positives, and 58 combined errors on the main
human_report_challenge_v2_all_current_117_no101 evaluation. It passes positive
controls 155 and 166 plus a one-case office-negative abstention guard.

Prompt-only recursive refinement has plateaued. Later prompt candidates often
improve recall at the cost of too many false positives, or collapse dense case
67. A recent autonomous tranche, v026, used a sentinel micro-pack before
all-current runs. Exact v020c replay stayed stable on the authorized
Ollama-backed OpenAI-compatible fallback endpoint, but every rendered prompt
delta failed the sentinel gate. A no-semantics blank-line-only prompt-shape
probe also collapsed case 67 from stable 9/2/4 behavior to 1/10/9. The preferred
upstream-style backend at http://localhost:8000/v1 was unavailable, so v026
paused under an evaluation-surface stability stop rule.

Research what we should do next if prompt engineering cannot reliably improve
metrics by itself. Focus on research-backed, practical approaches that preserve
the current v020c prompt as the candidate generator while improving precision
and recall through backend stability checks, prompt-serialization verification,
visual failure review, crop-based verifier passes, duplicate/tiling
post-processing, NMS/soft-NMS/weighted-boxes-fusion-style methods adapted to
confidence-less VLM boxes, and hybrid detector-verifier workflows.

Please produce:

1. A diagnosis of why the v026 stop was methodologically correct or incorrect.
2. A checklist for validating local OpenAI-compatible Qwen backend stability,
   including exact replay and no-semantics prompt-shape probes.
3. A recommended architecture for using v020c as a high-recall candidate
   generator plus a separate referee/verifier layer.
4. Candidate post-processing methods for VLM boxes without model confidence
   scores, including containment, IoU, geometry, duplicate-fragment, row/group
   box, and crop-evidence filters.
5. A crop-based VLM verifier design with JSON schema, prompts, abstention rules,
   and evaluation protocol.
6. A visual failure-review workflow using FiftyOne or static overlays/crops,
   including sampling strategy and failure taxonomy.
7. A safe experiment plan that does not mutate source truth, doctrine,
   assessment prompt, runtime code, eval truth, product config, or promotion
   branches without explicit approval.
8. A decision framework for when Codex should continue prompt mutation versus
   stop and pivot to backend repair, visual review, post-processing,
   verifier-pass design, or source-truth audit.

Use primary sources where possible for Qwen/Qwen-VL serving, OpenAI-compatible
local VLM serving, object-detection post-processing, VLM grounding, visual
evaluation tooling, and iterative/self-refinement methods. Do not let generic
research override the local evaluation facts. Treat Graphify, Mem0, and memory
notes as navigation only; local source artifacts, runner outputs, manifests,
eval summaries, raw predictions, overlays/crops, code, and explicit user
direction remain authoritative.
```

## Boundaries For GPT-5.5 Pro And Deep Research

- Do not recommend promoting any v026 candidate.
- Do not recommend replacing `v020c` as the incumbent without new source
  evidence.
- Do not score or use partial `v024o` evidence.
- Do not treat Graphify, Mem0, Qdrant, or memory notes as source truth.
- Do not recommend source-truth mutation unless it is explicitly framed as a
  separate audited truth-review task.
- Do not assume the fallback Ollama-backed endpoint and preferred
  `localhost:8000/v1` backend are equivalent.
- Do not propose broad runtime/product changes without an experiment-only plan
  first.
- Preserve the local evaluation goal: false negatives and false positives are
  equally weighted unless the user changes that objective.

## Source Pointers

Primary v026 artifacts:

```text
/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v026_autonomous_qwen_prompt_refinement_tranche/final_recommendation.md
/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v026_autonomous_qwen_prompt_refinement_tranche/pause_report_2026-05-07_runtime_shape_sensitivity.md
/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v026_autonomous_qwen_prompt_refinement_tranche/strategy_state.md
/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v026_autonomous_qwen_prompt_refinement_tranche/lessons_learned.md
```

Current method/live docs:

```text
/home/williambenitez1/Capstone/z_reference_docs/WORKING_CHANGELOG.md
/home/williambenitez1/Capstone/z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md
/home/williambenitez1/Capstone/z_reference_docs/PROJECT_BRAIN.md
```

New workflow skills:

```text
/home/williambenitez1/.codex/skills/capstone-qwen-recursive-prompt-refinement/
/home/williambenitez1/.codex/skills/recursive-prompt-engineering-method/
/home/williambenitez1/Capstone/z_reference_docs/Codex_Skills/capstone-qwen-recursive-prompt-refinement/
/home/williambenitez1/Capstone/z_reference_docs/Codex_Skills/recursive-prompt-engineering-method/
```
