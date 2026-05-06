# Case 67 Dense-Formation Diagnostic

Generated: `2026-05-03T23:57:07Z`

## Question

After `v017b_group_box_rejection` became the parked prompt-only main promotion
candidate, should case `67` change the candidate decision or trigger another
prompt attempt?

## Short Answer

No immediate candidate switch is justified. Case `67` is a real remaining
limitation, but it is not a `v017b`-specific failure. The same-image comparison
shows that every compared prompt family matches only one case `67` reference
and misses the other ten. `v017d` lowers the case `67` false-positive count by
one relative to `v017b`, but visual inspection indicates that it does so by
emitting fewer shifted row candidates, not by grounding the dense row correctly.

## Source Truth Shape

The current source report for `67` contains `11` objects:

| Ref | Confidence | Box | Size | Area |
| --- | --- | --- | --- | ---: |
| `target_1` | possible | `[90, 172, 109, 185]` | `19x13` | 247 |
| `target_2` | possible | `[131, 173, 146, 190]` | `15x17` | 255 |
| `target_3` | possible | `[150, 179, 162, 192]` | `12x13` | 156 |
| `target_4` | possible | `[167, 180, 181, 197]` | `14x17` | 238 |
| `target_5` | possible | `[185, 184, 201, 200]` | `16x16` | 256 |
| `target_6` | possible | `[204, 186, 226, 202]` | `22x16` | 352 |
| `target_7` | possible | `[230, 188, 255, 210]` | `25x22` | 550 |
| `target_8` | probable | `[256, 192, 286, 217]` | `30x25` | 750 |
| `target_9` | probable | `[315, 198, 351, 224]` | `36x26` | 936 |
| `target_10` | confirmed | `[424, 212, 490, 251]` | `66x39` | 2574 |
| `target_11` | confirmed | `[630, 235, 780, 330]` | `150x95` | 14250 |

This is valid current v2 source truth, but it is also a high-pressure tiny
target row: the first seven references are small `possible` objects and the
scene contains smoke/dust/perspective row cues.

## Same-Image Candidate Evidence

The fresh dev/no101 comparison scored every candidate on the same
`human_report_challenge_v2_dev_55_no101` manifest. Case `67` results were:

| Candidate | TP | FN | FP | Predicted Boxes | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| `v009_control_baseline` | 1 | 10 | 12 | 13 | over-enumerates row cues |
| `v014_weighted_building_selection` | 1 | 10 | 8 | 9 | same recall collapse, fewer extras |
| `v015e_individual_body_evidence` | 1 | 10 | 10 | 11 | no recall recovery |
| `v016a_reference_aware_candidate_discovery` | 1 | 10 | 9 | 10 | no recall recovery |
| `v017a_broad_group_box_lock` | 1 | 10 | 9 | 10 | no recall recovery |
| `v017b_group_box_rejection` | 1 | 10 | 9 | 10 | no recall recovery |
| `v017c_count_then_anchor` | 1 | 10 | 9 | 10 | no recall recovery |
| `v017d_visual_anchor_lock` | 1 | 10 | 8 | 9 | one fewer FP, still no recall recovery |
| `v017e_anti_span_guard` | 1 | 10 | 10 | 11 | no recall recovery |
| `v017f_compact_visual_anchor_balance` | 1 | 10 | 9 | 10 | no recall recovery |

For the three primary comparison candidates:

- `v017b` matched `target_11` with predicted `target_9`, IoU `0.434`,
  center error `41.110`, predicted-area ratio `0.677`, overlap coverage
  `0.508`.
- `v017d` matched `target_11` with predicted `target_8`, IoU `0.396`,
  center error `42.953`, predicted-area ratio `0.657`, overlap coverage
  `0.470`.
- `v017f` matched `target_11` with predicted `target_9`, IoU `0.434`,
  center error `41.110`, predicted-area ratio `0.677`, overlap coverage
  `0.508`.

In all three cases, `target_1` through `target_10` are false negatives.

## Visual Diagnosis

The bbox overlays show that case `67` is not dominated by a broad group box.
It is also not the same row-fragment enumeration failure that made case `101`
unsuitable as an active evaluation case.

The more precise diagnosis is:

- the model sees the row and emits target-like boxes along the visible
  formation line;
- many predictions sit above the reference body boxes, closer to dust,
  plume, rowline, or top-edge cues than to the vehicle body centers;
- the smallest references are both hard to see and heavily weighted by the
  current target count;
- the largest/rightmost vehicle is the only consistently matched target;
- `v017d` reduces one FP relative to `v017b`, but this is a shorter/fewer-box
  behavior rather than a genuine dense-row alignment solve.

## Classification

Labels:

- `dense_formation_anchor_failure`
- `perspective_row_target_failure`
- `smoke_dust_top_edge_anchor_failure`
- `tiny_possible_reference_pressure`
- `not_v017b_specific_regression`
- `not_case101_broad_group_box_failure`
- `known_prompt_only_limitation`

## Candidate Decision Impact

Case `67` does not justify replacing `v017b` with `v017d`.

Reasons:

- `v017b` and `v017d` both have `1` TP and `10` FNs on case `67`.
- `v017d` has one fewer FP on case `67`, but no recall improvement.
- `v017d` also fails the actual visual objective: the small-row boxes remain
  displaced from the reference bodies.
- The broader accepted comparison already favored `v017b` for the prompt-only
  promotion lane because it matched `v017d` on dev/no101 recall while reducing
  false positives overall.

Case `67` should remain a named limitation and follow-up diagnostic, not a
promotion blocker by itself.

## Future Prompt Axis If Authorized

If a later prompt-only v018 cycle is approved, the narrow axis should be dense
formation body-center anchoring under dust/smoke and perspective, not generic
recall expansion.

Constraints for a later prompt authoring wave:

- require boxes to cover visible target body evidence, not only dust, plume,
  shadow, sky, or rowline cues;
- reject evenly spaced placeholder boxes unless each has visible body support;
- prefer body-center/ground-contact anchoring for receding rows;
- keep broad group boxes and row-span boxes rejected;
- preserve separate-body recall for clearly visible targets;
- do not add case-specific examples or raw report text.

No prompt text is authored in this diagnostic.

## Recommendation

Keep `v017b_group_box_rejection` as the parked primary promotion candidate.
Record case `67` as a dense-formation follow-up caveat. Defer any new prompt
attempt until the user explicitly approves a v018 prompt-only cycle.
