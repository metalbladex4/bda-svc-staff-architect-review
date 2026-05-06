# Reference Master Index

This file is the main routing document for the local reference material in
`z_reference_docs`.

Generated: `2026-04-21T23:21:50-04:00`

## How To Use This Index

Use this file when you want to answer:

- which reference family should I open first
- which detailed index should I use next
- which specific document is most relevant to a doctrine, prompting, grounding,
  or capstone-documentation question

This file is intentionally more granular than a simple folder map, but it is
still a routing document rather than a full document-by-document commentary on
every single source file.

## Index Routing Guide

If you need the full doctrine list:
- start with `z_reference_docs/BDAs/BDAs_INDEX.md`

If you need the current Phase-1 doctrine audit and shadow-replacement package:
- start with
  `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/README.md`

If you want the paste-ready ChatGPT Deep Research prompts for MCP-server and
tokenization research tied to this project:
- start with
  `z_reference_docs/CHATGPT_DEEP_RESEARCH_PROMPTS_MCP_AND_TOKENIZATION.md`

If you want the external Codex subagent catalog analysis, the global vendor
path, and the Capstone-specific shortlist from `awesome-codex-subagents`:
- start with
  `z_reference_docs/CODEX_SUBAGENT_CATALOG_ANALYSIS.md`

If you want the portable Codex capability playbook for another project:
- start with `z_reference_docs/CODEX_CAPABILITY_TRANSFER_DOSSIER.md`
- use it to transfer MCP routing, skills, subagent discipline, AGENTS layering,
  Graphify/project-brain patterns, evidence workflows, memory citations, and
  live-document habits without copying Capstone-specific paths verbatim
- for the incoming MediaLab-derived comparison dossier, read
  `z_reference_docs/The_Incomming_CODEX_CAPABILITIES_DOSSIER.md` as the source
  of adopted/adapted/deferred ideas now summarized in the transfer dossier

If you need the current global Codex tooling overlay that now guides repo-local
work:
- start with `/home/williambenitez1/.codex/AGENTS.md`
- then use `/home/williambenitez1/.codex/MCP_USAGE_GUIDE.md`
- for canonical installed-tool names, risk labels, Mem0 boundaries, and future
  spences10 `available_tools`/`recommended_tools` inputs, use
  `/home/williambenitez1/.codex/TOOL_INVENTORY.md`,
  `/home/williambenitez1/.codex/tool_inventory.json`, and the Capstone overlay
  at `/home/williambenitez1/Capstone/TOOL_INVENTORY.md`
- `sequential-thinking` is active and implemented by Spences10
  `mcp-sequentialthinking-tools`; `mcpfinder` is active as an approval-gated
  missing-MCP discovery scout. NCP / Natural Context Provider remains the
  future/planned/deferred MCP router candidate after Wave 5B confirmed `run`
  exposure. Use the global MCP usage guide and canonical tool inventory for
  current routing boundaries.
- `mem0` is active as durable advisory memory only; it is manual,
  approval-gated for writes/deletes, and separate from Graphify/project-brain,
  native/project memory, and the existing MCP `memory` server
- `superpowers-skill-pack` is active as a global Codex skill pack from
  `obra/superpowers` `v5.0.7`; use it in Capstone-adapted mode for workflow
  scaffolding only, not as source truth, promotion authority, automatic
  subagent routing, or an override of existing prompt/eval gates
- for the global guarded Graphify prompt-submit reminder, inspect
  `/home/williambenitez1/.codex/hooks.json` and
  `/home/williambenitez1/.codex/hooks/user_prompt_submit_graphify_reminder.py`
- for the installed custom-agent subset and refresh provenance, use:
  `/home/williambenitez1/.codex/agents/VENDOR_MANIFEST.md`
- for visual BDA dataset/case review, use the `fiftyone` MCP only when the
  task explicitly needs local image/sample/bounding-box inspection; deterministic
  scoring and promotion authority still come from `bda_eval`, runner summaries,
  manifests, reference JSON, and promotion reports

If you need local-only Graphify routing:
- start with `z_reference_docs/PROJECT_BRAIN.md`
- use `.graphify_fleet/corpus/` or MCP `capstone-architecture-graph` for
  architecture, worktree-map, dependency, code-path, detector/eval
  implementation, and "how does this code connect?" questions
- use `.graphify_project_brain/corpus/` or MCP `capstone-project-brain` for
  experiment history, Qwen/Gemma status, architect-feedback rollout, promotion
  path, decisions, and rationale
- review `.graphify_fleet/corpus/graphify-out/GRAPH_REPORT.md` for the
  architecture graph
- review `.graphify_fleet/corpus/graphify-out/FLEET_KNOWLEDGE_REPORT.md` for
  the architecture/fleet semantic report; the older
  `PROJECT_BRAIN_REPORT.md` filename is only a compatibility alias there
- review
  `.graphify_project_brain/corpus/graphify-out/PROJECT_KNOWLEDGE_REPORT.md`
  for the project-knowledge brain
- use `.graphify_project_brain/corpus/graphify-out/wiki/index.md` as the
  generated agent-readable project-brain wiki
- use each graph's `capstone_benchmark_report.md` to see whether Graphify is
  high-signal for the question class before relying on graph recall
- use `.graphify_project_brain/corpus/graphify-out/memory/verified/` only for
  source-verified query notes that should become reusable local memory
- for project-state, promotion, evidence, and decision questions, start with
  `.graphify_project_brain/capstone_graphify.py recall` before broad
  `graphify query`; use `recall-benchmark` after retrieval changes to confirm
  expected trusted-note and semantic-seed hits still work
- use `.graphify_project_brain/capstone_graphify.py recall --deep` or
  `.graphify_project_brain/capstone_graphify.py search-all` only for broader
  discovery across notes, seeds, wiki, graph, and evidence-index hits; these
  commands label trust level and keep generated/wiki/index results separate
  from source-verified memory
- use `.graphify_project_brain/capstone_graphify.py doctor` for a local health
  check and `.graphify_project_brain/capstone_graphify.py update` for a full
  profile refresh
- use `.graphify_project_brain/capstone_graphify.py doctor --strict-stale`
  when graph freshness should be enforced before acting
- use `.graphify_project_brain/capstone_graphify.py evidence-index` and
  `.graphify_project_brain/capstone_graphify.py analytics` for local-only
  SQLite/DuckDB evidence query surfaces
- use `.graphify_project_brain/capstone_graphify.py estimate-extraction` to
  size broad safe-corpus LLM extraction before any future approval to run it
