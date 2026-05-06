# v023 Research Notes

Continuation contract: do not stop for prompt-only plateau. Continue from the
current Qwen incumbent until the literal `<=1` total-error target is reached,
the user interrupts, or usage forces a handoff.

Local evidence at start:

- `v020c_anchor_replay` remains the incumbent at `186` matches / `33` FNs /
  `25` FPs.
- v022 variants all regressed, especially on dense case `67`.
- The first v023 axis should avoid broad cleanup language and instead change
  the model's internal target-selection ritual.

## v023a Axis

Use a visible-center pin map: identify one visual body center per target before
creating boxes. This is intended to preserve dense separable targets without
inviting broad row or context boxes.

Result: rejected. `v023a_visible_center_pin_map` scored `177/42/33`; controls
passed, but case `67` collapsed to `1/10/11` and case `84` worsened to
`6/7/1`. Lesson: adding a new target-selection ritual still destabilizes dense
formation behavior.

## v023b Axis

Preserve v020c almost verbatim. Add only a narrow sparse-scene singleton audit
that must not run when multiple targets, rows, clusters, or dense formations are
visible. The goal is to reduce isolated false positives without disturbing case
`67`-style dense recall.

Result: rejected. `v023b_dense_safe_singleton_audit` scored `173/46/32`;
controls passed, but case `67` again collapsed to `1/10/11`.

Inspection note: v020c's case `67` predictions were row-aligned close enough to
match 9 targets, while v023a/v023b shifted the row upward/left and produced
nearly all misses plus extras. The next axis should target bbox placement drift
instead of filtering.

## v023c Axis

Use lower-body / body-baseline anchoring for small dusty target rows. Preserve
v020c's context-shadow balance, but explicitly tell the model not to anchor
boxes on dust plumes, top edges, or leading empty space.

Result: rejected. `v023c_body_baseline_anchor` scored `174/45/38`; controls
passed, but case `67` stayed at `1/10/11` and false positives rose.

## Pivot After v023a-c

The first three continuation candidates all regressed and all collapsed case
`67`. The next pivot is explicit anti-drift calibration: not "find centers" or
"filter extras," but "when dust/row cues pull boxes upward-left, bias final
boxes toward the lower/right solid vehicle body."

## v023d Axis

Use a dust-row anti-drift calibration for small vehicle rows: keep the v020c
context-shadow balance but tell the model to anchor boxes on solid vehicle body
mass when dust, plumes, road edges, or repeated row spacing tug boxes upward or
left.

Result: rejected. `v023d_dust_row_antidrift_calibration` scored `175/44/34`;
controls passed, but case `67` again stayed at `1/10/11` and case `84` slipped
to `5/8/1`. Lesson: the corrective rule itself appears to perturb the detector
away from the v020c coordinate pattern. The next axis should not add another
new detection ritual. It should keep v020c nearly intact and add only a tiny
output-stability rail.

## v023e Axis

Use v020c as the actual prompt body and add only a short final stability rail:
do not move a valid box away from the connected body during the audit, keep
dense-row boxes ordered left-to-right, and never replace a visible body box
with dust, smoke, gap, or row-position coordinates. This tests whether the
problem is instruction overload rather than missing anti-drift semantics.

Result: rejected. `v023e_v020c_stability_rail` scored `171/48/35`; controls
passed, but case `67` still collapsed to `1/10/11`. Lesson: even a tiny
addition to v020c can move Qwen away from the fragile coordinate pattern that
made v020c strong. The next axis should stop adding to v020c and instead
compress the winning ideas into a shorter prompt, closer to the upstream
brevity lesson while preserving the extra-box audit.

## v023f Axis

Use a compact shadow-audit prompt: fewer bullets, no named mental ritual, no
v020c/v019c calibration language, and only the concepts that repeatedly won:
visible connected bodies, context cues as search aids only, split rows only by
visible bodies, and one final duplicate/context/group-box audit. This tests
whether the model performs better when the same policy is presented as a small
checklist rather than a long procedure.

