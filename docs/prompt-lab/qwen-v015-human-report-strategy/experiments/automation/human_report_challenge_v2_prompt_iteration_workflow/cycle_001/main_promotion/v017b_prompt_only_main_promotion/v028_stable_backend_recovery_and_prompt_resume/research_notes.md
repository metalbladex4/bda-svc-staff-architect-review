# v028 Research Notes

## vLLM

- Source: Context7 vLLM docs, multimodal/OpenAI-compatible serving snippets.
- URL: https://docs.vllm.ai/en/latest/features/multimodal_inputs
- Useful note: vLLM documents `vllm serve <multimodal-model>` and
  OpenAI-compatible multimodal chat requests using user content lists with text
  and `image_url` items. It also documents seed-based deterministic examples.
- Local impact: vLLM would be a better target for the preferred backend, but it
  was not installed and the HF Qwen3-VL model was not cached.

## Hugging Face Model Metadata

- Source: Hugging Face repo details for `Qwen/Qwen3-VL-8B-Instruct`.
- URL: https://hf.co/Qwen/Qwen3-VL-8B-Instruct
- Useful note: the model is public, Apache-2.0, image-text-to-text, and not
  gated/private.
- Local impact: no download was performed because the full model was not cached
  and a blind vLLM/Transformers install plus full-model pull was not judged a
  safe recovery step on the current 16 GB VRAM machine.

## Ollama

- Source: official Ollama Modelfile Reference.
- URL: https://github.com/ollama/ollama/blob/main/docs/modelfile.mdx
- Useful note: `seed`, `temperature`, `top_k`, and `top_p` are documented
  Modelfile parameters.
- Local impact: v028 tested those deterministic controls directly. They did not
  make the Ollama-backed path pass the stability gate.