- use the generated GraphML exports only as local interoperability artifacts:
  `.graphify_fleet/corpus/graphify-out/capstone_architecture_graph.graphml`
  and
  `.graphify_project_brain/corpus/graphify-out/capstone_project_brain.graphml`
- treat graph output as a navigation aid and verify important claims against
  source files, manifests, decision notes, or runner artifacts

If you need the reference-organization and archive roadmap:
- start with `z_reference_docs/zz_archive/README.md`
- use `z_reference_docs/zz_archive/ORGANIZATION_INVENTORY.md` for the current
  hot/warm/cold/archive classification
- use `z_reference_docs/zz_archive/PROPOSED_MOVE_MANIFEST.csv` before any
  later approved move wave
- use `z_reference_docs/zz_archive/REDUNDANCY_REVIEW.md` for overlap and
  consolidation candidates
- use `z_reference_docs/zz_archive/GRAPHIFY_ARCHIVE_INDEX.md` for Graphify
  generated-history cleanup planning and status
- use `z_reference_docs/zz_archive/data_set_storage/` before any future
  `Data_set_Storage` cleanup or archive wave
  - use
    `z_reference_docs/zz_archive/data_set_storage/DATA_SET_REPORT_PROVENANCE_REVIEW.md`
    before touching `DATA_SET/Reports_(OLD)/` or
    `DATA_SET/Updated_Reports/`
  - use
    `z_reference_docs/zz_archive/data_set_storage/EMPTY_FOLDER_CLEANUP_REVIEW.md`
    before deleting or moving empty `Data_set_Storage` folders
- use `z_reference_docs/zz_archive/indexed_existing_archives/` for central
  registration indexes of archive folders that remain in their original
  locations
- Phase 0 created planning/index artifacts only
- Phase 1 moved the approved loose local-doc files into `zz_archive`
- Phase 2 moved only ignored Graphify generated-history folders into
  `.graphify_project_brain/archive/`; source files, Prompt_Labs evidence,
  human-report data, current graphs, trusted seeds, and worktrees stayed hot
- Phase 3 registered existing archive-like folders without moving them:
  `Prompt_Labs/archive/` and
  `Prompting/Model_research-Archive-Not-to-be Used/`
- Phase 4 completed the redundancy/consolidation review as a recommendation
  package only; no active docs were merged or moved, and proposed future rows
  remain unapproved
- SequentialThinking trigger policy is now canonical in the global AGENTS file,
  with Capstone-specific triggers in the Capstone root AGENTS overlay; use it as
  a compact checkpoint for genuinely complex or risky work, not merely because
  Plan Mode is active
- Phase 5 completed the `Data_set_Storage` data-path audit only; no images,
  reports, data folders, Prompt_Labs evidence, worktrees, source files, or
  Graphify outputs moved
- Phase 5A completed the `DATA_SET` old-vs-updated report provenance review
  only; it found `Updated_Reports/` is a partial structured-conversion lane,
  not a clean authoritative replacement
- Phase 5B completed the empty-folder cleanup review only; it found seven
  empty-folder candidates and recommended no deletion or move until a later
  explicit cleanup approval
- After explicit approval, only the empty `RoboFlow_/` placeholder was removed;
  use
  `z_reference_docs/zz_archive/data_set_storage/ROBOFLOW_EMPTY_FOLDER_CLEANUP.md`
  for the cleanup record and rollback command

If you need the new human-written report/image dataset intake and audit:
- start with
  `z_reference_docs/human_report_dataset_audit/HUMAN_REPORT_DATASET_INTAKE_AND_AUDIT.md`
- then review
  `z_reference_docs/human_report_dataset_audit/HUMAN_REPORT_DATASET_VISUAL_AUDIT.md`
  for the first-pass visual findings and the current active/held-out split
- for the approved prompt-example semantic index, use
  `z_reference_docs/human_report_dataset_audit/APPROVED_HUMAN_REPORT_EXAMPLES.md`
  and
  `z_reference_docs/human_report_dataset_audit/approved_human_report_examples_index.json`
  - this is also routed as the `human_report_examples` Graphify extraction
    shard
  - use this deterministic semantic index first; do not start agent/subagent
    extraction unless retrieval or prompt work proves the index too shallow
- use
  `z_reference_docs/human_report_dataset_audit/human_report_dataset_intake_summary.json`
  for active image/report counts, deterministic bbox/schema issue IDs, and
  visual-audit status counts
- use
  `z_reference_docs/human_report_dataset_audit/human_report_dataset_audit_ledger.csv`
  as the working audit ledger
- proposed draft/correction queue files live under
  `z_reference_docs/human_report_dataset_audit/proposed_corrections/`
- source images and reports live under
  `z_reference_docs/Data_set_Storage/human_reports/`
- held-out images and removed reports live under
  `z_reference_docs/Data_set_Storage/human_reports/no_reports/`
- the current active prompt-example candidate pool is `112` usable reports:
  `99` first-pass accurate plus `13` accepted after user review
- for broader `Data_set_Storage` organization and future path-move risk, start
  with `z_reference_docs/zz_archive/data_set_storage/DATA_PATH_AUDIT.md`
  before touching any source dataset path
- for older `DATA_SET` report provenance, use
  `z_reference_docs/zz_archive/data_set_storage/DATA_SET_REPORT_PROVENANCE_REVIEW.md`;
  do not treat `Reports_(OLD)/` or `Updated_Reports/` as current prompt-example
  truth without a later repair/review package
- for empty dataset-folder cleanup readiness, use
  `z_reference_docs/zz_archive/data_set_storage/EMPTY_FOLDER_CLEANUP_REVIEW.md`;
  Phase 5B did not delete or move any empty folder, and the later approved
  cleanup removed only `RoboFlow_/`
