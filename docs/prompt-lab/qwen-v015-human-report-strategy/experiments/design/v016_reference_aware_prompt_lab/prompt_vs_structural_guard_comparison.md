# Prompt Redesign vs Future Structural Guards

Status: `comparison_only_no_guard_implementation`

The next approved direction remains prompt engineering. This comparison records
why v016 should redesign the prompt-lab interface first, while keeping
deterministic structural guards as a future, separate scope.

## Prompt Redesign: v016

The selected prompt direction is
`reference_aware_candidate_discovery_with_evidence_budget`.

What it changes:

- The prompt-lab method becomes reference-aware before prompt authoring.
- Dense recall and precision rebound are treated as separate failure modes.
- Candidate discovery is separated from final detection acceptance.
- Final detections must survive an evidence filter inside the prompt
  interface.
- Case `101` is treated as a manual diagnostic with reference-shape caveats,
  not as a simple metric target.

Why this is still prompt engineering:

- The intervention is in prompt design, prompt interface, rubric structure, and
  prompt constraints.
- It does not add deterministic post-model code.
- It does not mutate source truth.
- It does not alter runtime config or promotion policy.

Risks:

- The model may still under-detect dense scenes if the evidence filter is too
  conservative.
- It may still hallucinate extras if candidate discovery is too permissive.
- It may not fully solve broad group boxes without downstream enforcement.

Why it is the right next lane:

- v015e showed that precision can be preserved, but recall did not generalize.
- v015a through v015e show that wording changes around individual bodies are
  not enough.
- The next prompt attempt needs a better design interface, not just another
  tighter sentence.

## Structural Guard: Future Scope

A non-prompt structural guard would be deterministic post-model rejection or
correction of output shapes such as:

- broad group or scene boxes
- row-fragment enumeration
- tiny ambiguous context boxes
- impossible duplicate or malformed output shapes

This is not implemented here.

The offline v015 structural guard simulator showed why this must remain future
scope. It could suppress broad/row outputs, but it was too blunt:

| Candidate | Raw matches/FNs/FPs | Guarded matches/FNs/FPs | Read |
| --- | --- | --- | --- |
| `v015a` | 13 / 10 / 15 | 6 / 17 / 3 | FP reduced, recall damaged. |
| `v015b` | 11 / 12 / 30 | 4 / 19 / 2 | FP reduced, recall damaged. |
| `v015c` | 11 / 12 / 29 | 4 / 19 / 1 | FP reduced, recall damaged. |
| `v015d` | 8 / 15 / 0 | 3 / 20 / 0 | Even zero-FP output lost recall. |

Structural guard risks:

- It changes system behavior beyond prompt text.
- It can delete valid recall along with invalid boxes.
- It needs its own approval, validation, and promotion path.
- It must be tested against source truth and visual review, not only aggregate
  metrics.

## Decision

Do v016 prompt-lab redesign first. Keep structural guards as a named future
discussion only. If v016 cannot recover recall without precision rebound, a
later wave can revisit a more selective structural guard, but that would be a
different scope from the current prompting lane.
