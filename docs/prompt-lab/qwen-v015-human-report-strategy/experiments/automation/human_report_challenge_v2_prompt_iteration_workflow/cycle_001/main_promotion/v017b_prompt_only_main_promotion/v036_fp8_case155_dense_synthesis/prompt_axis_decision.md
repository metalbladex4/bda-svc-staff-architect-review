# Prompt Axis Decision

Decision: **B**. Try a local case-155 FP guard that does not mention dense scenes, partial fragments, or uncertain fragments.

Do **not** author the prompt in v036. The synthesis identifies a plausible low-risk axis, but v035a showed enough case-67 sensitivity that the next candidate should be launched as a separate prompt tranche after review.

Candidate axis for the next tranche: base from v034a; preserve the v034a broad-context/scene-box guard and the v020c extra-box audit; add at most one compact BAD FINAL BOX clause rejecting a smaller duplicate box inside the same visible wreck already covered by a whole-vehicle box.
