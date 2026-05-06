# Offline Example Bank For Qwen v015 Human-Report Strategy

Status: `offline_evidence_only`

These examples are selected to support analysis and candidate design. They
are not approved for direct insertion into runtime prompts in this wave.

## Policy

- Use as offline review evidence for taxonomy and hypothesis design.
- Do not paste raw report text into prompts by default.
- Marked/cropped visual exemplar pilots require separate approval.

## Selected Examples

### Case `11`

- Split: `holdout`
- Roles: `v014_recall_loss`
- Image: `11.jpg`
- Slices: `human_building_damage_slice_v1`
- Delta label: `v014_recall_loss`
- v009: matches `2`, FN `0`, FP `0`
- v014: matches `1`, FN `1`, FP `0`
- Object summaries:
  - building / no damage / confirmed / [0,200,720,801]
  - military equipment / no damage / confirmed / [178,741,351,839]

### Case `13`

- Split: `dev`
- Roles: `v014_recall_loss`
- Image: `13.jpg`
- Slices: `none`
- Delta label: `v014_recall_loss`
- v009: matches `2`, FN `0`, FP `0`
- v014: matches `1`, FN `1`, FP `0`
- Object summaries:
  - building / no damage / confirmed / [38,90,563,357]
  - building / no damage / confirmed / [631,49,786,354]

### Case `19`

- Split: `dev`
- Roles: `persistent_false_positive_gap`
- Image: `19.jpg`
- Slices: `none`
- Delta label: `persistent_false_positive_gap`
- v009: matches `1`, FN `0`, FP `0`
- v014: matches `1`, FN `0`, FP `1`
- Object summaries:
  - military equipment / destroyed / confirmed / [315,149,690,577]

### Case `21`

- Split: `dev`
- Roles: `persistent_recall_gap`
- Image: `21.jpg`
- Slices: `human_building_damage_slice_v1, human_confidence_distance_slice_v1, human_dense_multi_target_slice_v1`
- Delta label: `persistent_recall_gap`
- v009: matches `2`, FN `1`, FP `0`
- v014: matches `2`, FN `1`, FP `0`
- Object summaries:
  - building / severe damage / confirmed / [146,27,432,328]
  - building / moderate damage / confirmed / [429,98,620,322]
  - building / no damage / possible / [3,213,96,312]

### Case `22`

- Split: `holdout`
- Roles: `stable_or_clean`
- Image: `22.jpg`
- Slices: `human_dense_multi_target_slice_v1, human_military_equipment_damage_slice_v1`
- Delta label: `stable_or_clean`
- v009: matches `6`, FN `0`, FP `0`
- v014: matches `6`, FN `0`, FP `0`
- Object summaries:
  - military equipment / destroyed / confirmed / [2,362,163,625]
  - military equipment / destroyed / confirmed / [360,403,643,557]
  - military equipment / destroyed / confirmed / [676,411,901,522]
  - military equipment / destroyed / confirmed / [1072,528,1369,667]
  - military equipment / destroyed / confirmed / [1036,269,1286,399]
  - military equipment / destroyed / confirmed / [726,97,997,233]

### Case `28`

- Split: `dev`
- Roles: `v014_fp_suppression`
- Image: `28.jpg`
- Slices: `none`
- Delta label: `v014_fp_suppression`
- v009: matches `1`, FN `0`, FP `2`
- v014: matches `1`, FN `0`, FP `0`
- Object summaries:
  - military equipment / no damage / confirmed / [567,364,862,640]

### Case `44`

- Split: `holdout`
- Roles: `persistent_recall_gap`
- Image: `44.jpg`
- Slices: `human_confidence_distance_slice_v1, human_dense_multi_target_slice_v1, human_military_equipment_damage_slice_v1`
- Delta label: `persistent_recall_gap`
- v009: matches `7`, FN `2`, FP `0`
- v014: matches `7`, FN `2`, FP `0`
- Object summaries:
  - military equipment / destroyed / confirmed / [7,415,443,815]
  - military equipment / destroyed / confirmed / [179,621,856,941]
  - military equipment / destroyed / confirmed / [529,709,1179,1110]
  - military equipment / damaged / confirmed / [591,1155,1170,1642]
  - military equipment / no damage / probable / [943,1227,1676,1839]
  - military equipment / damaged / probable / [1147,689,1837,1132]
  - military equipment / destroyed / probable / [1543,977,2281,1401]
  - military equipment / destroyed / confirmed / [2123,383,3014,872]
  - military equipment / destroyed / confirmed / [2431,911,3192,1453]

