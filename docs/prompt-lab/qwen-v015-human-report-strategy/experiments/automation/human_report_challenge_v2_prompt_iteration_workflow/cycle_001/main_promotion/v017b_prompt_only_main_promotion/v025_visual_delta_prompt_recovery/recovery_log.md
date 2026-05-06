# Recovery Log

No runtime recovery was required because this wave did not run model inference.

## Artifact Caveat

During source-artifact inventory, both `v020c` and `v024l` had complete
`images_bbox_review` images for all 117 all-current cases, but the derived
`images_bbox_both` and crop folders each contained 111 images.

Known priority cases with complete review images but missing some crop/both
derivatives:

- `42`
- `90`

Decision:

- use `images_bbox_review` as the complete first-pass review surface
- use raw predictions, eval CSV rows, and summary JSON for match details
- use crop/bbox-both images opportunistically where present
- do not regenerate eval artifacts in this package

## Stop Conditions Preserved

- `v024o` remains unscored
- no prompt candidate was authored
- no source truth was mutated
