# Winners

Copy only accepted prompt or method revisions here after they pass:

- the relevant eval tracks
- manual doctrinal review
- bbox/localization review when detection changes are involved

Until a version clears those checks, keep it in `experiments/versions/` and log
the outcome in `experiments/prompt_version_log.md`.

Current winner:

- `v009_unified_best-stack`
- see `v009_current_best_stack.md`

Current promoted branch state:

- the `v009` stack is now promoted into the tracked feature-branch
  `src/bda_svc/pipeline/config.yaml`
- the `v009` stack should now be treated as the active working config for this
  model line going forward
- the supporting review-artifact workflow in `bda_eval` is also preserved in
  tracked branch history
- the preserved commits for that branch-ready state are:
  - `566892a` — `Add prompt-lab review artifacts to bda_eval`
  - `127051a` — `Promote v009 prompt stack into pipeline config`
  - `ebeae30` — `Install workspace packages in CI`
- the feature branch is pushed to
  `origin/feat/qwen3-vl-8b-instruct/two-pass-refinement`
- PR `#134` is now open against `upstream/main`
- GitHub CI is green, but that green state should be read as branch-health
  validation rather than exact prompt-lab parity validation
