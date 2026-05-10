# Crop Detector Prompt

```text
You are detecting BDA-relevant targets in a cropped image tile.
Find visible damaged or BDA-relevant military equipment and building targets in this crop.
Return JSON only with this shape:
{"detections":[{"target_type":"military_equipment|buildings","bbox":[x1,y1,x2,y2],"confidence":0.0,"visibility":"clear|partial|smoke_obscured|low_contrast|ambiguous","damage_or_relevance":"damaged_or_bda_relevant|intact_context|unclear","reason":"short"}]}

Use crop-local pixel coordinates. If there are no valid targets, return {"detections":[]}.
Reject context-only boxes, intact background, broad scene boxes, and tiny ambiguous artifacts.
Include small, crowded, or smoke-obscured targets only when they are visibly BDA-relevant.
```

Schema:

```json
{
  "detections": [
    {
      "target_type": "military_equipment|buildings",
      "bbox": "[x1, y1, x2, y2] in crop-local pixels",
      "confidence": "number from 0.0 to 1.0",
      "visibility": "clear|partial|smoke_obscured|low_contrast|ambiguous",
      "damage_or_relevance": "damaged_or_bda_relevant|intact_context|unclear",
      "reason": "short text"
    }
  ]
}
```
