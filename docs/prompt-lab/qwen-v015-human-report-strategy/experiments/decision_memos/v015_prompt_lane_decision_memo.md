# v015 Prompt-Lane Decision Memo

Status: `v015_closed_v016_reference_aware_prompt_lab_next`

This memo closes the `v015` prompt-lane sequence as learning evidence and sets
the next experiment direction as `v016_reference_aware_prompt_lab`.

The decision is not that "prompt engineering is over." The decision is that
the specific `v015` family of prompt-only attempts did not produce a
dev-passing candidate. The next prompt experiment should change the prompt-lab
method, not keep tightening the same individual-body wording.

## Decision

Use `v015a` through `v015e` as source-backed learning evidence. Do not promote
any `v015` candidate, do not adopt one into runtime config, and do not run
holdout or all-112 from `v015e` without a new approval.

The next prompt experiment should be `v016_reference_aware_prompt_lab`.
`v016` remains prompting work, but it starts with a reference/eval-shape audit
and prompt-interface design pass before any new runtime prompt text is written.

## Source Evidence

Primary source artifacts:

- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015a_recall_recovery/executions/human_report_challenge_v1_hinge_smoke_2026-04-29_171438Z/v015a_gate_check_summary.json`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015e_individual_body_evidence/executions/human_report_challenge_v1_v015e_hinge_smoke_2026-04-29_223729Z/v015e_gate_check_summary.json`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015e_individual_body_evidence/executions/human_report_challenge_v1_v015e_hinge_smoke_2026-04-29_223729Z/case_101_manual_review.md`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015e_individual_body_evidence/executions/human_report_challenge_v1_dev_56_2026-04-29_231342Z/eval/evaluation_2026-04-29_231946Z_summary.json`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015e_individual_body_evidence/executions/human_report_challenge_v1_dev_56_2026-04-29_231342Z/v015e_dev_gate_summary.json`

Supporting source artifacts:

- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015a_recall_recovery/README.md`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015b_distinct_object_guard/README.md`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015c_count_first_uncertainty_gate/README.md`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015d_fail_closed_row_guard/README.md`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/runs/v015e_individual_body_evidence/README.md`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/diagnostics/v015a_hinge_failure_diagnostic/README.md`

## What v015 Tried

The all-112 human-report comparison showed the motivating tradeoff:

- `v009`: higher recall, but too many false positives.
- `v014`: stronger false-positive suppression, but lower recall.

The `v015` lane tried to recover valid multi-target recall while preserving
`v014`-style precision.

Candidate sequence:

- `v015a_recall_recovery`: recovered recall pressure but reopened false
  positives.
- `v015b_distinct_object_guard`: tried to add distinct-object filtering, but
  case `101` row-fragment and broad-box failures worsened.
- `v015c_count_first_uncertainty_gate`: abandoned row-enumeration wording, but
  still produced row fragments and a broad group box on `101`.
- `v015d_fail_closed_row_guard`: suppressed row fragments and false positives,
  but became too conservative and failed to improve recall.
- `v015e_individual_body_evidence`: strongest hinge result; preserved
  precision, suppressed row-fragment enumeration, but still produced the
  broad-box `101` failure and failed the dev recall gate.

## Why v015e Failed

`v015e` passed the standard hinge gate:

| Metric | v014 hinge baseline | v015e hinge result | Result |
| --- | ---: | ---: | --- |
| matches | 8 | 10 | pass |
| false negatives | 15 | 13 | pass |
| false positives | 1 baseline / 3 cap | 0 | pass |
| protected `155` | abstention-safe | abstention-safe | pass |

But the two-tier hinge gate failed because case `101` still produced one broad
group/scene box. Manual review confirmed:

- row-fragment enumeration was suppressed
- one predicted target remained a broad group/scene box
- the predicted box spanned image context rather than one individual target
  body
- the automatic match was helped by reference-shape caveats, including a large
  foreground reference box and duplicate `target_7` / `target_8` boxes

The learning-only 56-case dev run then showed that the hinge recall improvement
did not generalize:

| Metric | v014 dev baseline | v015e dev result | Result |
| --- | ---: | ---: | --- |
| matches | 70 | 61 | fail |
| false negatives | 47 | 56 | fail |
| false positives | 17 baseline / 21 cap | 17 | pass |
| protected `155` | abstention-safe | abstention-safe | pass |

Conclusion: `v015e` preserved precision, but it did not recover enough recall.
It became a cleaner precision-preserving prompt, not a balanced recovery
candidate.

## What Counts As Prompt Engineering Besides More Prompt-Only Attempts

Prompt engineering in this project is broader than repeatedly editing the
runtime prompt text. The useful prompt-engineering paths from here are:

1. Reference-aware prompt-lab design.
   Study how reference shapes, duplicated boxes, grouped targets, and
   qualitative caveats influence the feedback signal before writing the next
   prompt.

2. Prompt interface and rubric redesign.
   Reconsider the prompt's decision surface: what the model is asked to decide
   first, what uncertainty rule it applies, and how it distinguishes a
   legitimate recall miss from an unsafe broad or group box.

3. Case-pack and evaluation-shape diagnosis.
   Use the dev failures to decide which cases are true prompt failures, which
   are reference-shape caveats, and which are evaluation artifacts. This is
   still prompt work because it determines what signal the next prompt should
   optimize.

4. Prompt decomposition or self-filter prompting.
   A future candidate can still be prompt-only while changing structure:
   candidate discovery first, then an internal rejection pass before final JSON.
   That is not a runtime validator if the final output remains one model
   response.

5. Failure-taxonomy-driven constraints.
   Author the next prompt from named failure modes rather than from broad
   advice. The prompt should explicitly target the failure class it is meant to
   change and leave unrelated behavior alone.

These are still prompt-engineering activities because they shape the model
instruction, the prompt interface, the evaluation target, and the case
selection strategy. They are different from merely making another small wording
variant.

## v016 Direction

Next experiment name: `v016_reference_aware_prompt_lab`.

`v016` should remain prompting-focused and should not begin by implementing a
runtime guard or postprocessor. The first `v016` wave should be a design
package that asks:

- Which dev failures are true prompt failures?
- Which failures are reference-shape or evaluation-shape caveats?
- Which cases should be excluded from automatic pass/fail interpretation and
  kept as manual diagnostics?
- Which prompt-interface change is most likely to recover recall without
  widening boxes or reintroducing row-fragment enumeration?

Minimum pre-authoring cases to review:

- `101`: known reference-shape caveat and broad group-box diagnostic.
- `67`: largest combined precision/recall dev stress case for `v015e`.
- `84`: largest recall miss in the `v015e` dev run.
- `86`, `97`, and `103`: dev cases with false-positive signals that should be
  classified before writing new prompt text.
- `155`: protected object-not-found control.
- `166`: protected holdout control; do not run unless a later holdout wave is
  explicitly approved.

The first `v016` artifact should not be a prompt overlay. It should be a
reference-aware design memo that identifies which prompt axis to test.

## Non-Prompt Structural Guard Discussion

A non-prompt structural guard would be a deterministic or code-level layer
after the model output. It could reject or correct patterns such as:

- broad boxes covering a whole scene, row, convoy, group, or terrain strip
- repeated row-fragment enumeration
- boxes with impossible or suspicious geometry
- duplicate or near-duplicate detections
- detections that violate a declared output-shape rule

That may eventually be useful, but it is not the next implementation here.
It would change system behavior beyond prompt text, and it would need a
separate approval, separate tests, and separate promotion rules. It should not
be hidden inside a prompt-lab memo as if it were only another prompt variant.

For now, structural guards are discussion-only. They can be used to clarify
what prompt failures look like, but they should not be implemented as part of
the `v016_reference_aware_prompt_lab` decision.

## Closed Decisions

- Do not promote `v015a`, `v015b`, `v015c`, `v015d`, or `v015e`.
- Do not run `v015e` holdout or all-112 from current evidence.
- Do not adopt `v015e` into runtime config.
- Treat `v015e` as evidence that precision can be preserved, but recall did
  not generalize.
- Treat `101` as a manual diagnostic case with reference-shape caveats, not as
  a pure automatic metric.
- Keep the next experiment prompting-focused, but make it reference-aware
  before authoring prompt text.

## Next Natural Step

Plan and implement the first `v016_reference_aware_prompt_lab` design package.
It should classify the key dev failures and define the next prompt axis, but it
should not yet write a `v016` overlay.
