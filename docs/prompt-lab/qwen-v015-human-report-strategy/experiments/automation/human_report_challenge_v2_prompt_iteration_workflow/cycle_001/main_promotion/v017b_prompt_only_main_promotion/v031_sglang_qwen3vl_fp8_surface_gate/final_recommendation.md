# Final Recommendation

Final decision: **F. vllm_qwen3vl_8b_fp8_red_do_not_resume**.

SGLang launched, but failed the case-67 gate (`0/11/1` on every probe). vLLM backup launched and was mechanically stable, including blank-line and trailing-space probes, but the fresh v020c all-current baseline was `180 / 39 / 32 / 71`. That is red by the v031 acceptance gate.

The old/product Qwen incumbent remains `v020c_anchor_replay / v020c_extra_box_audit` under prior stable evidence at `186 / 33 / 25 / 58`. `v024l` remains high-recall learning evidence only. `v025a` remains rejected. `v024o` remains partial/unscored and forbidden as scored evidence.

Do not resume semantic prompt refinement on v031. The exact next fix is not prompt wording; it is a serving-surface decision: either recover a closer acceptable official Qwen surface, or explicitly start a separate FP8 model-line project with its own baseline and target.
