# v027 Recovery Log

Runtime and validation events are appended by `scripts/run_v027_runtime_stability_gate.py`.

## 2026-05-07

- Created v027 scaffold and scratch-only instrumentation scripts.
- Preferred backend `http://localhost:8000/v1` was unavailable with connection refused.
- Fallback backend `http://localhost:11434/v1` was available and used as
  Ollama-backed OpenAI-compatible fallback.
- First run exposed a runner scaffold bug (`os` import missing) before model
  inference; fixed the runner and removed two scratch worktrees.
- Ran all seven Stage 1 case-67 probes.
- Stage 1 failed; Stage 2 was not run.
- Semantic prompt refinement did not resume.
