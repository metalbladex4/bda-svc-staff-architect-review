# Qwen Detection Prompt Surface Inspection

## Purpose

This note is the local inspection packet for the next Qwen detection-cycle
decision.

The goal is to answer four questions before drafting another detect-only
candidate:

1. What is the **actual current** `detect_objects` prompt surface on the active
   Qwen line?
2. How does the current active surface compare to the historical `v006`
   detection winner?
3. How much of the current behavior difference between `1.2` and `1.3` comes
   from prompt-template wording versus doctrine injection?
4. Do we need more online research before the next experiment, or do we already
   have enough grounded evidence to define the next A/B lanes safely?

## Sources Re-Reviewed

### Runtime truth

- `src/bda_svc/pipeline/config.yaml`
- `src/bda_svc/pipeline/model.py`
- `src/bda_svc/pipeline/utilities.py`
- `src/bda_svc/pipeline/interfaces.py`

### Local Qwen references

- `z_reference_docs/Prompting/Qwen/Qwen3-VL-8B-Instruct_Model_Card.md`
- `z_reference_docs/Prompting/Qwen/Qwen_3_Chat_template_deep_dive_Prompting_Behavior.md`
- `z_reference_docs/Prompting/Qwen/Alibaba_Cloud_vision_docs_for_Qwen-VL.md`
- `z_reference_docs/Prompting/Research_Loops/2.main__qwen3-vl_8b-instruct/v004/run01_2026-04-12_155635_EDT/research.md`
- `z_reference_docs/Prompting/Research_Loops/2.main__qwen3-vl_8b-instruct/v005/run01_2026-04-12_161314_EDT/research.md`
- `z_reference_docs/Prompting/Research_Loops/2.main__qwen3-vl_8b-instruct/v006/run01_2026-04-12_162217_EDT/research.md`

### Targeted official online check

- Alibaba Cloud Model Studio Qwen vision docs:
  <https://www.alibabacloud.com/help/en/model-studio/vision/>

Working implication from that targeted check:

- Qwen’s current official guidance says that, in general conversational usage
  without tool calling, system messages are not always preferred and important
  instructions can be carried through the user message instead.

This is enough to justify a **system-role hypothesis lane** later. It is **not**
strong enough by itself to justify rewriting the runtime interface now.

## Online Research Decision

No broader online research is needed before the next Qwen inspection or A/B
cycle.

Why:

- the local Qwen source pack already covers:
  - grounding/localization capability framing
  - prompt salience lessons from the earlier `v004` -> `v006` cycle
  - the confirmed historical `v006` detect winner
- the one current official Qwen check already surfaced the only new ambiguity
  that matters right now:
  - whether the shared system prompt may be weakening instruction authority for
    this family

Working rule:

- do not browse more unless the later **system-role lane** stays ambiguous after
  we have local A/B evidence

## Current Surface Inventory

### Branch roles

- `1.2`
  - canonical active Qwen control
  - carries the active `v009` stack
  - carries the confirmed `v006` detection lineage
- `1.3`
  - doctrine-side verification lane
  - should not be treated as the active Qwen direction by default

### Template-level comparison

The current `detect_objects` prompt template in:

- `1.2` active branch
- `1.3` doctrine branch

is currently identical.

That means any current branch-to-branch detect difference comes from:

- doctrine injection
- or later candidate edits

not from a hidden prompt-template split that already exists today.

### Historical comparison against `v006`

The current template differs from the historical `v006` detect winner by only
two meaningful lines:

```diff
--- v006
+++ current_1.2
@@ -7,7 +7,6 @@
 RULES
 - First identify all valid targets using the target-type specific detection guidance below.
 - Then produce exactly one bounding box per valid target.
-- Do not produce a bounding box of all zeroes if target_type is not "object_not_found".
 - The number of detections must match the number of targets identified.
 - If multiple valid targets are visibly distinct, output multiple detections. Do not merge neighboring targets into one box.

@@ -46,6 +45,7 @@
 OUTPUT
 Return valid JSON only.
 Return a JSON object with a top-level detections field.
+If no valid targets are visible, return {"detections": []}.

 OUTPUT SCHEMA
 {
```

