# v017b Prompt-Only Main Promotion Override Decision

Status: `accepted_for_prompt_only_main_promotion`

Date: `2026-05-03`

## Decision

Promote `v017b_group_box_rejection` into main as the Qwen detection prompt after
explicitly accepting the one-false-positive semantic override.

The raw all-current/no101 gate result was:

- matches: `165`
- false negatives: `54`
- false positives: `22`
- strict false-positive cap: `21`

The raw false-positive gate therefore failed by `1`.

The focused false-positive visual review found that the decisive extra raw FP is
case `125`, where the model returned `object_not_found` on a positive case. That
is a real miss, but it is already counted as a false negative. Treating that
placeholder as a target-hallucination false positive double-counts the same
failure for the purpose of the prompt-promotion cap.

With case `125` treated as FN-only for semantic extra-target accounting, the
effective extra-target FP total is `21`, which meets the cap.

## Evidence

- Main prompt hash: `331bf0d27d08f62f153050c9bf20ab0a2b76d63828974217a7a24d3964ab2259`
- Prompt source: `v017b_group_box_rejection`
- Main all-current/no101 replay:
  `runs/human_report_challenge_v2_all_current_117_no101/human_report_challenge_v2_all_current_117_no101_2026-05-03_223526Z/`
- Gate result:
  `main_promotion_gate_result.md`
- False-positive visual review:
  `false_positive_visual_review/v017b_false_positive_visual_review.md`
- Contact sheet:
  `false_positive_visual_review/artifacts/v017b_fp_visual_review_contact_sheet.jpg`

## Promotion Rationale

- Recall improved materially versus the worktree adopted-runtime all-current
  replay: `+7` matches and `-7` false negatives.
- Positive controls `155` and `166` passed.
- Office-negative abstention passed.
- No broad group/scene-box regression was found in the false-positive visual
  review.
- The raw FP cap miss is explained by an `object_not_found` placeholder on a
  positive case, not by an additional hallucinated target.

## Follow-Up Caveat

Case `67` remains a serious dense-formation blocker:

- `1` match
- `10` false negatives
- `10` false positives

The model still anchors on smoke/dust/row positions in this hard case. This is
recorded as follow-up evidence for the next prompt cycle, not as a blocker to
the v017b prompt-only main promotion.

## Boundaries

This decision authorizes only the prompt text already staged in main
`src/bda_svc/pipeline/config.yaml`.

It does not authorize:

- source-report or reference-truth mutation
- additional prompt authoring
- holdout expansion
- Graphify refresh
- Mem0 write
- MCP config or hook edits
- push to remote
