# Codex Direction: Qwen Prompt-Engineering First After Deep Research Bundle

Generated: 2026-05-06  
Intended repo path:

```text
z_reference_docs/GPT-Pro_collab/CODEX_QWEN_PROMPT_ENGINEERING_DIRECTION_2026-05-06.md
```

## Purpose

This file gives Codex the next operating doctrine for the `bda-svc` Qwen prompt-engineering workflow.

It should be read together with:

```text
z_reference_docs/GPT-Pro_collab/bda_svc_qwen_prompt_engineering_deep_research_bundle.md
z_reference_docs/GPT-Pro_collab/chatgpt_5_5_pro_prompt_engineering_handoff.md
REVIEW_REFRESH_2026-05-06.md
src/bda_svc/pipeline/config.yaml
docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v023_literal99_qwen_no_stop_continuation/pause_report_2026-05-06.md
docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v023_literal99_qwen_no_stop_continuation/final_recommendation.md
```

## Important note about the attached “Deep Research” artifact

The artifact I received as the supposed Deep Research report appears to contain the Deep Research bundle/prompt and source snippets, not a completed structured Deep Research report.

Do not treat that artifact as a completed research conclusion unless you independently find the actual report content. Treat it as:

```text
source-grounded project bundle + research seed material + web/source snippets
```

The absence of a final Deep Research report does not block the next step. The evidence is already strong enough to define the next prompt-engineering operating model.

## Current source-truth state

These facts are authoritative unless newer source artifacts in the active local repo contradict them.

```text
Project: bda-svc
Task: multimodal VLM battle damage assessment
Primary prompt surface: src/bda_svc/pipeline/config.yaml -> prompts.detect_objects
Active model line: Qwen-style VLM detection
Main eval pack: human_report_challenge_v2_all_current_117_no101
Objective: equal-weight false_negatives + false_positives
Stretch target: <=1 combined FN+FP from 74-error upstream baseline
```

Current incumbent:

```text
v020c_extra_box_audit / v020c_anchor_replay
186 matches / 33 FNs / 25 FPs
58 combined errors
controls passed: 155, 166, office-negative
```

Best high-recall challenger:

```text
v024l_v023s_no_wheel_track_ablation
188 matches / 31 FNs / 35 FPs
66 combined errors
controls passed: 155, 166, office-negative
```

Interpretation:

```text
v020c remains incumbent.
v024l is high-recall learning evidence only.
v024l is worse overall because it buys 2 fewer FNs at the cost of 10 more FPs.
v024o is interrupted/partial/unscored and must not be treated as evidence.
```

## User intent constraints

The user clarified:

```text
Prompt-engineering first.
FNs and FPs remain equally weighted.
Do not promote without explicit approval.
Do not mutate source truth during exploration.
Do not treat Graphify, Mem0, or memory notes as source truth.
Use visual review, FiftyOne, post-processing, and hybrid detection research as support, diagnostics, and inspiration.
Do not replace the primary prompt-engineering workflow with a detector/post-processing architecture unless explicitly directed later.
```

## Staff AI Systems Architect assessment

The current recursive prompt process is strong but has hit a wording-centered plateau.

The next improvement should not be another blind near-neighbor prompt tweak.

The next improvement should be:

```text
visual failure review -> failure taxonomy -> one compact prompt hypothesis -> fixed eval -> diagnosis -> next decision
```

Prompt engineering remains first, but **visual review becomes mandatory before authoring the next serious candidate**.

## Why the current process is plateauing

The v023/v024 evidence shows:

```text
1. v020c is a stable but brittle local optimum.
2. Exact wording and order are load-bearing.
3. Long prompt bloat tends to hurt.
4. Dense case 67 is fragile and easy to collapse.
5. Long building-only de-tiling rules are dangerous.
6. v024n exploded to 102 false positives.
7. v024l proves more recall is possible but still creates too many false positives.
8. Metrics alone no longer explain the remaining errors.
```

The loop is not failing because Codex lacks persistence. It is failing because Codex is now inferring visual failure types from metric summaries instead of classifying the actual boxes and images.

## Research signals to use, without overfitting to research

The research/source snippets reinforce the following operating rules:

### Qwen-style VLM grounding favors direct bbox/JSON instructions

Qwen2.5-VL official material describes precise object grounding with bounding boxes/points and standardized JSON output. This supports keeping Qwen prompts compact, direct, and JSON/bbox oriented instead of adding large prose blocks.

Reference:

```text
https://qwenlm.github.io/blog/qwen2.5-vl/
```

### Region-level and visual prompting are relevant

