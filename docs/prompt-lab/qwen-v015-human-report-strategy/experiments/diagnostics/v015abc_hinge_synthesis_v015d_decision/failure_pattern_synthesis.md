# Failure Pattern Synthesis

Status: `diagnostic_complete_no_prompt_text`

## Primary Blocker

`case_101_row_fragment_and_group_box_failure`

The v015a/v015b/v015c sequence shows a real recall-recovery signal, but the
same structural failure keeps reappearing on case `101`: row-like fragments are
enumerated as individual targets, and broad group/scene boxes can appear as
target detections.

## What Changed Across Attempts

- `v015a` recovered the most hinge matches (`13`) but reopened false positives
  on `101`, `12`, and `28`.
- `v015b` added a distinct-object guard, but `101` worsened to `31` predicted
  targets and `28` false positives.
- `v015c` changed to count-first uncertainty gating. It preserved `155` and
  repaired `12`/`28`, but `101` still had `31` predicted targets, `28` false
  positives, row-fragment enumeration, and a broad group box.

## Prompt-Only Assessment

Prompt-only risk: `high`.

Reason: Three prompt-only variants changed wording but did not enforce the structural boundary that 101 needs.

## Non-Prompt Guard Signal

Assessment: `worth_planning_before_more_dev_runs`.

Reason: The failure has a detectable output shape: regular rows of small boxes and broad group boxes.

This does not approve a runtime guard or post-processing change. It only says
the next planning step should consider a structural output validator/guard
alongside any final prompt-only `v015d` attempt.
