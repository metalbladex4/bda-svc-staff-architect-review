# v020c vs v024l First-Pass Static Delta Review

Review timestamp: `2026-05-07T00:05:56Z`

## Source State

| Candidate | Role | Matches | FNs | FPs | Errors | Status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `v020c_anchor_replay` | incumbent | 186 | 33 | 25 | 58 | keep as current Qwen prompt incumbent |
| `v024l_v023s_no_wheel_track_ablation` | high-recall learning evidence | 188 | 31 | 35 | 66 | do not promote as-is |

Controls:

- `155`: both passed
- `166`: both passed
- office-negative: both passed

Forbidden row:

- `v024o_v024l_intact_building_piece_exclusion` is partial/unscored and not
  evidence in this review.

## Artifact Inventory

Source run aliases used in `visual_failure_taxonomy.csv`:

| Alias | Source root |
| --- | --- |
| `v020c_run` | `v023_literal99_qwen_no_stop_continuation/runs/v020c_anchor_replay/all_current_no101/human_report_challenge_v2_all_current_117_no101_2026-05-06_033103Z/` |
| `v024l_run` | `v023_literal99_qwen_no_stop_continuation/runs/v024l_v023s_no_wheel_track_ablation/all_current_no101/human_report_challenge_v2_all_current_117_no101_2026-05-06_113019Z/` |

| Artifact | v020c | v024l |
| --- | ---: | ---: |
| all-current summary | present | present |
| all-current CSV | present | present |
| raw predictions | 117 | 117 |
| eval predictions | 117 | 117 |
| `images_bbox_review` | 117 | 117 |
| `images_bbox_both` | 117 | 117 |
| `images_crop_predicted` | 117 | 117 |
| `images_crop_reference` | 117 | 117 |

Artifact caveat:

- The first scaffold under-counted derived images by extension because some
  artifacts are `.png` rather than `.jpg`.
- Recheck found complete first-pass static artifacts for all priority cases in
  both source runs.
- Static overlays/crops were sufficient for this pass. FiftyOne is not needed
  before the next prompt-candidate planning step.

Temporary non-repo review aids:

- `/tmp/v025_visual_review/recovered.jpg`
- `/tmp/v025_visual_review/added_fp.jpg`
- `/tmp/v025_visual_review/regress_dense_controls.jpg`
- `/tmp/v025_visual_review/annotated_recovered.jpg`
- `/tmp/v025_visual_review/annotated_added_fp.jpg`
- `/tmp/v025_visual_review/annotated_regress_dense_controls.jpg`

## Reviewed Cases

Reviewed priority cases:

```text
12, 14, 16, 21, 42, 66, 67, 76, 77, 84, 88, 90, 97, 103, 155, 164, 166, 172
```

`visual_failure_taxonomy.csv` contains first-pass rows for:

- `v020c` remaining false negatives
- `v020c` remaining false positives
- `v024l` recovered false negatives
- `v024l` added false positives
- `v024l` recall regressions
- dense/control sentinels

## Recovered Recall

| Case | Recovered target description | Failure class | Prompt-addressable? | Suggested compact cue |
| --- | --- | --- | --- | --- |
| `14` | lower smoke-obscured tank separated from upper tank | `under_split_dense_valid_targets` | yes but medium case-67 risk | separate visible target bodies even when smoke bridges them |
| `42` | right towed tank separated from left tank | `under_split_dense_valid_targets` | yes but high case-67 risk | split adjacent hull bodies only when two centers and boundaries are visible |
| `164` | small right background house recovered | `reference_ambiguity` | not stable prompt signal | do not generalize without manual target-definition review |
| `172` | left damaged building plus destroyed red vehicle recovered | `under_split_dense_valid_targets` | yes | include distinct visible bodies outside a broad main-building box |

Best useful recall cue:

- `v024l` proves the model can recover separate visible bodies that `v020c`
  sometimes merges into one broad target.
- The cue should be imported, if at all, as a compact patch on top of `v020c`,
  not by using `v024l` as the base prompt.

## Added False Positives

| Case | Added FP description | Failure class | Prompt-addressable? | Suggested compact guard |
| --- | --- | --- | --- | --- |
| `12` | adjacent left facade sliver beside main building | `building_piece_facade_roof_section` | yes | reject extra adjacent building slivers after one full building body is boxed |
| `16` | two intact background buildings behind a destroyed tank | `adjacent_off_target_object` | yes | keep target-class focus and reject intact background structures |
| `66` | additional tiny dense-row vehicle fragments | `nested_fragment_box` | yes but high case-67 risk | reject subpart boxes on an already boxed vehicle body |
| `77` | right adjacent building wing | `building_piece_facade_roof_section` | yes | avoid connected facade or wing boxes after the whole building body is boxed |
| `88` | intact white background truck | `adjacent_off_target_object` | yes but medium row risk | reject intact background support/civilian vehicles when not damage-supported target bodies |
| `90` | same adjacent left facade sliver as case `12` | `building_piece_facade_roof_section` | yes | same compact adjacent-sliver guard as case `12` |
| `103` | upper background apartment rows and building pieces | `building_piece_facade_roof_section` | yes | reject upper background rows and intact building pieces around one target complex |