Groma and Contrastive Region Guidance both support the idea that grounding improves when the model is anchored to regions, visual prompts, or region-level evidence. For this project, that translates to visual review, overlays, crops, rejected-region analysis, and possibly debug-only visual verifier passes.

References:

```text
https://eccv.ecva.net/virtual/2024/poster/1114
https://groma-mllm.github.io/
https://contrastive-region-guidance.github.io/
```

### Self-refinement loops work only when feedback is grounded

Self-Refine and Reflexion support iterative feedback and episodic lessons, but in this project the feedback signal must come from eval outputs, visual review, and source artifacts, not from the model's own persuasive explanation.

References:

```text
https://proceedings.neurips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html
https://huggingface.co/papers/2303.11366
```

### FiftyOne is a practical visual eval bridge

FiftyOne supports loading detection datasets, adding custom predictions, rendering ground truth/predicted boxes, creating patches views, and running `evaluate_detections()` to populate sample/object-level eval fields. Use it to classify v020c/v024l errors, not to replace source-truth eval.

References:

```text
https://docs.voxel51.com/getting_started/object_detection/index.html
https://docs.voxel51.com/getting_started/object_detection/02_adding_detections.html
https://docs.voxel51.com/getting_started/object_detection/04_evaluating_detections.html
https://docs.voxel51.com/user_guide/evaluation.html
```

### Qdrant/MCP memory is recall, not evidence

Qdrant MCP exposes semantic store/find memory. Use it to retrieve related Prompt_Labs lessons and failure patterns, but never let it outrank source artifacts, manifests, eval summaries, runner outputs, raw predictions, overlays/crops, or code.

Reference:

```text
https://github.com/qdrant/mcp-server-qdrant
```

## New operating rule

From now on, do not author a new Qwen detection prompt candidate after this plateau unless one of the following is true:

```text
A. visual failure review has classified the target failure family, or
B. the user explicitly orders a no-visual-review prompt-only run, or
C. the candidate is a replay/validation run, not a new prompt hypothesis.
```

If visual artifacts are missing, generate them before writing a new prompt candidate.

## Required next package

Create a new evidence package before the next prompt candidate.

Recommended path:

```text
docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v025_visual_delta_prompt_recovery/
```

Required files:

```text
README.md
source_manifest.json
backend_preflight.json
visual_review_plan.md
visual_failure_taxonomy.md
v020c_v024l_delta_review.md
candidate_registry.json
comparison_matrix.md
comparison_matrix.json
final_recommendation.md
runs/
overlays/
diagnoses/
scripts/
fiftyone/
```

Do not modify product source truth while creating this package.

## Read order before work

Read these first:

```text
REVIEW_INDEX.md
z_reference_docs/GPT-Pro_collab/bda_svc_qwen_prompt_engineering_deep_research_bundle.md
z_reference_docs/GPT-Pro_collab/chatgpt_5_5_pro_prompt_engineering_handoff.md
REVIEW_REFRESH_2026-05-06.md
z_reference_docs/WORKING_CHANGELOG.md
z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md
z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md
z_reference_docs/PROJECT_BRAIN.md
docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v023_literal99_qwen_no_stop_continuation/pause_report_2026-05-06.md
docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v023_literal99_qwen_no_stop_continuation/final_recommendation.md
src/bda_svc/pipeline/config.yaml
```

## Source authority

Use this order:

```text
1. Explicit user direction.
2. Source artifacts, manifests, eval summaries, runner outputs, raw predictions, overlays/crops, and code.
3. Repo docs and prompt-lab evidence.
4. Graphify/project-brain/Mem0/Qdrant as navigation only.
5. External research as support only.
```

If these conflict, source artifacts win.

## Current v020c prompt surface

The live config contains the v020c-style detection prompt:

```text
CONTEXT SHADOW REVERSAL
GOOD FINAL BOX
BAD FINAL BOX
EXTRA-BOX AUDIT
FINAL BALANCE
```

Do not rewrite it wholesale.

Treat `v020c` as the incumbent prompt text. Use patch-like prompt changes unless explicitly ordered otherwise.

## Visual failure taxonomy

Before creating a candidate, classify errors into this taxonomy.

False positive classes:

```text
FP_DUPLICATE_SAME_BODY
FP_NESTED_FRAGMENT
FP_BROAD_ROW_GROUP_BOX
FP_CONTEXT_ONLY_SMOKE_DEBRIS_TERRAIN
FP_BUILDING_PIECE_FACADE_ROOF_SECTION
FP_ADJACENT_OFF_TARGET_OBJECT
FP_ROW_FORMATION_SPACING_CUE
FP_BOX_TOO_BROAD_TARGET_PLUS_CONTEXT
FP_REFERENCE_AMBIGUITY
FP_EVAL_MATCHING_ARTIFACT
FP_SCHEMA_RUNTIME_ARTIFACT
```