- for corrected human-report prompt gates, use
  `human_report_challenge_v2` rather than the historical v1 lane:
  - source-refresh package:
    `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/source_refresh/human_report_challenge_v2_refresh/`
  - automation framework:
    `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/`
  - `155` and `166` are positive military-equipment cases in v2, not
    protected negatives; `166` remains holdout-only unless separately approved
  - current abstention guard is the separate legacy `office-negative` control
  - latest v2 source state has `118` approved pairs and `231` report objects;
    updated/recovered report cases `40`, `61`, `65`, `69`, `70`, `77`, `106`,
    `125`, `172`, and `187` are represented in current v2 references
  - the six recovered additions `40`, `65`, `106`, `125`, `172`, and `187`
    now have fresh v009/v014 baseline coverage in the current v2 source-refresh
    package
  - current automation must use the current v2 manifest and updated-report
    smoke manifest, not stale all-112 assumptions
  - first live v2 automation result, `v017a`, is a near miss, not a winner or
    promotion candidate
  - `v017a` Superpowers reassessment and consumed next-axis recommendation:
    `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/reassessments/v017a_superpowers_reassessment/`
    - consumed axis: `v017b_single_target_box_span_self_filter`
  - latest `v017b` bounded live run and diagnosis:
    `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/runs/v017b/live_2026-05-03_032920Z/`
    and
    `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/reassessments/v017b_gate_result/`
    - `v017b` is a near miss, not a winner: aggregate hinge checks,
      changed-source sanity, updated-report smoke, positive `155`, and
      `office-negative` abstention held, but case `101` still emitted one broad
      group/scene box `[75, 58, 1000, 547]`
    - no `v017c`, dev, holdout, all-112, promotion, runtime adoption,
      source-truth mutation, or structural guard implementation is approved by
      the `v017b` result
  - Superpowers adoption note for this lane:
    `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/superpowers_adoption/README.md`
- for the global creature-friendly Codex instruction override, use
  `/home/williambenitez1/.codex/AGENTS.md` and
  `/home/williambenitez1/.codex/MCP_USAGE_GUIDE.md`; the active file is
  `/home/williambenitez1/.codex/model_instructions/gpt-5.5-creatures-free.txt`
  and it does not replace Capstone source-truth or approval boundaries

If you need the new cross-branch Qwen detect-surface inspection before another
Qwen detect-only cycle:
- start with
  `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detection_prompt_surface_inspection.md`

If you need the full prompting/reference list:
- start with `z_reference_docs/Prompting/PROMPTING_MASTER_INDEX.md`

If you want the Gemma 4 local evidence pack and source manifest:
- start with `z_reference_docs/Prompting/Google_Gemma/Gemma_4/README.md`

If you only want PDF-derived prompting Markdown companions:
- start with `z_reference_docs/Prompting/PROMPTING_PDFS_INDEX.md`

If you want experiment-driven research notes that explain how one failed run
turned into the next prompt revision:
- start with `z_reference_docs/Prompting/Research_Loops/README.md`

If you want the active prompt-experiment state:
- start with `z_reference_docs/Prompt_Labs/PROMPT_LABS_INDEX.md`

If you want the formal post-architect Qwen adaptive follow-up protocol for
multi-attempt cycles and confirmation replays:
- start with
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/cycles/README.md`

If you want the completed Qwen building-reference truth audit, corrected replay,
and historical promotion-readiness evidence for `v014`:
- start with
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/decisions/qwen_1_2_building_reference_truth_audit_2026-04-23.md`
- then review
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runner_sessions/executions/qwen_1_2_v014_detect_weighted_building_selection_session_v1_2026-04-23_212114Z/runner_session_summary.json`
- and
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/decisions/qwen_1_2_v014_promotion_readiness_review_2026-04-23.md`
- for the Step 1 formal package, use
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/decisions/qwen_1_2_v014_formal_promotion_package_2026-04-27.md`
  and
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/promotion_reports/v014_detect_weighted_building_selection_pending_promotion.yaml`
  and remember this package is now paused/superseded by the human-report-informed
  comparison process

If you want the current Qwen `v009` vs `v014` human-report-informed comparison
and `v015` planning gate:
- start with
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/decisions/qwen_1_2_human_report_informed_v009_v014_comparison_plan_2026-04-28.md`
- then review
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/human_report_challenge_v1/executions/qwen_v009_vs_v014_all_112_2026-04-28_022159Z/comparison_summary.md`
  and
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/human_report_challenge_v1/executions/qwen_v009_vs_v014_all_112_2026-04-28_022159Z/slice_comparison_summary.md`
- use the challenge-lane context in
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/human_report_challenge_v1/README.md`
  and
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/human_report_challenge_v1/doctrine_grounding_report.md`
- then use the worktree-only `v015` strategy package at
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/README.md`
  for the failure taxonomy, stratified dev/holdout split, offline example bank,
  v015a-v015e prompt-candidate evidence, the v016 reference-aware design
  package, the blocked v016a expanded-hinge result, and the current next-step
  decision to build a `v016a` failure synthesis plus `v016b` prompt-axis
  decision package before another prompt authoring/run. This package remains
  worktree-only prompt-lab evidence, not runtime adoption or promotion truth.

If you want the recorded first detector-backend pilot comparison and decision:
- start with
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.4_feat__qwen3-vl-8b-instruct__detector-backend-pilot/experiments/decisions/qwen_detector_backend_strategy_phase7.md`

If you want the live prompt-method record:
- start with `z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`

If you want the teaching-grade, capability-first guide for reproducing this
workflow:
- start with `z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`

If you want the current overall project state and plan:
- start with `z_reference_docs/WORKING_CHANGELOG.md`

If you want the short completed-vs-deferred read on the staff-architect
feedback rollout:
- start with `z_reference_docs/ARCHITECT_FEEDBACK_COMPLETION_CHECKLIST.md`

If you want the architect-facing implementation narrative that explains how the
recommendations were actually carried out, where we adapted them, what
experiments were run, and what we now want reviewed next:
- start with `z_reference_docs/ARCHITECT_IMPLEMENTATION_PROGRESS_REPORT.md`

If you want the whole-program technical deep dive, experiment ledger, worktree
inventory, and extensibility/customization map:
- start with `z_reference_docs/PROGRAM_DEEP_DIVE_AND_EXTENSIBILITY_REPORT.md`
- then use `z_reference_docs/PROGRAM_EXPERIMENT_LEDGER.md`
- and `z_reference_docs/PROGRAM_FILE_AND_WORKTREE_INVENTORY.md`

If you want the safe branch/worktree update procedure for future upstream syncs:
- start with `z_reference_docs/GIT_WORKTREE_UPDATE_WORKFLOW.md`

If you need the canonical volatile worktree-state contract or the local
preservation validator that now protects future upstream refreshes:
- start with `z_reference_docs/WORKTREE_STATE.yaml`
- then use `z_reference_docs/local_tools/validate_worktree_state.py`

If you want the local prompt-lab integrity wrapper that can dispatch to the
Qwen or Gemma worktree validators:
- start with `z_reference_docs/local_tools/validate_prompt_lab_integrity.py`

If you want the copy-paste command checklist for the current Qwen branch line:
- start with `z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_QWEN.md`

If you want the copy-paste command checklist for the current Gemma branch line:
- start with `z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_GEMMA.md`

If you want Phase 3 capstone-document context:
- start with `z_reference_docs/capstone_tech_docs/understanding_tracking.md`

## Quick Search

Use these from `/home/williambenitez1/Capstone`:

```bash
rg -n "combat assessment|battle damage|physical damage|functional damage" z_reference_docs/BDAs
rg -n "system prompt|few-shot|examples|xml|long context|output format" \
  z_reference_docs/Prompting/Anthropic_Claude \
  z_reference_docs/Prompting/Google_Gemma \
  z_reference_docs/Prompting/OpenAI_GPT \
  z_reference_docs/Prompting/Google_Gemini
