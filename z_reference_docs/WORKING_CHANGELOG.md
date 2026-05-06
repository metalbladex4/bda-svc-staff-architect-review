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

Latest checkpoint as of `2026-05-06` local / `2026-05-06` UTC artifacts:

- Refresh checkpoint: no new prompt run, code change, doctrine change,
  promotion, or source-truth update has occurred since the v023/v024 pause
  closeout. The current routing remains the v023/v024 pause report plus the
  recommendation to preserve `v020c` and move the next improvement attempt
  toward visual review and non-prompt duplicate/tiling suppression.

- The v023/v024 literal-99 Qwen no-stop continuation is now paused by user
  request and preserved as prompt-lab evidence:
  - package:
    `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v023_literal99_qwen_no_stop_continuation/`
  - pause report:
    `pause_report_2026-05-06.md`
  - scope: Qwen-only, detect-prompt-only continuation from the v022 literal-99
    plateau, all-current `117_no101` plus office-negative, preferred upstream
    OpenAI-compatible endpoint first with authorized Ollama-backed `/v1`
    fallback when `localhost:8000/v1` stayed unavailable
  - status: `v024o_v024l_intact_building_piece_exclusion` was interrupted
    before all-current completion; it has partial predictions only and is not
    an evaluated row
  - best row remains `v020c_anchor_replay`: `186` matches, `33` false
    negatives, `25` false positives, `58` total errors, with `155`, `166`,
    and office-negative passing
  - best challenger is `v024l_v023s_no_wheel_track_ablation`: `188` matches,
    `31` false negatives, `35` false positives, `66` total errors, with
    controls passing; it improves recall but carries too many extra false
    positives to replace `v020c`
  - current conclusion: keep `v020c_extra_box_audit` as the Qwen config-prompt
    incumbent; treat `v024l` as high-recall learning evidence only; favor
    visual review plus non-prompt duplicate/tiling suppression or
    backend/post-processing before more long prompt-only building rules

- The v022 literal-99 Qwen prompt refinement cycle is now closed as
  prompt-only plateau evidence:
  - package:
    `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v022_literal99_qwen_recursive_prompt_refinement_cycle/`
  - scope: Qwen-only, fetched `upstream/main` OpenAI-compatible runtime path,
    detect-prompt-only scratch worktrees, all-current `117_no101` plus the
    office-negative guard
  - backend recovery: preferred `http://localhost:8000/v1` was unavailable
    after retry, so the run used the authorized Ollama OpenAI-compatible
    fallback at `http://localhost:11434/v1` and labeled it as such
  - literal target: reduce the upstream prompt's `74` combined FN+FP errors to
    `<=1`; the best row stayed at `58` total errors, so the target was not met
  - best row: `v020c_anchor_replay` reproduced `186` matches, `33` false
    negatives, and `25` false positives, with `155`, `166`, and
    office-negative passing
  - v022 candidates `v022a` through `v022e` all regressed; the repeated failure
    was dense case `67`, which collapsed from the v020c anchor's `9/2/4` to
    only `1-2` matches and `9-10` FNs under every new wording pattern
  - current conclusion: keep `v020c_extra_box_audit` as the Qwen config prompt
    incumbent and pivot future gains toward non-prompt duplicate/tiling
    suppression, detector/backend behavior, or visual review of remaining
    FP/FN slices

- The v021 OpenAI-compatible cross-model prompt matrix is now complete as
  comparison evidence:
  - package:
    `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v021_openai_compat_cross_model_prompt_matrix/`
  - scope: current `upstream/main` OpenAI-compatible code path with
    Ollama-backed `/v1` endpoints, shared doctrine, six detect prompts, and
    two model rows (`qwen3-vl:8b-instruct`, `gemma4:e4b`)
  - Qwen winner: `v020c_extra_box_audit` at `186` matches, `33` false
    negatives, and `25` false positives, with `155`, `166`, and
    office-negative passing
  - Gemma winner: `v018e_contrastive_body_anchor` at `138` matches, `81`
    false negatives, and `19` false positives, with `155`, `166`, and
    office-negative passing
  - current conclusion: `v020c` is the right Qwen config prompt candidate, but
    it does not transfer cleanly to Gemma because Gemma `v020c` fails positive
    control `155`; Gemma should keep `v018e` as the best prompt-comparison
    evidence row for this matrix
  - doctrine diff gate stayed closed: local and fetched `upstream/main`
    `src/bda_svc/pipeline/doctrine.yaml` matched exactly, so only the shared
    doctrine matrix was needed

- The Codex MCP/tooling migration is now stabilized on this laptop:
  - the canonical global inventory is
    `/home/williambenitez1/.codex/TOOL_INVENTORY.md`, with machine-readable
    JSON at `/home/williambenitez1/.codex/tool_inventory.json`
  - `sequential-thinking` is active and implemented by Spences10
    `mcp-sequentialthinking-tools`; use it only as a compact checkpoint and
    tool-plan validator, not as evidence or ritual overhead
  - `mem0` is active as durable advisory memory, manual/approval-gated, and
    separate from native/project memory, Graphify/project-brain, and the
    existing MCP `memory` server
  - `mcpfinder` is active as a discovery-only missing-MCP scout; use narrow,
    low-sensitive queries, treat generated config as advisory, and never
    auto-install candidate MCPs
  - `superpowers-skill-pack` is installed globally from `obra/superpowers`
    `v5.0.7` at `/home/williambenitez1/.codex/superpowers`, with Codex skill
    discovery through `/home/williambenitez1/.agents/skills/superpowers`; use
    it in Capstone-adapted mode as workflow scaffolding, not source truth,
    promotion authority, or an override of existing prompt/eval gates
  - global Codex config now uses
    `/home/williambenitez1/.codex/model_instructions/gpt-5.5-creatures-free.txt`
    through `model_instructions_file`; it preserves the cached `gpt-5.5` base
    instructions while removing the goblin/gremlin/raccoon/troll/ogre/pigeon/
    creature suppression line, and it does not override Capstone source-truth,
    MCP, Mem0, Graphify, prompt/eval, or approval boundaries
  - NCP remains planned/deferred and is not active in Codex MCP config because
    Wave 5B exposed `run` and did not prove internal MCP/state-isolation
    controls strongly enough for safe routing
  - source artifacts, project docs, tests, logs, validation artifacts, evidence
    indexes, Graphify verified memory, and explicit user direction remain
    authoritative over every memory or routing layer

- Mem0 is installed and active as the direct hosted MCP server `mem0` on the
  laptop:
  - auth uses `MEM0_API_KEY` by environment-variable reference; no literal key
    belongs in config, docs, inventory, logs, screenshots, or project files
  - Mem0 is durable advisory memory, not source truth
  - source artifacts, project docs, tests, logs, validation artifacts, evidence
    indexes, Graphify verified memory, and explicit user direction remain
    authoritative
  - search Mem0 only when durable preference, prior lesson, stable convention,
    anti-pattern, or environment-note memory may materially help the task
  - do not search Mem0 for every prompt
  - do not use automatic writes, lifecycle hooks, or the Mem0 plugin
  - `add_memory`, `update_memory`, `delete_memory`, `delete_all_memories`, and
    `delete_entities` require explicit user approval
- SequentialThinking has been migrated and validated:
  - final MCP server name remains `sequential-thinking`
  - implementation is now Spences10 `mcp-sequentialthinking-tools`
  - visible tools are `sequentialthinking_tools`, `get_thinking_history`, and
    `clear_thinking_history`
  - `invalid_recommendations` means tool-plan validation failed and must be
    corrected before acting
  - canonical trigger policy lives in `/home/williambenitez1/.codex/AGENTS.md`,
    with Capstone-specific triggers in `/home/williambenitez1/Capstone/AGENTS.md`
  - use it as a compact checkpoint for genuinely complex, risky, branchy,
    evidence-sensitive, critique-heavy, or high-blast-radius work; do not
    invoke it merely because Plan Mode is active
  - before risky edits, use it to name risk, safest path, non-negotiable
    boundaries, evidence needed, validation gate, stop rule, and next action
  - ground facts in source artifacts before and after the checkpoint;
    SequentialThinking is a whiteboard, not a witness
- FiftyOne MCP is now installed and configured:
  - package: `fiftyone-mcp-server==0.1.10`
  - command: `/home/williambenitez1/.local/bin/fiftyone-mcp`
  - Codex MCP entry: `fiftyone`
  - project rule: use it only for explicit local visual dataset/case review,
    validation-pack samples, predicted/reference bbox inspection, and curated
    FiftyOne datasets; source truth remains `bda_eval`, runner summaries,
    manifests, reference JSON, doctrine docs, and promotion reports
- Portable Codex capability transfer guidance now exists:
  - `z_reference_docs/CODEX_CAPABILITY_TRANSFER_DOSSIER.md`
  - purpose: explain how this Codex uses MCP routing, tools, skills, subagents,
    AGENTS layers, Graphify, evidence workflows, memory citations, and
    planning/documentation habits so another project can selectively adopt the
    techniques without copying Capstone-specific scripts or graph names
- Incoming Codex capability ideas from
  `z_reference_docs/The_Incomming_CODEX_CAPABILITIES_DOSSIER.md` have now been
  selectively adopted:
  - global guarded `UserPromptSubmit` Graphify reminder:
    `/home/williambenitez1/.codex/hooks/user_prompt_submit_graphify_reminder.py`
  - `codex_hooks = true` is enabled in `/home/williambenitez1/.codex/config.toml`
  - `project-brain-lite` and `architecture-plus` graph lanes remain deferred
    until benchmarks show a concrete routing gap
- Capstone now has two local-only Graphify profiles:
  - architecture/fleet profile root: `.graphify_fleet/`
  - project-knowledge brain profile root: `.graphify_project_brain/`
  - curated entrypoint: `z_reference_docs/PROJECT_BRAIN.md`
  - architecture report: `.graphify_fleet/corpus/graphify-out/GRAPH_REPORT.md`
  - architecture graph JSON: `.graphify_fleet/corpus/graphify-out/graph.json`
  - project-knowledge report:
    `.graphify_project_brain/corpus/graphify-out/PROJECT_KNOWLEDGE_REPORT.md`
  - project-knowledge graph JSON:
    `.graphify_project_brain/corpus/graphify-out/graph.json`
  - MCP entries:
    - `capstone-architecture-graph`
    - `capstone-project-brain`
  - coverage: the main checkout plus the seven active Capstone worktrees
  - generated graph artifacts are ignored and are not tracked repo truth
  - the preserved fleet graph is the code/worktree/architecture map
  - the new project-knowledge brain adds semantic agent seed relationships for
    Qwen v014 promotion readiness, v009/v010/v014 evidence, Gemma control
    status, backend-pilot deferral, MCP boundaries, and worktree governance
    - the project-brain profile now also generates:
    - a local wiki at
      `.graphify_project_brain/corpus/graphify-out/wiki/index.md`
    - fixed Capstone benchmark reports for both Graphify profiles
      - an opt-in verified query-note lane at
        `.graphify_project_brain/corpus/graphify-out/memory/verified/`
  - the human-written report/image dataset has been indexed for
    Graphify-visible recall and then culled into an active paired set plus a
    held-out no-report folder by user request:
    - active images: `112`
    - active report files: `112`
    - held-out images:
      `z_reference_docs/Data_set_Storage/human_reports/no_reports/images`
      (`86` files)
    - held-out removed reports:
      `z_reference_docs/Data_set_Storage/human_reports/no_reports/discarded_reports`
      (`87` files)
    - active visual-audit counts:
      - `99` accurate
      - `13` accepted after user review
      - current usable report count: `112`
    - active deterministic bbox/schema issue reports: `6`, all covered by
      user-accepted cases rather than active `bbox_off` status items
    - dedicated Graphify extraction shard: `human_report_examples`
    - approved-example semantic index:
      `z_reference_docs/human_report_dataset_audit/APPROVED_HUMAN_REPORT_EXAMPLES.md`
    - semantic companion files:
      - `z_reference_docs/human_report_dataset_audit/approved_human_report_examples_index.json`
      - `z_reference_docs/human_report_dataset_audit/approved_human_report_examples_graph_context.jsonl`
    - current extraction stance:
      - deterministic semantic indexing is active through
        `human_report_examples`
      - background/subagent extraction is deferred by default
      - run a stage-only agent pilot for this shard only if retrieval or prompt
        work proves the deterministic index too shallow
    - current approved-example semantic counts after the latest 2026-04-30
      source refresh:
      - `231` report objects across the `118` approved image/report pairs
      - `170` military-equipment objects and `61` building objects
      - `0` object-not-found entries in the corrected approved human-report
        source lane
      - source damage labels now include `122` no-damage, `57` destroyed,
        `27` damaged, `16` severe-damage, `5` moderate-damage,
        `2` light-damage, and `2` unknown entries; the unknown entries remain
        eval proxies only and must be read with their source caveats
    - doctrine grounding for the active human-report set is complete:
      - non-doctrinal `damage: unknown` source labels were normalized to valid
        BDA physical-damage labels while preserving uncertainty through
        `possible` confidence and explanatory logic
      - `155` and `166` are no longer object-not-found controls after the
        source refresh; both are positive military-equipment cases in
        `human_report_challenge_v2`
      - `155` is available as a positive hinge/dev diagnostic, while `166`
        remains holdout-only unless separately approved for dev/hinge
      - the old `human_report_challenge_v1` controls and runs remain
        historical evidence only
      - current source-refresh package:
        `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/source_refresh/human_report_challenge_v2_refresh/`
      - the later report update added or replaced cases `40`, `61`, `65`,
        `69`, `70`, `77`, `106`, `125`, `172`, and `187`; the recovered
        additions keep their source images in the previous `no_reports/images`
        folder while current v2 manifests point to the actual source paths
    - Qwen `v014` promotion is now paused and superseded by the
      human-report-informed process:
      - `v009` remains the promoted/tracked Qwen baseline
      - `v014` is `promotion_paused_superseded_by_human_report_process`, not
        rejected and not promoted
      - the old all-112 `human_report_challenge_v1` comparison remains the
        historical source for the original `v015` prompt-learning lane
      - `human_report_challenge_v2` is now the current authority for future
        human-report prompt gates
      - adjusted all-current `v2` baselines now cover all `118` current
        human-report cases by combining historical reuse for unchanged cases
        with fresh v009/v014 inference on the ten latest changed/recovered
        reports:
        - changed-report pack (`40`, `61`, `65`, `69`, `70`, `77`, `106`,
          `125`, `172`, `187`): `v009` scored `15` matches, `4` false
          negatives, `2` false positives; `v014` scored `13` matches,
          `6` false negatives, `2` false positives
        - adjusted all-current `v009`: `172` matches, `59` false negatives,
          `53` false positives across `118` cases
      - adjusted all-current `v014`: `157` matches, `74` false negatives,
        `24` false positives across `118` cases
      - the 2026-05-01 closeout correction fixed the generated
        `rebaseline_metrics.md` provenance wording: unchanged cases reused
        historical predictions, the ten updated/recovered report cases used
        fresh v009/v014 baseline inference, and no prompt-candidate inference
        was run
      - the changed-report baseline helper now records nested command
        `dry_run` metadata truthfully when invoked with `--dry-run`; the
        latest dry-run gate readiness check passed with no issues
      - autonomous prompt-cycle runs are no longer blocked by missing recovered
        addition baselines; the user later authorized one bounded continuation
        from `v017a` into `v017b`, with a hard stop before dev, holdout,
        all-112, promotion, runtime adoption, source-truth mutation, structural
        guard implementation, MCP config changes, hook edits, or tool installs
      - interpretation remains a precision/recall tradeoff: `v014` suppresses
        false positives but loses too much recall for direct promotion
      - worktree-only `v015` strategy package now exists under the active Qwen
        `1.2` worktree:
        `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/`
      - that package began as analysis-only: it contains a source manifest,
        failure taxonomy, balanced dev/holdout split, offline example bank,
        hypothesis candidates, and acceptance gates
      - subsequent worktree-only prompt candidates `v015a` through `v015e`
        have now been authored and hinge-smoke tested without runtime adoption,
        dev, holdout, all-112, source-truth mutation, or promotion
      - current prompt-only status: `v015e_individual_body_evidence` is the
        strongest hinge result so far by aggregate metrics (`10` matches,
        `13` false negatives, `0` false positives), but it remains blocked
        from dev by the manual case `101` two-tier gate because it still emits
        one broad group/scene box
      - the v015 lane is now closed into a design-only `v016` bridge package:
        `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/design/v016_reference_aware_prompt_lab/`
      - the selected next prompt axis is
        `v016_reference_aware_candidate_discovery_with_evidence_budget`;
        it is still prompt engineering, but it changes the prompt-lab method
        before authoring new prompt text
      - first authored `v016` candidate status:
        `v016a_reference_aware_candidate_discovery` ran the approved expanded
        12-case hinge smoke only; it improved recall (`27` matches, `29` false
        negatives versus v014 expanded hinge `22`/`34`) but failed precision
        (`33` false positives versus the `<=16` cap) and repeated case `101`
        row-fragment plus broad group/scene-box behavior
      - `v016a` is blocked from dev, holdout, all-112, runtime adoption, and
        promotion; it is learning evidence that the candidate-discovery axis
        reopened false positives while recovering recall
      - post-hinge comparison read:
        - `v009` remains the all-112 promoted control and recall baseline, but
          it is noisy (`54` false positives on all-112; `39` on the expanded
          hinge baseline)
        - `v014` remains the precision-suppression lesson, but it is too
          recall-suppressive for direct promotion (`69` all-112 false
          negatives; `34` expanded-hinge false negatives)
        - `v016a` is hinge-only bridge evidence: it recovered some recall
          versus `v014` but leaked precision back toward the `v009` failure
          mode
      - next natural prompt-lane step: build a worktree-only `v016a` failure
        synthesis and `v016b` prompt-axis decision package before authoring or
        running another prompt candidate
      - old package constraints are `v1_reference_context`; after the v2
        refresh, `155` and `166` are positive cases, not protected negatives
      - future prompt automation must use `human_report_challenge_v2`, with a
        separate legacy `office-negative` abstention guard
      - the automation package now includes an updated-report smoke manifest
        for the current source-refresh set and now records that `v017b` was
        authorized for one bounded live v2 gate run
      - the first v2 automation live run, `v017a_body_backed_candidate_filter`,
        is complete but not user-reviewed: it is a near miss, not a winner
      - `v017a` passed changed-source sanity, positive `155`, and
        `office-negative`, and it passed aggregate hinge metrics, but it failed
        the case `101` manual diagnostic because it still emitted one broad
        group/scene box `[75, 13, 1000, 571]`
      - a light Superpowers reassessment package now records the post-`v017a`
        workflow correction: near misses require a source-artifact diagnosis
        before the next prompt is authored
      - the recommended `v017b_single_target_box_span_self_filter` axis was
        approved, authored, and run as a worktree-only prompt overlay; `v017b`
        is also a near miss, not a winner
      - `v017b` results:
        - v2 hinge aggregate checks passed: `24` matches, `33` false
          negatives, `13` false positives, and positive `155` passed
        - changed-source sanity passed: `9` matches, `3` false negatives,
          `0` false positives, and positive `155` passed
        - updated-report smoke completed: `22` matches, `9` false negatives,
          `1` false positive
        - legacy `office-negative` abstention guard passed
        - blocker: case `101` still emitted one broad group/scene box
          `[75, 58, 1000, 547]` with area ratio about `0.4314`
      - later v017 continuation: case `101` is now diagnostic-only; `v017c`
        through `v017f` completed under the no-101 forward hinge, and
        `v017d_visual_anchor_lock` became the best balanced candidate
      - bounded dev validation is now complete on
        `human_report_challenge_v2_dev_55_no101`: `v017d` scored
        `72` matches, `34` false negatives, and `16` false positives, beating
        the same-split v014 baseline (`69`/`37`/`17`); `v017f` scored
        `73`/`33`/`18` and is the recall comparator but exceeds the v014
        false-positive ceiling
      - later same-image primary-candidate comparison reopened `v017b` as the
        precision challenger: on `human_report_challenge_v2_dev_55_no101`,
        fresh `v017b_group_box_rejection` scored `72` matches, `34` false
        negatives, and `13` false positives, matching `v017d` recall while
        reducing false positives from `16` to `13`
      - after user approval, `v017b` received a prompt-only main promotion
        closeout: the all-current/no-101 smoke scored `165` matches,
        `54` false negatives, and `22` raw false positives; a focused visual
        review accepted the one-FP semantic override for case `125`, treating
        its `object_not_found` placeholder on a positive case as FN-only for
        the promotion cap, yielding an effective `21` extra-target false
        positives
      - controls held: positive `155`, positive `166`, and the separate
        `office-negative` abstention guard passed; case `101` remains
        diagnostic-only and excluded from forward pass/fail evaluation
      - current v017 decision: `v017b_group_box_rejection` is the accepted
        prompt-only promotion candidate and its exact prompt text is parked in
        local `main` as commit `2f67016`; it has not been pushed to `origin` or
        `upstream`, and no further local commits should be made until the user
        asks
      - follow-up case `67` dense-formation diagnosis is complete: every
        compared prompt family scored only `1` match and `10` false negatives
        on the same `human_report_challenge_v2_dev_55_no101` surface; the
        failure is a dense smoke/dust, perspective-row, top-edge/body-anchor
        limitation, not a `v017b`-specific regression and not the old case
        `101` broad group-box failure
      - first `v018` follow-up, `v018a_dense_formation_body_center_anchor`, is
        learning evidence only: it passed the minimal formal no-101 smoke gate
        but failed as a challenger because it regressed versus parked `v017b`
        by `-1` match, `+1` false negative, and `+8` false positives; case
        `67` did not improve (`1` match, `10` false negatives, `10` false
        positives), so do not promote, deepen, dev-run, holdout-run,
        all-current-run, or replace `v017b` with `v018a`
      - follow-up `v017b` doctrine-iteration closeout is complete in a
        separate worktree-only lane:
        `/home/williambenitez1/Capstone_worktrees/1.5_feat__qwen3-vl-8b-instruct__v017b-doctrine-iteration/docs/prompt-lab/qwen-v017b-doctrine-iteration/cycle_001/`
      - doctrine-cycle decision: keep baseline doctrine unchanged; the
        15-candidate cycle did not produce a doctrine candidate that clearly
        improves the fixed `v017b` prompt without tradeoffs
      - doctrine-cycle baseline replay scored `74` matches, `32` false
        negatives, `15` false positives, and `0.7000` average assessment score
        on `human_report_challenge_v2_dev_55_no101`
      - useful doctrine signals:
        - `d001_visual_pda_scope` slightly improved assessment quality
          (`0.7014`) without changing detection counts
        - `d008_exterior_building_guard`, `d011_best_assess_plus_detect`, and
          `d013_recall_repair_blend` produced the best recall tradeoff
          (`75` matches, `31` false negatives) but raised false positives to
          `16` and lowered assessment quality
        - `d014_dense_case_blend` produced the best precision/assessment signal
          (`73` matches, `33` false negatives, `14` false positives, `0.7073`
          average assessment) but was too recall-conservative
      - positive `155` passed in every doctrine run; no recovery events
        affected trusted results; `doctrine.yaml` was restored to baseline
        checksum after temporary swaps
      - standing decision: `v017b_group_box_rejection` remains the accepted
        prompt-only promotion candidate parked locally, baseline doctrine
        remains unchanged, and doctrine-cycle outputs are learning evidence for
        future narrower work only
      - latest v018 upstream/v017b amalgamation cycle:
        `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/upstream_v017b_amalgamation_cycle/`
      - v018 tested five detect-only prompts that blended current
        `upstream/main` recall-friendly brevity with `v017b` control discipline
        on `human_report_challenge_v2_all_current_117_no101` plus the
        `office-negative` guard
      - no v018 prompt is adoption-ready: all five passed positive `155`,
        positive `166`, and office-negative, and all improved recall over both
        upstream and v017b, but every candidate exceeded the `v017b` raw
        false-positive ceiling
      - v018d is the recall-ceiling signal (`180` matches, `39` false
        negatives, `39` false positives) but is too loose for adoption
      - v018e is the best precision-balanced follow-up axis (`173` matches,
        `46` false negatives, `29` false positives), but still exceeds the
        false-positive ceiling
      - standing v018 decision: keep `v017b_group_box_rejection` parked as the
        accepted prompt-only candidate; do not promote any v018 prompt as-is;
        next technical step is focused visual review of `v018e` false positives
        and `v018d` recall wins before authoring a narrower follow-up
      - reassessment package:
        `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/reassessments/v017a_superpowers_reassessment/`
      - latest v017b run and diagnosis:
        `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/runs/v017b/live_2026-05-03_032920Z/`
        and
        `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/reassessments/v017b_gate_result/`
      - v017b comparison, visual review, and override/promotion closeout:
        `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/dev_validation/v017d_v017f_dev_no101/primary_candidate_comparison/`
        and
        `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/`
      - case `67` diagnostic and `v018a` follow-up:
        `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/case67_dense_formation_diagnostic/`
        and
        `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_002/runs/v018a/live_2026-05-04_003732Z/`
      - v018 amalgamation closeout:
        `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/upstream_v017b_amalgamation_cycle/final_recommendation.md`
      - v020 v019c goal-driven closeout:
        `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v020_v019c_goal_driven_self_improvement_cycle/final_recommendation.md`
      - v021 OpenAI-compatible cross-model matrix:
        `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v021_openai_compat_cross_model_prompt_matrix/final_recommendation.md`
      - v022 literal-99 Qwen prompt-only plateau closeout:
        `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v022_literal99_qwen_recursive_prompt_refinement_cycle/final_recommendation.md`

