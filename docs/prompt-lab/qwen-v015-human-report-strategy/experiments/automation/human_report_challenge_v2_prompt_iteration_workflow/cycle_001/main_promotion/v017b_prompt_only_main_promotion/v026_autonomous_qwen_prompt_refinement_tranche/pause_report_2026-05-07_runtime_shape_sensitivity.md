# v026 Pause Report: Runtime Shape Sensitivity

Generated: `2026-05-07T06:01:04Z`

## Why The Tranche Paused

The tranche paused under the runtime-validity stop rule.

This is not a promotion decision and not a stop caused by ordinary candidate
failure. The preferred upstream OpenAI-compatible backend
`http://localhost:8000/v1` was repeatedly unavailable, so the authorized
Ollama-backed OpenAI-compatible fallback at `http://localhost:11434/v1` was
used. On that fallback endpoint:

- exact v020c remained stable on a fresh sentinel check
- every rendered prompt delta failed the sentinel gate
- even `v026q_blank_line_shape_probe`, which added only one blank line and no
  detection semantics, collapsed case `67`

That makes further autonomous prompt mutation on the fallback endpoint
untrustworthy as a prompt-engineering improvement loop.

## Current Incumbent

`v020c_anchor_replay` remains incumbent.

All-current incumbent metrics:

- matches: `186`
- false negatives: `33`
- false positives: `25`
- combined errors: `58`

Fresh v026 sentinel check:

- matches: `38`
- false negatives: `11`
- false positives: `11`
- combined errors: `22`
- case `67`: `9/2/4`
- case `155`: `2/0/0`
- case `166`: `1/0/0`
- office-negative: `pass`

## Candidates Completed

Full all-current rows:

- `v026a_fragment_context_precision_guard`: `186/33/25/58`; no effective prompt
  delta rendered, exact-replay artifact
- `v026c_vehicle_body_anchor_not_rowline`: `186/33/25/58`; no effective prompt
  delta rendered, exact-replay artifact
- `v026f_tight_box_occupancy_guard`: `186/33/25/58`; no effective prompt delta
  rendered, exact-replay artifact

Micro-pack rejected rows:

- `v026b_audit_removal_only_lock`: `28/21/17`, case `67` `1/10/11`
- `v026d_qwen_native_grounding_header`: `32/17/20`, case `67` `1/10/11`
- `v026e_low_salience_separate_body_good_box`: `31/18/18`, case `67` `1/10/11`
- `v026g_actual_tight_occupancy_guard`: `30/19/17`, case `67` `2/9/9`
- `v026h_remove_calibration_preamble`: `36/13/12`, case `67` `7/4/5`
- `v026i_remove_v019c_label_only`: `29/20/18`, case `67` `2/9/10`
- `v026j_visible_body_occupancy_phrase`: `32/17/20`, case `67` `2/9/10`
- `v026k_unrelated_background_object_guard`: `33/16/25`, case `67` `2/9/11`
- `v026l_compact_context_shadow_schema`: `33/16/24`, case `67` `2/9/10`
- `v026m_target_guidance_before_context`: `29/20/23`, case `67` `1/10/11`
- `v026n_dense_row_body_safety_cue`: `31/18/20`, case `67` `1/10/11`
- `v026o_output_only_no_extra_keys`: `28/21/19`, case `67` `1/10/10`
- `v026p_quadrant_scan_search_cue`: `29/20/18`, case `67` `1/10/9`
- `v026q_blank_line_shape_probe`: `29/20/16`, case `67` `1/10/9`

## Main Lessons

- Do not branch from `v024l`; it remains high-recall learning evidence only.
- Do not use `v025a`; it remains rejected.
- Do not use `v024o`; it remains partial/unscored.
- Do not edit `EXTRA-BOX AUDIT`, `FINAL BALANCE`, context-shadow order, or
  target guidance order on the fallback backend without a better backend trust
  gate.
- On the fallback backend, v020c exact prompt bytes appear load-bearing.
- The sentinel micro-pack is valuable: it prevented many all-current runs that
  would have collapsed dense rows.

## Resume Plan

Before authoring another Qwen prompt candidate:

1. Restore or start the preferred `http://localhost:8000/v1` endpoint.
2. Verify it lists `Qwen/Qwen3-VL-8B-Instruct`.
3. Run exact v020c sentinel replay.
4. Run a no-semantics prompt-shape probe.
5. Resume candidate authoring only if both are stable.

Resume command:

```bash
cd /home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement
python3 docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v026_autonomous_qwen_prompt_refinement_tranche/scripts/run_v026_tranche.py baseline-micro
```

## Boundaries Preserved

- no product `src/bda_svc/pipeline/config.yaml` modification
- no doctrine modification
- no assessment-prompt modification
- no runtime-code modification
- no eval-truth modification
- no promotion
- no commit or push
- no Graphify refresh
- no Mem0 write
