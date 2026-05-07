# v026 Runtime Shape Probe Evidence

## Purpose

This note publishes the available evidence for the v026 stop decision so GPT-5.5 Pro can independently audit whether prompt mutation should pause before another Qwen tranche.

The central question is whether `v026q_blank_line_shape_probe` was a semantic prompt failure or evidence that the evaluation surface had become sensitive to prompt/rendering/runtime shape.

## Source State

- Product/current incumbent: `v020c_anchor_replay` / `v020c_extra_box_audit`.
- Incumbent all-current metrics: `186` matches / `33` false negatives / `25` false positives / `58` combined errors.
- `v024l_v023s_no_wheel_track_ablation`: `188 / 31 / 35 / 66`, high-recall learning evidence only.
- `v025a_v020c_compact_separate_body_recovery`: `176 / 43 / 35 / 78`, rejected.
- `v024o`: partial/unscored and forbidden as scored evidence.
- v026 stop status: prompt mutation paused after semantic deltas and a no-semantics blank-line shape probe collapsed the sentinel, especially case `67`.

## Rendered Prompt Hashes

Exact final rendered prompt text hashes were **not recorded** for either `v020c` or `v026q`.

The scratch worktrees referenced by the run summaries were no longer present when this evidence package was prepared, and the v026 package did not retain raw request payloads or final rendered prompt text.

Closest available evidence:

- `v020c` detect prompt overlay-template SHA-256: `fb3d1d2705bd5a0b567c50257f1929fb056b3a685e8fe4d731dfaadfa0b29b95`
- `v026q_blank_line_shape_probe` detect prompt overlay-template SHA-256: `de9aa26fc3d99b2ff5443c1013e8f50b94ca982de9837060cc43c1123f4ef5d5`

These are hashes of the YAML `prompts.detect_objects` template before runtime placeholder substitution.

## Overlay-Template Diff

The closest retained prompt-level diff shows one added blank line after `{categories}`:

```diff
--- v020c_detect_objects_template
+++ v026q_detect_objects_template
@@ -3,6 +3,7 @@
 TASK
 Detect targets whose doctrinal target_type is one of:
 {categories}
+

 Calibration from prior runs: broad recall additions raised false positives. Return to the v019c context-shadow balance and improve only the final cleanup of extra boxes.
```

## Intended Semantic Difference

The only intended semantic difference between `v020c` and `v026q` was a blank line. The candidate authoring function for `v026q` describes it as:

```text
Exact v020c with only one extra blank line after the categories block.
```

## Final Rendered Prompt Difference

The available evidence does **not** prove that the final rendered prompt differed only by that blank line.

What is known:

- The retained overlay-template prompt differs only by one blank line.
- All required prompt placeholders are present in both templates.
- The same runner family and same upstream-code/OpenAI-compatible path were used.

What is not known:

- The exact final rendered prompt text after `{categories}`, `{detection_guidance}`, `{bbox_format}`, and `{bbox_scale}` substitution.
- The exact OpenAI-compatible chat payload sent to the backend.
- Whether the backend chat-template or Ollama OpenAI-compatible serialization introduced any hidden shape difference.

Recommended follow-up: future runtime-shape probes should write final rendered prompt text, prompt SHA-256, system/user message boundaries, and sanitized request-shape metadata before inference.

## System/User Message Boundary Comparison

Direct system/user message boundary artifacts were not retained. The run summaries show both runs used the same upstream-code manifest runner path and the same command family:

```text
uv run bda-svc -i <image> -o <predicted-output-dir>
```

Both runs were launched from isolated scratch worktrees and used the same v026 sentinel manifest. Because the raw request payloads were not retained, message-boundary equality is an inference from the runner path, not a directly recorded fact.

## Placeholder Rendering Comparison

Template-level placeholder status:

| placeholder | v020c template | v026q template |
|---|---|---|
| `{categories}` | present | present |
| `{detection_guidance}` | present | present |
| `{bbox_format}` | present | present |
| `{bbox_scale}` | present | present |

Final substituted placeholder text was not retained. Do not overclaim that final rendered placeholder blocks were byte-identical.

## JSON And Schema Instruction Comparison

Template-level JSON/schema wording was preserved. Both templates retain the JSON-only instruction and the top-level output contract:

```text
Return valid JSON only. The top-level object must contain exactly one key, "detections".
```

No schema experiment was intended or recorded for `v026q`.

## Backend And Runtime Settings

Recorded backend preflight:

