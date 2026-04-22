# Gemma `v001` Initial Comparison Summary

## Top Line

This narrow detect-only `v001` probe recovered both tank cases that had
regressed in the active post-`e7a22a9` Gemma `v000` baseline.

What changed:

- `tank_pressure` no longer abstains with `{"detections":[]}`
- `operational_tank4` no longer drifts into `DAMAGED / PROBABLE`

What this means:

- the explicit empty-detections instruction was materially involved in the
  `tank_pressure` failure
- a small detect-contract adjustment can move Gemma back toward the original
  pre-refresh equipment behavior

## Case Readout

### `tank_pressure`

`v000` active baseline (`run02`):

- raw response: `{"detections":[]}`
- final output: `object_not_found / NOT APPLICABLE`

`v001` run01:

- raw response: one `military_equipment` detection
- kept bbox: `[68, 58, 158, 90]`
- final output: `DESTROYED / PROBABLE`
- supporting logic:
  `target body engulfed in sustained fire; dense smoke obscuring structure; visible burning material on the target body`

Interpretation:

- this is a direct recovery of the detect-stage abstention
- the kept box is very close to the older first-live Gemma `run01` box
  `[67, 57, 154, 89]`
- relative to Qwen `v009`, the box is still larger and the eval IoU remains
  modest (`0.189`), but the semantic target read is back in-family

### `operational_tank4`

`v000` active baseline (`run02`):

- raw response: one `military_equipment` detection
- kept bbox: `[29, 311, 545, 402]`
- final output: `DAMAGED / PROBABLE`

`v001` run01:

- raw response: one `military_equipment` detection
- kept bbox: `[29, 252, 545, 401]`
- final output: `NO DAMAGE / CONFIRMED`
- supporting logic:
  `active firing signature at muzzle; target body intact; no visible structural damage`

Interpretation:

- this is not just a category flip; the bbox also moved upward to include the
  vehicle body more like the earlier successful read
- the result now matches active Qwen `v009` at the category/confidence level
- eval vs Qwen remains a true positive with modest IoU (`0.312`), but the
  semantic regression is clearly reversed

## Current Read

This is a promising Gemma recovery signal, but it is still narrow evidence.

The run only covers the two tank cases that were directly implicated in the
detect-contract diagnosis. It does **not** yet prove that this `v001`
adjustment preserves:

- `destroyed_tank15`
- `operational_building7`
- `office_negative`
- `destroyed_building4`

## Decision

- keep `v001` as the active next candidate
- do not promote it yet
- next step should be a broader follow-up validation pass, starting with the
  held controls and the known building failure surfaces before deciding whether
  `v001` becomes the new active Gemma direction
