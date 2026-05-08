# V031 Qwen3-VL FP8 Surface Review Pointer

Package path in review repo:

`docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v031_sglang_qwen3vl_fp8_surface_gate/`

Primary review files:

- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v031_sglang_qwen3vl_fp8_surface_gate/final_recommendation.md`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v031_sglang_qwen3vl_fp8_surface_gate/surface_acceptance_decision.md` / `.json`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v031_sglang_qwen3vl_fp8_surface_gate/stability_matrix.md` / `.json`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v031_sglang_qwen3vl_fp8_surface_gate/v020c_baseline_comparison.md` / `.json`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v031_sglang_qwen3vl_fp8_surface_gate/sglang_launch_log.md` / `.json`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v031_sglang_qwen3vl_fp8_surface_gate/vllm_backup_launch_log.md` / `.json`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v031_sglang_qwen3vl_fp8_surface_gate/diagnoses/v031_surface_gate_diagnosis.md`
- `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v031_sglang_qwen3vl_fp8_surface_gate/live_metrics_log.md`

Current status:

- Old/product v020c remains incumbent under prior stable evidence: `186 / 33 / 25 / 58`.
- v024l remains high-recall learning evidence only: `188 / 31 / 35 / 66`.
- v025a remains rejected: `176 / 43 / 35 / 78`.
- v024o remains partial/unscored and forbidden as scored evidence.
- v031 SGLang official FP8 launched, but failed case 67 at `0 / 11 / 1` on every probe.
- v031 vLLM official FP8 passed case-67 and sentinel stability.
- v031 vLLM official FP8 fresh v020c all-current baseline was `180 / 39 / 32 / 71`, red by the acceptance gate.
- Case 155 regressed on vLLM FP8 from old v020c `2 / 0 / 0` to `2 / 0 / 2`.
- Office-negative guard passed: image_count `1`, negative-scene false positives `0`, abstention correct `1`.
- Semantic prompt refinement did not resume.
- No promotion was performed.

Next review question for GPT-5.5 Pro:

Does the available v031 evidence justify rejecting official Qwen3-VL-8B-Instruct-FP8 as the continuation surface for the existing v020c prompt branch, and should Codex next search for a closer exact-model serving path or open a separately scoped FP8 model-line baseline?
