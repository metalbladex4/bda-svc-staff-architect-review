# v023 Final Recommendation

Generated: `2026-05-06T12:24:51.894864+00:00`

## Literal Target

- upstream error baseline: `74`
- literal 99% target: `<= 1` combined false negatives + false positives

## Current Incumbent

- `v020c_anchor_replay`: 186 matches / 33 FNs / 25 FPs (58 total errors)
- literal target met: `False`

## Pause Status

- The loop is paused by user request as of `2026-05-06`.
- `v024o_v024l_intact_building_piece_exclusion` was interrupted before the
  all-current run completed and is not an evaluated row.
- Use `pause_report_2026-05-06.md` for the complete v020c/v023/v024 iteration
  report and resume instructions.

## Recommendation

- Keep `v020c_anchor_replay` / `v020c_extra_box_audit` as the Qwen
  config-prompt incumbent.
- Treat `v024l_v023s_no_wheel_track_ablation` as the best high-recall learning
  branch, not a promotion candidate, because its false positives remain too
  high.
- Next high-leverage work should favor visual review plus non-prompt
  duplicate/tiling suppression or backend/post-processing rather than more
  long prompt-only building rules.

## Boundary

- This package is prompt-lab evidence only.
- No source truth, doctrine, assessment prompt, runtime code, PR, commit, or push is adopted here.
- Backend labels distinguish preferred upstream OpenAI-compatible service from fallback Ollama OpenAI-compatible service.
