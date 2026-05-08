# V030 Exact Model Surface Review Pointer

## Package

`docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v030_exact_model_or_surface_equivalence_gate/`

## Purpose

v030 tested whether Codex could recover a stable model/backend surface close enough to the old Qwen v020c surface to resume autonomous prompt engineering.

## Current Status

- Old/product incumbent remains `v020c_anchor_replay / v020c_extra_box_audit`: `186 matches / 33 FNs / 25 FPs / 58 errors`.
- `v024l_v023s_no_wheel_track_ablation` remains high-recall learning evidence only: `188 / 31 / 35 / 66`.
- `v025a_v020c_compact_separate_body_recovery` remains rejected: `176 / 43 / 35 / 78`.
- `v024o` remains partial/unscored and forbidden as scored evidence.
- v027/v028 showed Ollama fallback instability.
- v029 found a stable quantized vLLM backend, but its v020c baseline was unacceptable: `153 / 66 / 25 / 91`.
- v030 downloaded and launched exact public `Qwen/Qwen3-VL-8B-Instruct`, but no exact-model surface completed the BDA case-67 stability gate.

## Key Evidence

- Final recommendation: `.../v030_exact_model_or_surface_equivalence_gate/final_recommendation.md`
- Decision: `.../v030_exact_model_or_surface_equivalence_gate/surface_equivalence_decision.md`
- Exact model feasibility: `.../v030_exact_model_or_surface_equivalence_gate/exact_model_feasibility.md`
- Backend attempts: `.../v030_exact_model_or_surface_equivalence_gate/backend_launch_attempts.md`
- Stability matrix: `.../v030_exact_model_or_surface_equivalence_gate/stability_matrix.md`
- Baseline comparison: `.../v030_exact_model_or_surface_equivalence_gate/v020c_baseline_comparison.md`
- Diagnosis: `.../v030_exact_model_or_surface_equivalence_gate/diagnoses/v030_exact_model_operational_failure_diagnosis.md`

## Review Question For GPT-5.5 Pro

Does the v030 evidence justify keeping semantic prompt refinement paused until the exact/close Qwen serving surface can complete case-67 stability and establish a fresh acceptable v020c baseline?
