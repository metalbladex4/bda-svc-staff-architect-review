# v032b Diagnosis

Generated: `2026-05-09T00:09:09Z`

What this tested: a real negative-only guard against smoke, debris, terrain, roof/facade patches, and cropped fragments standing in for visible target bodies.

What changed from FP8 working best: added one bad-final-box bullet. Rendered prompt hash changed to `0cd29a82d8c002e540ba8c5d61238eb6689ddba69bdbccb1ea1cc45d0da6d015`.

Metrics: sentinel `39 / 10 / 16 / 26` versus baseline sentinel `42 / 7 / 15 / 22`. Case 67 stayed `10/1/2`, but case 66 worsened from baseline `n/a` to `n/a`, case 84 worsened from `n/a` to `n/a`, and case 97 worsened from `n/a` to `n/a`. Case 155 improved from baseline `n/a` to `n/a`. Case 166 stayed `n/a`. Office-negative passed.

Decision: rejected. It reduced one FP in case 155 but increased total sentinel errors from 22 to 26 and reopened dense-case precision/recall drift.

Likely load-bearing phrase: "strongest evidence is only smoke, debris, road/terrain texture, roof/facade patch, or a cropped fragment". On FP8 this appears too broad; it helps a small FP slice but suppresses or disturbs valid dense detections.

Lesson type: model-surface-specific signal. FP8 did not benefit from old-surface-style fragment/context wording.

Next hypothesis: avoid broad context/fragment guards; test structure/order or smaller load-bearing replays instead.