rg -n "bbox|bounding box|grounding|spatial|ocr|document parsing" \
  z_reference_docs/Prompting/Qwen \
  z_reference_docs/Prompting/google_owlv2-base-patch16-ensemble \
  z_reference_docs/Prompting/VLM-Research-Papers
rg -n "case_id|Version|damage_category|confidence_level|winner" \
  z_reference_docs/Prompt_Labs
rg -n "deployment|verification|local tests|model documentation" \
  z_reference_docs/capstone_tech_docs
```

## Folder Index

- `z_reference_docs/BDAs/`
  Doctrine, targeting, combat assessment, and BDA methodology references.
- `z_reference_docs/Prompting/`
  Prompting guides, model cards, cookbooks, model-specific notes, and research
  papers.
- `z_reference_docs/Prompt_Labs/`
  Local-only prompt iteration workspaces, eval manifests, and experiment logs.
- `z_reference_docs/Doctrine_Experiments/`
  Local-only doctrine audits, replacement candidates, and branch test playbooks.
- `z_reference_docs/capstone_tech_docs/`
  Capstone deliverables, templates, presentations, and tech-doc understanding
  notes.

Primary indexes:
- `z_reference_docs/BDAs/BDAs_INDEX.md`
- `z_reference_docs/Prompting/PROMPTING_MASTER_INDEX.md`
- `z_reference_docs/Prompting/PROMPTING_PDFS_INDEX.md`
- `z_reference_docs/Prompting/Research_Loops/README.md`
- `z_reference_docs/Prompt_Labs/PROMPT_LABS_INDEX.md`
- `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/README.md`
- `z_reference_docs/capstone_tech_docs/understanding_tracking.md`

## Top-Level Support Files

These are support/context files, not primary doctrine or prompting authorities.

- `z_reference_docs/zz_archive/research/model_shortlists/Notes_2026-04-28.txt`
  Tags: personal notes, working context
- `z_reference_docs/zz_archive/backups/configs/config.yaml.backup`
  Tags: prior model config snapshot, backup reference
- `z_reference_docs/Capstone-Project.code-workspace`
  Tags: saved workspace, main repo plus active worktree root
- `z_reference_docs/zz_archive/workspaces/Capstone.code-workspace`
  Tags: archived smaller workspace, main repo only
- `z_reference_docs/zz_archive/codex_agents/Prompt_to_Start_up_agents_in_new_project_2026-04-28.txt`
  Tags: archived AGENTS planning prompt, superseded by current AGENTS layers
- `z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
  Tags: living prompt methodology, source usage, experiments, prompt decisions
- `z_reference_docs/PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`
  Tags: capability-first teaching guide, reproducible prompt workflow, branch-aware method
- `z_reference_docs/AGENTS.md`
  Tags: local AGENTS spec, canonical template, worktree guidance, instruction baseline
- `z_reference_docs/WORKING_CHANGELOG.md`
  Tags: running project understanding, current way forward, meaningful changes
- `z_reference_docs/PROJECT_BRAIN.md`
  Tags: project brain, Graphify, knowledge graph, architecture map, worktree map, verification rules
- `z_reference_docs/ARCHITECT_FEEDBACK_COMPLETION_CHECKLIST.md`
  Tags: architect review status, completed phases, intentionally deferred work, rollout closeout
- `z_reference_docs/ARCHITECT_IMPLEMENTATION_PROGRESS_REPORT.md`
  Tags: architect-facing implementation narrative, recommendation response, experiment ledger, worktree-vs-main rationale, next-review questions
- `z_reference_docs/PROGRAM_DEEP_DIVE_AND_EXTENSIBILITY_REPORT.md`
  Tags: whole-program deep dive, worktree map, runtime architecture, evaluation architecture, tooling, extensibility, current Qwen lane
- `z_reference_docs/PROGRAM_EXPERIMENT_LEDGER.md`
  Tags: experiment ledger, Qwen runs, Gemma runs, backend pilot, doctrine shadow, cause-and-effect analysis, current Codex assessment
- `z_reference_docs/PROGRAM_FILE_AND_WORKTREE_INVENTORY.md`
  Tags: file inventory, worktree inventory, prompt-lab run roots, Codex customization, AGENTS, skills, subagents, secret boundary
- `z_reference_docs/GIT_WORKTREE_UPDATE_WORKFLOW.md`
  Tags: git workflow, worktree refresh procedure, upstream sync safety, full parity completion
- `z_reference_docs/WORKTREE_STATE.yaml`
  Tags: canonical volatile state, branch direction contract, shadow-lane semantics, protected invariants, upstream refresh preservation
- `z_reference_docs/local_tools/validate_worktree_state.py`
  Tags: local validator, worktree governance, state-contract checks, preservation gate
- `z_reference_docs/local_tools/validate_prompt_lab_integrity.py`
  Tags: local validator wrapper, prompt-lab integrity, overlay contracts, model-line dispatch
- `z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_QWEN.md`
  Tags: qwen branch checklist, copy-paste commands, upstream refresh steps, smoke validation
- `z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_GEMMA.md`
  Tags: gemma branch checklist, copy-paste commands, upstream refresh steps, smoke validation, ollama host override
- `z_reference_docs/CHATGPT_DEEP_RESEARCH_PROMPTS_MCP_AND_TOKENIZATION.md`
  Tags: ChatGPT Deep Research prompts, MCP server research, tokenization theory, prompt-language research, local support bundle
- `z_reference_docs/CODEX_SUBAGENT_CATALOG_ANALYSIS.md`
  Tags: Codex subagents, vendor catalog, selective activation, global tooling, external reference analysis
- `z_reference_docs/CODEX_CAPABILITY_TRANSFER_DOSSIER.md`
  Tags: portable Codex playbook, MCP routing, skills, subagents, AGENTS layers, Graphify, memory citations, evidence workflow