Working implication:

- the current Qwen detect surface is **not** a wholesale departure from `v006`
- this is now an instruction-weighting / hierarchy problem, not a rewrite from
  scratch problem

## Rendered Prompt Comparison

### Current rendered `1.2`

This is the full current rendered detection prompt on the active `1.2` branch,
with doctrine injected:

```text
Perform a VISUAL-ONLY object detection.

TASK
Detect targets whose doctrinal target_type is one of:
buildings, military_equipment

RULES
- First identify all valid targets using the target-type specific detection guidance below.
- Then produce exactly one bounding box per valid target.
- The number of detections must match the number of targets identified.
- If multiple valid targets are visibly distinct, output multiple detections. Do not merge neighboring targets into one box.

TARGET-TYPE SPECIFIC DETECTION GUIDANCE
buildings:

Detect only buildings that are central to the scene or essential to interpreting it. Skip background or peripheral buildings that do not materially affect the scene.

military_equipment:

Military equipment is generally defined as armored vehicles, artillery systems, trucks, locomotives, aircrafts, rocket and missile systems, radar antennas, or fire control components.
Detect military equipment as individual objects -- do NOT merge multiple objects into one such as a group of vehicles.
Include all pieces of military equipment including partially visible ones, only skip objects whose boundaries cannot be distinguished from surrounding objects or background.

BOXING RULE
- Box the visible connected man-made body or structure of each target only.
- Use fire, smoke, muzzle flash, or debris only to help locate the target, not to define the box boundary.
- If smoke, flame, or dust hides part of a target, keep the box on the visible connected target body that remains.
- If two targets are visibly separate, even with nearby debris or overlap in the scene, return separate boxes.
- For buildings, return separate boxes for visibly separate buildings or clearly separate damaged structures. Do not merge neighboring structures into one box unless they are visibly one continuous target body.
- For buildings, only detect visible exterior building structures or clearly collapsed exterior structural remains.
- Do not treat indoor rooms, office interiors, cubicles, partitions, furniture, interior walls, ceiling tiles, or ordinary room contents as doctrinal building targets.
- If the image is primarily an indoor scene and no visible exterior building structure or collapsed structural remains are present, do not detect a building target.
- On intact or operational targets, box the visible target body only when the doctrinal target itself is clearly visible. Do not widen the detection prior from scene context alone.
- Do not box the smoke plume, flame column, muzzle flash, debris field between targets, rail bed, road, shadow, or empty ground.

CONTRASTIVE EXAMPLES
- Correct: a burning vehicle with smoke to the right -> box the visible connected vehicle body only.
- Correct: a firing vehicle with muzzle flash -> box the vehicle body only, not the flash or smoke.
- Correct: two neighboring damaged buildings with separate visible masses -> return separate boxes.
- Correct: collapsed exterior structural remains of two buildings -> return separate boxes if the structures are distinct.
- Incorrect: merge adjacent targets because smoke or debris overlaps them in the scene.
- Incorrect: treat an office interior, cubicle wall, or room partition as a building target.
- Incorrect: box the smoke plume, flash, empty terrain, or only the smallest local burn patch.

OUTPUT DISCIPLINE
- Return only the doctrinal target_type category.
- Do not infer a finer subtype such as locomotive, train car, truck, or artillery piece.

BOUNDING BOX FORMAT
- Format: [xmin, ymin, xmax, ymax]
- Coordinate scale: normalized coordinates from 0 to 1000

OUTPUT
Return valid JSON only.
Return a JSON object with a top-level detections field.
If no valid targets are visible, return {"detections": []}.

OUTPUT SCHEMA
{
  "detections": [
    {
      "target_type": string,
      "bbox": [xmin, ymin, xmax, ymax]
    }
  ]
}
```

### Current rendered `1.3`

This is the full current rendered detection prompt on the doctrine branch, with
the doctrine candidate injected:

