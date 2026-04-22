# Prompt Crafting Instructional Guide

## Purpose And Audience

This document is a teaching-grade guide for how we refined the current Qwen
prompt stack from a clean branch-aware baseline to the promoted `v009`
candidate.

It is written for a reader who may be:

- working manually without automation help
- using AI as optional support
- learning how to run a disciplined prompt workflow instead of making ad hoc
  prompt edits

This guide is manual-first and AI-optional. The goal is to explain the method
well enough that a careful person could reproduce it alone, while still making
it easy to use an assistant for speed.

This guide stops at branch promotion into tracked config. It does not treat
GitHub PR workflow as part of the core prompt-crafting method.

## AI Support Overlay

This guide is still manual-first and AI-optional, but the current local
workflow now sits on top of a stronger global Codex support layer in:

- `/home/williambenitez1/.codex/AGENTS.md`
- `/home/williambenitez1/.codex/MCP_USAGE_GUIDE.md`
- `/home/williambenitez1/.codex/agents/VENDOR_MANIFEST.md`

Practical rule:

- use MCP and source-specific connectors when they are the right fit, not as a
  reflex
- treat installed custom agents as optional specialists, not default
  participants in every prompt task
- use `sequentialthinking` before substantive updates to live maintained docs,
  global rules, or any `AGENTS.md`

Teaching implication:

- better AI tooling can speed research, synthesis, planning, and specialist
  support
- it still does not replace the need for a clean evidence hub, repeated runs,
  clear promotion gates, and code-to-doc verification

## Capability Map Before Repo Specifics

A serious prompt workflow needs more than a text editor and one lucky example.
It needs a set of capabilities that work together.

### 1. A Canonical Evidence And Reference Hub

You need one place to store:

- doctrine and requirements
- model-specific prompting references
- run manifests
- version notes
- sweep summaries
- critique notes
- winner notes

Why this matters:

- prompt work becomes unexplainable very quickly if the evidence trail is
  scattered across chat logs, screenshots, and memory
- when someone asks "why did we believe this version?", you need an answer that
  survives more than one day

In this repo, that role is filled by:

- `z_reference_docs/`

But the general lesson is broader:

- any repo doing this well needs a centralized local evidence/docs hub, even if
  it is named something else

### 2. A Stable Runtime Inference System

You need a reliable way to generate outputs from the current prompts against
real images or inputs.

Why this matters:

- prompt work is about behavior, not wording in the abstract
- if you cannot run the system repeatedly, you cannot tell whether a change is
  an improvement, a regression, or random variance

In this repo, that role is filled by:

- `bda-svc`

More specifically, the active runtime contract lives in:

- `src/bda_svc/pipeline/config.yaml`
- `src/bda_svc/pipeline/model.py`
- `src/bda_svc/pipeline/interfaces.py`
- `src/bda_svc/pipeline/doctrine.yaml`

But the general lesson is:

- any prompt workflow needs a stable runtime inference layer whose contract is
  treated as real engineering surface, not as disposable scaffolding

### 3. An Evaluation And Visual Review Layer

You need a way to compare outputs, especially when the task involves structure,
grounding, or localization.

Why this matters:

- raw JSON or plain text is often not enough to explain why one candidate is
  better than another
- localization work in particular needs visual review artifacts like overlays,
  crops, or side-by-side comparison sheets

In this repo, that role is filled by:

- `bda_eval`

But the general lesson is:

- any serious prompt workflow benefits from an evaluation/comparison layer that
  can turn raw outputs into reviewable evidence

### 4. A Controlled Experiment Workspace

You need a place to run candidates without confusing experimental work with the
stable baseline.

Why this matters:

- prompt versions need names, baselines, manifests, and repeated runs
- changing the live config directly makes it hard to tell what really happened

In this repo, that role is filled by:

- numbered prompt labs under `z_reference_docs/Prompt_Labs/`
- dedicated branches and worktrees

General lesson:

- prompt work needs controlled experiment space, even if the exact folder or
  branch structure differs

