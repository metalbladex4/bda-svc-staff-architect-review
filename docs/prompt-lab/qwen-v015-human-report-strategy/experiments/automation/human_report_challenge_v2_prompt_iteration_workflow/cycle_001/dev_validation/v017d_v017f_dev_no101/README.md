# v017d/v017f Dev Validation, No 101

Status: `bounded_dev_validation_complete`

This package validates whether `v017d_visual_anchor_lock` generalizes beyond the
active hinge pack. `v017f_compact_visual_anchor_balance` is run only as a
comparator because it is the recall-oriented alternate from the completed
v017c-v017f hinge cycle.

## Scope

- Active manifest: `validation_manifests/human_report_challenge_v2_dev_55_no101.yaml`
- Source manifest: `/home/williambenitez1/Capstone_worktrees/1.2_feat__qwen3-vl-8b-instruct__two-pass-refinement/docs/prompt-lab/qwen-v015-human-report-strategy/experiments/source_refresh/human_report_challenge_v2_refresh/validation_manifests/human_report_challenge_v2_v015e_dev.yaml`
- Case count: `55`
- Excluded from forward evaluation: `101`
- Holdout-only and absent: `166`
- Positive control retained: `155`

## Candidate Roles

- `v017d`: primary candidate to test for dev generalization.
- `v017f`: validation comparator only.

## Baselines

See `baselines/dev55_no101_baselines.json` for v009, v014, and v015e totals
recomputed on the same 55-case no-101 split.

## Results

| Candidate/baseline | Matches | FNs | FPs | Positive `155` |
| --- | ---: | ---: | ---: | ---: |
| `v009 adjusted baseline` | `74` | `32` | `27` | `n/a` |
| `v014 adjusted baseline` | `69` | `37` | `17` | `n/a` |
| `v015e dev baseline` | `59` | `47` | `18` | `n/a` |
| `v017d primary` | `72` | `34` | `16` | `2` matches |
| `v017f comparator` | `73` | `33` | `18` | `2` matches |

`v017d_visual_anchor_lock` remains the primary balanced candidate. It improves
on the v014 adjusted dev-no101 baseline on matches, false negatives, and false
positives. `v017f_compact_visual_anchor_balance` has a small recall advantage
over `v017d`, but exceeds the v014 false-positive baseline.

Decision packet: `dev_validation_decision_packet.md`

Focused visual review: `visual_review/`

## Boundaries

This package does not authorize holdout, all-112/all-current runs, promotion,
runtime config adoption, source-truth mutation, structural guards, or prompt
authoring beyond the already existing v017d/v017f overlays.