```text
Perform a VISUAL-ONLY object detection.

TASK
Detect targets whose doctrinal target_type is one of:
buildings, military_equipment

RULES
- First identify all valid targets using the target-type specific detection guidance below.
- Then produce exactly one bounding box per valid target.
- The number of detections must match the number of targets identified.
- If multiple valid targets are visibly distinct, output multiple detections. Do not merge neighboring targets into one box.

TARGET-TYPE SPECIFIC DETECTION GUIDANCE
buildings:

Detect only visible exterior building bodies or collapsed exterior building remains that are central to the scene or essential to interpreting observed damage.
In mixed adjacent-building scenes, anchor each detection to the selected building body itself, not to neighboring intact buildings, distant background structures, or shared rubble/debris context.
Do not split off an adjacent standing facade as a separate damaged building unless that neighboring building is itself a clear independent scene-central target with visible direct exterior damage.
For one damaged building with connected wings or sections, prefer one detection on the visibly contiguous selected target body unless two independent building bodies are clearly separable and both are central to the scene.
Skip distant background or peripheral buildings that do not materially affect the scene.

military_equipment:

Military equipment includes armored vehicles, artillery systems, trucks, locomotives and rolling stock, aircraft, rocket and missile systems, radar antennas, and fire control components.
Detect military equipment as individual visible objects and do not merge separate objects into one detection.
Include partially visible equipment only when the visible target body is still distinguishable from surrounding objects or background.

BOXING RULE
- Box the visible connected man-made body or structure of each target only.
- Use fire, smoke, muzzle flash, or debris only to help locate the target, not to define the box boundary.
- If smoke, flame, or dust hides part of a target, keep the box on the visible connected target body that remains.
- If two targets are visibly separate, even with nearby debris or overlap in the scene, return separate boxes.
- For buildings, return separate boxes for visibly separate buildings or clearly separate damaged structures. Do not merge neighboring structures into one box unless they are visibly one continuous target body.
- For buildings, only detect visible exterior building structures or clearly collapsed exterior structural remains.
- Do not treat indoor rooms, office interiors, cubicles, partitions, furniture, interior walls, ceiling tiles, or ordinary room contents as doctrinal building targets.
- If the image is primarily an indoor scene and no visible exterior building structure or collapsed structural remains are present, do not detect a building target.
- On intact or operational targets, box the visible target body only when the doctrinal target itself is clearly visible. Do not widen the detection prior from scene context alone.
- Do not box the smoke plume, flame column, muzzle flash, debris field between targets, rail bed, road, shadow, or empty ground.

CONTRASTIVE EXAMPLES
- Correct: a burning vehicle with smoke to the right -> box the visible connected vehicle body only.
- Correct: a firing vehicle with muzzle flash -> box the vehicle body only, not the flash or smoke.
- Correct: two neighboring damaged buildings with separate visible masses -> return separate boxes.
- Correct: collapsed exterior structural remains of two buildings -> return separate boxes if the structures are distinct.
- Incorrect: merge adjacent targets because smoke or debris overlaps them in the scene.
- Incorrect: treat an office interior, cubicle wall, or room partition as a building target.
- Incorrect: box the smoke plume, flash, empty terrain, or only the smallest local burn patch.

OUTPUT DISCIPLINE
- Return only the doctrinal target_type category.
- Do not infer a finer subtype such as locomotive, train car, truck, or artillery piece.

BOUNDING BOX FORMAT
- Format: [xmin, ymin, xmax, ymax]
- Coordinate scale: normalized coordinates from 0 to 1000

OUTPUT
Return valid JSON only.
Return a JSON object with a top-level detections field.
If no valid targets are visible, return {"detections": []}.

OUTPUT SCHEMA
{
  "detections": [
    {
      "target_type": string,
      "bbox": [xmin, ymin, xmax, ymax]
    }
  ]
}
```

### Historical rendered `v006`

Because the active `1.2` doctrine remained unchanged on that line, the
historical `v006` winner differs from the current active rendered surface only
by the no-target contract lines shown earlier:

