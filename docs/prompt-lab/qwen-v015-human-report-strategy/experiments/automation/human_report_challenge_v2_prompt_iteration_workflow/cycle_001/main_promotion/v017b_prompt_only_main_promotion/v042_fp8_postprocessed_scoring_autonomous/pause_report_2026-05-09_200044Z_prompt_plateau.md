# v042 Pause Report: Prompt Plateau

Generated: `2026-05-09T20:00:44Z`

Pause reason: live prompt mutation reached a safe plateau after five micro-pack rejected candidates. This is a safe checkpoint, not a product promotion and not a replacement claim.

Backend status: vLLM FP8 backend was restarted and validated at `http://localhost:8000/v1` with model `Qwen/Qwen3-VL-8B-Instruct-FP8`.

Review publication: the initial backend-unavailable v042 checkpoint was published to the private review mirror from the review checkout only.

Working best remains:

- Raw FP8 prompt: `v034a_fp8_broad_context_scene_box_guard = 181 / 38 / 25 / 63`.
- Composite experiment-only score: `v034a + p1753 = 181 / 38 / 24 / 62`.

p1753 reproduction:

- Reproduced on frozen v034a.
- Removed one case-88 false positive.
- Removed zero true positives.

Live v042 candidate outcomes:

- `v042a_fp8_case84_low_contrast_recall_probe`: rejected at micro-pack, `43 / 16 / 15 / 31` postprocessed; case 84 worsened to `7/6/0`, case 66 worsened to `8/0/6`.
- `v042b_fp8_mostly_context_box_guard`: rejected at micro-pack, `43 / 16 / 18 / 34` postprocessed; case 66 worsened to `7/1/6`.
- `v042c_fp8_uncertain_fragments_phrase_ablation`: rejected at micro-pack, `40 / 19 / 22 / 41` postprocessed; case 66 exploded to `8/0/10`, case 67 fell to `8/3/3`, case 84 worsened to `7/6/0`.
- `v042d_fp8_final_balance_simplification`: rejected at micro-pack, `44 / 15 / 15 / 30` postprocessed; case 67 improved to `10/1/1` but case 84 worsened to `7/6/1`.
- `v042e_fp8_separate_small_target_row_exception`: rejected at micro-pack, `42 / 17 / 21 / 38` postprocessed; case 66, case 67, and case 110 regressed.

Recommendation:

- Pause near-neighbor prompt wording from v034a.
- Continue postprocessed scoring only if the next tranche focuses on verifier/postprocessing design or visual review of exact remaining deltas.
- Do not promote FP8 and do not treat it as a product replacement.

Exact resume suggestion:

```bash
cd /home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement
uv run python docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v042_fp8_postprocessed_scoring_autonomous/scripts/run_v042_continuation.py --candidate <next_candidate>
```

Hard boundaries preserved: no product source truth, runtime code, doctrine, assessment prompt, eval ground truth, Graphify/Mem0, v024o scored evidence, raw images, or secrets were modified or copied.
