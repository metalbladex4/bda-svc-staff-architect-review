# v022 Final Recommendation

Generated: `2026-05-06T00:09:01.488491+00:00`

## Verdict

Do not promote any v022 prompt. Keep `v020c_extra_box_audit` / `v020c_anchor_replay`
as the current Qwen detect-prompt incumbent.

The literal target was intentionally extreme: reduce the current upstream
prompt baseline from `74` total detection errors (`38` FNs + `36` FPs) to
`<= 1` combined false negative + false positive on
`human_report_challenge_v2_all_current_117_no101`. The best v022 result was the
anchor replay itself at `58` total errors, so the target was not reached and no
new candidate improved the incumbent.

## Result Summary

| Candidate | Matches | FNs | FPs | Total Errors | Decision |
| --- | ---: | ---: | ---: | ---: | --- |
| `v020c_anchor_replay` | 186 | 33 | 25 | 58 | Keep incumbent |
| `v022d_compressed_context_shadow` | 176 | 43 | 36 | 79 | Reject |
| `v022b_sparse_scene_proxy_filter` | 173 | 46 | 33 | 79 | Reject |
| `v022e_v020c_dense_guard_sentence` | 172 | 47 | 34 | 81 | Reject |
| `v022c_candidate_ledger_balance` | 172 | 47 | 41 | 88 | Reject |
| `v022a_micro_target_sweep` | 183 | 36 | 84 | 120 | Reject |

All completed rows used the fetched `upstream/main` OpenAI-compatible runtime
path. The preferred `http://localhost:8000/v1` endpoint was unavailable after
retry, so the authorized fallback was Ollama's OpenAI-compatible
`http://localhost:11434/v1` endpoint, labeled in artifacts as
`ollama_openai_compat_fallback_11434`.

## Why The Incumbent Still Wins

- `v020c_anchor_replay` reproduced the known `186/33/25` Qwen result and kept
  `155`, `166`, and office-negative passing.
- `v022a` recovered no useful net signal: it raised false positives to `84`,
  including a case `66` FP spike from `4` to `19`.
- `v022b` and `v022c` showed that extra sparse-scene filters and candidate-ledger
  structure still damage dense formations, especially case `67`.
- `v022d` tested compression against the Qwen-family preference for compact
  grounding prompts, but it lost `10` matches overall and collapsed case `67`.
- `v022e` preserved the v020c text almost exactly and added only one dense-guard
  sentence; even that perturbation collapsed case `67` and worsened case `84`.

## Dense-Case Lesson

The practical blocker is not general prompt creativity. It is the fragility of
the dense-formation balance, especially case `67`.

| Candidate | Case 67 Matches | Case 67 FNs | Case 67 FPs |
| --- | ---: | ---: | ---: |
| `v020c_anchor_replay` | 9 | 2 | 4 |
| `v022a_micro_target_sweep` | 1 | 10 | 11 |
| `v022b_sparse_scene_proxy_filter` | 2 | 9 | 10 |
| `v022c_candidate_ledger_balance` | 2 | 9 | 10 |
| `v022d_compressed_context_shadow` | 1 | 10 | 11 |
| `v022e_v020c_dense_guard_sentence` | 2 | 9 | 10 |

This makes v020c look less like a wording pattern that should be elaborated and
more like a brittle local optimum. Additional prompt-only edits are likely to
keep trading dense recall for cleanup language.

## Recommendation

Close v022 as prompt-only plateau evidence. Preserve v020c as the Qwen config
prompt and make the next technical investigation non-prompt-side: duplicate /
tiling suppression, post-processing, detector/backend behavior, or visual review
of the remaining FP/FN slices. Any future prompt-only work should start from
exact v020c and use very small controlled A/B changes, not broad new instruction
patterns.

## Boundary

- This package is prompt-lab evidence only.
- No source truth, doctrine, assessment prompt, runtime code, PR, commit, or
  push is adopted here.
- Backend labels distinguish the preferred upstream OpenAI-compatible service
  from fallback Ollama OpenAI-compatible service.
