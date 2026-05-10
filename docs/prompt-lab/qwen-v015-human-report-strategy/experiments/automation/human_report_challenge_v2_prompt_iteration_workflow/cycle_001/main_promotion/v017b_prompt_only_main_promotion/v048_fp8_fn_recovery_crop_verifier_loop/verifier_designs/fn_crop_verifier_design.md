# Verifier Design Plan

Objective: recover selected FNs without reintroducing false positives.

The verifier should operate on crop/tile proposals and prediction geometry. It must not use reference boxes, eval state, case IDs, or ground truth at inference time.

## JSON Contract

```json
{
  "object_found": "boolean",
  "target_type": "buildings|military_equipment",
  "bbox_in_crop": "[x1,y1,x2,y2]",
  "confidence_rationale": "short string",
  "reject_reason": "short string or empty",
  "merge_candidate": "boolean"
}
```

## Merge Gates

- candidate must be generated from a fixed tile/crop policy, not reference-centered inference in deployment
- candidate target_type must be supported by visible damage/equipment evidence in crop
- candidate must not be mostly contained by an existing accepted prediction unless verifier says separate target
- candidate should be rejected if it is only smoke, road, intact structure, shadow, debris, or context
- full all-current scoring must show no FP increase and no dense/control regression

## Stop Modes

- any verifier-added FP on dense/control cases
- case 66/67/84/110 degradation
- office-negative false positive
- JSON instability
- verifier requires reference boxes at inference time
