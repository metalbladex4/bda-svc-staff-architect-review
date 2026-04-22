# Preserve / Adapt / Exclude Matrix

This matrix records what should survive unchanged, what should be rewritten for
prompt/runtime fit, and what should remain out of scope.

## Preserve

| Source Concept | Keep? | Why |
| --- | --- | --- |
| Building PDA category set (`NO DAMAGE` through `DESTROYED`) | Preserve | Already correct and runtime-compatible |
| Building percentage thresholds | Preserve | Directly aligned with the doctrine sources |
| Framed-building versus load-bearing distinction | Preserve | Important to correct building-severity interpretation |
| Multistory / wing / section reporting concept | Preserve | Needed for complex-building reasoning |
| Military-equipment PDA category set (`NO DAMAGE`, `DAMAGED`, `DESTROYED`) | Preserve | Correct for Phase-1 PDA |
| Military-equipment target-family list | Preserve | Helps keep the doctrinal category boundary stable |

## Adapt

| Source Concept | Adapt How | Why |
| --- | --- | --- |
| Building multistory / wing reporting | Rewrite for selected-target scenes and crops | The live runtime assesses one selected target body at a time |
| Building considerations | Add explicit visible-only framing | Keep the model from drifting into interior or functional inference |
| Military-equipment `DESTROYED` language | Remove `K-kill` shorthand | Current prompts explicitly reject kill-state labels in outputs |
| Military-equipment considerations | Rewrite around visible exterior evidence only | The runtime is Phase-1 visual-only |
| Detection guidance | Keep mostly stable, but label it as operational guidance rather than pure doctrine | It is useful, but it is not the same thing as PDA doctrine |
| Quantity-reporting note for equipment | Move out of prompt-facing doctrine and into experiment notes | The runtime already counts targets from detections and summaries |

## Exclude

| Source Concept | Why It Stays Out |
| --- | --- |
| FDA definitions | Out of Phase-1 scope for this runtime |
| Recuperation time | Not available from the current visual-only prompt loop |
| Target assessment / target system assessment | Too broad for current output contract |
| Reattack recommendation logic | Operational decision support, not Phase-1 PDA |
| MEA | Separate assessment component |
| All-source cues like inactivity, lack of emissions, or radio silence | Invalid in a visual-only runtime |
| Internal equipment damage inferred from exterior damage alone | Not reliably visible in current imagery |

## Decision Rule

If a doctrine sentence requires:

- non-imagery data
- time-based inference
- functional assessment
- or commander-level campaign interpretation

it should not go into the first runtime candidate doctrine file.
