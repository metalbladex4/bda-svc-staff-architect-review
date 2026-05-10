# V049 FP8 Reference-Crop Verifier Upper-Bound Pointer

Package path:

`docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v049_fp8_reference_crop_verifier_upper_bound/`

Current state:

- v049 is an experiment-only reference-crop verifier upper-bound tranche.
- Old/product v020c remains the incumbent under prior non-FP8 evidence: `186 / 33 / 25 / 58`.
- FP8 vLLM remains a separate experiment-only model line, not a product replacement.
- Locked FP8 composite baseline remains pp045c: `181 / 38 / 11 / 49`.
- pp046a remains diagnostic only at `181 / 38 / 0 / 38`; it failed visual lock in v047.
- v049 used reference-centered crops from v048 and therefore does not produce a deployable score.
- Backend ran with `Qwen/Qwen3-VL-8B-Instruct-FP8` on `http://127.0.0.1:8000/v1`.
- FN crops available/missing: `37 / 1`; case `40` / `40.png` remained missing from the configured source-image root.
- Verifier runs: `37`.
- High-confidence recoverable: `0`.
- Low-confidence recoverable: `34`.
- Ambiguous: `0`.
- Not recoverable: `3`.
- Decision: `A`; many FNs are recognizable in reference-centered crops, so the next tranche should be a non-oracle tiling/crop pass.
- No prompt candidate was authored.
- No product/runtime/source-truth/eval-ground-truth mutation occurred.
- v024o remains partial/unscored and forbidden.
- Raw crop/contact-sheet images were intentionally excluded from this review snapshot.

Next action:

Run v050 as an experiment-only non-oracle tiling/crop pass. It must generate crops without reference boxes and keep reference-centered v049 results as diagnostic upper-bound evidence only.
