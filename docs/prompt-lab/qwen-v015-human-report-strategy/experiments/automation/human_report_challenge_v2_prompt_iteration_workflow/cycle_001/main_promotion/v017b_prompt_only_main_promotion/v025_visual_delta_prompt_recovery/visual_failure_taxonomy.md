# Visual Failure Taxonomy

## Purpose

Use this taxonomy to classify visual failure cases before writing the next Qwen
prompt candidate. The taxonomy is a review aid, not source truth.

## False Positive Classes

| Class | Meaning | Prompt-addressability default |
| --- | --- | --- |
| `FP_DUPLICATE_SAME_BODY` | Multiple boxes describe the same connected target body. | maybe |
| `FP_NESTED_FRAGMENT` | Box covers a fragment of an already-detected body. | yes |
| `FP_BROAD_ROW_GROUP_BOX` | Box spans a row, convoy, cluster, or broad scene region. | yes |
| `FP_CONTEXT_ONLY_SMOKE_DEBRIS_TERRAIN` | Box is supported mainly by smoke, debris, terrain, shadow, dust, or fire. | yes |
| `FP_BUILDING_PIECE_FACADE_ROOF_SECTION` | Box covers a building piece, facade/roof section, or structural texture rather than one target body. | maybe |
| `FP_ADJACENT_OFF_TARGET_OBJECT` | Box covers a nearby non-target object. | maybe |
| `FP_ROW_FORMATION_SPACING_CUE` | Box is inferred from spacing or pattern cues rather than a visible body. | yes |
| `FP_BOX_TOO_BROAD_TARGET_PLUS_CONTEXT` | Box includes a target plus too much surrounding context and fails matching. | maybe |
| `FP_REFERENCE_AMBIGUITY` | Source/reference ambiguity may explain the FP. | no |
| `FP_EVAL_MATCHING_ARTIFACT` | Matcher behavior, not visual detection, likely explains the FP. | no |
| `FP_SCHEMA_RUNTIME_ARTIFACT` | JSON/schema/runtime issue created the FP. | no |

## False Negative Classes

| Class | Meaning | Prompt-addressability default |
| --- | --- | --- |
| `FN_SMALL_VALID_BODY_MISSED` | A small but valid visible body was missed. | maybe |
| `FN_PARTLY_OCCLUDED_VALID_BODY_MISSED` | A valid partly occluded body was missed. | maybe |
| `FN_DENSE_ROW_UNDER_SPLIT` | Dense neighboring bodies were under-counted. | risky |
| `FN_LOW_CONTRAST_BODY_MISSED` | Low-contrast but valid body was missed. | maybe |
| `FN_DAMAGED_BODY_INTERPRETED_AS_CONTEXT` | Damaged body or wreck was treated as debris/context. | maybe |
| `FN_BUILDING_EXTERIOR_BODY_MISSED` | Distinct exterior building or collapsed exterior remains were missed. | maybe |
| `FN_PROMPT_TOO_CONSERVATIVE` | Prompt likely suppressed a valid detection. | yes |
| `FN_REFERENCE_AMBIGUITY` | Source/reference ambiguity may explain the FN. | no |
| `FN_EVAL_MATCHING_ARTIFACT` | Matcher behavior, not visual detection, likely explains the FN. | no |
| `FN_SCHEMA_RUNTIME_ARTIFACT` | JSON/schema/runtime issue created the FN. | no |

## Dense-Case Classes

| Class | Meaning |
| --- | --- |
| `DENSE_TRUE_SEPARATE_TARGET` | Neighboring target has its own visible body center and edge/boundary. |
| `DENSE_DUPLICATE_ON_ONE_TARGET` | Multiple boxes land on one target body. |
| `DENSE_BROAD_GROUP_BOX` | One box covers multiple targets or a row. |
| `DENSE_ROW_SPACING_FALSE_CUE` | Detection follows row spacing without body support. |
| `DENSE_PARTIAL_OCCLUSION` | Occlusion makes separate-body decision difficult. |
| `DENSE_BOX_SPLIT_MERGE_AMBIGUITY` | Visual/eval ambiguity between split and merged boxes. |

## Lesson Types

| Type | Use when |
| --- | --- |
| `GENERAL_SIGNAL` | Repeated across cases/slices and visually supported. |
| `LOCAL_NOISE` | One case only; no broader pattern yet. |
| `SOURCE_CONFLICT` | Source/eval artifact is inconsistent or unclear. |
| `VISUAL_AMBIGUITY` | Needs human review before prompt action. |
| `RUNTIME_ARTIFACT` | Schema, JSON, backend, or crop/rendering issue. |
| `NON_PROMPT_LEVER` | Likely duplicate suppression, NMS, tiling, or detector/backend behavior. |

Only `GENERAL_SIGNAL` should drive stable prompt candidates.

## Required Row Fields

Each visual review row must include:

```text
case_id,candidate,target_type,event_type,failure_class,match_status,reference_label,predicted_label,visual_evidence,prompt_addressable,suggested_prompt_lever,risk_to_case_67,risk_to_155_166_office,lesson_type,reviewer_note,source_image,overlay_path,crop_path
```
