# Critique

## Comparison Against Fixed `v004` Reference

`v005` was designed as a detect-only follow-up to the mixed-sweep read. The
goal was to preserve the useful connected-body rule while adding explicit
multi-target separation guidance and a more generic non-burning target rule.

The result is mixed:

- improvement:
  - `destroyed_building4` now returns two separate building detections instead
    of collapsing the scene into one target
  - ground-truth clarification confirms that this is the correct outcome for
    that image because it contains two different buildings
- stable:
  - `tank_pressure`
  - `destroyed_tank15`
  - `operational_building7`
  - `operational_tank4` stayed unchanged from the fixed `v004` reference
- regression:
  - `office_negative` becomes a full-frame `buildings` false positive

## What Improved

- The explicit “do not merge neighboring targets” rule helped on the
  multi-target destroyed-building scene.
- The result suggests that target-separation wording is a real missing lever in
  the current detect prompt family.
- This is now stronger than a tentative signal: on `destroyed_building4`, the
  separation behavior is the correct behavior.

## What Regressed

- The broadened “box intact or operational targets even without damage cues”
  wording appears to have widened the detection prior too far.
- The negative office scene shows that the model can now interpret an entire
  indoor scene as a doctrinal building target.

## What This Means

`v005` is not safe to promote.

But it does give us a reusable lesson:

- keep the neighboring-target separation idea
- add a much stronger explicit non-target / indoor-scene guard before reusing
  it

## Research Questions

1. What is the shortest negative example or guardrail that suppresses indoor
   false positives without undoing the recovered building separation?
2. How should the detect prompt distinguish doctrinal building targets from
   ordinary interior walls, rooms, or office partitions?
3. Can we preserve building-scene target separation while narrowing the
   prompt’s “intact target” rule back toward the more conservative `v004`
   prior?

## Decision

- `partial reuse only`
- keep the multi-target separation lesson
- reject the broadened intact-target wording as written