FP conclusion:

- `v024l` does not have one clean FP failure family.
- Its added FPs span building slivers, intact background objects, dense-row
  nested fragments, and multi-piece facade/roof sections.
- That diversity makes `v024l` unsafe as a base prompt.

## Dense Cases 66/67/84/97

| Case | Visual behavior | Risk to next prompt | Required guard |
| --- | --- | --- | --- |
| `66` | both candidates match all 8 references but emit dense-row same-body fragments; `v024l` adds two more | high | any duplicate guard must preserve small true vehicles |
| `67` | both candidates preserve 9 matches and 2 FNs; `v024l` reduces one FP but still keeps dust-row duplicates | highest | preserve existing silhouette/exterior-boundary behavior and do not add broad dense cleanup |
| `84` | `v020c` misses 5 tiny/far vehicles; `v024l` misses 6 | high | do not branch from `v024l` for dense rows |
| `97` | both candidates keep two building/facade FPs | medium | treat as persistent building-piece or duplicate-suppression issue |

Dense conclusion:

- `v020c` remains the safer base for dense rows.
- Case `67` is not solved by `v024l`, but `v024l` does preserve it closely
  enough to provide a narrow recall cue.

## Controls 155/166/office

| Control | v020c | v024l | Risk note |
| --- | --- | --- | --- |
| `155` | passed | passed | Preserve two burned vehicle detections and avoid suppressing no-damage/low-damage military equipment broadly. |
| `166` | passed | passed | Preserve burned truck detection with no extra context boxes. |
| office-negative | passed | passed | No static re-review needed for prompt-candidate planning unless a future cue broadens target-class scope. |

## Dominant Failure Classes

| Rank | Class | Evidence cases | Prompt-addressable? | Notes |
| --- | --- | --- | --- | --- |
| 1 | `building_piece_facade_roof_section` | `12`, `77`, `90`, `97`, `103` | yes but compact only | Main reason `v024l` cannot replace `v020c`. |
| 2 | `duplicate_same_body_box` / `nested_fragment_box` | `66`, `67`, `84` | maybe | Dense-row cleanup is high risk and may be better as non-prompt suppression. |
| 3 | `under_split_dense_valid_targets` | `14`, `42`, `172` | yes | Best source for a narrow v020c-based recall patch. |
| 4 | `adjacent_off_target_object` | `16`, `88` | yes but narrow | Guard background intact objects without suppressing valid no-damage military equipment. |
| 5 | `schema_or_runtime_artifact` | `76` | no for detect prompt | `v024l` visually boxed target `3` but emitted invalid `SEVERE`; this is not a detect-prompt lever. |

## Prompt-Addressability Decision

Decision:

```text
continue_from_v020c
```

Reason:

```text
v024l recovers useful separate-body recall on cases 14, 42, and 172, but its added
false positives are diverse and include building slivers, intact background
objects, dense-row nested fragments, and facade/roof pieces. The next prompt,
if authorized later, should branch from v020c and import only one compact
separate-visible-body cue from v024l. Do not branch from v024l wholesale.
```

FiftyOne decision:

```text
not_needed_for_next_step
```

Reason:

```text
Static bbox-review images, annotated temporary overlays, eval CSV rows, raw/eval
predictions, and crops were sufficient to classify the first-pass priority
slice. FiftyOne can remain a phase-2 aid if the review expands beyond the
priority slice or if patch-level browsing becomes unwieldy.
```

## Next Candidate Gate

Do not author `v025a` until the user explicitly approves prompt authoring.

If approved, the next candidate should be gated as:

```text
Candidate ID: v025a_v020c_compact_separate_body_recovery
Base prompt: v020c_extra_box_audit
Dominant visual failure class: under_split_dense_valid_targets
Prompt-addressable reason: v024l recovered separate visible bodies in 14, 42, and 172 without needing a long prompt block
One-sentence hypothesis: A compact visible-body split cue can recover some v020c FNs while retaining v020c FP discipline
Exact text region to change: detect_objects prompt audit section only
Expected metric movement: +1 to +3 matches, -1 to -3 FNs, +0 to +3 FPs
Expected dense-case risk: medium to high for 67 and 84
Expected FP risk: building-piece FPs if wording says split too broadly
Expected FN risk: suppressing tiny/distant no-damage targets if the cue is over-defensive
Stop/disqualifier rule: any 155/166/office failure or case 67 collapse below v020c behavior
```
