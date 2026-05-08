# v031 SGLang Qwen3-VL FP8 Surface Gate

Created: 2026-05-08T22:45:58Z

Purpose: test the Deep Research recommendation that the next strongest local serving surface is official `Qwen/Qwen3-VL-8B-Instruct-FP8`, with SGLang first and vLLM backup, before resuming semantic prompt refinement.

## Decision

Final decision: **F. vllm_qwen3vl_8b_fp8_red_do_not_resume**. Semantic prompt refinement remains paused.

SGLang launched after isolated environment fixes, but every case-67 probe returned `0/11/1`, so it is not a usable scoring surface. vLLM backup launched and passed case-67 plus sentinel stability, but the fresh all-current v020c baseline was `180 / 39 / 32 / 71`, which is red by the v031 acceptance gate and also reopens case 155 false positives (`2/0/2` versus old v020c `2/0/0`).

## Key Metrics

- Old product v020c: `186 / 33 / 25 / 58`.
- v031 vLLM FP8 v020c baseline: `180 / 39 / 32 / 71`.
- Office-negative guard: image_count `1`, negative-scene FPs `0`, abstention correct `1`.
- Case 101 excluded from all-current: `True`.

## Required Boundary

No promotion, no semantic prompt candidate, no source truth mutation, no runtime/product config mutation, no eval truth mutation, no Graphify/Mem0 update, and no use of v024o as scored evidence.
