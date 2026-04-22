# Prompt Version Log

Use one row per experiment round. Change only one prompt surface at a time.

| Version | Date | Prompt Surface | Parent | Change Summary | Intended Effect | Eval Tracks Run | Result | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `v000` | `2026-04-10` | baseline | none | Fresh snapshot from `main:src/bda_svc/pipeline/config.yaml` after the upstream sync to `c077cd8`; metadata refreshed again after the sync to `21deaf5`, which hardened bbox/runtime validation and tests without changing prompt text or model tag. | Establish the new active current-main baseline before any further prompt iteration. | baseline run01 | first baseline run recorded: `DESTROYED`, `PROBABLE`, bbox `[51, 37, 128, 73]` | keep |
| `v001` | `2026-04-10` | detect_objects | `v000` | Adds a visible-boundary tightening method so the box anchors to the visible solid target body and stops at the last clear structural edge instead of extending through smoke, plume, track, or other scene context. | Tighten the bbox around the physical target body and reduce right-edge expansion that may be softening downstream assessment confidence. | `v001` run01, run02 | baseline repeated exactly; `v001` stayed directionally similar but shifted from `[56, 46, 123, 79]` to `[56, 46, 123, 85]`; confidence stayed `CONFIRMED`; subtype drift remained | not a clean win |
| `v002` | `2026-04-10` | detect_objects | `v000` | Uses an edge-by-edge grounding method so each bbox side must land on visible solid target structure and move inward if it falls on smoke, rail bed, ground, or other context. | Test a more concrete spatial localization tactic after `v001` proved only marginally and inconsistently better. | `v002` run01 | produced bbox `[56, 46, 123, 79]`, `CONFIRMED`, and summary/subtype drift identical to `v001` run01 | not a new win |
| `v003` | `2026-04-11` | detect_objects | `v000` | Replaces the long negative-rule wording family with a shorter Qwen-style grounding prompt: identify the visible solid target body first, place the target center on that structure, then expand to the smallest valid box. Adds one targeted smoke-and-rails reference example. | Test whether a more compact, example-anchored, center-first grounding strategy improves localization where `v001` and `v002` converged to the same off-target behavior. | `v003` run01 | produced bbox `[51, 37, 102, 73]`, kept `PROBABLE`, removed `locomotive` from logic, and tightened back to the older archived-baseline box shape; manual review showed the box still sat left of the actual target body and mostly captured terrain/track-side context | not a win |
| `v004` | `2026-04-12` | detect_objects | `v000` | Uses fire and smoke only as search cues, then tells the model to box the visible solid body segment directly attached to the fire source rather than the full plume, rail bed, or terrain context. | Test whether a fire-source-to-object-body grounding method can pull the box off the wide baseline without raising confidence or reusing the `v003` wording family. | `v004` run01 | produced bbox `[51, 37, 102, 61]`, kept `PROBABLE`, but over-shrank upward and still missed the target body; subtype drift worsened to `locomotive or rolling stock` / `likely a locomotive or heavy transport` | partial reuse only |
| `v005` | `2026-04-12` | detect_objects | `v000` | Uses a point-first, occlusion-aware grounding method that tells the model to use fire/smoke only to find the damaged object area, then anchor on the visible attached body segment and expand to the smallest box that covers the visible connected body section. | Test whether the point-first / occlusion-aware idea from the `v004` research note can move the box without over-shrinking onto the nearest burning patch. | `v005` run01 | matched the baseline output exactly: bbox `[51, 37, 128, 73]`, `PROBABLE`, same `locomotive` subtype drift, same summary | reject as no-effect wording |
| `v006` | `2026-04-12` | detect_objects | `v000` | Replaces the abstract `v005` prose with a shorter, more direct Qwen-style prompt plus contrastive examples showing what should and should not be boxed. | Test whether a shorter, example-driven prompt can make the desired bbox behavior more salient than the earlier abstract grounding blocks. | `v006` run01, run02 | produced bbox `[46, 46, 128, 92]`, moved materially onto the visible burning target body, removed `locomotive` from logic, and repeated exactly on confirmation run02; still raises confidence to `CONFIRMED` and strengthens downstream summary language | bbox win confirmed; next issue is downstream calibration |
| `v007` | `2026-04-12` | assess_damage | `v006` | Keeps the `v006` detection family and rewrites only `assess_damage` to make burn/smoke cases more conservative, explicitly discouraging `CONFIRMED`, K-kill, and unrepairable wording when the target body is partly obscured. | Reduce confidence inflation and target-level overclaiming while preserving the stronger `v006` target framing. | `v007` run01, run02 | repaired comparison in run02 kept `PROBABLE`, removed K-kill language, and removed subtype drift, but overcorrected to `DAMAGED` | partial reuse only |
| `v008` | `2026-04-12` | assess_damage | `v007` | Adds an abstract `CATEGORY GUIDANCE` block intended to recover `DESTROYED` at `PROBABLE` without undoing the anti-overconfidence framing. | Test whether explicit category rules can recover `DESTROYED` while keeping the safer `v007` tone. | `v008` run01 | no material improvement: still `DAMAGED`, still `PROBABLE`, and subtype drift returned | reject direction |
| `v009` | `2026-04-12` | assess_damage | `v007` | Replaces `v008`'s abstract category block with one short example showing the desired `DESTROYED` + `PROBABLE` output pattern and adds an explicit generic-target wording rule. | Restore `DESTROYED` without bringing back `CONFIRMED`, K-kill language, or subtype drift. | `v009` run01 | restored `DESTROYED` + `PROBABLE`, removed subtype drift from target-level logic, and kept bbox unchanged within the assessment-cycle comparison; summary drift still remains | best assessment candidate; hold fixed while grounding is revisited |
| `v010` | `2026-04-12` | detect_objects + bbox_convention | `v009` | Keeps the best-known `v006`/`v009` pair intact while switching detection from `xyxy_1000` to `xyxy_pixels` and making pixel-space output explicit in the prompt. | Test whether native image-space coordinates improve grounding more than another wording-only rewrite. | `v010` run01 | collapsed to `object_not_found`; bbox `[0, 0, 0, 0]`; no candidate overlay/crop artifacts were produced | reject `_pixels` swap on this seed case |
| `v011` | `2026-04-12` | detect_objects | `v009` | Reverts the failed `_pixels` swap and keeps the `v006`/`v009` baseline pair, but makes detection more explicitly Qwen-native: normalized `0..1000` coordinates, a short point-first grounding method, and one compact contrastive example. | Recover from the `v010` coordinate-contract mismatch while keeping the prompt generic across target types. | `v011` run01 | recovered detection and preserved `DESTROYED` + `PROBABLE`, but produced bbox `[56, 46, 123, 76]`, which is closer to the older `v001` / `v002` family than to the stronger `v006` bbox win | useful recovery, not yet a clear win |
| `v012` | `2026-04-12` | detect_objects | `v009` | Keeps the normalized-contract lesson from `v011` but returns to a stronger contrastive-example style and explicitly tells the model to box the full visible connected target body rather than shrinking around the most salient burn patch. | Test whether we can keep the corrected contract while avoiding the point-first over-shrinking behavior seen in `v011`. | `v012` run01 | preserved `DESTROYED` + `PROBABLE`, but produced bbox `[51, 49, 128, 85]`; raw debug showed the model kept the same left/right span as baseline and only shifted the box downward | reject as bbox-improving prompt |
| `v013` | `2026-04-12` | detect_objects + runtime detection aid | `v009` | Keeps the frozen `v009` working prompt surfaces intact and enables a new two-pass ROI refinement path: detect once on the full scene, expand an ROI around each accepted box, re-detect inside that ROI, and map the best overlapping same-label child box back to the scene. | Test the smallest code-level grounding aid after `v012` strengthened the case that prompt-only detection tuning is stalling on the tank pressure-test image. | `v013` run01, run02 | both runs preserved `DESTROYED` + `PROBABLE` and repeated exactly at bbox `[51, 37, 102, 73]`; debug showed the first pass narrowed to raw `[200, 300, 400, 600]`, the ROI-local second pass returned no detections, and refinement kept the narrowed original box | confirmed non-win; refine parameters next |
| `v014` | `2026-04-12` | runtime detection aid | `v013` | Keeps the two-pass ROI refinement path but increases `refinement_roi_buffer_ratio` from `0.35` to `0.75` so the second pass sees substantially more local context around the first-pass detection. | Test whether the second pass was failing only because the refinement ROI was too tight. | `v014` run01 | preserved `DESTROYED` + `PROBABLE`, but still ended at bbox `[51, 37, 102, 73]`; first pass again narrowed to raw `[200, 300, 400, 600]`, and the wider ROI still produced no second-pass detections | reject as helpful parameter change |

## Cross-Image Generalization Checks

### 2026-04-12 — Frozen `v006` + `v009` Sweep

- Cases:
  - `tank.jpg`
  - `destroyed_truck15.jpg`
  - `operational_truck4.jpg`
  - `office.jpg`
- Result:
  - truck scenes behaved sensibly
  - office stayed `object_not_found` / `NOT APPLICABLE`
  - the tank seed remained unstable across repeats
- Decision:
  - keep the current direction
  - do not create a new prompt version from this sweep alone
  - treat the tank seed as a repeatability pressure test rather than the only
    proof of quality

## Sequence Rules

- This lab restarts the version sequence from `v000`.
- Archived `v001` through `v010` remain in the previous `q8_0` lab and should
  not be treated as active current-main evidence.
- Add exactly one new version row per experiment round.
- Change one prompt surface at a time unless a deliberate multi-surface reset is
  explicitly documented.
- If schema reliability drops, reject the version even if semantics improve.
- Accepted versions should be copied into `experiments/winners/` once they pass.
- The upstream sync to `21deaf5` did not change prompt text, model tag, or
  dependencies, so the active `v000` through `v009` sequence remains current.
