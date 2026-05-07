# v028 Stable Backend Recovery Pointer

Status: published for GPT-5.5 Pro review.

Package path:

```text
docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v028_stable_backend_recovery_and_prompt_resume/
```

Primary files:

```text
final_recommendation.md
stability_decision.md
backend_inventory.md
local_model_inventory.md
backend_launch_attempts.md
deterministic_settings_probe.md
raw_request_replay_matrix.md
diagnoses/v028_stage1_backend_stability_diagnosis.md
```

Summary:

- v028 attempted to recover a stable local Qwen OpenAI-compatible backend.
- The original preferred `localhost:8000/v1` backend was unavailable before recovery.
- v028 created a cached/local deterministic Ollama model alias:
  `qwen3-vl:8b-instruct-v028-deterministic`.
- v028 launched an experiment-only Ollama-backed endpoint on
  `localhost:8000/v1`.
- Stage 1 still failed: exact v020c replay 1 collapsed to `1/10/9`, while
  exact replays 2 and 3 returned `9/2/4`; blank-line and trailing-space probes
  also collapsed.
- Stage 2 was not run.
- Semantic prompt refinement did not resume.
- v020c remains incumbent.
- v024l remains learning evidence only.
- v025a remains rejected.
- v024o remains partial/unscored and forbidden.

Review question:

```text
Does this v028 evidence justify continuing to pause prompt mutation until a
non-Ollama or otherwise proven-stable multimodal OpenAI-compatible backend is
available?
```
