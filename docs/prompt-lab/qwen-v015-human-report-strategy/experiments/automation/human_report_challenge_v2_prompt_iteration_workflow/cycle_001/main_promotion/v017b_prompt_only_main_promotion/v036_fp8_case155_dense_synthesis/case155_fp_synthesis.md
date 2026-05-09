# Case 155 FP Synthesis

The case-155 benefit was isolated. v034a had one remaining FP, `target_1` with bbox `[18,111,48,143]`, a small nested box inside/overlapping the larger valid wreck box `target_0` `[13,93,153,176]`. v035a removed that nested local box while keeping the two valid wreck detections.

This class is visually different from the dense-row failures in cases 66 and 67. The safer prompt lever is not broad fragment rejection. It is a local same-wreck duplicate idea: reject a smaller duplicate box inside the same visible wreck already covered by a whole-vehicle box.

Do not use the v035a wording. The words around dense-scene/partial/uncertain fragments were too broad and harmed case 67.
