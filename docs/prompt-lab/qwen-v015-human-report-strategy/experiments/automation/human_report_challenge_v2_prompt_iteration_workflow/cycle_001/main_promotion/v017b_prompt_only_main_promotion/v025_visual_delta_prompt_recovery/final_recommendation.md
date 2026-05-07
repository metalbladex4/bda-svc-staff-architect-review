# v025 Final Recommendation

Review timestamp: `2026-05-07T00:05:56Z`

## Status

The first-pass static visual delta review is complete for the priority slice.
This package remains evidence-only and has no promotion recommendation.

## Current Recommendation

- Keep `v020c_anchor_replay` / `v020c_extra_box_audit` as the Qwen incumbent.
- Treat `v024l_v023s_no_wheel_track_ablation` as high-recall learning evidence
  only.
- Do not use `v024o` unless it is rerun from scratch.
- Do not author `v025a` until the user explicitly approves prompt authoring.

## Visual Review Finding

`v024l` recovered useful recall by splitting separate visible target bodies that
`v020c` sometimes merged:

- lower smoke-obscured tank in `14`
- right towed tank in `42`
- left building and destroyed red vehicle in `172`

But `v024l` added diverse false positives:

- adjacent building slivers in `12`, `77`, and `90`
- intact background objects in `16` and `88`
- dense-row nested vehicle fragments in `66`
- extra facade/roof/building-piece boxes in `97` and `103`

Because those FPs are diverse, `v024l` should not be used as the next base
prompt.

## Next Action

If prompt authoring is later approved, branch from `v020c`, not `v024l`.

Recommended later axis:

```text
v025a_v020c_compact_separate_body_recovery
```

Intent:

- preserve `v020c` FP discipline
- import only a compact `v024l` lesson about separate visible target bodies
- avoid broad building-only cleanup wording
- preserve case `67`, positive controls `155` and `166`, and office-negative

FiftyOne is not needed before that next step. Static overlays/crops were enough
for this first pass. Use FiftyOne later only if the review expands beyond the
priority slice or if static patch browsing becomes too slow.

## Boundary

No source truth, doctrine, assessment prompt, runtime code, eval ground truth,
Graphify refresh, Mem0 write, prompt authoring, or promotion is adopted by this
package.