Result: rejected, but informative. `v023f_compact_shadow_audit` scored
`182/37/66`; controls passed and case `84` recovered to `8/5/0`, but false
positives exploded. Top pathology: case `110` generated a 19-box stair-step
sequence from only a few visible bodies, and case `67` again generated a
regular row shifted above/left of the reference row. Lesson: compression
improves recall but removes the anti-extrapolation brake. The next axis should
keep the compact recall core but add a geometric hallucination fuse against
arithmetic/stair-step box chains and extrapolated row continuation.

## v023g Axis

Use `v023f` as the recall core, but add a "ruler-chain veto": if candidate boxes
form a regular arithmetic sequence, staircase, border strip, or evenly spaced
line where bodies are not individually visible, delete the unsupported sequence
members. This targets the exact `110`/`67` runaway pattern without reintroducing
the longer v020c ritual.

Result: rejected. `v023g_compact_ruler_chain_veto` scored `183/36/71`; controls
were nominally safe, but the candidate increased false positives and added
extra boxes on the positive-control case `155`. The explicit pattern-veto
wording appears to have made Qwen attend to the bad geometry rather than
removing it. Lesson: avoid negative named-pattern prompts. The next axis should
use positive evidence accounting instead: every output must have its own
unique visible-body signature.

## v023h Axis

Use a private one-object ledger: each final detection must be backed by one
unique visible body signature, such as a silhouette, body edge, texture patch,
ground-contact footprint, chassis/hull/wreck mass, or exterior-structure
boundary. This reframes precision as positive evidence needed for inclusion,
instead of another list of things to reject.

Result: rejected. `v023h_unique_body_signature_ledger` scored `173/46/49`.
It repaired the case `110` runaway compared with `v023f/g`, but lost too much
recall and still collapsed case `67`. Lesson: positive evidence accounting can
control an FP explosion, but the ledger framing is too heavy and recall-hostile.

## Research Note: Qwen Grounding Style

Quick source check during the loop:

- Official Qwen2.5-VL material emphasizes visual localization through
  bounding boxes/points and stable JSON-style outputs for coordinates and
  attributes: https://qwenlm.github.io/blog/qwen2.5-vl/
- Qwen-family object-grounding examples are generally concise: ask the model to
  locate or detect objects and return structured JSON, rather than long
  procedural reasoning prompts.

Applied lesson: try a concise, JSON-grounding-native prompt that uses a silent
count lock before box output, instead of another long audit/ledger prompt.

## v023i Axis

Use official-style grounding brevity plus a count lock: silently count distinct
visible target bodies/exterior structures first, then output exactly one tight
box per counted item. This aims to prevent duplicate/chain outputs while
staying closer to the prompt style Qwen was trained to follow.

Result: rejected as a win, but useful. `v023i_official_style_count_lock` scored
`178/41/40`; controls passed and case `84` stayed at `8/5/0`, but false
positives remained too high and case `67` only improved from `1/10/11` to
`2/9/10`. Lesson: official-style brevity helps some recall-pressure cases, but
still lacks v020c's precision and coordinate pattern.

## v023j Axis

Return to the v020c incumbent but remove experiment-history wording such as
"v019c" and "prior runs." Preserve the actual context-shadow and extra-box
audit logic. This tests whether v020c's strong behavior can be kept while
reducing irrelevant meta-language that may not belong in production config.

Result: rejected. `v023j_v020c_no_history_clean` scored `174/45/30`. It kept
FPs relatively controlled and case `110` had no FPs, but recall fell hard
against the v020c anchor. Lesson: the exact v020c wording is strangely load
bearing. The next axis should keep v020c's wording intact and add only a
missed-target second pass for multi-target scenes.

## v023k Axis

Use exact v020c plus a narrow missed-target pass after the extra-box audit:
look for unboxed visible target bodies in multi-target scenes, but add only
targets that meet the same visible-body evidence standard as accepted boxes.
This attacks v020c's remaining FNs in cases like `84`, `110`, and `160` while
trying not to reopen the FP flood.

Result: rejected. `v023k_v020c_missed_target_pass` scored `172/47/35`.
Adding an explicit recall pass broke the v020c balance instead of improving
it.

## Fresh Incumbent Replay

`v020c_anchor_replay` was rerun inside the v023 package and exactly reproduced
the incumbent score: `186/33/25`, controls passed. This confirms the champion
is stable under the current backend and that the v023 regressions are prompt
effects, not backend drift.

