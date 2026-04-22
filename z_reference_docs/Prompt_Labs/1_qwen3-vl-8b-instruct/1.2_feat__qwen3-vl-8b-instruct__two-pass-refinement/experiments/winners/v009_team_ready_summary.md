# `v009` Team-Ready Summary

## Current Working Config

The active working prompt stack for this branch-aware Qwen line is:

- `detect_objects` from `v006`
- `assess_damage` from `v008`
- `summarize_scene` from `v004`

This combined stack is formalized as:

- `experiments/versions/v009_unified_best-stack.yaml`

## Why This Is More Than A Quick Mockup

Evidence collected so far:

1. Seed-case confirmation
   - the stack was first validated on the hard tank pressure case
   - detection, assessment, and summary behavior were each separately improved
     and then recombined
2. Focused unified-stack confirmation
   - direct `v009` run matched the expected inherited behavior on:
     - `tank_pressure`
     - `operational_tank4`
     - `destroyed_building4`
3. Additional challenge set
   - three extra images showed:
     - preserved multi-object building recall
     - no smoke/fire truck regression
     - preserved complex-scene building separation
4. Broader blind-style sweep
   - 10 additional images across buildings, tanks, and trucks
   - `10 / 10` preserved target-count recall
   - `6 / 10` preserved the same damage/confidence structure
   - only `2 / 10` changed damage category at all

## Strongest Honest Claim

We can say:

- the stack generalizes beyond the original tank seed case
- the strongest gains are in:
  - preserved recall
  - cleaner doctrinal wording
  - better negative-scene discipline
  - more stable cross-image behavior

## Caveats To Keep Visible

Two blind-sweep cases still deserve explicit review:

- `destroyed_building5`
  - likely a real `v009` building-severity overcall
- `destroyed_tank37`
  - bbox is cleaner under `v009`
  - `DAMAGED` is arguable under smoke/angle obscuration
  - but the current `v009` supporting logic is still too catastrophic for a
    clean `DAMAGED` read

These are category-calibration watch cases, not recall failures.

## Branch Promotion State

The feature branch now preserves the current reviewable state in tracked
history:

- `566892a` — `Add prompt-lab review artifacts to bda_eval`
- `127051a` — `Promote v009 prompt stack into pipeline config`
- `ebeae30` — `Install workspace packages in CI`

So the review workflow, the promoted branch config, and the CI fix are now all
preserved in tracked branch history.
