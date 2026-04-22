# Gemma 4 Operational Prompt Rules

This note captures the Gemma-family prompt rules that matter before we start
the first Gemma BDA prompt cycle.

## What We Must Assume Up Front

1. Gemma 4 supports a native `system` role.
2. Prefer framework chat templates over hand-rolled turn tokens when the
   runtime supports them cleanly.
3. For multimodal prompts, image content should come before text content when
   the interface allows that distinction.
4. Start with `thinking` disabled for the first BDA baseline.
5. If `thinking` is enabled later, do not carry earlier thinking traces into
   conversation history.
6. `E4B` is the active local-first target.
7. `E2B` is comparison-only during the bootstrap.
8. `26B` and `31B` remain reference sizes only until infrastructure changes.

## Immediate Implications For This Repo

- Keep the shared `system` prompt as a real system message for the Gemma line.
- Keep the current three-prompt-surface structure:
  - `system`
  - `detect_objects`
  - `assess_damage`
  - `summarize_scene`
- Keep the first Gemma line single-turn per surface, just as we did for the
  Qwen branch-aware line.
- Keep `think=False` for the initial Gemma baseline so the first comparison
  against Qwen `v009` is not confounded by reasoning-mode changes.

## Gemma-Specific Watch Points

### System-role behavior

Gemma 4 is different from the older Gemma 3 guidance we reviewed earlier.
Native system-role support exists, so we should not collapse the system prompt
into the user prompt just because older Gemma-family docs required that.

### Multimodal ordering

Gemma 4 guidance explicitly favors image-before-text multimodal ordering. Our
current Ollama interface handles images as a separate field on the user
message, so this becomes something to watch in the first baseline run rather
than a reason to rewrite prompt text now.

### Thinking mode

Gemma 4 supports a thinking mode, but that is not part of the first bootstrap.
The first clean question is:

- can Gemma 4 E4B reproduce the current BDA workflow and output contract with a
  semantic port of the active Qwen stack?

### Output formatting discipline

We should explicitly record in the first Gemma `v000` critique:

- whether detection JSON is cleaner or messier than Qwen
- whether assessment JSON is cleaner or messier than Qwen
- whether scene-summary wording drifts differently than Qwen

## Size Decision For The Bootstrap

### Active

- `gemma4:e4b`

### Comparison Only

- `gemma4:e2b`

### Not Active Yet

- `gemma4:26b`
- `gemma4:31b`

## Working Rule

Preserve the Qwen `v009` workflow shape first and treat Gemma differences as
explicit variables, not background assumptions.
