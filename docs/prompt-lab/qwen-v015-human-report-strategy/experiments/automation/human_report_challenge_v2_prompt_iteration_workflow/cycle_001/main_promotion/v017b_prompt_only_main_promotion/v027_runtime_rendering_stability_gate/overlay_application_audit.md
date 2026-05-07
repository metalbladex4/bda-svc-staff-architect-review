# v027 Overlay Application Audit

Overlay application records are generated per probe and summarized here by the
runner.

## Stage 1 Summary

Every Stage 1 probe reported:

- `overlay_actually_applied: true`
- an empty diff between intended overlay prompt text and scratch-config
  `prompts.detect_objects`
- no product config, doctrine, assessment prompt, runtime code, or eval-truth
  mutation

Exact v020c/no-op probes had rendered prompt hash
`0587223980d60833ca82c1458f3c878aebf7c66f2f470a260175dda4d77ae80b`.

Blank-line probes had rendered prompt hash
`6fbf853dfef7bf71f84e826194160bf27edac9b1c73d972d335b2d84b25a5926`.

The trailing-space probe had rendered prompt hash
`cc40f0dbeb7d8489e8e0cb709eb51124415ffe56a9d1823f5e4e101908142dbd`.

No overlay-application failure explains the case `67` collapse.
