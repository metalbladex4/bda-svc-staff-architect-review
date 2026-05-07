# V027 Runtime Rendering Stability Gate Pointer

## Review Package

```text
docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v027_runtime_rendering_stability_gate/
```

## Purpose

This package adds the instrumentation missing from v026: final rendered prompt
hashes, sanitized request-shape hashes, image serialization hashes, response
hashes, JSON repair/validation traces, and eval summaries.

The review question for GPT-5.5 Pro is:

```text
Does v027 justify keeping semantic prompt mutation paused until the preferred
backend or fallback runtime can pass a repeatability/request-shape stability
gate?
```

## Key Files

- Runtime evidence:
  `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v027_runtime_rendering_stability_gate/runtime_shape_probe_evidence.md`
- Final recommendation:
  `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v027_runtime_rendering_stability_gate/final_recommendation.md`
- Stage 1 diagnosis:
  `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v027_runtime_rendering_stability_gate/diagnoses/v027_stage1_case67_stability_diagnosis.md`
- Rendered prompt manifest:
  `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v027_runtime_rendering_stability_gate/rendered_prompt_manifest.json`
- Request shape manifest:
  `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v027_runtime_rendering_stability_gate/request_shape_manifest.json`
- Response trace manifest:
  `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v027_runtime_rendering_stability_gate/response_trace_manifest.json`
- Stability matrix:
  `docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v027_runtime_rendering_stability_gate/stability_matrix.md`

## Current Status

- Stage 1 failed on the fallback endpoint.
- Stage 2 was not run.
- Semantic prompt refinement did not resume.
- Preferred backend `http://localhost:8000/v1` was unavailable.
- Fallback backend `http://localhost:11434/v1` was used and labeled as
  Ollama-backed OpenAI-compatible.
- `v020c_anchor_replay` / `v020c_extra_box_audit` remains frozen as incumbent:
  `186 / 33 / 25 / 58`.
- `v024l` remains high-recall learning evidence only.
- `v025a` remains rejected.
- `v024o` remains partial/unscored and forbidden as scored evidence.

## Stage 1 Headline

Exact v020c/no-op probes used the same rendered prompt hash and request-shape
hash, but produced both collapsed and stable raw detection response hashes.

- collapsed: `1/10/9`, raw response hash `cc06a04e...`
- stable: `9/2/4`, raw response hash `91d10452...`

That points away from overlay application or placeholder rendering as the
primary explanation, and toward fallback backend/raw-response instability or an
unobserved backend serialization/cache state.

Raw image overlays were not copied to the review repo; text, JSON, YAML,
summaries, traces, and prompt artifacts were copied.
