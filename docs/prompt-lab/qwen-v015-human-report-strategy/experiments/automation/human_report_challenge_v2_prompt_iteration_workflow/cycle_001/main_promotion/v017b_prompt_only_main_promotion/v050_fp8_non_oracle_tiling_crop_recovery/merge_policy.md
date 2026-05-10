# Merge Policy

- valid crop-local bbox
- valid target_type
- confidence >= 0.55
- not intact_context
- ambiguous requires confidence >= 0.78
- reject self-reported context-only/unclear
- reject obvious same-label duplicates with IoU >= 0.45

`pp046a` is excluded because it failed visual lock.
