# Superpowers Workflow Reassessment

Status: `workflow_reassessment_complete`

## What Superpowers Changes

The current automation process should not become "run prompts until one wins."
Superpowers improves the loop by making each phase explicit:

- use `brainstorming` when choosing a new prompt axis or changing cycle shape
- use `writing-plans` when the next run needs a decision-complete execution
  plan
- use `executing-plans` only after the user approves the plan
- use `using-git-worktrees` to keep prompt artifacts in the Qwen `1.2`
  worktree and keep main as source evidence
- use `systematic-debugging` after a failure, near miss, contradiction, or
  surprising gate outcome
- use `dispatching-parallel-agents` for independent read-only sidecar review
  when it materially improves the decision
- reserve `subagent-driven-development` for later waves that explicitly grant
  disjoint write scopes
- use `verification-before-completion` before claiming a package, candidate, or
  closeout is complete

Superpowers remains workflow scaffolding. It is not source truth, promotion
authority, a Mem0 writer, an MCP router, or permission to bypass the
`human_report_challenge_v2` gates.

## What The v017a Near Miss Teaches

`v017a` produced useful signal and should not be discarded casually:

- it preserved the corrected v2 positive control `155`
- it passed the separate office-negative abstention guard
- it suppressed the row-fragment pattern on `101`
- it stayed within the v2 aggregate hinge near-miss band

But it still failed the manual diagnostic because the model accepted a broad
group/scene box as one military-equipment detection. That is enough to stop the
cycle. The next prompt attempt should be based on a failure diagnosis, not on a
generic "try another wording" reflex.

## Updated Cycle Recommendation

Add this required step after every failed or near-miss prompt candidate:

```text
run result -> source-artifact diagnosis -> one-axis recommendation -> user review -> next prompt plan
```

The diagnosis should record:

- the gate that failed
- the exact case or slice that caused the stop
- what improved and must be preserved
- what failed and must be targeted
- whether the failure is prompt-addressable, evaluation-shape related, or out
  of scope
- whether research or sidecar review is justified before another prompt

## Sidecar Subagent Use

Sidecars are useful only when the work can stay read-only and independent:

- `prompt-engineer`: critique whether the next axis is actually distinct from
  the failed axis
- `reviewer`: check gate logic, source citations, and scope boundaries
- `knowledge-synthesizer`: compress multiple candidate results into a user
  decision packet
- `research-analyst`: use only after repeated failures or a concrete
  source-backed prompt-method question

No sidecar should mutate files unless a later approved wave assigns a disjoint
write scope.

## Policy Patch Recommendation

Do not edit `cycle_policy.json` in this reassessment wave. If the user approves
the new workflow after review, a later small policy patch should encode:

- near-miss diagnosis is required before next prompt authoring
- one-axis recommendation is required before `v017b`
- sidecars are read-only by default
- research is conditional, not routine
- `v017b` remains user-gated

## Current Stop Rule

Stop here. Do not author prompt text, create an overlay, create a runner
session, run VLM inference, run dev, run holdout, run all-112, change runtime
config, change MCP config, write Mem0, or refresh Graphify as part of this
package.
