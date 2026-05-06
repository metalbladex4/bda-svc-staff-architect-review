# Capstone Project Brain

## Purpose

This file is the curated entrypoint for Capstone's local Graphify memory. The
brain is a hybrid system:

- tracked Markdown routing in `z_reference_docs`
- generated local-only Graphify outputs under ignored profile folders
- source verification against code, manifests, decision notes, Prompt_Labs
  evidence, runner artifacts, promotion reports, and `WORKTREE_STATE.yaml`

The project brain is a navigation and recall layer. It is not a replacement for
source truth, promotion gates, worktree state, executable validation, or human
review.

## Two Graphs

Capstone now has two local-only Graphify profiles with different jobs.

| Graph | Profile | MCP entry | Best for |
| --- | --- | --- | --- |
| Architecture/fleet graph | `.graphify_fleet/` | `capstone-architecture-graph` | runtime architecture, code paths, detector/eval implementation structure, worktree comparison |
| Project-knowledge brain | `.graphify_project_brain/` | `capstone-project-brain` | experiment history, Qwen/Gemma status, architect rollout, promotion path, decisions and rationale |

The first graph is preserved as the architecture/fleet map. The second graph is
the preferred project-knowledge graph for evidence and decision questions.

## Generated Artifacts

Architecture/fleet graph:

- `.graphify_fleet/corpus/graphify-out/GRAPH_REPORT.md`
- `.graphify_fleet/corpus/graphify-out/FLEET_KNOWLEDGE_REPORT.md`
- `.graphify_fleet/corpus/graphify-out/PROJECT_BRAIN_REPORT.md`
  - compatibility alias for older routing; prefer `FLEET_KNOWLEDGE_REPORT.md`
- `.graphify_fleet/corpus/graphify-out/graph.json`
- `.graphify_fleet/corpus/graphify-out/capstone_architecture_graph.graphml`
- `.graphify_fleet/corpus/graphify-out/fleet_manifest.json`

Project-knowledge brain:

- `.graphify_project_brain/corpus/graphify-out/GRAPH_REPORT.md`
- `.graphify_project_brain/corpus/graphify-out/PROJECT_KNOWLEDGE_REPORT.md`
- `.graphify_project_brain/corpus/graphify-out/graph.json`
- `.graphify_project_brain/corpus/graphify-out/capstone_project_brain.graphml`
- `.graphify_project_brain/corpus/graphify-out/project_brain_manifest.json`
- `.graphify_project_brain/corpus/graphify-out/wiki/index.md`
- `.graphify_project_brain/corpus/graphify-out/capstone_benchmark_report.md`
- `.graphify_project_brain/corpus/graphify-out/memory/verified/`

Benchmark reports:

- `.graphify_fleet/corpus/graphify-out/capstone_benchmark_report.md`
- `.graphify_project_brain/corpus/graphify-out/capstone_benchmark_report.md`
- pack-specific reports now also exist for `project-state` and `architecture`
  benchmark packs when generated

Both corpora mirror the main checkout plus the seven active Capstone worktrees.
Both exclude secrets, credential-like files, raw datasets/media, caches,
generated runner artifacts, promotion-review outputs, and binary-heavy outputs.

Evidence/analytics support:

- `.capstone_evidence/evidence.sqlite`
- `.capstone_evidence/analytics.duckdb`
- `.capstone_evidence/evidence_index_report.md`
- `.capstone_evidence/duckdb_analytics_report.md`
- MCP entries:
  - `capstone-evidence-sqlite`
  - `capstone-evidence-duckdb`

These databases are local query aids. Source artifacts still win.

## Mem0 Boundary

Mem0 is installed as the direct hosted MCP server `mem0` on the laptop. It is
durable advisory memory, not source truth and not a replacement for Graphify or
the project-brain verified memory lane.

Use order:

1. Source/project artifacts first for project truth.
2. Graphify/project-brain for project/corpus navigation and source-verified
   recall.
3. Mem0 only for durable preferences, prior lessons, stable conventions,
   anti-patterns, and environment notes that may materially help the task.

Do not search Mem0 for every prompt. Do not write to Mem0 automatically. Do not
use lifecycle hooks or the Mem0 plugin. Mem0 `add_memory`, `update_memory`,
`delete_memory`, `delete_all_memories`, and `delete_entities` require explicit
user approval. Label Mem0 results as memory, not evidence.

## Codex VS Code Diagnostics Boundary

The 2026-04-30 local Codex VS Code diagnostics wave closed with a stock
extension boundary:

- the earlier laptop environment fixes held:
  - `bubblewrap` PATH warnings are gone
  - the `desktop-commander` Chrome/PDF bootstrap failure is gone
- the remaining warning families are currently treated as monitored noise:
  - connector/logo overload and occasional `outbound queue is full`
  - `workspace_dependencies` unsupported feature-enable sync mismatch
  - `thread-stream-state-changed` and related IPC broadcast-handler warnings
  - `https://chatgpt.com/ces/v1/rgstr` `403` analytics/event-log rejections
  - plugin `interface.defaultPrompt` metadata validation warnings

Current boundary:

- keep the VS Code extension stock
- do not patch compiled extension bundles locally unless a future wave has a
  clearly safer plan and a stronger validation gate
- revisit only if the warnings turn into visible failures such as send/resume
  breakage, stale thread state, or material IDE sluggishness

## MCP Routing Safety Notes

Current Codex tool routing is governed by the global instruction and inventory
layers:

- `/home/williambenitez1/.codex/AGENTS.md`
- `/home/williambenitez1/.codex/MCP_USAGE_GUIDE.md`
- `/home/williambenitez1/.codex/TOOL_INVENTORY.md`
- `/home/williambenitez1/.codex/tool_inventory.json`
- `/home/williambenitez1/Capstone/TOOL_INVENTORY.md`

As of Wave 5C, `sequential-thinking` is active and implemented by Spences10
`mcp-sequentialthinking-tools`; `mcpfinder` is also active as an approval-gated
missing-MCP discovery scout. NCP / Natural Context Provider remains
planned/deferred only.

NCP is the candidate with the most safety impact. Its routing value is real: it
could reduce tool-schema clutter and act as an MCP librarian. The project-brain
boundary is that NCP should not be put in front of high-power tools until it can
preserve Capstone's existing explicit confirmation rules. The risk is not that
NCP is inherently unsafe; the risk is that a generic `find`/`run`/`code` layer
can hide whether the underlying action is really Desktop Commander, filesystem,
Graphify, FiftyOne, browser automation, or an evidence wrapper.

Wave 5B laptop diagnostics observed NCP exposing `find` and `run`. Even though
temp state stayed isolated on the laptop, `run` remains privileged because it
can execute routed tools. Desktop diagnostics also created unexpected global
`.ncp` state, so cross-machine state isolation is not proven. NCP must not be
installed or routed here until a future wave proves find-only or strictly
read-only routing, project-local state isolation, no auto-import, disabled
scheduler/MCP-management/skills/analytics/code/Photon internals, excluded
high-risk tools not routable, and visible logging of the underlying tool,
target path, parameters, and read/write intent.

MCPfinder is best treated as a catalog/scout for MCP discovery, trust signals,
and install-config drafting, not as a Capstone hot-path dependency. Generated
install config is advisory only and requires explicit user approval before any
install, activation, or MCP config change.

Spences10 `mcp-sequentialthinking-tools` is the current implementation behind
the canonical `sequential-thinking` server. It is a compact checkpoint and
tool-plan validation aid, not evidence, memory, truth, or authority.

## Current Codex MCP Stack Checkpoint

As of the 2026-04-29 stabilization pass:

- `mem0` is active as manual, durable advisory memory; writes/deletes require
  explicit approval and Mem0 remains separate from Graphify/project-brain,
  native/project memory, and the existing MCP `memory` server
- `sequential-thinking` is active and implemented by Spences10
  `mcp-sequentialthinking-tools`; it exposes `sequentialthinking_tools`,
  `get_thinking_history`, and `clear_thinking_history`
- spences10 tool planning must use task-scoped active inventory
  `canonical_name` values, and `invalid_recommendations` means the tool plan
  failed validation