### 2026-05-05 - Closed v022 Literal-99 Qwen Prompt Cycle As Plateau Evidence

- created and completed the worktree-only
  `v022_literal99_qwen_recursive_prompt_refinement_cycle` under the existing
  `v017b_prompt_only_main_promotion` lane
- replayed the promoted Qwen incumbent first:
  - `v020c_anchor_replay`
  - `186` matches, `33` false negatives, `25` false positives
  - `58` total errors
  - positive `155`, positive `166`, and office-negative passed
- literal target was not reached:
  - upstream baseline: `74` total errors (`38` FNs + `36` FPs)
  - target: `<=1` combined false negative + false positive
  - achieved best: `58` total errors from the v020c replay
- sequential candidates `v022a` through `v022e` all regressed from the anchor:
  - `v022a_micro_target_sweep`: `183/36/84`
  - `v022b_sparse_scene_proxy_filter`: `173/46/33`
  - `v022c_candidate_ledger_balance`: `172/47/41`
  - `v022d_compressed_context_shadow`: `176/43/36`
  - `v022e_v020c_dense_guard_sentence`: `172/47/34`
- method lesson:
  - v020c is a brittle prompt-only local optimum, not a pattern that improved
    through extra wording
  - every v022 wording change collapsed dense case `67` from the anchor's
    `9` matches / `2` FNs / `4` FPs to only `1-2` matches and `9-10` FNs
  - even the smallest perturbation, one dense-guard sentence added to v020c,
    worsened case `67` and case `84`
  - future improvement should move to non-prompt duplicate/tiling suppression,
    detector/backend behavior, or visual review of remaining FP/FN slices
- backend note:
  - preferred `http://localhost:8000/v1` was unavailable after retry
  - the cycle used the authorized Ollama OpenAI-compatible fallback
    `http://localhost:11434/v1`
  - artifacts label this honestly as `ollama_openai_compat_fallback_11434`
- boundaries preserved: no source-truth edit, doctrine edit, assessment prompt
  edit, runtime adoption, commit, push, or PR

Artifacts:

- package:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v022_literal99_qwen_recursive_prompt_refinement_cycle/`
- matrix:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v022_literal99_qwen_recursive_prompt_refinement_cycle/comparison_matrix.md`
- recommendation:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v022_literal99_qwen_recursive_prompt_refinement_cycle/final_recommendation.md`

### 2026-05-05 - Completed v021 OpenAI-Compatible Cross-Model Prompt Matrix

- created and completed the worktree-only
  `v021_openai_compat_cross_model_prompt_matrix` under the existing
  `v017b_prompt_only_main_promotion` lane
- compared six detect prompts through the fetched `upstream/main`
  OpenAI-compatible runtime path with Ollama-backed `/v1` endpoints:
  - current `upstream/main` config prompt
  - `v009_unified_best_stack`
  - `v017b_group_box_rejection`
  - `v018e_contrastive_body_anchor`
  - `v019c_context_shadow_reversal`
  - `v020c_extra_box_audit`
- doctrine check:
  - local and fetched `upstream/main` `doctrine.yaml` matched exactly
  - shared doctrine SHA-256:
    `bd83e50bd1b5cf369264f53db3d2fe58e46d7a032211db1a51ab6cbdb94b9813`
  - no two-doctrine expansion was needed
- Qwen result:
  - winner: `v020c_extra_box_audit`
  - score: `186` matches, `33` false negatives, `25` false positives
  - controls: positive `155`, positive `166`, and office-negative passed
  - comparison to current upstream config prompt:
    `+5` matches, `-5` false negatives, `-11` false positives
- Gemma result:
  - winner among eligible rows: `v018e_contrastive_body_anchor`
  - score: `138` matches, `81` false negatives, `19` false positives
  - controls: positive `155`, positive `166`, and office-negative passed
  - `v020c_extra_box_audit` scored `127/92/18` but was disqualified because
    it failed positive control `155`
- method lesson:
  - the upstream OpenAI-compatible `OPENAI_BASE_URL` code path should be the
    default prompt-comparison path going forward
  - Qwen and Gemma should not be assumed to share a winning detect prompt;
    Qwen prefers the `v020c` extra-box audit, while Gemma's best eligible row
    in this matrix is the earlier `v018e` contrastive body-anchor prompt
- boundaries preserved: no doctrine promotion, runtime-code change,
  source-truth mutation, commit, push, or PR was part of this evidence wave

Artifacts:

- package:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v021_openai_compat_cross_model_prompt_matrix/`
- matrix:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v021_openai_compat_cross_model_prompt_matrix/cross_model_comparison_matrix.md`
- recommendation:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v021_openai_compat_cross_model_prompt_matrix/final_recommendation.md`

### 2026-05-05 - Closed v020 v019c Goal-Driven Prompt Cycle As Learning Evidence

- created and ran the worktree-only
  `v020_v019c_goal_driven_self_improvement_cycle` under the existing
  `v017b_prompt_only_main_promotion` lane
- replayed the `v019c_context_shadow_reversal` anchor first:
  `174` matches, `45` false negatives, `28` false positives, with positive
  `155`, positive `166`, and office-negative passing
- authored and ran candidates `v020a` through `v020k` one at a time against
  `human_report_challenge_v2_all_current_117_no101` plus the
  `legacy_abstention_guard_office_negative` guard
- best stable balanced incumbent:
  - `v020c_v019c_extra_box_audit`
  - `186` matches, `33` false negatives, `25` false positives
  - controls passing
  - exact replay `v020h` reproduced the same `186/33/25` result
- success target was not reached:
  - target: false negatives `<=25` and false positives `<=15`
  - achieved best: false negatives `33`, false positives `25`
- method lesson:
  - `v020c` is stable prompt-only learning evidence and the next diagnostic
    anchor, not a runtime adoption candidate
  - post-`v020c` refinements repeatedly disturbed dense-case behavior,
    especially case `67`, or created tiling/extra-box false positives
  - the next productive lever is likely a non-prompt or post-processing
    investigation for duplicate/tiling suppression that preserves `v020c`
    dense-row recall
- boundaries preserved: no source-truth edit, doctrine edit, runtime adoption,
  commit, push, or PR

Artifacts:

- package:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v020_v019c_goal_driven_self_improvement_cycle/`
- recommendation:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v020_v019c_goal_driven_self_improvement_cycle/final_recommendation.md`
- matrix:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v020_v019c_goal_driven_self_improvement_cycle/comparison_matrix.json`

### 2026-04-30 - Installed Superpowers As Capstone-Adapted Skill Pack

- installed `obra/superpowers` as a global Codex skill pack:
  - clone: `/home/williambenitez1/.codex/superpowers`
  - release: `v5.0.7`
  - commit: `1f20bef3f59b85ad7b52718f822e37c4478a3ff5`
  - discovery symlink:
    `/home/williambenitez1/.agents/skills/superpowers`
- installed skills only; upstream hooks, MCP servers, agents, and deprecated
  command wrappers were not activated
- recorded the Capstone-adapted boundary:
  - Superpowers can support brainstorming, implementation plans, systematic
    debugging, subagent orchestration, worktree hygiene, review, and
    verification
  - Superpowers does not override source artifacts, project `AGENTS.md`,
    Graphify verification, Mem0 approval gates, MCPfinder approval gates, NCP
    deferral, prompt/eval gates, or human review
  - the upstream every-task skill-trigger doctrine is not adopted as ritual
    overhead for Capstone
- added a worktree-local adoption note beside the
  `human_report_challenge_v2` prompt-iteration automation package
- preserved the current Qwen prompt pause: `v017a` remains near miss pending
  user review, and no `v017b` authoring or run is approved by this install
    - start with:
      `z_reference_docs/human_report_dataset_audit/HUMAN_REPORT_DATASET_INTAKE_AND_AUDIT.md`
    - then review:
      `z_reference_docs/human_report_dataset_audit/HUMAN_REPORT_DATASET_VISUAL_AUDIT.md`
    - use the `accurate` and `accepted_after_user_review` buckets as the first
      candidate prompt-example pool
    - keep held-out `no_reports/` material out of prompt work unless it is
      explicitly repaired later
    - `20`, `61`, `84`, and `101` were reviewed and accepted by the user on
      `2026-04-27`; `61.txt` was adjusted so the distant far-left truck is
      `probable` instead of `confirmed`
  - current benchmark interpretation:
    - Graphify is high-signal for narrow implementation questions such as
      `DetectorBackend`
    - broad project-state questions still need curated docs or verified query
      notes before graph recall should be treated as sufficient
  - query-quality hardening is now implemented:
    - `.graphify_project_brain/capstone_graphify.py` provides `update`,
      `wiki`, `benchmark`, `doctor`, `evidence-index`, `analytics`,
      `estimate-extraction`, `extraction-pilot`, `diff`, `path`, `explain`,
      `recall`, `recall-benchmark`, and `graphml` commands
    - `recall` is now the preferred first Graphify doorway for project-state,
      promotion, evidence, and decision questions because it checks
      source-verified notes and accepted semantic seeds before raw graph search
    - `recall --deep` and `search-all` now provide an opt-in broad discovery
      lane across verified notes, accepted semantic seeds, generated wiki
      articles, raw graph nodes, and derived evidence-index records; results
      are labeled by trust level so exploratory hits stay separate from
      source-verified memory
    - `recall-benchmark` now guards expected retrieval targets such as the
      Qwen promotion path, `v014` resolved-config hash caveat,
      `office_negative` raw JSON review boundary, `WORKTREE_STATE.yaml`
      contract, and `DetectorBackend` implementation seed
    - `doctor --strict-stale` is available when graph freshness must be
      enforced instead of merely reported
    - local-only evidence query surfaces now exist:
      - `.capstone_evidence/evidence.sqlite`
      - `.capstone_evidence/analytics.duckdb`
      - MCP entries `capstone-evidence-sqlite` and `capstone-evidence-duckdb`
    - architecture-specific and project-state benchmark packs now generate
      pack-specific benchmark reports
    - prompt/version visual diffs now write Markdown/HTML review aids under
      `.capstone_visual_diffs/`
    - broad safe-corpus LLM extraction remains gated; the current estimator
      reports `very_high` review burden across `2240` eligible files, `2318`
      chunks, about `1,339,756` approximate tokens, `11590` expected candidate
      edges, and `2307` expected candidate notes
    - current broad extraction gate recommendation:
      `stop_before_full_extraction`
    - the first stage-only extraction pilot has now run:
      - pilot root:
        `.graphify_project_brain/archive/extraction_pilots/failed_or_incomplete/pilot_2026-04-24_172000Z/`
      - shards: `architect_docs` first, then `qwen_evidence`
      - outputs reviewed: `9`
      - staged items reviewed: `292`
      - source-supported items: `292`
      - unsupported items: `0`
      - duplicate items: `0`
      - invalid outputs: `1`
      - final pilot recommendation:
        `revise_extraction_contract_before_full_run`
      - no staged output was ingested into verified memory or semantic seeds
    - the contract-fix confirmation has now passed:
      - first confirmation root:
        `.graphify_project_brain/archive/extraction_pilots/failed_or_incomplete/pilot_2026-04-24_174500Z/`
      - final confirmation root:
        `.graphify_project_brain/extraction_pilots/pilot_2026-04-24_175500Z/`
      - final confirmation outputs reviewed: `1`
      - final confirmation staged items reviewed: `33`
      - final confirmation source-supported items: `33`
      - final confirmation unsupported items: `0`
      - final confirmation duplicate items: `0`
      - final confirmation invalid outputs: `0`
      - final confirmation recommendation:
        `ready_for_full_safe_corpus_extraction`
      - no staged output was ingested into verified memory or semantic seeds
    - the runtime/eval architecture domain pilot has now passed:
      - pilot root:
        `.graphify_project_brain/extraction_pilots/pilot_pilot_2026-04-24_183942Z/`
      - shard: `runtime_eval_architecture`
      - outputs reviewed: `6`
      - staged items reviewed: `116`
      - source-supported items: `116`
      - unsupported items: `0`
      - duplicate items: `0`
      - invalid outputs: `0`
      - final recommendation:
        `ready_for_full_safe_corpus_extraction`
      - no staged output was ingested into verified memory or semantic seeds
    - the full safe-corpus staged extraction gate has now passed:
      - pilot root:
        `.graphify_project_brain/extraction_pilots/pilot_full_safe_corpus_2026-04-24_191412Z/`
      - shards:
        `architect_docs`, `graphify_tooling`, `governance_worktrees`,
        `runtime_eval_architecture`, `qwen_evidence`, `gemma_evidence`, and
        `general_project_context`
      - outputs reviewed: `44`
      - staged items reviewed: `815`
      - source-supported items: `815`
      - unsupported items: `0`
      - duplicate identifier items: `4`
      - invalid outputs: `0`
      - source references checked: `1996`
      - do-not-ingest items: `99`
      - metadata warnings: `42`
      - final recommendation:
        `ready_for_full_safe_corpus_extraction`
      - no staged output was ingested into verified memory or semantic seeds
    - VS Code disconnected multiple times during the full extraction, but the
      file-based staged workflow recovered safely:
      - no extraction data corruption was found
      - memory and disk were healthy
      - logs pointed to repeated VS Code extension-host lock recovery and
        `openai.chatgpt` activation errors
      - the final shard completed by using one worker at a time
      - a local-only ignored `.vscode/settings.json` now excludes generated
        Graphify, evidence, and visual-diff artifacts from watcher/search load
    - focused project-brain ingestion V1 has now promoted a bounded,
      source-verified subset of the staged queue into local Graphify memory:
      - review root:
        `.graphify_project_brain/ingestion_reviews/focused_ingestion_v1_2026-04-24/`
      - verified query notes accepted: `7`
      - semantic nodes accepted: `8`
      - semantic edges accepted: `10`
      - semantic hyperedges accepted: `1`
      - accepted themes: `v014` hash caveat, adaptive-cycle truth freeze,
        bounded-runner no-self-promotion, office-negative raw JSON review,
        runtime/eval/promotion evidence flow, `WORKTREE_STATE.yaml` branch
        contract, and Graphify stage-only ingestion boundaries
      - remaining staged extraction items are still untrusted candidate memory
    - expanded doctrine plus Prompting ingestion V1.5 has now promoted a larger
      curated, source-verified subset into local Graphify memory:
      - review root:
        `.graphify_project_brain/ingestion_reviews/expanded_doctrine_prompting_v1_5_2026-04-27/`
      - Prompting pilot root:
        `.graphify_project_brain/extraction_pilots/pilot_prompting_vlm_research_2026-04-27_1438Z/`
      - Prompting pilot result: `8` outputs reviewed, `201` staged items,
        `201` source-supported items, `0` unsupported items, and `0` invalid
        outputs
      - trusted memory accepted: `17` verified query notes, `17` semantic
        nodes, `25` semantic edges, and `3` semantic hyperedges
      - accepted themes: BDA target-element scope, image-only output as initial
        evidence, building/critical-target-element boundaries, collateral/CDA
        boundaries, Qwen normalized grounding, anti-neighbor bbox prompting,
        micro-examples, and VLM visual-prompt fragility
      - all `REJECT`, unsupported, and ambiguous staged candidates stayed out
        of trusted memory
      - Prompting references remain supporting context only; they do not
        override doctrine decisions, validation manifests, runner summaries,
        promotion reports, or runtime source code
    - Graphify ingestion-readiness scoring is now implemented as a review aid
      between `extraction-pilot review` and any future trusted-memory
      ingestion package:
      - command:
        `.graphify_project_brain/capstone_graphify.py ingestion-readiness --pilot-dir <pilot>`
      - output:
        `<pilot>/ingestion_readiness/readiness_report.md`,
        `readiness_summary.json`, `accept_candidates.json`,
        `defer_candidates.json`, and `reject_candidates.json`
      - BDA doctrine pilot readiness:
        `111` accept candidates, `9` defer candidates, `15` reject candidates,
        `0` unsupported items, `0` invalid outputs, and label
        `ready_for_curated_ingestion`
      - Prompting/VLM research pilot readiness:
        `143` accept candidates, `21` defer candidates, `37` reject
        candidates, `0` unsupported items, `0` invalid outputs, and label
        `ready_for_curated_ingestion`
      - the scorer does not ingest trusted memory; it only shortlists material
        for a later curated source-check/dedupe pass
    - curated doctrine plus Prompting ingestion V2 has now promoted a second
      bounded, source-verified subset from the readiness queues:
      - review root:
        `.graphify_project_brain/ingestion_reviews/curated_doctrine_prompting_v2_2026-04-27/`
      - trusted memory accepted: `12` verified query notes, `12` semantic
        nodes, `17` semantic edges, and `2` semantic hyperedges
      - accepted themes: Phase 1 BDA nonfinality, BDA beyond destroyed-system
        counting, deception/reconstitution/time-window cautions, BDA
        review-loop discipline, target-validation versus engagement-authority
        separation, observable-effects boundaries, prompt-attempt logging,
        structured JSON tradeoffs, schema-guided inputs, prompt chaining,
        visual-prompt replay discipline, and Qwen detail controls as runtime
        levers rather than prompt-only fixes
      - deferred themes: broad Gemma capability details, OWLv2/Llama 4 adoption
        implications, and duplicate Qwen normalized-coordinate or
        anti-neighbor bbox lessons
    - Version Experiment Memory V1 has now promoted a bounded,
      source-verified subset from the full safe-corpus readiness queue:
      - review root:
        `.graphify_project_brain/ingestion_reviews/version_experiment_memory_v1_2026-04-27/`
      - trusted memory accepted: `12` verified query notes, `18` semantic
        nodes, `22` semantic edges, and `3` semantic hyperedges
      - accepted themes: Qwen `v001`-`v004` tank-seed progression, Qwen
        `v005`/`v006` detection guardrail lesson, Qwen `v007`/`v008`
        assessment progression, Qwen `v006 + v008 + v004` consolidation into
        promoted `v009`, Qwen `v010`-`v013` non-promotion lessons, Qwen `1.3`
        and `1.4` side-lane boundaries, and Gemma `v000`-`v003` plus
        doctrine-shadow status
      - no staged `REJECT`, `AMBIGUOUS`, unsupported, stale-status, or
        volatile git-state items were accepted
      - validation also removed two older pre-existing `AMBIGUOUS` semantic
        edges from trusted memory so the seed file matches the stricter
        ingestion-readiness boundary
    - trusted project-brain memory source verification is now implemented:
      - command:
        `.graphify_project_brain/capstone_graphify.py verify-memory`
      - verifier script:
        `z_reference_docs/local_tools/verify_graphify_trusted_memory.py`
      - first audit root:
        `.graphify_project_brain/archive/verification_reviews/superseded/trusted_memory_source_audit_2026-04-27_160409Z/`
      - post-refresh rerun root:
        `.graphify_project_brain/archive/verification_reviews/superseded/trusted_memory_source_audit_2026-04-27_160858Z/`
      - checked items: `288`
      - verified: `186`
      - verified with limits: `100`
      - source missing: `2`
      - duplicate trusted note slugs, node IDs, or edge IDs: `0`
      - bad trusted `REJECT` or `AMBIGUOUS` confidence entries: `0`
      - required lanes covered: Prompt_Labs evidence, runtime/eval code,
        governance, BDA doctrine, Prompting docs, Graphify local memory, and
        SQLite/DuckDB evidence DBs
      - proposed corrections for a later approved cleanup:
        `brain:overlay_runtime_config` cites
        `src/bda_svc/pipeline/runtime_config.py`, and
        `brain:trace_eval_promotion_flow` cites `src/bda_svc/tracing.py`
      - those paths are not present in `main`; treat those two semantic nodes
        as path-stale navigation hints until source links are corrected
    - trusted-memory correction and regression hardening is now implemented:
      - corrected `brain:overlay_runtime_config` and
        `brain:trace_eval_promotion_flow` to cite the active Qwen `1.2`
        worktree architecture files instead of nonexistent `main` paths
      - added strict verification:
        `.graphify_project_brain/capstone_graphify.py verify-memory --strict`
      - added doctor integration:
        `.graphify_project_brain/capstone_graphify.py doctor --strict-memory`
      - added expanded recall expectations:
        `.graphify_project_brain/capstone_graphify_recall_expectations.json`
      - latest strict audit root:
        `.graphify_project_brain/archive/verification_reviews/superseded/trusted_memory_source_audit_2026-04-27_174621Z/`
      - latest strict audit result: `188` verified, `100` verified with
        limits, `0` source-missing items, `0` duplicate trusted IDs, `0` bad
        trusted confidence entries, and `0` missing generated note Markdown
        files
      - expanded recall regression result: `20` checks, `0` failures
    - focused promotion/eval memory V1 has now strengthened recall before
      Qwen `v014` promotion-package planning:
      - review root:
        `.graphify_project_brain/ingestion_reviews/promotion_eval_memory_v1_2026-04-27/`
      - trusted memory accepted: `5` verified query notes, `5` semantic
        nodes, `8` semantic edges, and `1` semantic hyperedge
      - accepted themes: formal `v014` promotion package required artifacts,
        clean promotion-mode re-score behavior, broader visual validation
        behavior, no direct fold-in from clean scores, and the eval behavior
        summaries that mattered before the later human-report comparison
      - recall regression suite now covers `26` checks with `0` failures
      - this is project-brain memory only; it does not promote `v014` or change
        runtime code, prompts, overlays, references, manifests, promotion
        artifacts, or model-line truth
    - Qwen `v014` formal promotion package Step 1 now exists:
      - machine-readable package:
        `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/promotion_reports/v014_detect_weighted_building_selection_pending_promotion.yaml`
      - human-facing package note:
        `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/decisions/qwen_1_2_v014_formal_promotion_package_2026-04-27.md`
      - package state:
        `formal_package_ready_pending_user_approved_fold_in`
      - promotion report decision: `deferred`
      - no tracked runtime/config fold-in has happened
      - `v009` remains the promoted Qwen baseline until a later explicit Step 2
        approval
    - broad source-verified seed notes now cover Qwen promotion path, why
      `v014` was package-ready under declared-pack evidence but is now paused,
      `v009`/`v010`/`v014` evidence,
      building-reference truth, backend deferral, Gemma control status,
      Qwen `1.3` evidence debt, architect rollout status, worktree/main
      governance, BDA doctrine target-element boundaries, Qwen grounding
      lessons, Prompting research guidance, and MCP/Graphify boundaries
    - latest graph stats after hardening:
      - architecture/fleet: `12565` nodes and `27950` links
      - project-brain: `12660` nodes and `30033` links
    - the preserved architecture/fleet graph now has a clearer generated
      `FLEET_KNOWLEDGE_REPORT.md`; its older `PROJECT_BRAIN_REPORT.md` file is
      retained only as a compatibility alias
    - GraphML exports now exist for both profiles as local-only interoperability
      artifacts
- the approved `destroyed_building3` executable truth correction is now
  implemented in the Qwen `1.2` guard-pack manifest:
  - `experiments/validation/qwen_six_case_guard_pack_v1.yaml`
  - `experiments/validation/references/qwen_six_case_guard_pack_v1/destroyed_building3_corrected_2026-04-23.json`
- corrected-truth replay completed for the important Qwen reads:
  - `v009` control and `v010` candidate:
    `experiments/runner_sessions/executions/qwen_1_2_v010_detect_overlay_session_v1_2026-04-23_211612Z/`
  - `v014` candidate:
    `experiments/runner_sessions/executions/qwen_1_2_v014_detect_weighted_building_selection_session_v1_2026-04-23_211842Z/`
  - exact `v014` confirmation replay:
    `experiments/runner_sessions/executions/qwen_1_2_v014_detect_weighted_building_selection_session_v1_2026-04-23_212114Z/`
- corrected-truth result:
  - `v009` control failed the corrected guard pack with `2` false positives
  - `v010` improved to `1` guard-pack false positive but still kept the
    `destroyed_building3` background false positive
  - `v014` passed both the corrected six-case guard pack and grounding pack
    twice with `0` false positives and `0` false negatives
- broader visual validation is now complete for the replay-comparable Qwen
  versions:
  - artifact:
    `experiments/visual_validation/qwen_1_2_v014_broader_visual_validation_2026-04-23/README.md`
  - scope: `v009`, `v010`, and `v014` across the declared guard and grounding
    packs
  - outcome: `v014_visual_validation_passed_for_declared_packs`
- promotion-readiness review is now complete:
  - artifact:
    `experiments/decisions/qwen_1_2_v014_promotion_readiness_review_2026-04-23.md`
  - outcome: `ready_for_formal_promotion_package`
  - deterministic promotion-mode re-score: `0` false positives and `0` false
    negatives on both declared packs
- standing interpretation:
  - `v009` remains the confirmed promoted/tracked Qwen baseline
  - `v014` is now a promotion-paused historical follow-up overlay after the
    all-112 human-report comparison showed false-positive reduction with recall
    loss
  - do not promote `v014` or fold it into tracked runtime/config truth from
    declared-pack scores; use the human-report comparison to plan `v015`

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

Latest update on `2026-04-28` for reference organization:

- Phase 5 completed the audit-only `Data_set_Storage` path review:
  - audit package:
    `z_reference_docs/zz_archive/data_set_storage/`
  - `human_reports/` remains hot and in place as the active approved
    human-report source lane plus held-out no-report material
  - `Unlabeled Photos/` remains high-risk and in place because Prompt_Labs and
    validation history reference it
  - `Reports_(OLD)/`, `Updated_Reports/`, `RoboFlow_/`, and
    `Unlabeled_Photos/` are future review/cleanup candidates only
  - no data folders, source images, human reports, Prompt_Labs evidence,
    worktrees, source files, or Graphify outputs moved
- Phase 5A completed the review-only `DATA_SET` report provenance review:
  - review package:
    `z_reference_docs/zz_archive/data_set_storage/DATA_SET_REPORT_PROVENANCE_REVIEW.md`
  - `Reports_(OLD)/` is historical prose provenance, not a delete candidate
  - `Updated_Reports/` is a partial structured-conversion lane, not a clean
    authoritative replacement
  - no old or updated report files, Zone.Identifier companions, folders,
    images, Prompt_Labs evidence, or worktrees moved
- Phase 5B completed the review-only empty-folder cleanup review:
  - review package:
    `z_reference_docs/zz_archive/data_set_storage/EMPTY_FOLDER_CLEANUP_REVIEW.md`
  - seven empty-folder candidates were found under `Data_set_Storage`
  - `RoboFlow_/` and the whole `Unlabeled_Photos/` empty tree are the
    lowest-risk later cleanup candidates
  - empty folders under `Unlabeled Photos/` and
    `DATA_SET/Assigned_Photos_to_Write_Report/` remain deferred until their
    parent lanes are reviewed
  - no empty folders, dataset files, images, reports, Prompt_Labs evidence, or
    worktrees were moved or deleted
- After explicit approval, only the empty `RoboFlow_/` placeholder was removed:
  - cleanup record:
    `z_reference_docs/zz_archive/data_set_storage/ROBOFLOW_EMPTY_FOLDER_CLEANUP.md`
  - rollback command:
    `mkdir -p z_reference_docs/Data_set_Storage/RoboFlow_`
  - `Unlabeled_Photos/` and all other empty folders remain in place
- Phase 4 of the organization effort completed the redundancy and
  consolidation review as a recommendation package:
  - source:
    `z_reference_docs/zz_archive/REDUNDANCY_REVIEW.md`
  - canonical/supporting roles are now recorded for program reports,
    architect rollout docs, Codex/MCP tooling docs, prompt-method docs,
    worktree governance docs, capstone tech-doc tracking, and human-report/data
    surfaces
  - no active docs were merged, moved, deleted, renamed, or consolidated
  - proposed future rows were added to
    `z_reference_docs/zz_archive/PROPOSED_MOVE_MANIFEST.csv`, but no Phase 4
    row is marked completed
- Phase 4B completed the tiny live-doc wording cleanup for stale
  SequentialThinking deactivation text:
  - updated `PROMPT_DEVELOPMENT_METHODOLOGY.md`
  - updated `PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`
  - updated `capstone_tech_docs/understanding_tracking.md`
  - marked the manifest row as `completed_wording_cleanup`
- Phase 3 of the organization effort registered existing archive folders
  without moving them:
  - `z_reference_docs/Prompt_Labs/archive/` is registered at
    `z_reference_docs/zz_archive/indexed_existing_archives/Prompt_Labs_archive.md`
  - `z_reference_docs/Prompting/Model_research-Archive-Not-to-be Used/` is
    registered at
    `z_reference_docs/zz_archive/indexed_existing_archives/Prompting_model_research_archive.md`
  - original archive paths remain authoritative for historical source checks
- Phase 2 of the organization effort cleaned up Graphify generated-history
  clutter only inside ignored `.graphify_project_brain/` archive folders:
  - failed or incomplete extraction pilots now live under
    `.graphify_project_brain/archive/extraction_pilots/failed_or_incomplete/`
  - superseded trusted-memory verification reviews now live under
    `.graphify_project_brain/archive/verification_reviews/superseded/`
  - the latest three verification reviews remain hot
  - successful pilots, ingestion reviews, current graphs, trusted seed JSON,
    evidence indexes, and newest snapshots remain hot
- Phase 1 of the `z_reference_docs` organization effort moved only approved
  loose local-doc files into `z_reference_docs/zz_archive/`:
  - `z_reference_docs/zz_archive/backups/configs/config.yaml.backup`
  - `z_reference_docs/zz_archive/research/model_shortlists/Notes_2026-04-28.txt`
  - `z_reference_docs/zz_archive/codex_agents/Prompt_to_Start_up_agents_in_new_project_2026-04-28.txt`
  - `z_reference_docs/zz_archive/workspaces/Capstone.code-workspace`
- Phase 0 remains the inventory and planning baseline:
  - central archive planning hub:
    `z_reference_docs/zz_archive/`
  - proposed move manifest:
    `z_reference_docs/zz_archive/PROPOSED_MOVE_MANIFEST.csv`
- `z_reference_docs/Capstone-Project.code-workspace` remains the hot workspace
  file because it includes the main checkout and active worktree root
- keep active live docs, current human-report challenge evidence, Prompt_Labs,
  Data_set_Storage, and current Graphify graphs hot until separate
  approval-gated waves
- the next organization choice is either an explicit delete-or-archive approval
  for the remaining `Unlabeled_Photos/` empty tree, a repair/review package for
  the old `DATA_SET` updated reports if they become useful again, or a later
  approved archive move for a Phase 4A document candidate

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

### 2026-04-30 - Enabled Global Creature-Friendly Codex Instructions

- created the persistent custom instruction file:
  `/home/williambenitez1/.codex/model_instructions/gpt-5.5-creatures-free.txt`
- updated `/home/williambenitez1/.codex/config.toml` with
  `model_instructions_file` so new Codex sessions use that file globally,
  including full-access sessions unless a launch flag or profile overrides it
- generated the file from the cached `gpt-5.5` base instructions while removing
  the goblin/gremlin/raccoon/troll/ogre/pigeon/creature suppression line
- validation confirmed:
  - `model = "gpt-5.5"`
  - the custom instruction file exists with permission `600`
  - the custom file no longer contains the creature-suppression terms
  - Codex CLI config loading succeeds
- boundary:
  - this is a personality/instruction override only
  - it does not override system/developer instructions, project guardrails,
    Capstone source authority, MCP boundaries, Mem0 approval gates, Graphify
    verification, prompt/eval gates, or user approval requirements

### 2026-04-28 - Updated Mem0 Manual Operating Doctrine

- recorded the active Mem0 operating doctrine across global and Capstone
  instruction/routing surfaces:
  - Mem0 remains manual/deliberate; no every-prompt search
  - Mem0 is advisory memory, not evidence or source truth
  - source/project artifacts and Graphify/project-brain verified memory remain
    authoritative for project truth
  - Mem0 writes/deletes require explicit user approval
  - no lifecycle hooks, no plugin, and no automatic writes
- updated the canonical tool inventory and Capstone overlay so future
  spences10/NCP/MCPFinder planning sees the same boundary
- no Mem0 memory write/delete tools were called in this doctrine update
- Graphify refresh is required after this live-doc update by normal Capstone
  policy and was handled as part of closeout

### 2026-04-23 — Added Local-Only Capstone Graphify Fleet Graph

Implemented the Capstone Graphify fleet profile as a local-only architecture
and evidence-navigation aid.

What changed:

- rule-disabled `SequentialThinking` until the user explicitly re-enables it:
  - global and project instruction layers now say not to invoke the
    `sequentialthinking` tool
  - this is a rules-level deactivation, not an MCP uninstall
- hardened the global Graphify skill at
  `/home/williambenitez1/.codex/skills/graphify/SKILL.md`
- created a local ignored Graphify profile under `.graphify_fleet/`
- mirrored a safe corpus from:
  - `/home/williambenitez1/Capstone`
  - all seven active Capstone worktree roots under
    `/home/williambenitez1/Capstone_worktrees`
- generated:
  - `.graphify_fleet/corpus/graphify-out/GRAPH_REPORT.md`
  - `.graphify_fleet/corpus/graphify-out/graph.json`
  - `.graphify_fleet/corpus/graphify-out/fleet_manifest.json`
- updated routing docs so architecture, worktree-map, dependency, and "how does
  this all connect" questions can start from the generated Graphify report when
  it exists

Safety boundary:

- Graphify outputs are generated local artifacts, not tracked repo truth.
- The corpus excludes secrets, `.env` files, credential/key files, caches,
  generated run artifacts, datasets, raw media, and binary-heavy outputs.
- Important graph-derived claims still need verification against source files,
  manifests, decision notes, or runner artifacts before acting.

Validation:

- `graphify --help` works.
- the initial fleet graph was built successfully with `8077` nodes, `9966`
  edges, `9` root/worktree communities, `2231` mirrored source files, and about
  `1.0M` indexed words.
- a graph query smoke test succeeded from `.graphify_fleet/corpus/`.
- the graph-derived `v014`/`v009` status read was verified against the Qwen
  `1.2` README and `v014` promotion-readiness decision note.

### 2026-04-24 — Upgraded Graphify Into Capstone Project Brain V1

Built the first hybrid Capstone project brain.

What changed:

- added the curated tracked entrypoint:
  - `z_reference_docs/PROJECT_BRAIN.md`
- upgraded the local ignored Graphify profile from a structural fleet map into a
  semantic project-brain build
- added generated local-only brain output:
  - `.graphify_fleet/corpus/graphify-out/PROJECT_BRAIN_REPORT.md`
- the semantic pass now adds:
  - project concept mention edges
  - rationale nodes and `rationale_for` edges
  - extracted file-reference edges
  - inferred concept co-mention edges
  - worktree-equivalent file edges
  - sparse hyperedges

Current generated baseline:

- `2232` mirrored files across `main` plus seven active worktrees
- `9031` graph nodes
- `17029` graph edges
- `9` root/worktree communities
- `2231` semantically processed files
- `919` semantic/rationale nodes
- `9576` semantic edges
- `405` hyperedges

Interpretation:

- the brain is stronger than the first fleet graph because it now links docs,
  decisions, worktrees, runtime/eval concepts, and promotion evidence through
  explicit concept and rationale edges
- it remains a navigation and recall layer, not project truth
- graph-derived claims still require verification against source artifacts
  before implementation, promotion, or reporting decisions

### 2026-04-24 — Added Dual Graphify MCP Routing And Project-Knowledge Brain Profile

Implemented the two-graph Graphify split.

What changed:

- preserved `.graphify_fleet/` as the architecture/fleet graph for code,
  runtime, detector/eval structure, and worktree-map questions
- added a second ignored local profile:
  - `.graphify_project_brain/`
- added a project-knowledge build script:
  - `.graphify_project_brain/build_project_brain_graph.py`
- added semantic seed relationships from read-only extraction agents for:
  - Qwen `v009`/`v010`/`v014` evidence and promotion readiness
  - building-reference truth audit and corrected replay interpretation
  - backend-pilot deferral
  - Gemma `v002` control and paused Gemma lanes
  - worktree governance and MCP boundaries
- added two Graphify MCP wrapper entries:
  - `capstone-architecture-graph`
  - `capstone-project-brain`
- updated `PROJECT_BRAIN.md`, `REFERENCE_MASTER_INDEX.md`, root `AGENTS.md`,
  and the global MCP guide so future graph use is routed by question type

Generated project-knowledge baseline:

- `2232` mirrored files across `main` plus seven active worktrees
- `9056` graph nodes
- `17374` graph links
- `415` hyperedges
- `2231` semantically processed files
- semantic seed injection added `11` nodes, `9` links, and `2` hyperedges,
  including explicit `AMBIGUOUS` edges for unresolved Qwen `1.3` and Gemma
  `v003` evidence-debt lanes

Safety boundary:

- generated graph outputs remain ignored and local-only
- both graph corpora exclude secrets, credential-like files, raw datasets/media,
  caches, generated run artifacts, and binary-heavy outputs
- Graphify remains a navigation aid; source artifacts still win

### 2026-04-24 — Hardened Graphify Query Quality And Reviewed The Architecture Graph

Implemented Deep Semantic V1 query-quality hardening for the Capstone
project-brain graph and performed the planned review of the preserved
architecture/fleet graph.

What changed:

- added `.graphify_project_brain/capstone_graphify.py` as the local profile
  utility with `update`, `wiki`, `benchmark`, `doctor`, `diff`, `path`,
  `explain`, and `graphml` subcommands
- moved fixed benchmark questions into
  `.graphify_project_brain/capstone_graphify_questions.json`
- expanded the project-brain semantic seed pack to cover recurring broad
  project-state questions, including Qwen `v014` promotion path, why `v014` is
  not promoted yet, Qwen `v009`/`v010`/`v014` evidence, corrected building
  truth, backend-pilot deferral, Gemma `v002`/`v003`, Qwen `1.3`, architect
  rollout status, worktree governance, and MCP/Graphify boundaries
- added source-verified query-note seeds at
  `.graphify_project_brain/verified_query_seed_notes.json`; the usefulness
  exporter writes them into
  `.graphify_project_brain/corpus/graphify-out/memory/verified/`
- generated GraphML exports for both profiles:
  - `.graphify_fleet/corpus/graphify-out/capstone_architecture_graph.graphml`
  - `.graphify_project_brain/corpus/graphify-out/capstone_project_brain.graphml`
- clarified the architecture/fleet graph's generated semantic report as
  `.graphify_fleet/corpus/graphify-out/FLEET_KNOWLEDGE_REPORT.md`, while
  retaining the older `PROJECT_BRAIN_REPORT.md` filename as a compatibility
  alias

Validation:

- `capstone_graphify.py doctor` passed for both graphs, reports, wiki,
  benchmarks, verified notes, GraphML exports, ignored status, and MCP wrapper
  presence
- `capstone_graphify.py diff --profile both` recorded:
  - architecture/fleet: `9031 -> 9034` nodes and `17029 -> 17033` edges
  - project-brain: `9056 -> 9064` nodes and `17374 -> 17384` edges
- a final post-doc-refresh rebuild brought the current on-disk graph baselines
  to:
  - architecture/fleet: `9036` nodes and `17034` edges
  - project-brain: `9066` nodes and `17385` edges
- local path/explain smoke checks now resolve the Qwen `v014` formal promotion
  path directly to the source-verified semantic seed node

Interpretation:

- this pass improves broad project-state query starts without pretending the
  graph is authoritative
- the architecture/fleet graph is still useful as the code/worktree map, so it
  received naming clarity and GraphML export rather than a heavier rework
- high-overhead Graphify extensions remain deferred: watch hooks, Neo4j,
  Obsidian/Canvas, full HTML visualization, and broad unconstrained LLM
  extraction over the full corpus

### 2026-04-23 — Added A Short Completed-Vs-Deferred Checklist For The Architect Rollout

What changed:
- added a dedicated local status file:
  - `z_reference_docs/ARCHITECT_FEEDBACK_COMPLETION_CHECKLIST.md`
- updated `REFERENCE_MASTER_INDEX.md` so the new checklist is discoverable from
  the normal startup sweep and doc-routing flow

Why it matters:
- we now have one explicit answer to the recurring question:
  - did we complete the architect feedback
- it separates:
  - the five implemented architect phases
  - the intentionally deferred future items
- that should reduce future confusion between:
  - completed rollout work
  - optional later architecture follow-ons

Current consequence:
- future sessions should use the checklist as the quick status bridge between
  the architect handoff and the implementation phases recorded later in this
  changelog
- the correct short status is now documented as:
  - yes for the agreed five-phase rollout
  - no for every optional future idea the architect mentioned

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
- `v010` remained the active local Qwen detect follow-up candidate under the
  then-current read; later review now caveats that status pending the
  `destroyed_building4` building-reference audit, while `v009` remains the
  confirmed promoted Qwen control baseline
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
- `v010` remained the active local Qwen detect follow-up candidate under the
  then-current read; later review now caveats that status pending the
  `destroyed_building4` building-reference audit, while `v009` remains the
  confirmed promoted Qwen control baseline
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
- `v010` remained the active local Qwen detect follow-up candidate under the
  then-current read; later review now caveats that status pending the
  `destroyed_building4` building-reference audit, while `v009` remains the
  confirmed promoted Qwen control baseline
- both live Qwen worktrees were restored from `v013` back to `v010`
- the next useful clue is now explicit:
  hierarchy matters, but the active line may need a hierarchy change that is
  even more tightly coupled to the building-selection language around
  `destroyed_building3`

### 2026-04-22 — Private Staff-Architect Review Snapshot Was Created

What changed:
- created a new standalone private personal repo:
  `metalbladex4/bda-svc-staff-architect-review`
- used it as a branch-preserving private review snapshot for the current local
  Capstone workspace, including the local `z_reference_docs` evidence layer and
  the active branch/worktree line
- packaged the review repo with dedicated orientation files so an external
  Staff AI Systems Architect / Prompt-Evaluation lead can understand:
  - how `z_reference_docs` fits into the project
  - which parts are runtime code versus local evidence or reference shelves
  - which Codex-only surfaces exist locally but are not visible from GitHub

Why it matters:
- this gives us a private outside-review surface without exposing the work on
  the public team repo or public fork
- it preserves a recoverable snapshot of the project state, branch line, and
  local evidence system as of this point in time
- it also makes the intended future boundary explicit:
  the private review repo is not the new working repo

Current consequence:
- normal work should continue in `/home/williambenitez1/Capstone` and the real
  Capstone worktrees, not in the private review repo
- future pushes to `metalbladex4/bda-svc-staff-architect-review` should happen
  only when explicitly requested
- the review snapshot can now act as:
  - a private architectural review surface
  - a point-in-time backup of the local workflow state
  - a recovery/reference source if later work needs to revisit or recover
    something that existed at snapshot time

### 2026-04-22 — Architect Review Snapshot Was Temporarily Made Public

What changed:
- changed `metalbladex4/bda-svc-staff-architect-review` from private to public
  so ChatGPT Pro can inspect the repository through GitHub
- kept the repo purpose the same:
  it is still a review snapshot and not the active development repo

Why it matters:
- the original private visibility blocked the intended external repo-grounded
  review flow in ChatGPT
- making it public removes that access barrier for the current review pass

Current consequence:
- the architect-review repo is temporarily public until we explicitly switch it
  back to private after the review is complete
- normal work should still continue only in `/home/williambenitez1/Capstone`
  and the real Capstone worktrees
- future refreshes or visibility changes to the architect-review repo should
  still happen only when explicitly requested

### 2026-04-22 — Worktree State Contract And Preservation-Aware Refresh Rules Were Added

What changed:
- added a canonical local worktree-state contract at:
  `z_reference_docs/WORKTREE_STATE.yaml`
- added a local validator at:
  `z_reference_docs/local_tools/validate_worktree_state.py`
- patched the local AGENTS/workflow layer so governed worktrees now point to
  `WORKTREE_STATE.yaml` for volatile branch state instead of hardcoding that
  state directly in AGENTS
- updated the worktree refresh workflow and the Qwen/Gemma refresh checklists
  so future upstream refreshes now include:
  - a Branch Direction Preservation Gate
  - explicit shadow-lane ordering
  - validator use before and after refresh

Why it matters:
- this turns future upstream integration into a contract-driven process rather
  than relying on memory or assuming a clean rebase preserved the intended
  direction
- it also fixes the live stale-state problem where governed worktree AGENTS
  files had started to drift from the branch READMEs and actual worktree state

Current consequence:
- the clean `main` mirror remains untouched and upstream-aligned
- branch-local worktrees now have an explicit place to declare:
  - active direction
  - allowed dirty files
  - control/shadow relationships
  - protected invariants that future refreshes must preserve
- future upstream refreshes should now be treated as incomplete until:
  - the branch-direction preservation gate is checked
  - the validator passes
  - the declared invariants still survive after the refresh
- the validator now passes for all seven governed branch entries, and the
  workflow docs/checklists were normalized to use `uv run python` for the
  validator command in this environment

### 2026-04-23 — Phase 2 Qwen Eval/Traceability Hardening Landed On `1.2`

What changed:
- classified the dirty Qwen `1.3` pair in:
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.3_feat__qwen3-vl-8b-instruct__doctrine-bda-alignment/DIRTY_PAIR_CLASSIFICATION.md`
  before reopening any further branch-local behavior work
