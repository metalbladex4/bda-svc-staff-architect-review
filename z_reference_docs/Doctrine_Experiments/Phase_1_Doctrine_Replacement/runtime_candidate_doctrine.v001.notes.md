# Runtime Candidate Doctrine `v001` Notes

This note explains why `runtime_candidate_doctrine.v001.yaml` differs from the
live doctrine snapshot.

## High-Level Intent

`v001` is a **Phase-1 PDA-only, visual-only-adapted** rewrite.

It is not trying to become a complete doctrine digest. It is trying to become a
better prompt-facing runtime doctrine file for the current pipeline.

## Main Differences From Live Doctrine

### Buildings

- keeps the existing five PDA bands
- keeps framed-building versus load-bearing logic
- keeps multistory / wing / section logic
- adds explicit visible-only language
- translates section-versus-whole-building reporting into wording that is safer
  for a selected-target runtime
- explicitly blocks drift into interior damage, recuperation, and FDA

### Military Equipment

- keeps the existing three PDA labels
- keeps the target-family scope
- removes the `K-kill` shorthand from the runtime-facing definitions
- removes the all-source `NO DAMAGE` note about movement / radio traffic
- rewrites the considerations around visible exterior evidence only

### Detection Guidance

- kept mostly stable
- slightly cleaned for wording and consistency
- still treated as operational prompt support, not as the same thing as PDA
  doctrine

## Expected Benefits

- less doctrinal noise that conflicts with a visual-only runtime
- fewer prompt collisions with the current “no kill-state labels” discipline
- cleaner building reasoning for multistory / partial-collapse cases
- safer military-equipment reasoning that does not rely on unseen cues

## Known Tradeoff

The candidate is intentionally less literal in a few places than the source
handbooks, because the goal is a doctrine-faithful runtime artifact, not a
verbatim doctrinal transcript dropped into a prompt.
