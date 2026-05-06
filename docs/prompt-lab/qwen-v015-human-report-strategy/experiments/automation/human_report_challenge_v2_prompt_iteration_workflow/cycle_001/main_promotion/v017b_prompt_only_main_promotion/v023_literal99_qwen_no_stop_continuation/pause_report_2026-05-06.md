# v023/v024 Literal-99 Qwen Pause Report

Generated: `2026-05-06T08:33:09-04:00`

## Pause Status

- User requested pause before the in-flight `v024o_v024l_intact_building_piece_exclusion` all-current run completed.
- The runner was stopped. `v024o` has partial predictions only and must not be scored or treated as evidence.
- If the loop resumes from this point, rerun `v024o_v024l_intact_building_piece_exclusion` from scratch instead of resuming from partial outputs.
- No prompt from this continuation is promoted or adopted here.

## Current Champion

- `v020c_anchor_replay` remains the best row: `186` matches / `33` false negatives / `25` false positives (`58` total errors).
- Controls passed: case `155` = `2/0/0`, case `166` = `1/0/0`, office-negative = `1/1`.
- Literal 99 target was not met: target was `<=1` combined FN+FP; the best row remained `58` combined errors.
- Backend note: preferred `http://localhost:8000/v1` was unavailable after retry, so these rows used the authorized Ollama-backed OpenAI-compatible fallback at `http://localhost:11434/v1`.

## Best Challenger

- `v024l_v023s_no_wheel_track_ablation` is the best challenger / high-recall learning row: `188` matches / `31` FNs / `35` FPs (`66` total errors).
- It improved recall versus `v020c`, but the extra `10` false positives make it worse overall than `v020c`.
- Dense case behavior: `67` held at `9/2/3`, but `66` stayed FP-heavy at `8/0/6` and `84` lost one match versus `v020c` at `7/6/0`.
- Lesson: removing the `wheel/track contact` support phrase from the v023s branch helped enough to preserve row `67`, but it did not solve the FP burden.

## Iteration Matrix

| Prompt | Matches | FNs | FPs | Errors | 155 | 166 | Office | Status |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| `v020c_anchor_replay` | 186 | 33 | 25 | 58 | 2/0/0 | 1/0/0 | 1/1 | `champion` |
| `v023a_visible_center_pin_map` | 177 | 42 | 33 | 75 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023b_dense_safe_singleton_audit` | 173 | 46 | 32 | 78 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023c_body_baseline_anchor` | 174 | 45 | 38 | 83 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023d_dust_row_antidrift_calibration` | 175 | 44 | 34 | 78 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023e_v020c_stability_rail` | 171 | 48 | 35 | 83 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023f_compact_shadow_audit` | 182 | 37 | 66 | 103 | 2/0/0 | 1/0/0 | 1/1 | `fp_explosion` |
| `v023g_compact_ruler_chain_veto` | 183 | 36 | 71 | 107 | 2/0/2 | 1/0/0 | 1/1 | `fp_explosion` |
| `v023h_unique_body_signature_ledger` | 173 | 46 | 49 | 95 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023i_official_style_count_lock` | 178 | 41 | 40 | 81 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023j_v020c_no_history_clean` | 174 | 45 | 30 | 75 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023k_v020c_missed_target_pass` | 172 | 47 | 35 | 82 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023l_v020c_silent_qa_loupe` | 175 | 44 | 35 | 79 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023m_v020c_perspective_depth_recall` | 171 | 48 | 32 | 80 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023n_v020c_locked_policy_header` | 173 | 46 | 32 | 78 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023o_v020c_output_contract_first` | 177 | 42 | 53 | 95 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023p_four_edge_boundary_detector` | 176 | 43 | 36 | 79 | 2/0/1 | 1/0/0 | 1/1 | `learning_only` |
| `v023q_v020c_edge_support_audit_swap` | 173 | 46 | 32 | 78 | 2/0/1 | 1/0/0 | 1/1 | `learning_only` |
| `v023r_dense_row_exception_precision_audit` | 175 | 44 | 36 | 80 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023s_qwen_native_conservative_json` | 190 | 29 | 37 | 66 | 2/0/0 | 1/0/0 | 1/1 | `high_recall_branch` |
| `v023t_qwen_native_duplicate_collapse` | 178 | 41 | 41 | 82 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023u_qwen_native_sparse_only_cleanup` | 180 | 39 | 34 | 73 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023v_qwen_native_nested_overlap_guard` | 182 | 37 | 42 | 79 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023w_qwen_native_building_centrality_guard` | 178 | 41 | 38 | 79 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023x_qwen_native_connected_body_only` | 180 | 39 | 48 | 87 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023y_qwen_native_row_count_discipline` | 180 | 39 | 42 | 81 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v023z_qwen_native_high_confidence_filter` | 178 | 41 | 37 | 78 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v024a_coco_instance_annotator` | 184 | 35 | 44 | 79 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v024b_v020c_imagewide_scan_first` | 175 | 44 | 40 | 84 | 2/0/2 | 1/0/0 | 1/1 | `learning_only` |
| `v024c_official_style_ground_all_targets` | 166 | 53 | 37 | 90 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v024d_v020c_recall_balance_before_audit` | 173 | 46 | 31 | 77 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v024e_v020c_bbox_physical_extent_calibration` | 168 | 51 | 30 | 81 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v024f_silent_three_role_arbiter` | 183 | 36 | 44 | 80 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v024g_v020c_visual_sequence_output` | 182 | 37 | 39 | 76 | 2/0/1 | 1/0/0 | 1/1 | `learning_only` |
| `v024h_v020c_dust_base_vehicle_body` | 174 | 45 | 30 | 75 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v024i_v023s_body_mass_only` | 183 | 36 | 40 | 76 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v024j_v023s_no_silhouette_ablation` | 179 | 40 | 39 | 79 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v024k_v023s_no_wall_roof_boundary_ablation` | 182 | 37 | 39 | 76 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v024l_v023s_no_wheel_track_ablation` | 188 | 31 | 35 | 66 | 2/0/0 | 1/0/0 | 1/1 | `best_challenger, high_recall_branch` |
| `v024m_v024l_bda_salience_gate` | 173 | 46 | 37 | 83 | 2/0/0 | 1/0/0 | 1/1 | `learning_only` |
| `v024n_v024l_building_only_detiling` | 181 | 38 | 102 | 140 | 2/0/0 | 1/0/0 | 1/1 | `fp_explosion` |
| `v024o_v024l_intact_building_piece_exclusion` | n/a | n/a | n/a | n/a | office-negative passed | n/a | 1/1 | `interrupted_partial_by_user_pause` |

