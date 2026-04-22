# Caution Case Review

This note records the deeper manual review of the two judgment-change watch
cases from the 10-image baseline-vs-`v009` blind sweep.

## Scope

Reviewed cases:

- `destroyed_building5`
- `destroyed_tank37`

Reference sources used for the review:

- the saved baseline and `v009` JSON reports in this run folder
- the saved `bbox_review_sheet.jpg` files for each case
- local doctrine in `src/bda_svc/pipeline/doctrine.yaml`
- prior local research note:
  `z_reference_docs/Prompting/Research_Loops/2.main__qwen3-vl_8b-instruct/v007/run02_2026-04-12_164250_EDT/research.md`

## Case 1: `destroyed_building5`

### Baseline

- category: `SEVERE DAMAGE`
- confidence: `PROBABLE`
- bbox: `[65, 18, 434, 479]`

### `v009`

- category: `DESTROYED`
- confidence: `PROBABLE`
- bbox: `[63, 18, 462, 493]`

### Review

- Both versions identify the same building.
- The bbox difference is modest; `v009` is slightly wider/taller.
- The real disagreement is damage severity.
- The local building doctrine says:
  - `SEVERE DAMAGE` = `45 to 75 percent`
  - `DESTROYED` = `75 to 100 percent`
  - for high multistory buildings, report damage relative to the whole
    structure, not only the worst-hit section
- In the image, the left side is catastrophically damaged, but a substantial
  right-side section of the building remains standing.

### Judgment

Baseline is more defensible on this case.

Best read:

- bbox: near-tie, minor `v009` expansion only
- category: baseline better
- overall: `v009` looks like a building-severity overcall here

## Case 2: `destroyed_tank37`

### Baseline

- category: `DESTROYED`
- confidence: `PROBABLE`
- bbox: `[299, 673, 896, 1212]`

### `v009`

- category: `DAMAGED`
- confidence: `PROBABLE`
- bbox: `[299, 678, 751, 1201]`

### Review

- Both versions identify the same burning vehicle.
- `v009` gives the cleaner bbox, with less extra smoke/background than the
  baseline box.
- The real disagreement is again damage severity.
- The local equipment doctrine says:
  - `DAMAGED` = visible deformation while major components remain intact
  - `DESTROYED` = unrepairable, catastrophic damage
- Our earlier local research note also concluded that sustained engulfing fire
  plus heavy smoke over the target body can still support
  `DESTROYED / PROBABLE` when catastrophic loss is strongly suggested but some
  details are obscured.
- In the image, the target body is engulfed in sustained fire and heavy smoke.
- Because the angle and smoke obscure important details, a cautious drop from
  `DESTROYED` to `DAMAGED` is arguable on this case.
- But the current `v009` logic text says the target is "catastrophically
  affected," which aligns more naturally with the doctrine wording for
  `DESTROYED` than for `DAMAGED`.

### Judgment

This case is mixed.

Best read:

- bbox: `v009` better
- category: `v009` is arguable as a cautious call under obscuration
- logic wording: current `v009` phrasing is too catastrophic for a `DAMAGED`
  label
- overall: `v009` likely improves localization here, but its target-level logic
  should be softened if we want `DAMAGED` to be the doctrinally clean read

## Overall Read

These two cases do not overturn the broader blind-sweep result, but they do
clarify its remaining edge-case risk.

The residual issue is best described as:

- category-calibration watch cases, not recall failures
- one building overcall on `v009`
- one burning-equipment case where `v009` may be making the right cautious
  category call, but with logic text that overstates the certainty/severity

## Doctrine File Note

`src/bda_svc/pipeline/doctrine.yaml` was not changed as part of this review.

Current working rule:

- keep using the tracked doctrine file as-is
- only consider revising it later if repeated experiment drift shows a durable
  mismatch against the official BDA material preserved under
  `z_reference_docs/BDAs/`

That is the honest interpretation to carry into any team-facing summary.