False negative classes:

```text
FN_SMALL_VALID_BODY_MISSED
FN_PARTLY_OCCLUDED_VALID_BODY_MISSED
FN_DENSE_ROW_UNDER_SPLIT
FN_LOW_CONTRAST_BODY_MISSED
FN_DAMAGED_BODY_INTERPRETED_AS_CONTEXT
FN_BUILDING_EXTERIOR_BODY_MISSED
FN_PROMPT_TOO_CONSERVATIVE
FN_REFERENCE_AMBIGUITY
FN_EVAL_MATCHING_ARTIFACT
FN_SCHEMA_RUNTIME_ARTIFACT
```

Dense-row classes:

```text
DENSE_TRUE_SEPARATE_TARGET
DENSE_DUPLICATE_ON_ONE_TARGET
DENSE_BROAD_GROUP_BOX
DENSE_ROW_SPACING_FALSE_CUE
DENSE_PARTIAL_OCCLUSION
DENSE_BOX_SPLIT_MERGE_AMBIGUITY
```

For every visual review note, include:

```text
case_id
candidate
target_type
match/fp/fn
failure_class
visual_evidence
prompt_addressable: yes/no/unclear
suggested_prompt_lever
risk_to_case_67
risk_to_155_166_office
```

## FiftyOne starting workflow

FiftyOne has not yet been employed. Start minimally.

Goal:

```text
Create a local visual review dataset comparing v020c and v024l against references.
```

Dataset fields:

```text
filepath
case_id
split_or_pack
ground_truth
v020c_predictions
v024l_predictions
v020c_eval
v024l_eval
dense_case_flag
control_case_flag
delta_tags
failure_notes
```

Implementation notes:

```text
FiftyOne uses normalized [x, y, width, height] boxes.
bda-svc/Qwen outputs use xyxy_1000.
Convert xyxy_1000 -> normalized xywh using image width/height or scale 1000 convention consistently with current eval code.
Do not change evaluation source truth while building this view.
```

Minimum views to create:

```text
view_v020c_fns
view_v020c_fps
view_v024l_added_fps
view_v024l_recovered_fns
view_dense_cases_66_67_84_97
view_case_67_delta
view_case_66_fp_heavy
view_case_84_recall_loss
view_controls_155_166_office
```

Use `evaluate_detections()` if compatible with existing labels. If the existing bda_eval matcher differs materially from FiftyOne's COCO-style matcher, keep bda_eval as authoritative and use FiftyOne for visualization and taxonomy only.

Required outputs from visual review:

```text
visual_failure_taxonomy.csv
v020c_v024l_delta_review.md
case_66_67_84_97_visual_notes.md
prompt_addressability_summary.md
```

## Prompt candidate rules after visual review

Each new candidate must satisfy:

```text
one primary hypothesis only
detect_objects only
placeholders preserved:
  {categories}
  {detection_guidance}
  {bbox_format}
  {bbox_scale}
JSON schema preserved
no assessment prompt changes
no doctrine changes
no runtime code changes unless explicitly approved
no source-truth mutation
no promotion without explicit approval
```

Candidate style:

```text
compact patch over v020c
prefer 1-3 sentence/bullet changes
avoid long building-only sections
avoid broad "do not detect buildings" style rules
avoid changing many concepts at once
avoid deleting load-bearing phrases unless testing a named ablation
```

Hard warning:

```text
Do not repeat v024n.
Any long building-only de-tiling or intact-building exclusion block is high-risk unless visual review proves the failure class is building-piece FPs and the candidate includes dense-row-safe constraints.
```

## Load-bearing phrase constraints

From current evidence:

```text
silhouette
exterior wall/roof boundary
```

were load-bearing in the v023s branch because removing either collapsed dense case 67.

Do not remove or weaken these without a named ablation and a case-67 guard.

`wheel/track contact` removal produced v024l, the best high-recall challenger, but did not solve FP burden. Treat this as learning evidence, not a universal rule.

## How to choose the next prompt base

Use this decision table after visual review.

### Continue from v020c when:

```text
v020c FPs are mostly context-only, duplicate, broad-row, or building-piece boxes.
v024l recovered few important true targets.
v024l added FPs are mostly not prompt-addressable.
The proposed change is precision cleanup without recall expansion.
```

