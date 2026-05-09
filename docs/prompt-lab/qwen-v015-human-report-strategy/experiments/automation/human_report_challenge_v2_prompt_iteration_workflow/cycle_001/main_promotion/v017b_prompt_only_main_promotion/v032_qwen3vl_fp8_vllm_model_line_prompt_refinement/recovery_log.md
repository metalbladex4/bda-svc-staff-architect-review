# v032 Recovery Log

- Created v032 as a separate FP8 vLLM model-line prompt-refinement package.
- Verified the vLLM FP8 endpoint on `http://localhost:8000/v1` using `Qwen/Qwen3-VL-8B-Instruct-FP8`.
- Replayed exact v020c on the v032 sentinel: `42 / 7 / 15 / 22`, case 67 `10/1/2`.
- Ran v032a, v032b, v032c, and v032d micro-pack gates.
- v032a was an unintended no-op; v032b and v032c regressed; v032d matched micro total while improving FP pressure but weakening recall.
- Started v032d full all-current; stopped when case 110 timed out. The full run is invalid and unscored.
- Wrote diagnoses, comparison matrix, lessons, strategy state, final recommendation, and pause report.