## v023l Axis

Keep v020c exact, but add only a tiny silent QA loupe at the end: compare final
boxes against the image once, fix only clear visual errors, and otherwise keep
the audit result. This tests whether a non-semantic quality-check instruction
can improve small errors without perturbing the selection policy.

Result: rejected. `v023l_v020c_silent_qa_loupe` scored `175/44/35`, and again
collapsed case `67`. Even a generic QA instruction perturbs the stable v020c
selection behavior.

## Visual Review Note

Reviewed high-FN cases directly:

- `84`: perspective row of parked military vehicles. v020c gets the foreground
  and mid-row bodies but misses several far/partly visible row vehicles.
- `110`: road convoy scene with a large foreground armored vehicle plus smaller
  distant vehicles. v020c avoids the runaway FP chain but misses several
  distant targets.
- `160`: urban damaged-structure scene with multiple small vehicles/structures.
- `67`: dusty moving row where v020c is uniquely stable; most added prompts
  shift boxes upward/left into dust/spacing.

Applied lesson: if we add anything, make it a narrow perspective-depth recall
rule for distant/partly visible bodies, while preserving v020c's context-shadow
audit.

## v023m Axis

Use exact v020c plus a perspective-depth recall pass: in rows/roads/convoys
receding into depth, count distant or partly visible target bodies when enough
body outline remains, but keep the same context-shadow audit. This targets
`84` and `110` rather than generic recall.

Result: rejected. `v023m_v020c_perspective_depth_recall` needed partial-run
recovery after repeated timeout-style exits, but the completed row scored
`171/48/32`; controls passed and case `67` again collapsed to `1/10/11`.
Lesson: even visually grounded additions aimed at known FN cases perturb the
incumbent. Next pivot: stop adding detection semantics. Try a control-surface
lock that preserves the exact v020c detector policy and only asks Qwen to apply
it literally, without inventing new criteria or extra detections.

## v023n Axis

Use exact v020c wording with a tiny policy-lock header. This tests whether a
non-semantic instruction-control wrapper can preserve v020c while reducing
drift, without changing the detection rule set.

Result: rejected. `v023n_v020c_locked_policy_header` scored `173/46/32`;
controls passed, but the tiny header still collapsed case `67` to `1/10/11`.
Lesson: even instruction-control text outside the detector policy perturbs the
winner. Next pivot: presentation-only reshaping with no new visual rule. Try
frontloading the JSON/output contract while keeping the v020c detector policy
itself unchanged.

## v023o Axis

Use the same v020c detection rule set but move the output and bbox contract
near the top, closer to official Qwen grounding examples that ask for JSON bbox
objects directly. This is a prompt-shape test, not a new detection tactic.

Result: rejected. `v023o_v020c_output_contract_first` scored `177/42/53`;
controls passed, but false positives jumped and case `67` still collapsed to
`1/10/11`. Lesson: the original v020c order matters. Schema-forward ordering
loosens the precision audit.

Incumbent error concentration after rechecking `v020c_anchor_replay`: `67`,
`160`, `84`, `110`, `66`, then isolated FP-heavy one-target cases such as `28`,
`97`, and `105`. Next axis should target coordinate/support quality rather than
adding recall. Try a four-edge boundary test so each output box side is
anchored by visible target-body or exterior-structure pixels, not smoke, dust,
road, spacing, or debris.

## v023p Axis

Use a four-edge boundary detector: each side of each final bbox must be
supported by visible target pixels or a visible exterior-structure boundary.
This is intended to trim context boxes while improving coordinate fit on dense
and partly visible targets.

Result: rejected. `v023p_four_edge_boundary_detector` scored `176/43/36`;
case `155` gained one FP, case `67` improved only slightly to `2/9/9`, and
case `84` was `7/6/0`. Lesson: edge-boundary language has some signal for
partial/dense targets, but replacing v020c's context-shadow structure loses too
much. Next test: keep v020c intact and only swap the extra-box audit into an
edge-support audit.

## v023q Axis