Default next base: `v020c`.

### Continue from v024l when:

```text
v024l recovered true visually valid FNs that v020c missed.
v024l added FPs fall into one or two clearly prompt-addressable categories.
The FP problem can be addressed with a compact audit, not a broad rule block.
Case 67 held or improved under v024l-style wording.
```

Allowed but risky. Use only after visual delta review.

### Hybridize v020c and v024l when:

```text
v024l recovered a real visual cue missing from v020c.
v020c avoided a clear FP class that v024l created.
The hybrid can be expressed as one compact candidate with one recall cue and one audit guard.
```

### Do not branch from v024o

```text
v024o is partial/unscored.
If needed, rerun from scratch before using it as evidence.
```

## Candidate invalidation rules

A candidate is disqualified or learning-only if:

```text
case 155 fails
case 166 fails
office-negative fails
case 101 appears in no101 eval
manifest count wrong
run incomplete
JSON/runtime invalid
candidate modifies non-detect prompt surfaces without approval
candidate depends on partial v024o evidence
candidate improves recall but worsens combined FN+FP
candidate repeats v024n-style FP explosion
```

## Plateau and pivot rules

Prompt engineering remains first, but prompt wording search must be disciplined.

Run visual review before another prompt when:

```text
two consecutive candidates regress from v020c without a new diagnosed failure class
case 67 collapses in two variants from the same idea family
FPs rise by >=10 without enough FN reduction to improve combined error
a candidate creates FP explosion status
diagnosis says "likely duplicate/context/building piece" but no visual class was assigned
```

Pause and report when:

```text
incumbent replay drifts materially
backend is unavailable repeatedly
source artifacts conflict
visual artifacts are missing and cannot be generated
no prompt-addressable failure class remains
```

Research non-prompt levers as support when:

```text
visual review shows many FPs are duplicate/nested/same-body boxes
visual review shows dense-row behavior needs box clustering rather than wording
visual review shows broad boxes and tight boxes compete in ways a prompt cannot reliably solve
```

But do not implement non-prompt runtime changes unless user explicitly approves.

## Convert post-processing lessons into prompt tactics

Use post-processing concepts as prompt-design inspiration first:

```text
NMS -> "if two boxes describe the same connected body, keep one tighter whole-body box"
same-body suppression -> "do not output both whole target and fragment"
overlap clustering -> "do not box broad group when individual bodies are separable"
broad-box rejection -> "reject boxes that are mostly context around target body"
dense-row-safe exception -> "do not suppress neighboring boxes when separate visible body centers and edges exist"
visual verifier -> "use debug-only second pass or review, not final schema change"
```

Do not implement actual NMS/box clustering in runtime until user approves a non-prompt experiment lane.

## Recommended next sequence

### Step 0: Verify artifact situation

Check whether an actual Deep Research report exists.

If only the bundle exists, write in the new package README:

```text
Deep Research final report not present; current plan derived from bundle, repo evidence, and source snippets.
```

### Step 1: Build visual delta review

Create visual comparison for:

```text
v020c vs v024l
all_current_117_no101
dense cases 66, 67, 84, 97
controls 155, 166, office-negative
```

Answer:

```text
Which v020c FNs did v024l recover?
Which v024l FPs did v020c avoid?
What visual class are the added v024l FPs?
What visual class are the remaining v020c FPs?
What visual class are the remaining v020c FNs?
Which classes are prompt-addressable?
```

### Step 2: Candidate v025a: visual-delta micro hybrid

Only after Step 1.

Starting base:

```text
v020c unless visual review strongly proves v024l base is safer.
```

Candidate intent:

```text
Recover one v024l true-positive cue without importing v024l FP behavior.
```

Constraints:

```text
1 recall cue maximum
1 precision audit cue maximum
no building-only long block
preserve v020c structure
```

### Step 3: Candidate v025b: dense-safe duplicate/context audit

Use only if visual review shows FPs are mostly duplicates/context.

Intent:

```text
Reduce duplicate/context FPs while preserving dense separate bodies.
```

Must include dense-safe language:

```text
Do not suppress neighboring boxes when each has its own visible body center and visible body edge/boundary.
```

### Step 4: Candidate v025c: high-recall branch salvage

Use only if v024l recovered meaningful true targets and added FPs are visually classifiable.

Starting base:

```text
v024l
```

Intent:

```text
Keep v024l recovered FNs while removing its dominant FP class.
```

Disqualifier:

```text
If v024l added FPs span many unrelated classes, do not use v024l base.
```

