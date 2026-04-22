# v009 Run 01

- version: `v009`
- parent: `frozen_stack(v006_detect, v008_assess, v004_summary)`
- branch: `feat/qwen3-vl-8b-instruct/two-pass-refinement`
- model line: `qwen3-vl:8b-instruct`
- base commit: `28e863b`
- run type: `focused_comparison`
- evaluation pack:
  - `tests/data/tank.jpg`
  - `operational_tank4.jpg`
  - `destroyed_building4.jpg`

## Run Method

1. Started from the clean branch-aware baseline snapshot.
2. Built `v009_effective_config.yaml` from:
   - `detect_objects` from `v006`
   - `assess_damage` from `v008`
   - `summarize_scene` from `v004`
3. Ran three representative comparison cases chosen to reflect the three
   inherited surfaces:
   - `tank_pressure`
   - `operational_tank4`
   - `destroyed_building4`
4. For each case:
   - copied the matching `v008 run02` JSON into `reference/`
   - ran `bda-svc` into `v009_candidate/`
   - ran `bda_eval` to generate overlays, crops, and
     `bbox_review_sheet.jpg`
5. Compared each `v009_candidate` JSON against the matching reference JSON
   after removing only routine metadata:
   - `image_id`
   - `date_created`
   - `inference_time`
6. Restored the live feature-branch config to the clean branch-aware baseline
   snapshot and verified it matched exactly.

## Headline Result

`v009` behaved exactly like the already validated frozen winner stack on all
three focused comparison cases.

Per-case normalized JSON comparison result:

- `tank_pressure` -> `MATCH`
- `operational_tank4` -> `MATCH`
- `destroyed_building4` -> `MATCH`

This confirms that the unified version file is not introducing new behavior. It
faithfully packages the already validated surfaces into one explicit promotion
candidate.

## Source-Version Comparison

- versus `v006`:
  - `v009` preserves the same key detection geometry on the representative
    detect-driven cases:
    - `tank_pressure` bbox `[51, 37, 128, 73]`
    - `destroyed_building4` bboxes `[0, 18, 69, 141]` and
      `[69, 18, 250, 158]`
- versus `v008`:
  - `v009` matches the full normalized output exactly on all three cases in
    this focused run, including:
    - `operational_tank4` -> `NO DAMAGE` / `CONFIRMED`
    - `destroyed_building4` -> two `DESTROYED` / `PROBABLE` building targets
    - `tank_pressure` -> `DESTROYED` / `PROBABLE`
- versus `v004`:
  - `v009` preserves the same conservative summary wording on the seed tank
    case:
    - `The scene shows a burning target in open terrain with dense black smoke.`
    - `The likely functional impact is severe degradation or loss of capability for the assessed target.`

## Tooling Note

- `bda_eval` completed successfully on all three focused comparison cases.
- As expected for this feature branch, LLMaaJ logic scoring was skipped because
  `OLLAMA_API_KEY` is not set.

## Decision

- `v009` is now both:
  - the staged current best stack
  - and a directly executed unified-stack run
- `v009` is ready to use as the single explicit reference version when we want
  to compare the packaged winner against future candidates or promote it into
  tracked config work
