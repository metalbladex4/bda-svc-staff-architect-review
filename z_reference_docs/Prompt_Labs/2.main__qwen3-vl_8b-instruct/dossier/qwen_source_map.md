# Qwen Source Map

This file records which local Qwen references inform the prompt work and why.

| Source | Most Relevant Takeaways | How It Should Affect This Lab |
| --- | --- | --- |
| `z_reference_docs/Prompting/Qwen/Qwen3-VL-8B-Instruct_Model_Card.md` | Qwen3-VL is strong at multi-image reasoning, spatial grounding, OCR, and evidence-based multimodal understanding. | Keep multi-image assessment prompts explicit and lean on structured, visually grounded outputs. |
| `z_reference_docs/Prompting/Qwen/Qwen_3_Chat_template_deep_dive_Prompting_Behavior.md` | Qwen's chat template cleanly separates system, user, assistant, and tool paths. | Keep this pipeline on the plain system + user path; do not mix in tool or XML patterns unless intentionally testing them. |
| `z_reference_docs/Prompting/Qwen/Alibaba_Cloud_vision_docs_for_Qwen-VL.md` | Qwen-VL supports single and multiple image inputs in one request with direct task text. | Phrase image roles explicitly in prompts and keep the actual ask in one clear user instruction block. |
| `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/2d_grounding.ipynb` | Qwen3-VL uses relative 0–1000 coordinates by default and responds well to direct “Locate every instance...” phrasing. | Preserve the current bbox convention and simplify detection prompts around direct grounding language. |
| `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/spatial_understanding.ipynb` | Spatial prompts are phrased as direct questions or direct point/region requests. | Favor narrow spatial instructions over verbose reasoning scripts. |
| `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/think_with_images.ipynb` | Tool-driven analysis exists in the broader Qwen ecosystem, but only when explicit tools are available. | Do not borrow tool-oriented prompt patterns into `bda-svc`; this repo does not expose those tools. |
| `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/ocr.ipynb` | Output-only tasks work well with simple format instructions such as “output only the text content.” | Use short, explicit output constraints for JSON-only and plain-text-only tasks. |

## Lab Implications

- Qwen docs are the primary authority for model tactics.
- BDA doctrine remains the primary authority for semantic correctness.
- General prompting guides are backup references, not the first place to pull
  tactics from for this model.