### Step 5: Candidate v025d: diagnostic evidence-trace prompt

This is not automatically a production candidate.

Intent:

```text
Ask Qwen in a scratch/debug run to include rejected candidates or visible cue rationale only if the eval runner can support a non-production schema.
```

If schema cannot be extended, do not change output schema. Instead, run a separate visual verifier/debug script outside the main scored candidate.

## Required comparison matrix additions

Add columns:

```text
visual_review_done
dominant_fp_class
dominant_fn_class
prompt_addressable_class
base_prompt
candidate_axis
changed_lines_count
case_67_delta
v024l_recovered_fns_kept
v024l_added_fps_removed
notes
```

## Candidate diagnosis template

Every diagnosis must include:

```markdown
# Candidate Diagnosis: <candidate_id>

## Hypothesis
## Source base
## Exact prompt lever
## Changed lines summary
## Main metrics
## Control gates
## Dense cases
## Dominant FP classes
## Dominant FN classes
## What improved
## What regressed
## Case 67 behavior
## Visual evidence consulted
## Prompt-addressability judgment
## Lesson type
- general signal / local noise / source conflict / visual ambiguity / runtime artifact

## Next move
- continue from incumbent / continue from challenger / hybridize / visual review / pause
```

## Lesson classification

Do not convert every failure into prompt text.

Classify each lesson:

```text
GENERAL_SIGNAL: repeated across cases/slices and visually supported
LOCAL_NOISE: one case only, no broader pattern
SOURCE_CONFLICT: eval/source artifact inconsistent
VISUAL_AMBIGUITY: human review needed
RUNTIME_ARTIFACT: schema/JSON/backend/crop issue
NON_PROMPT_LEVER: likely duplicate suppression, NMS, tiling, or detector issue
```

Only `GENERAL_SIGNAL` should drive stable prompt candidates.

## Tool and MCP guidance

Use tools in this order:

```text
1. Local source artifacts and eval outputs.
2. Git/worktree checks.
3. Graphify/project-brain for navigation only.
4. Qdrant/Mem0 for recall only, if installed.
5. FiftyOne or generated overlays for visual review.
6. Web/OpenAI/Context7/Hugging Face/arXiv/Semantic Scholar for research support only.
```

Suggested MCP use:

```text
Qdrant MCP:
  Retrieve prior Prompt_Labs lessons, but never as source truth.

FiftyOne MCP or local FiftyOne:
  Build visual review, slice false positives/false negatives, inspect boxes.

Hugging Face MCP:
  Research Qwen/Gemma/model grounding behavior only when model/backend questions arise.

Context7/OpenAI Docs MCP:
  Use before changing Python, eval tooling, Codex skills, OpenAI-compatible runtime, structured outputs, or MCP setup.

Git/GitHub MCP:
  Verify branch/worktree state and source diffs.

Sequential Thinking:
  Use for planning checkpoints only, not evidence.
```

## What not to do

Do not:

```text
promote v024l
score v024o
resume v024o partial predictions
add long building-only exclusion blocks
change assessment prompt
change doctrine
change runtime code
change eval ground truth
change no101 manifest semantics
use Graphify/Mem0/Qdrant as evidence
batch-write many final prompts before running
claim Deep Research final report exists unless actual report is present
```

## Acceptance criteria for next package

The next package is successful if it produces:

```text
1. Confirmed source state.
2. v020c and v024l prediction paths found.
3. visual_failure_taxonomy.csv completed for priority slices.
4. v020c_v024l_delta_review.md completed.
5. one candidate authored only after visual review.
6. candidate run completed on main pack and office-negative guard.
7. comparison matrix updated.
8. diagnosis written before next candidate.
9. no source truth mutation.
```

## Minimum prompt for a new candidate

Before authoring candidate, Codex must fill this:

```text
Candidate ID:
Base prompt:
Dominant visual failure class:
Prompt-addressable reason:
One-sentence hypothesis:
Exact text region to change:
Expected metric movement:
Expected dense-case risk:
Expected FP risk:
Expected FN risk:
Stop/disqualifier rule:
```

If this cannot be filled, do not author the candidate.

## Bottom line

The next gain is not from "more clever wording" alone.

The next gain is from making the recursive loop visually grounded:

```text
metrics -> visual taxonomy -> compact prompt hypothesis -> fixed eval -> diagnosis -> updated lesson
```

Keep prompt engineering first. Use visual review to aim the prompt work. Use post-processing theory only as prompt inspiration or future pivot evidence. Preserve v020c until a candidate beats it on combined FN+FP and passes controls.
