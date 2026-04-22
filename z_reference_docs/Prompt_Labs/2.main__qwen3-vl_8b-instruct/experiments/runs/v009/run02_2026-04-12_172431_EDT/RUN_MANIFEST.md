# Generalization Run Manifest

## Run Metadata

- Run timestamp folder: `run02_2026-04-12_172431_EDT`
- Lab: `2.main__qwen3-vl_8b-instruct`
- Frozen prompt pair under evaluation:
  - detection: `v006`
  - assessment: `v009`
- Purpose: check whether the current best prompt pair generalizes beyond the
  `tank.jpg` seed case and does not overfit to that one scene.

## Cases

### `tank`

- Scene image: `tests/data/tank.jpg`
- Current-main baseline result:
  - `DESTROYED`
  - `PROBABLE`
  - bbox `[51, 37, 128, 73]`
- Frozen pair result:
  - `DAMAGED`
  - `PROBABLE`
  - bbox `[46, 46, 128, 92]`
- Note:
  - the tank seed is still unstable across runs
  - the frozen pair did not simply memorize the tank scene, but it also did not
    preserve the earlier `DESTROYED` category on this repeat pass

### `destroyed_truck15`

- Scene image:
  `z_reference_docs/Data_set_Storage/Unlabeled Photos/Trucks/Destroyed/destroyed_truck15.jpg`
- Current-main baseline result:
  - `DAMAGED`
  - `PROBABLE`
  - bbox `[97, 120, 1173, 600]`
- Frozen pair result:
  - `DAMAGED`
  - `PROBABLE`
  - bbox `[124, 103, 1177, 583]`
- Note:
  - the frozen pair stayed consistent with the baseline category and confidence
  - the bbox shifted but remained broadly aligned with the damaged truck scene

### `operational_truck4`

- Scene image:
  `z_reference_docs/Data_set_Storage/Unlabeled Photos/Trucks/Operational/operational_truck4.jpg`
- Current-main baseline result:
  - `NO DAMAGE`
  - `CONFIRMED`
  - bbox `[21, 129, 769, 488]`
- Frozen pair result:
  - `NO DAMAGE`
  - `CONFIRMED`
  - bbox `[21, 129, 759, 495]`
- Note:
  - the frozen pair preserved the no-damage conclusion cleanly
  - this is a good sign that the prompt is not blindly keying on tank-specific
    fire language

### `office`

- Scene image:
  `z_reference_docs/Prompting/Qwen/Qwen-3-VL_cookbooks/assets/spatial_understanding/office.jpg`
- Current-main baseline result:
  - `object_not_found`
  - `NOT APPLICABLE`
- Frozen pair result:
  - `object_not_found`
  - `NOT APPLICABLE`
- Note:
  - the prompt pair did not hallucinate a military target in a clearly
    non-military scene

## High-Level Read

- The frozen pair generalizes reasonably on the truck and negative-scene cases.
- The tank seed is still the least stable case and should not be treated as
  fully settled.
- This sweep suggests the prompt pair is not obviously overfit to `tank.jpg`,
  but repeatability on that seed still needs attention before we call the
  detection/assessment direction fully done.
