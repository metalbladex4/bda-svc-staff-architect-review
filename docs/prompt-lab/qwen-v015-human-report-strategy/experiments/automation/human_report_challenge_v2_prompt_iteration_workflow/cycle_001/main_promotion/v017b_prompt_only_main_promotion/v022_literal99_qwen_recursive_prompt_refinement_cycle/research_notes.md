# v022 Research Notes

- Qwen3-VL official materials emphasize stronger 2D grounding and OpenAI-compatible serving.
- Qwen2.5-VL official grounding examples show concise JSON bbox prompts as the family pattern.
- Local v020/v021 evidence is the primary decision source for this cycle.

## 2026-05-05 Pivot Note After v022a-c

Sources checked:

- https://github.com/QwenLM/Qwen3-VL
- https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct
- https://qwenlm.github.io/blog/qwen2.5-vl/

Useful takeaway: Qwen's own grounding/localization material highlights spatial
grounding and JSON localization output, but the examples stay relatively
compact. After v022a-c all regressed from v020c, the next prompt should test
whether compressing v020c's winning behavior is safer than adding more audit
or filter wording.
