# V029 Stable Non-Ollama Backend Review Pointer

## Package

Review package:

`docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v029_stable_non_ollama_backend_build/`

## Purpose

This package documents the v029 attempt to recover or build a stable non-Ollama OpenAI-compatible Qwen backend, then establish a fresh `v020c` baseline before any further semantic prompt refinement.

## Key Evidence

- Final recommendation:
  `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v029_stable_non_ollama_backend_build/final_recommendation.md`
- Fresh backend-specific baseline:
  `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v029_stable_non_ollama_backend_build/new_backend_v020c_baseline.md`
- Stability matrix:
  `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v029_stable_non_ollama_backend_build/backend_stability_matrix.md`
- Baseline diagnosis:
  `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v029_stable_non_ollama_backend_build/diagnoses/v029_baseline_unacceptable_diagnosis.md`
- Backend feasibility and launch notes:
  `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v029_stable_non_ollama_backend_build/backend_feasibility_matrix.md`
  `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v029_stable_non_ollama_backend_build/backend_launch_log.md`
- Request/render/response trace manifests:
  `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v029_stable_non_ollama_backend_build/rendered_prompt_manifest.json`
  `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v029_stable_non_ollama_backend_build/request_shape_manifest.json`
  `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v029_stable_non_ollama_backend_build/response_trace_manifest.json`

## Current Status

- Non-Ollama backend launched: yes, vLLM OpenAI-compatible.
- Backend used: `vllm_quantized_qwen3_vl_8b_local_8000`.
- Served model name: `Qwen/Qwen3-VL-8B-Instruct`.
- Actual model root: `SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16`.
- Model source: public Hugging Face download/cache, no private token or paid API.
- Case-67 stability gate: passed.
- Sentinel stability gate: passed.
- Fresh v020c all-current baseline on this backend: `153 matches / 66 FNs / 25 FPs / 91 errors`.
- Prior v020c incumbent evidence remains: `186 matches / 33 FNs / 25 FPs / 58 errors`.
- Final v029 decision: `D. stable_backend_found_but_v020c_baseline_unacceptable_pause`.
- Semantic prompt refinement did not resume.

## Standing Candidate State

- `v020c_anchor_replay` / `v020c_extra_box_audit` remains the product/current incumbent under prior stable evidence.
- `v024l_v023s_no_wheel_track_ablation` remains high-recall learning evidence only.
- `v025a_v020c_compact_separate_body_recovery` remains rejected.
- `v024o_v024l_intact_building_piece_exclusion` remains partial/unscored and forbidden as scored evidence.

## Sanitization Note

The review copy keeps text evidence, JSON/CSV/YAML summaries, request-shape hashes, prompt/render/response traces, logs, scripts, and diagnoses. Raw image binaries, generated image artifacts, Python bytecode, PID files, and local command crumbs were intentionally omitted from the review repo mirror.

## Review Question For GPT-5.5 Pro

Does v029 justify pausing semantic prompt refinement until either:

- the exact 8B model can be served stably on suitable hardware,
- a different non-Ollama backend/model line is deliberately baselined as a new comparison surface, or
- the project moves away from prompt-only optimization toward non-prompt detector/eval/runtime levers?
