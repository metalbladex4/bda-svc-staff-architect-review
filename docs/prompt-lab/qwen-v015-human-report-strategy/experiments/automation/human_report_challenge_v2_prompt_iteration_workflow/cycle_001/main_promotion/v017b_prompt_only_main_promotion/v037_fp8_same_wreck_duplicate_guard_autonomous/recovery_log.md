# v037 Recovery Log

- Re-grounded in v036 synthesis, v035/v034 closeouts, and v033 timeout policy.
- Recovered and used the vLLM FP8 backend on `http://localhost:8000/v1`.
- Applied the v033 experiment-only retry policy: 180-second request timeout, max 2 retries, 5-second cooldown.
- Replayed exact v034a sentinel before candidate work.
- Ran v037a, v037b, v037c, and v037d one at a time.
- Stopped semantic prompt iteration after repeated micro-gate failures rather than scoring partial or unsafe evidence.
