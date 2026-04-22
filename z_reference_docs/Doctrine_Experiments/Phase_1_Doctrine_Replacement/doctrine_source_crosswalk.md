# Doctrine Source Crosswalk

This note maps the current live `doctrine.yaml` against the BDA source set in
`z_reference_docs/BDAs/` with Phase-1 PDA scope in mind.

## Source Priority Used For This Audit

1. `CJCSI 3162.02A METHODOLOGY FOR COMBAT ASSESSMENT July 2021.md`
2. `Methodology For Combat Assessment.md`
3. `jp3_60 Joint Targeting.md`
4. `ARN39048-FM_3-60 Army Targetting.md`
5. `Fusing Data Into a BDA for the Commander.md`

Why this order:

- the CJCSI / methodology texts provide the most directly usable PDA
  definitions and target-specific considerations
- JP 3-60 and FM 3-60 provide framing for BDA and combat assessment
- the CALL article helps explain what doctrine often fails to translate into a
  usable reporting workflow

## Crosswalk

| Runtime Section | Current Fit | Main Source Basis | What It Does Well | Main Gap |
| --- | --- | --- | --- | --- |
| `buildings.physical_damage_definitions` | Strong | CJCSI 3162.02A, Methodology appendix on buildings | Preserves the five PDA bands almost directly | Needs slightly cleaner wording for prompt consumption |
| `buildings.physical_damage_considerations` | Moderate-to-strong | CJCSI 3162.02A / Methodology building notes 1–4 | Preserves framed vs load-bearing and multistory/wing logic | Does not explicitly translate section-versus-whole-building logic into a visual-only selected-target workflow |
| `military_equipment.physical_damage_definitions` | Moderate-to-strong | CJCSI 3162.02A / Methodology military-equipment PDA definitions | Preserves the three-label PDA set | Keeps `K-kill` language that conflicts with the current prompt discipline |
| `military_equipment.physical_damage_considerations` | Partial | CJCSI 3162.02A / Methodology military-equipment notes | Preserves useful target-family scope | Includes all-source and non-visual reasoning that should not sit in a Phase-1 visual-only runtime doctrine block |
| `buildings.detection_guidance` | Prompt heuristic, not doctrine | No direct doctrine equivalent | Practical for current runtime selectivity | Not traceable as straight doctrine; should be treated as operational guidance, not doctrinal PDA meaning |
| `military_equipment.detection_guidance` | Prompt heuristic built from doctrine categories | Target-family lists in CJCSI / Methodology | Useful category compression for detection | Still a prompt-operational layer, not pure doctrine text |

## Key Findings

### What the live doctrine already captures well

- The building PDA percentage bands are already aligned with the methodology.
- The framed-building versus load-bearing distinction is already present.
- The multistory / wing reporting concept is already present.
- The military-equipment PDA label set is already correct for Phase-1 physical
  damage.
- The military-equipment family list is already grounded in the methodology.

### What the live doctrine captures only partially

- The building notes assume a reporting context broader than a single selected
  target crop; they need translation into a per-target visual workflow.
- The military-equipment notes include analytical cues that are doctrinally
  valid in all-source BDA but not valid in this runtime.
- The live file does not explain the line between:
  - target-element PDA meaning
  - broader BDA / FDA / target assessment
- The current runtime relies on prompts for confidence semantics; the doctrine
  file does not explicitly carry that part of the doctrinal picture.

### What the live doctrine should not try to carry in prompt-facing form

- recuperation assessments
- target-system assessment
- reattack logic
- MEA
- non-imagery confidence support
- functional damage determination

## Practical Conclusion

The current doctrine file should be treated as:

- a **usable PDA seed**
- not a complete doctrinal representation
- and not yet the best prompt-facing translation of Phase-1 doctrine

That means the right next step is a **prompt-compatible Phase-1 rewrite**, not a
full doctrinal transplant.