- `mcpfinder` is active as a discovery-only missing-MCP scout; use narrow,
  low-sensitive queries and treat generated install config as advisory only
- NCP is planned/deferred, not installed or routable, because Wave 5B exposed
  `run` and did not prove internal MCP/state-isolation controls enough for a
  safe read-only profile
- installed active tools from the canonical inventory are preferred first;
  source artifacts remain authoritative over every memory, graph, or routing
  layer
- `superpowers-skill-pack` is active as a global Codex skill pack pinned to
  `obra/superpowers` `v5.0.7`. For Capstone, it is workflow scaffolding only:
  use it to strengthen brainstorming, planning, systematic debugging, bounded
  subagent orchestration, worktree hygiene, review, and verification, while
  keeping source artifacts, prompt/eval gates, Graphify verification, Mem0
  approval rules, MCPfinder boundaries, NCP deferral, and human review in
  charge.
- Global Codex config now uses the persistent model-instructions file
  `/home/williambenitez1/.codex/model_instructions/gpt-5.5-creatures-free.txt`
  via `model_instructions_file`. It removes the cached `gpt-5.5`
  goblin/gremlin/raccoon/troll/ogre/pigeon/creature suppression line for new
  sessions, including full-access sessions, but does not override Capstone
  source-truth, MCP, Mem0, Graphify, prompt/eval, or user-approval boundaries.

## Current Baseline

Latest generated baselines as of `2026-04-30` after the v016a/v009/v014
comparison next-step refresh:

- architecture/fleet graph: `13456` nodes, `30668` links, `2160` hyperedges
- project-knowledge brain: `13560` nodes, `32908` links, `2218` hyperedges
- project-knowledge corpus: `4192` mirrored files across `main` plus seven
  active worktrees
- project-knowledge semantic pass: `4191` files processed
- semantic agent seed injection: `92` nodes, `122` links, and `17` hyperedges,
  including source-verified status nodes for Qwen `v014`, `v009`/`v010`/`v014`
  evidence, building-reference truth, backend deferral, Gemma status,
  worktree/main governance, BDA doctrine target-element boundaries, Qwen
  grounding-contract lessons, Prompting research guidance, Phase 1 BDA
  nonfinality, BDA review-loop and deception/reconstitution cautions, prompt
  experiment governance, Qwen and Gemma version-experiment lessons, v014
  promotion package requirements, eval behavior summaries, Graphify/MCP
  boundaries, NCP/MCP router safety boundaries, current MCP stack migration
  status, Data_set_Storage path-governance boundaries, and the current
  `v015e` prompt-only hinge status, the completed worktree-only
  `v016_reference_aware_prompt_lab` design package, the selected prompt axis
  `v016_reference_aware_candidate_discovery_with_evidence_budget`, and the
  blocked `v016a_reference_aware_candidate_discovery` expanded-hinge result,
  plus the v016a/v009/v014 comparison next-step decision before any `v016b`
  authoring/run
- project-knowledge wiki: `29` generated community/god-node articles plus
  `index.md`
- verified query-note lane: `77` seeded source-verified notes plus the
  README/template support files
- trusted recall command: `.graphify_project_brain/capstone_graphify.py recall`
  now prefers verified notes and accepted semantic seeds before raw graph
  search
- fixed Capstone benchmark result:
  - architecture/fleet graph: `2.4x` average token reduction
  - project-knowledge brain: `2.3x` average token reduction
  - broad architecture, prompt-lab, and
    Qwen/Gemma state questions remain low-signal and should start from curated
    docs or verified memory

## Human Report Dataset Intake

The new human-written report/image dataset is now represented in the project
brain as metadata and review state, not as raw image pixels.

Start with:

```text
z_reference_docs/human_report_dataset_audit/HUMAN_REPORT_DATASET_INTAKE_AND_AUDIT.md
z_reference_docs/human_report_dataset_audit/HUMAN_REPORT_DATASET_VISUAL_AUDIT.md
```

Current active intake and first-pass visual-audit status:

- `112` active images indexed from
  `z_reference_docs/Data_set_Storage/human_reports/images_with_reports`
- `112` active report files indexed from
  `z_reference_docs/Data_set_Storage/human_reports/human_written_reports`
- held-out no-report image folder:
  `z_reference_docs/Data_set_Storage/human_reports/no_reports/images`
- held-out discarded-report folder:
  `z_reference_docs/Data_set_Storage/human_reports/no_reports/discarded_reports`
- held-out counts:
  - `86` preserved images
  - `87` removed report files
- active visual audit counts:
  - `99` accurate
  - `19` accepted after user review
  - current usable report count: `118`
- active deterministic bbox/schema issue reports: `12`, all covered by
  user-accepted cases rather than active `bbox_off` status items
- dedicated project-brain shard: `human_report_examples`
- graph-visible approved-example index:
  `z_reference_docs/human_report_dataset_audit/APPROVED_HUMAN_REPORT_EXAMPLES.md`
- semantic companion files:
  - `z_reference_docs/human_report_dataset_audit/approved_human_report_examples_index.json`
  - `z_reference_docs/human_report_dataset_audit/approved_human_report_examples_graph_context.jsonl`
- current extraction stance:
  - deterministic semantic indexing is active through `human_report_examples`
  - do not start background/subagent extraction by default
  - run a stage-only agent pilot for this shard only if retrieval or prompt
    work proves the deterministic index too shallow
- approved-example semantic counts after the latest 2026-04-30 source refresh:
  - `231` reported objects across `118` approved image/report pairs
  - target types: `170` military equipment and `61` building
  - `0` object-not-found entries in the corrected approved human-report lane
  - source damage labels: `122` no damage, `57` destroyed, `27` damaged,
    `16` severe damage, `5` moderate damage, `2` light damage, and
    `2` unknown entries that remain eval proxies only
- proposed visual-summary drafts and correction queue records live under
  `z_reference_docs/human_report_dataset_audit/proposed_corrections/`

Trust boundary:

- these examples are important future prompt-development material
- use the `accurate` and `accepted_after_user_review` buckets as the first
  candidate prompt-example pool
- keep the remaining held-out `no_reports/` material out of prompt work unless
  it is explicitly repaired later; repaired additions may be referenced by
  current v2 manifests without moving their source image files
- `20`, `61`, `84`, and `101` were reviewed and accepted by the user on
  `2026-04-27`; `61.txt` was adjusted so the distant far-left truck is
  `probable` instead of `confirmed`
- `155.txt` and `166.txt` were corrected after the original v1 challenge:
  - `155` is now a positive military-equipment case with two destroyed
    military-equipment objects
  - `166` is now a positive military-equipment holdout-only diagnostic with
    one destroyed vehicle/truck wreck unless separately approved for dev/hinge
- doctrine grounding for the active set is now complete:
  - non-doctrinal `damage: unknown` labels were normalized to valid BDA
    physical-damage labels with low confidence and explanatory logic
  - the approved human-report source lane now has no object-not-found cases
  - old `human_report_challenge_v1` object-not-found control semantics remain
    historical only
  - current v2 source-refresh package:
    `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/source_refresh/human_report_challenge_v2_refresh/`
- latest report update:
  - `40`, `65`, `106`, `125`, `172`, and `187` are recovered additions from
    the old no-report lane; their images remain in `no_reports/images`, but
    current v2 references point to those source paths
  - `61`, `69`, `70`, and `77` are replacement reports inside the previously
    approved pair set
  - fresh v009/v014 baseline inference has now been run on the ten latest
    changed/recovered cases; autonomous prompt-cycle runs are no longer paused
    because of missing recovered-addition baselines
  - candidate automation still remains paused for user approval and because
    `v017b` is not authorized yet
- raw images remain in `Data_set_Storage` and are still excluded from Graphify
  corpus mirroring; Graphify sees the approved-example index, audit ledger,
  image metadata, source paths, and report semantics

## Data Set Storage Path Governance

Phase 5 completed an audit-only map of the broader `Data_set_Storage` area:

