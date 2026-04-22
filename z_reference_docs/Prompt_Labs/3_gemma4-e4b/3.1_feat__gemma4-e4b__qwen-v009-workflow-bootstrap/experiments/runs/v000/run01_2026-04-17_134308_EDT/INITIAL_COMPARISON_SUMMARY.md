# Gemma `v000` Initial Comparison Summary

## Overall Read

The first live Gemma baseline is a meaningful bootstrap success, not a failed
port.

Gemma 4 E4B:

- honored the runtime contract
- produced valid JSON on the inherited pack
- stayed strong on equipment cases
- stayed clean on the negative office control

The first clear weakness is building-specific:

- `destroyed_building4` is not acceptable yet

So the next Gemma cycle should be Gemma-specific prompt work, not workflow
rebuilding.

## Case Readout

### `tank_pressure`

- Gemma:
  - bbox `[67, 57, 154, 89]`
  - `DESTROYED`
  - `PROBABLE`
- Qwen active reference:
  - bbox `[51, 37, 128, 73]`
  - `DESTROYED`
  - `PROBABLE`
- `origin/main` baseline:
  - bbox `[51, 37, 102, 73]`
  - `DESTROYED`
  - `PROBABLE`

Read:

- Gemma stayed doctrinally correct.
- Gemma boxed a wider and lower visible mass than either inherited Qwen
  reference.
- It is closer in intent to the active Qwen stack than to the tighter
  `origin/main` baseline, but it still drifts geometrically.

### `destroyed_tank15`

- Gemma:
  - bbox `[0, 37, 458, 129]`
  - `DESTROYED`
  - `PROBABLE`
- Qwen active reference:
  - bbox `[36, 21, 457, 166]`
  - `DESTROYED`
  - `PROBABLE`

Read:

- Category and confidence held cleanly.
- The Gemma box stayed broadly aligned but became vertically tighter and
  shifted left.
- This looks acceptable as a first baseline, not a severe regression.

### `operational_tank4`

- Gemma:
  - bbox `[49, 252, 461, 401]`
  - `NO DAMAGE`
  - `CONFIRMED`
- Qwen active reference:
  - bbox `[66, 317, 515, 499]`
  - `NO DAMAGE`
  - `CONFIRMED`

Read:

- Gemma preserved the critical operational-firing assessment behavior.
- The box is materially smaller than the Qwen reference, so equipment
  localization style differs, but the doctrinal read is still correct.

### `destroyed_building4`

- Gemma:
  - target 0: `MODERATE DAMAGE`, `CONFIRMED`, bbox `[0, 52, 96, 176]`
  - target 1: `NO DAMAGE`, `CONFIRMED`, bbox `[0, 53, 67, 176]`
- Qwen active reference:
  - two targets, both `DESTROYED / PROBABLE`
- `origin/main` baseline:
  - one `SEVERE DAMAGE / PROBABLE`
  - one `DESTROYED / CONFIRMED`

Read:

- This is the clearest first-pass Gemma failure.
- Gemma did not preserve the inherited building read.
- One box overlaps the left structure only, and the second target undercalls to
  `NO DAMAGE`.
- This is the first prompt surface that needs Gemma-specific refinement.

### `operational_building7`

- Gemma:
  - bbox `[14, 121, 1346, 421]`
  - `NO DAMAGE`
  - `CONFIRMED`
- Qwen active reference:
  - bbox `[64, 119, 1315, 459]`
  - `NO DAMAGE`
  - `CONFIRMED`

Read:

- Strong hold.
- Geometry drift exists, but category and confidence are stable and the IoU is
  still strong.

### `office_negative`

- Gemma:
  - `object_not_found`
  - `NOT APPLICABLE`
  - `CONFIRMED`
- Qwen active reference:
  - same

Read:

- Negative-scene behavior held cleanly at raw `bda-svc` level.
- `bda_eval` still could not produce a normal CSV because it does not handle
  `NOT APPLICABLE` cleanly.

## Decision

- keep `v000` as the real Gemma baseline
- do not reopen workflow structure
- do not change doctrine
- start Gemma-specific prompt refinement from the building failure surface

## Best Next Step

Create `v001` as a Gemma-specific prompt candidate, but keep the cycle scoped:

- start with the surface most responsible for `destroyed_building4`
- preserve the equipment and negative-control behavior unless Gemma forces a
  tradeoff
