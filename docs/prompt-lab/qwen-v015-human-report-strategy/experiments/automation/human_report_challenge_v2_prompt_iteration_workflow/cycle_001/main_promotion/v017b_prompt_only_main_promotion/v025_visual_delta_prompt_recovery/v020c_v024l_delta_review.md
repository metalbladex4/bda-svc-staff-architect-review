# v020c vs v024l Delta Review Template

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

| Artifact | v020c | v024l |
| --- | --- | --- |
| all-current summary | present | present |
| all-current CSV | present | present |
| raw predictions | 117 | 117 |
| eval predictions | 117 | 117 |
| `images_bbox_review` | 117 | 117 |
| `images_bbox_both` | 111 | 111 |
| `images_crop_predicted` | 111 | 111 |
| `images_crop_reference` | 111 | 111 |

Artifact caveat:

- use `images_bbox_review` as the complete visual surface
- use bbox-both and crop images where present
- cases `42` and `90` have complete review images but missing some crop/both
  derivative images in both source runs

## Priority Cases

| Case | v020c | v024l | Delta | Review question |
| --- | --- | --- | --- | --- |
| `12` | `1/0/0` | `1/0/1` | `+0/+0/+1` | What FP did v024l add? |
| `14` | `1/1/0` | `2/0/0` | `+1/-1/+0` | What valid target did v024l recover? |
| `16` | `1/0/0` | `1/0/2` | `+0/+0/+2` | Are added FPs duplicate, context, or broad boxes? |
| `21` | `3/0/0` | `2/1/0` | `-1/+1/+0` | Why did v024l lose recall? |
| `42` | `1/1/0` | `2/0/0` | `+1/-1/+0` | What visible cue did v024l use? |
| `66` | `8/0/4` | `8/0/6` | `+0/+0/+2` | Dense FP burden; classify added boxes. |
| `67` | `9/2/4` | `9/2/3` | `+0/+0/-1` | Dense sentinel; preserve this behavior. |
| `76` | `2/1/0` | `1/2/0` | `-1/+1/+0` | Why did v024l lose one match? |
| `77` | `1/0/0` | `1/0/1` | `+0/+0/+1` | What FP did v024l add? |
| `84` | `8/5/0` | `7/6/0` | `-1/+1/+0` | Dense recall regression. |
| `88` | `1/0/0` | `1/0/1` | `+0/+0/+1` | What FP did v024l add? |
| `90` | `1/0/0` | `1/0/1` | `+0/+0/+1` | What FP did v024l add? |
| `97` | `1/0/2` | `1/0/2` | `+0/+0/+0` | Why do both keep the same FP burden? |
| `103` | `1/0/1` | `1/0/4` | `+0/+0/+3` | Highest added-FP priority case. |
| `155` | `2/0/0` | `2/0/0` | `+0/+0/+0` | Positive control safety check. |
| `164` | `1/1/0` | `2/0/0` | `+1/-1/+0` | What target did v024l recover? |
| `166` | `1/0/0` | `1/0/0` | `+0/+0/+0` | Positive control safety check. |
| `172` | `1/2/0` | `3/0/0` | `+2/-2/+0` | Best recovered-recall case. |

## Recovered Recall

Fill after visual review.

| Case | Recovered target description | Failure class | Prompt-addressable? | Suggested compact cue |
| --- | --- | --- | --- | --- |
| `14` |  |  |  |  |
| `42` |  |  |  |  |
| `164` |  |  |  |  |
| `172` |  |  |  |  |

## Added False Positives

Fill after visual review.

| Case | Added FP description | Failure class | Prompt-addressable? | Suggested compact guard |
| --- | --- | --- | --- | --- |
| `12` |  |  |  |  |
| `16` |  |  |  |  |
| `66` |  |  |  |  |
| `77` |  |  |  |  |
| `88` |  |  |  |  |
| `90` |  |  |  |  |
| `103` |  |  |  |  |

## Dense Cases 66/67/84/97

Fill after visual review.

| Case | Visual behavior | Risk to next prompt | Required guard |
| --- | --- | --- | --- |
| `66` |  |  |  |
| `67` |  |  |  |
| `84` |  |  |  |
| `97` |  |  |  |

## Controls 155/166/office

Fill after visual review if any proposed prompt lever could affect controls.

| Control | v020c | v024l | Risk note |
| --- | --- | --- | --- |
| `155` | passed | passed |  |
| `166` | passed | passed |  |
| office-negative | passed | passed |  |

## Dominant Failure Classes

Fill after completing `visual_failure_taxonomy.csv`.

| Rank | Class | Evidence cases | Prompt-addressable? | Notes |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |

## Prompt-Addressability Decision

Choose exactly one:

- `continue_from_v020c`
- `continue_from_v024l`
- `compact_hybrid`
- `pause_prompting`

Decision:

```text
pending_visual_review
```

Reason:

```text
pending_visual_review
```

## Next Candidate Gate

Do not author `v025a` until the following fields are complete:

```text
Candidate ID:
Base prompt:
Dominant visual failure class:
Prompt-addressable reason:
One-sentence hypothesis:
Exact text region to change:
Expected metric movement:
Expected dense-case risk:
Expected FP risk:
Expected FN risk:
Stop/disqualifier rule:
```