```text
z_reference_docs/zz_archive/data_set_storage/DATA_PATH_AUDIT.md
z_reference_docs/zz_archive/data_set_storage/DATA_PATH_REFERENCE_MAP.csv
z_reference_docs/zz_archive/data_set_storage/DATA_PATH_MOVE_READINESS.csv
```

Use this audit before any future data cleanup or archive wave.

Current path stance:

- `Data_set_Storage/human_reports/` stays hot because it contains the active
  approved 118-pair human-report source lane plus remaining held-out no-report
  material.
- `Data_set_Storage/Unlabeled Photos/` stays in place because it is referenced
  across Prompt_Labs and validation history.
- `Data_set_Storage/DATA_SET/Reports_(OLD)/` is a future archive candidate only
  after its relationship to `Updated_Reports/` is reviewed.
- Phase 5A completed that relationship review and found
  `Updated_Reports/` is a partial structured-conversion lane, not a clean
  authoritative replacement for `Reports_(OLD)/`.
- Phase 5B completed an empty-folder cleanup review and found seven
  empty-folder candidates. `RoboFlow_/` and the whole `Unlabeled_Photos/` tree
  are the lowest-risk later cleanup candidates; empty folders under
  `Unlabeled Photos/` and `DATA_SET/Assigned_Photos_to_Write_Report/` remain
  deferred until their parent lanes are reviewed.
- After explicit user approval, only `RoboFlow_/` was removed. The
  `Unlabeled_Photos/` empty tree and all other empty folders remain in place.

Trust boundary:

- Graphify memory records this routing and risk map, not raw image pixels.
- Any future dataset move requires a fresh reference scan, explicit approval,
  rollback notes, live-doc updates, and Graphify refresh in the same wave.
- Do not use the older `DATA_SET/Reports_(OLD)/` or `DATA_SET/Updated_Reports/`
  folders as current prompt/eval truth without a later repair/review package.

Phase 5A review:

```text
z_reference_docs/zz_archive/data_set_storage/DATA_SET_REPORT_PROVENANCE_REVIEW.md
z_reference_docs/zz_archive/data_set_storage/DATA_SET_REPORT_PROVENANCE_MAP.csv
```

Phase 5B review:

```text
z_reference_docs/zz_archive/data_set_storage/EMPTY_FOLDER_CLEANUP_REVIEW.md
z_reference_docs/zz_archive/data_set_storage/EMPTY_FOLDER_CLEANUP_MAP.csv
z_reference_docs/zz_archive/data_set_storage/ROBOFLOW_EMPTY_FOLDER_CLEANUP.md
```

## Human-Report-Informed Qwen Comparison

The immediate `v014` promotion path is paused by the new human-report process.

Current state:

- `v009` remains the promoted/tracked Qwen control baseline
- `v014` is `promotion_paused_superseded_by_human_report_process`
- `v014` is not rejected; the corrected-pack win remains historical evidence
- the first all-112 run is complete and shows the key tradeoff:
  - `v009`: `161` matches, `56` false negatives, `54` false positives
  - `v014`: `148` matches, `69` false negatives, `24` false positives
  - `v014` suppresses false positives but loses recall, especially on dense
    multi-target, confidence/distance, building, and equipment slices
- the worktree-only `v015` strategy package converted that evidence into
  explicit prompt-learning artifacts:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/`
  contains the source manifest, failure taxonomy, `56`/`56` dev/holdout split,
  offline example bank, hypothesis-only candidate directions, and acceptance
  gates; those original gates are now `v1_reference_context` because `155` and
  `166` are positive cases in `human_report_challenge_v2`
- prompt-only candidates `v015a` through `v015e` now exist in that worktree and
  are local prompt-lab evidence only
- current candidate status:
  - `v015a` recovered recall but reopened false positives
  - `v015b` and `v015c` did not resolve the `101` row-fragment/broad-box
    boundary
  - `v015d` suppressed row fragments but was too conservative
  - the offline structural guard simulator showed simple geometry suppression
    is too blunt for runtime promotion
  - `v015e_individual_body_evidence` is the strongest prompt-only hinge result
    so far by aggregate metrics (`10` matches, `13` false negatives,
    `0` false positives), but dev remains blocked because manual review
    confirms case `101` still emits one broad group/scene box
- case `101` remains a manual diagnostic hinge with reference/eval-shape
  caveats: a very large foreground-tank reference box can make oversized
  predictions look numerically better than they look visually, and two
  duplicate reference boxes are present for a small target
- the completed v016 bridge package is design-only and lives at:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/design/v016_reference_aware_prompt_lab/`
- the selected next prompt axis is
  `v016_reference_aware_candidate_discovery_with_evidence_budget`
- the first authored v016 candidate,
  `v016a_reference_aware_candidate_discovery`, tested that axis on the expanded
  12-case hinge smoke only
- `v016a` recovered recall but failed precision and the case `101` diagnostic:
  - result: `27` matches, `29` false negatives, `33` false positives, and
    `60` predicted targets
  - expanded v014 hinge baseline: `22` matches, `34` false negatives, `16`
    false positives
- historical v1 protected case `155` was abstention-safe in the old run, but
  `155` is now a positive case in `human_report_challenge_v2`
  - case `101` still produced row-fragment enumeration and a broad group/scene
    box
- decision: `v016a` is blocked from dev, holdout, all-112, promotion, runtime
  adoption, or source-truth mutation; treat it as learning evidence that the
  candidate-discovery axis reopened false positives while recovering recall
- the source-refresh package now has adjusted all-current v2 baselines covering
  all `118` current cases by combining historical reuse for unchanged cases
  with fresh v009/v014 inference on the ten latest changed/recovered reports:
  - changed-report pack (`40`, `61`, `65`, `69`, `70`, `77`, `106`, `125`,
    `172`, `187`): `v009` scored `15` matches, `4` false negatives,
    `2` false positives; `v014` scored `13` matches, `6` false negatives,
    `2` false positives
  - adjusted all-current `v009`: `172` matches, `59` false negatives,
    `53` false positives across `118` cases
  - adjusted all-current `v014`: `157` matches, `74` false negatives,
    `24` false positives across `118` cases
- the 2026-05-01 closeout correction fixed the source-refresh provenance and
  diagnostic metadata:
  - `rebaseline_metrics.md` now says unchanged cases reused historical
    predictions, the ten updated/recovered report cases used fresh v009/v014
    baseline inference, and no prompt-candidate inference was run
  - `run_v2_changed_report_baseline_refresh.py --dry-run` now records nested
    command `dry_run` metadata truthfully
  - the latest v2 automation dry-run gate readiness check passed with no issues
- after the later 10-report update, current v2 has `118` approved pairs and
  `231` objects; baseline coverage is current
- the v2 automation framework now exists under the Qwen `1.2` worktree:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/`
- the Superpowers adoption note for that framework lives at:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/superpowers_adoption/README.md`
- first live v2 automation candidate:
  - `v017a_body_backed_candidate_filter`
  - status: near miss, not user-reviewed and not a winner
  - v2 hinge: `23` matches, `34` false negatives, `17` false positives;
    aggregate checks passed, but case `101` failed the manual diagnostic
  - changed-source sanity: `9` matches, `3` false negatives, `0` false
    positives; passed
  - positive `155`: passed with `2` matches
  - legacy `office-negative` abstention guard: passed
  - case `101`: row-fragment enumeration was suppressed, but one broad
    group/scene box remained: `[75, 13, 1000, 571]`
- `v017b_single_target_box_span_self_filter` was approved, authored, and run as
  a worktree-only prompt overlay. It is an old-gate near miss, not a winner:
  aggregate hinge checks passed (`24` matches, `33` false negatives,
  `13` false positives), changed-source sanity passed (`9` matches,
  `3` false negatives, `0` false positives), updated-report smoke completed
  (`22` matches, `9` false negatives, `1` false positive), positive `155` and
  `office-negative` abstention held, but case `101` still emitted broad box
  `[75, 58, 1000, 547]`.
- case `101` is now diagnostic-only and removed from forward pass/fail
  evaluation use. The active forward hinge pack is
  `human_report_challenge_v2_hinge_11_no101`; the old 12-case hinge pack
  remains historical/manual diagnostic context only.