### 5. A Promotion Target

You need a final place where accepted prompt changes land after they earn it.

Why this matters:

- if the winning prompt never moves into tracked branch state, it stays a lab
  curiosity rather than becoming real project progress

In this repo, that role is filled by:

- tracked branch config in `src/bda_svc/pipeline/config.yaml`

General lesson:

- any prompt workflow needs a clear difference between:
  - local evidence and experimentation
  - accepted tracked branch state

## Core Philosophy

This workflow is built on a few rules that matter more than any specific
wording trick.

### Prompt Work Is Evidence-Driven

We do not treat prompt drafting as creative writing. We treat it as behavioral
engineering backed by evidence.

That means:

- a prompt change is interesting only if it changes behavior
- a behavior change is useful only if we can inspect and explain it
- an apparent improvement is not a real win until it survives repetition and
  broader validation

### One Prompt Surface At A Time When Possible

The active runtime here has three main prompt surfaces:

- `detect_objects`
- `assess_damage`
- `summarize_scene`

When one run improves and another regresses, debugging becomes much easier if
only one surface changed.

That is why the clean branch-aware line moved in phases:

- detection cycle
- assessment cycle
- summary cycle

### Seed Cases Matter, But They Are Not Enough

We used the tank pressure image as a pressure test because it exposed a real
grounding problem. That was useful.

But the process changed once the question became:

- are we improving the grounding rule, or only making one image look better?

That is why generalization sweeps and negative-scene controls became promotion
gates instead of optional extras.

### Promotion Requires Repeatability

A single impressive run is not enough.

The working rule is:

- first get a candidate
- then repeat it unchanged
- then test it outside the seed case
- then package it into a unified version
- only then promote it into tracked branch config

### Local Evidence And Tracked Config Have Different Jobs

The local evidence hub is where we keep:

- references
- artifacts
- critiques
- sweeps
- teaching notes

Tracked branch config is where we keep:

- the accepted candidate state that is serious enough to review as code

You need both. One does not replace the other.

### Green CI And Full Prompt-Lab Parity Are Different Guarantees

This matters enough to name directly.

Green CI usually means:

- the branch builds
- tests passed
- basic runtime health checks passed

That is important, but it does **not** automatically mean:

- every active worktree can run the local prompt-lab smoke loop
- every model branch is a reusable experimental root
- the exact local winner behavior has been re-proven after a refresh

The broader lesson is:

- CI health is one validation lane
- local prompt-lab parity is another
- strong workflow docs should explain both instead of mixing them together

## Repo And Workspace Setup

This repo now uses a structure designed to keep the clean baseline separate
from experimental work.

### Clean `main`

`main` is meant to stay a boring mirror of `upstream/main`.

Why that matters:

- prompt work should not happen on the mirrored baseline
- upstream syncs are safer when `main` is intentionally boring

### Model And Feature Branches

The active line here uses:

- model branch:
  - `model/qwen3-vl-8b-instruct`
- feature branch:
  - `feat/qwen3-vl-8b-instruct/two-pass-refinement`

Why that matters:

- model-level differences and task-level experiments are not the same thing
- feature work should stay narrow and reviewable
- model branches are not meant to be ancestry placeholders only
- if a model branch is going to parent future feature branches, it should stay
  capable of running the same minimal evidence loop those future branches will
  depend on

### Worktrees

Active code work happens in worktrees instead of by repeatedly switching one
checkout.

Current examples:

- `/home/williambenitez1/Capstone_worktrees/1_model__qwen3-vl-8b-instruct`
- `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement`

Why that matters:

- no branch-switching collisions
- cleaner mental separation between clean baseline and active work
- upstream refreshes become much easier to reason about
- but only if we distinguish:
  - a safe rebase
  - a validated branch
  - a fully parity-checked branch line

### Refresh Workflow As A Separate Capability

Once a repo starts using long-lived model and feature worktrees, it also needs
an explicit refresh workflow.

Why that matters:

- upstream sync safety is not the same thing as prompt correctness
- a clean rebase does not automatically prove that every active worktree is
  still usable for experiments