### Case `51`

- Split: `holdout`
- Roles: `persistent_false_positive_gap`
- Image: `51.jpg`
- Slices: `none`
- Delta label: `persistent_false_positive_gap`
- v009: matches `1`, FN `0`, FP `1`
- v014: matches `1`, FN `0`, FP `1`
- Object summaries:
  - military equipment / destroyed / confirmed / [45,120,1199,817]

### Case `66`

- Split: `dev`
- Roles: `v014_fp_suppression`
- Image: `66.jpg`
- Slices: `human_confidence_distance_slice_v1, human_dense_multi_target_slice_v1, human_military_equipment_damage_slice_v1`
- Delta label: `v014_fp_suppression`
- v009: matches `7`, FN `1`, FP `5`
- v014: matches `7`, FN `1`, FP `4`
- Object summaries:
  - military equipment / damaged / confirmed / [459,33,971,482]
  - military equipment / damaged / confirmed / [312,128,465,386]
  - military equipment / damaged / probable / [239,174,346,363]
  - military equipment / no damage / possible / [209,240,242,332]
  - military equipment / no damage / possible / [183,249,209,323]
  - military equipment / no damage / possible / [160,256,181,316]
  - military equipment / no damage / possible / [133,260,161,309]
  - military equipment / no damage / possible / [111,263,132,300]

### Case `67`

- Split: `dev`
- Roles: `v014_fp_suppression`
- Image: `67.jpg`
- Slices: `human_confidence_distance_slice_v1, human_dense_multi_target_slice_v1`
- Delta label: `v014_fp_suppression`
- v009: matches `1`, FN `10`, FP `12`
- v014: matches `1`, FN `10`, FP `8`
- Object summaries:
  - military equipment / no damage / possible / [90,172,109,185]
  - military equipment / no damage / possible / [131,173,146,190]
  - military equipment / no damage / possible / [150,179,162,192]
  - military equipment / no damage / possible / [167,180,181,197]
  - military equipment / no damage / possible / [185,184,201,200]
  - military equipment / no damage / possible / [204,186,226,202]
  - military equipment / no damage / possible / [230,188,255,210]
  - military equipment / no damage / probable / [256,192,286,217]
  - military equipment / no damage / probable / [315,198,351,224]
  - military equipment / no damage / confirmed / [424,212,490,251]
  - military equipment / no damage / confirmed / [630,235,780,330]

### Case `68`

- Split: `holdout`
- Roles: `stable_or_clean`
- Image: `68.jpg`
- Slices: `none`
- Delta label: `stable_or_clean`
- v009: matches `2`, FN `0`, FP `0`
- v014: matches `2`, FN `0`, FP `0`
- Object summaries:
  - military equipment / no damage / confirmed / [290,103,1075,599]
  - military equipment / no damage / confirmed / [39,167,522,545]

### Case `69`

- Split: `dev`
- Roles: `persistent_false_positive_gap`
- Image: `69.jpg`
- Slices: `none`
- Delta label: `persistent_false_positive_gap`
- v009: matches `1`, FN `0`, FP `1`
- v014: matches `1`, FN `0`, FP `1`
- Object summaries:
  - military equipment / no damage / confirmed / [2,136,467,578]

### Case `70`

- Split: `holdout`
- Roles: `stable_or_clean`
- Image: `70.jpg`
- Slices: `human_building_damage_slice_v1`
- Delta label: `stable_or_clean`
- v009: matches `2`, FN `0`, FP `0`
- v014: matches `2`, FN `0`, FP `0`
- Object summaries:
  - military equipment / no damage / confirmed / [148,198,363,295]
  - building / destroyed / confirmed / [135,1,588,278]

### Case `84`

