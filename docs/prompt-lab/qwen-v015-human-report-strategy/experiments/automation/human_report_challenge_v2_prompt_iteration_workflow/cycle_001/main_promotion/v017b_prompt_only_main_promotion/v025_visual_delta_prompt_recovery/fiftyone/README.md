# FiftyOne

FiftyOne is not used directly in the first pass.

Reason:

- existing `images_bbox_review` artifacts cover all 117 all-current cases
- static review is enough to begin the priority slice
- plain Python import of `fiftyone` was not available during planning

Escalate here later only if static review cannot classify the dominant failure
families or if the review expands beyond the priority slice.

FiftyOne must remain a visual review aid only. `bda_eval` summaries, source
manifests, prediction JSON, and source images remain authoritative.
