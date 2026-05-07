# Visual Failure Taxonomy

## Purpose

Use this taxonomy to classify visual failure cases before writing the next Qwen
prompt candidate. The taxonomy is a review aid, not source truth.

## Required Failure Classes

| Class | Meaning | Prompt-addressability default |
| --- | --- | --- |
| `duplicate_same_body_box` | Multiple boxes describe the same connected target body. | maybe |
| `nested_fragment_box` | Box covers a fragment of an already detected body. | yes |
| `broad_row_or_group_box` | Box spans a row, convoy, cluster, or broad scene region. | risky |
| `context_only_smoke_debris_terrain` | Box is supported mainly by smoke, debris, dust, terrain, shadow, or fire. | yes |
| `building_piece_facade_roof_section` | Box covers a building piece, facade, roof section, or structural texture rather than one target body. | maybe |
| `adjacent_off_target_object` | Box covers a nearby non-target object. | maybe |
| `missed_small_valid_object` | A small but valid visible body was missed. | risky |
| `missed_obscured_valid_object` | A valid partly obscured body was missed. | maybe |
| `under_split_dense_valid_targets` | Multiple valid neighboring bodies were under-counted or merged. | risky |
| `over_split_one_continuous_target` | One continuous target body was split into too many detections. | maybe |
| `reference_ambiguity` | Source or reference ambiguity may explain the apparent error. | no |
| `schema_or_runtime_artifact` | JSON, schema, category normalization, matcher, or runtime behavior explains the apparent error. | no |
| `visual_artifact_missing` | Required overlay, crop, prediction, or summary artifact is missing. | no |
| `other` | Case was reviewed but does not fit a more specific class. | maybe |

## Lesson Types

| Type | Use when |
| --- | --- |
| `general_signal` | Repeated across cases or visually supported enough to shape a prompt. |
| `local_noise` | One case only with no broader pattern yet. |
| `reference_ambiguity` | Source or target definition is ambiguous. |
| `visual_artifact_limitation` | Static artifact quality limits the conclusion. |
| `schema_or_runtime_artifact` | A schema, JSON, category, or matcher issue dominates. |
| `non_prompt_lever` | Duplicate suppression, NMS, tiling, matcher, or backend behavior is a better lever. |

Only `general_signal` should drive stable prompt candidates.

## Required Row Fields

Each visual review row must include:

```text
case_id,candidate,target_type,event_type,failure_class,match_status,reference_label,predicted_label,visual_evidence,prompt_addressable,suggested_prompt_lever,risk_to_case_67,risk_to_155_166_office,lesson_type,reviewer_note,source_image,overlay_path,crop_path
```
