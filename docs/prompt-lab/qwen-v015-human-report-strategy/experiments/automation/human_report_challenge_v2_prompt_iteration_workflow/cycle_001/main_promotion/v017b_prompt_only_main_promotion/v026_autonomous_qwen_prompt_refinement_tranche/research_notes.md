# v026 Research Notes

- Local doctrine and v025 visual/autopsy evidence are primary for candidate design.
- External research may inform prompt tactics but cannot override local eval evidence.

## Local References Consulted During Tranche

- `/home/williambenitez1/Capstone/z_reference_docs/GPT-Pro_collab/bda_svc_qwen_prompt_engineering_deep_research_bundle.md`
  - useful lesson: keep prompt-engineering first, but use visual review and
    deterministic support methods to diagnose remaining failures; current best
    remains `v020c` and `v024l` is learning evidence only.
- `/home/williambenitez1/Capstone/z_reference_docs/Prompting/Qwen/Qwen3-VL-8B-Instruct_Model_Card.md`
  - useful lesson: Qwen3-VL has stronger 2D grounding and spatial perception,
    which motivated the compact Qwen-style and quadrant-scan experiments.
- `/home/williambenitez1/Capstone/z_reference_docs/Prompting/Qwen/Alibaba_Cloud_vision_docs_for_Qwen-VL.md`
  - useful lesson: Qwen-family localization examples emphasize JSON bbox output,
    which motivated the compact JSON grounding experiment.

No new web research was used during this tranche because local source-grounded
research bundles were sufficient and the blocking issue became fallback-backend
prompt-shape sensitivity rather than a lack of prompt-pattern ideas.
