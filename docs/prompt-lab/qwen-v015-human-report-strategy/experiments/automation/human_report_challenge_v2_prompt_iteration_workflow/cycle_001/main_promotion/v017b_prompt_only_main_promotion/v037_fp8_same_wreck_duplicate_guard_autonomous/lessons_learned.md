# v037 Lessons Learned

- v034a remains the FP8 working best at `181 / 38 / 25 / 63`.
- v037a isolated the case-155 same-wreck duplicate (`2/0/0`) but reopened broad FPs, especially case 110 (`2/5/16`).
- v037b proved the vLLM FP8 4096-token context cap is still a practical prompt-length constraint; case 110 reached 4097 input tokens.
- v037c showed that an ultra-short same-wreck duplicate cue can avoid runtime failure, but it did not improve case 155 and still worsened case 66.
- v037d showed a tiny recall cue can improve case 155, but it did not recover case 84 and worsened cases 66/67.
- The same-wreck duplicate benefit is real but appears better tested through post-processing or visual/eval simulation than another prompt clause.
- Do not reuse v037a/v037d wording families unless a non-prompt simulation proves the dense-row risk can be separated.
