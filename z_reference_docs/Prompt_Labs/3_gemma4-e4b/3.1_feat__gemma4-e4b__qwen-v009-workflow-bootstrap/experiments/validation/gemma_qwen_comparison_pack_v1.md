# Gemma Qwen Comparison Pack V1

## Purpose

This pack exists to keep the first Gemma line directly comparable to the active
Qwen workflow.

It answers two questions:

- can Gemma hold the same contract on the inherited seed pack?
- if behavior drifts, is that drift better, worse, or just different from
  Qwen `v009`?

## Validation Images

- `tests/data/tank.jpg`
- `/home/williambenitez1/Capstone/z_reference_docs/Data_set_Storage/Unlabeled Photos/Tanks/Destroyed/destroyed_tank15.jpg`
- `/home/williambenitez1/Capstone/z_reference_docs/Data_set_Storage/Unlabeled Photos/Tanks/Operational/operational_tank4.jpg`
- `/home/williambenitez1/Capstone/z_reference_docs/Data_set_Storage/Unlabeled Photos/Buildings/Destroyed/destroyed_building4.jpg`
- `/home/williambenitez1/Capstone/z_reference_docs/Data_set_Storage/Unlabeled Photos/Buildings/Operational/operational_building7.jpg`
- `/home/williambenitez1/Capstone/z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/assets/spatial_understanding/office.jpg`

## First Comparison Rule

For the first Gemma baseline run:

1. run Gemma `v000`
2. compare Gemma `v000` against the clean `origin/main` baseline where useful
3. compare Gemma `v000` against Qwen `v009`
4. document drift in:
   - bbox behavior
   - JSON/output discipline
   - damage category
   - confidence behavior
   - summary wording
