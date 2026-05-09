# v037b Diagnosis

What did this candidate test? A narrower containment-only same-wreck duplicate guard after v037a's broader wording reopened FPs.

What changed from current FP8 working best? One BAD FINAL BOX line was added from v034a: `second smaller box entirely inside another box for the same connected wreck/body`.

Result: runtime invalid. Case 110 failed all three attempts with a vLLM BadRequestError because the request reached 4097 input tokens against a 4096-token context cap.

Lesson: the FP8 vLLM surface remains mechanically stable, but prompt-length margin is thin on case 110. Longer clauses are risky even before semantic quality is evaluated.
