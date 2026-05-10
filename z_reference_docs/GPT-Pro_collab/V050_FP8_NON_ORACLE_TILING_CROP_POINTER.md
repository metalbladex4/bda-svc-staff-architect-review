# V050 FP8 Non-Oracle Tiling/Crop Pointer

Package path:

`docs/prompt-lab/qwen-v015-human-report-strategy/experiments/automation/human_report_challenge_v2_prompt_iteration_workflow/cycle_001/main_promotion/v017b_prompt_only_main_promotion/v050_fp8_non_oracle_tiling_crop_recovery/`

Current status:

- Backend ran against `Qwen/Qwen3-VL-8B-Instruct-FP8` at `http://127.0.0.1:8000/v1`.
- Case `40 / 40.png` was resolved from alternate configured source-image roots.
- Strategies tested: A full-image 2x2 overlap, B generic dense-row strips, C prediction-anchored neighbor crops, and D smoke/debris broad-context crop.
- Locked FP8 composite baseline remains pp045c: `181 / 38 / 11 / 49`.
- Diagnostic pp046a remains diagnostic-only and is not locked: `181 / 38 / 0 / 38`.
- Old/product v020c remains incumbent under prior non-FP8 evidence: `186 / 33 / 25 / 58`.
- v024o remains partial/unscored and was not used.

Result:

- Micro-pack baseline: `51 / 25 / 5 / 30`.
- Micro-pack raw merged: `58 / 18 / 48 / 66`.
- Micro-pack postprocessed merged: `58 / 18 / 48 / 66`.
- Added detections: `50`.
- Added true positives: `8`.
- Added false positives: `42`.
- Full all-current/no101 was not run because the micro-pack failed the FP gate.
- Decision: `B` - non-oracle tiling recovered FNs but created too many FPs; it needs a crop-level verifier gate before any broader merge.

Boundary:

- No product/runtime/source-truth/doctrine/assessment/eval-ground-truth files were intentionally changed by v050.
- Reference boxes were not used to generate inference crops.
- Reference-centered crop results from v049 were not counted as deployable score.
- Raw tile/crop images were excluded from this review snapshot.

Next action:

Run v051 as an experiment-only crop-level verifier gate for non-oracle tile candidates before merging them into pp045c outputs.