- if the workflow does not define what “done” means after a refresh, teams tend
  to stop too early

In this repo, that role is filled by:

- `z_reference_docs/GIT_WORKTREE_UPDATE_WORKFLOW.md`
- model-line-specific checklists such as:
  - `z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_QWEN.md`
  - `z_reference_docs/GIT_WORKTREE_UPDATE_CHECKLIST_GEMMA.md`

General lesson:

- any prompt workflow using multiple long-lived worktrees should define three
  separate ideas:
  - refresh success
  - validation success
  - full prompt-lab parity completion

### Centralized Docs And Evidence Hub

The canonical local docs/evidence path stays at:

- `/home/williambenitez1/Capstone/z_reference_docs`

Why that matters:

- worktrees can change, but the evidence hub stays stable
- everyone knows where the authoritative local artifacts live

### Numbered Prompt Labs

The active branch-aware lab is:

- `z_reference_docs/Prompt_Labs/1_qwen3-vl-8b-instruct/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/`

Why the numbering helps:

- model lines scan cleanly
- feature lines tie back visually to their parent model line
- the folder names are easy to sort and compare at a glance

## Source Hierarchy And Grounding Rules

The workflow used a clear source hierarchy to keep prompt edits defensible.

### 1. Runtime Contract First

Before any prompt idea matters, the runtime has to support it.

That means checking:

- placeholders
- schemas
- bbox conventions
- output structure
- model call behavior

If an idea needs the runtime contract to change, it is no longer a prompt-only
change.

### 2. Doctrine Second

Doctrine defines what the outputs should mean.

For this project, doctrine was the authority for:

- damage-category meaning
- confidence semantics
- what visible evidence can support
- where phrasing drifts into unsupported claims

### 3. Model-Specific Guidance Third

Model docs help answer:

- how the model tends to respond
- what kinds of examples or structure help it
- what styles tend to overreach or underperform

### 4. General Prompting Guidance Fourth

General prompting guidance is useful, but only after:

- runtime fit
- doctrine fit
- model fit

### 5. Observed Behavior Last, But Decisive

If theory says a prompt should work but real runs show otherwise, the real runs
win.

That does not mean we abandon theory. It means theory must survive contact with
the actual runtime.

## The Actual Prompt-Crafting Workflow

This is the core operating loop that produced the current branch-aware winner.

### Step 1. Establish A Fresh Branch-Aware Baseline

We first rebuilt a fresh `v000` from clean mirrored `main` at `28e863b`.

Why this mattered:

- older preserved main-branch history existed, but it was tied to a different
  baseline state
- new work needed a clean, branch-aware anchor

### Step 2. Snapshot The Baseline

The baseline was recorded in the active lab so later candidates could be judged
against something concrete instead of memory.

Why this mattered:

- if the baseline is not preserved, later comparisons get fuzzy

### Step 3. Choose A Pressure-Test Seed Case

We used the tank pressure image because it made the grounding problem obvious.

Why this mattered:

- a hard seed case gives the first clear signal for whether a new idea is worth
  following

### Step 4. Run A Candidate

Each candidate lived as a versioned snapshot and a run folder with artifacts.

Why this mattered:

- prompt versions need durable names and durable outputs

### Step 5. Critique What Changed

After each run, the right question was not just:

- "is this better?"

It was:

- what moved?
- what held?
- what regressed?
- which prompt surface is actually responsible?

### Step 6. Decide Which Surface Owns The Problem

In this repo, the three surfaces serve different jobs:

- detection handles target identification and localization
- assessment handles damage/confidence/logic
- summary handles scene-level wording

Why this mattered:

- once the problem is assigned to the right surface, the next iteration becomes
  much more targeted

### Step 7. Revise Only The Active Surface

This is how the clean branch-aware line avoided random drift.

Examples:

- `v005` and `v006` were detect-only
- `v007` and `v008` were assess-only
- `v004` was summary-only

### Step 8. Repeat Until A Surface-Level Leader Is Confirmed