- Preferred endpoint: `http://localhost:8000/v1`
- Preferred model name: `Qwen/Qwen3-VL-8B-Instruct`
- Preferred endpoint status: unavailable, `Connection refused`
- Authorized fallback endpoint used: `http://localhost:11434/v1`
- Fallback model name: `qwen3-vl:8b-instruct`
- Backend label: `ollama_openai_compat_fallback_11434`
- API-key placeholder: `no-auth`

Settings not recorded in the v026 evidence package:

- temperature
- max image size
- max tokens
- stop sequences
- response schema enforcement details beyond the prompt text and upstream runtime path

Recommended follow-up: make these settings explicit in runner summaries before any future prompt-vs-runtime attribution.

## Image Payload Comparison

Both `v020c` fresh sentinel and `v026q` used the same sentinel micro-pack manifest:

```text
v026_sentinel_micro_pack_no101
```

Sentinel cases:

```text
12, 14, 16, 42, 66, 67, 77, 84, 88, 90, 97, 103, 155, 166, 172
```

The manifest excludes case `101`.

Local source image hashes from the sentinel manifest:

| case | image filename | source SHA-256 |
|---:|---|---|
| 12 | `12.jpg` | `e4cd0d4efb461c14df61ab37c8ca4175306bc4c08b70577e9c5c29110548bcd6` |
| 14 | `14.jpg` | `bb72653c7be57e2590cea4212b0aba535d85be4d93c75a7e95d710ea45a81e52` |
| 16 | `16.jpg` | `54a292b759e66097cf7a1853ec40b39a546f8dfb399f973d7c0d66fbaf79ed1b` |
| 42 | `42.png` | `11cf5c5eafde8e97570d6512a85c5c3e13e8f8ea1c43158c47ca7c4f16752413` |
| 66 | `66.jpg` | `176a19d405cf592c9b0781bbccabab70c6bbc21182a4064353f9f080edc6cb49` |
| 67 | `67.jpg` | `efee332a8e66c25f3a3d10713e77e77b89386e6d1834edcd213f3bf002410ec0` |
| 77 | `77.jpg` | `28888db6da94d8e6e6f363fd5bba4fc5b679a04c97112565d32f00794d036c0f` |
| 84 | `84.jpg` | `2747d46bef2f4eafad53285f2a82f1adc21b85382dcf78b3615e91c4f5de0280` |
| 88 | `88.jpg` | `db8a9ad1c33ad4921507f8a4adfe9bcab8fb3cba3611af0fb5cb40bc5d94fbfe` |
| 90 | `90.png` | `e4cd0d4efb461c14df61ab37c8ca4175306bc4c08b70577e9c5c29110548bcd6` |
| 97 | `97.jpg` | `7b0544c22e1212dc72ec34def93bea18cadc83997fb8f317b8be6d76c672d04d` |
| 103 | `103.jpg` | `d38891608467f9ea9be482f2f6230c0005eac594bd9b078cf9fd130a5b338e5c` |
| 155 | `155.jpg` | `c5439edfbab0d823c7e2af813d9b816978c92b5d229c9a88c4fa83c5a20f8056` |
| 166 | `166.jpg` | `ac3a8b179c8221f7e12fb429adadb88cc89eeea275668312a957b63d67a0e911` |
| 172 | `172.jpg` | `20529fb85671b3c3aa0267672728b515b8685f9be3ab1bca61570bc14c249510` |

Raw image files were not copied into this review package.

## Case 67 Comparison

`v020c_anchor_replay` fresh sentinel result:

- case `67`: `9` matches / `2` FNs / `4` FPs
- reference targets: `11`
- predicted targets: `13`

`v026q_blank_line_shape_probe` sentinel result:

- case `67`: `1` match / `10` FNs / `9` FPs
- reference targets: `11`
- predicted targets: `10`

Delta from `v020c` to `v026q`:

- `-8` matches
- `+8` FNs
- `+5` FPs

Short interpretation: case `67` did not merely add a few extra boxes. It lost most of the previously matched dense-row targets while adding more false positives, matching the same major dense-case collapse pattern seen in several semantic prompt deltas.

## No-Op Or Effective-Replay Candidates

These candidates reproduced the v020c full all-current metrics and are documented as having no effective prompt delta or exact-replay behavior:

| candidate | stage | metrics | case 67 | note |
|---|---|---|---|---|
| `v026a_fragment_context_precision_guard` | full all-current | `186 / 33 / 25 / 58` | `9/2/4` | no effective prompt delta rendered |
| `v026c_vehicle_body_anchor_not_rowline` | full all-current | `186 / 33 / 25 / 58` | `9/2/4` | no effective prompt delta rendered |
| `v026f_tight_box_occupancy_guard` | full all-current | `186 / 33 / 25 / 58` | `9/2/4` | no effective prompt delta rendered |

