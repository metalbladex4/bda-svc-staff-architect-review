# Superpowers Adoption For Human Report Challenge v2 Prompt Iteration

Status: `active_workflow_scaffolding`

This note records how the global `obra/superpowers` skill pack should be used
inside the Qwen `1.2` `human_report_challenge_v2` prompt-iteration lane.

The lane-level operating contract is:

- `../cycle_controller_operating_contract.md`

## Installed Surface

- Clone: `/home/williambenitez1/.codex/superpowers`
- Discovery symlink: `/home/williambenitez1/.agents/skills/superpowers`
- Release: `v5.0.7`
- Commit: `1f20bef3f59b85ad7b52718f822e37c4478a3ff5`
- Active surface: skills only
- Not active: Superpowers hooks, MCP servers, agents, or deprecated command
  wrappers

## Capstone-Adapted Rule

Use Superpowers as workflow scaffolding. It can make the prompt cycle more
disciplined, but it is not source truth, promotion authority, or permission to
run the next candidate.

Existing Capstone rules still govern:

- source artifacts, eval outputs, runner artifacts, and human review are
  authoritative
- Graphify/project-brain is navigation memory, verified against source
  artifacts
- Mem0 is manual/advisory and requires explicit write/delete approval
- MCPfinder is discovery-only and cannot install candidates without approval
- NCP remains deferred
- `v017a_body_backed_candidate_filter` remains a near miss pending user review
- do not author or run `v017b` until the user approves that next wave

## Skill Mapping For This Lane

| Superpowers skill | Capstone prompt-cycle use |
| --- | --- |
| `brainstorming` | Shape a candidate axis or cycle design before prompt authoring. |
| `writing-plans` | Produce decision-complete prompt-run plans after the axis is approved. |
| `systematic-debugging` | Diagnose gate failures before proposing the next prompt change. |
| `dispatching-parallel-agents` | Run bounded read-only sidecar critique, research, review, and synthesis tasks when independent. |
| `subagent-driven-development` | Use only for approved implementation waves with disjoint write scopes; not for routine prompt runs. |
| `using-git-worktrees` | Reinforce the existing rule that prompt work stays in active worktrees, not the clean main checkout. |
| `verification-before-completion` | Require fresh command/artifact evidence before claiming a run, install, or docs update passed. |
| `writing-skills` | Future option for a Capstone-specific prompt-cycle skill, only after a separate approval. |

## Current Pause Point

The first live v2 automation candidate, `v017a_body_backed_candidate_filter`,
is not user-reviewed and is not a winner. It passed changed-source sanity,
positive `155`, legacy `office-negative`, and aggregate hinge checks, but
failed case `101` by emitting one broad group/scene box:

```text
[75, 13, 1000, 571]
```

Next action is user review of `v017a`, not automatic `v017b` authoring.
