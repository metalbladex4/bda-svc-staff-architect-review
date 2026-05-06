# Validation Plan

Status: `future_wave_plan`

## Recommended Next Wave

`offline_guard_simulator_only`

## Approval Gates

- run offline simulator on existing hinge predictions only
- compare raw vs guarded metrics without inference
- manually review case 101 before any dev recommendation
- do not insert into runtime until simulator proves value and user approves

## Primary Success Criteria

- row-fragment groups on v015b/v015c case 101 are flagged
- v015d broad group box on case 101 is flagged
- raw predictions remain available for audit

## Secondary Success Criteria

- guard does not alter protected 155 abstention
- guard preserves v015c-safe 12 and 28 outputs
- before/after metrics are explicit about recall loss

## Explicit Non-Runs

- no new VLM inference
- no dev split
- no holdout
- no all-112
- no runtime config adoption
- no source truth mutation
- no Graphify refresh
- no evidence rebuild
- no Mem0 update