- added branch-local runtime trace capture on the active Qwen `1.2` line:
  - `--debug-trace`
  - `--trace-dir`
  - `BDA_DEBUG_TRACE=1`
  - per-image `trace_meta.json` and `trace.jsonl`
- hardened `bda_eval` in the Qwen `1.2` worktree with:
  - `--manifest`
  - `--eval-mode {legacy,detection_study,promotion}`
  - manifest validation
  - negative-scene scoring for `object_not_found / NOT APPLICABLE`
  - richer localization metrics
  - machine-readable `summary.json`
- added the first explicit Qwen phase-2 validation contracts under:
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/validation/`
  - `qwen_feature_smoke_recipe_v1.yaml`
  - `qwen_six_case_guard_pack_v1.yaml`
  - `grounding_generalization_pack_v1.yaml`
  plus companion Markdown notes where needed
- updated the Qwen `1.2` README and `WORKTREE_STATE.yaml` so the active branch
  state now records:
  - phase-2 eval/trace hardening in progress on the control branch
  - expanded allowed dirty tracked files for the active worktree
  - explicit smoke/validation pack IDs

Why it matters:
- this is the first real implementation pass for the architect’s eval and
  traceability tranche, not just a planning note
- the active Qwen control lane now has a cleaner operator path for:
  - smoke checks
  - guard-pack execution
  - broader grounding promotion reads
- negative scenes are now treated as a scored evaluation path rather than an
  “unknown NOT_APPLICABLE” dead end
- the branch now preserves more useful machine-readable evidence for future
  debugging and promotion decisions

Current consequence:
- the active Qwen `1.2` worktree is now the phase-2 implementation surface
- the Qwen `1.3` doctrine shadow lane remains paused as classified evidence
  debt and should not absorb phase-2 prompt/doctrine changes yet
- Gemma is still deferred until the Qwen tranche is validated and stabilized
- targeted branch tests now pass for:
  - `tests/unit/test_cli.py`
  - `tests/unit/test_export.py`
  - `tests/unit/test_main.py`
  - `tests/unit/test_model.py`
  - `tests/unit/test_yamls.py`
  - `bda_eval/tests`

### 2026-04-23 — Phase 3 Qwen Runtime Semantics Hardening Landed On `1.2`

What changed:
- rewrote the tracked Qwen `1.2` runtime doctrine at:
  `src/bda_svc/pipeline/doctrine.yaml`
  so the active runtime doctrine is now explicitly visual-only
- added a maintained broader doctrinal reference file at:
  `z_reference_docs/Doctrine_Experiments/Phase_1_Doctrine_Replacement/doctrine_full_reference.yaml`
- clarified the doctrine package split so:
  - runtime doctrine is the active visual-runtime authority
  - `doctrine_full_reference.yaml` is the maintained local reference shelf
  - `current_live_doctrine.snapshot.yaml` remains historical
- tightened `summarize_scene` in the active Qwen `1.2` control branch with:
  - a stricter scene-summary prompt
  - a lightweight rule-based runtime guard
  - a deterministic fallback summary built only from structured target results
- added branch tests covering:
  - unsupported subtype rejection
  - unsupported infrastructure wording rejection
  - unsupported stronger damage/impact claims
  - conservative no-target fallback behavior

Why it matters:
- this is the first runtime-semantics hardening pass from the architect review,
  not just another prompt-surface experiment
- the active Qwen control line now has a cleaner semantic boundary between:
  - visual runtime doctrine
  - broader local doctrinal reference
  - scene-level summary text versus structured target truth
- it reduces the risk that scene summaries quietly reintroduce target subtypes,
  infrastructure assumptions, or broad mission/operational effects that are not
  supported by the structured target assessments

Current consequence:
- the active Qwen `1.2` control branch now carries both:
  - phase-2 eval/traceability hardening
  - phase-3 visual-runtime doctrine and constrained-summary hardening
- the Qwen `1.3` doctrine shadow lane still remains paused evidence debt and
  should **not** be read as resolved by the new control-branch baseline
- targeted branch validation passed after the phase-3 change set:
  - `tests/unit/test_cli.py`
  - `tests/unit/test_export.py`
  - `tests/unit/test_main.py`
  - `tests/unit/test_model.py`
  - `tests/unit/test_utilities.py`
  - `tests/unit/test_yamls.py`
  - `bda_eval/tests`
- the manifest-driven Qwen smoke path still completed successfully through:
  - `experiments/validation/qwen_feature_smoke_recipe_v1.yaml`
- `WORKTREE_STATE.yaml` now records the phase-3 baseline and updated allowed
  dirty files for the active Qwen control branch

### 2026-04-23 — Phase 4 Qwen Promotion And Experiment-Integrity Hardening Landed On `1.2`

What changed:
- added machine-readable hypothesis cards under the active Qwen `1.2` prompt
  lab:
  - `experiments/hypotheses/`
- added machine-readable promotion reports as the new promotion authority:
  - `experiments/promotion_reports/`
- backfilled one historical promotion example for the already-promoted
  `v009_unified_best-stack`:
  - hypothesis backfill:
    `experiments/hypotheses/qwen_1_2_v009_unified_stack_promotion_backfill.yaml`
  - promotion report:
    `experiments/promotion_reports/v009_unified_best_stack_promotion.yaml`
  - backfilled promotion pack:
    `experiments/validation/qwen_v009_promotion_pack_v1.yaml`
- added a new prompt-lab integrity validator in:
  - `z_reference_docs/local_tools/validate_prompt_lab_integrity.py`
  - with supporting schema files in:
    `z_reference_docs/local_tools/schemas/`
- added tracked branch integrity support on the active Qwen worktree with:
  - `scripts/prompt_lab_contracts.py`
  - `scripts/validate_prompt_lab_integrity.py`
  - `tests/unit/test_prompt_lab_integrity.py`
  - a new `integrity` job in `.github/workflows/ci.yml`
- made the promotion rule explicit across the docs:
  - deterministic metrics and required packs are the gate
  - manual visual/doctrinal review is the second gate
  - LLMaaJ is advisory only

Why it matters:
- phase 4 turns the Qwen control line from a workflow explained mostly by
  winner notes and run manifests into one with machine-readable promotion
  authority
- it also gives the branch a real integrity slice in CI without adding heavy
  Ollama-dependent evaluation to GitHub Actions
- the new backfilled `v009` record gives future work one concrete historical
  example of what a valid promotion packet should look like

Current consequence:
- future Qwen `1.2` experiments should now start with a hypothesis card
- future Qwen `1.2` promotions should now require a promotion report
- the Qwen `1.3` doctrine shadow lane still does not self-promote; it remains
  subordinate to the control-line promotion workflow
- the full prompt-eval-runner Codex skill remains intentionally deferred until
  the manual phase-4 workflow proves stable enough to package cleanly

### 2026-04-23 — Phase 5 Qwen Overlay-First Architecture Landed On `1.2`

What changed:
- re-baselined the tracked Qwen `1.2` control runtime back to the last formally
  promoted `v009` stack in:
  - `src/bda_svc/pipeline/config.yaml`
- introduced explicit runtime config resolution and overlay layering in:
  - `src/bda_svc/pipeline/runtime_config.py`
- split detection behind a backend interface while keeping the current prompt
  detector as the only concrete backend in this phase:
  - `src/bda_svc/pipeline/interfaces.py`
  - `src/bda_svc/pipeline/detectors.py`
  - runtime backend id: `vlm_prompt_detector`
- added tracked model-line overlay support under:
  - `src/bda_svc/pipeline/overlays/model_lines/`
- preserved the former live `v010` detect-only direction as the first explicit
  local overlay-backed candidate under:
  - `experiments/overlays/qwen_1_2_v010_detect_adjacent_building_priority.yaml`
- added a matching explicit control overlay for the rebaselined `v009` control
  state:
  - `experiments/overlays/qwen_1_2_v009_control_baseline.yaml`
- added bounded runner session specs under:
  - `experiments/runner_sessions/`
  - historical control anchor:
    `qwen_1_2_v009_historical_promotion_backfill_v1.yaml`
  - active overlay-backed session:
    `qwen_1_2_v010_detect_overlay_session_v1.yaml`
- extended the prompt-lab contract and schemas so hypothesis cards and
  promotion reports now carry:
  - overlay ids or overlay stacks
  - runner session ids
  - detector backend ids
  - resolved config hashes
- updated traces and report metadata so they now carry:
  - `detector_backend_id`
  - `resolved_config_hash`
  - `experiment_overlay_ids`
- added the bounded local runner and the new tracked integrity slice:
  - `scripts/run_bounded_experiment_runner.py`
  - `tests/unit/test_runtime_config.py`
  - `tests/unit/test_runner_session.py`
  - updated `.github/workflows/ci.yml` integrity job

Why it matters:
- phase 5 finishes the architect’s near-term architecture pass by separating:
  - promoted tracked control truth
  - overlay-backed local candidates
  - bounded runner execution
  - future backend-pluggability hooks
- it makes future Qwen experimentation less fragile because the active control
  baseline no longer has to carry whichever local candidate happened to be
  under test that day
- it also creates the contract needed for a later detector pilot or future
  prompt-eval-runner Codex skill without granting open-ended automation now

Current consequence:
- `v009` is again the tracked control baseline on the active Qwen `1.2` line
- `v010` is no longer treated as direct tracked control state; it now survives
  as the first explicit overlay-backed local candidate
- future prompt/doctrine/backend candidates should now start as overlays plus
  bounded runner sessions, not direct tracked config edits
- the bounded runner can execute declared overlay queues, but it cannot
  self-promote or edit reference truth
- Qwen `1.3` remains paused evidence debt and should not be read as resolved by
  the new overlay-first control baseline

### 2026-04-23 — Post-Architect Follow-On Phases 6-10 Landed

What changed:
- created a durable Qwen backend-pilot worktree and prompt-lab root at:
  - `feat/qwen3-vl-8b-instruct/detector-backend-pilot`
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.4_feat__qwen3-vl-8b-instruct__detector-backend-pilot/`
- added the first concrete second detector backend there:
  - `vlm_tiled_detector`
- ran the first declared live control-versus-pilot backend comparison through
  the same overlay, trace, eval, and bounded-runner flow already used by the
  Qwen control line
- recorded the phase-7 strategy decision in:
  - `.../experiments/decisions/qwen_detector_backend_strategy_phase7.md`
- created the global local-only Codex skill:
  - `~/.codex/skills/bda-prompt-eval-runner/`
- added the self-hosted heavy-eval workflow on the active Qwen control line:
  - `1.2.../.github/workflows/heavy-eval.yml`
- ported the proven overlay-first control-line architecture onto the active
  Gemma `3.1` line, including:
  - runtime layering in `src/bda_svc/pipeline/config.yaml`
  - model-line overlay at
    `src/bda_svc/pipeline/overlays/model_lines/gemma4-e4b.yaml`
  - Gemma overlays, runner sessions, and hypothesis scaffolding under the
    Gemma prompt-lab root

Why it matters:
- the first concrete backend pilot is now evidence-backed rather than
  theoretical
- the first live comparison did **not** beat the control detector, so the
  branch now records a clear keep/defer decision instead of leaving the pilot
  direction ambiguous
- the bounded workflow is now packaged as a reusable local skill without
  turning the skill into runtime truth
- the Qwen control line now has a self-hosted heavy-eval path without making
  heavy Ollama work a normal GitHub-hosted CI requirement
- the Gemma control line now shares the same overlay-first and bounded-runner
  architecture as Qwen, while keeping its own evidence chain and model-line
  identity

Current consequence:
- `vlm_prompt_detector` remains the active default on the Qwen control line
- the first tiled detector pilot is preserved but deferred after the first live
  comparison
- the local `bda-prompt-eval-runner` skill is now available as an operator
  wrapper for declared runner sessions
- the heavy-eval workflow exists for self-hosted Qwen runs, but it is not yet
  a merge blocker
- Gemma `3.1` now treats `v002` as the tracked control baseline and preserves
  the old `v003` follow-up as an overlay-backed paused candidate rather than as
  implicit dirty tracked drift
- the Gemma static validators and bounded-runner dry run now pass on the new
  architecture, but the live control-session replay is still pending because
  `OLLAMA_HOST=http://127.0.0.1:11435` was unavailable during this pass

### 2026-04-23 — Architect Completion Checklist Refreshed To Include Phases 6-10

What changed:
- rewrote `ARCHITECT_FEEDBACK_COMPLETION_CHECKLIST.md` so it no longer stops at
  the old phase-1 through phase-5 read
- the refreshed checklist now records:
  - phases 6-9 as completed
  - phase 10 as structurally complete
  - the one remaining open item as the live Gemma control-session replay

Why it matters:
- future sessions no longer have to reconstruct the later post-architect work
  from changelog fragments
- the status record now distinguishes clearly between:
  - completed architecture/workflow changes
  - the one remaining environment-dependent live replay

### 2026-04-23 — Gemma Live Control-Session Replay Closed The Last Open Rollout Gap

What changed:
- brought the dedicated Gemma Ollama host back up on
  `OLLAMA_HOST=http://127.0.0.1:11435` against the user-local Gemma model
  store
- reran the declared live Gemma control session through the bounded runner:
  - `gemma-3.1-v002-control-session-v1`
- recorded the successful execution under:
  - `z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runner_sessions/executions/gemma_3_1_v002_control_session_v1_2026-04-23_135932Z/`
- completed both declared validation packs in that live replay:
  - `qwen-six-case-guard-pack-v1`
  - `grounding-generalization-pack-v1`

Why it matters:
- the one remaining operational caveat after the phases 6-10 rollout is now
  closed
- Gemma `3.1` is no longer only structurally ported; it has now completed the
  declared live bounded-runner replay on the phase-10 architecture baseline
- the architect-feedback rollout can now be described as complete for the
  implementation scope we chose, not merely "complete except for one Gemma
  replay"

Current consequence:
- the architect-feedback implementation program is now complete through phases
  1-10 for the scope we chose to implement
- `ARCHITECT_FEEDBACK_COMPLETION_CHECKLIST.md` should now be read as fully
  closed rather than "almost closed"
- Gemma `3.1` keeps `v002` as the tracked control baseline and `v003` as the
  paused overlay-backed follow-up candidate

### 2026-04-23 — Created The Live Architect Implementation Progress Report

What changed:
- created:
  - `z_reference_docs/ARCHITECT_IMPLEMENTATION_PROGRESS_REPORT.md`
- positioned it as the architect-facing implementation narrative that sits
  between:
  - the original review handoff
  - the narrow completion checklist
  - the full internal evidence trail in the changelog, worktree-state
    contract, and Prompt_Labs artifacts
- wired the new report into the doc-routing system through:
  - `REFERENCE_MASTER_INDEX.md`
  - `ARCHITECT_FEEDBACK_COMPLETION_CHECKLIST.md`

Why it matters:
- the project now has one stable live report that explains, in architect-facing
  language:
  - how the recommendations were implemented
  - what changed outside the original guidance
  - what experiments were run
  - what we expected versus what actually happened
  - why the work happened in worktrees instead of on `main`
  - what questions we want reviewed next
- future sessions no longer have to reconstruct that narrative from the raw
  handoff, checklist, and changelog separately

### 2026-04-23 — First Post-Architect Qwen `v010` Evidence-Gate Replay Kept `v010` Alive

What changed:
- ran the first post-architect Qwen-first live bounded session against the
  active control baseline using:
  - hypothesis:
    `qwen_1_2_v010_detect_overlay_hypothesis.yaml`
  - runner session:
    `qwen_1_2_v010_detect_overlay_session_v1.yaml`
- completed the raw bounded-runner live replay under:
  - `.../executions/qwen_1_2_v010_detect_overlay_session_v1_2026-04-23_150638Z/`
- then reproduced the same declared session once more by following the local
  `bda-prompt-eval-runner` skill workflow under:
  - `.../executions/qwen_1_2_v010_detect_overlay_session_v1_2026-04-23_151028Z/`
- both runs completed live and produced the same pack-level conclusion:
  - control `v009`
    - guard pack: `9 matches / 0 fn / 1 fp`
    - grounding pack: `6 matches / 0 fn / 1 fp`
  - candidate `v010`
    - guard pack: `9 matches / 0 fn / 0 fp`
    - grounding pack: `6 matches / 0 fn / 0 fp`

Why it matters:
- this was the first real test of the new Qwen-first direction after the
  architect rollout was completed
- it proved that the current `v010` overlay candidate still reproduces the
  known `destroyed_building4` recovery while holding the negative and tank
  controls
- it also proved that the raw runner path and the packaged local skill path
  produce materially matching evidence for the same declared session

Current consequence:
- decision outcome:
  - `keep_v010_as_active_followup_candidate`
- `v010` should remain the next Qwen follow-up direction
- this replay does **not** promote `v010` into tracked control state
- the next Qwen move should stay detect-only and target the still-open
  `destroyed_building3` and `destroyed_building6` failures from the `v010`
  base
- one minor workflow note remains:
  - the candidate-level `overlay_ids` field in `runner_session_summary.json`
    stayed empty even though the per-report metadata preserved the correct
    experiment overlay id

### 2026-04-23 — Staged The Next Qwen Detect-Only Follow-Up Packet From `v010`

What changed:
- prepared the next Qwen-only detect follow-up as a new overlay-backed
  experiment packet rooted in the still-viable `v010` candidate:
  - overlay:
    `experiments/overlays/qwen_1_2_v014_detect_weighted_building_selection.yaml`
  - hypothesis:
    `experiments/hypotheses/qwen_1_2_v014_detect_weighted_building_selection_hypothesis.yaml`
  - runner session:
    `experiments/runner_sessions/qwen_1_2_v014_detect_weighted_building_selection_session_v1.yaml`
- kept the declared validation packs unchanged from the successful `v010`
  evidence-gate replay:
  - `qwen-six-case-guard-pack-v1`
  - `grounding-generalization-pack-v1`
- kept `v010` as the active follow-up candidate in branch guidance rather than
  prematurely advancing branch state before a live `v014` run exists

Why it matters:
- the previous rejected `v011` through `v013` candidates already showed that
  "more prose", "more examples", and "top-of-prompt hierarchy by itself" were
  not enough on the active `1.2` line
- the local inspection packet instead pointed to a narrower next lever:
  - keep the intervention inside the detection user prompt
  - keep doctrine unchanged
  - keep assessment and summary unchanged
  - reduce competition from the later generic boxing rules that may still be
    pulling Qwen toward background-building selection and scene partitioning

Current consequence:
- the next Qwen run is now cleanly staged as `v014`
- `v014` should be read as a prepared detect-only follow-up from `v010`, not
  as a promoted winner or a new tracked control state
- the next actual live experiment should execute the staged `v014` runner
  session before we consider any Gemma follow-up

### 2026-04-23 — Qwen `v014` Produced A Useful Signal But Did Not Advance

What changed:
- executed the staged Qwen detect-only follow-up through the raw bounded
  runner:
  - `qwen_1_2_v014_detect_weighted_building_selection_session_v1`
- recorded the live run under:
  - `.../executions/qwen_1_2_v014_detect_weighted_building_selection_session_v1_2026-04-23_153816Z/`
- candidate packet used:
  - overlay:
    `experiments/overlays/qwen_1_2_v014_detect_weighted_building_selection.yaml`
  - hypothesis:
    `experiments/hypotheses/qwen_1_2_v014_detect_weighted_building_selection_hypothesis.yaml`
  - runner session:
    `experiments/runner_sessions/qwen_1_2_v014_detect_weighted_building_selection_session_v1.yaml`
- pack-level result:
  - control `v009`
    - guard pack: `9 matches / 0 fn / 1 fp`
    - grounding pack: `6 matches / 0 fn / 1 fp`
  - candidate `v014`
    - guard pack: `8 matches / 1 fn / 0 fp`
    - grounding pack: `6 matches / 0 fn / 0 fp`

Why it matters:
- `v014` did remove the extra `destroyed_building4` building false positive
  and it kept the office negative plus the tank controls clean
- but it did **not** improve `destroyed_building6`
- and it failed the declared six-case guard pack because
  `destroyed_building3` collapsed from two buildings to one
- that `destroyed_building3` result is important because it exposes a real
  evidence conflict:
  - qualitatively, the one-building read looks like the background-building
    suppression signal we were trying to elicit
  - under the current guard-pack reference, that same behavior is scored as a
    false negative because the declared reference still expects two building
    targets

Current consequence:
- `v014` is recorded as useful evidence, but it does **not** replace `v010` as
  the active Qwen follow-up candidate
- `v010` remains the active Qwen detect-only base
- the next Qwen clarification point is now the `destroyed_building3`
  reference-truth semantics rather than another immediate prompt rewrite from
  the same lever

### 2026-04-23 — Formalized The Adaptive 3-Attempt Qwen Follow-Up Protocol

What changed:
- created a new cycle-level protocol home for the active Qwen `1.2` prompt lab
  under:
  - `.../experiments/cycles/README.md`
  - `.../experiments/cycles/adaptive_three_attempt_qwen_cycle_protocol_v1.md`
  - `.../experiments/cycles/adaptive_three_attempt_qwen_cycle_brief_template.md`
- updated the Qwen `1.2` branch README, runner-session README, prompt-lab
  index, reference master index, methodology record, instructional guide, and
  architect-facing progress report so the new workflow is discoverable and
  explained consistently

Why it matters:
- the bounded runner already handled fixed declared sessions, but it did not by
  itself define how a three-attempt uninterrupted follow-up cycle should work
- the missing part was the between-attempt governance:
  - when research is allowed
  - when exact confirmation replays happen
  - when the cycle should pause instead of spending more attempt slots

Current consequence:
- post-rollout Qwen detect follow-up work now has an explicit operating
  contract instead of relying on session-by-session chat guidance
- significantly good results now replay immediately with no pre-replay
  research
- anomalous or conflicting results now allow light diagnosis before replay but
  still forbid candidate edits between the first run and replay
- replay-confirmed truth conflicts now pause the cycle for audit instead of
  encouraging more prompt churn against contradictory pack semantics

### 2026-04-23 — Added Whole-Program Deep-Dive And Extensibility Report Package

What changed:
- created the maintained whole-program report package:
  - `z_reference_docs/PROGRAM_DEEP_DIVE_AND_EXTENSIBILITY_REPORT.md`
  - `z_reference_docs/PROGRAM_EXPERIMENT_LEDGER.md`
  - `z_reference_docs/PROGRAM_FILE_AND_WORKTREE_INVENTORY.md`
- routed the package from:
  - `z_reference_docs/REFERENCE_MASTER_INDEX.md`
  - `z_reference_docs/Prompt_Labs/PROMPT_LABS_INDEX.md`
  - `z_reference_docs/ARCHITECT_IMPLEMENTATION_PROGRESS_REPORT.md`

Why it matters:
- the architect progress report explains how the recommendations were carried
  out, but it is intentionally not a full code/worktree/tooling inventory