Use v020c context-shadow selection, but replace only the final extra-box audit
with an edge-support audit. This tries to keep v020c's dense-row coordinate
pattern while using v023p's useful support language only at cleanup time.

Result: rejected. `v023q_v020c_edge_support_audit_swap` scored `173/46/32`,
added one FP on `155`, and still collapsed `67` to `1/10/11`. Lesson:
edge-support wording is not a safe cleanup lever; it perturbs the row pattern
and weakens controls.

Next pivot: make dense rows an explicit exception instead of trying to clean
them up. v020c's best behavior is unusually row-friendly. Preserve that in
scenes with many small similar visible bodies, then apply a stricter audit only
outside dense rows.

## v023r Axis

Use v020c as the base, add a dense-row preservation exception, and tighten
singletons/non-row extras. This tries to keep `67` while reducing isolated FPs.

Result: rejected. `v023r_dense_row_exception_precision_audit` scored
`175/44/36`; controls passed, `84` stayed at `8/5/0`, but `67` still collapsed
to `1/10/11` and `97` regressed. Lesson: explicitly naming dense-row
preservation still becomes an attractor and does not preserve the incumbent's
coordinate pattern.

Additional web/source note: Qwen-family grounding examples generally use short
requests to detect/outline objects and return JSON bbox coordinates. Alibaba's
Qwen vision docs describe object detection by asking for detected item bbox
coordinates in JSON, and Qwen examples commonly emit JSON-style coordinate
objects. The local counterweight is that compact v023f improved recall but
exploded FPs, so the next concise prompt must be conservative.

## v023s Axis

Use a Qwen-native concise detector: ask for all visible target bodies in JSON,
with a small conservative support rule and no long procedural ritual. This
tests whether brevity plus explicit visible-body conservatism can outperform
both upstream-style recall and v020c-style audit.

Result: useful but not winner. `v023s_qwen_native_conservative_json` scored
`190/29/37`; controls passed. It beat v020c on recall and recovered case `67`
to `8/3/4`, but total error stayed worse than v020c because FPs rose. Error
map: `84`, `67`, `110`, `66`, `160`, plus one-target/sparse FP cases such as
`28`, `103`, `97`, and `105`.

Next axis: keep v023s's concise recall core and add only a tiny duplicate /
singleton-collapse audit. The audit should reduce extra boxes in one-target
and sparse scenes while preserving one-per-visible-body behavior in dense rows.

## v023t Axis

Use v023s plus a compact duplicate/singleton collapse audit.

Result: rejected. `v023t_qwen_native_duplicate_collapse` scored `178/41/41`.
The collapse audit erased the v023s recall gain and pushed `67` back to
`2/9/10`. Lesson: global duplicate-collapse wording is too intrusive. The
next test should leave dense rows alone and apply cleanup only to sparse or
singleton scenes.

## v023u Axis

Use v023s plus sparse-scene-only cleanup. This tries to reduce one-target and
sparse-scene FPs without touching dense rows, convoys, or clusters.

Result: rejected. `v023u_qwen_native_sparse_only_cleanup` scored `180/39/34`.
It reduced FPs versus v023s but destroyed the recall recovery, again pushing
`67` down to `2/9/10`. Lesson: even sparse-only cleanup language changes dense
row behavior.

Direct v023s output inspection showed the major FP modes are often not random:
large overlapping/nested boxes on the same building/vehicle, building quadrant
tiling, and telescoping boxes on a single road/convoy object. Next axis: keep
v023s but add an overlap/nesting guard that collapses boxes only when they
describe the same visible body or continuous building, while preserving
side-by-side row members.

## v023v Axis

Use v023s plus a nested/overlap guard.

Result: rejected. `v023v_qwen_native_nested_overlap_guard` scored
`182/37/42`; controls passed, but `67` collapsed to `2/9/10`. Lesson: even a
guard intended for nested boxes changes dense-row military-equipment behavior.

Next pivot: make the cleanup target-type specific. v023s's useful gain is
mostly military-equipment recall, while inspected FPs include building tiling
and intact/peripheral building boxes. Add a building-only centrality/tiling
guard while leaving military-equipment behavior unchanged.

## v023w Axis

Use v023s plus a building-only centrality and tiling guard.

