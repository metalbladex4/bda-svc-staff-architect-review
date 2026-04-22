# Gemma 4 Evidence Pack

This folder is the local evidence hub for the Gemma 4 model line bootstrap.

It preserves:

- local snapshots of the official docs and model-card pages
- selected official cookbook notebooks
- a source manifest with direct URLs
- one synthesis note for the prompt rules that matter operationally before the
  first Gemma BDA run

It now also supports a completed first live Gemma baseline run in the
branch-aware prompt lab, so this folder is no longer just preparation
material. It is now the standing local reference pack behind the active Gemma
`v000` baseline.

## Current Working Decision

- active local-first target: `gemma4:e4b`
- comparison-only size: `gemma4:e2b`
- reference-only sizes for now:
  - `gemma4:26b`
  - `gemma4:31b`

## Current Execution Status

- first live Gemma `v000` run:
  - completed
- active runtime model:
  - `gemma4:e4b`
- runtime note:
  - the system Ollama install remains `0.15.2`
  - the first live Gemma run used a user-local Ollama `0.21.0` runtime on
    `127.0.0.1:11435`
- first live run record:
  - `/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/v000/run01_2026-04-17_134308_EDT/`
- first live read:
  - equipment and negative-scene behavior held
  - `destroyed_building4` exposed the first major Gemma-specific failure

Why this is the current default:

- the Gemma 4 family is the chosen next model family for the new line
- `E4B` is the strongest realistic local-first option on this machine
- `E2B` is still worth preserving because it gives us a smaller comparison
  point without opening a second heavy infrastructure path
- `26B` and `31B` remain useful research references, but they are not the
  bootstrap target for the first local BDA worktree

## Folder Map

- `official_docs/`
  Local HTML snapshots of the core Google AI for Developers Gemma docs.
- `model_cards/`
  Local HTML snapshots of the official Google Gemma 4 model-card pages on
  Hugging Face plus the Ollama Gemma 4 library page.
- `prompting_behavior/`
  Local HTML snapshots of the Gemma 4 behavior docs most likely to affect BDA
  prompt work.
- `cookbooks/`
  Local copies of selected official Gemma cookbook notebooks.
- `context/`
  Local copies of Gemma 4 launch/context blog pages.
- `normalized_md/`
  Markdown mirrors of the pulled `.html` and `.ipynb` sources, formatted for
  easier search and prompt-work reuse while staying close to the originals.
- [SOURCE_MANIFEST.md](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/SOURCE_MANIFEST.md)
  Source URL manifest and why each source matters.
- [operational_prompt_rules.md](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/operational_prompt_rules.md)
  The first-pass synthesis note for Gemma-specific prompt behavior.
- [normalized_md/README.md](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/normalized_md/README.md)
  The normalization approach and regeneration instructions.

## Recommended Review Order

1. Read the synthesis note first:
   [operational_prompt_rules.md](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/operational_prompt_rules.md)
2. Review the source map:
   [SOURCE_MANIFEST.md](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/SOURCE_MANIFEST.md)
3. Open the core docs snapshots:
   - [gemma_overview.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/official_docs/gemma_overview.html)
   - [get_started.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/official_docs/get_started.html)
   - [run_framework_guidance.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/official_docs/run_framework_guidance.html)
   - [ollama_integration.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/official_docs/ollama_integration.html)
4. Review the size and capability references:
   - [gemma4_e2b_hf.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/model_cards/gemma4_e2b_hf.html)
   - [gemma4_e4b_hf.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/model_cards/gemma4_e4b_hf.html)
   - [gemma4_26b_a4b_hf.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/model_cards/gemma4_26b_a4b_hf.html)
   - [gemma4_31b_hf.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/model_cards/gemma4_31b_hf.html)
   - [gemma4_ollama_library.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/model_cards/gemma4_ollama_library.html)
5. Review the prompting-behavior docs that could change how we craft prompts:
   - [function_calling_gemma4.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/prompting_behavior/function_calling_gemma4.html)
   - [prompt_with_visual_data.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/prompting_behavior/prompt_with_visual_data.html)
   - [image_understanding.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/prompting_behavior/image_understanding.html)
   - [audio_processing.html](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/prompting_behavior/audio_processing.html)
6. Use the notebooks as practical implementation references:
   - [huggingface_inference.ipynb](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/cookbooks/huggingface_inference.ipynb)
   - [pytorch_gemma.ipynb](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/cookbooks/pytorch_gemma.ipynb)
   - [basic_text_prompting.ipynb](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/cookbooks/basic_text_prompting.ipynb)
   - [function_calling_gemma4.ipynb](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/cookbooks/function_calling_gemma4.ipynb)
   - [thinking.ipynb](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/cookbooks/thinking.ipynb)
   - [vision_image.ipynb](/home/williambenitez1/Capstone/z_reference_docs/Prompting/Google_Gemma/Gemma_4/cookbooks/vision_image.ipynb)

## Source Hierarchy

When there is any disagreement, use this precedence:

1. official Gemma docs on `ai.google.dev`
2. official Google Gemma 4 model cards on Hugging Face
3. official Google Gemma cookbook notebooks
4. Ollama library page for local runtime tag guidance
5. Google launch and developer blogs for context only

## Related Live Lab

The active Gemma branch-aware prompt lab is here:

- [3.1 feature lab README](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/README.md)
- [first live run manifest](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/v000/run01_2026-04-17_134308_EDT/RUN_MANIFEST.md)
- [initial comparison summary](/home/williambenitez1/Capstone/z_reference_docs/Prompt_Labs/3_gemma4-e4b/3.1_feat__gemma4-e4b__qwen-v009-workflow-bootstrap/experiments/runs/v000/run01_2026-04-17_134308_EDT/INITIAL_COMPARISON_SUMMARY.md)

## BDA Bootstrap Rule

This folder supports the Gemma 4 branch bootstrap only.

Bootstrap scope:

- image + text BDA work
- local-first inference assumptions
- prompt engineering and runtime behavior intake

Bootstrap non-goals:

- audio workflows
- video workflows
- hosted Gemini API integration
- Gemma fine-tuning
- 26B or 31B local promotion
