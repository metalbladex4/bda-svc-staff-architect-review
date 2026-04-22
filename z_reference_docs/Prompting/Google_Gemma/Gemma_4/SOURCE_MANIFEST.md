# Gemma 4 Source Manifest

This file maps each local artifact in the Gemma 4 evidence pack back to the
official source URL and explains why it is worth keeping.

## Core Official Docs

- [official_docs/gemma_overview.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/official_docs/gemma_overview.html)
  Source: <https://ai.google.dev/gemma/docs>
  Why keep it: family overview, official framing, and top-level capability map.

- [official_docs/get_started.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/official_docs/get_started.html)
  Source: <https://ai.google.dev/gemma/docs/get_started>
  Why keep it: official onboarding flow and model-access framing.

- [official_docs/run_framework_guidance.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/official_docs/run_framework_guidance.html)
  Source: <https://ai.google.dev/gemma/docs/run>
  Why keep it: framework/runtime overview and official size-selection guidance.

- [official_docs/ollama_integration.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/official_docs/ollama_integration.html)
  Source: <https://ai.google.dev/gemma/docs/integrations/ollama>
  Why keep it: official local-Ollama path and quantized local-run framing.

## Model Cards And Size References

- [model_cards/gemma4_e2b_hf.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/model_cards/gemma4_e2b_hf.html)
  Source: <https://huggingface.co/google/gemma-4-E2B>
  Why keep it: official Google Gemma 4 E2B card and smallest local comparison
  size.

- [model_cards/gemma4_e4b_hf.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/model_cards/gemma4_e4b_hf.html)
  Source: <https://huggingface.co/google/gemma-4-E4B>
  Why keep it: official Google Gemma 4 E4B card and current local-first active
  target.

- [model_cards/gemma4_26b_a4b_hf.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/model_cards/gemma4_26b_a4b_hf.html)
  Source: <https://huggingface.co/google/gemma-4-26B-A4B-it>
  Why keep it: official reference for the MoE size we are not adopting yet.

- [model_cards/gemma4_31b_hf.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/model_cards/gemma4_31b_hf.html)
  Source: <https://huggingface.co/google/gemma-4-31B-it>
  Why keep it: official reference for the dense large model and the quality
  ceiling within the family.

- [model_cards/gemma4_ollama_library.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/model_cards/gemma4_ollama_library.html)
  Source: <https://ollama.com/library/gemma4>
  Why keep it: local tag names and practical local size table for E2B, E4B,
  26B, and 31B.

## Prompting And Behavior Docs

- [prompting_behavior/function_calling_gemma4.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/prompting_behavior/function_calling_gemma4.html)
  Source: <https://ai.google.dev/gemma/docs/capabilities/text/function-calling-gemma4>
  Why keep it: structured tool-use patterns and prompt-format discipline for
  future agentic extensions.

- [prompting_behavior/prompt_with_visual_data.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/prompting_behavior/prompt_with_visual_data.html)
  Source: <https://ai.google.dev/gemma/docs/capabilities/vision/prompt-with-visual-data>
  Why keep it: multimodal prompting guidance with image-first usage patterns.

- [prompting_behavior/image_understanding.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/prompting_behavior/image_understanding.html)
  Source: <https://ai.google.dev/gemma/docs/capabilities/vision/image>
  Why keep it: official image-understanding/task framing relevant to BDA-like
  visual work.

- [prompting_behavior/audio_processing.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/prompting_behavior/audio_processing.html)
  Source: <https://ai.google.dev/gemma/docs/capabilities/audio>
  Why keep it: family-context reference for modality support.

## Official Cookbook Notebooks

- [cookbooks/huggingface_inference.ipynb](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/cookbooks/huggingface_inference.ipynb)
  Source: <https://github.com/google-gemma/cookbook/blob/main/docs/core/huggingface_inference.ipynb>

- [cookbooks/pytorch_gemma.ipynb](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/cookbooks/pytorch_gemma.ipynb)
  Source: <https://github.com/google-gemma/cookbook/blob/main/docs/core/pytorch_gemma.ipynb>

- [cookbooks/basic_text_prompting.ipynb](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/cookbooks/basic_text_prompting.ipynb)
  Source: <https://github.com/google-gemma/cookbook/blob/main/docs/capabilities/text/basic.ipynb>

- [cookbooks/function_calling_gemma4.ipynb](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/cookbooks/function_calling_gemma4.ipynb)
  Source: <https://github.com/google-gemma/cookbook/blob/main/docs/capabilities/text/function-calling-gemma4.ipynb>

- [cookbooks/thinking.ipynb](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/cookbooks/thinking.ipynb)
  Source: <https://github.com/google-gemma/cookbook/blob/main/docs/capabilities/thinking.ipynb>

- [cookbooks/vision_image.ipynb](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/cookbooks/vision_image.ipynb)
  Source: <https://github.com/google-gemma/cookbook/blob/main/docs/capabilities/vision/image.ipynb>

## Context And Launch References

- [context/gemma4_launch_blog.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/context/gemma4_launch_blog.html)
  Source: <https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/>

- [context/gemma4_edge_agentic_blog.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/context/gemma4_edge_agentic_blog.html)
  Source: <https://developers.googleblog.com/bring-state-of-the-art-agentic-skills-to-the-edge-with-gemma-4/>