## Dense-Case Anchors

| Prompt | 66 | 67 | 84 | 97 |
| --- | --- | --- | --- | --- |
| `v020c_anchor_replay` | 8/0/4 | 9/2/4 | 8/5/0 | 1/0/2 |
| `v023s_qwen_native_conservative_json` | 8/0/6 | 8/3/4 | 6/7/3 | 1/0/2 |
| `v024l_v023s_no_wheel_track_ablation` | 8/0/6 | 9/2/3 | 7/6/0 | 1/0/2 |
| `v024n_v024l_building_only_detiling` | 8/0/6 | 2/9/10 | 6/7/3 | 1/0/2 |

## Lessons Learned

- `v020c` remains the stable prompt incumbent. None of the v023/v024 continuation prompts beat its combined error count.
- Case `67` is still the brittle dense-row sentinel. Many edits that look reasonable globally collapse it to only `1-2` matches with `9-11` FNs/FPs.
- Exact wording and order are load-bearing. `v023j_v020c_no_history_clean` shows that simplifying v020c without preserving its complete structure loses the incumbent balance.
- `v023s` and `v024l` define a useful high-recall branch, but the recall gain comes with too many false positives for adoption.
- In the v023s support phrase ablations, `silhouette` and `exterior wall/roof boundary` were load-bearing for dense-row behavior; removing either collapsed case `67`.
- Removing the `wheel/track contact` support phrase produced the best v024 challenger (`v024l`), but did not reduce false positives enough.
- Broad BDA-salience wording has some signal for building/background FPs but globally harms dense-vehicle behavior.
- Long building-specific de-tiling sections are dangerous: `v024n` exploded to `102` FPs and should be treated as a hard warning against long building-only prompt sections.
- The next high-leverage improvement is probably not another near-neighbor prompt edit; it is visual review plus non-prompt duplicate/tiling suppression or backend/post-processing that preserves `v020c` dense recall.

## Resume Command

If the user asks to continue the paused prompt loop, rerun `v024o` fully from the Qwen `1.2` worktree:

```bash
uv run python docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v023_literal99_qwen_no_stop_continuation/scripts/run_v023_literal99_cycle.py run-candidate v024o_v024l_intact_building_piece_exclusion
```

Working directory:

```text
/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement
```

Do not use the partial `v024o` all-current predictions as an evaluated row.