We did not stop at first success. We repeated winning candidates unchanged to
separate real improvement from lucky variance.

## Why The Three Major Capabilities Mattered Here

This project’s success was not just about clever wording. It depended on three
capabilities working together.

### The Evidence Hub

In general, prompt work needed:

- a place to preserve references
- a place to store run manifests
- a place to keep critique notes and winner notes
- a place to record why a version was accepted or rejected

In this repo, that was:

- `z_reference_docs`

Without that hub:

- the process would have turned into disconnected runs with no durable chain of
  reasoning

### The Runtime Inference Layer

In general, prompt work needed:

- a stable way to produce outputs from the current prompt stack
- repeatable runs against real inputs
- enough contract stability that changes in behavior could be interpreted

In this repo, that was:

- `bda-svc`

Without that layer:

- we would have had prompt text, but no reliable system for observing what it
  actually did

### The Evaluation And Review Layer

In general, prompt work needed:

- a comparison layer
- overlays and crops for bbox review
- a way to compare baseline and candidate outputs side by side

In this repo, that was:

- `bda_eval`

Without that layer:

- the grounding work would have depended too much on raw JSON and ad hoc
  interpretation

## Visual Review And Artifact Workflow

The visual review flow on the clean branch-aware line became:

1. run the runtime pipeline to produce baseline and candidate reports
2. run the evaluation layer on those reports plus the source image folder
3. inspect overlays, crops, and `bbox_review_sheet.jpg`

Why this mattered:

- it anchored review in tracked evaluation functionality instead of temporary
  local-only debug helpers

### Why Tracked Evaluation Was Better Than Ad Hoc Debug Export

Temporary debug helpers are useful for diagnosis, but they are fragile as the
main workflow.

Tracked evaluation is better because:

- it is reviewable
- it can be tested
- it survives promotion into branch state
- it creates a reusable process instead of a one-off tool

### When Copied Evaluation Images Are Acceptable

This workflow also allowed copying images from:

- `z_reference_docs/Data_set_Storage/`

into per-run output folders.

Why that is acceptable:

- those copied images become part of the saved artifact set for that run
- they preserve exactly what was reviewed

General lesson:

- it is reasonable to copy evaluation inputs into run folders when doing so
  improves traceability and review clarity

## Generalization And Promotion Gates

This is where the workflow became disciplined instead of merely interesting.

### Mixed-Pack Validation

The seed case was not enough, so later detect-only changes were judged against
the mixed grounding pack.

That pack intentionally included:

- another destroyed tank
- an operational tank
- destroyed and operational building controls
- a negative office scene

### Negative-Scene Control

The office scene mattered because it answered:

- are we improving detection, or just broadening it until it hallucinates?

This is what killed `v005` as a winner even though it taught a valuable lesson
about building separation.

### Repeat Runs

Candidates had to repeat cleanly.

That is what turned:

- `v006` into a confirmed detect leader
- `v008` into a confirmed assess leader
- `v004` into a confirmed summary leader

### Frozen-Stack Sweep

Once the surfaces had confirmed leaders, they were frozen together and judged
as a stack.

Why this mattered:

- sometimes individually good surfaces interact badly when combined

### Unified Version Packaging

After the frozen stack held, it was packaged into:

- `v009_unified_best-stack.yaml`

Why this mattered:

- reviewers should not have to reconstruct the winner from multiple old files

### Promotion Into Tracked Branch Config

Only after the stack survived:

- focused confirmation
- mixed-pack validation
- extra hard-case comparisons
- a 10-image blind-style sweep

did it move into tracked branch config.

That is the line between:

- interesting local experiments
- the active tracked working config for the model line

## Worked Example: `v000` To `v009`

This is the shortest faithful story of how the current winner emerged.

### `v000`

Fresh branch-aware baseline from clean mirrored `main` at `28e863b`.

Why it mattered:

- it reset the active evidence chain onto the clean branch-aware line

### `v001`

The first real bbox jump.

Why it mattered:

- it showed there was real detection upside available
- it also showed that a better-looking box could come with downstream drift

Lesson:

- bbox wins cannot be judged in isolation

### `v003`

Recovered `DESTROYED / PROBABLE` while holding the stronger detection behavior.

Why it mattered:

- it proved the improved detection behavior was not inherently tied to
  `CONFIRMED` inflation

Lesson:

- once detection improves, the next problem may be assessment calibration, not
  detection itself

### `v004`

Improved the summary without destabilizing detection or assessment.

Why it mattered:

- it showed the remaining overreach had moved into the summary surface

Lesson:

- once one surface is stable, isolate the next surface instead of changing
  everything again

### `v005`

Recovered multi-target building separation but hallucinated the office negative
scene.

Why it mattered:

- it taught the right building-separation lesson
- it also proved that a partial win can still be unsafe

Lesson:

- keep the useful rule, reject the unsafe package

### `v006`

Preserved the separation win and restored the negative-scene guard.

Why it mattered:

- it became the confirmed detect-only leader

Lesson:

- the best detection changes are the ones that generalize and repeat

### `v008`

Preserved the operational firing-signature fix and removed destroyed-case logic
overreach.

Why it mattered:

- it became the confirmed assess-only leader

Lesson:

- downstream fixes must preserve the good detect behavior while tightening logic
  discipline

### `v009`

Packaged:

- `v006` detect
- `v008` assess
- `v004` summary

Why it mattered:

- it became the single explicit winner version
- it then moved into tracked feature-branch config

Lesson:

- promotion should follow confirmed surface leaders, not precede them

## Common Failure Patterns And How To React

### Seed-Case-Only Overfitting

Symptom:

- the seed image improves, but broader behavior gets worse

Response:

- move quickly to mixed-pack validation

### Negative-Scene Hallucination

Symptom:

- the model starts treating interiors, walls, or clutter as doctrinal targets

Response:

- add explicit non-target guards and retest negative scenes immediately

### Subtype Drift

Symptom:

- the model invents a more specific target identity than the evidence supports

Response:

- tighten detection and logic wording back toward visible evidence and allowed
  categories

### Confidence Drift

Symptom:

- the model upgrades to `CONFIRMED` too easily

Response:

- fix assessment wording before touching summary or detection again

### Logic And Category Mismatch

Symptom:

- the category says one thing but the supporting logic sounds more catastrophic
  or more cautious than the label

Response:

- keep the useful classification only if the supporting logic can be brought
  back into alignment

### Bbox "Improvement" That Hurts Multi-Target Separation

Symptom:

- one object looks better, but two-object scenes collapse into one target

Response:

- treat this as a regression even if the seed image looks nicer

### CI Green But Prompt Behavior Not Fully Enforced

Symptom:

- the branch is healthy, but CI is not proving exact winner parity

Response:

- be explicit about what CI proves and what the prompt-lab evidence proves

## Reproducible Operating Checklist

Use this as the compact version of the workflow.

1. Start from a clean branch-aware baseline, not a fuzzy inherited state.
2. Snapshot that baseline as `v000`.
3. Pick one hard seed case that exposes the problem clearly.
4. Run one candidate and record the outputs.
5. Critique the result in terms of what moved, held, and regressed.
6. Assign the problem to the right prompt surface.
7. Change only that surface when possible.
8. Repeat the candidate unchanged before trusting it.
9. Move promising detection changes to a mixed validation pack quickly.
10. Keep a negative-scene control in the promotion gate.
11. Once surface leaders exist, freeze them together and sweep the combined
    stack.
12. Package the combined winner as one explicit unified version.
13. Promote the winner into tracked branch config only after it has earned it.
14. Keep the evidence hub, runtime outputs, and review artifacts synchronized so
    the work stays explainable.

## Final Operating Principle

The most important thing to copy from this workflow is not any one sentence of
prompt text. It is the structure:

- stable runtime
- centralized evidence
- reviewable artifacts
- one-surface-at-a-time iteration
- broader validation before promotion

That structure is what made `v009` believable.
