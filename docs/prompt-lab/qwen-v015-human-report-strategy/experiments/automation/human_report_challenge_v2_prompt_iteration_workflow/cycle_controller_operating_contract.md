# Cycle Controller Operating Contract

Status: `active_workflow_scaffolding`

This contract defines how the Qwen `1.2` `human_report_challenge_v2`
prompt-iteration lane uses the global `obra/superpowers` skill pack. It is a
workflow discipline layer only. It does not authorize promotion, source-truth
mutation, or tool installation.

## Authority Order

1. Explicit user approval and current project instructions.
2. Source artifacts, runner outputs, eval summaries, gate summaries, and human
   review notes.
3. Capstone live docs, trusted project-brain notes, and Graphify recall, verified
   against source artifacts.
4. Superpowers skills as workflow scaffolding.
5. Mem0 advisory memory and other non-source recall.

Superpowers is never source truth, promotion authority, an MCP router, a Mem0
writer, an MCPfinder installer, or permission to bypass prompt/eval gates.

## Superpowers Skill Use

Use Superpowers skills at these cycle checkpoints:

| Checkpoint | Skill | Required behavior |
| --- | --- | --- |
| New prompt-axis or cycle design | `brainstorming` | Shape the axis, constraints, tradeoffs, and user decision points before authoring prompt text. |
| Approved multi-step prompt run | `writing-plans` | Produce a decision-complete run plan with files, gates, stop rules, and validation commands. |
| Existing approved plan execution | `executing-plans` | Execute the plan task-by-task, stopping on blockers or failed verification. |
| Worktree boundary setup or verification | `using-git-worktrees` | Keep prompt work in the active Qwen `1.2` worktree; do not use clean main for prompt artifacts. |
| Failed, near-miss, or contradictory result | `systematic-debugging` | Diagnose failure class before proposing the next prompt change. |
| Independent sidecar work | `dispatching-parallel-agents` | Use bounded read-only sidecars only when tasks are independent and materially useful. |
| Approved implementation with disjoint write scopes | `subagent-driven-development` | Use only after explicit approval assigns sidecar write scope; otherwise sidecars remain read-only. |
| Any success/completion claim | `verification-before-completion` | Run fresh validation and cite artifacts before claiming a candidate, docs update, or closeout passed. |

Do not use Superpowers as ritual overhead for routine file reads, one-line
checks, or validation-only summaries unless a skill materially improves the work.

## User-Gated Steps

The following actions always require explicit user approval:

- authoring or running a new prompt candidate after a pause point
- running dev, holdout, all-112, promotion, or runtime adoption checks
- changing gates, source truth, validation manifests, runtime config, MCP config,
  hooks, Mem0 writes/deletes beyond an approved closeout memory, or Graphify
  trusted-memory inputs
- installing, activating, importing, or removing tools or MCP servers
- giving any subagent write scope

## Sidecar Subagent Boundary

Main Codex remains the cycle owner and final decision-maker. Sidecar subagents
may be used for bounded read-only work such as prompt-axis critique, targeted
research, gate review, validation coverage review, or result synthesis. They
must not mutate files unless a later approved implementation wave assigns them
a disjoint write scope and validation gate.

## Evidence Before Candidate Status

Before claiming a candidate is a winner, near miss, failure, or ready for final
cycle review, the cycle controller must verify and cite:

- candidate overlay or prompt artifact path, if one was authored in that wave
- validation manifest paths used
- run output directory
- candidate manifest run summaries
- eval summaries and gate summaries
- manual review notes for diagnostic-only cases when they are intentionally run
- checks proving no forbidden dev, holdout, all-112, promotion, runtime config,
  MCP config, hook, source-truth, or tool-install side effect occurred

Graphify/project-brain may help navigate these artifacts, but claims must be
verified against the source artifacts themselves.

## Current Cycle State

`v017a_body_backed_candidate_filter` is the first live
`human_report_challenge_v2` automation candidate. It is a near miss, not a
winner. It passed changed-source sanity, positive `155`, legacy
`office-negative`, and aggregate hinge checks, but failed the manual case `101`
diagnostic by emitting one broad military-equipment group/scene box:

```text
[75, 13, 1000, 571]
```

The user approved a bounded continuation to
`v017b_single_target_box_span_self_filter`. That approval is narrow:

- author one `v017b` prompt overlay and hypothesis in the active Qwen `1.2`
  worktree
- run only the `human_report_challenge_v2` hinge pack, changed-source sanity
  pack, updated-report smoke pack, and separate `office-negative` abstention
  guard
- generate gate and decision artifacts for review
- stop before dev, holdout, all-112, promotion, runtime config adoption,
  structural guard implementation, source-truth mutation, MCP config changes,
  hook edits, or tool installs

`v017b` is an old-gate near miss. Its case `101` result remains useful as
manual diagnostic evidence, but case `101` is no longer a forward pass/fail
gate. Future candidates must pass the active `human_report_challenge_v2`
`hinge_11_no101` pack, changed-source sanity, updated-report smoke, the
separate `office-negative` abstention guard, and the hard-stop boundaries before
any wider run.

## Latest Candidate Result

`v017b_single_target_box_span_self_filter` was authored and run under that
bounded approval. Under the old 12-case gate it was also a near miss, not a
winner.

It improved the aggregate hinge totals and preserved the main controls, but it
still failed the manual case `101` diagnostic with one broad group/scene box:

```text
[75, 58, 1000, 547]
```

The current state is therefore:

- `v017a`: near miss; broad case `101` box remained
- `v017b`: old-gate near miss; broad case `101` box remained, row fragments
  still suppressed
- case `101` is now diagnostic-only and excluded from forward pass/fail gates
- the active forward hinge pack is now
  `human_report_challenge_v2_hinge_11_no101`
- `v017c` through `v017f` may continue within the already approved cycle budget
  unless a hard stop triggers
- no dev, holdout, all-112, promotion, runtime adoption, source-truth mutation,
  structural guard implementation, MCP config change, hook edit, or tool install
  is authorized by the v017b result

Near-miss diagnosis remains mandatory before the next candidate, but it is not a
human approval gate inside the approved `v017a` through `v017f` cycle. Stop only
for abstention-guard failure, source/manifest integrity failure, scope violation,
runtime/tool-boundary violation, candidate budget exhaustion, or explicit user
stop.