- Split: `dev`
- Roles: `v014_fp_suppression`
- Image: `84.jpg`
- Slices: `human_dense_multi_target_slice_v1, human_military_equipment_damage_slice_v1`
- Delta label: `v014_fp_suppression`
- v009: matches `5`, FN `8`, FP `2`
- v014: matches `5`, FN `8`, FP `1`
- Object summaries:
  - military equipment / no damage / confirmed / [278,144,724,434]
  - military equipment / no damage / confirmed / [174,156,374,339]
  - military equipment / no damage / confirmed / [128,178,235,291]
  - military equipment / no damage / confirmed / [110,164,164,266]
  - military equipment / no damage / confirmed / [93,176,116,264]
  - military equipment / no damage / confirmed / [81,181,94,250]
  - military equipment / no damage / confirmed / [72,184,82,244]
  - military equipment / no damage / confirmed / [58,204,68,240]
  - military equipment / no damage / confirmed / [53,208,64,238]
  - military equipment / no damage / confirmed / [691,127,765,332]
  - military equipment / no damage / confirmed / [0,190,12,236]
  - military equipment / no damage / confirmed / [21,186,58,233]
  - military equipment / no damage / confirmed / [66,186,100,214]

### Case `93`

- Split: `holdout`
- Roles: `stable_or_clean`
- Image: `93.jpg`
- Slices: `human_dense_multi_target_slice_v1`
- Delta label: `stable_or_clean`
- v009: matches `3`, FN `0`, FP `0`
- v014: matches `3`, FN `0`, FP `0`
- Object summaries:
  - military equipment / no damage / confirmed / [36,277,244,427]
  - military equipment / no damage / confirmed / [275,185,1068,602]
  - building / no damage / confirmed / [328,0,1200,525]

### Case `100`

- Split: `dev`
- Roles: `v014_recall_loss`
- Image: `100.jpg`
- Slices: `human_building_damage_slice_v1, human_confidence_distance_slice_v1, human_dense_multi_target_slice_v1`
- Delta label: `v014_recall_loss`
- v009: matches `2`, FN `1`, FP `0`
- v014: matches `1`, FN `2`, FP `0`
- Object summaries:
  - building / light damage / possible / [0,37,149,574]
  - building / destroyed / confirmed / [178,3,834,554]
  - building / moderate damage / probable / [844,4,1078,541]

### Case `101`

- Split: `dev`
- Roles: `precision_recall_tradeoff, required_guardrail_case`
- Image: `101.jpg`
- Slices: `human_confidence_distance_slice_v1, human_dense_multi_target_slice_v1, human_military_equipment_damage_slice_v1`
- Delta label: `precision_recall_tradeoff`
- v009: matches `6`, FN `6`, FP `14`
- v014: matches `1`, FN `11`, FP `0`
- Object summaries:
  - military equipment / damaged / possible / [87,151,996,534]
  - military equipment / no damage / possible / [59,133,112,180]
  - military equipment / no damage / possible / [119,135,206,187]
  - military equipment / no damage / possible / [213,140,256,185]
  - military equipment / no damage / possible / [232,149,297,195]
  - military equipment / no damage / possible / [469,132,525,198]
  - military equipment / no damage / possible / [531,131,568,170]
  - military equipment / no damage / possible / [531,131,568,170]
  - military equipment / no damage / possible / [717,152,791,193]
  - military equipment / no damage / possible / [869,142,918,189]
  - military equipment / no damage / possible / [926,139,972,180]
  - military equipment / no damage / possible / [999,125,1024,184]

### Case `110`

- Split: `holdout`
- Roles: `persistent_recall_gap`
- Image: `110.jpg`
- Slices: `human_dense_multi_target_slice_v1`
- Delta label: `persistent_recall_gap`
- v009: matches `1`, FN `6`, FP `2`
- v014: matches `1`, FN `6`, FP `2`
- Object summaries:
  - military equipment / no damage / confirmed / [159,80,259,196]
  - military equipment / no damage / confirmed / [132,83,178,142]
  - military equipment / no damage / confirmed / [131,56,159,91]
  - military equipment / no damage / confirmed / [151,42,168,65]
  - military equipment / no damage / confirmed / [150,25,169,43]
  - military equipment / no damage / confirmed / [99,12,110,29]
  - military equipment / no damage / confirmed / [17,8,28,20]