- `hinge_11_no101` baselines: `v009` has `24` matches, `21` false negatives,
  and `26` false positives; `v014` has `20` matches, `25` false negatives, and
  `17` false positives. Forward gates require more than `20` matches, fewer
  than `25` false negatives, no more than `21` false positives, positive
  `155`, changed-source sanity, updated-report smoke, and the separate
  `office-negative` abstention guard.
- `v017c` through `v017f` may continue inside the approved cycle budget unless
  a hard stop triggers. Do not run dev, holdout, all-112, promotion, runtime
  adoption, source-truth mutation, structural guards, MCP config changes, hook
  edits, or tool installs without separate approval.
- overnight `v017c` through `v017f` continuation completed under the active
  `human_report_challenge_v2_hinge_11_no101` gate. All four prompt-only
  candidates passed the active forward gates.
- current recommendation: `v017d_visual_anchor_lock` is the best balanced
  potential winner:
  - hinge 11 no101: `22` matches, `23` false negatives, `13` false positives
  - changed-source sanity: `10` matches, `2` false negatives, `0` false positives
  - updated-report smoke: `24` matches, `7` false negatives, `1` false positive
  - office-negative abstention: passed
- recall-oriented alternate: `v017f_compact_visual_anchor_balance` produced
  better hinge recall (`23` matches, `22` false negatives) but more false
  positives and weaker sanity checks.
- bounded dev validation on `human_report_challenge_v2_dev_55_no101` is now
  complete:
  - `v017d_visual_anchor_lock`: `72` matches, `34` false negatives,
    `16` false positives; positive `155` passed with `2` matches
  - `v017f_compact_visual_anchor_balance`: `73` matches, `33` false negatives,
    `18` false positives; positive `155` passed with `2` matches
  - same-split `v014` adjusted baseline: `69` matches, `37` false negatives,
    `17` false positives
  - same-split `v009` adjusted baseline: `74` matches, `32` false negatives,
    `27` false positives
- later primary-candidate comparison on the exact
  `human_report_challenge_v2_dev_55_no101` split reopened
  `v017b_group_box_rejection` as the precision challenger: `v017b` scored
  `72` matches, `34` false negatives, and `13` false positives, matching
  `v017d` recall while reducing false positives from `16` to `13`.
- after user approval, `v017b` received a prompt-only main promotion closeout:
  all-current/no-101 raw scoring produced `165` matches, `54` false negatives,
  and `22` false positives against the `21` FP cap. A focused visual review
  accepted the one-FP semantic override for case `125` because an
  `object_not_found` placeholder on a positive case is a recall miss already
  represented by a false negative, not an extra hallucinated target.
- current recommendation: `v017b_group_box_rejection` is the accepted
  prompt-only main promotion candidate. Its exact detect prompt text is parked
  in local `main` as commit `2f67016`; it has not been pushed to `origin` or
  `upstream`. Do not make further local commits, push, or reconcile upstream
  unless the user explicitly asks.
- preserved caveat: case `67` remains a dense smoke/dust row-formation
  failure-analysis follow-up (`1` match, `10` false negatives, `10` false
  positives), but it is not a promotion blocker after the accepted override.
- follow-up doctrine decision: the 15-candidate `v017b` doctrine iteration
  cycle is learning evidence only. With the fixed `v017b` prompt/config
  surface, baseline doctrine scored `74` matches, `32` false negatives,
  `15` false positives, and `0.7000` average assessment on
  `human_report_challenge_v2_dev_55_no101`; no candidate improved this
  cleanly. `d001` slightly improved assessment only, `d008`/`d011`/`d013`
  improved recall with a false-positive and assessment-quality cost, and
  `d014` improved precision/assessment while losing recall. Keep baseline
  doctrine unchanged.
- bounded dev packet:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/dev_validation/v017d_v017f_dev_no101/dev_validation_decision_packet.md`
- decision packet:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/overnight_v017c_to_v017f_decision_packet.md`
- primary-candidate comparison:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/dev_validation/v017d_v017f_dev_no101/primary_candidate_comparison/`
- prompt-only main promotion closeout:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/`
- v017b doctrine-cycle closeout:
  `/home/williambenitez1/Capstone_worktrees/1.5_feat__qwen3-vl-8b-instruct__v017b-doctrine-iteration/docs/prompt-lab/qwen-v017b-doctrine-iteration/cycle_001/final_doctrine_cycle_report.md`
- comparison read after the user asked to compare `v016a`, `v009`, and `v014`:
  - `v009` remains the promoted all-112 control and recall baseline, but it is
    noisy (`54` all-112 false positives; `39` expanded-hinge false positives)
  - `v014` remains the false-positive suppression lesson, but it is too
    recall-suppressive for direct promotion (`69` all-112 false negatives;
    `34` expanded-hinge false negatives)
  - `v016a` is hinge-only bridge evidence, not an all-112 candidate: it
    recovered some recall versus `v014` but leaked precision back toward the
    `v009` false-positive failure mode
- next prompt-lane step: continue with `v017c` under the active
  case-101-excluded v2 forward gate, preserving near-miss diagnosis before each
  next candidate and hard stops for abstention/source/scope/tool-boundary
  failures.

Primary lane:

- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/human_report_challenge_v1/`

Primary comparison artifacts:

- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/human_report_challenge_v1/executions/qwen_v009_vs_v014_all_112_2026-04-28_022159Z/comparison_summary.md`
- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/human_report_challenge_v1/executions/qwen_v009_vs_v014_all_112_2026-04-28_022159Z/slice_comparison_summary.md`

Decision note:

- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/decisions/qwen_1_2_human_report_informed_v009_v014_comparison_plan_2026-04-28.md`

Worktree-only `v015` strategy package:

- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/README.md`

Current `v015e` prompt-only evidence:

- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015e_individual_body_evidence/README.md`
- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015e_individual_body_evidence/executions/human_report_challenge_v1_v015e_hinge_smoke_2026-04-29_223729Z/v015e_gate_check_summary.json`
- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015e_individual_body_evidence/executions/human_report_challenge_v1_v015e_hinge_smoke_2026-04-29_223729Z/case_101_manual_review.md`

Current `v016` design evidence:

- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/design/v016_reference_aware_prompt_lab/README.md`
- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/design/v016_reference_aware_prompt_lab/case_failure_review.md`
- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/design/v016_reference_aware_prompt_lab/reference_shape_audit.md`
- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/design/v016_reference_aware_prompt_lab/v016_prompt_axis_recommendation.md`

Current `v016a` prompt-only evidence:

- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v016a_reference_aware_candidate_discovery/README.md`
- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v016a_reference_aware_candidate_discovery/executions/human_report_challenge_v1_v016a_hinge_smoke_2026-04-30_015313Z/v016a_gate_check_summary.json`
- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v016a_reference_aware_candidate_discovery/executions/human_report_challenge_v1_v016a_hinge_smoke_2026-04-30_015313Z/case_101_manual_review.md`
- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v016a_reference_aware_candidate_discovery/executions/human_report_challenge_v1_v016a_hinge_smoke_2026-04-30_015313Z/expanded_hinge_notes.md`

## When To Use Which Graph

Use `capstone-architecture-graph` or `.graphify_fleet` for:

- runtime architecture
- detector/eval implementation structure
- code path discovery
- worktree comparison
- "how does this code connect?"

Use `capstone-project-brain` or `.graphify_project_brain` for:

- active Qwen promotion path
- why `v014` is not promoted yet
- how architect feedback changed the workflow
- evidence linking `v009`, `v010`, and `v014`
- Gemma/Qwen transfer boundaries
- Prompt_Labs, decision notes, and promotion status

If both graphs disagree or a result is surprising, verify against the source
artifact before acting.

## Query Commands

For project-state, promotion, evidence, and decision questions, start with the
trusted recall doorway instead of broad raw graph search:

```bash
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py recall "What is the active Qwen promotion path?"
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py recall "Why is v014 not promoted yet?"
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py recall "Which resolved config hash should a future v014 promotion package use?"
```

