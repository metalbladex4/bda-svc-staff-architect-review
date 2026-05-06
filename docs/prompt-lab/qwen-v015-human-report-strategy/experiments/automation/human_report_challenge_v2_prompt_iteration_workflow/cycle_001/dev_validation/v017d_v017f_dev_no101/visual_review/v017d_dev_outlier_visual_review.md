# v017d Dev Outlier Visual Review

## Purpose

This review explains where `v017d_visual_anchor_lock` is still visually weak
after the bounded `human_report_challenge_v2_dev_55_no101` run. The review is
diagnostic only. It does not change references, run inference, author `v017g`,
promote `v017d`, or alter runtime config.

## Aggregate Context

| Candidate | Split | Matches | FNs | FPs | Positive `155` |
| --- | --- | ---: | ---: | ---: | ---: |
| `v017d_visual_anchor_lock` | `dev_55_no101` | `72` | `34` | `16` | `2` matches |

Against the adjusted `v014` dev-no101 baseline, `v017d` improved matches,
false negatives, and false positives. The visual review therefore treats it as
a real candidate, not a failed prompt. The remaining question is whether its
errors are narrow enough to diagnose before any holdout or promotion decision.

## Reviewed Cases

| Case | Matches | FNs | FPs | Pred | Ref | Visual label |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `67` | `1` | `10` | `8` | `9` | `11` | dense formation anchor drift |
| `84` | `5` | `8` | `1` | `6` | `13` | broad row/span boxing |
| `66` | `8` | `0` | `6` | `14` | `8` | dense-row over-enumeration |
| `100` | `1` | `2` | `0` | `1` | `3` | building merge undersegmentation |
| `147` | `1` | `2` | `0` | `1` | `3` | dominant foreground target suppresses background buildings |
| `103` | `1` | `0` | `1` | `2` | `1` | duplicate/broad building-complex precision issue |
| `155` | `2` | `0` | `0` | `2` | `2` | positive control preserved |
| `97` | `1` | `0` | `0` | `1` | `1` | pass with broad reference-shape caveat |

The reviewed set accounts for `38` of the `50` total v017d dev error units.
Cases `67`, `84`, and `66` alone account for `33` error units.

## Case Notes

### `67`

`67` is the most important visual blocker. The image contains a dense receding
formation of military equipment along a smoky road. The reference boxes mark
many distinct targets. The predictions show partial recognition of the row, but
the boxes drift above or across the vehicles, creating many false positives
while still missing most reference targets.

This is not the old `101` row-fragment failure. The candidate is not simply
enumerating tiny repeated fragments. It is trying to recover the formation but
cannot anchor distant/overlapping bodies cleanly.

Prompt implication: the next prompt axis should target dense-formation anchor
discipline, not broad recall looseness.

### `84`

`84` is another dense formation case. The model identifies the general military
vehicle row, but several predictions become broad horizontal row/span boxes
instead of clean individual target boxes. The result is high false-negative
pressure even though the candidate clearly understands that targets are present.

Prompt implication: avoid wording that encourages row-level grouping or wide
stripe boxes. The prompt needs stronger language that a final box must wrap one
visibly separate body, not a visual row.

### `66`

`66` is the opposite side of the same dense-row problem. Recall is strong:
all eight references match. Precision suffers because the model also emits six
extra candidates in the repeated vehicle row.

Prompt implication: do not throw away `v017d`. It can recover dense military
equipment, but it needs a final self-filter against unsupported extra candidates
in rows, smoke, and small distant formations.

### `100`

`100` shows damaged buildings. The model selects one dominant building complex,
but the reference expects three separate building targets. The failure is
undersegmentation and missing separate building structures, not a military
equipment precision rebound.

Prompt implication: dense-row fixes should not erase the separate-building
lesson. However, building undersegmentation is secondary to the dense military
equipment failure mass.

### `147`

`147` contains one foreground tank and two small background buildings. The model
correctly detects the tank but misses the two background buildings. This is a
dominant-object suppression pattern: the foreground military equipment absorbs
the scene and secondary valid targets disappear.

Prompt implication: a future candidate should preserve secondary visible target
recall, but without returning to broad group boxes or row placeholders.

### `103`

`103` has one large reference building/complex. The prediction includes a large
matching building-complex box plus an extra overlapping/broad sub-box. This is a
small precision issue and may be partly tied to the reference's own broad shape.

Prompt implication: the model still needs duplicate/overlap suppression for
building complexes, but this is not the main blocker.

### `155`

`155` is clean. It remains a corrected positive-control case, and `v017d`
returns two matched detections with no false positives or false negatives.

Prompt implication: the current candidate respects the corrected source update
that `155` is positive, not an abstention case.

### `97`

`97` passes numerically. The reference is broad and scene-scale, and the
prediction is also broad. Treat this as a pass with a reference-shape caveat,
not as evidence that broad building/scene boxes are generally safe.

Prompt implication: do not use this case to justify broad box relaxation.

## Pattern Synthesis

The visual evidence supports three conclusions:

1. `v017d` generalizes better than the old baseline, but its remaining errors
   cluster in dense target formations.
2. The densest military-equipment cases split into two failure modes:
   misaligned/unsupported row candidates (`67`) and over-enumerated extras
   after good recall (`66`).
3. Building/background cases are secondary but still real: `100`, `147`, and
   `103` show undersegmentation, secondary-target omission, or duplicate broad
   boxes.

## Decision Guidance

Recommended next move:

- Keep `v017d_visual_anchor_lock` as the primary candidate.
- Do not promote or run holdout from aggregate metrics alone.
- Before any holdout, do either:
  - a focused v017d-v017f visual comparison on `66`, `67`, and `84`, or
  - a tightly scoped next prompt attempt aimed at dense-formation anchor
    discipline and unsupported-row self-filtering.

Do not reintroduce case `101` into forward scoring. It should remain
diagnostic-only unless the source/reference policy changes again.

## Boundaries

This review does not authorize:

- `v017g` prompt authoring
- dev/holdout/all-current reruns
- source-truth mutation
- reference edits
- structural guards
- runtime config adoption
- promotion
