# Experiment Run Manifest

## Run Metadata

- Run timestamp folder: `run02_2026-04-12_164250_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Version under test: `v007`
- Input image: `tests/data/tank.jpg`
- Purpose: start cycle 02 by testing whether a more conservative
  burn/smoke-aware `assess_damage` prompt can keep the `v006` detection style
  while reducing confidence inflation and K-kill language.

## Conditions

### Condition 1: `v006_working_baseline`

- Prompt/config source: merged full config using live current `main` plus the
  `v006` `detect_objects` override
- Effective config artifact:
  `v006_working_baseline/effective_config.v006-working-baseline.yaml`
- Command:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run bda-svc \
  --input tests/data/tank.jpg \
  --output z_reference_docs/Prompt_Labs/2.main__qwen3-vl_8b-instruct/experiments/runs/v007/run02_2026-04-12_164250_EDT/v006_working_baseline \
  --debug-export-images
```

- JSON report:
  `v006_working_baseline/tank_2026-04-12_204350Z.json`
- Debug overlay:
  `v006_working_baseline/tank_2026-04-12_204350Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v006_working_baseline/tank_2026-04-12_204350Z_debug/target_0_crop.jpg`

Headline result:

- `target_0.target_type`: `military_equipment`
- `damage_category`: `DESTROYED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[51, 37, 128, 73]`
- `metadata.inference_time`: `6.42`

### Condition 2: `v007_candidate`

- Prompt/config source: `v007_assess_damage_conservative-burn-calibration.yaml`
- Effective config artifact:
  `v007_candidate/effective_config.v007.yaml`
- Command note:
  The version file is a prompt-surface wrapper, so the candidate run used a
  merged full config generated from the live baseline plus the `v007`
  `detect_objects` and `assess_damage` overrides. That merged config was
  swapped into `src/bda_svc/pipeline/config.yaml` for the run and the live
  config was restored immediately afterward. Post-run verification showed no
  diff in the live config.
- JSON report:
  `v007_candidate/tank_2026-04-12_204408Z.json`
- Debug overlay:
  `v007_candidate/tank_2026-04-12_204408Z_debug/target_0_overlay.jpg`
- Debug crop:
  `v007_candidate/tank_2026-04-12_204408Z_debug/target_0_crop.jpg`

Headline result:

- `target_0.target_type`: `military_equipment`
- `damage_category`: `DAMAGED`
- `confidence_level`: `PROBABLE`
- `target_0.bounding_box`: `[46, 46, 128, 92]`
- `metadata.inference_time`: `5.74`

## Comparison Notes

- Relative to the `v006_working_baseline` condition, `v007`:
  - moved `xmin` left by `5` px
  - moved `ymin` down by `9` px
  - kept the same `xmax`
  - moved `ymax` down by `19` px
  - lowered the target-level category from `DESTROYED` to `DAMAGED`
  - kept confidence at `PROBABLE`
  - removed K-kill and unrepairable wording from supporting logic
- Manual review of `bbox_review_sheet.jpg` shows `v007` still lands on the same
  improved burning-target body region seen in the stronger `v006` outputs.
- The main regression is semantic, not formatting:
  - `v007` became too conservative on `damage_category`
  - the scene summary still overclaims likely complete loss for a `DAMAGED`
    target

## Reproducibility Note

- This run reproduced the same pattern seen in `run01`: the `v007` candidate
  kept the improved lower/wider bbox while the `v006_working_baseline`
  condition returned the older `[51, 37, 128, 73]` box.
- Because the saved `effective_config.v006-working-baseline.yaml` matches the
  original `v006` prompt content, this difference is being treated as
  model/output nondeterminism rather than a config-merge failure.

## Review Artifact

- Side-by-side overlay/crop review:
  `bbox_review_sheet.jpg`

## Initial Decision State

- `v007` is a partial downstream improvement, not a winner.
- Keep:
  - `PROBABLE` confidence
  - removal of K-kill and unrepairable language
- Do not keep as-is:
  - `DAMAGED` downgrade for this seed case
  - summary claim that still implies complete operational loss despite the
    downgraded category
