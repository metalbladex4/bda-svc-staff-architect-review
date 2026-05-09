# v037 Final Recommendation

Generated: `2026-05-09T16:23:57Z`

Status: `stopped_no_new_fp8_working_best`.

Best FP8 candidate remains `v034a_fp8_broad_context_scene_box_guard = 181 / 38 / 25 / 63`.

No v037 candidate beat v034a's 63 combined errors. No v037 candidate reached or beat the old 58-error reference, and the <=1 target was not reached.

Candidate outcomes:
- `v037a_fp8_same_wreck_duplicate_local_guard`: rejected at micro-pack, `41 / 15 / 30 / 45`; case 155 improved to `2/0/0`, but case 110 exploded to `2/5/16` and case 66 worsened to `8/0/6`.
- `v037b_fp8_same_wreck_inside_box_guard`: runtime invalid; case 110 exceeded the 4096-token context cap at 4097 input tokens on all three attempts.
- `v037c_fp8_same_wreck_inner_duplicate_guard`: rejected at micro-pack, `43 / 13 / 17 / 30`; case 110 stayed controlled, but case 155 stayed `2/0/1` and case 66 worsened to `8/0/6`.
- `v037d_fp8_low_contrast_body_recall_cue`: rejected at micro-pack, `42 / 14 / 18 / 32`; case 155 improved to `2/0/0`, but case 84 did not improve and dense precision regressed (`66 = 8/0/7`, `67 = 8/3/6`).

Recommendation: keep FP8 as a separate model line, but pause further prompt clauses from this family. The next safe move is a non-prompt visual/eval simulation of same-wreck duplicate suppression, then only return to prompt wording if that simulation proves the case-155 duplicate class can be separated from dense valid rows.

Hard boundaries were preserved: no promotion, no product config/doctrine/assessment/runtime/eval-ground-truth mutation, no v024o scored evidence, no FP8 product-replacement claim, and no secrets copied.
