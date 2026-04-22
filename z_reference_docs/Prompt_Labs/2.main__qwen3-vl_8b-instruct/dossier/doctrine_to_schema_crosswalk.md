# Doctrine To Schema Crosswalk

This note maps Phase 1 BDA doctrine to the current prompt/output contract used by
`bda-svc`.

## Phase 1 Scope

Phase 1 for this lab is **physical damage assessment only**.

Allowed semantic scope:
- visible target identification
- visible physical damage categorization
- conservative confidence assignment
- short scene summary consistent with prior assessments

Out of scope unless directly visible and already justified by the prior
assessments:
- internal damage
- functional damage determination
- target system assessment
- operational intent or intelligence conclusions

## Detection Contract

| Prompt Surface | Output Field | Allowed Values / Shape | Source of Truth |
| --- | --- | --- | --- |
| `detect_objects` | `detections[*].target_type` | `buildings`, `military_equipment` | `src/bda_svc/pipeline/doctrine.yaml` keys |
| `detect_objects` | `detections[*].bbox` | `[xmin, ymin, xmax, ymax]` as 0–1000 integers | `config.yaml`, `model.py`, Qwen 2D grounding cookbook |

Detection notes:
- one box per physical object
- no duplicate detections
- no non-doctrinal labels
- bbox must tightly cover the visible extent of the object

## Assessment Contract

| Target Type | `damage_category` Semantic Set | Source of Truth |
| --- | --- | --- |
| `buildings` | `NO DAMAGE`, `LIGHT DAMAGE`, `MODERATE DAMAGE`, `SEVERE DAMAGE`, `DESTROYED` | `src/bda_svc/pipeline/doctrine.yaml` |
| `military_equipment` | `NO DAMAGE`, `DAMAGED`, `DESTROYED` | `src/bda_svc/pipeline/doctrine.yaml` |

Shared assessment fields:

| Output Field | Allowed Values / Shape | Notes |
| --- | --- | --- |
| `damage_category` | one doctrinally valid label for the selected target type | Final pipeline uppercases the value in `model.py` |
| `confidence_level` | `CONFIRMED`, `PROBABLE`, `POSSIBLE` | Use the lowest level consistent with the visible evidence |
| `brief_supporting_logic` | short semicolon-separated visible evidence phrases | No mention of crops, prompts, overlays, or internal analysis |

Assessment notes:
- selected target only
- visible evidence only
- no drift into functionality, mission effects, or unseen internal damage
- doctrine guides interpretation, but visible evidence remains the limiting factor

## Summary Contract

| Prompt Surface | Output | Rule |
| --- | --- | --- |
| `summarize_scene` | plain text only | must stay consistent with prior target assessments |

Summary notes:
- do not introduce new targets
- do not contradict target-level assessments
- if broader impact is mentioned, keep it conservative and anchored to assessed
  physical damage
- handle no-target scenes explicitly

## Watch Item

The current live summary prompt asks for likely functional impact only if it is
supported by the prior target assessments. That is the only place where the
pipeline approaches functionality claims. Prompt revisions should keep that
language tightly bounded to the already established physical damage and should
avoid speculative intelligence conclusions.
