# Stratified Split For Qwen v015 Human-Report Strategy

Status: `analysis_only`

The split is designed to support prompt-lever selection on dev while
holding back enough coverage to detect overfit before any all-112 rerun.

## Policy

- Dev: 56 cases.
- Holdout: 56 cases.
- Case `101` is pinned to dev as the major precision/recall hinge case.
- Case `155` is a dev protected out-of-scope negative control.
- Case `166` is a holdout protected out-of-scope negative control.

## Validation

- `no_overlap`: `True`
- `all_cases_covered`: `True`
- `case_101_in_dev`: `True`
- `protected_out_of_scope_controls`: `{'155': 'dev', '166': 'holdout'}`
- `slice_coverage`: `{'human_building_damage_slice_v1': {'total': 21, 'dev': 10, 'holdout': 11, 'covered_in_both': True}, 'human_confidence_distance_slice_v1': {'total': 24, 'dev': 12, 'holdout': 12, 'covered_in_both': True}, 'human_dense_multi_target_slice_v1': {'total': 18, 'dev': 9, 'holdout': 9, 'covered_in_both': True}, 'human_military_equipment_damage_slice_v1': {'total': 23, 'dev': 11, 'holdout': 12, 'covered_in_both': True}, 'human_out_of_scope_negative_slice_v1': {'total': 2, 'dev': 1, 'holdout': 1, 'covered_in_both': True}}`

## Slice Coverage

- `human_building_damage_slice_v1`: total `21`, dev `10`, holdout `11`, covered in both `True`
- `human_confidence_distance_slice_v1`: total `24`, dev `12`, holdout `12`, covered in both `True`
- `human_dense_multi_target_slice_v1`: total `18`, dev `9`, holdout `9`, covered in both `True`
- `human_military_equipment_damage_slice_v1`: total `23`, dev `11`, holdout `12`, covered in both `True`
- `human_out_of_scope_negative_slice_v1`: total `2`, dev `1`, holdout `1`, covered in both `True`

## Dev Cases

3, 6, 9, 12, 13, 14, 16, 19, 20, 21, 24, 28, 41, 42, 46, 48, 49, 50, 56, 57, 61, 63, 66, 67, 69, 73, 74, 76, 77, 78, 79, 80, 81, 82, 84, 86, 87, 89, 97, 100, 101, 103, 108, 109, 143, 144, 146, 147, 148, 149, 150, 151, 155, 163, 164, 170

## Holdout Cases

7, 8, 10, 11, 15, 17, 18, 22, 25, 26, 27, 29, 44, 51, 53, 59, 62, 64, 68, 70, 75, 83, 85, 88, 90, 91, 92, 93, 94, 95, 96, 98, 99, 102, 104, 105, 107, 110, 141, 142, 145, 152, 153, 154, 156, 157, 158, 159, 160, 161, 162, 165, 166, 167, 168, 169