- `z_reference_docs/The_Incomming_CODEX_CAPABILITIES_DOSSIER.md`
  Tags: incoming Codex playbook, MediaLab comparison, Graphify hook pattern, graph lane taxonomy, adoption source
- `z_reference_docs/Prompt_Labs/AGENTS.md`
  Tags: prompt-lab instructions, local experimentation, promotion discipline, private workflow guardrails
- `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/README.md`
  Tags: phase-1 doctrine audit, replacement candidate, doctrinal crosswalk, local-only A/B experiment
- `z_reference_docs/Prompting/Research_Loops/README.md`
  Tags: experiment-linked research notes, critique-to-revision workflow
- `z_reference_docs/capstone_tech_docs/understanding_tracking.md`
  Tags: capstone deliverables understanding, phase tracking, deployment-doc context
- `z_reference_docs/capstone_tech_docs/Deliverables_Phase_3_(S26-P1)/Deployment procedure Draft.docx`
  Tags: Phase 3 deployment procedure draft, upstream/main deployment, team-facing document

Maintenance note:
- `PROMPT_DEVELOPMENT_METHODOLOGY.md` should be revisited periodically during
  prompt work, especially when method, direction, or prompt-promotion decisions
  change in a meaningful way.
- The git/worktree reset on `2026-04-15` established a clean mirrored `main`
  at upstream commit `28e863b`, preserved the older local line on
  `snapshot/2026-04-15-pre-main-reset`, and introduced a new branch-structured
  prompt-lab root at `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/`.
- A later upstream sync moved mirrored `main` again to `c19940a`.
- The earlier active prompt workflow remains preserved in the legacy lab
  `z_reference_docs/Prompt_Labs/2.main__qwen3-vl-8b-instruct/`.
- The earlier `q8_0` prompt work now lives in
  `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/`.
- The earlier `28e863b` upstream sync mostly added image-aware evaluation
  features in `bda_eval/` and one live detect-objects safeguard line against
  all-zero non-null boxes in `src/bda_svc/pipeline/config.yaml`.
- The latest upstream sync moved the repo baseline to `c19940a` and changed
  only CI/container infrastructure:
  - `.github/workflows/ci.yml`
  - `docker/Dockerfile`
- The first fresh branch-aware baseline has now been recorded under
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/`
  and should be treated as the active `28e863b` baseline anchor for new work
  on that feature line.
- The active Qwen and Gemma worktrees have now been refreshed through
  `c19940a` without rebuilding their prompt baselines, because that newer
  upstream delta did not change live prompt/runtime semantics.
- The refresh docs now explicitly treat “clean rebase” and “full parity
  completion” as different milestones.
- The workflow/checklist layer now defines the standard post-refresh smoke
  recipe and expects active model branches to remain reusable smoke-capable
  roots, not just ancestry placeholders.
- The active prompt workflow now also generates paired research notes under
  `z_reference_docs/Prompting/Research_Loops/`.
- The active detection-localization loop now has research notes for `v004`,
  `v005`, and `v006`, plus a completed cycle summary under the active prompt
  lab.
- The active downstream-calibration loop now also has research notes for
  `v007`, `v008`, and `v009`, plus a second cycle summary under the active
  prompt lab.
- The active grounding-recovery work now also includes a `v010` prep note, a
  `v010` post-failure research note, and a queued `v011` recovery candidate in
  the active prompt lab.
- The active branch-aware Qwen line now also has:
  - the last confirmed staged `v009` winner preserved in the prompt lab
  - a local tracked feature-branch config now carrying an exploratory detect-only `v010` candidate
  - an open PR `#134` against `upstream/main`
  - green GitHub CI after the workspace-package install fix
- The active next model-line bootstrap is now anchored on:
  - `model/gemma4-e4b`
  - `feat/gemma4-e4b/qwen-v009-workflow-bootstrap`
  - `z_reference_docs/Prompting/Google_Gemma/Gemma_4/`
  - `z_reference_docs/Prompt_Labs/3_gemma4-e4b/`
- That Gemma line now also has a completed first live `v000` run under:
  - `z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/v000/run01_2026-04-17_134308_EDT/`
- The current local doctrine-replacement effort is now anchored on:
  - `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/`
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/`
  - `z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.2_feat__gemma4-e4b__doctrine-bda-alignment/`
- The next Qwen follow-up after the doctrine-only stall is now also recorded
  under:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/detect_surface/run01_2026-04-20_200611_EDT/`
  - `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detect_candidate_a_run01_review.md`
- The next detect-only Qwen follow-up after that promising partial win is now
  also recorded under:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/detect_surface/run02_2026-04-20_204540_EDT/`
  - `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detect_candidate_b_run02_review.md`
- The next example-structured Qwen detect-only follow-up after that is now
  also recorded under:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/detect_surface/run03_2026-04-20_224812_EDT/`
  - `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detect_candidate_c_run03_review.md`
- The next hierarchy-first Qwen detect-only follow-up after that is now also
  recorded under:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runs/detect_surface/run04_2026-04-20_233900_EDT/`
  - `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detect_candidate_d_run04_review.md`
- Prompt-behavior claims for that active working config still rely primarily on the
  local prompt-lab evidence chain; GitHub CI validates branch/runtime health,
  not exact prompt-lab parity.
- The repo-local doc system now also assumes a global Codex tooling overlay in:
  - `/home/williambenitez1/.codex/AGENTS.md`
  - `/home/williambenitez1/.codex/MCP_USAGE_GUIDE.md`
  - `/home/williambenitez1/.codex/agents/VENDOR_MANIFEST.md`

## Prompt Labs

Primary index:
- `z_reference_docs/Prompt_Labs/PROMPT_LABS_INDEX.md`

Current working labs:
- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/`
  Tags: branch-structured qwen lab root, centralized model-first docs layout
- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1_model__qwen3-vl-8b-instruct/`
  Tags: model branch root, clean mirrored-main descendant, future qwen model-line work, smoke-capable reusable root
- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/`
  Tags: first feature branch root, dedicated worktree, post-reset grounding work, `v009` tracked control, `v014` promotion paused by human-report comparison, completed building-reference correction replay
- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/`
  Tags: qwen doctrine A/B branch root, phase-1 doctrine replacement, local-only control comparison, detect-surface verification lane
- `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_destroyed_building4_manual_review.md`
  Tags: qwen doctrine manual review, destroyed_building4 tradeoff, BDA text vs held control
- `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/qwen_detect_candidate_a_run01_review.md`
  Tags: qwen detect follow-up, mirrored prompt-surface candidate, destroyed_building4 recovery, doctrine-vs-prompt lever read
- `z_reference_docs/Prompt_Labs/3_gemma4-e4b/`
  Tags: gemma4 local-first branch root, active next model-line bootstrap
- `z_reference_docs/Prompt_Labs/3_gemma4-e4b/3_model__gemma4-e4b/`
  Tags: long-lived gemma model branch root, reusable workflow inheritance point, smoke-capable reusable root
- `z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/`
  Tags: first gemma feature branch root, qwen-v009 workflow bootstrap, first live v000 run recorded
- `z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.2_feat__gemma4-e4b__doctrine-bda-alignment/`
  Tags: gemma doctrine A/B branch root, phase-1 doctrine replacement, local-only control comparison

Legacy working labs:
- `z_reference_docs/Prompt_Labs/2.main__qwen3-vl-8b-instruct/`
  Tags: preserved pre-reset prompt iteration history, snapshot-associated legacy lab

Archived labs:
- `z_reference_docs/Prompt_Labs/archive/1.main__qwen3-vl_8b-instruct-q8_0/`
  Tags: archived prior model-tag sequence, historical runs, superseded prompt versions

## BDAs

Primary index:
- `z_reference_docs/BDAs/BDAs_INDEX.md`

### BDA Questions To Start From

If you are asking which BDA/doctrine file to open first, start from the
question you are trying to answer rather than from the branch of doctrine it
belongs to.

#### If You Are Defining Combat Assessment Methodology Or Terminology

Start here:
- `z_reference_docs/BDAs/CJCSI 3162.02A METHODOLOGY FOR COMBAT ASSESSMENT July 2021.md`
- `z_reference_docs/BDAs/Methodology For Combat Assessment.md`

Use this when the question is:
- what PDA, FDA, or target system assessment mean
- how combat assessment is structured doctrinally
- what phase boundaries or doctrinal definitions should control our outputs

#### If You Are Framing Physical-Damage Assessment Versus Functional Or Broader Effects

Start here:
- `z_reference_docs/BDAs/CJCSI 3162.02A METHODOLOGY FOR COMBAT ASSESSMENT July 2021.md`
- `z_reference_docs/BDAs/Fusing Data Into a BDA for the Commander.md`

Use this when the question is:
- what we can say safely from visible evidence alone
- where physical damage ends and broader assessment begins
- how to keep summary language from drifting into unsupported effects claims

#### If You Are Looking For Broader Targeting Context

Start here:
- `z_reference_docs/BDAs/jp3_60 Joint Targeting.md`
- `z_reference_docs/BDAs/ARN39048-FM_3-60 Army Targetting.md`

Use this when the question is:
- how targets are categorized doctrinally
- how targeting and assessment relate
- what broader target-development context should shape label interpretation

#### If You Are Looking For Analyst Workflow Or Fused Reporting Context

Start here:
- `z_reference_docs/BDAs/Fusing Data Into a BDA for the Commander.md`
- `z_reference_docs/BDAs/CJCSI 3162.02A METHODOLOGY FOR COMBAT ASSESSMENT July 2021.md`

Use this when the question is:
- how an analyst should combine observations into a usable BDA
- how evidence should be communicated upward
- how to think about commander-facing reporting language

#### If You Are Working On Dynamic Targeting, Strike Support, Or Recon Context

Start here:
- `z_reference_docs/BDAs/ARN43356-ATP_3-60.1 MULTI-SERVICE TTPs for Dynamic Targetting.md`
- `z_reference_docs/BDAs/ARN7244-ATP_3-60.2 SCAR MULTI-SERVICE TTPS for Strike Coordination and Recon.md`

Use this when the question is:
- how BDA fits into dynamic targeting operations
- what strike-support or reconnaissance context matters
- how target observation and strike coordination shape assessment timing or use

### Core BDA / Doctrine Files

- `z_reference_docs/BDAs/CJCSI 3162.02A METHODOLOGY FOR COMBAT ASSESSMENT July 2021.md`
  Tags: joint doctrine, combat assessment, PDA, FDA, target system assessment
- `z_reference_docs/BDAs/Methodology For Combat Assessment.md`
  Tags: earlier combat-assessment methodology, doctrine comparison, background reference
- `z_reference_docs/BDAs/Fusing Data Into a BDA for the Commander.md`
  Tags: analyst workflow, fusion, commander-facing BDA interpretation
- `z_reference_docs/BDAs/jp3_60 Joint Targeting.md`
  Tags: joint targeting, target development, assessment, doctrine
- `z_reference_docs/BDAs/ARN39048-FM_3-60 Army Targetting.md`
  Tags: army targeting, target categories, targeting process, assessment
- `z_reference_docs/BDAs/ARN43356-ATP_3-60.1 MULTI-SERVICE TTPs for Dynamic Targetting.md`
  Tags: dynamic targeting, multi-service TTPs, strike workflow
- `z_reference_docs/BDAs/ARN7244-ATP_3-60.2 SCAR MULTI-SERVICE TTPS for Strike Coordination and Recon.md`
  Tags: SCAR, reconnaissance, strike coordination, targeting support

### Other BDA Source Files

- `z_reference_docs/BDAs/BDA.docx`
  Tags: uncataloged source document, not yet converted to Markdown

## Prompting

Primary indexes:
- `z_reference_docs/Prompting/PROMPTING_MASTER_INDEX.md`
- `z_reference_docs/Prompting/PROMPTING_PDFS_INDEX.md`
- `z_reference_docs/Prompting/Research_Loops/README.md`

### Prompting Questions To Start From

If you are asking which prompting file to open first, start from the question
you are trying to answer rather than from the vendor name.

#### If You Are Designing Or Tightening A System Prompt

Start here:
- `z_reference_docs/Prompting/Anthropic_Claude/Claude system-prompts Giving Claude a role with a system prompt.md`
- `z_reference_docs/Prompting/Anthropic_Claude/Claude Prompt engineering overview.md`
- `z_reference_docs/Prompting/OpenAI_GPT/gpt-5-4_prompting_guide.md`
- `z_reference_docs/Prompting/Google_Gemini/22365_3_Prompt Engineering_v7_gemini.md`

Use this when the question is:
- how short should the system prompt be
- what belongs in the system prompt versus the task prompt
- how to keep policy and task mechanics separated

#### If You Are Making A Task Prompt Clearer Or More Direct

Start here:
- `z_reference_docs/Prompting/Anthropic_Claude/Claude Prompt engineering be-clear-and-direct.md`
- `z_reference_docs/Prompting/OpenAI_GPT/gpt-5-2_prompting_guide.md`
- `z_reference_docs/Prompting/OpenAI_GPT/gpt-5-4_prompting_guide.md`
- `z_reference_docs/Prompting/Google_Gemini/gemini-for-google-workspace-prompting-guide-101.md`

Use this when the question is:
- how to reduce prompt bloat
- how to make instructions less ambiguous
- how to tighten task wording without changing the schema

#### If You Are Deciding Whether To Use Examples, Chained Steps, Or Reasoning Scaffolds

Start here:
- `z_reference_docs/Prompting/Anthropic_Claude/Claude multishot-prompting Use examples (multishot prompting) to guide Claude_s behavior.md`
- `z_reference_docs/Prompting/Anthropic_Claude/Claude chain-prompts Chain complex prompts for stronger performance.md`
- `z_reference_docs/Prompting/Anthropic_Claude/Claude chain-of-thought Let Claude think (chain of thought prompting) to increase performance.md`

Use this when the question is:
- whether examples will likely help this task
- whether to split a task into multiple prompt stages
- whether reasoning scaffolding is worth the risk for this model/task

#### If You Are Trying To Control Output Format

Start here:
- `z_reference_docs/Prompting/OpenAI_GPT/gpt-5-4_prompting_guide.md`
- `z_reference_docs/Prompting/Anthropic_Claude/Claude prefill-claudes-response Prefill Claude_s response for greater output control.md`
- `z_reference_docs/Prompting/Anthropic_Claude/Claude use-xml-tags Use XML tags to structure your prompts.md`

Use this when the question is:
- how to enforce JSON-only output
- how to keep plain-text summaries narrow
- how to reduce preamble, explanation, or format drift

#### If You Are Working On Qwen-Specific Multimodal Behavior

Start here:
- `z_reference_docs/Prompting/Qwen/Qwen3-VL-8B-Instruct_Model_Card.md`
- `z_reference_docs/Prompting/Qwen/Qwen_3_Chat_template_deep_dive_Prompting_Behavior.md`
- `z_reference_docs/Prompting/Qwen/Alibaba_Cloud_vision_docs_for_Qwen-VL.md`

Use this when the question is:
- how Qwen expects system and user messages to be shaped
- how multiple images should be described by role
- how Qwen generally behaves on multimodal tasks

#### If You Are Working On Grounding, Boxes, Or Detection

Start here:
- `z_reference_docs/Prompting/Qwen/Qwen3-VL-8B-Instruct_Model_Card.md`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/2d_grounding.ipynb`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/spatial_understanding.ipynb`
- `z_reference_docs/Prompting/google_owlv2-base-patch16-ensemble/google_owlv2-base-patch16-ensemble_Task_guide.md`
- `z_reference_docs/Prompting/VLM-Research-Papers/Visually Prompted Benchmarks Are Surprisingly Fragile.md`

Use this when the question is:
- how to phrase bbox requests
- how to think about relative coordinates versus pixel-space results
- how to ask for spatial localization more directly
- why visually plausible prompts can still produce fragile boxes

#### If You Are Working On Image Roles, OCR, Or Document-Style Multimodal Inputs

Start here:
- `z_reference_docs/Prompting/Qwen/Qwen_3_Chat_template_deep_dive_Prompting_Behavior.md`
- `z_reference_docs/Prompting/Qwen/Alibaba_Cloud_vision_docs_for_Qwen-VL.md`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/document_parsing.ipynb`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/ocr.ipynb`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/long_document_understanding.ipynb`

