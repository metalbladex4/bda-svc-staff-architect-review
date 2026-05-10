# V048 FP8 FN Recovery Crop/Verifier Pointer

Package path:

`docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v048_fp8_fn_recovery_crop_verifier_loop/`

Current state:

- v048 is an experiment-only false-negative recovery crop/verifier planning tranche.
- Old/product v020c remains the incumbent under prior non-FP8 evidence: `186 / 33 / 25 / 58`.
- FP8 vLLM remains a separate experiment-only model line, not a product replacement.
- Locked FP8 composite baseline remains pp045c: `181 / 38 / 11 / 49`.
- pp046a remains diagnostic only at `181 / 38 / 0 / 38`; it failed visual lock in v047.
- All 38 pp045c residual FNs were inventoried.
- Local-only FN crop/contact-sheet aids were generated in the active worktree; raw JPG/PNG review images were intentionally excluded from this review snapshot.
- `37` of `38` FN crops were generated; case `40` / `40.png` was missing from the configured source-image root.
- Dominant residual FN classes: building/structure pieces, adjacent-target confusions, dense valid targets, smoke/debris-obscured targets, one edge/boundary target, and one small valid target.
- No live VLM call occurred in v048.
- No prompt candidate was authored.
- No product/runtime/source-truth/eval-ground-truth mutation occurred.
- v024o remains partial/unscored and forbidden.

Next action:

Run a gated experiment-only crop/tiling verifier tranche from pp045c before considering any narrow prompt-recall candidate.