- the new deep-dive package gives us a single maintained place to explain:
  - the full program architecture
  - every active worktree
  - conducted experiments and outcomes
  - current Codex assessment by experiment family
  - AGENTS, MCP, skills, subagents, plugins, validators, CI, heavy eval, and
    other extensibility mechanisms

Current consequence:
- future architecture reviews can start from the architect narrative and then
  drill into the deep-dive package for technical detail
- secret-bearing files remain role-inventoried only, not read or quoted
- `main` remains protected as the upstream mirror while real
  architect-guided implementation and experimentation remain in worktrees

### 2026-04-23 — Clarified Qwen `v009` Versus `v010` Interpretation

What changed:
- updated live guidance and state docs to stop treating `v010` as an
  unqualified improvement over `v009`
- updated:
  - root `AGENTS.md`
  - Qwen `1.2` worktree `AGENTS.md`
  - `z_reference_docs/WORKTREE_STATE.yaml`
  - Qwen `1.2` README
  - `PROMPT_LABS_INDEX.md`
  - `PROMPT_DEVELOPMENT_METHODOLOGY.md`
  - `PROGRAM_DEEP_DIVE_AND_EXTENSIBILITY_REPORT.md`
  - `PROGRAM_EXPERIMENT_LEDGER.md`
  - `ARCHITECT_IMPLEMENTATION_PROGRESS_REPORT.md`

Why it matters:
- `v009` remains the best confirmed/promoted Qwen stack and tracked control
  baseline
- `v010` remains a viable overlay-backed detect-only follow-up candidate, but
  it is not an overall replacement for `v009`
- the apparent `v010` advantage comes from the current post-architect replay
  manifest where `destroyed_building4` expects one building
- older branch-aware evidence explicitly recorded `destroyed_building4` as a
  two-building case and credited the `v009` lineage with restoring that recall

Current consequence:
- the later building-reference truth audit now supersedes this as the next
  gate
- the current next step is the `destroyed_building3` reference/manifest
  correction and replay, not another prompt attempt
- keep Gemma paused until Qwen resolves whether the next lesson is prompt
  weighting, reference truth, or a different detection approach

### 2026-04-23 — Revalidated Architect Recommendations After Rollout Completion

What changed:
- updated the existing live architect and program docs with a post-completion
  recommendation revalidation:
  - `ARCHITECT_FEEDBACK_COMPLETION_CHECKLIST.md`
  - `ARCHITECT_IMPLEMENTATION_PROGRESS_REPORT.md`
  - `PROGRAM_DEEP_DIVE_AND_EXTENSIBILITY_REPORT.md`
  - `PROGRAM_EXPERIMENT_LEDGER.md`

Why it matters:
- the original architect-feedback rollout remains complete through phases
  1-10
- the revalidation separates completed implementation obligations from
  follow-on quality work
- the Qwen `1.3` dirty pair is explicitly classified but not adopted
- the failed tiled-detector pilot remains a valid reason to defer another
  backend lane until the current reference-truth issue is resolved

Current consequence at that checkpoint:
- next recommended improvement was the Qwen building-reference truth audit:
  `destroyed_building4` first, then `destroyed_building3`
- `v009` remained the confirmed promoted Qwen baseline
- `v010` remained only an overlay-backed follow-up candidate pending that audit
- no AGENTS or `WORKTREE_STATE.yaml` change was needed at that time because
  the standing invariant already blocked treating `v010` as better than
  `v009` before the audit

### 2026-04-23 — Completed Qwen Building-Reference Truth Audit

What changed:
- created the Qwen `1.2` building-reference audit decision note:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/decisions/qwen_1_2_building_reference_truth_audit_2026-04-23.md`
- updated the Qwen `1.2` README, architect progress report, and program
  experiment ledger with the audit decision

Why it matters:
- the audit grounded the disputed building cases in the BDA doctrine:
  target-element PDA, building damage by percent of target-element area, and
  section/wing reporting when the target structure supports that distinction
- `destroyed_building4` is no longer treated as a valid reason to prefer the
  older two-box `v009` behavior; the current one-target reference better fits
  the visible damaged target body
- `destroyed_building3` is now the real executable truth problem because its
  second target is an intact background building, not a damaged BDA target
  element under the current guard-pack policy

Current consequence:
- audit outcome: `revise_destroyed_building3_reference`
- no executable reference JSON, manifest YAML, prompt overlay, doctrine file,
  or runtime code changed in this audit pass
- next step should be a separate approved `destroyed_building3`
  reference/manifest correction, followed by reruns of `v009`, `v010`, and
  `v014` against the corrected guard pack
- `v009` remains the confirmed promoted Qwen baseline
- `v010` remains an overlay-backed follow-up candidate, not a promotion
- at audit time, `v014` remained rejected as a candidate, but its one-target
  `destroyed_building3` behavior was useful evidence for the reference fix

### 2026-04-23 — Implemented Corrected `destroyed_building3` Truth And Replayed Qwen Candidates

What changed:
- added the corrected one-target `destroyed_building3` reference:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/validation/references/qwen_six_case_guard_pack_v1/destroyed_building3_corrected_2026-04-23.json`
- updated the executable guard-pack manifest so `destroyed_building3` now
  expects one `buildings` target and no longer scores the intact background
  high-rise as a target:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/validation/qwen_six_case_guard_pack_v1.yaml`
- preserved the old `qwen_candidate_a` JSON as historical run evidence rather
  than editing it in place
- replayed `v009` control, `v010`, and `v014` through the bounded-runner path
  after the correction
- exact-confirmation replayed `v014` because the first corrected-truth result
  was materially strong

Corrected-truth replay artifacts:
- `v009` control and `v010`:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runner_sessions/executions/qwen_1_2_v010_detect_overlay_session_v1_2026-04-23_211612Z/runner_session_summary.json`
- `v014` first corrected replay:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runner_sessions/executions/qwen_1_2_v014_detect_weighted_building_selection_session_v1_2026-04-23_211842Z/runner_session_summary.json`
- `v014` confirmation replay:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/runner_sessions/executions/qwen_1_2_v014_detect_weighted_building_selection_session_v1_2026-04-23_212114Z/runner_session_summary.json`

Result:
- corrected guard-pack replay:
  - `v009` control: `8 matches / 0 fn / 2 fp`
  - `v010`: `8 matches / 0 fn / 1 fp`
  - `v014`: `8 matches / 0 fn / 0 fp`
- grounding pack:
  - `v009` control: `6 matches / 0 fn / 1 fp`
  - `v010`: `6 matches / 0 fn / 0 fp`
  - `v014`: `6 matches / 0 fn / 0 fp`
- `v014` reproduced the same pass/fail conclusion in the exact confirmation
  replay

Current consequence:
- `v009` remains the confirmed promoted/tracked Qwen baseline
- `v010` remains useful historical overlay evidence but is no longer the
  strongest follow-up signal after corrected truth
- `v014` became the strongest unpromoted Qwen detect follow-up overlay under
  the declared corrected guard and grounding packs, but the later all-112
  human-report comparison now pauses direct promotion
- do not promote `v014` automatically; future prompt work should use the
  human-report comparison to preserve its false-positive suppression while
  recovering recall

### 2026-04-23 — Completed Broader Visual Validation For `v009`, `v010`, And `v014`

What changed:
- created a broader visual-validation decision note and contact-sheet review
  package for the replay-comparable Qwen versions:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/visual_validation/qwen_1_2_v014_broader_visual_validation_2026-04-23/README.md`
- reviewed all cases in:
  - `qwen-six-case-guard-pack-v1`
  - `grounding-generalization-pack-v1`
- compared `v009`, `v010`, and `v014` against the corrected replay artifacts
  before authoring any new Qwen prompt attempt

Visual outcome:
- `v009` still visibly over-selects adjacent/background buildings in
  `destroyed_building3` and `destroyed_building4`
- `v010` fixes `destroyed_building4` but still over-selects the
  `destroyed_building3` background high-rise
- `v014` suppresses both of those false-positive patterns while holding
  `destroyed_building6`, the office negative case, tank controls, and the
  grounding-pack cases under the current reference policy

Current consequence:
- outcome: `v014_visual_validation_passed_for_declared_packs`
- the later promotion-readiness review completed and reached
  `ready_for_formal_promotion_package`
- the later all-112 human-report comparison supersedes the direct
  promotion-package path before any fold-in
- `v009` remains the confirmed promoted/tracked Qwen baseline until a formal
  promotion report approves an overlay fold-in

### 2026-04-23 — Completed Qwen `v014` Promotion-Readiness Review

What changed:
- deterministically re-scored existing exact-confirmation `v014` predictions
  in `promotion` eval mode
- created the review decision note:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/decisions/qwen_1_2_v014_promotion_readiness_review_2026-04-23.md`
- wrote re-score outputs under:
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/promotion_reviews/qwen_1_2_v014_promotion_readiness_2026-04-23/`

Promotion-mode result:
- `qwen-six-case-guard-pack-v1`: `8 matches / 0 fn / 0 fp`
- `grounding-generalization-pack-v1`: `6 matches / 0 fn / 0 fp`
- `office_negative` remained a clean negative-scene abstention
- LLMaaJ was skipped because no key was configured, which is acceptable
  because LLMaaJ is advisory-only

Current consequence:
- outcome: `ready_for_formal_promotion_package`
- `v014` was ready for the formal phase-4 promotion package under the
  declared-pack process; this adoption path is now paused by the later
  human-report-informed comparison
- `v014` is still not promoted and is not folded into tracked runtime/config
  truth
- the next step is no longer direct promotion packaging; use the all-112
  human-report comparison to design or reject a future `v015` lever first

### 2026-04-24 — Added Graphify Wiki, Benchmarks, And Verified Query Notes

What changed:
- generated a project-brain wiki from the existing `.graphify_project_brain`
  graph:
  - `.graphify_project_brain/corpus/graphify-out/wiki/index.md`
- generated fixed Capstone benchmark reports for both Graphify profiles:
  - `.graphify_fleet/corpus/graphify-out/capstone_benchmark_report.md`
  - `.graphify_project_brain/corpus/graphify-out/capstone_benchmark_report.md`
- added a local-only verified query-note lane:
  - `.graphify_project_brain/corpus/graphify-out/memory/verified/`
- updated `PROJECT_BRAIN.md`, `REFERENCE_MASTER_INDEX.md`, and the global
  Graphify skill guidance to explain the new workflow

Why it matters:
- Graphify is now not just a graph JSON and MCP endpoint; it has a browseable
  wiki, usefulness measurement, and a safe path for source-verified graph
  answers to become reusable local memory
- the benchmark makes the tradeoff visible:
  - narrow implementation questions such as `DetectorBackend` are high-signal
  - broad project-state questions still fan out across too much context and
    should start from curated docs or verified notes

Current consequence:
- Graphify remains a navigation and recall aid, not source truth
- no runtime code, BDA prompts, overlays, references, promotion artifacts, or
  tracked control truth changed
- future meaningful live-doc updates should refresh the graph and then rerun
  `.graphify_project_brain/export_usefulness_artifacts.py`

### 2026-04-24 — Added Graphify Extensions Machinery And Evidence Query Surfaces

What changed:
- extended `.graphify_project_brain/capstone_graphify.py` with:
  - `doctor --strict-stale`
  - `evidence-index`
  - `analytics`
  - `estimate-extraction`
  - benchmark pack selection through `--pack`
- added a local-only SQLite evidence index:
  - `.capstone_evidence/evidence.sqlite`
  - `.capstone_evidence/evidence_index_report.md`
  - `.capstone_evidence/canned_queries.sql`
- added a local-only DuckDB analytics mirror:
  - `.capstone_evidence/analytics.duckdb`
  - `.capstone_evidence/duckdb_analytics_report.md`
- added read-only MCP wrappers:
  - `capstone-evidence-sqlite`
  - `capstone-evidence-duckdb`
- added prompt/version visual diff tooling:
  - `z_reference_docs/local_tools/capstone_visual_diff.py`
  - sample output under `.capstone_visual_diffs/qwen-v010-overlay__vs__qwen-v014-overlay/`
- added the global `source-verified-mermaid` skill for targeted, source-checked
  Mermaid diagrams
- added the broad safe-corpus LLM extraction estimator and subagent output
  contract, but did not launch extraction

Current estimator result:
- eligible files: `2240`
- approximate tokens: `1,339,756`
- chunks: `2318`
- expected candidate edges: `11590`
- expected candidate notes: `2307`
- review burden: `very_high`
- gate recommendation: `stop_before_full_extraction`

Current consequence:
- the infrastructure for the next Graphify/evidence phase exists
- broad LLM extraction remains blocked pending a later explicit approval and
  review-burden decision

### 2026-04-24 - Ran Stage-Only Architect/Qwen Extraction Pilot

What changed:

- added `z_reference_docs/local_tools/run_graphify_extraction_pilot.py`
- added `.graphify_project_brain/capstone_graphify.py extraction-pilot`
- created local-only pilot workspace:
  `.graphify_project_brain/archive/extraction_pilots/failed_or_incomplete/pilot_2026-04-24_172000Z/`
- initialized source manifests and agent prompts for:
  - `architect_docs`
  - `qwen_evidence`
- ran subagent-backed stage-only extraction:
  - architect docs: `1` batch
  - Qwen evidence: `8` batches
- reviewed staged outputs with the local orchestrator validator

Result:

- outputs reviewed: `9`
- total staged items: `292`
- source-supported items: `292`
- unsupported items: `0`
- duplicate items: `0`
- invalid outputs: `1`
- final recommendation:
  `revise_extraction_contract_before_full_run`

Interpretation:

- the stage-only workflow is viable
- bounded Qwen batching is viable
- subagents can produce useful source-linked candidate memory without writing
  trusted memory
- the extraction contract needs tightening because one Qwen batch returned
  `confidence_labels` as a map instead of the required list
- no staged output was ingested into verified memory or semantic seeds

Next recommended move:

- tighten the extraction contract/schema prompt around scalar/list fields
- rerun or revalidate the narrow bad contract case
- then decide whether to run another domain pilot or approve full safe-corpus
  extraction
- no BDA runtime code, prompts, doctrine, overlays, references, manifests, or
  promotion artifacts changed

### 2026-04-24 - Passed Graphify Extraction Contract-Fix Confirmation

What changed:

- ran a one-batch Qwen evidence confirmation pilot:
  `.graphify_project_brain/archive/extraction_pilots/failed_or_incomplete/pilot_2026-04-24_174500Z/`
- confirmed the original `confidence_labels` map/object issue was fixed
- found the same schema-shape issue on `do_not_ingest`
- tightened the extraction contract and generated pilot prompt so all
  collection fields must be JSON arrays, even when empty
- ran a second one-batch Qwen evidence confirmation pilot:
  `.graphify_project_brain/extraction_pilots/pilot_2026-04-24_175500Z/`

Final confirmation result:

- outputs reviewed: `1`
- total staged items: `33`
- source-supported items: `33`
- unsupported items: `0`
- duplicate items: `0`
- invalid outputs: `0`
- final recommendation:
  `ready_for_full_safe_corpus_extraction`

Interpretation:

- the tested contract-shape blocker is cleared
- extraction remains stage-only until a later explicit approval
- full safe-corpus extraction is now blocked by scale/review-burden approval,
  not by the basic JSON contract issue
- no staged output was ingested into verified memory or semantic seeds

### 2026-04-24 - Passed Runtime/Eval Architecture Extraction Pilot

What changed:

- restarted the `runtime_eval_architecture` stage-only pilot from a fresh
  workspace after the earlier disconnected workspace produced no staged output
- used six bounded batches under:
  `.graphify_project_brain/extraction_pilots/pilot_pilot_2026-04-24_183942Z/`
- ran workers in two small waves so each worker wrote exactly one staged-output
  JSON file
- reviewed all staged outputs with the local orchestrator validator

Result:

- outputs reviewed: `6`
- total staged items: `116`
- source-supported items: `116`
- unsupported items: `0`
- duplicate items: `0`
- invalid outputs: `0`
- final recommendation:
  `ready_for_full_safe_corpus_extraction`

Interpretation:

- the tightened extraction contract held for a code/config/test/eval
  architecture shard, not just narrative evidence
- subagent-backed extraction remains viable when staged in bounded waves
- the pilot does not ingest trusted memory or semantic seeds
- the natural next gate is full safe-corpus extraction planning with explicit
  review-burden controls, not automatic full extraction

### 2026-04-24 - Passed Full Safe-Corpus Stage-Only Extraction Gate

What changed:

- ran the approved full safe-corpus Graphify extraction as a stage-only,
  shard-checkpointed workflow under:
  `.graphify_project_brain/extraction_pilots/pilot_full_safe_corpus_2026-04-24_191412Z/`
- covered all configured shards:
  `architect_docs`, `graphify_tooling`, `governance_worktrees`,
  `runtime_eval_architecture`, `qwen_evidence`, `gemma_evidence`, and
  `general_project_context`
- hardened review reporting with orchestrator-stamped metadata, confidence
  mix, source-reference counts, duplicate-identifier counts,
  `do_not_ingest` counts, and metadata mismatch warnings
- completed the final `general_project_context` shard one worker at a time
  after VS Code disconnected repeatedly

Result:

- outputs reviewed: `44`
- total staged items: `815`
- source-supported items: `815`
- unsupported items: `0`
- duplicate items: `0`
- duplicate identifier items: `4`
- invalid outputs: `0`
- source references checked: `1996`
- do-not-ingest items: `99`
- metadata warnings: `42`
- final recommendation:
  `ready_for_full_safe_corpus_extraction`

Recovery and environment diagnosis:

- the staged extraction workspace was intact after each restart
- the interrupted worker for `general_project_context_batch_018` disappeared
  from the agent registry and had not written an output file, so it was safe to
  rerun from that batch
- memory and disk were healthy during diagnosis
- VS Code logs repeatedly showed stale workspace lock recovery and
  `openai.chatgpt` `PendingMigrationError` activation errors, so the likely
  failure mode was VS Code/Codex extension-host instability under generated
  artifact and background-agent load rather than repository corruption or
  extraction data failure
- added a local-only ignored `.vscode/settings.json` that excludes generated
  Graphify, evidence, visual-diff, and `graphify-out` artifacts from VS Code
  watcher/search load

Interpretation:

- full safe-corpus extraction is now proven as a staged candidate-generation
  workflow
- nothing was ingested into trusted verified memory or semantic seeds
- the next meaningful gate is not more extraction; it is a reviewed ingestion
  plan that samples, dedupes, source-checks, and selectively promotes only
  high-signal staged material
- `INFERRED`, `AMBIGUOUS`, and `REJECT` items remain supporting staged evidence
  only unless a later review explicitly reclassifies them

### 2026-04-24 - Completed Focused Project-Brain Ingestion V1

What changed:

- created the first reviewed ingestion package from the completed full
  safe-corpus staged extraction:
  `.graphify_project_brain/ingestion_reviews/focused_ingestion_v1_2026-04-24/`
- accepted only a bounded, source-verified subset from focused shards:
  `qwen_evidence`, `architect_docs`, `runtime_eval_architecture`, and
  `governance_worktrees`
- updated local Graphify memory inputs:
  `.graphify_project_brain/verified_query_seed_notes.json` and
  `.graphify_project_brain/agent_semantic_seed.json`

Result:

- verified query notes accepted: `7`
- semantic nodes accepted: `8`
- semantic edges accepted: `10`
- semantic hyperedges accepted: `1`
- accepted seed edge confidence: all new semantic edges are `EXTRACTED`
- source checks: all accepted note and seed source paths resolve

Interpretation:

- the project brain now has trusted local memory for the v014 hash caveat,
  adaptive-cycle truth-freeze rule, bounded-runner no-self-promotion boundary,
  office-negative raw JSON review caveat, runtime/eval/promotion evidence flow,
  worktree-state contract, and Graphify stage-only ingestion boundary
- the remaining staged queue is still untrusted candidate memory
- no runtime code, prompts, overlays, references, manifests, doctrine, or
  promotion artifacts changed

### 2026-04-25 - Hardened Graphify Recall Retrieval Before More BDA Work

What changed:

- added `.graphify_project_brain/capstone_graphify.py recall` as the preferred
  trusted retrieval doorway for Capstone project-state questions
- added `.graphify_project_brain/capstone_graphify.py recall-benchmark` to
  catch retrieval regressions against expected verified notes and accepted
  semantic seed nodes
- updated project-brain routing docs so future BDA work starts from source-
  verified recall before broad raw graph search

Result:

- recall now prefers verified query notes, then accepted semantic seeds, then
  graph fallback
- retrieval aliases cover the current high-value BDA decision questions:
  `v014` hash caveat, `office_negative` raw JSON review, adaptive-cycle truth
  freeze, worktree-state contract, and `DetectorBackend`
- the recall benchmark passed all fixed checks

Interpretation:

- this is retrieval hardening only; no BDA runtime code, prompts, overlays,
  references, manifests, promotion artifacts, or trusted experiment conclusions
  changed
- raw `graphify query` remains useful for exploration, but trusted recall is
  now the safer first route before resuming Qwen/Gemma BDA decisions

### 2026-04-25 - Installed FiftyOne MCP And Added Capstone Visual-Review Rules

What changed:

- installed the global `fiftyone-mcp-server` package through `uv tool`
- added the `fiftyone` MCP entry to `/home/williambenitez1/.codex/config.toml`
  using `/home/williambenitez1/.local/bin/fiftyone-mcp`
- updated global and project MCP guidance to define FiftyOne as an explicit
  visual dataset/case review tool for BDA imagery, validation-pack samples,
  predicted/reference bounding boxes, failure slices, and curated local
  FiftyOne datasets
- recorded the SequentialThinking follow-up: troubleshoot the MCP later and
  only re-enable it for Plan Mode structured prompt/eval planning, critique
  loops, failure analysis, and decision trees after the odd behavior is
  diagnosed and fixed

Interpretation:

- FiftyOne is now available after a Codex/VS Code restart, but it should not be
  treated as deterministic scoring, reference truth, promotion authority, or a
  replacement for `bda_eval`, runner summaries, manifests, reference JSON,
  doctrine docs, or promotion reports
- broad dataset imports, label mutation, plugin/operator installation, dataset
  export, or large App sessions require explicit user approval for the dataset
  and output path

### 2026-04-25 - Re-enabled SequentialThinking MCP With Plan-Mode Scope

What changed:

- verified the configured SequentialThinking MCP entry still points to
  `/home/williambenitez1/.local/bin/npx` with
  `@modelcontextprotocol/server-sequential-thinking`
- confirmed the MCP tools are exposed in the restarted Codex session
- ran a minimal smoke test through `mcp__sequential_thinking__.sequentialthinking`
  and confirmed the server returned normally
- updated global and project guidance from "deactivated" to "available for
  Plan Mode by default"

Current rule:

- use SequentialThinking by default only in Plan Mode
- intended uses: structured prompt/eval planning, critique loops, failure
  analysis, and decision trees
- in Default mode, use normal reasoning unless the user explicitly asks for
  SequentialThinking or the task is an MCP troubleshooting/smoke test
- do not treat SequentialThinking as a replacement for source inspection,
  tests, runner artifacts, Graphify recall, or documented evidence

### 2026-04-27 - Expanded Graphify Trusted Memory With Doctrine And Prompting Research

What changed:

- ran a new stage-only `prompting_vlm_research` Graphify extraction pilot:
  `.graphify_project_brain/extraction_pilots/pilot_prompting_vlm_research_2026-04-27_1438Z/`
- used 8 bounded extraction workers in small waves and reviewed the staged
  outputs with `capstone_graphify.py extraction-pilot review`
- combined the clean Prompting pilot with the earlier clean
  `bda_doctrine_targeting` pilot in one curated ingestion package:
  `.graphify_project_brain/ingestion_reviews/expanded_doctrine_prompting_v1_5_2026-04-27/`
- updated local Graphify memory inputs:
  `.graphify_project_brain/verified_query_seed_notes.json` and
  `.graphify_project_brain/agent_semantic_seed.json`

Result:

- Prompting pilot passed: `8` outputs reviewed, `201` staged items, `201`
  source-supported items, `0` unsupported items, and `0` invalid outputs
- trusted memory accepted: `17` verified query notes, `17` semantic nodes,
  `25` semantic edges, and `3` semantic hyperedges
- accepted themes include BDA target-element scope, image-only output as
  initial evidence, building/critical-target-element boundaries,
  collateral/CDA boundaries, functional-damage recuperation limits, Qwen
  normalized grounding, anti-neighbor bbox prompting, micro-examples, and VLM
  visual-prompt fragility

Interpretation:

- this is Graphify/project-brain memory only; no BDA runtime code, prompts,
  overlays, references, manifests, doctrine, or promotion artifacts changed
- Prompting references are now easier to recall, but they remain supporting
  context and cannot override doctrine decisions, validation manifests, runner
  summaries, promotion reports, or runtime source code
- all `REJECT`, unsupported, and ambiguous staged candidates stayed out of
  trusted memory

### 2026-04-27 - Added Graphify Ingestion-Readiness Scorer V1

What changed:

- added `z_reference_docs/local_tools/score_graphify_ingestion_readiness.py`
  as a deterministic local-only scorer for reviewed stage-only extraction
  output
- exposed the scorer through:
  `.graphify_project_brain/capstone_graphify.py ingestion-readiness --pilot-dir <pilot>`
- the scorer writes local generated queues under `<pilot>/ingestion_readiness/`:
  `readiness_report.md`, `readiness_summary.json`,
  `accept_candidates.json`, `defer_candidates.json`, and
  `reject_candidates.json`
- documented the trust boundary in `z_reference_docs/PROJECT_BRAIN.md`

Validation result:

- BDA doctrine pilot:
  - readiness label: `ready_for_curated_ingestion`
  - accept/defer/reject: `111` / `9` / `15`
  - unsupported items: `0`
  - invalid outputs: `0`
  - inferred accept candidates: `8`
  - duplicate/defer handling confirmed
- Prompting/VLM research pilot:
  - readiness label: `ready_for_curated_ingestion`
  - accept/defer/reject: `143` / `21` / `37`
  - unsupported items: `0`
  - invalid outputs: `0`
  - inferred accept candidates: `9`
  - duplicate/defer handling confirmed

Interpretation:

- the scorer is a review-burden reducer, not an ingestion authority
- accepted candidates are only a shortlist for a future curated package; they
  still need source-checking, dedupe review, and explicit approval before any
  trusted verified note or semantic seed update
- no BDA runtime code, prompts, overlays, references, manifests, doctrine, or
  promotion artifacts changed

### 2026-04-27 - Added Curated Graphify Trusted Memory V2 From Readiness Queues

What changed:

- used the new `ingestion-readiness` outputs as a shortlist for a second
  curated doctrine plus Prompting trusted-memory package
- created the local review package:
  `.graphify_project_brain/ingestion_reviews/curated_doctrine_prompting_v2_2026-04-27/`
- updated local Graphify memory inputs:
  `.graphify_project_brain/verified_query_seed_notes.json` and
  `.graphify_project_brain/agent_semantic_seed.json`

Result:

- trusted memory accepted: `12` verified query notes, `12` semantic nodes,
  `17` semantic edges, and `2` semantic hyperedges
- accepted BDA themes: Phase 1 BDA nonfinality, BDA as more than
  destroyed-system counting, deception/reconstitution/time-window concerns,
  working-group style review loops, target-validation versus
  engagement-authority separation, and measurable/observable effect boundaries
- accepted Prompting themes: full prompt-attempt logging, structured JSON
  tradeoffs, schema-guided inputs, prompt chaining for staged review,
  single-visual-prompt replay discipline, and Qwen detail controls as runtime
  levers rather than prompt-only fixes

Interpretation:

- this is still Graphify/project-brain memory only; no BDA runtime code,
  prompts, overlays, references, manifests, doctrine, or promotion artifacts
  changed
- readiness queues reduced review burden, but did not self-approve ingestion;
  each V2 item was selected as durable source-backed memory
- broad Gemma capability details, OWLv2/Llama 4 adoption implications, and
  duplicate Qwen normalized-coordinate or anti-neighbor bbox lessons remain
  deferred review context

### 2026-04-27 - Added Trusted Project-Brain Source Verification

What changed:

- added `z_reference_docs/local_tools/verify_graphify_trusted_memory.py`
  as a local-only source verifier for trusted Graphify memory
- exposed it through:
  `.graphify_project_brain/capstone_graphify.py verify-memory`
- ran the first report-only audit under:
  `.graphify_project_brain/archive/verification_reviews/superseded/trusted_memory_source_audit_2026-04-27_160409Z/`

Result:

- checked items: `288`
- trusted notes: `58`
- semantic nodes: `72`
- semantic edges: `88`
- semantic hyperedges: `12`
- generated verified-note Markdown files expected: `58`
- verified: `186`
- verified with limits: `100`
- source missing: `2`
- duplicate trusted note slugs, node IDs, or edge IDs: `0`
- bad trusted `REJECT` or `AMBIGUOUS` confidence entries: `0`
- required verification lanes were present: Prompt_Labs evidence,
  runtime/eval code, governance, BDA doctrine, Prompting docs, Graphify local
  memory, and SQLite/DuckDB evidence DBs

Interpretation:

- the trusted memory is broadly usable as navigation and recall, including BDA
  doctrine and Prompting research support, but source artifacts remain
  authoritative
- the two stale semantic-node source links were later corrected to active Qwen
  `1.2` worktree architecture paths and strict verification now passes with
  `0` source-missing items
- no trusted memory was auto-edited during verification

### 2026-04-27 - Added Project-Brain Memory Correction And Regression Gate

What changed:

- corrected the two trusted semantic seed source links that previously pointed
  at paths not present in `main`
- added strict trusted-memory verification through:
  `.graphify_project_brain/capstone_graphify.py verify-memory --strict`
- added `doctor --strict-memory` so Graphify health checks can enforce trusted
  memory integrity separately from graph staleness
- added `.graphify_project_brain/capstone_graphify_recall_expectations.json`
  with broader recall regression coverage across Qwen, Gemma, BDA doctrine,
  Prompting guidance, worktree governance, and runtime/eval architecture

Result:

- `verify-memory --json` now reports `188` verified items, `100`
  verified-with-limits items, and `0` source-missing items
- `verify-memory --strict` exits cleanly
- expanded `recall-benchmark` passes `20/20`
- the corrected semantic nodes remain scoped as active worktree architecture
  memory, not `main` runtime truth

Interpretation:

- the project brain is now better protected against stale trusted-memory source
  links and retrieval regressions
- future memory updates can use `doctor --strict-stale --strict-memory` as the
  stronger closeout gate after meaningful Graphify/project-brain changes

### 2026-04-27 - Created Qwen v014 Formal Promotion Package Step 1

What changed:

- created the deferred machine-readable promotion report:
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/promotion_reports/v014_detect_weighted_building_selection_pending_promotion.yaml`
- created the paired human-facing pending promotion package note:
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/decisions/qwen_1_2_v014_formal_promotion_package_2026-04-27.md`
- routed the new package through the Qwen `1.2` README, Prompt Labs index,
  Reference Master Index, and Project Brain entrypoint

Decision state:

- package outcome: `formal_package_ready_pending_user_approved_fold_in`
- promotion report decision: `deferred`
- `promotion_commit`: `pending_user_approved_fold_in`
- no fresh VLM run was performed
- no runtime code, base `config.yaml`, prompt overlay, reference, manifest, or
  model-line truth changed
- `v009` remains the promoted Qwen baseline

Recommended next step:

- if the user approves Step 2 later, fold the `v014` detect prompt into
  `src/bda_svc/pipeline/overlays/model_lines/qwen3-vl-8b-instruct.yaml`,
  validate that no experiment overlay is needed for the behavior, then update
  the promotion report/winner shelf only after validation

### 2026-04-27 - Indexed New Human Report Dataset For Audit

What changed:

- created a Graphify-visible intake scaffold for the new human-written
  report/image dataset:
  `z_reference_docs/human_report_dataset_audit/HUMAN_REPORT_DATASET_INTAKE_AND_AUDIT.md`
- added deterministic companion artifacts:
  - `human_report_dataset_intake_summary.json`
  - `human_report_dataset_media_index.json`
  - `human_report_dataset_audit_ledger.csv`
- added the local generator:
  `z_reference_docs/local_tools/human_report_dataset_audit.py`
- added the first-pass visual-audit closeout:
  `z_reference_docs/local_tools/human_report_visual_audit_closeout.py`
- created the visual-audit report:
  `z_reference_docs/human_report_dataset_audit/HUMAN_REPORT_DATASET_VISUAL_AUDIT.md`
- created separated proposed-correction queues under:
  `z_reference_docs/human_report_dataset_audit/proposed_corrections/`
- updated the Reference Master Index, Project Brain entrypoint, trusted recall
  note lane, semantic seeds, and recall expectations

Current intake and first-pass visual-audit result:

- active images indexed: `112`
- active reports indexed: `112`
- held-out images preserved under
  `z_reference_docs/Data_set_Storage/human_reports/no_reports/images`:
  `86`
- removed reports preserved under
  `z_reference_docs/Data_set_Storage/human_reports/no_reports/discarded_reports`:
  `87`
- active first-pass visual-audit counts:
  - `99` accurate
  - `13` accepted after user review
  - current usable report count: `112`
- active deterministic bbox/schema issue reports: `6`, all covered by
  user-accepted cases rather than active `bbox_off` status items
- dedicated Graphify extraction shard: `human_report_examples`
- approved-example semantic index:
  `z_reference_docs/human_report_dataset_audit/APPROVED_HUMAN_REPORT_EXAMPLES.md`
- semantic companion files:
  - `z_reference_docs/human_report_dataset_audit/approved_human_report_examples_index.json`
  - `z_reference_docs/human_report_dataset_audit/approved_human_report_examples_graph_context.jsonl`
- approved-example semantic counts:
  - `217` report objects across the `112` approved image/report pairs
  - `159` military-equipment objects, `56` building objects, and
    `2` object-not-found entries
  - damage labels after doctrine grounding include `119` no-damage,
    `48` destroyed, `26` damaged, `16` severe-damage, `5` moderate-damage,
    `2` not-applicable, and `1` light-damage entries
- no active human-review cases remain
- `20`, `61`, `84`, and `101` were reviewed and accepted by the user on
  `2026-04-27`; `61.txt` was adjusted so the distant far-left truck is
  `probable` instead of `confirmed`
- `21`, `144`, `146`, `160`, and `164` were doctrine-normalized from
  non-doctrinal `damage: unknown` to `no damage` with `possible` confidence and
  explicit distant/too-small-to-assess logic
- `155` and `166` were doctrine-normalized to confirmed object-not-found
  abstentions under the user rule that non-military vehicles are out of scope
- move manifest:
  `z_reference_docs/Data_set_Storage/human_reports/no_reports/move_manifest_2026-04-27.json`

Boundary:

- the held-out material has been removed from the active image/report folders
  but preserved under `no_reports/` for reversibility
- raw image pixels remain excluded from Graphify corpus mirroring
- the active `accurate` and `accepted_after_user_review` buckets are now the
  `112`-report prompt-example candidate pool
- the `human_report_examples` shard and deterministic approved-example index
  are the first retrieval route for this dataset
- do not run agent/subagent extraction for these examples by default; use a
  stage-only pilot only if deterministic retrieval is not deep enough for
  prompt work
- keep held-out material out of prompt work unless it is explicitly repaired
  later

### 2026-04-28 - Completed Human-Report-Informed Qwen v009 vs v014 Comparison

What changed:

- paused the `v014` promotion path as
  `promotion_paused_superseded_by_human_report_process`
- preserved the corrected-pack `v014` win as historical evidence, not a
  rejected result
- kept `v009` as the promoted/tracked Qwen control baseline
- created the derived local challenge lane:
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/human_report_challenge_v1/`
- added the process decision note:
  `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/experiments/decisions/qwen_1_2_human_report_informed_v009_v014_comparison_plan_2026-04-28.md`