- it kept the explicit all-zero-bbox safeguard line
- it did **not** include the explicit `{"detections": []}` instruction

Operationally:

- the current active rendered `1.2` prompt is best understood as
  `v006 + inherited no-target contract change`

## Exact Branch-To-Branch Rendered Diff

At the rendered-prompt level, `1.2` and `1.3` differ only in the injected
doctrine block:

```diff
--- rendered_1.2
+++ rendered_1.3
@@ -13,13 +13,17 @@
 TARGET-TYPE SPECIFIC DETECTION GUIDANCE
 buildings:

-Detect only buildings that are central to the scene or essential to interpreting it. Skip background or peripheral buildings that do not materially affect the scene.
+Detect only visible exterior building bodies or collapsed exterior building remains that are central to the scene or essential to interpreting observed damage.
+In mixed adjacent-building scenes, anchor each detection to the selected building body itself, not to neighboring intact buildings, distant background structures, or shared rubble/debris context.
+Do not split off an adjacent standing facade as a separate damaged building unless that neighboring building is itself a clear independent scene-central target with visible direct exterior damage.
+For one damaged building with connected wings or sections, prefer one detection on the visibly contiguous selected target body unless two independent building bodies are clearly separable and both are central to the scene.
+Skip distant background or peripheral buildings that do not materially affect the scene.

 military_equipment:

-Military equipment is generally defined as armored vehicles, artillery systems, trucks, locomotives, aircrafts, rocket and missile systems, radar antennas, or fire control components.
-Detect military equipment as individual objects -- do NOT merge multiple objects into one such as a group of vehicles.
-Include all pieces of military equipment including partially visible ones, only skip objects whose boundaries cannot be distinguished from surrounding objects or background.
+Military equipment includes armored vehicles, artillery systems, trucks, locomotives and rolling stock, aircraft, rocket and missile systems, radar antennas, and fire control components.
+Detect military equipment as individual visible objects and do not merge separate objects into one detection.
+Include partially visible equipment only when the visible target body is still distinguishable from surrounding objects or background.
```

Working implication:

- `1.3` is not hiding a separate prompt-template world
- the current doctrine branch changes only the rendered doctrine block, not the
  surrounding prompt architecture

## Authority-Level Classification

This is the current authority stack for detection:

### 1. Shared system prompt

Role:

- generic analyst framing
- visual-only constraint
- general conservatism and schema-following posture

Strength:

- high formal priority in message role
- low task specificity

Risk:

- may be weaker than expected for Qwen if the family really prefers critical
  instructions in the user message

### 2. Top-level detection task and rules

Role:

- defines the actual job
- constrains target count and one-box-per-target behavior
- establishes the first broad object-detection contract

Strength:

- highest task-specific instruction block in the user message
- likely stronger than doctrine prose that appears later or more indirectly

### 3. Doctrine-injected category guidance

Role:

- target-family-specific meaning
- category-specific selection hints
- branch-dependent building/equipment wording

Strength:

- real and present in the prompt
- lower practical authority than it first appears, because it sits mid-prompt
  and is followed by stronger-looking general boxing rules

### 4. Generic boxing rules

Role:

- operational localization behavior
- target-body boundaries
- indoor-building exclusions
- intact-target handling
- non-target exclusion rules

Strength:

- very high practical salience
- this is the longest and most operationally concrete behavioral block

### 5. Contrastive examples

Role:

- edge-case steering
- concrete examples of good vs bad bounding behavior

Strength:

- historically strong on this Qwen line
- the earlier `v005` -> `v006` cycle strongly suggests compact examples helped
  more than longer abstract grounding prose

### 6. Output-format and schema rules

Role:

- JSON contract
- bbox format
- no-target behavior

Strength:

- very strong for output shape
- not necessarily strong for target-body selection quality

## Overlap And Competition Analysis

### Where `1.3` doctrine tries to help

The doctrine branch tries to make these ideas explicit:

- select the building body itself
- do not peel off neighboring standing facades casually
- prefer one contiguous damaged building body unless two bodies are clearly
  separable
- skip background/peripheral buildings

### What competes with it later

The generic boxing rules still say:

- return separate boxes for visibly separate buildings or clearly separate
  damaged structures
- only detect visible exterior building structures or clearly collapsed
  exterior structural remains

Those later generic rules are not wrong, but they are broader and likely more
salient. That means the model can still default to:

- scene partitioning
- “two damaged masses means two buildings”
- adjacent-structure carving

without being forced to respect the more nuanced doctrinal selection language
inserted earlier.

### Practical read

This is why the doctrine edits could be sensible and still fail:

- they were injected into a weaker middle layer
- the stronger later rules remained mostly unchanged
- the model’s old adjacent-building habit kept winning

## Main Inspection Conclusion

The current Qwen problem is most likely:

- **not** a missing doctrine concept
- **not** a fundamentally different current prompt from `v006`

It is more likely:

- an instruction-weighting problem inside the detection user prompt
- plus a possible message-hierarchy issue for the Qwen family

That means the best next intervention surface is:

- the actual detection user prompt

and only secondarily:

- the shared system-role usage pattern

## Candidate Lanes For The Next A/B Cycle

### Lane A — User-prompt weighting

Keep:

- shared system prompt unchanged
- doctrine unchanged within each branch

Change only:

- detection user prompt text

Focus:

- move the strongest adjacent-building selection rule into the top `RULES`
  block
- shorten or compress duplicated lower-value building wording later in the
  prompt
- reduce competition between doctrine prose and later generic boxing rules
- preserve the compact example-driven steering that historically helped `v006`

### Lane B — System-role hypothesis

Keep:

- runtime interfaces unchanged
- doctrine injection mechanism unchanged

Test:

- effective-config variants that reduce reliance on the shared system prompt and
  instead place the critical detection instructions inside the user prompt

Why this lane exists:

- official current Qwen guidance makes this plausible
- our current runtime still uses a short shared system prompt for everything
- the current family may respond better when the critical detection rules live
  in the user message

Working discipline:

- do not change code interfaces first
- use config-only experiment variants first
- if this lane shows strong but confounded signal, only then plan a runtime
  change later

## Candidate Shapes To Test Later

### Candidate A — User-prompt reordering only

- move the most important building target-body selection rule into the top
  `RULES` block
- keep the rest of the detect surface structurally similar
- remove or compress repeated lower-value building wording later in the prompt

### Candidate B — User-prompt salience plus example cleanup

- keep the core target-body rule compact
- reduce generic clutter in the later boxing section
- add one stronger adjacent-building contrastive example instead of more prose

### Candidate C — System-role lane

- minimize dependence on the shared system prompt for detection behavior
- place the strongest detection constraints into the user prompt
- judge only on detection outputs and bbox review artifacts

## Planned Evaluation Pack

Keep the next cycle detection-specific and building-heavy:

- `destroyed_building3`
- `destroyed_building4`
- `destroyed_building5`
- `destroyed_building6`
- `destroyed_building8`
- `operational_building2`
- `operational_building7`
- `operational_building91`
- `tank_pressure`
- `destroyed_tank15`
- `operational_tank4`
- `office_negative`

Primary judging questions:

1. Did `destroyed_building3` stop boxing the background building?
2. Did `destroyed_building4` improve target delimitation without collapsing the
   split the wrong way?
3. Did `destroyed_building6` become less like broad scene partitioning?
4. Did the office negative remain clean?
5. Did the tank controls remain acceptable?

## Final Decision For This Inspection

No more broad online research is needed now.

The best next move, when we are ready to execute, is:

1. keep Gemma untouched
2. treat `1.2` as the canonical active control
3. use `1.3` only as a doctrine-side verification lane
4. start with a **detect user-prompt weighting** candidate before spending
   effort on another doctrine-only rewrite
5. keep the system-role lane as an explicit secondary hypothesis, not as the
   first rewrite
