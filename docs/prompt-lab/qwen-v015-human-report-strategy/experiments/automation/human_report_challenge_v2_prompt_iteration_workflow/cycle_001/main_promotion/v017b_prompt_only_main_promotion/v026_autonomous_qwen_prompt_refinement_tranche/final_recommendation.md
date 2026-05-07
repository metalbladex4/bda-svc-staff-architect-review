# v026 Final Recommendation

Updated: `2026-05-07T06:01:04Z`

## Status

`paused_runtime_shape_sensitivity`

This tranche is paused under the runtime-validity stop rule, not because a
candidate merely failed. The preferred upstream OpenAI-compatible endpoint
`http://localhost:8000/v1` remained unavailable, so the tranche used the
authorized Ollama-backed OpenAI-compatible fallback at `http://localhost:11434/v1`.
On that fallback endpoint, exact `v020c` remained stable, but every real prompt
delta through `v026q` failed the sentinel gate, including a no-semantics
blank-line-only prompt-shape probe.

## Incumbent

- product incumbent: `v020c_anchor_replay` / `v020c_extra_box_audit`
- incumbent metrics: `186` matches / `33` FNs / `25` FPs / `58` errors
- fresh sentinel check during v026: `38` matches / `11` FNs / `11` FPs, case
  `67` at `9/2/4`, `155` at `2/0/0`, `166` at `1/0/0`

## Best Candidate

No v026 candidate beat `v020c`.

The only full-run rows that matched `v020c` were no-op/exact-replay artifacts:

- `v026a_fragment_context_precision_guard`: no effective prompt delta rendered;
  full `186/33/25/58`
- `v026c_vehicle_body_anchor_not_rowline`: no effective prompt delta rendered;
  full `186/33/25/58`
- `v026f_tight_box_occupancy_guard`: no effective prompt delta rendered; full
  `186/33/25/58`

The first correctly rendered occupancy guard was `v026g_actual_tight_occupancy_guard`;
it failed the micro-pack with case `67` at `2/9/9`.

## Candidate Pattern

Rendered prompt deltas that failed the sentinel gate:

| Candidate | Axis | Stage | M/FN/FP | Case 67 | Status |
| --- | --- | --- | ---: | ---: | --- |
| `v026b_audit_removal_only_lock` | audit-region negative lock | micro | `28/21/17` | `1/10/11` | rejected |
| `v026d_qwen_native_grounding_header` | opening grounding header | micro | `32/17/20` | `1/10/11` | rejected |
| `v026e_low_salience_separate_body_good_box` | separate-body good-box cue | micro | `31/18/18` | `1/10/11` | rejected |
| `v026g_actual_tight_occupancy_guard` | actual bad-box occupancy guard | micro | `30/19/17` | `2/9/9` | rejected |
| `v026h_remove_calibration_preamble` | remove calibration paragraph | micro | `36/13/12` | `7/4/5` | rejected |
| `v026i_remove_v019c_label_only` | remove final-balance version label | micro | `29/20/18` | `2/9/10` | rejected |
| `v026j_visible_body_occupancy_phrase` | rewrite tight-box phrase | micro | `32/17/20` | `2/9/10` | rejected |
| `v026k_unrelated_background_object_guard` | adjacent background object guard | micro | `33/16/25` | `2/9/11` | rejected |
| `v026l_compact_context_shadow_schema` | compact Qwen-style rewrite | micro | `33/16/24` | `2/9/10` | rejected |
| `v026m_target_guidance_before_context` | guidance-order ablation | micro | `29/20/23` | `1/10/11` | rejected |
| `v026n_dense_row_body_safety_cue` | protective dense-row cue | micro | `31/18/20` | `1/10/11` | rejected |
| `v026o_output_only_no_extra_keys` | output-only suffix cue | micro | `28/21/19` | `1/10/10` | rejected |
| `v026p_quadrant_scan_search_cue` | search-order cue | micro | `29/20/18` | `1/10/9` | rejected |
| `v026q_blank_line_shape_probe` | blank-line-only shape probe | micro | `29/20/16` | `1/10/9` | rejected |

## Decision

- Target `FN + FP <= 1` was not reached.
- Do not promote any v026 candidate.
- Keep `v020c_anchor_replay` as product/current Qwen incumbent.
- Treat `v024l` as high-recall learning evidence only.
- Keep `v025a` rejected.
- Keep `v024o` forbidden as scored evidence.

## Current Lesson

On the fallback Ollama-backed OpenAI-compatible endpoint, v020c appears to be a
brittle exact-prompt local optimum. The sentinel gate is doing its job: it
prevented many all-current runs that would have collapsed dense-row behavior,
especially case `67`.

The blank-line-only `v026q` failure is the strongest new signal. It says that
continuing autonomous mutation on this fallback endpoint is likely to measure
prompt-byte/shape sensitivity rather than meaningful prompt-engineering gains.

## Recommended Resume

Resume only after one of these is true:

1. The preferred `http://localhost:8000/v1` backend is available and can replay
   exact `v020c` plus a blank-line/no-semantics probe.
2. The user explicitly authorizes continuing random/micro prompt search on the
   fallback endpoint despite the blank-line sensitivity.
3. The user authorizes a prompt-engineering-first workflow that uses visual
   review plus deterministic non-promoted post-processing simulations as
   diagnostic support before another prompt candidate.

Suggested resume command after backend recovery:

```bash
cd /home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement
python3 docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v026_autonomous_qwen_prompt_refinement_tranche/scripts/run_v026_tranche.py baseline-micro
```

Boundary: no product config, doctrine, assessment prompt, runtime code, eval
truth, commit, push, PR, Graphify refresh, or Mem0 write was adopted by this
tranche.
