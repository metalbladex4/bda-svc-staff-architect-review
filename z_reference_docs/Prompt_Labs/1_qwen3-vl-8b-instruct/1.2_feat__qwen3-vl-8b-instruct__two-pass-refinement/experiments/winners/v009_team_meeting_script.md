# `v009` Team Meeting Script

## One-Sentence Bottom Line

We now have a tracked feature-branch working config that performs more consistently
than the clean `origin/main` baseline across tanks, buildings, trucks, and
negative scenes, and the result is supported by repeated runs rather than a
single good-looking example.

## 30-Second Version

We built the current candidate by taking the best confirmed prompt surfaces
from three separate cycles and unifying them into `v009`. We then checked it
against the clean `origin/main` baseline on focused cases, extra hard cases,
and a 10-image blind-style sweep. The strongest result is not “every image got
dramatically better,” but that recall stayed stable, negative scenes stayed
clean, and the prompt behavior generalized across multiple target classes
instead of only looking good on the original tank image.

## 90-Second Version

Our current candidate is `v009`, which combines:

- `detect_objects` from `v006`
- `assess_damage` from `v008`
- `summarize_scene` from `v004`

We did not treat that as a paper combination only. We ran it directly and
validated it in layers:

1. Focused confirmation
   - `v009` matched the expected inherited behavior on:
     - `tank_pressure`
     - `operational_tank4`
     - `destroyed_building4`
2. Additional hard cases
   - preserved three-building recall on a new multi-object scene
   - did not regress on a smoke/fire truck case
   - preserved building separation in a cluttered complex scene
3. 10-image blind-style comparison against the clean `origin/main` baseline
   - `10 / 10` preserved target-count recall
   - `6 / 10` preserved the same damage/confidence structure
   - only `2 / 10` changed damage category at all

So the honest claim is that this is a real stability and generalization
improvement, not just a quick prompt mockup.

## Strongest Points To Emphasize

- We preserved recall across all 10 blind-sweep images.
- We fixed earlier regressions on:
  - `destroyed_building4` target separation
  - `operational_tank4` false damage
  - office negative behavior
- The winner stack is now preserved in tracked branch history, not only in
  local lab notes.

## Caveats To Say Out Loud

Two cases should stay visible so we do not overclaim:

- `destroyed_building5`
  - likely a real `v009` building-severity overcall
- `destroyed_tank37`
  - `v009` localizes the target more cleanly
  - the cautious `DAMAGED` call is arguable under smoke/angle obscuration
  - but the current supporting logic is still too catastrophic for a clean
    `DAMAGED` read

These are category-calibration watch cases, not recall failures.

## If Someone Asks “How Is This Different From The Baseline?”

Say:

- the baseline from `origin/main` was used directly as the comparison point
- the current stack is stronger mainly in:
  - recall discipline
  - negative-scene discipline
  - multi-target separation
  - cross-image stability
- the improvement is more about reliable behavior across image types than about
  dramatic wins on every single image

## If Someone Asks “Is This In The Repo Yet?”

Say:

- yes, on the feature branch
- pushed to `origin/feat/qwen3-vl-8b-instruct/two-pass-refinement`
- preserved in tracked branch history:
  - `566892a` — `Add prompt-lab review artifacts to bda_eval`
  - `127051a` — `Promote v009 prompt stack into pipeline config`
  - `ebeae30` — `Install workspace packages in CI`

## Suggested Closing

My recommendation is to treat `v009` as the active working config for this
model line. It has enough evidence to justify that role, while the remaining
risk is narrow enough to describe clearly and watch deliberately.
