# v029 Final Recommendation

Updated: `2026-05-08T01:12:49Z`

Decision: `D. stable_backend_found_but_v020c_baseline_unacceptable_pause`

## Summary

v029 successfully launched a non-Ollama local vLLM OpenAI-compatible backend on `localhost:8000/v1` using a public quantized Qwen3-VL 8B derivative. The backend passed the case-67 stability probes and the sentinel stability probes. However, the fresh v020c all-current baseline on this backend was much worse than the old incumbent baseline, so semantic prompt refinement did not resume.

## Backend

- server: `vLLM`
- endpoint: `http://localhost:8000/v1`
- served model name: `Qwen/Qwen3-VL-8B-Instruct`
- actual model root: `SherlockID365/Qwen3-VL-8B-Instruct-quantized.w4a16`
- model source: public HF download/cache, no token or private credential

## Stability

- Stage 1 case-67 stability: passed
- Stage 2 sentinel stability: passed
- case 67 exact replays: `8/3/7`, `8/3/7`, `8/3/7`
- blank-line probes: `9/2/7`, `9/2/8`
- trailing-space probe: `8/3/7`
- no-op roundtrip: `9/2/8`
- sentinel exact replays: `9/2/5`, `9/2/5`
- sentinel blank-line: `9/2/9`
- sentinel trailing-space: `9/2/4`
- sentinel no-op: `9/2/5`

## Fresh v020c Baseline

- old v020c: `186 / 33 / 25 / 58`
- vLLM quantized v020c: `153 / 66 / 25 / 91`
- delta: `+33` combined errors
- office-negative: passed
- case 155: passed
- case 166: passed

## Recommendation

Do not resume autonomous semantic prompt refinement on this backend. The backend is repeatable enough, but the quantized model baseline is not close enough to the old incumbent behavior to make prompt deltas comparable.

The next fix is either:

- recover a stable non-Ollama backend for the exact `Qwen/Qwen3-VL-8B-Instruct` model on hardware with enough VRAM, or
- test a smaller official Qwen3-VL model as a new model line with its own baseline and expectations, not as a drop-in replacement for the old v020c evidence.

Product v020c remains the incumbent under prior stable evidence. v024l remains learning evidence only, v025a remains rejected, and v024o remains unscored/forbidden.