`recall` ranks source-verified query notes first, accepted semantic seed nodes
second, and raw graph matches last. Use `--profile auto` for mixed
project-state/code questions, `--profile brain` for project memory only, and
`--profile fleet` for architecture graph fallback.

Use `recall --deep` or `search-all` only when the question is broader than
trusted memory and you want a discovery sweep across verified notes, accepted
semantic seeds, generated wiki articles, raw graph nodes, and the derived
evidence index:

```bash
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py recall "incoming codex dossier adoption" --deep
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py search-all "incoming codex dossier adoption"
```

Deep search labels every result by `kind`, `confidence`, `limits`, `sources`,
and `verification`. Treat verified notes and accepted semantic seeds as the
highest-trust memory layer. Treat wiki, graph, and evidence-index hits as
exploratory leads that must be checked against source artifacts before being
used in a decision.

Run the recall regression check when changing project-brain retrieval:

```bash
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py recall-benchmark
```

Execute `capstone_graphify.py` directly through its shebang. Do not call it
with plain `python3`, because Graphify dependencies live in the Graphify
uv-tool interpreter.

Raw `graphify query` remains useful for exploratory graph search after recall
and source docs have been checked.

Architecture/fleet graph:

```bash
cd /home/williambenitez1/Capstone/.graphify_fleet/corpus
graphify query "How do runtime traces connect to eval summaries?"
graphify query "Where is the detector backend interface implemented?"
```

Project-knowledge brain:

```bash
cd /home/williambenitez1/Capstone/.graphify_project_brain/corpus
graphify query "What is the active Qwen promotion path?"
graphify query "Why is v014 not promoted yet?"
graphify query "How did the architect feedback change the workflow?"
graphify query "What evidence links v009, v010, and v014?"
```

Start with generated reports when orienting:

```bash
sed -n '1,220p' /home/williambenitez1/Capstone/.graphify_fleet/corpus/graphify-out/GRAPH_REPORT.md
sed -n '1,220p' /home/williambenitez1/Capstone/.graphify_project_brain/corpus/graphify-out/PROJECT_KNOWLEDGE_REPORT.md
```

Use the generated wiki as an agent-readable map when you need to browse the
project brain by community:

```bash
sed -n '1,220p' /home/williambenitez1/Capstone/.graphify_project_brain/corpus/graphify-out/wiki/index.md
```

## Prompt Submit Reminder Hook

Capstone now benefits from a global guarded Codex `UserPromptSubmit` hook:

```text
/home/williambenitez1/.codex/hooks/user_prompt_submit_graphify_reminder.py
```

The hook is read-only. It does not rebuild graphs, query graphs, scan secrets,
use network access, or traverse broad directory trees. It only adds a short
Graphify routing reminder when the active cwd is inside Capstone, a Capstone
worktree, or another project that already has local `graphify-out` artifacts.

For Capstone, the reminder points back to this file, `capstone_graphify.py
recall`, the architecture/fleet graph, the project-knowledge brain, and the
source-verification rule. Full activation may require restarting or forking the
Codex/VS Code session after hook/config changes.

Use the fixed benchmark reports to decide whether Graphify is likely to help a
question before relying on graph recall:

```bash
sed -n '1,220p' /home/williambenitez1/Capstone/.graphify_fleet/corpus/graphify-out/capstone_benchmark_report.md
sed -n '1,220p' /home/williambenitez1/Capstone/.graphify_project_brain/corpus/graphify-out/capstone_benchmark_report.md
```

## Profile Utility Commands

Capstone has one local utility wrapper for the Graphify profiles:

```bash
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py --help
```

Use these subcommands instead of assuming hidden Graphify CLI flags exist:

- `update`: snapshot current graphs, rebuild both profiles, regenerate wiki,
  benchmarks, verified notes, and GraphML exports
- `wiki`: regenerate only the project-brain wiki
- `benchmark`: rerun the reusable Capstone benchmark question list for both
  graphs; use `--pack project-state`, `--pack architecture`, `--pack shared`,
  or `--pack all`
- `recall`: retrieve trusted project memory by checking verified notes, accepted
  semantic seeds, and graph fallback in that order; add `--deep` only for a
  clearly labeled exploratory sweep over wiki and evidence-index hits too
- `search-all`: broad discovery over verified notes, accepted semantic seeds,
  generated wiki articles, raw graph nodes, and the derived evidence index; each
  result is labeled by trust level and source-verification reminder
- `recall-benchmark`: verify fixed recall questions still hit the expected
  trusted note or seed targets before relying on retrieval for BDA work
- `doctor`: validate graph presence, ignored status, reports, wiki, benchmarks,
  verified notes, GraphML exports, MCP wrapper presence, evidence DB presence,
  staleness, and optional trusted-memory integrity; use `--strict-stale` to
  fail when graph outputs are older than configured key inputs and
  `--strict-memory` to fail on missing trusted sources, duplicate trusted IDs,
  bad trusted confidence labels, missing required lanes, or missing generated
  verified-note Markdown
- `evidence-index`: build the local-only SQLite evidence index
- `analytics`: build the local-only DuckDB analytics mirror after SQLite exists
- `estimate-extraction`: estimate broad safe-corpus LLM extraction size and
  review burden without launching extraction
- `extraction-pilot init`: create a stage-only local pilot workspace for
  approved extraction shards without ingesting trusted memory
- `extraction-pilot review --pilot-dir <path>`: validate staged subagent
  outputs for contract shape, source links, duplicates, and shard summaries
- `ingestion-readiness --pilot-dir <path>`: score reviewed staged extraction
  items into accept, defer, and reject queues before any curated trusted-memory
  ingestion pass
- `verify-memory`: audit trusted project-brain notes and semantic seeds against
  source lanes, generated verified-note Markdown, recall surfaces, BDA
  doctrine, Prompting references, Prompt_Labs evidence, runtime/eval code,
  worktree governance, and evidence DBs; use `--strict` to fail on trusted
  memory integrity problems
- `diff`: compare the latest graph against the previous snapshot
- `path`: find a shortest path between two local query labels
- `explain`: show a matched node, source, summary, and neighbors
- `graphml`: export GraphML for the project brain, architecture graph, or both

The reusable benchmark questions live at:

```text
.graphify_project_brain/capstone_graphify_questions.json
```

The trusted-memory recall regression expectations live at:

```text
.graphify_project_brain/capstone_graphify_recall_expectations.json
```

The recall suite now includes `31` expected-hit checks, including v014 formal
promotion package requirements, promotion-mode re-score behavior, broader
visual validation behavior, the no-direct-fold-in boundary, human-report
comparison memory, the `Data_set_Storage` path-governance boundary, and the
older `DATA_SET` report-provenance boundary.

The broad source-verified seed notes are generated from:

```text
.graphify_project_brain/verified_query_seed_notes.json
```

GraphML exports are generated local-only artifacts. Use them for external graph
tools when helpful, but keep the JSON graph and source artifacts as the normal
Codex-facing surfaces.

## Evidence Index And Analytics

The local evidence index is built from Prompt_Labs, runner summaries, eval
summaries, hypotheses, overlays, promotion reports, decision notes, and key
governance docs.

Use SQLite for stable, structured evidence lookup:

```bash
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py evidence-index
```

Use DuckDB for heavier read-only aggregate analysis:

```bash
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py analytics
```

The custom MCP wrappers are read-only and reject write statements. They are
for structured querying, not reference mutation.

## Trusted Memory Verification

Trusted Graphify memory can now be audited against the source lanes it claims
to summarize:

```bash
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py verify-memory
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py verify-memory --strict
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py doctor --strict-memory
```

The verifier checks the trusted note JSON, semantic seed JSON, generated
verified-note Markdown, representative recall surfaces, BDA doctrine,
Prompting references, Prompt_Labs evidence, runtime/eval code, worktree
governance, and local SQLite/DuckDB evidence indexes. It is report-only: it
does not auto-edit trusted memory when it finds a contradiction or stale path.

The latest strict source audit after memory-source correction wrote:

```text
.graphify_project_brain/archive/verification_reviews/superseded/trusted_memory_source_audit_2026-04-27_174621Z/
```

Audit result:

- checked items: `288`
- verified: `188`
- verified with limits: `100`
- source missing: `0`
- bad `REJECT` or `AMBIGUOUS` trusted confidence entries: `0`
- duplicate trusted note slugs, node IDs, or edge IDs: `0`
- missing generated verified-note Markdown files: `0`
- required lanes present: Prompt_Labs, runtime/eval code, governance, BDA
  doctrine, Prompting docs, Graphify local memory, and evidence DBs

The previous two path-stale semantic nodes are now corrected to cite the active
Qwen `1.2` worktree architecture lane rather than nonexistent `main` paths:

- `brain:overlay_runtime_config` cites
  `worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/src/bda_svc/pipeline/runtime_config.py`
- `brain:trace_eval_promotion_flow` cites
  `worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/src/bda_svc/tracing.py`

This keeps both nodes scoped as worktree architecture memory, not `main`
runtime truth.

The later focused promotion/eval memory pass and Step 1 package refresh raised
trusted memory to `316` checked items, `64` notes, `78` semantic nodes, `97`
semantic edges, and `13`
semantic hyperedges. Its added notes focus on:

- formal `v014` promotion package required artifacts
- clean promotion-mode re-score metrics on the guard and grounding packs
- broader visual validation behavior versus `v009` and `v010`
- the boundary against direct tracked config fold-in from clean scores alone
- the eval behavior summaries that matter before promotion packaging

The Step 1 formal `v014` package now exists as a deferred approval packet:

- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/promotion_reports/v014_detect_weighted_building_selection_pending_promotion.yaml`
- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/decisions/qwen_1_2_v014_formal_promotion_package_2026-04-27.md`

Read this as historical `formal_package_ready_pending_user_approved_fold_in`
evidence, not as promoted runtime truth and not as the current adoption path.
`v009` remains the promoted Qwen baseline; `v014` is paused by the all-112
human-report comparison, which showed false-positive reduction with recall
loss.

## Gated LLM Extraction

Broad safe-corpus extraction now starts with an estimator only:

```bash
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py estimate-extraction
```

The current estimator result is `very_high` review burden over `2240` eligible
files, about `1,339,756` approximate tokens, `2318` chunks, `11590` expected
candidate edges, and `2307` expected candidate notes. The gate recommendation
is `stop_before_full_extraction` until a later explicit approval chooses either
a full reviewed extraction or narrower domain shards.

Future extraction model policy:

- orchestrator: `gpt-5.5 high` in Codex if available, otherwise
  `gpt-5.4-pro xhigh`
- shard extraction workers: `gpt-5.4 medium`
- classifiers/dedupe helpers: `gpt-5.4-mini medium`
- evidence reviewers: `gpt-5.5 high` in Codex if available, otherwise
  `gpt-5.4-pro xhigh`
- code-architecture reviewer: `gpt-5.3-codex high` or existing read-only
  `code-mapper` / `search-specialist` style agents
- final acceptance reviewer: `gpt-5.5 high` if available, otherwise
  `gpt-5.4-pro high/xhigh`

Subagents may stage candidate concepts, relationships, contradictions, and
verified-note drafts, but only orchestrator-reviewed and source-verified
material can enter trusted project-brain memory.

### Stage-Only Extraction Pilot

The first narrow extraction pilot ran on `2026-04-24` over `architect_docs`
first, then `qwen_evidence`:

```text
.graphify_project_brain/archive/extraction_pilots/failed_or_incomplete/pilot_2026-04-24_172000Z/
```

Pilot result:

- mode: `stage_only`
- outputs reviewed: `9`
- staged items reviewed: `292`
- source-supported items: `292`
- unsupported items: `0`
- duplicate items: `0`
- invalid outputs: `1`
- final recommendation: `revise_extraction_contract_before_full_run`

Interpretation: the workflow mechanics worked, bounded Qwen batching worked,
and source-link review was successful. The one invalid output used
`confidence_labels` as a map instead of the required list, so the next step
before broader extraction is contract tightening and one quick rerun/review of
that contract shape. No staged pilot output was ingested into verified memory or
semantic seeds.

### Contract-Fix Confirmation

The contract-fix confirmation ran on `2026-04-24` as one-batch Qwen evidence
rechecks:

```text
.graphify_project_brain/archive/extraction_pilots/failed_or_incomplete/pilot_2026-04-24_174500Z/
.graphify_project_brain/extraction_pilots/pilot_2026-04-24_175500Z/
```

The first confirmation fixed `confidence_labels`, but exposed the same
collection-field problem on `do_not_ingest`. The contract and generated pilot
prompt were then tightened so all collection fields must be JSON arrays.

Final confirmation result:

- mode: `stage_only`
- outputs reviewed: `1`
- staged items reviewed: `33`
- source-supported items: `33`
- unsupported items: `0`
- duplicate items: `0`
- invalid outputs: `0`
- final recommendation: `ready_for_full_safe_corpus_extraction`

Interpretation: the contract-shape blocker is cleared for the tested Qwen
batch shape. Full safe-corpus extraction still requires a separate approval,
but the next planning gate can now focus on scale and review burden rather than
basic output schema reliability.

### Runtime/Eval Architecture Domain Pilot

The runtime/eval architecture domain pilot ran on `2026-04-24` as a fresh
stage-only workspace after the earlier disconnected workspace produced no
staged outputs:

```text
.graphify_project_brain/extraction_pilots/pilot_pilot_2026-04-24_183942Z/
```

The pilot covered the `runtime_eval_architecture` shard in six bounded batches.
It tested whether the extraction workflow also works on code, tests, config,
runtime, evaluator, overlay, and worktree architecture material rather than
only narrative docs and Prompt_Labs evidence.

Pilot result:

- mode: `stage_only`
- outputs reviewed: `6`
- staged items reviewed: `116`
- source-supported items: `116`
- unsupported items: `0`
- duplicate items: `0`
- invalid outputs: `0`
- final recommendation: `ready_for_full_safe_corpus_extraction`

Interpretation: the tightened extraction contract held across a code/config
architecture shard. The pilot supports moving to full safe-corpus extraction
planning, with review-burden controls, but it still does not approve trusted
memory ingestion or semantic seed promotion by itself.

### Full Safe-Corpus Staged Extraction Gate

The full safe-corpus staged extraction gate completed on `2026-04-24` under:

```text
.graphify_project_brain/extraction_pilots/pilot_full_safe_corpus_2026-04-24_191412Z/
```

The run covered all configured shards:

- `architect_docs`
- `graphify_tooling`
- `governance_worktrees`
- `runtime_eval_architecture`
- `qwen_evidence`
- `gemma_evidence`
- `general_project_context`

Final review result:

- mode: `stage_only`
- outputs reviewed: `44`
- staged items reviewed: `815`
- source-supported items: `815`
- unsupported items: `0`
- duplicate items: `0`
- duplicate identifier items: `4`
- invalid outputs: `0`
- source references checked: `1996`
- do-not-ingest items: `99`
- metadata warnings: `42`
- final recommendation: `ready_for_full_safe_corpus_extraction`

Interpretation: the extraction machinery is now proven across the safe text,
code, documentation, governance, and Prompt_Labs corpus as a staging workflow.
The metadata warnings are expected review signals because worker self-reported
model metadata is not authoritative; orchestrator-stamped metadata remains the
authority. The staged outputs are not trusted project-brain memory and were not
ingested into verified notes or semantic seeds.

Operational note: VS Code disconnected several times during the final shard,
but the file-based stage-only design allowed safe recovery without data loss.
The crashes aligned with VS Code extension-host lock recovery and
`openai.chatgpt` activation errors rather than disk, memory, or extraction-file
corruption. The final batches were completed one worker at a time, and a
local-only ignored `.vscode/settings.json` now excludes generated Graphify,
evidence, and visual-diff artifacts from workspace watching/search.

