# v017d/v017f Dense Formation Visual Comparison

## Purpose

This comparison checks whether `v017f_compact_visual_anchor_balance` actually
improves the dense-formation failure surface that remains after the bounded
`v017d` dev validation. It focuses only on `66`, `67`, and `84`, because those
three cases account for `33` of `50` v017d dev error units.

This is a diagnosis artifact only. It does not authorize prompt authoring,
holdout, all-current evaluation, source-truth mutation, reference edits,
runtime config adoption, structural guards, or promotion.

## Metrics Comparison

| Case | v017d matches | v017d FNs | v017d FPs | v017f matches | v017f FNs | v017f FPs | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `66` | `8` | `0` | `6` | `8` | `0` | `6` | unchanged |
| `67` | `1` | `10` | `8` | `1` | `10` | `9` | v017f adds `1` FP |
| `84` | `5` | `8` | `1` | `5` | `8` | `0` | v017f removes `1` FP |

Dense-formation error units:

- `v017d`: `33`
- `v017f`: `33`

The top-line v017f recall advantage does not come from these dense formation
cases.

## Visual Findings

### `66`

Both candidates produce the same metric shape: all eight references matched and
six false positives. Visually, both candidates over-enumerate along the row of
trucks. The useful behavior is that the visible vehicles are found; the failure
is extra repeated-row candidates that are not supported strongly enough by the
reference shape.

Readout: `v017f` does not improve `66`.

### `67`

`v017d` already failed this case badly: one match, ten false negatives, and
eight false positives. `v017f` keeps the same one match and ten false negatives,
then adds one more false positive. The visual issue remains poor anchoring in a
smoky, receding line of vehicles/tanks. The model detects that a formation is
present, but the boxes do not lock onto separate bodies cleanly.

Readout: `v017f` is worse on the largest dense-formation blocker.

### `84`

`v017f` removes one false positive, but the case remains five matches and eight
false negatives. Visually, this is still a row/span boxing problem: the model
recognizes the formation but does not reliably separate the individual vehicle
bodies required by the references. The one-FP improvement is not a meaningful
fix for the failure mode.

Readout: `v017f` slightly cleans the metric, but does not solve recall or box
shape.

## Interpretation

`v017f` is not the better candidate for the dense-formation problem. Its global
dev advantage over `v017d` is real numerically, but it comes from outside the
core blocker cases reviewed here. On the cases that matter most for the next
prompt-learning decision, the dense-formation error mass is unchanged.

The next prompt axis should therefore not be "prefer v017f" or "loosen recall."
It should be a narrow dense-formation anchoring constraint:

- identify separate visible target bodies before finalizing boxes
- reject broad row, stripe, and span boxes
- reject evenly spaced placeholder boxes in receding formations
- after candidate discovery, remove unsupported extras that appear only because
  nearby row members exist
- keep distant valid targets only when there is body evidence, not just row
  rhythm

## Recommendation

Keep `v017d_visual_anchor_lock` as the primary candidate. Treat `v017f` as a
useful comparator but not as the next promotion/holdout candidate.

If the user approves another prompt attempt, author a narrow successor focused
on dense-formation anchor discipline and unsupported-row self-filtering. If the
user prefers more diagnosis before authoring, expand this comparison to the
nearest additional dense-row cases and inspect whether the same row/span pattern
recurs outside `66`, `67`, and `84`.

Do not reintroduce `101` into forward scoring.