- doctrine-grounded the approved human-report labels before challenge
  generation:
  - non-doctrinal damage labels after correction: `0`
  - non-doctrinal confidence labels after correction: `0`
  - active challenge examples: `112`
  - active challenge objects: `217`
- generated balanced challenge manifests:
  - `human_building_damage_slice_v1`
  - `human_military_equipment_damage_slice_v1`
  - `human_dense_multi_target_slice_v1`
  - `human_confidence_distance_slice_v1`
  - `human_out_of_scope_negative_slice_v1`
- ran fresh current-state all-112 Qwen comparison:
  - `v009`: `161` matches, `56` false negatives, `54` false positives,
    mean IoU `0.675`
  - `v014`: `148` matches, `69` false negatives, `24` false positives,
    mean IoU `0.6851`
- ran slice scoring from the same prediction outputs:
  - building slice: `v014` changed `-4` matches, `+4` false negatives,
    `-4` false positives
  - military equipment slice: `v014` changed `-7` matches, `+7` false
    negatives, `-16` false positives
  - dense multi-target slice: `v014` changed `-8` matches, `+8` false
    negatives, `-20` false positives
  - confidence/distance slice: `v014` changed `-7` matches, `+7` false
    negatives, `-20` false positives
  - out-of-scope negative slice: unchanged

Boundary:

- that hold is now satisfied by the later worktree-only `v015` strategy package
  and `v015a` through `v015e` prompt-candidate sequence
- the human-report challenge is prompt-learning evidence, not automatic
  promotion truth
- original images remain in place; challenge references are derived
  doctrine-compatible scoring views
- first v015 lesson: preserve `v014`-style false-positive suppression while
  restoring `v009`-style multi-target recall

### 2026-04-27 - Added Portable Codex Capability Transfer Dossier

What changed:

- created `z_reference_docs/CODEX_CAPABILITY_TRANSFER_DOSSIER.md` as a durable
  Markdown playbook for another Codex instance working on a different project
- documented transferable practices across MCP routing, shell/tool selection,
  skills, plugins, subagents, AGENTS layers, Graphify, evidence workflows,
  planning habits, documentation closeout, and memory citations
- used Capstone as an illustrative example only, not as a template that must be
  copied verbatim
- updated the Reference Master Index and program deep-dive routing so the
  dossier is discoverable

Interpretation:

- the dossier is meant to help another Codex evaluate whether to adopt these
  techniques in its own project environment
- it does not change BDA runtime code, prompts, overlays, manifests,
  references, promotion artifacts, or experiment truth

### 2026-04-27 - Adopted Incoming Codex Dossier Ideas Into This Environment

What changed:

- reviewed `z_reference_docs/The_Incomming_CODEX_CAPABILITIES_DOSSIER.md`
  against the current Capstone/global Codex setup
- removed the accidental generic Graphify CLI insertion from root `AGENTS.md`
  because it pointed future agents at nonexistent root `graphify-out/`
  artifacts instead of Capstone's `.graphify_fleet` and
  `.graphify_project_brain` profiles
- enabled Codex hooks with `codex_hooks = true` in
  `/home/williambenitez1/.codex/config.toml`
- added a global guarded `UserPromptSubmit` hook:
  `/home/williambenitez1/.codex/hooks/user_prompt_submit_graphify_reminder.py`
- added `/home/williambenitez1/.codex/hooks.json` to route
  `UserPromptSubmit` to that read-only hook script
- updated the global AGENTS layer, global MCP usage guide, Project Brain
  entrypoint, Reference Master Index, and Codex capability transfer dossier

Adoption decision:

- adopted the incoming dossier's hook idea, but implemented it as a guarded
  global Codex hook that only emits context when a local Graphify graph/profile
  exists or the cwd belongs to Capstone/main worktrees
- kept Capstone's existing two-graph architecture; `project-brain-lite` and
  `architecture-plus` remain deferred until benchmark evidence shows they are
  needed
- kept stale/doctor checks and explicit refreshes instead of automatic broad
  graph rebuilds
- kept subagent extraction staged and orchestrator-reviewed instead of adopting
  broad unattended swarms

Boundary:

- no BDA runtime code, prompts, overlays, manifests, references, promotion
  artifacts, or experiment truth changed
- hook activation may require restarting/forking the Codex or VS Code session
  because hook/config changes may not hot-load

Self-test follow-up:

- ran a focused self-test over the global guarded Graphify prompt-submit hook,
  hook JSON, Codex config, Capstone cwd, Capstone worktree cwd, generic
  graphified cwd, non-Graphify cwd, empty stdin, malformed JSON, and missing
  cwd input
- tightened
  `/home/williambenitez1/.codex/hooks/user_prompt_submit_graphify_reminder.py`
  so missing, empty, or malformed hook input fails quiet instead of falling
  back to the current working directory

### 2026-04-27 - Added Trust-Labeled Deep Graphify Retrieval

What changed:

- extended `.graphify_project_brain/capstone_graphify.py recall` with an
  optional `--deep` mode
- added `.graphify_project_brain/capstone_graphify.py search-all` as a broad
  discovery command over verified notes, accepted semantic seeds, generated
  wiki articles, raw graph nodes, and derived evidence-index records
- tuned deep-search ranking so trusted notes and accepted semantic seeds remain
  first for project-state questions while weak evidence-index lookup hits do
  not outrank stronger graph matches
- updated `PROJECT_BRAIN.md`, `REFERENCE_MASTER_INDEX.md`, root/global
  `AGENTS.md`, the global MCP usage guide, and the portable Codex capability
  dossier to document the trust boundary

Interpretation:

- normal `recall` remains the first route for source-verified project memory
  and BDA decision questions
- `recall --deep` and `search-all` are exploratory discovery aids; they label
  every result with kind, confidence, limits, sources, and verification guidance
  so generated wiki, raw graph, and evidence-index hits do not blur into
  trusted memory

Boundary:

- no BDA runtime code, prompts, overlays, manifests, references, promotion
  artifacts, or experiment truth changed

### 2026-04-27 - Clarified Portable Memory Citation Policy

What changed:

- updated `z_reference_docs/CODEX_CAPABILITY_TRANSFER_DOSSIER.md` and
  `z_reference_docs/PROJECT_BRAIN.md` with the memory-citation policy chosen
  during the cross-Codex capability-transfer discussion
- recorded that citable "memory" should mean certified memory artifacts:
  source-verified query notes, accepted semantic seed files, or their project
  equivalents
- recorded that ordinary live docs should be cited as source evidence in the
  answer, not placed into the literal memory-citation block
- recorded that raw graph hits, generated wiki articles, and derived
  evidence-index records are discovery aids unless they are later promoted into
  verified memory
- recorded that the literal memory-citation block appears only when verified
  memory materially shaped an answer or plan, not on every project answer and
  not only upon user request
- promoted the policy into local Graphify memory inputs:
  `.graphify_project_brain/verified_query_seed_notes.json` and
  `.graphify_project_brain/agent_semantic_seed.json`

Interpretation:

- this keeps reusable memory, source authority, and exploratory retrieval in
  separate lanes
- the policy is portable to MediaLab or another project without requiring that
  project to copy Capstone's exact graph names or scripts

Boundary:

- no BDA runtime code, prompts, overlays, manifests, references, promotion
  artifacts, or experiment truth changed

### 2026-04-28 - Refined SequentialThinking Governance Checkpoint Rule

What changed:

- updated the global Codex rules, global MCP usage guide, and Capstone root
  `AGENTS.md` so SequentialThinking remains Plan Mode-focused and
  non-authoritative, but is now also an explicit pre-action governance
  checkpoint for high-blast-radius changes
- added concrete trigger classes:
  - global rule or `AGENTS.md` changes
  - MCP/tool routing changes
  - live-doc protocol or meaning changes
  - Graphify memory or trust-boundary changes
  - tool/subagent/FiftyOne activation changes
  - prompt/eval protocols, promotion gates, worktree governance, and
    multi-gate edit/validate/refresh workflows
- defined the checkpoint shape as: risk, safest path, what must not change, and
  validation

Interpretation:

- SequentialThinking is still not evidence and does not replace source
  inspection, tests, Graphify recall, runner artifacts, eval outputs,
  documented evidence, or human review
- the refinement adds blast-radius awareness without making SequentialThinking
  routine overhead for simple facts, quick checks, routine command output, or
  obvious low-risk edits

Boundary:

- no MCP config, BDA runtime code, prompts, overlays, manifests, references,
  promotion artifacts, or experiment truth changed

### 2026-04-28 - Added Phase 0 Reference Organization And Archive Planning Hub

What changed:

- created the central archive planning hub at `z_reference_docs/zz_archive/`
- added Phase 0 planning artifacts:
  - `README.md`
  - `ORGANIZATION_INVENTORY.md`
  - `PROPOSED_MOVE_MANIFEST.csv`
  - `REDUNDANCY_REVIEW.md`
  - `GRAPHIFY_ARCHIVE_INDEX.md`
- updated `REFERENCE_MASTER_INDEX.md` and `PROJECT_BRAIN.md` so the new
  organization map is discoverable

Interpretation:

- Phase 0 is decision prep only, not a file-reorganization wave
- the first safe later wave should focus on obvious backups and loose inactive
  docs
- generated Graphify history should be archived, if approved later, inside
  ignored Graphify profile-local archive areas with only lightweight tracked
  routing in `zz_archive`
- active live docs, Prompt_Labs evidence, human-report materials, current
  Graphify outputs, and worktree governance remain hot

Boundary:

- no source files, Prompt_Labs evidence, human reports/images, runtime code,
  prompts, overlays, references, manifests, AGENTS layers, or Graphify generated
  workspaces were moved

### 2026-04-28 - Completed Phase 1 Loose Local-Doc Archive Moves

What changed:

- moved four approved loose files from the hot `z_reference_docs` root into
  `z_reference_docs/zz_archive/`:
  - `config.yaml.backup`
  - `Notes.txt`
  - `Prompt_to_Start_up_agents_in_new_project.txt`
  - `Capstone.code-workspace`
- kept `z_reference_docs/Capstone-Project.code-workspace` hot as the preferred
  workspace file because it includes the main checkout and active worktree root
- updated the archive manifest, organization inventory, project brain, master
  index, and prompt methodology references

Interpretation:

- Phase 1 reduced visible root clutter without losing traceability
- the next approved organization wave should be Graphify generated-history
  cleanup, not Data_set_Storage or active Prompt_Labs movement

Boundary:

- no worktree files, source code, runtime config, prompts, overlays, manifests,
  references, promotion artifacts, active Prompt_Labs evidence, Data_set_Storage
  content, human reports/images, AGENTS layers, or generated Graphify history
  were moved

### 2026-04-28 - Completed Phase 2 Graphify Generated-History Cleanup

What changed:

- moved `4` failed or incomplete extraction pilot workspaces into
  `.graphify_project_brain/archive/extraction_pilots/failed_or_incomplete/`
- moved superseded trusted-memory verification review workspaces into
  `.graphify_project_brain/archive/verification_reviews/superseded/`
- kept the latest three verification reviews hot in
  `.graphify_project_brain/verification_reviews/`