Next gate: decide whether to plan a reviewed ingestion package. That later
step should sample and dedupe staged candidates, promote only source-verified
high-signal material, and keep `INFERRED`, `AMBIGUOUS`, and `REJECT` items out
of trusted memory unless explicitly reviewed and reclassified.

### Focused Ingestion V1

Focused project-brain ingestion V1 ran after the full staged extraction and
accepted only a bounded, source-verified subset:

```text
.graphify_project_brain/ingestion_reviews/focused_ingestion_v1_2026-04-24/
```

Accepted material:

- verified query notes: `7`
- semantic nodes: `8`
- semantic edges: `10`
- semantic hyperedges: `1`

Accepted themes:

- `v014` actual runtime/eval hash caveat for future promotion packaging
- Qwen adaptive-cycle truth/manifests freeze boundary
- bounded runner as a no-self-promotion governance boundary
- office-negative raw JSON review boundary for known evaluator limitations
- runtime metadata to eval summary to promotion evidence flow
- `WORKTREE_STATE.yaml` as the canonical volatile branch-state contract
- Graphify stage-only extraction and focused ingestion boundaries

The remaining staged queue is still untrusted candidate memory. This ingestion
did not bulk-import staged output and did not change runtime code, prompts,
overlays, manifests, references, doctrine, or promotion artifacts.

### Expanded Doctrine Plus Prompting Ingestion V1.5

Expanded project-brain ingestion V1.5 promoted a larger curated subset from the
approved BDA doctrine shard plus a new clean `prompting_vlm_research` stage-only
pilot:

```text
.graphify_project_brain/ingestion_reviews/expanded_doctrine_prompting_v1_5_2026-04-27/
```

Prompting pilot result:

- outputs reviewed: `8`
- staged items reviewed: `201`
- source-supported items: `201`
- unsupported items: `0`
- invalid outputs: `0`
- do-not-ingest items: `22`
- ambiguous items: `15`

Accepted material:

- verified query notes: `17`
- semantic nodes: `17`
- semantic edges: `25`
- semantic hyperedges: `3`

Accepted themes:

- BDA starts at the target-element level; image-only VLM output is initial
  evidence, not complete BDA
- building sections, critical target elements, adjacent additional damage, and
  collateral damage need separate treatment
- functional damage and recuperation claims require more evidence than visible
  physical damage
- bbox prompt improvements should come from hierarchy, discriminative spatial
  detail, and micro-examples rather than short-word synonym chasing
- Qwen3-VL should stay aligned to normalized grounding coordinates; the older
  pixel-coordinate experiment remains a rejected lesson
- visually prompted VLM results are fragile, so bounded replay and artifact
  review remain necessary
- Anthropic prompting guidance is useful as transferable structure support, not
  as proof of Qwen or Gemma runtime behavior

The ingestion intentionally excluded all `REJECT`, unsupported, and ambiguous
staged candidates from trusted memory. Prompting references remain supporting
context only; they do not override doctrine decisions, validation manifests,
runner summaries, promotion reports, or runtime source code.

### Curated Doctrine Plus Prompting Ingestion V2

Curated ingestion V2 used the new readiness queues as a shortlist and promoted
a second bounded package:

```text
.graphify_project_brain/ingestion_reviews/curated_doctrine_prompting_v2_2026-04-27/
```

Accepted material:

- verified query notes: `12`
- semantic nodes: `12`
- semantic edges: `17`
- semantic hyperedges: `2`

Accepted themes:

- Phase 1 BDA is not final destroyed-target confirmation.
- BDA decision value is not just destroyed-system counting; deception,
  reconstitution, reinforcement, and time windows matter.
- BDA working-group style review loops support evidence reconciliation before
  later targeting decisions.
- Target validation and target engagement authority stay separate from visual
  target recognition.
- Doctrine-aligned assessment should preserve measurable/observable effect
  boundaries.
- Prompt attempts need full logging because outputs vary across models,
  versions, settings, and repeated runs.
- Structured JSON and schema-guided inputs improve reviewability but carry
  token, truncation, and repair costs.
- Prompt chaining supports staged research/review/extraction workflows.
- Single visual prompt wins require confirmation replay and artifact review.
- Qwen high-resolution/detail controls are runtime/image-detail levers, not
  prompt-only fixes.

The package intentionally deferred most Gemma capability details, OWLv2/Llama 4
adoption implications, and duplicate Qwen normalized-coordinate or
anti-neighbor bbox lessons. Those remain review context unless future local
Capstone evidence makes them decision-relevant.

### Version Experiment Memory V1

Version Experiment Memory V1 promoted a curated, source-verified subset from
the full safe-corpus readiness queue to strengthen underrepresented version
experiment history:

```text
.graphify_project_brain/ingestion_reviews/version_experiment_memory_v1_2026-04-27/
```

Accepted material:

- verified query notes: `12`
- semantic nodes: `18`
- semantic edges: `22`
- semantic hyperedges: `3`

Accepted themes:

- Qwen `v001` through `v004` tank-seed progression.
- Qwen `v005` and `v006` detection-separation plus negative-scene guardrail
  lesson.
- Qwen `v007` and `v008` assessment-only progression.
- Qwen `v006 + v008 + v004` consolidation into promoted `v009`.
- Qwen `v010` through `v013` follow-up chain and non-promotion lessons.
- Qwen `1.3` doctrine-side signal as evidence debt, not transfer authority.
- Qwen `1.4` backend pilot as a deferred side lane.
- Gemma `v000` reset anchor, `v001` recovery, `v002` control baseline, `v003`
  blocked overlay, and Gemma doctrine-shadow no-go.

This package intentionally did not bulk-ingest all accepted readiness
candidates. It keeps one-off output details in Prompt_Labs and runner artifacts
unless they explain durable version decisions. Graphify memory remains a recall
aid; Prompt_Labs artifacts, runner summaries, promotion reports, validation
manifests, and source code remain authoritative.

Validation also removed two older pre-existing `AMBIGUOUS` semantic edges from
trusted memory so the current seed file matches the stricter ingestion-readiness
boundary.

### Ingestion Readiness Scorer V1

The ingestion-readiness scorer now runs after `extraction-pilot review` and
before any curated trusted-memory package:

```bash
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py ingestion-readiness --pilot-dir <pilot>
```

It writes local-only generated review queues under:

```text
<pilot>/ingestion_readiness/
```

Generated files:

- `readiness_report.md`
- `readiness_summary.json`
- `accept_candidates.json`
- `defer_candidates.json`
- `reject_candidates.json`

The V1 scorer uses the `Balanced` policy. It allows source-supported
`EXTRACTED` items into the accept queue, and it can allow source-supported,
high-signal, non-volatile `INFERRED` items only as supporting-context accept
candidates with explicit limits. Unsupported, `REJECT`, `AMBIGUOUS`,
`do_not_ingest`, unresolved-source, and invalid items are rejected. Duplicates
against existing trusted notes or semantic seeds are downgraded to defer by
default.

Initial scorer checks on the two clean doctrine/prompting pilots:

- `bda_doctrine_targeting`: `111` accept candidates, `9` defer candidates,
  `15` reject candidates, `0` unsupported items, `0` invalid outputs, readiness
  label `ready_for_curated_ingestion`
- `prompting_vlm_research`: `143` accept candidates, `21` defer candidates,
  `37` reject candidates, `0` unsupported items, `0` invalid outputs, readiness
  label `ready_for_curated_ingestion`

Important boundary: readiness output is a shortlist, not approval. A separate
curated ingestion package must still source-check, dedupe, and explicitly
accept any item before it enters `verified_query_seed_notes.json` or
`agent_semantic_seed.json`.

## Visual Diffs And Diagrams

Prompt/version visual diffs are generated locally under:

```text
.capstone_visual_diffs/
```

Use `z_reference_docs/local_tools/capstone_visual_diff.py` to compare overlays,
prompt surfaces, doctrine snippets, config fragments, or rendered prompt text.
The output includes Markdown, local HTML, similarity, behavioral-risk tags, and
a Mermaid change map.

The global `source-verified-mermaid` skill supports targeted Mermaid diagrams
for promotion paths, worktree maps, experiment chains, runtime/eval flow,
detector boundaries, evidence schemas, and Graphify routing.

