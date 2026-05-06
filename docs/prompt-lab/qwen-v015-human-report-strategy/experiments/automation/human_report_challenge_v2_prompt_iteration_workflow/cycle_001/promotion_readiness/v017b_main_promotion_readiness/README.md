# v017b Main Promotion Readiness

This package records whether `v017b_group_box_rejection` is ready to be
considered for a later `main` promotion.

It is a decision packet only. It does not promote anything to `main`, does not
change source truth, and does not edit runtime code in this wave.

## Artifacts

- `source_manifest.json` lists the source evidence and forbidden mutations.
- `v017b_main_promotion_readiness_packet.md` is the human-facing packet.
- `v017b_main_promotion_readiness_packet.json` is the structured companion.

## Recommendation

Prefer a future prompt-only `main` promotion if the user approves adoption:
replace `prompts.detect_objects` in `main` `src/bda_svc/pipeline/config.yaml`
with the v017b prompt. Do not bring the Qwen `1.2` runtime-overlay machinery
into `main` as part of the same wave unless that larger infrastructure change
is separately approved.