- updated the archive manifest, Graphify archive index, organization
  inventory, project brain, and master index

Interpretation:

- Phase 2 reduced Graphify visual clutter without deleting generated history
- successful pilot evidence, ingestion review packages, current graphs,
  trusted memory seeds, evidence indexes, and snapshots remain in their active
  locations
- the next approved organization wave should be Wave 3 existing-archive
  registration

Boundary:

- no worktree files, source code, runtime config, prompts, overlays, manifests,
  references, promotion artifacts, active Prompt_Labs evidence,
  Data_set_Storage content, human reports/images, trusted project-brain memory,
  or current Graphify graph outputs were moved

### 2026-04-28 - Completed Phase 3 Existing Archive Registration

What changed:

- created central registration indexes under
  `z_reference_docs/zz_archive/indexed_existing_archives/`
- registered `z_reference_docs/Prompt_Labs/archive/` without moving it
- registered
  `z_reference_docs/Prompting/Model_research-Archive-Not-to-be Used/`
  without moving it
- updated the archive manifest, archive README, organization inventory, master
  index, project brain, Prompt_Labs index, and Prompting index

Interpretation:

- Phase 3 improves discoverability of historical archive material without
  breaking existing references
- the original archive folders remain authoritative for source checks
- the next organization wave should be Wave 4 redundancy and consolidation
  review as a recommendation package first

Boundary:

- no source files, worktree files, active Prompt_Labs model lines,
  human-report challenge evidence, Data_set_Storage content, runtime config,
  prompts, overlays, manifests, references, promotion artifacts, Graphify
  generated outputs, or archive contents were moved

### 2026-04-28 - Completed Phase 4 Redundancy And Consolidation Review

What changed:

- expanded `z_reference_docs/zz_archive/REDUNDANCY_REVIEW.md` into a
  decision-ready recommendation package
- classified overlap clusters for program reports, architect rollout docs,
  Codex/MCP/tooling docs, prompt-method docs, worktree/update governance,
  capstone tech-doc tracking, and dataset/human-report surfaces
- added future proposal rows to
  `z_reference_docs/zz_archive/PROPOSED_MOVE_MANIFEST.csv`
- updated the archive README, organization inventory, master index, project
  brain, and this changelog

Interpretation:

- Phase 4 intentionally did not consolidate anything
- current human-report and v015 planning materials remain hot
- likely next choices are a tiny live-doc consistency cleanup for stale
  SequentialThinking wording, or Phase 5 data-path audit for the remaining
  high-risk dataset clutter

Boundary:

- no files or folders were moved, merged, deleted, renamed, or consolidated
- no worktree files, source code, runtime config, prompts, overlays, manifests,
  references, promotion artifacts, Prompt_Labs evidence, Data_set_Storage
  content, human reports/images, trusted project-brain memory, or Graphify
  generated outputs were changed by hand

### 2026-04-28 - Completed Phase 4B SequentialThinking Wording Cleanup

What changed:

- aligned stale SequentialThinking wording in:
  - `PROMPT_DEVELOPMENT_METHODOLOGY.md`
  - `PROMPT_CRAFTING_INSTRUCTIONAL_GUIDE.md`
  - `capstone_tech_docs/understanding_tracking.md`
- updated the Phase 4B manifest row to `completed_wording_cleanup`
- updated archive routing docs, project brain, master index, and this changelog

Interpretation:

- this is wording cleanup only, not a rule change
- current guidance is now consistent: SequentialThinking is re-enabled,
  Plan Mode-scoped by default, available as a compact governance checkpoint,
  and not evidence or source truth
- Phase 5 data-path audit remains the likely next structural cleanup step

Boundary:

- no global rules, project AGENTS, MCP config, source code, Prompt_Labs
  evidence, data folders, human reports/images, worktree files, prompts,
  overlays, manifests, references, promotion artifacts, trusted memory, or
  Graphify generated outputs were changed by hand

### 2026-04-28 - Completed Phase 5 Data-Path Audit

What changed:

- created the audit-only `Data_set_Storage` routing package under
  `z_reference_docs/zz_archive/data_set_storage/`
- recorded current size, file counts, reference counts, classifications, and
  future move-readiness for the major data paths
- added a trusted project-brain note/semantic seed for the durable data-path
  boundary
- updated archive routing docs, project brain, master index, and this changelog

Interpretation:

- `human_reports/` remains hot because it contains the approved 112-pair source
  lane and held-out no-report material for current Qwen/v015 work
- `Unlabeled Photos/` remains high-risk because it is referenced by Prompt_Labs
  and validation history
- `Reports_(OLD)/` is still only a future archive candidate; it should be
  compared with `Updated_Reports/` before any move
- empty folders such as `RoboFlow_/` and `Unlabeled_Photos/` are only future
  cleanup candidates

Boundary:

- no data folders, source images, human reports, Prompt_Labs evidence,
  worktree files, source code, runtime config, prompts, overlays, manifests,
  references, promotion artifacts, or Graphify generated outputs were moved,
  deleted, renamed, merged, or rewritten

### 2026-04-28 - Completed Phase 5A DATA_SET Report Provenance Review

What changed:

- created the review-only old-vs-updated report provenance package:
  - `z_reference_docs/zz_archive/data_set_storage/DATA_SET_REPORT_PROVENANCE_REVIEW.md`
  - `z_reference_docs/zz_archive/data_set_storage/DATA_SET_REPORT_PROVENANCE_MAP.csv`
- mapped every clean file and every `:Zone.Identifier` companion in
  `Reports_(OLD)/` and `Updated_Reports/`
- updated the Phase 5 data-path audit, move-readiness map, archive manifest,
  project brain, master index, and this changelog

Interpretation:

- `Updated_Reports/` is a partial structured conversion of `Reports_(OLD)/`,
  not a clean authoritative replacement
- known review flags include malformed JSON-like updated reports `01` and
  `43`, object-count reductions in `03`, `04`, and `05`, typo-like
  `02..txt`, and a non-doctrinal `unknown` damage value in `45`
- old-only `40.txt`, `71.txt`, and `BDA Report Template.docx` remain
  provenance items

Boundary:

- no report files, metadata companions, folders, source images, human reports,
  Prompt_Labs evidence, worktree files, source code, runtime config, prompts,
  overlays, manifests, references, promotion artifacts, or Graphify generated
  outputs were moved, deleted, renamed, merged, normalized, or rewritten

### 2026-04-28 - Completed Phase 5B Empty Folder Cleanup Review

What changed:

- created the review-only empty-folder cleanup package:
  - `z_reference_docs/zz_archive/data_set_storage/EMPTY_FOLDER_CLEANUP_REVIEW.md`
  - `z_reference_docs/zz_archive/data_set_storage/EMPTY_FOLDER_CLEANUP_MAP.csv`
- confirmed seven empty-folder candidates under `Data_set_Storage`
- updated the Phase 5 data-path audit, move-readiness map, archive manifest,
  project brain, master index, redundancy review, and this changelog

Interpretation:

- `RoboFlow_/` is the lowest-risk later cleanup candidate
- `Unlabeled_Photos/` is an empty duplicate-like tree, but should still wait
  for explicit cleanup approval because `Unlabeled Photos/` is a high-risk
  similarly named raw-media path
- empty folders inside `Unlabeled Photos/` and
  `DATA_SET/Assigned_Photos_to_Write_Report/` should remain deferred until
  their parent lanes are reviewed

Boundary:

- no empty folders, data folders, source images, human reports, Prompt_Labs
  evidence, worktree files, source code, runtime config, prompts, overlays,
  manifests, references, promotion artifacts, or Graphify generated outputs
  were moved, deleted, renamed, merged, normalized, or rewritten

### 2026-04-28 - Removed Empty RoboFlow Placeholder

What changed:

- removed only `z_reference_docs/Data_set_Storage/RoboFlow_/` after explicit
  user approval
- added the cleanup record:
  `z_reference_docs/zz_archive/data_set_storage/ROBOFLOW_EMPTY_FOLDER_CLEANUP.md`
- updated data-path audit docs, move-readiness maps, project brain, master
  index, redundancy review, and this changelog

Interpretation:

- `RoboFlow_/` was empty and had no observed direct references beyond the
  audit/manifest records
- this does not approve broader dataset cleanup
- `Unlabeled_Photos/` and all other empty folders remain in place as deferred
  cleanup candidates

Rollback:

- recreate the empty placeholder with
  `mkdir -p z_reference_docs/Data_set_Storage/RoboFlow_`

Boundary:

- no source image, human report, Prompt_Labs evidence, worktree file, source
  code, runtime config, prompt, overlay, manifest, reference, promotion
  artifact, Graphify generated output, or other data folder was moved, deleted,
  renamed, merged, normalized, or rewritten

### 2026-04-28 - Recorded NCP, MCPFinder, And Spences10 MCP Candidate Boundaries

What changed:

- researched the requested MCP candidates before later migration waves changed
  their status:
  - NCP / Natural Context Provider
  - MCPFinder
  - Spences10 `mcp-sequentialthinking-tools`
- updated the global MCP usage guide with the candidate-era section that was
  later renamed to "MCP Candidate And Migration Notes"
- updated the project brain and master index so future Capstone work can recall
  the NCP safety boundary without treating NCP as an active tool
- corrected the trusted `brain:mcp_boundaries` seed so it no longer says
  SequentialThinking is rule-disabled

Interpretation:

- this is a superseded candidate-era entry; use the 2026-04-29 stack
  stabilization checkpoint for current status
- `sequential-thinking` is now active and implemented by Spences10
  `mcp-sequentialthinking-tools`
- MCPfinder is now active as a discovery-only missing-MCP scout
- NCP remains planned/deferred and should not sit in front of high-power tools
  until find-only or strictly read-only routing, project-local state isolation,
  disabled internals, and visible/auditable underlying routing are proven

Boundary:

- no MCP config, global AGENTS rule, source code, runtime config, prompt,
  overlay, manifest, reference, promotion artifact, worktree file, dataset path,
  or generated Graphify output was changed by hand

### 2026-04-28 - Patched SequentialThinking Brain Recall

What changed:

- corrected the trusted `mcp_graphify_boundaries` verified note so it reflects
  the current SequentialThinking rule: Plan Mode by default, compact
  governance checkpoint for high-blast-radius work, not evidence
- added a dedicated recall expectation for
  `How should SequentialThinking be used?`
- added a narrow recall alias so that question resolves to the corrected
  trusted note rather than adjacent MCP research notes

Interpretation:

- project-brain recall should now answer SequentialThinking usage from the
  corrected trusted note instead of stale deactivation wording
- no tool routing behavior changed; this is a trusted-memory and regression
  coverage correction

Boundary:

- no MCP config, hooks, AGENTS files, source code, runtime config, prompt,
  overlay, manifest, reference, promotion artifact, worktree file, dataset path,
  or generated Graphify output was changed by hand

### 2026-04-28 - Canonicalized SequentialThinking Trigger Policy

What changed:

- made `/home/williambenitez1/.codex/AGENTS.md` the canonical
  SequentialThinking trigger policy
- made `/home/williambenitez1/.codex/MCP_USAGE_GUIDE.md` reflect and
  illustrate that policy instead of redefining it
- made Capstone root `AGENTS.md` the project-specific overlay for Capstone
  triggers
- collapsed nested active AGENTS and live-doc wording into pointers so they no
  longer carry separate policy copies
- updated the project-brain trusted note and semantic seed so recall answers
  the newer rule cleanly

Interpretation:

- SequentialThinking remains available, but should be used as a compact
  checkpoint for genuinely complex, risky, branchy, evidence-sensitive,
  critique-heavy, or high-blast-radius work
- it should not be invoked merely because Plan Mode is active
- it remains a whiteboard, not evidence or source truth

Boundary:

- no MCP config, hooks, source code, runtime config, prompt, overlay, manifest,
  reference, promotion artifact, worktree file, dataset path, or generated
  Graphify output was changed by hand

### 2026-04-29 - Stabilized Codex MCP Stack And Refreshed Project Brain

What changed:

- closed the laptop MCP/tooling migration into the current operating stack:
  - Mem0 is active as manual, durable advisory memory
  - `sequential-thinking` is active and backed by Spences10
    `mcp-sequentialthinking-tools`
  - MCPfinder is active as a discovery-only missing-MCP scout
  - NCP remains planned/deferred, not installed or routable
- corrected stale candidate-era wording in the global MCP usage guide so active
  MCPfinder and active Spences10 are no longer grouped under a "not installed"
  heading
- corrected the NCP/MCP router trusted note and semantic seed so project-brain
  recall now records:
  - spences10 active
  - MCPfinder active and discovery-only
  - Mem0 active and manual/approval-gated
  - NCP planned/deferred because of `run` exposure and unproven internal
    MCP/state-isolation controls
- refreshed Graphify/project-brain outputs and verified trusted memory:
  - `.graphify_project_brain/capstone_graphify.py update`
  - `.graphify_project_brain/capstone_graphify.py doctor --strict-stale`
  - `.graphify_project_brain/capstone_graphify.py recall-benchmark`
  - `.graphify_project_brain/capstone_graphify.py verify-memory --strict --json`
- added this migration checkpoint to the live docs and project-brain trusted
  memory lanes so future recall starts from the current stack, not the
  candidate-era research state

Validation:

- Graphify update completed
- `doctor --strict-stale` passed
- recall benchmark passed `36/36`
- strict trusted-memory verification checked `353` items with no duplicate ids
  and no missing generated notes
- targeted recall checks returned the current stack state from trusted memory
- MCP config, hooks, Mem0, MCPfinder, existing MCP memory, runtime code,
  prompts/evals/datasets, promotion artifacts, and active worktrees were not
  modified by this stabilization pass

Boundary:

- this documents and refreshes the current tooling stack only; it does not
  approve Mem0 writes, candidate MCP installs, NCP activation, MCP config
  edits, hook edits, runtime changes, prompt/eval changes, dataset mutation, or
  promotion artifact mutation

### 2026-04-29 - Added Worktree-Only Qwen v015 Human-Report Strategy Package

What changed:

- implemented the first human-report-informed `v015` strategy package only in
  the active Qwen `1.2` worktree:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/`
- generated analysis artifacts for the next prompt-engineering decision:
  - `README.md`
  - `source_manifest.json`
  - `failure_taxonomy.md` and `failure_taxonomy.json`
  - `stratified_split.md` and `stratified_split.json`
  - `example_bank.md` and `example_bank.json`
  - `candidate_hypotheses.md`
  - `acceptance_gates.json`
- added the helper script only in the Qwen `1.2` worktree:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/scripts/build_v015_human_report_strategy.py`

Validation:

- main checkout and `origin/main` were confirmed unchanged before and after the
  package build
- all generated JSON parsed
- the split has no dev/holdout overlap and preserves all five human-report
  slices in both sets
- `101` is included in the diagnostic/dev set as a hinge case
- out-of-scope controls `155` and `166` remain explicitly protected
- candidate directions remain hypothesis-only with no final prompt text

Boundary:

- this package is prompt-learning analysis, not a `v015` prompt, overlay,
  runtime change, VLM inference run, evaluation promotion, or source-of-truth
  change
- main checkout source artifacts remain read-only evidence for this wave; any
  later promotion into runtime, prompt overlays, or public docs requires
  separate approval

### 2026-04-29 - Ran Worktree-Only Qwen v015a-v015e Prompt Candidate Sequence

What changed:

- stayed inside the active Qwen `1.2` worktree for all prompt-candidate work:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/`
- authored and hinge-smoke tested prompt-only candidates:
  - `v015a_recall_recovery`
  - `v015b_distinct_object_guard`
  - `v015c_count_first_uncertainty_gate`
  - `v015d_fail_closed_row_guard`
  - `v015e_individual_body_evidence`
- added diagnostic packages for:
  - `v015a` hinge failure review
  - `v015abc` hinge synthesis and `v015d` decision
  - an offline structural guard simulator using existing hinge outputs only
  - `v015e` case `101` manual review

Interpretation:

- `v015a` recovered recall but reopened false positives, especially on case
  `101`
- `v015b` and `v015c` did not solve the `101` row-fragment/broad-box boundary
- `v015d` suppressed row fragments and held precision guards, but was too
  conservative and failed to beat the v014 hinge baseline
- the offline guard simulator caught row-fragment and broad-box shapes, but
  was too blunt: it reduced false positives by deleting too many detections and
  is diagnostic evidence only, not a runtime-ready guard
- `v015e` is the strongest prompt-only hinge result so far:
  - standard hinge gate passed
  - aggregate result: `10` matches, `13` false negatives, `0` false positives
  - protected case `155` passed
  - case `101` row-fragment enumeration was suppressed
  - case `101` still emitted one broad group/scene box, so the two-tier gate
    failed and dev remains blocked

Current decision state:

- do not promote `v015e`
- do not adopt any `v015` runtime config
- do not run dev, holdout, or all-112 automatically
- `101` remains a manual diagnostic hinge with reference/eval-shape caveats:
  the large foreground-tank reference box can make oversized predictions look
  better numerically than visually, and `target_7` / `target_8` are duplicate
  reference boxes
- if the user later approves a dev run, frame it as a learning-only
  generalization check for `v015e`, with `101` retained as a known
  manual-review failure and with no automatic holdout, all-112, runtime
  adoption, or promotion

Key worktree artifacts:

- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015e_individual_body_evidence/README.md`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015e_individual_body_evidence/executions/human_report_challenge_v1_v015e_hinge_smoke_2026-04-29_223729Z/v015e_gate_check_summary.json`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015e_individual_body_evidence/executions/human_report_challenge_v1_v015e_hinge_smoke_2026-04-29_223729Z/case_101_manual_review.md`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/diagnostics/v015_offline_structural_guard_simulator/raw_vs_guarded_metrics.md`

Boundary:

- this sequence created local prompt-lab evidence only
- no main checkout tracked source/runtime prompt was changed during the
  candidate runs
- no source human-report data, challenge references, runtime config,
  promotion artifact, Graphify generated output, evidence index, Mem0 memory,
  MCP config, or hook was changed by the candidate runs

### 2026-04-29 - Updated Live Docs, Project-Brain, And Mem0 For v015e State

What changed:

- updated live documentation so future sessions no longer think the v015 lane
  is only a pre-prompt analysis package:
  - `z_reference_docs/WORKING_CHANGELOG.md`
  - `z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
  - `z_reference_docs/PROJECT_BRAIN.md`
  - `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/README.md`
- updated trusted project-brain inputs:
  - `.graphify_project_brain/verified_query_seed_notes.json`
  - `.graphify_project_brain/agent_semantic_seed.json`
- refreshed Graphify/project-brain outputs and verified the trusted-memory lane
- wrote one explicit user-approved Mem0 advisory memory for the current Qwen
  v015 state

Current durable recall point:

- v015a-v015e are worktree-only prompt-learning evidence, not runtime truth
- `v015e_individual_body_evidence` is the strongest prompt-only hinge result
  so far (`10` matches, `13` false negatives, `0` false positives), but it is
  not promoted
- dev remains blocked unless explicitly approved as a learning-only run because
  manual review confirms case `101` still emits one broad group/scene box
- case `101` remains a manual diagnostic hinge with reference/eval-shape
  caveats, including a very large foreground reference box and duplicate
  `target_7` / `target_8` boxes

Validation:

- project-brain update completed
- `doctor --strict-stale` passed
- recall benchmark passed `36/36`
- strict trusted-memory verification checked `365` items with no duplicate ids
  and no missing generated notes
- targeted recall for the v015e status returned the new verified note and
  semantic seed
- Mem0 write was explicitly approved by the user and queued through the hosted
  `mem0` MCP

Boundary:

- this was a documentation, Graphify/project-brain, and Mem0 advisory-memory
  update only
- no runtime config, source human-report data, challenge references, prompt
  candidate overlays, dev/holdout/all-112 runs, promotion artifacts, MCP
  config, hooks, or existing MCP memory were changed by this update

### 2026-04-29 - Completed v016 Reference-Aware Prompt-Lab Design Package

What changed:

- completed the worktree-only design package:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/design/v016_reference_aware_prompt_lab/`
- added design-only artifacts:
  - `README.md`
  - `source_manifest.json`
  - `case_failure_review.md` / `case_failure_review.json`
  - `reference_shape_audit.md` / `reference_shape_audit.json`
  - `prompt_vs_structural_guard_comparison.md`
  - `v016_prompt_axis_recommendation.md` /
    `v016_prompt_axis_recommendation.json`
- updated the worktree-local v015 strategy README so the v016 design package
  is discoverable

Current durable recall point:

- `v015e` held dev precision but failed dev recall:
  - v015e dev: `61` matches, `56` false negatives, `17` false positives
  - v014 dev baseline: `70` matches, `47` false negatives,
    `17` false positives
- case `101` remains a manual diagnostic with reference/eval-shape caveats and
  broad-box behavior; it should guide method design, not become a simple
  metric target
- the selected v016 axis is
  `v016_reference_aware_candidate_discovery_with_evidence_budget`
- the next natural work remains prompting-focused: author one worktree-only
  `v016a` prompt/overlay from that axis and run hinge smoke only

Boundary:

- this was a design package and recall update only
- no v016 prompt text, overlay, runner session, validation manifest, run
  directory, promotion report, runtime config change, source-truth mutation,
  holdout/all-112 run, Graphify refresh, evidence rebuild, or Mem0 write was
  created during the package build itself
- this later live-doc/brain/Mem0 update records the completed design package;
  it still does not approve dev, holdout, all-112, promotion, or runtime
  adoption

### 2026-04-30 - Updated Live Docs, Project-Brain, And Mem0 For v016 Design State

What changed:

- updated current project live docs so future sessions recall that the v015
  lane now bridges into a design-only v016 prompt-lab package:
  - `z_reference_docs/WORKING_CHANGELOG.md`
  - `z_reference_docs/PROMPT_DEVELOPMENT_METHODOLOGY.md`
  - `z_reference_docs/PROJECT_BRAIN.md`
- updated trusted project-brain inputs:
  - `.graphify_project_brain/verified_query_seed_notes.json`
  - `.graphify_project_brain/agent_semantic_seed.json`
- refreshed Graphify/project-brain outputs and verified the trusted-memory lane
- wrote one user-approved Mem0 advisory update for the v016 design state

Current durable recall point:

- v015a-v015e remain worktree-only prompt-learning evidence
- v015e preserved dev precision but failed dev recall:
  - v015e dev: `61` matches, `56` false negatives, `17` false positives
  - v014 dev baseline: `70` matches, `47` false negatives,
    `17` false positives
- completed design-only package:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/design/v016_reference_aware_prompt_lab/`
- selected next axis:
  `v016_reference_aware_candidate_discovery_with_evidence_budget`
- next implementation should remain prompt-focused: one worktree-only `v016a`
  prompt/overlay and hinge smoke only, before any dev/holdout/all-112,
  promotion, or runtime-adoption discussion

Validation:

- trusted-memory JSON inputs parsed
- project-brain update completed
- `doctor --strict-stale` passed
- recall benchmark passed `36/36`
- strict trusted-memory verification checked `372` items with no duplicate ids
  and no missing generated notes
- targeted recall for the v016 direction returned the new verified note and
  semantic seed
- Mem0 add event `73bb25af-ed03-476f-80fe-5b4a476d9451` succeeded

Boundary:

- this update changed documentation, generated Graphify/project-brain outputs,
  trusted-memory inputs, and approved Mem0 advisory memory only
- no runtime config, source human-report data, challenge references, prompt
  overlay, runner session, dev/holdout/all-112 run, promotion artifact, MCP
  config, hooks, or existing MCP memory was intentionally changed

