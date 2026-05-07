=== CANDIDATE COMPLETE ===
candidate: v020c_anchor_replay
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 38
false_negatives: 11
false_positives: 11
combined_errors: 22
vs_v020c_errors_delta: n/a
case_67: 9/2/4
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: baseline_micro
main_lesson: baseline
next_axis: sentinel calibration
==========================

=== CANDIDATE COMPLETE ===
candidate: v026a_fragment_context_precision_guard
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 38
false_negatives: 11
false_positives: 11
combined_errors: 22
vs_v020c_errors_delta: n/a
case_67: 9/2/4
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: learning_evidence
main_lesson: Micro-pack passed dense/control gate; candidate earned an all-current run.
next_axis: Run full all-current for the same candidate.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026a_fragment_context_precision_guard
backend: ollama_openai_compat_fallback_11434
stage: full_all_current
matches: 186
false_negatives: 33
false_positives: 25
combined_errors: 58
vs_v020c_errors_delta: 0
case_67: 9/2/4
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: learning_evidence
main_lesson: Full run did not beat v020c; retain as learning evidence.
next_axis: Try a smaller v020c load-bearing ordering ablation.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026b_audit_removal_only_lock
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 28
false_negatives: 21
false_positives: 17
combined_errors: 38
vs_v020c_errors_delta: n/a
case_67: 1/10/11
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: rejected
main_lesson: Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
next_axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026c_vehicle_body_anchor_not_rowline
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 38
false_negatives: 11
false_positives: 11
combined_errors: 22
vs_v020c_errors_delta: n/a
case_67: 9/2/4
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: learning_evidence
main_lesson: Micro-pack passed dense/control gate; candidate earned an all-current run.
next_axis: Run full all-current for the same candidate.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026c_vehicle_body_anchor_not_rowline
backend: ollama_openai_compat_fallback_11434
stage: full_all_current
matches: 186
false_negatives: 33
false_positives: 25
combined_errors: 58
vs_v020c_errors_delta: 0
case_67: 9/2/4
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: learning_evidence
main_lesson: Full run did not beat v020c; retain as learning evidence.
next_axis: Try a smaller v020c load-bearing ordering ablation.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026d_qwen_native_grounding_header
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 32
false_negatives: 17
false_positives: 20
combined_errors: 37
vs_v020c_errors_delta: n/a
case_67: 1/10/11
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: rejected
main_lesson: Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
next_axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026e_low_salience_separate_body_good_box
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 31
false_negatives: 18
false_positives: 18
combined_errors: 36
vs_v020c_errors_delta: n/a
case_67: 1/10/11
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: rejected
main_lesson: Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
next_axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026f_tight_box_occupancy_guard
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 38
false_negatives: 11
false_positives: 11
combined_errors: 22
vs_v020c_errors_delta: n/a
case_67: 9/2/4
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: learning_evidence
main_lesson: Micro-pack passed dense/control gate; candidate earned an all-current run.
next_axis: Run full all-current for the same candidate.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026f_tight_box_occupancy_guard
backend: ollama_openai_compat_fallback_11434
stage: full_all_current
matches: 186
false_negatives: 33
false_positives: 25
combined_errors: 58
vs_v020c_errors_delta: 0
case_67: 9/2/4
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: learning_evidence
main_lesson: Full run did not beat v020c; retain as learning evidence.
next_axis: Try a smaller v020c load-bearing ordering ablation.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026g_actual_tight_occupancy_guard
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 30
false_negatives: 19
false_positives: 17
combined_errors: 36
vs_v020c_errors_delta: n/a
case_67: 2/9/9
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: rejected
main_lesson: Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
next_axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026h_remove_calibration_preamble
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 36
false_negatives: 13
false_positives: 12
combined_errors: 25
vs_v020c_errors_delta: n/a
case_67: 7/4/5
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: rejected
main_lesson: Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
next_axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026i_remove_v019c_label_only
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 29
false_negatives: 20
false_positives: 18
combined_errors: 38
vs_v020c_errors_delta: n/a
case_67: 2/9/10
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: rejected
main_lesson: Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
next_axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026j_visible_body_occupancy_phrase
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 32
false_negatives: 17
false_positives: 20
combined_errors: 37
vs_v020c_errors_delta: n/a
case_67: 2/9/10
case_155: 2/0/2
case_166: 1/0/0
office_negative: pass
status: rejected
main_lesson: Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
next_axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026k_unrelated_background_object_guard
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 33
false_negatives: 16
false_positives: 25
combined_errors: 41
vs_v020c_errors_delta: n/a
case_67: 2/9/11
case_155: 2/0/1
case_166: 1/0/0
office_negative: pass
status: rejected
main_lesson: Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
next_axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026l_compact_context_shadow_schema
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 33
false_negatives: 16
false_positives: 24
combined_errors: 40
vs_v020c_errors_delta: n/a
case_67: 2/9/10
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: rejected
main_lesson: Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
next_axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026m_target_guidance_before_context
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 29
false_negatives: 20
false_positives: 23
combined_errors: 43
vs_v020c_errors_delta: n/a
case_67: 1/10/11
case_155: 2/0/1
case_166: 1/0/0
office_negative: pass
status: rejected
main_lesson: Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
next_axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026n_dense_row_body_safety_cue
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 31
false_negatives: 18
false_positives: 20
combined_errors: 38
vs_v020c_errors_delta: n/a
case_67: 1/10/11
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: rejected
main_lesson: Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
next_axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026o_output_only_no_extra_keys
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 28
false_negatives: 21
false_positives: 19
combined_errors: 40
vs_v020c_errors_delta: n/a
case_67: 1/10/10
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: rejected
main_lesson: Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
next_axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026p_quadrant_scan_search_cue
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 29
false_negatives: 20
false_positives: 18
combined_errors: 38
vs_v020c_errors_delta: n/a
case_67: 1/10/9
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: rejected
main_lesson: Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
next_axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
==========================

=== CANDIDATE COMPLETE ===
candidate: v026q_blank_line_shape_probe
backend: ollama_openai_compat_fallback_11434
stage: micro_pack_only
matches: 29
false_negatives: 20
false_positives: 16
combined_errors: 36
vs_v020c_errors_delta: n/a
case_67: 1/10/9
case_155: 2/0/0
case_166: 1/0/0
office_negative: pass
status: rejected
main_lesson: Micro-pack rejected the candidate before all-current, preserving model time and protecting case 67/control gates.
next_axis: Use a v020c load-bearing ordering ablation or remove the new guard entirely before another hypothesis.
==========================