## Sentinel-Failing Prompt Deltas

Semantic prompt deltas that failed sentinel:

| candidate | sentinel metrics | case 67 | hard disqualifiers |
|---|---|---|---|
| `v026b_audit_removal_only_lock` | `28 / 21 / 17 / 38` | `1/10/11` | `case_67_regression`, `case_84_regression` |
| `v026d_qwen_native_grounding_header` | `32 / 17 / 20 / 37` | `1/10/11` | `case_67_regression` |
| `v026e_low_salience_separate_body_good_box` | `31 / 18 / 18 / 36` | `1/10/11` | `case_67_regression` |
| `v026g_actual_tight_occupancy_guard` | `30 / 19 / 17 / 36` | `2/9/9` | `case_67_regression`, `case_97_match_loss` |
| `v026h_remove_calibration_preamble` | `36 / 13 / 12 / 25` | `7/4/5` | `case_67_regression` |
| `v026i_remove_v019c_label_only` | `29 / 20 / 18 / 38` | `2/9/10` | `case_67_regression`, `case_84_regression` |
| `v026j_visible_body_occupancy_phrase` | `32 / 17 / 20 / 37` | `2/9/10` | `case_155_failed`, `case_67_regression` |
| `v026k_unrelated_background_object_guard` | `33 / 16 / 25 / 41` | `2/9/11` | `case_155_failed`, `case_67_regression`, `nested_fragment_or_context_fp_reopened` |
| `v026l_compact_context_shadow_schema` | `33 / 16 / 24 / 40` | `2/9/10` | `case_67_regression` |
| `v026m_target_guidance_before_context` | `29 / 20 / 23 / 43` | `1/10/11` | `case_155_failed`, `case_67_regression`, `case_84_regression` |
| `v026n_dense_row_body_safety_cue` | `31 / 18 / 20 / 38` | `1/10/11` | `case_67_regression` |
| `v026o_output_only_no_extra_keys` | `28 / 21 / 19 / 40` | `1/10/10` | `case_67_regression`, `case_84_regression` |
| `v026p_quadrant_scan_search_cue` | `29 / 20 / 18 / 38` | `1/10/9` | `case_67_regression` |

No-semantics shape probe:

| candidate | sentinel metrics | case 67 | hard disqualifiers |
|---|---|---|---|
| `v026q_blank_line_shape_probe` | `29 / 20 / 16 / 36` | `1/10/9` | `case_67_regression`, `case_84_regression` |

## Codex Conclusion

Candidate failure means the candidate idea failed.

Shape-probe failure means the evaluation surface itself is suspect. Because the retained `v026q` overlay-template diff was blank-line-only, the safe conclusion is not "a blank line semantically caused the model to fail." The safer conclusion is that prompt mutation on the fallback OpenAI-compatible Ollama path was not stable enough to support confident semantic attribution.

The v026 decision was therefore:

- freeze `v020c` as the incumbent;
- do not treat `v024l` as a base;
- do not use `v024o`;
- pause new prompt mutation;
- run backend/rendering stability checks before another autonomous prompt tranche.

## Uncertainty And Anti-Overclaim Boundaries

GPT-5.5 Pro should not overclaim the v026q result because these artifacts are missing:

- final rendered `v020c` prompt text and hash;
- final rendered `v026q` prompt text and hash;
- sanitized raw OpenAI-compatible request payloads;
- direct system/user message boundary captures;
- exact chat-template serialization behavior;
- exact Ollama OpenAI-compatible payload normalization behavior;
- temperature, max-token, stop, and max-image-size settings in per-run evidence;
- final substituted placeholder blocks.

The available evidence is strong enough to justify a pause-and-audit recommendation, but not strong enough to prove that the final backend request differed only by one byte-level blank line.

## Recommended Follow-Up Checks

Before any next prompt candidate:

1. Run exact `v020c` replay on the preferred `http://localhost:8000/v1` backend if available.
2. Capture final rendered prompt text and SHA-256 for every run.
3. Capture sanitized request-shape metadata: message count, role sequence, image path/hash, model name, temperature, max tokens, stop/schema settings, and payload byte hash when safe.
4. Run a no-semantics shape probe with final rendered hashes proving the intended diff.
5. Only resume semantic prompt mutation after exact replay and no-semantics shape probe preserve case `67`, `155`, `166`, and office-negative.
