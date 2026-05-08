# Deep Research Summary

Deep Research guidance for v031 selected official `Qwen/Qwen3-VL-8B-Instruct-FP8` as the next strongest serving-surface experiment. The intended order was SGLang first, vLLM backup second, and Transformers only as a debug path.

Reasoning preserved in this package:

- The FP8 surface is official Qwen and closer to exact `Qwen/Qwen3-VL-8B-Instruct` than the third-party SherlockID365 w4a16 surface from v029.
- SGLang and vLLM are preferred active serving stacks for this kind of local OpenAI-compatible multimodal backend.
- TGI was not pursued because the research guidance marked it as maintenance-mode/not first choice.
- Local eval remains authoritative; external guidance only selected the serving-surface experiment.

Outcome: SGLang launched but failed behaviorally; vLLM backup was mechanically stable but red by baseline acceptance.