Result: rejected. `v023w_qwen_native_building_centrality_guard` scored
`178/41/38`; controls passed, but `67` again collapsed to `2/9/10`. Lesson:
even target-type-specific added sections perturb the useful v023s military-row
behavior.

Next pivot: change v023s by subtraction instead of addition. The broad include
terms "wreck mass", "wheel/track contact", and "silhouette" may invite extra
boxes. Try a shorter connected-body-only prompt with the same native JSON style
and no extra cleanup sections.

## v023x Axis

Use a reduced v023s: concise JSON grounding with connected visible body or
exterior structure only, removing broad evidence terms that may cause FPs.

Result: rejected. `v023x_qwen_native_connected_body_only` scored `180/39/48`.
Subtraction removed useful stabilizers and caused `67` to explode to
`2/9/15`. Lesson: v023s's broad support list is not merely permissive; it
helps stabilize the row enough to get 8 matches.

Next axis: keep v023s intact and add only row count discipline. The goal is to
reduce v023s's overproduction in rows (`66`, `67`) without triggering the
global cleanup collapse seen in `v023t/u/v/w`.

## v023y Axis

Use v023s plus row body-center count discipline.

Result: rejected. `v023y_qwen_native_row_count_discipline` scored `180/39/42`;
`84` improved to `8/5/0`, but `67` collapsed to `1/10/11`. Lesson: even
row-only discipline changes the coordinate behavior away from v023s.

Next axis: avoid explicit cleanup mechanics. Preserve concise native grounding
but shift the confidence threshold: output only detections whose visible target
evidence is strong enough to be confidently boxed.

## v023z Axis

Use v023s-style concise JSON grounding with a high-confidence visible-evidence
threshold.
## v024a Axis: COCO-Style Instance Annotation

- Trigger: `v023z_qwen_native_high_confidence_filter` finished at `178/41/37`; controls passed, but dense case `67` collapsed to `2/9/10`.
- Lesson: confidence, cleanup, duplicate-collapse, sparse-cleanup, and connected-body filters all perturb Qwen away from row enumeration.
- New tactic: avoid reasoning/audit language and instead frame detection as strict instance annotation: one physical visible target instance, one whole-instance box, scan rows/convoys/clusters, no subparts/effects/context.
- Expected risk: may behave like v023s and overproduce if “instance annotation” lowers the threshold too far; pass/fail is whether it preserves case `67` while reducing v023s-style extras.
## v024b Axis: Minimal Image-Wide Scan Graft

- Trigger: `v024a_coco_instance_annotator` finished at `184/35/44`, not a winner. It recovered some non-dense misses (`40`, `144`, `160`) but worsened `67`, `84`, `103`, and sparse false positives.
- Lesson: the annotation frame increases recall but weakens v020c's extra-box discipline.
- New tactic: preserve v020c nearly exactly and graft only a pre-decision full-image scan reminder before the context-shadow reversal, avoiding new final cleanup or confidence language.
- Expected risk: even tiny preambles have perturbed v020c before; this tests whether scan ordering is separable from annotation-mode overproduction.
## v024c Axis: Official-Style Terse Grounding

- Trigger: `v024b_v020c_imagewide_scan_first` finished at `175/44/40`; it collapsed case `67` to `1/10/9` and added false positives on control case `155`.
- Lesson: even tiny v020c grafts can destabilize the row/control behavior, so stop grafting micro-preambles.
- Outside note: Qwen-family grounding examples commonly use concise locate/detect prompts plus JSON bbox output rather than long self-audit instructions.
- New tactic: a direct `Locate every visible BDA target... return JSON` prompt with only category list, dense-row enumeration, and context-only exclusions.
- Expected risk: may resemble upstream/v023s and raise FPs; useful if it restores row behavior while avoiding v020c sensitivity.
## v024d Axis: v020c Instruction Order Test

- Trigger: `v024c_official_style_ground_all_targets` finished at `166/53/37`; concise official-style grounding undercounted badly and again collapsed `67` to `2/9/10`.
- Lesson: this dataset needs v020c's context-shadow and audit scaffold; direct grounding is not enough.
- New tactic: keep v020c text, but move the existing `FINAL BALANCE` recall protection before `EXTRA-BOX AUDIT` so the model reads the recall guard before pruning.
- Expected risk: ordering alone may perturb the prompt; if it does, v020c's exact sequence is confirmed load-bearing.
## v024e Axis: BBox Placement Instead Of Selection Policy