### 2026-04-30 - Ran Worktree-Only Qwen v016a Prompt Candidate Hinge Smoke

What changed:

- authored one prompt-only `v016a_reference_aware_candidate_discovery`
  candidate in the active Qwen `1.2` worktree from the selected v016 axis:
  `v016_reference_aware_candidate_discovery_with_evidence_budget`
- added only worktree-local candidate artifacts:
  - overlay:
    `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/overlays/qwen_1_2_v016a_detect_reference_aware_candidate_discovery.yaml`
  - hypothesis:
    `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/hypotheses/qwen_1_2_v016a_detect_reference_aware_candidate_discovery_hypothesis.yaml`
  - expanded hinge manifest:
    `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/validation/human_report_challenge_v1_v016a_hinge_smoke.yaml`
  - runner session:
    `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runner_sessions/qwen_1_2_v016a_detect_reference_aware_candidate_discovery_session_v1.yaml`
  - run README:
    `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v016a_reference_aware_candidate_discovery/README.md`
  - hinge gate helper:
    `scripts/check_v016a_hinge_gate.py`
- ran only the approved expanded 12-case hinge smoke:
  `101`, `13`, `42`, `147`, `12`, `28`, `19`, `155`, `66`, `67`, `84`, `97`

Result:

- run directory:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v016a_reference_aware_candidate_discovery/executions/human_report_challenge_v1_v016a_hinge_smoke_2026-04-30_015313Z/`
- aggregate expanded-hinge result:
  - `27` matches
  - `29` false negatives
  - `33` false positives
  - `60` predicted targets
- compared with the expanded v014 hinge baseline:
  - v014 baseline: `22` matches, `34` false negatives, `16` false positives
  - v016a improved recall but failed the precision cap
- protected case `155` remained abstention-safe
- case `101` failed the two-tier diagnostic:
  - row-fragment enumeration remained present
  - a broad group/scene box remained present
  - `101` produced `7` matches, `5` false negatives, and `16` false positives
- added manual review artifacts:
  - `case_101_manual_review.md`
  - `case_101_manual_review.json`
  - `expanded_hinge_notes.md`
  - `expanded_hinge_notes.json`

Decision:

- `v016a` is blocked from dev
- do not run dev, holdout, all-112, promotion, runtime config adoption, or
  source-truth mutation from this result without a new approval
- interpretation: the reference-aware candidate-discovery prompt axis recovered
  hinge recall but reopened precision failures; the next prompt move should
  treat v016a as learning evidence, not as a candidate to deepen automatically

Validation:

- main still matched `origin/main` before and after the work
- main tracked and staged diffs remained clean
- prompt placeholders were preserved
- YAML/JSON artifacts parsed
- prompt-lab integrity validation passed
- targeted prompt-lab/runtime/session unit tests passed
- `git diff --check` passed
- no dev, holdout, all-112, promotion, runtime config adoption, source-truth
  mutation, MCP config change, hook edit, or candidate MCP install was run

### 2026-04-30 - Recorded v016a/v009/v014 Comparison And Next Prompt Step

What changed:

- updated live docs and trusted project-brain memory inputs so the latest
  prompt-lane comparison is recallable:
  - `v009` remains the all-112 promoted control and recall baseline, but it is
    noisy: `161` matches, `56` false negatives, `54` false positives on
    all-112; `31` matches, `25` false negatives, `39` false positives on the
    expanded hinge baseline
  - `v014` remains the precision-suppression lesson, but it is too
    recall-suppressive for direct promotion: `148` matches, `69` false
    negatives, `24` false positives on all-112; `22` matches, `34` false
    negatives, `16` false positives on the expanded hinge baseline
  - `v016a` is hinge-only learning evidence: `27` matches, `29` false
    negatives, `33` false positives, and `60` predicted targets on the
    expanded hinge; it recovered some recall versus `v014` but leaked precision
    back toward the `v009` false-positive failure mode
- recorded the next natural prompt-lane step as a worktree-only `v016a`
  failure synthesis plus `v016b` prompt-axis decision package before any new
  prompt text, hinge run, dev run, holdout, all-112 run, runtime adoption, or
  promotion

Decision:

- do not deepen `v016a`
- do not author or run `v016b` until the failure-synthesis package explains
  where `v016a` helped, where it leaked precision, and what final-output
  discipline a prompt-only `v016b` should test
- keep this work prompt-engineering-focused; structural guards remain a
  separate future scope, not the next implementation path

### 2026-04-30 - Closed Codex VS Code Diagnostics And Recorded Safe-Noise Boundaries

What changed:

- closed the local Codex VS Code diagnostics wave without further extension
  surgery:
  - verified the earlier laptop environment fixes held in later clean logs:
    `bubblewrap` PATH is now clean and the `desktop-commander` Chrome/PDF
    bootstrap failure is gone
  - verified that the remaining connector/logo overload flood persists in the
    stock extension and may still trigger `Server overloaded; retry later.`
    plus occasional `outbound queue is full` pressure
  - researched the other recurring warning families and documented them as
    separate boundaries:
    - `workspace_dependencies` is an internal feature-enable mismatch between a
      broader feature list and a narrower sync API
    - `thread-stream-state-changed` and related IPC warnings are broadcast
      handler-gap noise, not direct evidence of broken turn state
    - `https://chatgpt.com/ces/v1/rgstr` `403` responses come from the stock
      webview analytics/event transport rather than core Codex chat or MCP
      execution
    - plugin `interface.defaultPrompt` warnings are metadata validation noise
      limited to starter/example prompt UI for two cached plugins

Decision:

- keep the VS Code extension stock
- do not patch compiled extension bundles again; the earlier local bundle edits
  were brittle and could destabilize Codex
- treat the remaining warning families as monitored noise unless they cross
  into user-visible failure

Revisit trigger:

- reopen this only if turns fail to send or resume, thread/read status stops
  updating in the UI, Codex becomes materially sluggish or unavailable, or the
  connector/logo flood starts blocking normal IDE use instead of just filling
  the log

Boundary:

- no apps/connectors were removed or reconfigured
- no further compiled-extension patching was performed
- no Capstone runtime code, prompt code, datasets, MCP config, hooks, or
  worktree contents were changed by this closeout
### 2026-05-02 - Accepted Poster V3 Polish And Opened Scratch Poster Concept Branch

What changed:

- The local PowerPoint poster v3 final-polish copy was accepted as a useful
  improvement for the team's current slide 3 direction:
  `z_reference_docs/capstone_tech_docs/Poster/Poster sample template - 24x36 - local redesign draft v3 final polish.pptx`.
- The accepted v3 idea keeps the team-compatible pipeline-centered direction
  while improving the problem panel, proof callout, scoring caption, and visual
  friction around the pipeline-spine chip.
- The next poster branch is a separate from-scratch concept for comparison, not
  a replacement for the team deck or the v3 review copy.

Current direction:

- Preserve the team deck, v1, v2, and v3 review copies.
- Create any scratch poster concept as a clearly named, separate artifact under
  the Poster workspace.
- Keep the concept source-grounded in current repo behavior, the Phase 4 deck,
  the User Guide Part 1 Draft, and `Data_set_Storage/evaluation`.
- Keep the proof frame concise: `gemma4:26b` led total score at `0.674` and ran
  `68.9% faster` than `qwen3-vl:235b-cloud`.
- Keep Canva output and prompt-lab/worktree material out of the poster concept.

### 2026-05-02 - Created From-Scratch Poster Concept V1

What changed:

- Created a separate from-scratch poster concept:
  `z_reference_docs/capstone_tech_docs/Poster/BDA_from_scratch_concept_v1.pptx`.
- Added companion notes:
  `z_reference_docs/capstone_tech_docs/Poster/BDA_from_scratch_concept_v1_notes.md`.
- Rendered the concept to `/tmp/capstone_poster_scratch_concept_v1/slide-1.png`
  for visual review.

Current direction:

- Treat the scratch concept as a comparison artifact, not a replacement for the
  team deck or v3 final-polish copy.
- The concept tests a fresh hierarchy: thesis ribbon, BDA problem definition,
  native `bda-svc` pipeline, BDA-200 data card, evaluation-proof card, and a
  closing takeaway band.
- Keep source grounding: Phase 4 result framing and eval CSVs support the
  `gemma4:26b` `0.674` total score and `68.9% faster` claim.
- Continue excluding Canva output and prompt-lab/worktree material from poster
  deliverables.

### 2026-05-02 - Created From-Scratch Poster Concept V1.1 Intense Polish

What changed:

- Created a stronger polish pass on the scratch poster concept:
  `z_reference_docs/capstone_tech_docs/Poster/BDA_from_scratch_concept_v1_1_intense_polish.pptx`.
- Added notes:
  `z_reference_docs/capstone_tech_docs/Poster/BDA_from_scratch_concept_v1_1_intense_polish_notes.md`.
- Rendered the review PNG at
  `/tmp/capstone_poster_scratch_concept_v1_1/slide-1.png`.

Current direction:

- Treat v1.1 as the most assertive comparison concept, not as a replacement for
  the team deck or v3 final-polish copy.
- Use it to compare scan speed, visual confidence, and project-story clarity
  against the team-compatible v3 direction.
- Transferable ideas include the mission-flow rail, visual BDA-200 distribution
  bars, larger result proof cards, and final claim band.
- Keep proof wording grounded in Phase 4 and eval CSVs: `gemma4:26b` total
  score `0.674` and `68.9% faster` than `qwen3-vl:235b-cloud`.

### 2026-05-02 - Closed Canva Poster Sidecar And Removed Canva MCP

What changed:

- Human visual review rejected all four generated Canva poster concepts; the
  team PowerPoint direction and local source-grounded drafts remain stronger.
- The active poster workflow is now PowerPoint-local:
  - v3 final polish remains the conservative team-compatible slide 3 upgrade.
  - v1.1 intense polish remains the bold comparison concept to mine for ideas.
  - Canva output remains historical context only, not design authority or
    source truth.
- The task-scoped Canva MCP `canva-poster-task` was removed from the active
  global Codex MCP config and marked `removed` in the global/project tool
  inventories.

Current direction:

- On Monday, discuss the poster with the team using v3 as the safe path and
  v1.1 as the bolder idea source.
- Do not involve Canva unless a future explicit approval reinstalls or
  re-enables a Canva connector for a narrow sidecar use.
- Continue grounding poster claims in the Phase 4 deck, the user guide draft,
  evaluation CSVs, and rendered PowerPoint review artifacts.

### 2026-05-03 - Removed Case 101 From Forward Prompt-Evaluation Gates

What changed:

- Reclassified human-report case `101` as diagnostic-only for future Qwen
  prompt-cycle work. It remains preserved as historical/manual diagnostic
  evidence, but it is no longer a forward pass/fail evaluation gate.
- Added active forward manifest
  `human_report_challenge_v2_hinge_11_no101.yaml` in the Qwen `1.2`
  worktree automation lane.
- Preserved the old `human_report_challenge_v2_hinge_12` pack as
  historical/manual diagnostic context only.
- Updated the v2 prompt-iteration gate policy, cycle policy, controller
  contract, v017b diagnosis, and automation scripts so future dry-run/live
  plans route through `hinge_11_no101`.

Current direction:

- Continue `v017c` through `v017f` inside the approved cycle budget unless a
  hard stop triggers.
- Active forward gate: `13`, `42`, `147`, `12`, `28`, `19`, `155`, `66`,
  `67`, `84`, and `97`; case `101` is excluded from pass/fail use.
- Recalibrated 11-case baselines:
  - `v009`: `24` matches, `21` false negatives, `26` false positives
  - `v014`: `20` matches, `25` false negatives, `17` false positives
- Forward thresholds: more than `20` matches, fewer than `25` false negatives,
  no more than `21` false positives, positive-control `155`, changed-source
  sanity, updated-report smoke, and separate `office-negative` abstention.
- Do not run dev, holdout, all-112, promotion, runtime adoption, source-truth
  mutation, structural guards, MCP config changes, hook edits, or tool installs
  without separate approval.

### 2026-05-03 - Completed Qwen v017c-v017f Overnight Prompt Cycle

What changed:

- Continued the approved Qwen `1.2` `human_report_challenge_v2` prompt-only
  automation cycle through `v017f` using the active
  `human_report_challenge_v2_hinge_11_no101` forward gate.
- Authored and ran four worktree-only prompt overlays:
  - `v017c_evidence_named_finalization`
  - `v017d_visual_anchor_lock`
  - `v017e_footprint_aligned_anchors`
  - `v017f_compact_visual_anchor_balance`
- All four passed the active forward gates: hinge 11 without `101`,
  changed-source sanity, and the separate `office-negative` abstention guard.
- Wrote the cycle decision packet:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/overnight_v017c_to_v017f_decision_packet.md`

Results:

- `v017c`: `21` hinge matches, `24` false negatives, `15` false positives;
  changed-source `10/2/0`; updated-smoke `25/6/1`; office-negative passed.
- `v017d`: `22` hinge matches, `23` false negatives, `13` false positives;
  changed-source `10/2/0`; updated-smoke `24/7/1`; office-negative passed.
- `v017e`: `22` hinge matches, `23` false negatives, `14` false positives;
  changed-source `10/2/0`; updated-smoke `24/7/1`; office-negative passed.
- `v017f`: `23` hinge matches, `22` false negatives, `17` false positives;
  changed-source `9/3/1`; updated-smoke `24/7/2`; office-negative passed.

Current direction:

- Recommend `v017d_visual_anchor_lock` as the best balanced potential winner
  for morning review.
- Treat `v017f_compact_visual_anchor_balance` as the recall-oriented alternate
  if the next decision prioritizes one more hinge match over precision margin.
- Do not run dev, holdout, all-112, promotion, runtime adoption, source-truth
  mutation, structural guards, MCP config changes, hook edits, or tool installs
  without separate approval.
- Case `101` remains diagnostic-only unless a later source/reference audit
  changes that policy.

### 2026-05-03 - Completed Bounded v017d/v017f Dev Validation

What changed:

- Ran a bounded 55-case dev validation on
  `human_report_challenge_v2_dev_55_no101`, derived from the v2 dev split with
  case `101` removed from forward pass/fail evaluation.
- Treated `v017d_visual_anchor_lock` as the primary candidate and
  `v017f_compact_visual_anchor_balance` as a validation comparator only.
- Preserved boundaries: no holdout, all-112/all-current, promotion, runtime
  config adoption, source-truth mutation, structural guard implementation,
  MCP config change, hook edit, or Mem0 write.
- Wrote the bounded dev validation package:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/dev_validation/v017d_v017f_dev_no101/`

Results:

- same-split baselines:
  - `v009`: `74` matches, `32` false negatives, `27` false positives
  - `v014`: `69` matches, `37` false negatives, `17` false positives
  - `v015e`: `59` matches, `47` false negatives, `18` false positives
- `v017d`: `72` matches, `34` false negatives, `16` false positives;
  positive `155` passed with `2` matches.
- `v017f`: `73` matches, `33` false negatives, `18` false positives;
  positive `155` passed with `2` matches.

Current direction:

- Keep `v017d_visual_anchor_lock` as the primary balanced candidate because it
  improves on the v014 no-101 dev baseline across matches, false negatives, and
  false positives.
- Treat `v017f_compact_visual_anchor_balance` as the recall-oriented comparator:
  it gains one match / one fewer false negative versus `v017d`, but exceeds the
  v014 false-positive ceiling.
- Next decision should be human review of the bounded dev packet before any
  holdout, all-current, promotion, or runtime adoption step.

### 2026-05-03 - Accepted v017b Prompt-Only Main Promotion, Parked Locally

What changed:

- Reran the focused primary-candidate comparison on the exact
  `human_report_challenge_v2_dev_55_no101` manifest for `v009`, `v014`,
  `v015e`, `v016a`, and `v017a` through `v017f`.
- The `v017d` replay matched the accepted bounded-dev result exactly
  (`72` matches, `34` false negatives, `16` false positives), so the anchor
  was stable.
- Fresh same-split comparison reopened `v017b_group_box_rejection` as the
  precision challenger: it scored `72` matches, `34` false negatives, and
  `13` false positives, matching `v017d` recall while reducing false
  positives by `3`.
- Ran the final prompt-only main pre-adoption smoke/all-current no-101 check
  for `v017b` after applying only the `prompts.detect_objects` text in
  `src/bda_svc/pipeline/config.yaml`.
- Raw all-current/no-101 result: `165` matches, `54` false negatives, and
  `22` false positives against a cap of `21`.
- Focused visual review of the nine FP-bearing cases accepted a semantic
  override for case `125`: the `object_not_found` placeholder on a positive
  case is already a recall miss represented by a false negative, not an extra
  hallucinated target for the promotion false-positive cap.
- Effective extra-target false positives are therefore `21`, which meets the
  cap; positive `155`, positive `166`, and `office-negative` abstention all
  passed.
- Case `67` remains the preserved follow-up caveat: `1` match, `10` false
  negatives, and `10` false positives in dense smoke/dust row-formation
  imagery. It is not a promotion blocker after the accepted override, but it
  should guide the next failure-analysis cycle.
- The exact `v017b` prompt text was committed locally as:
  `2f67016 Promote v017b Qwen detection prompt`.

Current direction:

- Treat `v017b_group_box_rejection` as the accepted prompt-only main promotion
  candidate, parked locally.
- Do not make further local commits, do not push to `origin` or `upstream`, and
  do not reconcile `upstream/main` unless the user explicitly asks.
- `origin/main` remains unchanged; local `main` is one commit ahead of
  `origin/main` because of the parked promotion commit.
- The existing untracked `NUL` and `TOOL_INVENTORY.md` files in the main
  checkout remain untouched.
- Next useful choices are a source-grounded doc/brain closeout, a deliberate
  push/PR plan, or a case-`67` follow-up diagnosis after the promotion state is
  safely recorded.

### 2026-05-04 - Case 67 Diagnosis And v018a Failed Challenger Closeout

- Completed the follow-up diagnostic for case `67` after the parked `v017b`
  prompt-only promotion decision.
- Diagnostic conclusion:
  - case `67` is a real dense-formation limitation, but not a
    `v017b`-specific regression
  - every compared prompt family scored only `1` match and `10` false
    negatives on the same case
  - the failure is best read as dense smoke/dust plus perspective-row
    body-anchor pressure, with predictions often pulled toward top-edge,
    plume, rowline, or dust cues instead of visible target body centers
  - it is not the same failure mode as the old case `101` broad group/scene-box
    diagnostic
- Ran one bounded `v018a_dense_formation_body_center_anchor` prompt-only
  follow-up under `cycle_002`.
- `v018a` result:
  - formal no-101 smoke checks passed, including positive `155` and the
    separate `office-negative` abstention guard
  - compared with parked `v017b` on the same no-101 hinge scope, `v018a`
    regressed by `-1` match, `+1` false negative, and `+8` false positives
  - dense cases worsened rather than improving: case `66` added false
    positives, case `84` lost one match and added false positives, and case
    `67` stayed at `1` match and `10` false negatives while increasing to
    `10` false positives
- Decision:
  - `v018a` is learning evidence only
  - do not promote, deepen, dev-run, holdout-run, all-current-run, or replace
    `v017b` with `v018a`
  - keep `v017b_group_box_rejection` as the parked prompt-only main candidate
  - if another dense-formation attempt is considered later, it needs a tighter
    plan than generic body-center/ground-contact wording because that wording
    caused a false-positive rebound
- Source artifacts:
  - case `67` diagnostic:
    `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/case67_dense_formation_diagnostic/`
  - `v018a` run summary:
    `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_002/runs/v018a/live_2026-05-04_003732Z/v018a_dense_smoke_gate_summary.md`

### 2026-05-04 - v017b Doctrine Iteration Closed As Learning Evidence

- Ran the approved 15-candidate `doctrine.yaml` cycle with the fixed `v017b`
  prompt/config surface in the worktree-only lane:
  `/home/williambenitez1/Capstone_worktrees/1.5_feat__qwen3-vl-8b-instruct__v017b-doctrine-iteration/docs/prompt-lab/qwen-v017b-doctrine-iteration/cycle_001/`
- The cycle used temporary `doctrine.yaml` swaps and restored the baseline
  doctrine checksum after each run.
- Baseline fixed-`v017b` doctrine replay on
  `human_report_challenge_v2_dev_55_no101`: `74` matches, `32` false
  negatives, `15` false positives, `0.7000` average assessment score.
- Best assessment-only signal: `d001_visual_pda_scope` preserved `74/32/15`
  while slightly improving average assessment to `0.7014`.
- Best recall signals: `d008_exterior_building_guard`,
  `d011_best_assess_plus_detect`, and `d013_recall_repair_blend` reached
  `75` matches and `31` false negatives, but all increased false positives to
  `16` and reduced average assessment quality.
- Best precision/assessment signal: `d014_dense_case_blend` reduced false
  positives to `14` and improved average assessment to `0.7073`, but lost
  recall at `73` matches and `33` false negatives.
- Positive `155` passed in every run, and no recovery events affected trusted
  results.
- Decision: keep baseline doctrine unchanged. The doctrine candidates are
  useful learning evidence, not adoption candidates; `v017b_group_box_rejection`
  remains the accepted prompt-only parked candidate.

### 2026-05-04 - v018 Upstream/v017b Amalgamation Cycle Closed With No Adoption

- Ran the worktree-only v018 upstream/v017b amalgamation cycle under the
  existing v017b main-promotion evidence lane:
  `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/upstream_v017b_amalgamation_cycle/`
- The cycle tested five detect-only prompt candidates on
  `human_report_challenge_v2_all_current_117_no101` plus the separate
  `office-negative` guard using current `upstream/main` code through Ollama's
  OpenAI-compatible endpoint.
- Baselines preserved for interpretation:
  - upstream prompt-controlled row: `169` matches, `50` false negatives,
    `24` false positives, but positive `155` failed
  - parked `v017b` local Qwen row: `165` matches, `54` false negatives,
    `22` raw false positives / `21` effective extra-target false positives,
    with `155`, `166`, and office-negative passing
  - `v017b` upstream-code compatibility row: `166` matches,
    `53` false negatives, `26` false positives, with controls passing
- v018 results:
  - `v018d_evidence_budget_pruner`: `180` matches, `39` false negatives,
    `39` false positives; controls passed
  - `v018b_compressed_v017b`: `178` matches, `41` false negatives,
    `36` false positives; controls passed
  - `v018c_upstream_first_precision_audit`: `175` matches,
    `44` false negatives, `43` false positives; controls passed
  - `v018a_upstream_plus_control_guard`: `174` matches,
    `45` false negatives, `40` false positives; controls passed
  - `v018e_contrastive_body_anchor`: `173` matches,
    `46` false negatives, `29` false positives; controls passed
- Decision:
  - no v018 prompt should be promoted as-is
  - `v018d` is the recall-ceiling learning signal, not an adoption candidate
  - `v018e` is the best precision-balanced follow-up axis, but still exceeds
    the false-positive ceiling
  - keep `v017b_group_box_rejection` parked as the accepted prompt-only main
    candidate
- Next technical step: focused visual review of `v018e` false positives and
  `v018d` recall wins, then author one narrower follow-up that keeps v018e's
  contrastive/body-anchor discipline while selectively importing v018d's
  evidence-budget recall behavior.
- Boundaries: no source reports, references, doctrine, runtime config,
  prompt-overlays, runner outputs, commits, pushes, PRs, source truth, or
  promotion state were changed by this closeout.