### Case `141`

- Split: `holdout`
- Roles: `persistent_false_positive_gap`
- Image: `141.jpg`
- Slices: `human_confidence_distance_slice_v1, human_military_equipment_damage_slice_v1`
- Delta label: `persistent_false_positive_gap`
- v009: matches `1`, FN `0`, FP `1`
- v014: matches `1`, FN `0`, FP `1`
- Object summaries:
  - military equipment / damaged / possible / [24,21,170,142]

### Case `147`

- Split: `dev`
- Roles: `v014_recall_loss`
- Image: `147.jpg`
- Slices: `human_building_damage_slice_v1, human_dense_multi_target_slice_v1`
- Delta label: `v014_recall_loss`
- v009: matches `3`, FN `0`, FP `0`
- v014: matches `1`, FN `2`, FP `0`
- Object summaries:
  - military equipment / no damage / confirmed / [21,124,478,322]
  - building / no damage / possible / [207,23,294,92]
  - building / no damage / possible / [337,20,423,89]

### Case `154`

- Split: `holdout`
- Roles: `qualitative_bbox_caveat`
- Image: `154.jpg`
- Slices: `human_building_damage_slice_v1, human_dense_multi_target_slice_v1`
- Delta label: `persistent_recall_gap`
- v009: matches `2`, FN `1`, FP `0`
- v014: matches `2`, FN `1`, FP `0`
- Object summaries:
  - military equipment / no damage / confirmed / [33,218,339,408]
  - building / severe damage / confirmed / [1,1,613,224]
  - building / destroyed / probable / [379,303,612,417]

### Case `155`

- Split: `dev`
- Roles: `protected_out_of_scope_negative, required_guardrail_case`
- Image: `155.jpg`
- Slices: `human_out_of_scope_negative_slice_v1`
- Delta label: `stable_or_clean`
- v009: matches `1`, FN `0`, FP `0`
- v014: matches `1`, FN `0`, FP `0`
- Object summaries:
  - object_not_found / not applicable / confirmed / [0,0,0,0]

### Case `159`

- Split: `holdout`
- Roles: `qualitative_bbox_caveat`
- Image: `159.jpg`
- Slices: `human_military_equipment_damage_slice_v1`
- Delta label: `stable_or_clean`
- v009: matches `2`, FN `0`, FP `0`
- v014: matches `2`, FN `0`, FP `0`
- Object summaries:
  - military equipment / damaged / possible / [33,220,251,273]
  - military equipment / damaged / probable / [7,105,613,358]

### Case `160`

- Split: `holdout`
- Roles: `persistent_recall_gap, qualitative_bbox_caveat`
- Image: `160.jpg`
- Slices: `human_building_damage_slice_v1, human_dense_multi_target_slice_v1`
- Delta label: `persistent_recall_gap`
- v009: matches `2`, FN `3`, FP `0`
- v014: matches `2`, FN `3`, FP `0`
- Object summaries:
  - building / severe damage / confirmed / [2,61,179,321]
  - building / severe damage / confirmed / [339,66,543,333]
  - building / severe damage / possible / [270,3,477,68]
  - building / severe damage / possible / [44,5,206,59]
  - building / no damage / possible / [516,1,590,84]

### Case `164`

- Split: `dev`
- Roles: `qualitative_bbox_caveat`
- Image: `164.jpg`
- Slices: `human_building_damage_slice_v1`
- Delta label: `persistent_recall_gap`
- v009: matches `1`, FN `1`, FP `0`
- v014: matches `1`, FN `1`, FP `0`
- Object summaries:
  - building / destroyed / confirmed / [105,86,565,321]
  - building / no damage / possible / [480,159,613,289]

### Case `166`

- Split: `holdout`
- Roles: `protected_out_of_scope_negative, required_guardrail_case`
- Image: `166.jpg`
- Slices: `human_out_of_scope_negative_slice_v1`
- Delta label: `persistent_recall_gap`
- v009: matches `0`, FN `1`, FP `1`
- v014: matches `0`, FN `1`, FP `1`
- Object summaries:
  - object_not_found / not applicable / confirmed / [0,0,0,0]