## Architecture/Fleet Graph Review Outcome

The preserved `.graphify_fleet` graph was reviewed as the "other brain" during
the query-quality hardening pass.

Implemented now:

- clearer architecture/fleet report naming via
  `.graphify_fleet/corpus/graphify-out/FLEET_KNOWLEDGE_REPORT.md`
- retained `.graphify_fleet/corpus/graphify-out/PROJECT_BRAIN_REPORT.md` as a
  compatibility alias only
- local architecture GraphML export at
  `.graphify_fleet/corpus/graphify-out/capstone_architecture_graph.graphml`
- `doctor`, `diff`, `path`, and `explain` checks that can inspect either graph
- shared benchmark reporting for both graphs so the architecture graph can be
  compared against the project-brain graph

Deferred:

- a separate architecture wiki, because the project-brain wiki is the stronger
  reading surface and the fleet graph is mostly used through reports, MCP, and
  targeted path/explain queries
- architecture-only benchmark packs, until we see repeated architecture
  questions that the shared benchmark does not measure well
- targeted architecture semantic seeds for runtime/eval flow, unless future
  `DetectorBackend`, trace, overlay, or eval-flow questions remain low-signal

Not worth doing now:

- full HTML visualization for either full graph; both graphs are larger than
  the practical visualizer threshold
- watch hooks, Neo4j, Obsidian/Canvas, or broad unconstrained LLM extraction
  over the whole corpus without a concrete next use case

## Verified Query Notes

The project-brain graph has an opt-in verified-memory lane at:

```text
.graphify_project_brain/corpus/graphify-out/memory/verified/
```

Use this only after a graph-derived answer has been checked against source
artifacts. A verified note should include the question, answer, source paths,
confidence label, and any limits. Do not save raw graph guesses, unverified
model output, secrets, credentials, or private key material as memory.

## Reference Organization And Archive Planning

The `z_reference_docs` archive cleanup now has a tracked Phase 0 planning hub:

```text
z_reference_docs/zz_archive/
```

Use it when the question is about where files should live, what can be safely
archived later, or which Graphify generated-history folders should stay hot.

Current Phase 0 files:

- `z_reference_docs/zz_archive/README.md`
- `z_reference_docs/zz_archive/ORGANIZATION_INVENTORY.md`
- `z_reference_docs/zz_archive/PROPOSED_MOVE_MANIFEST.csv`
- `z_reference_docs/zz_archive/REDUNDANCY_REVIEW.md`
- `z_reference_docs/zz_archive/GRAPHIFY_ARCHIVE_INDEX.md`
- `z_reference_docs/zz_archive/indexed_existing_archives/`

Phase 1 moved the approved loose local-doc files into:

- `z_reference_docs/zz_archive/backups/configs/`
- `z_reference_docs/zz_archive/research/model_shortlists/`
- `z_reference_docs/zz_archive/codex_agents/`
- `z_reference_docs/zz_archive/workspaces/`

`z_reference_docs/Capstone-Project.code-workspace` remains the hot workspace
file.

Phase 2 cleaned up Graphify generated-history clutter inside ignored
profile-local archive folders:

- failed or incomplete extraction pilots:
  `.graphify_project_brain/archive/extraction_pilots/failed_or_incomplete/`
- superseded verification reviews:
  `.graphify_project_brain/archive/verification_reviews/superseded/`

Successful pilots, ingestion reviews, current graph outputs, trusted seed JSON
files, evidence indexes, and newest snapshots remain hot.

Phase 3 registered existing archive folders without moving them:

- `z_reference_docs/Prompt_Labs/archive/`
  - central index:
    `z_reference_docs/zz_archive/indexed_existing_archives/Prompt_Labs_archive.md`
- `z_reference_docs/Prompting/Model_research-Archive-Not-to-be Used/`
  - central index:
    `z_reference_docs/zz_archive/indexed_existing_archives/Prompting_model_research_archive.md`

The original archive paths remain authoritative. The central indexes are
routing aids only.

Phase 4 completed the review-only redundancy/consolidation package:

- source:
  `z_reference_docs/zz_archive/REDUNDANCY_REVIEW.md`
- result: overlap clusters are classified, canonical/supporting docs are
  identified, and future candidates are recorded for later approval
- no files were moved, merged, deleted, renamed, or consolidated
- no Phase 4 manifest row is marked completed

Phase 4B completed the tiny SequentialThinking wording cleanup:

- stale deactivation text was removed from the prompt-method and capstone
  tech-doc tracking surfaces
- the updated wording matched the then-current AGENTS/MCP guidance: compact
  governance checkpoint for high-blast-radius work, and not evidence or source
  truth
- no archive move, rule change, MCP config change, worktree change, or source
  change happened

Trust boundary:

- Phase 0 did not move source files, Prompt_Labs evidence, human-report data,
  Graphify generated workspaces, or AGENTS layers.
- Phase 2 moved only ignored generated Graphify history; it did not change
  trusted project-brain memory or source truth.
- Phase 3 did not move archive contents; it only registered existing archive
  folders centrally.
- Phase 4 did not consolidate active docs; it only recorded recommendations and
  future proposal rows.
- Phase 4B changed wording only; it did not change the SequentialThinking
  operating rule itself.
- Archive candidates are proposals until the user approves a later wave or the
  manifest marks them completed.
- Graphify generated bulk history should stay local-only inside ignored
  profile folders; the tracked archive hub records only lightweight routing and
  move decisions.

## Memory Citation Policy

When transferring this workflow to another Codex/project, keep memory citations
narrow. A literal memory-citation block should cite only source-verified query
notes, accepted semantic seed files, or equivalent certified memory artifacts
when they materially shaped the answer or plan.

Do not put ordinary live docs, raw graph hits, generated wiki articles, or
derived evidence-index records into the memory-citation block. Those surfaces
can guide discovery, but they should be cited as normal source evidence or
verified first and promoted into the memory lane.

The block should not appear on every project answer. It should appear only when
verified memory materially influenced the answer. If the answer came only from
current file reads, tests, source docs, or the user's current message, omit the
memory block.

## Verification Rule

Treat Graphify answers as leads. Before acting on a graph-derived conclusion:

- open the cited source file
- verify the claim against the relevant code, manifest, decision note, README,
  promotion report, runner summary, or eval summary
- prefer `WORKTREE_STATE.yaml` for current branch roles and protected
  invariants
- prefer Prompt_Labs decision notes and runner artifacts for experiment truth
- prefer promotion reports and winner notes for promotion status

If the graph and a source artifact disagree, the source artifact wins and the
brain should be refreshed or corrected.

## Relationship To Existing Live Docs

- `WORKING_CHANGELOG.md` records current state, recent decisions, and direction.
- `WORKTREE_STATE.yaml` is the volatile branch/worktree contract.
- `REFERENCE_MASTER_INDEX.md` routes readers into the local docs.
- `Prompt_Labs/` stores branch-local experiment evidence.
- `ARCHITECT_IMPLEMENTATION_PROGRESS_REPORT.md` briefs the architect on rollout
  and follow-up decisions.
- `PROGRAM_DEEP_DIVE_AND_EXTENSIBILITY_REPORT.md` remains the narrative deep
  technical map.
- The Graphify profiles tie those surfaces together for discovery and recall.

## Maintenance Rule

Refresh the relevant graph after meaningful live-document, code, or evidence
changes when Graphify is relevant to the task. Skip refreshes only for typo-only
or non-substantive edits.

Use:

```bash
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py update
```

For a lighter check after a refresh, run:

```bash
/home/williambenitez1/Capstone/.graphify_project_brain/capstone_graphify.py doctor
```

SequentialThinking has been smoke-tested and re-enabled. The canonical trigger
policy now lives in `/home/williambenitez1/.codex/AGENTS.md`, with Capstone
project-specific triggers in `/home/williambenitez1/Capstone/AGENTS.md`.
Use it as a compact checkpoint for genuinely complex, risky, branchy,
evidence-sensitive, or critique-heavy work; do not invoke it merely because
Plan Mode is active.
