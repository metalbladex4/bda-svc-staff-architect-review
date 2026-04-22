# v010 Run01 Research Note

## Target Weakness

`v010` switched detection from `xyxy_1000` to `xyxy_pixels` and collapsed to
`object_not_found` on `tank.jpg`.

Observed failure:

- frozen `v009` working baseline still detected the target with bbox
  `[51, 37, 128, 73]`
- `v010` returned no usable detections
- candidate output fell back to `object_not_found` with bbox `[0, 0, 0, 0]`

## Research Questions

1. Did `v010` fail because Qwen3-VL expects normalized grounding coordinates
   rather than raw pixel coordinates?
2. Is there evidence that Qwen3-VL uses a different grounding coordinate regime
   than Qwen2.5-VL?
3. What prompt changes are more likely to help `v011` without overfitting the
   tank seed?

## Online Sources Used

- Qwen2.5-VL grounding examples:
  https://qwenlm.github.io/blog/qwen2.5-vl/
- Alibaba Cloud Qwen vision docs:
  https://www.alibabacloud.com/help/en/model-studio/vision
- Qwen3-VL issue `#1623` about 1000-scaled grounding coordinates:
  https://github.com/QwenLM/Qwen3-VL/issues/1623
- Qwen3-VL issue `#1741` discussing normalized grounding coordinates:
  https://github.com/QwenLM/Qwen3-VL/issues/1741
- Qwen3-VL issue `#1576` reporting weak grounding despite normalized
  coordinates:
  https://github.com/QwenLM/Qwen3-VL/issues/1576
- Ollama structured outputs docs:
  https://docs.ollama.com/capabilities/structured-outputs

## Extracted Findings

### 1. Qwen3-VL and Qwen2.5-VL do not use the same grounding coordinate regime

- Qwen2.5-VL public examples show `bbox_2d` and `point_2d` outputs in absolute
  image-space coordinates.
- Alibaba's Qwen vision docs explicitly distinguish the families:
  - Qwen2.5-VL returns absolute pixel coordinates relative to the scaled image.
  - Qwen3-VL returns relative coordinates normalized to a `[0, 999]` range.

Implication:

- The direct `_pixels` swap in `v010` was fighting Qwen3-VL's newer grounding
  convention instead of aligning with it.

### 2. The official/community issue history reinforces the `0..1000` expectation

- Issue `#1623` cites cookbook logic that converts Qwen3-VL grounding outputs
  to absolute coordinates by dividing by `1000`.
- Issue `#1741` shows that users are explicitly asking whether Qwen3-VL outputs
  normalized `0..1000` or actual pixel values, which confirms this is a known
  point of confusion in the official repo.

Implication:

- `xyxy_1000` remains the safer contract for Qwen3-VL in this project.

### 3. `v010` likely failed at our validation boundary, not only in the prompt

Local code review:

- [model.py](/home/williambenitez1/Capstone/src/bda_svc/pipeline/model.py#L137)
  changes prompt wording based on `_pixels` vs `_1000`.
- [utilities.py](/home/williambenitez1/Capstone/src/bda_svc/pipeline/utilities.py#L112)
  validates `_pixels` boxes against `model_image.width/height`.

Inference:

- If Qwen3-VL still emitted normalized `0..999`-style coordinates under the
  hood, those values would exceed the resized image width/height and be
  rejected by `bbox_to_pixels(...)`.
- That would naturally collapse detection to an empty list and trigger the
  fallback `object_not_found` output we saw in `v010`.

### 4. Prompt-only grounding is still fragile even on the normalized contract

- Issue `#1576` reports poor grounding performance even when users were already
  working in normalized `0..1000` space.

Implication:

- Returning to `xyxy_1000` is necessary after `v010`, but it is not by itself
  the full solution.
- The next prompt revision still needs a stronger grounding method.

## Local Reference Reconciliation

This aligns with the earlier local Qwen notes:

- `z_reference_docs/Prompting/Qwen/Qwen3-VL-8B-Instruct_Model_Card.md`
- `z_reference_docs/Prompting/Qwen/Alibaba_Cloud_vision_docs_for_Qwen-VL.md`
- `z_reference_docs/Prompting/Qwen/Qwen_3_Chat_template_deep_dive_Prompting_Behavior.md`

It also explains why `v006` helped more than longer or more novel wording:

- Qwen responds better when the task is short, explicit, JSON-grounded, and
  close to the model's native format.

## Prompt Implications For v011

1. Revert detection back to `xyxy_1000`.
2. Keep `assess_damage` frozen from `v009`.
3. Keep `summarize_scene` frozen.
4. Make `v011` detection-only.
5. Explicitly say the coordinates are relative and normalized from `0` to
   `1000`.
6. Explicitly say not to return raw pixel coordinates.
7. Keep the prompt generic across doctrinal target types rather than steering
   toward tank-specific behavior.
8. Use a short point-first or center-first grounding method instead of another
   large abstract rule block.

## Decision

- Reject the direct `_pixels` swap as the next active direction.
- Carry forward the lesson that Qwen3-VL appears to be more comfortable with a
  normalized grounding contract.
- Use `v011` to test a Qwen-native normalized grounding prompt rather than a
  second `_pixels` experiment.
