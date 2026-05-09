# v037c Diagnosis

What did this candidate test? An ultra-short same-wreck duplicate cue intended to avoid v037b's context overflow.

What changed from current FP8 working best? One BAD FINAL BOX line was added from v034a: `inner duplicate of the same wreck/body`.

Micro-pack result: `43/13/17/30`.

What improved? Runtime recovered and case 110 stayed controlled at `3/4/1`.

What regressed? Case 66 worsened to `8/0/6`, causing micro-gate failure. Case 155 stayed at `2/0/1`, so the intended local duplicate benefit did not appear.

Lesson: very short same-wreck wording is runtime-safe but not enough to isolate the case-155 duplicate class.
