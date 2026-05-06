# Visual Review Plan

## Goal

Classify the visual failure families behind the `v020c` and `v024l` delta
before writing any new Qwen `detect_objects` prompt.

The review should answer whether the next prompt should:

- stay on the `v020c` incumbent,
- salvage one cue from `v024l`, or
- pause prompt authoring because the remaining failures are better handled by
  duplicate/tiling suppression or another non-prompt lever.

## Source Artifacts

Use the existing `v023_literal99_qwen_no_stop_continuation` source package.

Required rows:

| Candidate | Role | Metrics |
| --- | --- | --- |
| `v020c_anchor_replay` | incumbent | `186 / 33 / 25` |
| `v024l_v023s_no_wheel_track_ablation` | high-recall learning evidence | `188 / 31 / 35` |

Do not use `v024o`; it is partial and unscored.

## First-Pass Tool Decision

Use static artifacts first:

- `eval/images_bbox_review/`
- `eval/images_bbox_both/` where present
- `eval/images_crop_predicted/` where present
- `eval/images_crop_reference/` where present
- raw prediction JSON
- eval summary JSON and CSV

Reason: both source runs already have complete `images_bbox_review` sets for
all 117 all-current cases. FiftyOne is useful later, but not required to begin
the priority slice.

Escalate to FiftyOne only after the first pass if:

- the priority-slice review cannot classify dominant failure classes,
- the review expands beyond the priority cases,
- or patch-level browsing becomes too slow to maintain reliably.

## Priority Cases

| Case | v020c | v024l | Review reason |
| --- | --- | --- | --- |
| `12` | `1/0/0` | `1/0/1` | v024l added FP |
| `14` | `1/1/0` | `2/0/0` | v024l recovered FN |
| `16` | `1/0/0` | `1/0/2` | v024l added FPs |
| `21` | `3/0/0` | `2/1/0` | v024l recall regression |
| `42` | `1/1/0` | `2/0/0` | v024l recovered FN |
| `66` | `8/0/4` | `8/0/6` | dense case, v024l added FPs |
| `67` | `9/2/4` | `9/2/3` | dense sentinel, v024l held recall and reduced 1 FP |
| `76` | `2/1/0` | `1/2/0` | v024l recall regression |
| `77` | `1/0/0` | `1/0/1` | v024l added FP |
| `84` | `8/5/0` | `7/6/0` | dense case, v024l recall regression |
| `88` | `1/0/0` | `1/0/1` | v024l added FP |
| `90` | `1/0/0` | `1/0/1` | v024l added FP |
| `97` | `1/0/2` | `1/0/2` | dense/control-like FP behavior unchanged |
| `103` | `1/0/1` | `1/0/4` | v024l added 3 FPs |
| `155` | `2/0/0` | `2/0/0` | positive control |
| `164` | `1/1/0` | `2/0/0` | v024l recovered FN |
| `166` | `1/0/0` | `1/0/0` | positive control |
| `172` | `1/2/0` | `3/0/0` | v024l recovered 2 FNs |

## Review Questions

For each priority case:

1. What did `v024l` recover that `v020c` missed?
2. What did `v024l` add that became a false positive?
3. Did `v020c` avoid that false positive because of useful prompt behavior or
   because of under-recall?
4. Is the failure class prompt-addressable with one compact patch?
5. Would that patch risk dense case `67`, positive controls `155`/`166`, or
   office-negative abstention?

## Decision Gate

After the first visual pass, choose exactly one next action:

- `continue_from_v020c`: default if v024l added FPs are diverse, context-heavy,
  or not prompt-addressable.
- `continue_from_v024l`: only if v024l recovered important true targets and
  added FPs share one compact prompt-addressable class.
- `compact_hybrid`: only if one v024l recall cue can be imported without
  importing its FP behavior.
- `pause_prompting`: if remaining failures look like duplicate/tiling,
  matching, or post-processing problems rather than prompt wording.

No prompt candidate may be authored until this gate has a filled decision in
`v020c_v024l_delta_review.md`.