Use this when the question is:
- how to describe multiple image inputs by purpose
- how to structure inputs where the model must read or parse from images
- how to think about longer multimodal contexts

#### If You Are Evaluating Prompt Failures Or Looking For Research Context

Start here:
- `z_reference_docs/Prompting/VLM-Research-Papers/Visual Prompting in Multimodal Large Language Models A Survey.md`
- `z_reference_docs/Prompting/VLM-Research-Papers/Visually Prompted Benchmarks Are Surprisingly Fragile.md`
- `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/experiments/failure_taxonomy.md`

Use this when the question is:
- what kind of failure mode we are seeing
- whether a weakness is likely prompt-related or evaluation-related
- what literature says about grounding fragility or multimodal prompt brittleness

### Active Model-Specific References

#### Qwen

- `z_reference_docs/Prompting/Qwen/Qwen3-VL-8B-Instruct_Model_Card.md`
  Tags: capabilities, multimodal behavior, grounding, OCR, image reasoning
- `z_reference_docs/Prompting/Qwen/Qwen_3_Chat_template_deep_dive_Prompting_Behavior.md`
  Tags: chat formatting, system/user separation, prompt structure
- `z_reference_docs/Prompting/Qwen/Alibaba_Cloud_vision_docs_for_Qwen-VL.md`
  Tags: multimodal input formatting, multi-image usage, vision request structure

#### Google OWLv2

- `z_reference_docs/Prompting/google_owlv2-base-patch16-ensemble/google_owlv2-base-patch16-ensemble-Model-card.md`
  Tags: model behavior, object detection, zero-shot grounding
- `z_reference_docs/Prompting/google_owlv2-base-patch16-ensemble/google_owlv2-base-patch16-ensemble_Prompting_Usage-Guide.md`
  Tags: usage patterns, prompt constraints, detection framing
- `z_reference_docs/Prompting/google_owlv2-base-patch16-ensemble/google_owlv2-base-patch16-ensemble_Task_guide.md`
  Tags: task examples, detection workflow, bbox tasks

#### Llama 4 Scout

- `z_reference_docs/Prompting/llama4_scout/meta-llama-Llama-4-Scout-17B-16E_Model-Card.md`
- `z_reference_docs/Prompting/llama4_scout/meta-llama_Llama-4-Scout-17B-16E-Instruct-Original_Model-Card.md`
- `z_reference_docs/Prompting/llama4_scout/meta-llama_Llama-4-Scout-17B-16E-Instruct_prompt_guide.md`

### Grounding / Boxes / Detection / Spatial Reasoning

If the question is about Qwen grounding or bbox behavior:
- `z_reference_docs/Prompting/Qwen/Qwen3-VL-8B-Instruct_Model_Card.md`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/2d_grounding.ipynb`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/spatial_understanding.ipynb`

