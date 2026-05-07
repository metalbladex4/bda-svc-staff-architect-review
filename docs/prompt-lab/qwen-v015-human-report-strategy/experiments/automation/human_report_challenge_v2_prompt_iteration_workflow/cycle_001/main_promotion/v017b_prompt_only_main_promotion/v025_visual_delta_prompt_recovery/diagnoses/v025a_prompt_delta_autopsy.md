# v025a Prompt Delta Autopsy

Generated: `2026-05-07T02:06:00Z`

## Source Rows

| Prompt | Role | Metrics | Status |
| --- | --- | --- | --- |
| `v020c_v019c_extra_box_audit` / `v020c_anchor_replay` | incumbent base | `186 / 33 / 25 / 58` | keep incumbent |
| `v025a_v020c_compact_separate_body_recovery` | tested candidate | `176 / 43 / 35 / 78` | rejected |

`v024l_v023s_no_wheel_track_ablation` remains high-recall learning evidence only
at `188 / 31 / 35 / 66`. `v024o` remains partial/unscored and is not evidence.

## Exact Detect-Prompt Diff

```diff
--- v020c_detect_objects
+++ v025a_detect_objects
@@ -30,6 +30,8 @@
 EXTRA-BOX AUDIT
 Before output, silently inspect every detection that sits near another detection or near a strong context cue. Remove it unless it has its own visible body center and at least one visible body edge or exterior-structure boundary. If two boxes describe the same connected body or the same continuous exterior building, keep only the tighter whole-body box.

+Separate-body recovery: if one candidate spans two nearby targets, split only when each target has its own visible body center and at least one visible body edge or exterior-structure boundary; smoke, debris, row alignment, proximity, or broad scene context alone never justifies an extra box.
+
 FINAL BALANCE
 Keep v019c recall behavior: small, damaged, crowded, or partly obscured targets are valid when their own target body remains visible after context is removed. The audit removes extras; it should not remove a true separable target body.
```

## Exact Text Change

Added text:

```text
Separate-body recovery: if one candidate spans two nearby targets, split only when each target has its own visible body center and at least one visible body edge or exterior-structure boundary; smoke, debris, row alignment, proximity, or broad scene context alone never justifies an extra box.
```

Removed text: none.

Moved text: none.

## Section Changed

| Section | Changed? | Notes |
| --- | --- | --- |
| Task section | no | Candidate preserved v020c task wording. |
| Context-shadow reversal | no | Candidate preserved the visual-search and context-removal sequence. |
| Good final box | no | Candidate preserved the connected-body and tight-box wording. |
| Bad final box | no | Candidate preserved context/group/fragment/subsection rejections. |
| Extra-box audit | yes | One separate-body recovery sentence was inserted immediately after the audit-removal sentence. |
| Final balance | no | Candidate preserved the v020c recall/balance sentence. |
| Output/schema | no | Candidate preserved JSON-only output and schema. |

## Placeholder And Schema Check

| Contract item | Preserved? |
| --- | --- |
| `{categories}` | yes |
| `{detection_guidance}` | yes |
| `{bbox_format}` | yes |
| `{bbox_scale}` | yes |
| JSON-only output wording | yes |
| top-level `detections` field | yes |
| empty-scene `{"detections": []}` instruction | yes |
| output schema shape | yes |

## Instruction-Type Analysis

`v025a` added both kinds of language in one sentence:

- Positive split language: "if one candidate spans two nearby targets, split"
- Negative guard language: "smoke, debris, row alignment, proximity, or broad
  scene context alone never justifies an extra box"

The added negative guard was semantically compatible with v020c, but it was
attached to a new positive "split" command in the audit region. That likely
changed the effective emphasis from "remove extras" to "look for split
opportunities while auditing extras."

## Order, Salience, And Emphasis

The instruction order changed only by insertion, but the insertion point was
high-impact:

- `v020c` used `EXTRA-BOX AUDIT` as a final rejection/removal checkpoint.
- `v025a` inserted an affirmative recovery action inside that rejection
  checkpoint.
- The sentence repeats "visible body center" and "visible body edge" from the
  removal rule, but reframes those cues as permission to split nearby targets.

This did not weaken a load-bearing v020c phrase by deletion. It weakened the
load-bearing behavior by salience: the final audit was no longer purely a
cleanup rule.

## Dense-Row Risk

The added phrase is broad enough to affect dense rows because it says:

```text
if one candidate spans two nearby targets, split
```

Even with the later guard against row alignment and broad context, that phrase
can invite the model to inspect a continuous row for nearby body centers. In
case `67`, the model then shifted most row detections upward toward the dust
and top-edge rowline, producing boxes that visually correspond to row fragments
but no longer overlap the reference body boxes enough to match.

## Load-Bearing Phrase Assessment

No exact v020c wording was removed. The likely load-bearing behavior that broke
was the v020c final-audit priority:

```text
Remove it unless it has its own visible body center and at least one visible body edge or exterior-structure boundary.
```

`v025a` reused that phrase but inverted its practical role from a removal gate
to a split-permission gate. The collapse suggests that this phrase is safe as a
negative filter but dangerous when immediately reused as positive split
authorization.

## Split-Versus-Reject Balance

The change accidentally increased the weight of splitting over rejection.
Evidence:

- case `172` improved from `1/2/0` to `3/0/0`, so the split/recovery cue did
  activate in at least one intended target case
- cases `14` and `42` stayed unchanged at `1/1/0`, so the cue did not recover
  two of the three intended visual targets
- case `66` worsened from `8/0/4` to `8/0/6`, reopening nested-fragment burden
- case `67` collapsed from `9/2/4` to `1/10/9`, the hard disqualifier

## Autopsy Conclusion

The exact prompt delta was mechanically tiny but behaviorally too salient. The
failure is most likely caused by inserting a positive split-recovery command
inside the final audit section, where v020c's stable behavior depends on
removing extra boxes rather than creating new split opportunities.

Do not attempt another positive separate-body cue in the audit/final-balance
region. The next direction should not assume separate-body recovery remains
viable until a targeted micro-ablation proves placement and salience can be
controlled without collapsing case `67`.
