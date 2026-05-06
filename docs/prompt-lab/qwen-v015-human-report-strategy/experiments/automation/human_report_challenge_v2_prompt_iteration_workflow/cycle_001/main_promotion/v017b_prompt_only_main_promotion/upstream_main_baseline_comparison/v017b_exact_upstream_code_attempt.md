# v017b Exact-Upstream-Code Compatibility Attempt

Generated: `2026-05-04T18:39:07.691627+00:00`

## What Ran

This was the practical upstream-code compatibility test requested after the pure
upstream endpoint was unavailable.

- Code path: current `upstream/main` at `f462ef4516b63ca1a2cd2434e75692f65d0e94cb`
- Scratch change: replaced only `prompts.detect_objects` with the accepted
  `v017b` prompt
- Endpoint: `OPENAI_BASE_URL=http://localhost:11434/v1`
- Backing server: Ollama OpenAI-compatible endpoint
- Model overrides: `qwen3-vl:8b-instruct` for detection and assessment
- Dataset: `human_report_challenge_v2_all_current_117_no101`
- Evaluator: same v2 manifest evaluator used by the existing comparison rows

This is **not** a pure upstream `localhost:8000/v1`/vLLM result. It is upstream
runtime code using an Ollama OpenAI-compatible backend.

## Results

| Pack | Images | Matches | FNs | FPs | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| all-current no-101 | 117 | 166 | 53 | 26 | `155` passed; `166` passed |
| office-negative guard | 1 | 1 | 0 | 0 | abstention passed |

Case checks:

- `155`: 2 match / 0 FN / 0 FP
- `166`: 1 match / 0 FN / 0 FP
- office-negative: 1 abstention-correct / 0 negative-scene FP

## Comparison Meaning

Against the existing local-Qwen `v017b` reference row, the upstream-code/Ollama
compatibility row gained `+1` match and `-1` FN, but increased raw FPs by `+4`.

Against the upstream/main prompt-controlled row, the upstream-code/Ollama
compatibility row had `-3` matches, `+3` FNs, and `+2` FPs, but it fixed the
corrected positive-control `155` behavior.

So the PR-safe story remains: `v017b` is a control-safety and target-boxing
improvement, especially for corrected positive controls, not a same-pack raw
metric winner over the current upstream prompt.

## Run Artifacts

- All-current summary: `runs/v017b_upstream_code_openai_compat/human_report_challenge_v2_all_current_117_no101_2026-05-04_182205Z/upstream_code_manifest_run_summary.json`
- Office-negative summary: `runs/v017b_upstream_code_openai_compat_office_negative/legacy_abstention_guard_office_negative_2026-05-04_182132Z/upstream_code_manifest_run_summary.json`
- Machine-readable attempt record: `v017b_exact_upstream_code_attempt.json`

## Boundaries

- No source reports or references were changed.
- No doctrine files were changed.
- No runtime adoption, commit, push, PR creation, Graphify refresh, or Mem0
  write happened in this comparison wave.