If the question is about alternative object-detection prompting patterns:
- `z_reference_docs/Prompting/google_owlv2-base-patch16-ensemble/google_owlv2-base-patch16-ensemble_Task_guide.md`
- `z_reference_docs/Prompting/google_owlv2-base-patch16-ensemble/google_owlv2-base-patch16-ensemble_Cookbook-Notebook-Zero_and_one_shot_object_detection_with_OWLv2.ipynb`

If the question is about grounding fragility or evaluation risk:
- `z_reference_docs/Prompting/VLM-Research-Papers/Visual Prompting in Multimodal Large Language Models A Survey.md`
- `z_reference_docs/Prompting/VLM-Research-Papers/Visually Prompted Benchmarks Are Surprisingly Fragile.md`

### Multimodal Input Formatting / Image Roles

- `z_reference_docs/Prompting/Qwen/Qwen_3_Chat_template_deep_dive_Prompting_Behavior.md`
- `z_reference_docs/Prompting/Qwen/Alibaba_Cloud_vision_docs_for_Qwen-VL.md`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/document_parsing.ipynb`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/ocr.ipynb`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/long_document_understanding.ipynb`

### Evaluation / Failure Analysis / Research Context

- `z_reference_docs/Prompting/VLM-Research-Papers/Visual Prompting in Multimodal Large Language Models A Survey.md`
- `z_reference_docs/Prompting/VLM-Research-Papers/Visually Prompted Benchmarks Are Surprisingly Fragile.md`
- `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/experiments/failure_taxonomy.md`

### PDF-Derived Prompting Markdown

Use `z_reference_docs/Prompting/PROMPTING_PDFS_INDEX.md` when you specifically
want PDF-derived Markdown companions rather than hand-written notes, model
cards, or notebooks.

PDF-derived prompting Markdown currently includes:
- `z_reference_docs/Prompting/Google_Gemini/22365_3_Prompt Engineering_v7_gemini.md`
- `z_reference_docs/Prompting/Google_Gemini/gemini-for-google-workspace-prompting-guide-101.md`
- `z_reference_docs/Prompting/VLM-Research-Papers/Visual Prompting in Multimodal Large Language Models A Survey.md`
- `z_reference_docs/Prompting/VLM-Research-Papers/Visually Prompted Benchmarks Are Surprisingly Fragile.md`

### Archive / Not For Active Use

These remain searchable, but they are archived and should not be treated as
active guidance by default.

- `z_reference_docs/Prompting/Model_research-Archive-Not-to-be Used/Florence_community_Florence-2-base/Florence_community_Florence-2-base_Model_card.md`
- `z_reference_docs/Prompting/Model_research-Archive-Not-to-be Used/Florence_community_Florence-2-base/Florence_community_Florence-2-base_Prompting_Guide.md`
- `z_reference_docs/Prompting/Model_research-Archive-Not-to-be Used/IDEA-Research_grounding-dino-base/IDEA-Research_grounding-dino-base_model_card.md`
- `z_reference_docs/Prompting/Model_research-Archive-Not-to-be Used/IDEA-Research_grounding-dino-base/IDEA-Research_grounding-dino-base_practical_usage_docs.md`
- `z_reference_docs/Prompting/Model_research-Archive-Not-to-be Used/OpenGVLab_InternVL3-8B-hf/OpenGVLab_InternVL3_Model_Card.md`
- `z_reference_docs/Prompting/Model_research-Archive-Not-to-be Used/OpenGVLab_InternVL3-8B-hf/OpenGVLab_InternVL_chat_data_format_docs.md`

## Capstone Technical Documentation

Primary routing file:
- `z_reference_docs/capstone_tech_docs/understanding_tracking.md`

Use this area when the question is about:
- Phase 1, Phase 2, or Phase 3 deliverables
- deployment procedure drafting
- document dependency mapping
- what the team has already delivered versus what is still template-only

Best starting points:
- `z_reference_docs/capstone_tech_docs/understanding_tracking.md`
- `z_reference_docs/capstone_tech_docs/Deliverables_Phase_3_(S26-P1)/Deployment procedure Draft.docx`

## Best Starting Points By Task

If the question is about BDA doctrine:
- `z_reference_docs/BDAs/CJCSI 3162.02A METHODOLOGY FOR COMBAT ASSESSMENT July 2021.md`
- `z_reference_docs/BDAs/jp3_60 Joint Targeting.md`
- `z_reference_docs/BDAs/Fusing Data Into a BDA for the Commander.md`

If the question is about prompt-writing strategy:
- `z_reference_docs/Prompting/OpenAI_GPT/gpt-5-4_prompting_guide.md`
- `z_reference_docs/Prompting/Anthropic_Claude/Claude Prompt engineering overview.md`
- `z_reference_docs/Prompting/Google_Gemini/22365_3_Prompt Engineering_v7_gemini.md`
- `z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/dossier/qwen_prompt_rules.md`

If the question is about structured output / format control:
- `z_reference_docs/Prompting/OpenAI_GPT/gpt-5-4_prompting_guide.md`
- `z_reference_docs/Prompting/Anthropic_Claude/Claude prefill-claudes-response Prefill Claude_s response for greater output control.md`
- `z_reference_docs/Prompting/Anthropic_Claude/Claude use-xml-tags Use XML tags to structure your prompts.md`

If the question is about VLM grounding, boxes, or detection:
- `z_reference_docs/Prompting/Qwen/Qwen3-VL-8B-Instruct_Model_Card.md`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/2d_grounding.ipynb`
- `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/spatial_understanding.ipynb`
- `z_reference_docs/Prompting/google_owlv2-base-patch16-ensemble/google_owlv2-base-patch16-ensemble_Task_guide.md`
- `z_reference_docs/Prompting/VLM-Research-Papers/Visually Prompted Benchmarks Are Surprisingly Fragile.md`

If the question is about multimodal prompt/input formatting:
- `z_reference_docs/Prompting/Qwen/Qwen_3_Chat_template_deep_dive_Prompting_Behavior.md`
- `z_reference_docs/Prompting/Qwen/Alibaba_Cloud_vision_docs_for_Qwen-VL.md`
- `z_reference_docs/Prompting/PROMPTING_MASTER_INDEX.md`

If the question is about current prompt-experiment status:
- `z_reference_docs/Prompt_Labs/PROMPT_LABS_INDEX.md`
- `z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
- `z_reference_docs/WORKING_CHANGELOG.md`

If the question is about Phase 3 capstone documentation:
- `z_reference_docs/capstone_tech_docs/understanding_tracking.md`
- `z_reference_docs/capstone_tech_docs/Deliverables_Phase_3_(S26-P1)/Deployment procedure Draft.docx`
