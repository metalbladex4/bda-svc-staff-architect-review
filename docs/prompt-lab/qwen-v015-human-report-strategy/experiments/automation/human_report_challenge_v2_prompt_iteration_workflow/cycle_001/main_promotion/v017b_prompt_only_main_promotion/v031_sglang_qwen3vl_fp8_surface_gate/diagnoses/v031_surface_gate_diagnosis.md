# v031 Surface Gate Diagnosis

What was tested: official `Qwen/Qwen3-VL-8B-Instruct-FP8` as a potentially stable and behaviorally closer Qwen surface for prompt optimization.

SGLang result: launch succeeded after isolated dependency repairs, but the model surface produced `0/11/1` on case 67 for all exact/no-op/shape probes. That is stable failure, not prompt evidence.

vLLM result: launch succeeded, case 67 exact replays were stable at `10/1/2`, blank-line stayed within gate at `8/3/5`, trailing-space/no-op stayed `10/1/2`, and sentinel probes passed. The surface then failed the full baseline acceptance gate at `180/39/32/71`.

Failure class: behaviorally unacceptable model surface, not backend nondeterminism and not prompt-candidate failure.

Load-bearing evidence: old v020c is `186/33/25/58`; v031 vLLM FP8 is `180/39/32/71`; case 155 reopened from old `2/0/0` to `2/0/2`.

Next hypothesis: do not continue prompt mutation on this surface. Either find a closer acceptable official Qwen serving path, or explicitly scope FP8 as a new model line with its own baseline and target.
