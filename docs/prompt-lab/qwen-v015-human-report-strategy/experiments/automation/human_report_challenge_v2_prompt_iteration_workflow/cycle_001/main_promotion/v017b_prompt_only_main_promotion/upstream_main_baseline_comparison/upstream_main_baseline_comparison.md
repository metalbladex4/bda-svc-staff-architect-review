# Upstream/Main Baseline Comparison For v017b

Generated: `2026-05-04T18:39:07.691627+00:00`

## Question

How does accepted Qwen `v017b` compare with the current `upstream/main`
`src/bda_svc/pipeline/config.yaml` prompt on the same
`human_report_challenge_v2_all_current_117_no101` dataset?

## Sources

- Upstream config snapshot: `snapshots/upstream_main_config_f462ef4516b63ca1a2cd2434e75692f65d0e94cb.yaml`
- Upstream commit: `f462ef4516b63ca1a2cd2434e75692f65d0e94cb`
- Upstream config SHA-256: `6389404387e2c1034f108d3d961cba144411bf8ffb11c9fda6fd7d51417fca36`
- Prompt-controlled overlay: `upstream_main_prompt_controlled_overlay.yaml`
- Prompt-controlled run summary: `runs/prompt_controlled_upstream_main/human_report_challenge_v2_all_current_117_no101_2026-05-04_174441Z/candidate_manifest_run_summary.json`
- Practical upstream-code/Ollama run summary: `runs/v017b_upstream_code_openai_compat/human_report_challenge_v2_all_current_117_no101_2026-05-04_182205Z/upstream_code_manifest_run_summary.json`
- Practical upstream-code/Ollama office-negative summary: `runs/v017b_upstream_code_openai_compat_office_negative/legacy_abstention_guard_office_negative_2026-05-04_182132Z/upstream_code_manifest_run_summary.json`
- v017b reference: `../main_promotion_gate_result.json` and `../promotion_override_decision.md`

## Metric Comparison

| Row | Code path | Backend | Images | Matches | FNs | FPs | `155` | `166` | Office-negative |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| `upstream/main` prompt-controlled | local Qwen prompt-lab runner | Ollama native/local Qwen | 117 | 169 | 50 | 24 | 0 match / 2 FN / 1 FP | 1 match / 0 FN / 0 FP | pass |
| `v017b` accepted prompt | local Qwen prompt-lab runner | Ollama native/local Qwen | 117 | 165 | 54 | 22 raw / 21 effective | 2 match / 0 FN / 0 FP | 1 match / 0 FN / 0 FP | pass |
| `v017b_upstream_code_ollama_openai_compat` | current `upstream/main` code | Ollama OpenAI-compatible `11434/v1` | 117 | 166 | 53 | 26 | 2 match / 0 FN / 0 FP | 1 match / 0 FN / 0 FP | pass |
| exact upstream default runtime | current `upstream/main` code | `localhost:8000/v1` | n/a | n/a | n/a | n/a | n/a | n/a | not run: endpoint unavailable |

Delta, existing `v017b` local-Qwen minus `upstream/main` prompt-controlled:

- Matches: `-4`
- False negatives: `+4`
- Raw false positives: `-2`
- Effective extra-target false positives: `-3`

Delta, `v017b_upstream_code_ollama_openai_compat` minus existing `v017b` local-Qwen:

- Matches: `+1`
- False negatives: `-1`
- Raw false positives: `+4`

Delta, `v017b_upstream_code_ollama_openai_compat` minus `upstream/main` prompt-controlled:

- Matches: `-3`
- False negatives: `+3`
- False positives: `+2`

## Interpretation

The current upstream/main prompt-controlled baseline still produced the strongest
raw same-pack totals: `169` matches and `50` FNs. The existing accepted `v017b`
row is cleaner on false positives and corrected positive-control behavior, but
it is not a raw recall improvement over current upstream/main on this pack.

The practical upstream-code/Ollama compatibility row proves the v017b prompt can
run through current upstream's OpenAI-compatible client path. It scored `166`
matches, `53` FNs, and `26` FPs, while passing corrected positive controls `155`
and `166` and the office-negative abstention guard. That row does **not** make
v017b a raw metric winner either; it mainly confirms compatibility plus the
same corrected-control behavior.

The strongest reviewer-safe `v017b` claim remains precision/control safety and
prompt discipline, especially the corrected `155` behavior. Do not frame it as
broad raw metric superiority over `upstream/main`.

## Exact Upstream Runtime Attempt

Exact upstream runtime at the default endpoint was not executed because the
required OpenAI-compatible endpoint was unavailable:

- endpoint checked: `http://localhost:8000/v1/models`
- required model: `Qwen/Qwen3-VL-8B-Instruct`
- result: `not_run_endpoint_unavailable`
- error: `URLError: <urlopen error [Errno 111] Connection refused>`

The practical compatibility row used `http://localhost:11434/v1` and must be
labeled as upstream-code plus Ollama OpenAI compatibility, not pure upstream
vLLM/server.

## PR-Safe Language

Use this instead of claiming broad recall improvement:

```markdown
On the same `human_report_challenge_v2_all_current_117_no101` pack, the current
`upstream/main` detect prompt produced `169` matches, `50` false negatives, and
`24` false positives in a prompt-controlled local Qwen run, but failed corrected
positive-control case `155`. The proposed `v017b` prompt produced `165`
matches, `54` false negatives, and `22` raw false positives / `21` effective
extra-target false positives, while passing positive controls `155` and `166`
and the office-negative abstention guard. A practical upstream-code run using
Ollama's OpenAI-compatible endpoint also passed `155`, `166`, and office-negative
with `166` matches, `53` false negatives, and `26` false positives. The validation
claim is therefore corrected-control and prompt-discipline improvement, not raw
same-pack metric superiority over `upstream/main`.
```

## Boundaries

- No source reports or references were changed.
- No doctrine files were changed.
- No runtime adoption, commit, push, PR creation, Graphify refresh, or Mem0
  write happened in this comparison wave.
