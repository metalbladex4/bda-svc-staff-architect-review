# v026 Lessons Learned

- Start from v020c. Do not branch from v024l or v025a.
- Do not place positive split/recovery cues in EXTRA-BOX AUDIT or FINAL BALANCE.
- Case 67 is a sentinel for dense-row localization drift.

## v026a_fragment_context_precision_guard micro_pack_only

- Micro-pack passed dense/control gate; candidate earned an all-current run.
- Next axis: Run full all-current for the same candidate.

## v026a_fragment_context_precision_guard full_all_current

- Full run did not beat v020c; retain as learning evidence.
- Next axis: Try a smaller v020c load-bearing ordering ablation.

## v026b_audit_removal_only_lock micro_pack_only

- Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
- Next axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.

## v026c_vehicle_body_anchor_not_rowline micro_pack_only

- Micro-pack passed dense/control gate; candidate earned an all-current run.
- Next axis: Run full all-current for the same candidate.

## v026c_vehicle_body_anchor_not_rowline full_all_current

- Full run did not beat v020c; retain as learning evidence.
- Next axis: Try a smaller v020c load-bearing ordering ablation.

## v026d_qwen_native_grounding_header micro_pack_only

- Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
- Next axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.

## v026e_low_salience_separate_body_good_box micro_pack_only

- Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
- Next axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.

## v026f_tight_box_occupancy_guard micro_pack_only

- Micro-pack passed dense/control gate; candidate earned an all-current run.
- Next axis: Run full all-current for the same candidate.

## v026f_tight_box_occupancy_guard full_all_current

- Full run did not beat v020c; retain as learning evidence.
- Next axis: Try a smaller v020c load-bearing ordering ablation.

## v026g_actual_tight_occupancy_guard micro_pack_only

- Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
- Next axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.

## v026h_remove_calibration_preamble micro_pack_only

- Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
- Next axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.

## v026i_remove_v019c_label_only micro_pack_only

- Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
- Next axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.

## v026j_visible_body_occupancy_phrase micro_pack_only

- Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
- Next axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.

## v026k_unrelated_background_object_guard micro_pack_only

- Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
- Next axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.

## v026l_compact_context_shadow_schema micro_pack_only

- Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
- Next axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.

## v026m_target_guidance_before_context micro_pack_only

- Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
- Next axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.

## v026n_dense_row_body_safety_cue micro_pack_only

- Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
- Next axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.

## v026o_output_only_no_extra_keys micro_pack_only

- Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
- Next axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.

## v026p_quadrant_scan_search_cue micro_pack_only

- Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
- Next axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.

## v026q_blank_line_shape_probe micro_pack_only

- Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
- Next axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.

## Pause Lesson

- Exact `v020c` remained stable on a fresh sentinel check after `v026q`: `38/11/11`, case `67` at `9/2/4`, controls passed.
- `v026q_blank_line_shape_probe` changed no detection semantics, only adding one blank line after `{categories}`, yet collapsed case `67` to `1/10/9`.
- The fallback endpoint is therefore unsafe for further autonomous prompt mutation unless the user explicitly wants prompt-byte random search on that endpoint.
- The next trustworthy route is to restore the preferred `http://localhost:8000/v1` OpenAI-compatible backend, then replay exact `v020c` and a no-semantics shape probe before authoring another detection prompt.
- Keep `v020c` as incumbent; no v026 candidate is replay-worthy.
