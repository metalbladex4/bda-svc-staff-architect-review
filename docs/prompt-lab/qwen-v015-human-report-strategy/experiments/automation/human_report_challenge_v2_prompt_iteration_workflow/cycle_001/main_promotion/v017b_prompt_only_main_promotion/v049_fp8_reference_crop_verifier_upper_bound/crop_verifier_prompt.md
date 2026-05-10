# Crop Verifier Prompt

This compact verifier prompt was used for cropped images only. It does not ask for boxes and does not include case IDs.

```text
You are checking a focused crop from a battle-damage assessment image.
Expected target type: {target_type}

Decide whether the crop visibly contains the expected target type. Do not draw boxes.
Return JSON only with exactly these keys:
contains_target, target_type, visibility, damage_or_relevance, confidence, reason.

Use target_type "unknown" if unsure. Keep reason short.
```

## Schema

```json
{
  "contains_target": "boolean",
  "target_type": "military_equipment|buildings|unknown",
  "visibility": "clear|partial|smoke_obscured|low_contrast|ambiguous|not_visible",
  "damage_or_relevance": "damaged_or_bda_relevant|intact_context|unclear",
  "confidence": "number from 0.0 to 1.0",
  "reason": "short text"
}
```