- Trigger: visual/source inspection of case `67` showed v020c's better row outputs are anchored near the tank body/track line, while failed variants often float boxes upward into dust/context.
- Lesson: selection-policy edits keep damaging dense recall. Try improving IoU/FP behavior through box-placement calibration only.
- New tactic: preserve v020c selection text exactly and add one bbox-format note: box visible physical extent; for vehicles include lower hull/wheel/track/ground-contact edge when visible; do not float boxes onto smoke/dust/shadow.
- Expected risk: bbox-format notes may still perturb detection count, but this is a different lever than target filtering.
## v024f Axis: Silent Three-Role Arbiter

- Trigger: `v024e_v020c_bbox_physical_extent_calibration` finished at `168/51/30`; it reduced case `66` FPs but still collapsed `67` to `1/10/9`.
- Lesson: even bbox-placement notes alter target selection. Single-rule edits are not preserving the row/precision balance.
- New tactic: separate internal functions instead of adding one more veto: SCOUT finds all bodies, SKEPTIC rejects context-only candidates without removing true small/crowded bodies, BOXER places tight final boxes.
- Expected risk: role framing may be too abstract or increase FPs, but it is a different control structure than v020c micro-edits.
## v024g Axis: Output Sequencing Cue

- Trigger: `v024f_silent_three_role_arbiter` finished at `183/36/44`; it recovered several non-dense misses but still collapsed `67` to `2/9/10` and raised FPs.
- Lesson: internal role framing is not enough; dense-row enumeration remains the recurring fragile behavior.
- New tactic: preserve v020c selection policy and add only an output sequencing cue: in rows/convoys/clusters, list detections from one visible body to the next rather than skipping through the row.
- Expected risk: even output-only wording may perturb selection, but it avoids new veto/cleanup semantics.
## v024h Axis: Vehicle Body At Dust-Plume Base

- Trigger: `v024g_v020c_visual_sequence_output` finished at `182/37/39`; it improved `11`, `14`, `84`, `97`, `144`, `164`, and `172`, but failed `155` with one FP and collapsed `67` to `1/10/11`.
- Visual/source diagnosis: bad `67` variants output the convoy sequence but place small boxes too high into dust/plume context; v020c's better boxes are lower and closer to the visible vehicle body/track line.
- New tactic: preserve v020c policy and add only one GOOD FINAL BOX definition: for vehicles in dust, body means dark hull/chassis/turret/wheel/track mass at the base of the plume, not the plume itself.
- Expected risk: this may still perturb dense behavior, but it targets the observed geometry failure without adding count/order/cleanup instructions.
## v024i Axis: Subtractive v023s Body-Mass-Only Include List

- Trigger: `v024h_v020c_dust_base_vehicle_body` finished at `174/45/30`; it kept controls and some FP gains but still collapsed `67` to `1/10/11`.
- Lesson: additive v020c edits remain too fragile. Switch to subtractive edits on v023s, the strongest recall branch.
- New tactic: preserve v023s concise structure but narrow the include support list to visible body, wreck mass, hull/chassis/roofline, or exterior building structure; remove broad `wheel/track contact`, generic `silhouette`, and `wall/roof boundary` phrasing.
- Expected risk: may lower recall; useful if it preserves v023s row behavior while cutting FPs.

## v024j Axis: One-Term v023s Silhouette Ablation

- Trigger: `v024i_v023s_body_mass_only` finished at `183/36/40`; it partially preserved dense row behavior better than additive v020c edits, but removing three support terms cost too much recall and left FPs high.
- Lesson: the v023s support list likely contains both useful anchors and FP sources. Test one removed term at a time instead of narrowing the support list wholesale.
- New tactic: preserve v023s structure and remove only generic `silhouette`, while keeping wheel/track contact and exterior wall/roof boundary.
- Expected risk: if `silhouette` was a recall stabilizer, dense rows or partially obscured targets may degrade; if it was an FP source, this should lower false positives without the v024i recall loss.

