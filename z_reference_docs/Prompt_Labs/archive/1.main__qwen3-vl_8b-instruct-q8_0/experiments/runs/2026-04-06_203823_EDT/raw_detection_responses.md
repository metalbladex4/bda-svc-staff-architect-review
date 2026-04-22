# Raw Detection Responses

Purpose:

- capture the raw detection VLM bbox outputs for the `2026-04-06_203823_EDT`
  run after visual review showed the exported boxes were off target
- distinguish prompt/model localization failure from runtime coordinate
  conversion failure

Image:

- `tests/data/tank.jpg`
- source image size: `256x122`
- VLM image size: `256x122`

## `current-main_baseline`

Config bbox convention:

- `xyxy_1000`

Raw VLM response:

```json
{
  "detections": [
    {
      "target_type": "military_equipment",
      "bbox": [200, 300, 400, 600]
    }
  ]
}
```

Runtime converted output bbox:

- `[51, 37, 102, 73]`

Review note:

- The converted box is consistent with the raw response and configured
  convention, but the box is visually off target.

## `v008_reconciled-chain`

Config bbox convention:

- `xyxy_1000`

Raw VLM response:

```json
{
  "detections": [
    {
      "target_type": "military_equipment",
      "bbox": [200, 400, 450, 700]
    }
  ]
}
```

Runtime converted output bbox:

- `[51, 49, 115, 85]`

Review note:

- The converted box is consistent with the raw response and configured
  convention, but the box is visually off target.

## Interpretation

- This run indicates a detection localization failure, not a coordinate
  conversion failure.
- Both baseline and `v008` found the correct class and downstream assessment
  label, but neither produced a reliable bbox for the target.
- Do not promote `v008` based on this seed run.
- Next prompt work should focus on detection localization and bbox/crop
  reliability before evaluating summary improvements.
