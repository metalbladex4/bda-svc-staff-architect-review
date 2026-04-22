# Detection Prompt Assembly Analysis

## Purpose

This note traces the exact Qwen `1.3` detection prompt assembly path so the
doctrine experiment can distinguish between:

- a doctrine text problem
- a detection prompt weighting problem
- a deeper model/runtime localization habit

The immediate question was whether `doctrine.yaml` is being injected strongly
enough for the detection model to treat it as a high-authority instruction.

## Exact Injection Path

The detection path is:

1. `BDAPipeline.__init__()` loads:
   - `config.yaml`
   - `doctrine.yaml`
2. `BDAPipeline._vlm_detections()` starts from
   `prompts.detect_objects` in `config.yaml`
3. It replaces:
   - `{categories}` with the top-level doctrine keys
   - `{detection_guidance}` with the result of
     `format_detection_doctrine(self.categories)`
   - `{bbox_format}` and `{bbox_scale}` with config-derived values
4. The assembled prompt is sent to Ollama as a single `user` message with the
   image attached
5. The shared `system` prompt is sent separately as a single `system` message

Relevant code paths:

- `src/bda_svc/pipeline/model.py`
- `src/bda_svc/pipeline/utilities.py`
- `src/bda_svc/pipeline/interfaces.py`

## What `format_detection_doctrine()` Actually Does

The doctrine helper is mechanically simple:

- it loads `doctrine.yaml`
- it iterates the selected categories in order
- it appends:
  - `buildings:`
  - raw `buildings.detection_guidance`
  - `military_equipment:`
  - raw `military_equipment.detection_guidance`
- it joins those sections with blank lines

Important implication:

- no ranking or emphasis is added
- no doctrinal text is promoted into the system prompt
- no selected doctrine lines are repeated in the stronger global rules block
- the doctrine text is inserted as plain mid-prompt prose

## Current Message Structure Sent To Ollama

For detection, the model currently receives:

1. `system` message
   - short, generic, visual-only analyst framing
2. `user` message
   - full detection prompt
   - attached image

There is no multi-turn reinforcement and no separate doctrinal message.
`think=False` is also hardcoded in the Ollama chat call.

## Relative Prompt Weight

From the fully assembled current Qwen `1.3` detection prompt:

- system prompt: 8 lines / 350 chars
- full detection user prompt: 70 lines / 4511 chars
- injected doctrine block alone: 13 lines / 1330 chars

That means doctrine is present, but it is only one block inside a much larger
user prompt.

## Where Doctrine Sits In The Prompt

The doctrine block is injected here:

- after the initial `TASK` and top-level `RULES`
- before the longer generic `BOXING RULE`
- before contrastive examples
- before output discipline and schema

That placement matters. The model reads doctrine before a long run of broader
boxing instructions and examples that may dominate behavior.

## Why This Likely Weakens Doctrine As A Lever

The current assembly suggests doctrine is not being treated as a maximally
authoritative instruction layer.

Reasons:

1. It is not in the system prompt.
2. It is not the last instruction block before output.
3. It is followed by a larger generic boxing section that already contains
   building-specific rules.
4. Some of those later generic building rules partially overlap with, soften,
   or compete with the doctrine block.
5. The doctrine block is formatted as raw prose paragraphs rather than a short
   high-salience checklist.

This does **not** mean doctrine is ignored. It does mean doctrine is probably
being treated as one mid-prompt reference block among many, not as the most
important directive in the detection stack.

## Practical Interpretation For The Qwen Adjacency Problem

This assembly is consistent with the run evidence:

- doctrine wording changes can slightly shift behavior
- but they do not reliably override the model's existing scene-partition and
  adjacent-building selection habit
- the stronger control seems to be the broader detection prompt surface, not
  `doctrine.yaml` alone

That is why `runtime_candidate_doctrine.v002.yaml` could be operationally
neutral on many scenes while still failing to fix:

- `destroyed_building3`
- `destroyed_building4`
- `destroyed_building6`

## Current Conclusion

The doctrine experiment taught something useful:

- `doctrine.yaml` is definitely part of the detection prompt
- but it is not injected with enough authority to be assumed the main lever
  for adjacent-building target selection

So the most likely next leverage point is:

- the detection prompt surface itself
- or the way doctrinal selection rules are elevated within that surface

not another doctrine-only rewrite by itself.

## Suggested Next Moves

If this line continues later, the clean next experiments are:

1. Detection-prompt experiment:
   move the strongest adjacent-building selection rules into the main
   high-authority detection rule block rather than leaving them only inside
   doctrine text.

2. Prompt-assembly experiment:
   test whether selected doctrine lines need to be repeated or elevated into a
   stricter instruction location.

3. Doctrine hold:
   keep doctrine focused on Phase-1 semantics and avoid using it as the only
   tool for fixing a localization habit that looks prompt-dominant.
