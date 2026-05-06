# Candidate Hypotheses For Future Qwen v015

Status: `hypothesis_only_no_prompt_text`

This file names candidate directions only. It intentionally does not
author prompt text, overlays, or runtime config.

## `v015a_recall_recovery`

- Status: `hypothesis_only_no_prompt_text`
- Goal: Recover valid target enumeration that v014 lost on dense, building, equipment, and confidence/distance cases.
- Expected gain: More matches and fewer false negatives than v014.
- Main risk: May reopen v009-style adjacent/background false positives.
- Dev focus: Cases with v014_recall_loss and precision_recall_tradeoff labels, especially case 101.

## `v015b_precision_guard`

- Status: `hypothesis_only_no_prompt_text`
- Goal: Preserve v014 abstention and false-positive suppression behavior as explicit guardrails.
- Expected gain: False positives remain close to v014 and materially below v009.
- Main risk: May keep too much v014 over-abstention and fail recall recovery.
- Dev focus: Cases with v014_fp_suppression, protected out-of-scope controls, and persistent false-positive gaps.

## `v015c_balanced_hybrid`

- Status: `hypothesis_only_no_prompt_text`
- Goal: Combine target enumeration pressure with object-existence and no-adjacent/background hallucination guards.
- Expected gain: Best balance of recall recovery and precision retention.
- Main risk: Could become too verbose or internally conflicting if prompt wording is not kept tight.
- Dev focus: Run only after v015a/v015b lessons are compared, or draft as a predeclared hybrid candidate.

## Shared Gate

A future candidate must improve recall versus `v014` without letting false
positives rebound toward `v009`. Any candidate that wins recall by
reopening adjacent/background hallucinations is learning evidence, not a
promotion candidate.
