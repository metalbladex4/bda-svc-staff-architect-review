# v025a Case 67 Collapse Autopsy

Generated: `2026-05-07T02:06:00Z`

## Source Rows

| Candidate | Role | Case 67 M/FN/FP | Overall M/FN/FP/Errors |
| --- | --- | ---: | ---: |
| `v020c_anchor_replay` | incumbent | `9/2/4` | `186/33/25/58` |
| `v024l_v023s_no_wheel_track_ablation` | high-recall learning evidence | `9/2/3` | `188/31/35/66` |
| `v025a_v020c_compact_separate_body_recovery` | rejected candidate | `1/10/9` | `176/43/35/78` |

Case `67` source truth has 11 `military_equipment` references. `v024o` is not
used in this autopsy.

## Evaluation-Row Comparison

### v020c

- True positives: `target_1`, `target_2`, `target_3`, `target_4`, `target_5`,
  `target_6`, `target_7`, `target_9`, `target_11`
- False negatives: `target_8`, `target_10`
- False positives: predicted `target_0`, `target_1`, `target_9`, `target_11`

### v024l

- True positives: `target_1`, `target_2`, `target_3`, `target_4`, `target_6`,
  `target_7`, `target_8`, `target_9`, `target_11`
- False negatives: `target_5`, `target_10`
- False positives: predicted `target_0`, `target_1`, `target_10`

### v025a

- True positives: `target_11` only
- False negatives: `target_1`, `target_2`, `target_3`, `target_4`, `target_5`,
  `target_6`, `target_7`, `target_8`, `target_9`, `target_10`
- False positives: predicted `target_0`, `target_1`, `target_2`, `target_3`,
  `target_4`, `target_5`, `target_6`, `target_7`, `target_8`

## Which v020c Matches Disappeared?

Eight v020c true-positive matches disappeared in v025a:

```text
target_1, target_2, target_3, target_4, target_5, target_6, target_7, target_9
```

The only v020c/v025a shared true-positive reference is `target_11`, the large
rightmost vehicle.

## Which v025a FPs Appeared?

`v025a` emitted nine unmatched predictions on the row:

```text
target_0, target_1, target_2, target_3, target_4, target_5, target_6, target_7, target_8
```

The predicted boxes are visually arranged along the same row, but they are
shifted upward and left relative to the lower vehicle-body reference boxes.
They track rowline/top-edge/dust cues more than the reference body extents.

## FP Class Assessment

The v025a false positives are best classified as mixed dense-row fragment
failures:

- `nested_fragment_box`: the boxes act like top-edge or partial-body fragments
  of vehicles already represented by the reference row
- `context_only_smoke_debris_terrain`: several boxes appear anchored by dust,
  motion plume, and row context rather than enough body overlap
- `duplicate_same_body_box`: at the row level, the model is still enumerating
  nearby bodies, but the boxes no longer align with distinct full body centers

They are not primarily broad group boxes, building fragments, or unrelated
off-target objects.

## Under-Detection Or Over-Splitting?

Both.

`v025a` under-detected true objects because 10 of 11 references became FNs. It
also over-split row fragments because it still predicted 10 boxes, but only one
matched. The failure is not absence of detections; it is wrong dense-row
localization and fragment selection.

## Silhouette / Exterior-Boundary Behavior

`v024l` explicitly includes silhouette and exterior wall/roof boundary language
and preserves case `67` at `9/2/3`. `v020c` also preserves case `67` well at
`9/2/4` through its context-shadow and final-audit balance.

`v025a` did not preserve the stable visual behavior. Even though it kept the
v020c text and reused "visible body center" plus "visible body edge", the new
split-recovery sentence appears to redirect the dense row toward upper-edge and
row-context boxes instead of the lower visible body centers used by v020c.

## Did The Selection Rule Change?

The written rule did not remove "target body remains visible", but the behavior
changed in practice. The final audit now contained a positive split command:

```text
if one candidate spans two nearby targets, split
```

That appears to have changed the model's visual selection priority from
"candidate body remains visible after context is removed" to "find separate
nearby bodies to split." In a dust-obscured dense row, this led to aggressive
fragment/rowline selection.

## Most Likely Responsible Phrase

The most likely responsible phrase is:

```text
if one candidate spans two nearby targets, split
```

The risk was amplified by its placement inside `EXTRA-BOX AUDIT`, immediately
after a sentence about detections near other detections and strong context
cues. That made the final audit a split-recovery instruction rather than a
pure extra-box rejection instruction.

## Is This Local To Case 67?

No, but case `67` is the severe collapse.

| Case | v020c | v024l | v025a | Autopsy note |
| --- | ---: | ---: | ---: | --- |
| `66` | `8/0/4` | `8/0/6` | `8/0/6` | v025a picked up v024l-like nested-fragment FP burden. |
| `67` | `9/2/4` | `9/2/3` | `1/10/9` | hard collapse; dense-row body alignment failed. |
| `84` | `8/5/0` | `7/6/0` | `8/5/0` | unchanged from v020c. |
| `97` | `1/0/2` | `1/0/2` | `0/1/1` | lost the only match while reducing one FP. |

The collapse is strongest in `67`, but the same cue also reopened nested
fragment burden in `66` and caused a match loss in `97`.

## Decision

`v025a` is rejected. Do not branch from it. Do not branch from `v024l`.

Recommended next direction:

```text
D. Run a targeted replay/micro-ablation pack before all-current.
```

Rationale: the separate-body concept is now suspect. Before any future all-current
candidate, the next approved wave should use a small targeted pack around
`14`, `42`, `66`, `67`, `84`, `97`, `103`, `155`, `166`, `172`, and
office-negative to test whether placement/salience can be controlled. Do not
author another positive separate-body cue in the audit/final-balance region.
