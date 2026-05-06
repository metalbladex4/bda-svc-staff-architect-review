# v022 Literal-99 Qwen Recursive Prompt Refinement Cycle

Generated: `2026-05-05T23:53:07.853348+00:00`

This package runs Qwen-only sequential prompt candidates through fetched
`upstream/main` OpenAI-compatible runtime code. It replaces only
`prompts.detect_objects` in scratch worktrees.

Literal 99% target: reduce the current upstream prompt's 74 total detection
errors to <=1 combined false negatives + false positives on
`human_report_challenge_v2_all_current_117_no101`.

No prompt, doctrine, source truth, runtime code, PR, commit, or push is adopted
by this package.

## Closeout

The cycle closed as prompt-only plateau evidence. `v020c_anchor_replay`
remained the best row at `186` matches / `33` FNs / `25` FPs, while all v022
variants regressed. The clearest repeated failure was dense case `67`, which
collapsed under every new wording pattern. Use `final_recommendation.md` and
`comparison_matrix.md` as the authoritative summary for this package.