Result: rejected. `v024j_v023s_no_silhouette_ablation` scored `179/40/39`;
controls passed, but case `67` collapsed to `2/9/9`. Lesson: generic
`silhouette` is not just an FP source; it appears to stabilize small or
partially obscured row targets.

## v024k Axis: One-Term v023s Wall/Roof-Boundary Ablation

- Trigger: `v024j` proved `silhouette` is load-bearing. Continue the one-term support-list isolation instead of guessing.
- New tactic: preserve v023s structure and remove only `exterior wall/roof boundary`, while keeping `silhouette` and `wheel/track contact`.
- Expected risk: may hurt building recall if that phrase was the building anchor; useful if it trims structure/context FPs without damaging vehicle row behavior.

Result: rejected. `v024k_v023s_no_wall_roof_boundary_ablation` scored
`182/37/39`; controls passed, but case `67` collapsed to `2/9/11`.
Lesson: removing only wall/roof-boundary improves no global error axis and
still destabilizes the row. The v023s include sentence is behaving like a
coupled pattern, not independent knobs.

## v024l Axis: One-Term v023s Wheel/Track-Contact Ablation

- Trigger: `v024j` and `v024k` both collapsed case `67`, but the support-list isolation is incomplete.
- New tactic: remove only `wheel/track contact`, preserving `silhouette` and `exterior wall/roof boundary`.
- Expected risk: high for vehicle rows, because wheel/track contact may be the phrase that keeps lower vehicle-body anchoring; useful as the final isolation check before pivoting away from support-list ablation.

Result: near-miss learning row. `v024l_v023s_no_wheel_track_ablation`
scored `188/31/35`; controls passed, case `67` stayed strong at `9/2/3`,
and case `84` improved over v023s by removing three FPs. It still lost to
v020c because sparse/background false positives grew, especially intact or
background building boxes in cases like `16` and `103`.

## v024m Axis: BDA Salience Gate

- Trigger: v024l showed useful recall but too many scene-inventory boxes.
- Local diagnosis: v024l's extra boxes are often intact/background buildings or scene-setting structures; its wins are true multi-target recall cases such as `172`, `14`, `164`, and `42`.
- Outside grounding: Qwen-family grounding docs favor concise JSON bbox prompts, so this candidate keeps the v024l compact style and changes only the domain salience policy rather than adding long audit scaffolding.
- New tactic: add a BDA salience gate. Military equipment remains reportable when visible, but buildings should be damaged, primary, foreground, or battle-relevant rather than merely visible background/campus/facade structures.
- Expected risk: may undercount legitimate no-damage building targets; useful if it cuts sparse building FPs without disturbing dense vehicle rows.

Result: rejected but informative. `v024m_v024l_bda_salience_gate` scored
`173/46/37`; it improved building/sparse FP cases like `103`, `105`, and
`16`, but collapsed case `67` to `1/10/11`. Lesson: global salience wording
helps building overproduction but changes military-equipment row behavior.

## v024n Axis: Building-Only De-Tiling With Equipment-Row Exemption

- Trigger: v024m proved salience has signal, but broad BDA framing harmed dense equipment rows.
- New tactic: keep v024l and replace global salience with a narrow building-only de-tiling rule, explicitly saying it does not apply to military equipment rows, convoys, or clusters.
- Expected risk: even building-only wording has previously perturbed dense behavior; useful if the explicit exemption protects case `67` while keeping v024m's building-FP reductions.

Result: hard rejection. `v024n_v024l_building_only_detiling` scored
`181/38/102`; case `103` exploded to 65 predicted boxes. Lesson: long
building-specific sections can make Qwen tile buildings more aggressively,
even when the section says not to. Avoid long building blocks.

## v024o Axis: Micro Building-Piece Exclusion

- Trigger: v024m had real building-FP signal, v024n showed long building rules are dangerous.
- New tactic: return to v024l and add only one short phrase to the existing exclusion list: `intact background building pieces, facade or roof tiles`.
- Expected risk: even a micro building phrase may perturb dense rows; useful if it cuts `103`-style building tiling without a new section or global frame.
